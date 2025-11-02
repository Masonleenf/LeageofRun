"""
Crew endpoints for team management
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.database import get_db
from app.schemas.crew import CrewCreate, CrewResponse, CrewUpdate, CrewMemberResponse
from app.models.crew import Crew, CrewMembership
from app.models.user import User
from app.api.deps import get_current_user

router = APIRouter(prefix="/crews", tags=["Crews"])


@router.post("", response_model=CrewResponse, status_code=status.HTTP_201_CREATED)
async def create_crew(
    crew_data: CrewCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new crew

    - User becomes the captain
    - Crew name must be unique
    """
    # Check if crew name already exists
    existing_crew = db.query(Crew).filter(Crew.name == crew_data.name).first()
    if existing_crew:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Crew name already taken"
        )

    # Check if user is already captain of another crew
    existing_captain = db.query(Crew).filter(Crew.captain_id == current_user.id).first()
    if existing_captain:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You are already a captain of another crew"
        )

    # Create crew
    new_crew = Crew(
        name=crew_data.name,
        description=crew_data.description,
        captain_id=current_user.id,
        is_public=crew_data.is_public,
        max_members=crew_data.max_members,
        total_members=1
    )

    db.add(new_crew)
    db.commit()
    db.refresh(new_crew)

    # Add captain as first member
    membership = CrewMembership(
        crew_id=new_crew.id,
        user_id=current_user.id,
        role='captain'
    )
    db.add(membership)
    db.commit()

    return CrewResponse.from_orm(new_crew)


@router.get("", response_model=List[CrewResponse])
async def get_crews(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """
    Get list of public crews

    - Only returns public crews
    - Ordered by total members
    """
    crews = db.query(Crew).filter(
        Crew.is_public == True
    ).order_by(
        Crew.total_members.desc()
    ).offset(skip).limit(limit).all()

    return [CrewResponse.from_orm(crew) for crew in crews]


@router.get("/{crew_id}", response_model=CrewResponse)
async def get_crew_detail(
    crew_id: str,
    db: Session = Depends(get_db)
):
    """Get specific crew details"""
    crew = db.query(Crew).filter(Crew.id == crew_id).first()

    if not crew:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Crew not found"
        )

    return CrewResponse.from_orm(crew)


@router.get("/{crew_id}/members", response_model=List[CrewMemberResponse])
async def get_crew_members(
    crew_id: str,
    db: Session = Depends(get_db)
):
    """Get all members of a crew"""
    crew = db.query(Crew).filter(Crew.id == crew_id).first()

    if not crew:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Crew not found"
        )

    memberships = db.query(CrewMembership).filter(
        CrewMembership.crew_id == crew_id
    ).all()

    members = []
    for membership in memberships:
        user = db.query(User).filter(User.id == membership.user_id).first()
        if user:
            members.append(CrewMemberResponse(
                user_id=str(user.id),
                username=user.username,
                avatar_url=user.avatar_url,
                role=membership.role,
                joined_at=membership.joined_at,
                total_distance_km=user.total_distance_km,
                total_runs=user.total_runs
            ))

    return members


@router.post("/{crew_id}/join", status_code=status.HTTP_200_OK)
async def join_crew(
    crew_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Join a crew

    - Crew must be public
    - User cannot be in multiple crews
    - Crew must not be full
    """
    crew = db.query(Crew).filter(Crew.id == crew_id).first()

    if not crew:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Crew not found"
        )

    if not crew.is_public:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This crew is private"
        )

    # Check if user is already in a crew
    existing_membership = db.query(CrewMembership).filter(
        CrewMembership.user_id == current_user.id
    ).first()

    if existing_membership:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You are already in a crew"
        )

    # Check if crew is full
    if crew.total_members >= crew.max_members:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Crew is full"
        )

    # Add member
    membership = CrewMembership(
        crew_id=crew.id,
        user_id=current_user.id,
        role='member'
    )
    db.add(membership)

    # Update crew member count
    crew.total_members += 1
    db.commit()

    return {"message": "Successfully joined crew"}


@router.delete("/{crew_id}/leave", status_code=status.HTTP_204_NO_CONTENT)
async def leave_crew(
    crew_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Leave a crew

    - Captain cannot leave (must transfer or delete crew)
    """
    membership = db.query(CrewMembership).filter(
        CrewMembership.crew_id == crew_id,
        CrewMembership.user_id == current_user.id
    ).first()

    if not membership:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="You are not a member of this crew"
        )

    if membership.role == 'captain':
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Captain cannot leave crew. Transfer ownership or delete crew."
        )

    # Remove member
    db.delete(membership)

    # Update crew member count
    crew = db.query(Crew).filter(Crew.id == crew_id).first()
    if crew:
        crew.total_members -= 1
        db.commit()

    return None


@router.put("/{crew_id}", response_model=CrewResponse)
async def update_crew(
    crew_id: str,
    crew_data: CrewUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update crew information

    - Only captain can update
    """
    crew = db.query(Crew).filter(Crew.id == crew_id).first()

    if not crew:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Crew not found"
        )

    if crew.captain_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the captain can update crew information"
        )

    # Update fields
    if crew_data.description is not None:
        crew.description = crew_data.description
    if crew_data.is_public is not None:
        crew.is_public = crew_data.is_public
    if crew_data.max_members is not None:
        crew.max_members = crew_data.max_members

    crew.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(crew)

    return CrewResponse.from_orm(crew)


@router.delete("/{crew_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_crew(
    crew_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a crew

    - Only captain can delete
    - All members will be removed
    """
    crew = db.query(Crew).filter(Crew.id == crew_id).first()

    if not crew:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Crew not found"
        )

    if crew.captain_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the captain can delete the crew"
        )

    # Delete crew (memberships will cascade delete)
    db.delete(crew)
    db.commit()

    return None


@router.get("/my/crew", response_model=CrewResponse)
async def get_my_crew(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get the crew that the current user belongs to"""
    membership = db.query(CrewMembership).filter(
        CrewMembership.user_id == current_user.id
    ).first()

    if not membership:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="You are not in any crew"
        )

    crew = db.query(Crew).filter(Crew.id == membership.crew_id).first()

    if not crew:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Crew not found"
        )

    return CrewResponse.from_orm(crew)
