from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ...core.database import get_db
from ...models.agent import Agent
from ...schemas.agent import AgentCreate, AgentResponse, AgentUpdate
from ...services.agent_service import AgentService

router = APIRouter()

@router.post("/", response_model=AgentResponse)
def create_agent(agent: AgentCreate, db: Session = Depends(get_db)):
    """Create a new agent"""
    agent_service = AgentService(db)
    return agent_service.create_agent(agent)

@router.get("/", response_model=List[AgentResponse])
def read_agents(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all agents"""
    agent_service = AgentService(db)
    return agent_service.get_agents(skip=skip, limit=limit)

@router.get("/{agent_id}", response_model=AgentResponse)
def read_agent(agent_id: int, db: Session = Depends(get_db)):
    """Get a specific agent by ID"""
    agent_service = AgentService(db)
    agent = agent_service.get_agent(agent_id)
    if agent is None:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent

@router.put("/{agent_id}", response_model=AgentResponse)
def update_agent(agent_id: int, agent: AgentUpdate, db: Session = Depends(get_db)):
    """Update an agent"""
    agent_service = AgentService(db)
    updated_agent = agent_service.update_agent(agent_id, agent)
    if updated_agent is None:
        raise HTTPException(status_code=404, detail="Agent not found")
    return updated_agent

@router.delete("/{agent_id}")
def delete_agent(agent_id: int, db: Session = Depends(get_db)):
    """Delete an agent"""
    agent_service = AgentService(db)
    success = agent_service.delete_agent(agent_id)
    if not success:
        raise HTTPException(status_code=404, detail="Agent not found")
    return {"message": "Agent deleted successfully"}

@router.post("/{agent_id}/run", response_model=dict)
def run_agent(agent_id: int, input_data: dict, db: Session = Depends(get_db)):
    """Run an agent with input data"""
    agent_service = AgentService(db)
    result = agent_service.run_agent(agent_id, input_data)
    return result

@router.get("/{agent_id}/runs", response_model=List[dict])
def get_agent_runs(agent_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all runs for a specific agent"""
    agent_service = AgentService(db)
    return agent_service.get_agent_runs(agent_id, skip=skip, limit=limit)