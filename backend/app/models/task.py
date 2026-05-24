from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .base import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(512), nullable=False)
    description = Column(Text)
    agent_type = Column(String(100), nullable=False, index=True)
    priority = Column(Integer, server_default="3")
    status = Column(String(50), server_default="pending", index=True)
    source = Column(String(100), server_default="orchestrator")
    scheduled_date = Column(DateTime(timezone=True))
    result_summary = Column(Text)
    error_message = Column(Text)
    metadata_json = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    agent_runs = relationship("AgentRun", back_populates="task")
