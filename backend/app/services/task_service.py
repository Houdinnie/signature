"""Task CRUD — Polsia pattern: source tracking, priority, status lifecycle."""
import json
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
from sqlalchemy.orm import Session
from ..models.task import Task
from ..models.agent import AgentRun

logger = logging.getLogger(__name__)


def create_task(
    db: Session,
    title: str,
    agent_type: str,
    description: Optional[str] = None,
    source: str = "orchestrator",
    priority: int = 3,
    scheduled_date: Optional[datetime] = None,
    metadata_dict: Optional[Dict[str, Any]] = None,
) -> Task:
    task = Task(
        title=title,
        description=description,
        agent_type=agent_type,
        source=source,
        priority=priority,
        status="pending",
        scheduled_date=scheduled_date,
        metadata_json=json.dumps(metadata_dict) if metadata_dict else None,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    logger.info(f"Task created: {task.id} — {title} ({agent_type})")
    return task


def get_task(db: Session, task_id: int) -> Optional[Task]:
    return db.query(Task).filter(Task.id == task_id).first()


def update_task_status(
    db: Session,
    task_id: int,
    status: str,
    result_summary: Optional[str] = None,
    error_message: Optional[str] = None,
) -> Optional[Task]:
    task = get_task(db, task_id)
    if not task:
        return None
    task.status = status
    if result_summary:
        task.result_summary = result_summary
    if error_message:
        task.error_message = error_message
    db.commit()
    db.refresh(task)
    return task


def get_pending_tasks(db: Session, agent_type: Optional[str] = None, limit: int = 50) -> List[Task]:
    query = db.query(Task).filter(Task.status == "pending").order_by(Task.priority.asc(), Task.created_at.asc())
    if agent_type:
        query = query.filter(Task.agent_type == agent_type)
    return query.limit(limit).all()


def get_today_tasks(db: Session) -> Dict[str, int]:
    from datetime import date
    today = date.today()
    tasks = db.query(Task).filter(
        Task.created_at >= datetime.combine(today, datetime.min.time())
    ).all()
    return {
        "total": len(tasks),
        "completed": sum(1 for t in tasks if t.status == "completed"),
        "pending": sum(1 for t in tasks if t.status == "pending"),
        "failed": sum(1 for t in tasks if t.status == "failed"),
    }


def create_agent_run(
    db: Session,
    agent_type: str,
    task_id: Optional[int] = None,
    input_context: Optional[Dict[str, Any]] = None,
) -> AgentRun:
    run = AgentRun(
        agent_type=agent_type,
        task_id=task_id,
        run_type="task",
        status="running",
        input_data=json.dumps(input_context) if input_context else None,
    )
    db.add(run)
    db.commit()
    db.refresh(run)
    return run


def finish_agent_run(
    db: Session,
    run_id: int,
    status: str,
    output: Optional[Dict[str, Any]] = None,
    duration_secs: Optional[int] = None,
    error_message: Optional[str] = None,
) -> Optional[AgentRun]:
    run = db.query(AgentRun).filter(AgentRun.id == run_id).first()
    if not run:
        return None
    run.status = status
    run.output_data = json.dumps(output) if output else None
    run.duration_secs = duration_secs
    run.error_message = error_message
    run.completed_at = datetime.utcnow()
    db.commit()
    db.refresh(run)
    return run
