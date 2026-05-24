from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime
from ..models.agent import AgentType, AgentStatus

class AgentBase(BaseModel):
    name: str
    agent_type: AgentType
    description: Optional[str] = None
    is_active: bool = True
    config: Optional[Dict[str, Any]] = None

class AgentCreate(AgentBase):
    pass

class AgentUpdate(BaseModel):
    name: Optional[str] = None
    agent_type: Optional[AgentType] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    status: Optional[AgentStatus] = None
    config: Optional[Dict[str, Any]] = None

class AgentInDBBase(AgentBase):
    id: int
    status: AgentStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class AgentResponse(AgentInDBBase):
    pass

class AgentRunBase(BaseModel):
    agent_id: int
    status: AgentStatus
    input_data: Optional[Dict[str, Any]] = None
    output_data: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None

class AgentRunCreate(AgentRunBase):
    pass

class AgentRunUpdate(BaseModel):
    status: Optional[AgentStatus] = None
    input_data: Optional[Dict[str, Any]] = None
    output_data: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    completed_at: Optional[datetime] = None

class AgentRunInDBBase(AgentRunBase):
    id: int
    started_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class AgentRunResponse(AgentRunInDBBase):
    pass