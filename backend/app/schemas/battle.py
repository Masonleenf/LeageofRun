from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BattleCreate(BaseModel):
    distance_km: float

class BattleResponse(BaseModel):
    id: str
    user1_id: str
    user2_id: str
    distance_km: float
    winner_id: Optional[str]
    status: str
    created_at: datetime
    started_at: Optional[datetime]
    completed_at: Optional[datetime]

    class Config:
        from_attributes = True
