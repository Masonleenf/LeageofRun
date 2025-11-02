from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CrewCreate(BaseModel):
    """Request to create a crew"""
    name: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = None
    is_public: bool = True
    max_members: int = Field(default=50, ge=2, le=100)


class CrewUpdate(BaseModel):
    """Request to update crew information"""
    description: Optional[str] = None
    is_public: Optional[bool] = None
    max_members: Optional[int] = Field(default=None, ge=2, le=100)


class CrewResponse(BaseModel):
    """Crew information response"""
    id: str
    name: str
    description: Optional[str]
    captain_id: str
    total_members: int
    total_distance_km: float = 0.0
    total_runs: int = 0
    is_public: bool
    max_members: int = 50
    created_at: datetime

    class Config:
        from_attributes = True


class CrewMemberResponse(BaseModel):
    """Crew member information"""
    user_id: str
    username: str
    avatar_url: Optional[str] = None
    role: str
    joined_at: datetime
    total_distance_km: float = 0.0
    total_runs: int = 0
