from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from app.database import Base

class Run(Base):
    __tablename__ = "runs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    # Metrics
    distance_km = Column(Float, nullable=False)
    duration_seconds = Column(Integer, nullable=False)
    avg_pace = Column(Float, nullable=False)  # min/km
    avg_speed = Column(Float, nullable=False)  # km/h
    calories_burned = Column(Float, default=0.0)

    # Route data (encoded polyline string)
    route_polyline = Column(Text)
    start_lat = Column(Float)
    start_lng = Column(Float)
    end_lat = Column(Float)
    end_lng = Column(Float)

    # Timestamps
    started_at = Column(DateTime, nullable=False)
    completed_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Source
    source = Column(String(20), default='app')  # 'app', 'strava', 'nike'
    external_id = Column(String(100))  # ID from external source

    # Relationship
    user = relationship("User", back_populates="runs")
