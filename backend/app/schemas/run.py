from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class RoutePoint(BaseModel):
    lat: float
    lng: float

class RunCreate(BaseModel):
    distance_km: float
    duration_seconds: int
    avg_pace: float
    avg_speed: float
    route: List[RoutePoint]
    start_time: datetime
    end_time: datetime
    calories_burned: Optional[float] = 0.0

class RunResponse(BaseModel):
    id: str
    user_id: str
    distance_km: float
    duration_seconds: int
    avg_pace: float
    avg_speed: float
    calories_burned: float
    started_at: datetime
    completed_at: datetime
    source: str

    class Config:
        from_attributes = True
