from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from app.database import Base

class Battle(Base):
    __tablename__ = "battles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Participants
    user1_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    user2_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    # Battle config
    distance_km = Column(Float, nullable=False)

    # Results
    winner_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    user1_distance = Column(Float, default=0.0)
    user2_distance = Column(Float, default=0.0)
    user1_time = Column(Integer, default=0)  # seconds
    user2_time = Column(Integer, default=0)  # seconds
    user1_pace = Column(Float, default=0.0)
    user2_pace = Column(Float, default=0.0)

    # ELO changes
    user1_elo_before = Column(Integer)
    user2_elo_before = Column(Integer)
    user1_elo_after = Column(Integer)
    user2_elo_after = Column(Integer)

    # Status: 'pending', 'active', 'completed', 'cancelled'
    status = Column(String(20), default='pending')

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)

    # Relationships
    user1 = relationship("User", foreign_keys=[user1_id], back_populates="battles_as_user1")
    user2 = relationship("User", foreign_keys=[user2_id], back_populates="battles_as_user2")
    winner = relationship("User", foreign_keys=[winner_id])
