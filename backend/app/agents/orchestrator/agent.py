"""Orchestrator agent — morning plan, evening summary, workflow dispatch."""
import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, date
from ..base_agent import BasePolsiaAgent

logger = logging.getLogger(__name__)


class OrchestratorAgent(BasePolsiaAgent):
    def __init__(self, agent_id: int):
        super().__init__(agent_id)
        self.agent_type = "orchestrator"

    def build_prompt(self, task: Dict[str, Any], context: Dict[str, Any]) -> str:
        title = task.get("title", "Orchestration task")
        desc = task.get("description", "")

        if "morning" in title.lower():
            return self._morning_prompt(context)
        elif "evening" in title.lower() or "summary" in title.lower():
            return self._evening_prompt(context)
        elif "plan" in title.lower():
            return self._planning_prompt(context)
        else:
            return self._default_prompt(title, desc, context)

    def _morning_prompt(self, context: Dict[str, Any]) -> str:
        company = context.get("company", {})
        goals = context.get("goals", {})
        kpis = context.get("kpis", {})

        return f"""You are the orchestrator AI for {company.get('name', 'a business')}.
Today is {date.today().isoformat()}.

Company context:
- Mission: {company.get('mission', 'N/A')}
- Industry: {company.get('industry', 'N/A')}
- Target market: {company.get('target_market', 'N/A')}

Current goals: {json.dumps(goals)}
Current KPIs: {json.dumps(kpis)}

Create a morning briefing plan that:
1. Lists 3-5 priorities for today
2. Identifies which agents should handle each priority
3. Specifies any metrics to check
4. Notes any risks or blockers

Output as JSON with keys: "summary" (string), "priorities" (array of objects with "agent", "task", "reason"), "metrics_to_check" (array of strings), "risks" (array of strings)."""

    def _evening_prompt(self, context: Dict[str, Any]) -> str:
        company = context.get("company", {})
        return f"""You are the orchestrator AI for {company.get('name', 'a business')}.
Today is {date.today().isoformat()}.

Generate an end-of-day summary that:
1. Reviews what was accomplished
2. Identifies any unfinished items
3. Suggests tomorrow's focus areas
4. Highlights any anomalies or concerns

Output as JSON with keys: "summary" (string), "accomplishments" (array of strings), "unfinished" (array of strings), "tomorrow_focus" (array of strings), "concerns" (array of strings)."""

    def _planning_prompt(self, context: Dict[str, Any]) -> str:
        return f"""Analyze the current business context and create a strategic plan.

Context: {json.dumps(context, default=str)}

Output as JSON with: "summary" (string), "recommendations" (array of objects), "timeline" (string)."""

    def _default_prompt(self, title: str, desc: str, context: Dict[str, Any]) -> str:
        return f"""Task: {title}
Description: {desc}

Context: {json.dumps(context, default=str)}

Provide a structured response as JSON with keys: "summary", "insights" (array), "action_items" (array)."""
