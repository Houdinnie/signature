from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .base import Base


class WorkflowTemplate(Base):
    __tablename__ = "workflow_templates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    steps_json = Column(Text, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    instances = relationship("WorkflowInstance", back_populates="template")


class WorkflowInstance(Base):
    __tablename__ = "workflow_instances"

    id = Column(Integer, primary_key=True, index=True)
    template_id = Column(Integer, ForeignKey("workflow_templates.id"))
    name = Column(String(255), nullable=False)
    status = Column(String(50), server_default="pending")
    current_step = Column(Integer, server_default="0")
    total_steps = Column(Integer, server_default="0")
    context_json = Column(Text)
    result_json = Column(Text)
    error_message = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    completed_at = Column(DateTime(timezone=True))

    template = relationship("WorkflowTemplate", back_populates="instances")
    steps = relationship("WorkflowStep", back_populates="workflow")
    approvals = relationship("ApprovalRequest", back_populates="workflow")


class WorkflowStep(Base):
    __tablename__ = "workflow_steps"

    id = Column(Integer, primary_key=True, index=True)
    workflow_id = Column(Integer, ForeignKey("workflow_instances.id"), nullable=False)
    step_number = Column(Integer, nullable=False)
    name = Column(String(255), nullable=False)
    agent_type = Column(String(100), nullable=False)
    phase = Column(String(50), nullable=False)
    risk_level = Column(String(20), server_default="low")
    status = Column(String(50), server_default="pending")
    input_json = Column(Text)
    output_json = Column(Text)
    error_message = Column(Text)
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))

    workflow = relationship("WorkflowInstance", back_populates="steps")


class ApprovalRequest(Base):
    __tablename__ = "approval_requests"

    id = Column(Integer, primary_key=True, index=True)
    workflow_id = Column(Integer, ForeignKey("workflow_instances.id"))
    step_id = Column(Integer, ForeignKey("workflow_steps.id"))
    title = Column(String(512), nullable=False)
    description = Column(Text)
    level = Column(String(20), server_default="human")
    status = Column(String(20), server_default="pending")
    requested_by = Column(Integer, ForeignKey("agents.id"))
    approved_by = Column(Integer, ForeignKey("users.id"))
    context_json = Column(Text)
    response_message = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    responded_at = Column(DateTime(timezone=True))

    workflow = relationship("WorkflowInstance", back_populates="approvals")
