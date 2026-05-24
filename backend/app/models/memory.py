from sqlalchemy import Column, Integer, String, DateTime, Text, Float, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .base import Base


class MemoryEntry(Base):
    __tablename__ = "memory_entries"

    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(Integer, ForeignKey("agents.id"))
    category = Column(String(100), nullable=False, index=True)
    title = Column(String(512), nullable=False)
    content = Column(Text, nullable=False)
    source = Column(String(100))
    tags = Column(Text)
    importance_score = Column(Float, server_default="0")
    chroma_id = Column(String(255), unique=True)
    access_count = Column(Integer, server_default="0")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    agent = relationship("Agent")


class LearningEntry(Base):
    __tablename__ = "learning_entries"

    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(Integer, ForeignKey("agents.id"))
    trigger_event = Column(String(255), nullable=False)
    pattern_detected = Column(Text, nullable=False)
    action_taken = Column(Text)
    outcome = Column(Text)
    success_rating = Column(Float, server_default="0")
    tags = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    agent = relationship("Agent")
