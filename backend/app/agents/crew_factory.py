"""Agent registry — maps agent_type strings to their implementation classes."""
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

AGENT_MAP: Dict[str, tuple[str, str]] = {
    "orchestrator": ("app.agents.orchestrator.agent", "OrchestratorAgent"),
    "planning": ("app.agents.planning.agent", "PlanningAgent"),
    "competitor_research": ("app.agents.competitor_research.agent", "CompetitorResearchAgent"),
    "social_posts": ("app.agents.social_posts.agent", "SocialPostsAgent"),
    "email_outreach": ("app.agents.email_outreach.agent", "EmailOutreachAgent"),
    "support_reply": ("app.agents.support_reply.agent", "SupportReplyAgent"),
    "ads": ("app.agents.ads.agent", "AdsAgent"),
    "code": ("app.agents.code.agent", "CodeAgent"),
    "finance": ("app.agents.finance.agent", "FinanceAgent"),
}

VALID_AGENT_TYPES = set(AGENT_MAP.keys())


def get_agent_class(agent_type: str):
    """Lazy-import and return the agent class for the given type."""
    if agent_type not in AGENT_MAP:
        raise ValueError(f"Unknown agent type: {agent_type}. Valid: {sorted(VALID_AGENT_TYPES)}")

    module_path, class_name = AGENT_MAP[agent_type]
    import importlib
    module = importlib.import_module(module_path)
    return getattr(module, class_name)


def run_agent_for_task(agent_type: str, task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    """Dispatch a task to the appropriate agent and return structured result."""
    agent_class = get_agent_class(agent_type)
    agent = agent_class(agent_id=0)
    logger.info(f"Running agent {agent_type} for task: {task.get('title', 'Untitled')}")
    try:
        result = agent.run(task, context)
        return {
            "summary": result.get("summary", result.get("result", "Completed.")),
            "insights": result.get("insights", []),
            "raw": result,
        }
    except Exception as e:
        logger.error(f"Agent {agent_type} failed: {e}")
        return {
            "summary": f"Agent {agent_type} failed: {str(e)}",
            "insights": [],
            "raw": {"error": str(e)},
        }
