from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.database import get_db
from app.schemas.run import RunCreate, RunResponse
from app.models.run import Run
from app.models.user import User
from app.api.deps import get_current_user
from app.services.gps_calculator import GPSCalculator
import json

router = APIRouter(prefix="/runs", tags=["Runs"])

@router.post("", response_model=RunResponse, status_code=status.HTTP_201_CREATED)
async def create_run(
    run_data: RunCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Save a completed run"""
    # Calculate calories if not provided
    if run_data.calories_burned == 0:
        run_data.calories_burned = GPSCalculator.calculate_calories(
            run_data.distance_km,
            current_user.weight_kg
        )

    # Create route polyline (simplified - store as JSON string)
    route_polyline = json.dumps([{"lat": p.lat, "lng": p.lng} for p in run_data.route])

    # Create run
    new_run = Run(
        user_id=current_user.id,
        distance_km=run_data.distance_km,
        duration_seconds=run_data.duration_seconds,
        avg_pace=run_data.avg_pace,
        avg_speed=run_data.avg_speed,
        calories_burned=run_data.calories_burned,
        route_polyline=route_polyline,
        start_lat=run_data.route[0].lat if run_data.route else None,
        start_lng=run_data.route[0].lng if run_data.route else None,
        end_lat=run_data.route[-1].lat if run_data.route else None,
        end_lng=run_data.route[-1].lng if run_data.route else None,
        started_at=run_data.start_time,
        completed_at=run_data.end_time,
        source='app'
    )

    db.add(new_run)

    # Update user stats
    current_user.total_distance_km += run_data.distance_km
    current_user.total_duration_seconds += run_data.duration_seconds
    current_user.total_runs += 1

    # Recalculate average pace
    if current_user.total_distance_km > 0:
        current_user.avg_pace = (
            current_user.total_duration_seconds / 60
        ) / current_user.total_distance_km

    db.commit()
    db.refresh(new_run)

    return RunResponse.from_orm(new_run)

@router.get("", response_model=List[RunResponse])
async def get_user_runs(
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's run history"""
    runs = db.query(Run).filter(
        Run.user_id == current_user.id
    ).order_by(
        Run.completed_at.desc()
    ).offset(skip).limit(limit).all()

    return [RunResponse.from_orm(run) for run in runs]

@router.get("/{run_id}", response_model=RunResponse)
async def get_run_detail(
    run_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific run details"""
    run = db.query(Run).filter(
        Run.id == run_id,
        Run.user_id == current_user.id
    ).first()

    if not run:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Run not found"
        )

    return RunResponse.from_orm(run)
