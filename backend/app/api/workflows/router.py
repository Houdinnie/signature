from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from ...core.database import get_db
from ...models.workflow import WorkflowTemplate, WorkflowInstance, WorkflowStep

router = APIRouter()

@router.get("/templates")
async def list_templates(db: Session = Depends(get_db)):
    templates = db.query(WorkflowTemplate).filter(WorkflowTemplate.is_active == True).all()
    return [
        {
            "id": t.id,
            "name": t.name,
            "description": t.description,
            "is_active": t.is_active,
            "created_at": t.created_at.isoformat() if t.created_at else None
        }
        for t in templates
    ]

@router.get("/templates/{template_id}")
async def get_template(template_id: int, db: Session = Depends(get_db)):
    template = db.query(WorkflowTemplate).filter(WorkflowTemplate.id == template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    return {
        "id": template.id,
        "name": template.name,
        "description": template.description,
        "steps": template.steps_json,
        "is_active": template.is_active,
        "created_at": template.created_at.isoformat() if template.created_at else None
    }

@router.get("/instances")
async def list_instances(status: str = None, db: Session = Depends(get_db)):
    query = db.query(WorkflowInstance)
    if status:
        query = query.filter(WorkflowInstance.status == status)
    instances = query.order_by(WorkflowInstance.created_at.desc()).limit(50).all()
    return [
        {
            "id": i.id,
            "name": i.name,
            "status": i.status,
            "current_step": i.current_step,
            "total_steps": i.total_steps,
            "created_at": i.created_at.isoformat() if i.created_at else None,
            "completed_at": i.completed_at.isoformat() if i.completed_at else None
        }
        for i in instances
    ]

@router.get("/instances/{instance_id}")
async def get_instance(instance_id: int, db: Session = Depends(get_db)):
    instance = db.query(WorkflowInstance).filter(WorkflowInstance.id == instance_id).first()
    if not instance:
        raise HTTPException(status_code=404, detail="Workflow instance not found")
    steps = db.query(WorkflowStep).filter(WorkflowStep.workflow_id == instance_id).order_by(WorkflowStep.step_number).all()
    return {
        "id": instance.id,
        "name": instance.name,
        "status": instance.status,
        "current_step": instance.current_step,
        "total_steps": instance.total_steps,
        "error": instance.error_message,
        "created_at": instance.created_at.isoformat() if instance.created_at else None,
        "completed_at": instance.completed_at.isoformat() if instance.completed_at else None,
        "steps": [
            {
                "step_number": s.step_number,
                "name": s.name,
                "agent_type": s.agent_type,
                "phase": s.phase,
                "risk_level": s.risk_level,
                "status": s.status,
                "error": s.error_message,
                "started_at": s.started_at.isoformat() if s.started_at else None,
                "completed_at": s.completed_at.isoformat() if s.completed_at else None
            }
            for s in steps
        ]
    }
