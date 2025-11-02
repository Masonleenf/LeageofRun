"""
Battle endpoints for 1v1 competitions
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.database import get_db
from app.schemas.battle import (
    BattleCreate,
    BattleResponse,
    BattleStart,
    BattleComplete,
    BattleWithUsers
)
from app.models.battle import Battle
from app.models.user import User
from app.api.deps import get_current_user
from app.services.matchmaking import MatchmakingService

router = APIRouter(prefix="/battles", tags=["Battles"])


@router.post("/matchmaking", response_model=BattleResponse, status_code=status.HTTP_201_CREATED)
async def find_match(
    battle_data: BattleCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Find an opponent and create a battle

    - Matches users with similar ELO ratings
    - Creates a pending battle
    """
    # Check if user is already in an active battle
    existing_battle = db.query(Battle).filter(
        (
            (Battle.user1_id == current_user.id) |
            (Battle.user2_id == current_user.id)
        ),
        (
            (Battle.status == 'pending') |
            (Battle.status == 'active')
        )
    ).first()

    if existing_battle:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You are already in an active battle"
        )

    # Find opponent
    opponent = MatchmakingService.find_opponent(current_user, db)

    if not opponent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No suitable opponent found. Please try again later."
        )

    # Create battle
    battle = MatchmakingService.create_battle(
        user1=current_user,
        user2=opponent,
        distance_km=battle_data.distance_km,
        db=db
    )

    return BattleResponse.from_orm(battle)


@router.post("/{battle_id}/start", response_model=BattleResponse)
async def start_battle(
    battle_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Start a pending battle

    - Both users must be ready
    - Changes status from 'pending' to 'active'
    """
    battle = db.query(Battle).filter(Battle.id == battle_id).first()

    if not battle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Battle not found"
        )

    # Check if user is part of this battle
    if battle.user1_id != current_user.id and battle.user2_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not part of this battle"
        )

    if battle.status != 'pending':
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Battle is already {battle.status}"
        )

    # Start the battle
    battle.status = 'active'
    battle.started_at = datetime.utcnow()

    db.commit()
    db.refresh(battle)

    return BattleResponse.from_orm(battle)


@router.post("/{battle_id}/complete", response_model=BattleResponse)
async def complete_battle(
    battle_id: str,
    result_data: BattleComplete,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Complete a battle and submit results

    - Updates battle with user's performance
    - Calculates winner when both users complete
    - Updates ELO ratings
    """
    battle = db.query(Battle).filter(Battle.id == battle_id).first()

    if not battle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Battle not found"
        )

    # Check if user is part of this battle
    if battle.user1_id != current_user.id and battle.user2_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not part of this battle"
        )

    if battle.status == 'completed':
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Battle is already completed"
        )

    # Update user's results
    if battle.user1_id == current_user.id:
        battle.user1_distance = result_data.distance_km
        battle.user1_time = result_data.duration_seconds
        if result_data.distance_km > 0:
            battle.user1_pace = (result_data.duration_seconds / 60) / result_data.distance_km
    else:
        battle.user2_distance = result_data.distance_km
        battle.user2_time = result_data.duration_seconds
        if result_data.distance_km > 0:
            battle.user2_pace = (result_data.duration_seconds / 60) / result_data.distance_km

    # Check if both users have completed
    if battle.user1_distance > 0 and battle.user2_distance > 0:
        # Complete the battle
        battle = MatchmakingService.complete_battle(
            battle=battle,
            user1_distance=battle.user1_distance,
            user2_distance=battle.user2_distance,
            user1_time=battle.user1_time,
            user2_time=battle.user2_time,
            db=db
        )
    else:
        # Just save the results, waiting for the other user
        db.commit()
        db.refresh(battle)

    return BattleResponse.from_orm(battle)


@router.get("", response_model=List[BattleResponse])
async def get_user_battles(
    skip: int = 0,
    limit: int = 20,
    status_filter: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get user's battle history

    - Returns all battles (as user1 or user2)
    - Optional status filter (pending, active, completed, cancelled)
    """
    query = db.query(Battle).filter(
        (Battle.user1_id == current_user.id) |
        (Battle.user2_id == current_user.id)
    )

    if status_filter:
        query = query.filter(Battle.status == status_filter)

    battles = query.order_by(
        Battle.created_at.desc()
    ).offset(skip).limit(limit).all()

    return [BattleResponse.from_orm(battle) for battle in battles]


@router.get("/{battle_id}", response_model=BattleWithUsers)
async def get_battle_detail(
    battle_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get specific battle details with user information
    """
    battle = db.query(Battle).filter(Battle.id == battle_id).first()

    if not battle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Battle not found"
        )

    # Check if user is part of this battle or completed
    if battle.status != 'completed':
        if battle.user1_id != current_user.id and battle.user2_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not part of this battle"
            )

    # Get user information
    user1 = db.query(User).filter(User.id == battle.user1_id).first()
    user2 = db.query(User).filter(User.id == battle.user2_id).first()

    response_data = BattleResponse.from_orm(battle).model_dump()
    response_data['user1_username'] = user1.username if user1 else None
    response_data['user2_username'] = user2.username if user2 else None
    response_data['user1_avatar'] = user1.avatar_url if user1 else None
    response_data['user2_avatar'] = user2.avatar_url if user2 else None

    return BattleWithUsers(**response_data)


@router.delete("/{battle_id}", status_code=status.HTTP_204_NO_CONTENT)
async def cancel_battle(
    battle_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Cancel a pending or active battle

    - Only the participants can cancel
    - Cannot cancel completed battles
    """
    battle = db.query(Battle).filter(Battle.id == battle_id).first()

    if not battle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Battle not found"
        )

    # Check if user is part of this battle
    if battle.user1_id != current_user.id and battle.user2_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not part of this battle"
        )

    if battle.status == 'completed':
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot cancel completed battle"
        )

    battle.status = 'cancelled'
    db.commit()

    return None
