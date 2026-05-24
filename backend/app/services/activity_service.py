"""Structured activity logging — Polsia pattern: agent_type, action, summary, level."""
import json
import logging
from typing import Dict, Any, Optional, List
from sqlalchemy.orm import Session
from ..models.activity import ActivityLog
from ..core.database import SessionLocal

logger = logging.getLogger(__name__)


def log_activity(
    db: Session,
    agent_type: str,
    action: str,
    summary: str,
    level: str = "info",
    detail: Optional[Dict[str, Any]] = None,
) -> ActivityLog:
    entry = ActivityLog(
        agent_type=agent_type,
        action=action,
        summary=summary,
        level=level,
        detail=json.dumps(detail) if detail else None,
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


def get_recent_activity(
    db: Session,
    agent_type: Optional[str] = None,
    limit: int = 50,
    level: Optional[str] = None,
) -> List[ActivityLog]:
    query = db.query(ActivityLog)
    if agent_type:
        query = query.filter(ActivityLog.agent_type == agent_type)
    if level:
        query = query.filter(ActivityLog.level == level)
    return query.order_by(ActivityLog.created_at.desc()).limit(limit).all()


def get_activity_stats(db: Session) -> Dict[str, Any]:
    total = db.query(ActivityLog).count()
    by_level = {}
    for level in ("info", "success", "warning", "error"):
        count = db.query(ActivityLog).filter(ActivityLog.level == level).count()
        if count:
            by_level[level] = count
    return {"total": total, "by_level": by_level}
