from sqlalchemy import Column, String, Float, Integer, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100))
    avatar_url = Column(String(500))
    weight_kg = Column(Float, default=70.0)

    # Stats
    total_distance_km = Column(Float, default=0.0)
    total_duration_seconds = Column(Integer, default=0)
    total_runs = Column(Integer, default=0)
    avg_pace = Column(Float, default=0.0)

    # Rankings
    elo_rating = Column(Integer, default=1200)
    league_tier = Column(String(20), default='Bronze')
    league_points = Column(Integer, default=0)

    # Integrations
    strava_access_token = Column(String(255))
    strava_refresh_token = Column(String(255))
    strava_athlete_id = Column(String(50))

    # Premium
    is_premium = Column(Boolean, default=False)
    premium_expires_at = Column(DateTime, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login_at = Column(DateTime)

    # Relationships
    runs = relationship("Run", back_populates="user", cascade="all, delete-orphan")
    battles_as_user1 = relationship("Battle", foreign_keys="Battle.user1_id", back_populates="user1")
    battles_as_user2 = relationship("Battle", foreign_keys="Battle.user2_id", back_populates="user2")
