from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Boolean, Text, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from app.database import Base

class Crew(Base):
    __tablename__ = "crews"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    avatar_url = Column(String(500))

    captain_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    # Stats
    total_members = Column(Integer, default=0)
    total_distance_km = Column(Float, default=0.0)
    total_runs = Column(Integer, default=0)
    battle_wins = Column(Integer, default=0)
    battle_losses = Column(Integer, default=0)

    # Settings
    is_public = Column(Boolean, default=True)
    max_members = Column(Integer, default=50)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    captain = relationship("User")
    members = relationship("CrewMembership", back_populates="crew", cascade="all, delete-orphan")


class CrewMembership(Base):
    __tablename__ = "crew_memberships"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    crew_id = Column(UUID(as_uuid=True), ForeignKey('crews.id', ondelete='CASCADE'), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    role = Column(String(20), default='member')  # 'captain', 'admin', 'member'

    joined_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    crew = relationship("Crew", back_populates="members")
    user = relationship("User")
