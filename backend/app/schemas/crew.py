from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CrewCreate(BaseModel):
    name: str
    description: Optional[str] = None
    is_public: bool = True
    max_members: int = 50

class CrewResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    captain_id: str
    total_members: int
    total_distance_km: float
    total_runs: int
    is_public: bool
    created_at: datetime

    class Config:
        from_attributes = True
