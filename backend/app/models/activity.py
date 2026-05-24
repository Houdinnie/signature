from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from .base import Base


class ActivityLog(Base):
    __tablename__ = "activity_log"

    id = Column(Integer, primary_key=True, index=True)
    agent_type = Column(String(100), nullable=False, index=True)
    action = Column(String(255), nullable=False)
    summary = Column(Text, nullable=False)
    detail = Column(Text)
    level = Column(String(20), server_default="info")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
