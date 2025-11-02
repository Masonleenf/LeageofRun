from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class BattleCreate(BaseModel):
    """Request to create/find a battle"""
    distance_km: float = 5.0  # Default 5km battle


class BattleStart(BaseModel):
    """Request to start a pending battle"""
    pass


class BattleComplete(BaseModel):
    """Request to complete a battle with results"""
    distance_km: float
    duration_seconds: int


class BattleResponse(BaseModel):
    """Battle response with all details"""
    id: str
    user1_id: str
    user2_id: str
    distance_km: float

    # Results
    winner_id: Optional[str] = None
    user1_distance: float = 0.0
    user2_distance: float = 0.0
    user1_time: int = 0
    user2_time: int = 0
    user1_pace: float = 0.0
    user2_pace: float = 0.0

    # ELO
    user1_elo_before: Optional[int] = None
    user2_elo_before: Optional[int] = None
    user1_elo_after: Optional[int] = None
    user2_elo_after: Optional[int] = None

    # Status
    status: str
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class BattleWithUsers(BattleResponse):
    """Battle response with user information"""
    user1_username: Optional[str] = None
    user2_username: Optional[str] = None
    user1_avatar: Optional[str] = None
    user2_avatar: Optional[str] = None
