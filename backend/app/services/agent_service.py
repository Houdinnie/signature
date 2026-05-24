"""Agent CRUD + run dispatch — uses crew_factory for agent execution."""
import json
import logging
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from ..models.agent import Agent, AgentRun
from ..models.task import Task
from ..schemas.agent import AgentCreate, AgentUpdate
from ..agents.crew_factory import run_agent_for_task, VALID_AGENT_TYPES
from ..services.activity_service import log_activity
from ..services.task_service import create_task, update_task_status, create_agent_run, finish_agent_run, get_today_tasks
from ..services.company_service import get_full_context

logger = logging.getLogger(__name__)


class AgentService:
    def __init__(self, db: Session):
        self.db = db

    def create_agent(self, agent: AgentCreate) -> Agent:
        db_agent = Agent(
            name=agent.name,
            agent_type=agent.agent_type,
            description=agent.description,
            is_active=agent.is_active,
            config=json.dumps(agent.config) if agent.config else None,
        )
        self.db.add(db_agent)
        self.db.commit()
        self.db.refresh(db_agent)
        return db_agent

    def get_agents(self, skip: int = 0, limit: int = 100) -> List[Agent]:
        return self.db.query(Agent).offset(skip).limit(limit).all()

    def get_agent(self, agent_id: int) -> Optional[Agent]:
        return self.db.query(Agent).filter(Agent.id == agent_id).first()

    def update_agent(self, agent_id: int, agent: AgentUpdate) -> Optional[Agent]:
        db_agent = self.get_agent(agent_id)
        if db_agent:
            update_data = agent.dict(exclude_unset=True)
            for field, value in update_data.items():
                if field == "config" and value is not None:
                    setattr(db_agent, field, json.dumps(value))
                else:
                    setattr(db_agent, field, value)
            self.db.commit()
            self.db.refresh(db_agent)
        return db_agent

    def delete_agent(self, agent_id: int) -> bool:
        db_agent = self.get_agent(agent_id)
        if db_agent:
            self.db.delete(db_agent)
            self.db.commit()
            return True
        return False

    def run_agent(self, agent_id: int, input_data: Dict[str, Any]) -> Dict[str, Any]:
        db_agent = self.get_agent(agent_id)
        if not db_agent:
            raise ValueError(f"Agent with ID {agent_id} not found")

        context = get_full_context(self.db)
        task = create_task(
            self.db,
            title=input_data.get("title", f"Run {db_agent.name}"),
            description=input_data.get("description"),
            agent_type=db_agent.agent_type,
            source="user",
            priority=input_data.get("priority", 3),
            metadata_dict=input_data,
        )
        agent_run = create_agent_run(self.db, db_agent.agent_type, task_id=task.id, input_context=input_data)
        self.db.commit()

        try:
            task_dict = {"id": task.id, "title": task.title, "description": task.description}
            result = run_agent_for_task(db_agent.agent_type, task_dict, context)
            update_task_status(self.db, task.id, "completed", result_summary=result.get("summary"))
            finish_agent_run(self.db, agent_run.id, "completed", output=result)
            log_activity(self.db, db_agent.agent_type, "task_completed", result.get("summary", "Task completed"), level="success")
            self.db.commit()
            return {"status": "success", "agent_id": agent_id, "result": result}

        except Exception as e:
            update_task_status(self.db, task.id, "failed", error_message=str(e))
            finish_agent_run(self.db, agent_run.id, "failed", error_message=str(e))
            log_activity(self.db, db_agent.agent_type, "task_failed", str(e), level="error")
            self.db.commit()
            return {"status": "error", "agent_id": agent_id, "error": str(e)}

    def get_agent_runs(self, agent_id: int, skip: int = 0, limit: int = 100) -> List[AgentRun]:
        return self.db.query(AgentRun).filter(AgentRun.agent_id == agent_id).offset(skip).limit(limit).all()

    def get_agent_statuses(self) -> List[Dict[str, Any]]:
        from sqlalchemy import func
        agents = self.get_agents()
        statuses = []
        for agent in agents:
            last_run = self.db.query(AgentRun).filter(
                AgentRun.agent_id == agent.id
            ).order_by(AgentRun.started_at.desc()).first()

            tasks_today = self.db.query(AgentRun).filter(
                AgentRun.agent_id == agent.id
            ).count()

            statuses.append({
                "agent_type": agent.agent_type,
                "last_run_at": last_run.started_at.isoformat() if last_run and last_run.started_at else None,
                "last_run_status": last_run.status if last_run else None,
                "tasks_today": tasks_today,
                "tasks_total": tasks_today,
            })
        return statuses

    def get_dashboard_summary(self) -> Dict[str, Any]:
        task_counts = get_today_tasks(self.db)
        agents = self.get_agents()
        context = get_full_context(self.db)
        return {
            "tasks_today_total": task_counts["total"],
            "tasks_today_completed": task_counts["completed"],
            "tasks_today_pending": task_counts["pending"],
            "tasks_today_failed": task_counts["failed"],
            "active_agents": [a.agent_type for a in agents if a.is_active],
            "kpis": context.get("kpis", {}),
        }
