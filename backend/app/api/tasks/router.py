from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ...core.database import get_db
from ...models.task import Task
from ...services.task_service import create_task, update_task_status

router = APIRouter()


@router.get("/")
def list_tasks(status: str = None, agent_type: str = None, db: Session = Depends(get_db)):
    query = db.query(Task)
    if status:
        query = query.filter(Task.status == status)
    if agent_type:
        query = query.filter(Task.agent_type == agent_type)
    tasks = query.order_by(Task.priority.asc(), Task.created_at.desc()).limit(100).all()
    return [
        {
            "id": t.id,
            "title": t.title,
            "agent_type": t.agent_type,
            "status": t.status,
            "priority": t.priority,
            "source": t.source,
            "created_at": t.created_at.isoformat() if t.created_at else None,
            "result_summary": t.result_summary,
        }
        for t in tasks
    ]


@router.get("/{task_id}")
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "agent_type": task.agent_type,
        "status": task.status,
        "priority": task.priority,
        "source": task.source,
        "result_summary": task.result_summary,
        "error_message": task.error_message,
        "created_at": task.created_at.isoformat() if task.created_at else None,
        "updated_at": task.updated_at.isoformat() if task.updated_at else None,
    }


@router.post("/")
def create_new_task(title: str, agent_type: str, description: str = None, priority: int = 3, db: Session = Depends(get_db)):
    task = create_task(db, title=title, agent_type=agent_type, description=description, source="user", priority=priority)
    return {"id": task.id, "status": "created"}


@router.post("/{task_id}/cancel")
def cancel_task(task_id: int, db: Session = Depends(get_db)):
    task = update_task_status(db, task_id, "cancelled")
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"status": "cancelled"}
