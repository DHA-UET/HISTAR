import datetime
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Technician(Base):
    __tablename__ = "technicians"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, index=True)
    target_index = Column(Integer, unique=True, index=True, nullable=False)
    campaign_name = Column(String, nullable=False)
    marker_image_url = Column(String, nullable=True)
    video_overlay_url = Column(String, nullable=True)
    chroma_threshold = Column(Float, default=0.4, nullable=False)
    key_color = Column(String, default="#00ff00", nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    logs = relationship("VisitorLog", back_populates="campaign", cascade="all, delete-orphan")

class VisitorLog(Base):
    __tablename__ = "visitor_logs"

    id = Column(Integer, primary_key=True, index=True)
    visitor_session_id = Column(String, index=True, nullable=False)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=False)
    scanned_at = Column(DateTime, default=datetime.datetime.utcnow)

    campaign = relationship("Campaign", back_populates="logs")
