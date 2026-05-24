from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .base import Base


class Agent(Base):
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    agent_type = Column(String(100), nullable=False)
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    status = Column(String(50), server_default="idle")
    config = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    runs = relationship("AgentRun", back_populates="agent")


class AgentRun(Base):
    __tablename__ = "agent_runs"

    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(Integer, ForeignKey("agents.id"), nullable=False)
    task_id = Column(Integer, ForeignKey("tasks.id"))
    agent_type = Column(String(100))
    run_type = Column(String(100), server_default="task")
    status = Column(String(50), server_default="running")
    input_data = Column(Text)
    output_data = Column(Text)
    error_message = Column(Text)
    tokens_used = Column(Integer)
    cost_usd = Column(Integer)
    duration_secs = Column(Integer)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True))

    agent = relationship("Agent", back_populates="runs")
    task = relationship("Task", back_populates="agent_runs")
