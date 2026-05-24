from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ...core.database import get_db
from ...services.agent_service import AgentService

router = APIRouter()


@router.get("/summary")
def dashboard_summary(db: Session = Depends(get_db)):
    service = AgentService(db)
    return service.get_dashboard_summary()


@router.get("/agents/status")
def agent_statuses(db: Session = Depends(get_db)):
    service = AgentService(db)
    return service.get_agent_statuses()
