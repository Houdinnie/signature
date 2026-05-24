import json
import logging
import os
import subprocess
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


def call_claude(prompt: str, output_format: str = "json") -> Dict[str, Any]:
    """Call Claude Code CLI as a subprocess — no API key needed."""
    if os.getenv("CLAUDE_CLI_MOCK"):
        return json.loads(os.getenv("CLAUDE_CLI_MOCK_RESPONSE", '{"result": "Mock Claude response for testing"}'))

    claude_path = os.getenv("CLAUDE_CLI_PATH", "claude")
    try:
        result = subprocess.run(
            [claude_path, "-p", prompt, "--output-format", output_format],
            capture_output=True, text=True, timeout=120,
        )
        if result.returncode != 0:
            raise RuntimeError(f"Claude CLI error (exit {result.returncode}): {result.stderr.strip()}")
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return {"result": result.stdout.strip()}
    except FileNotFoundError:
        raise RuntimeError("Claude Code CLI not found. Install via: npm install -g @anthropic-ai/claude-code")


class BasePolsiaAgent(ABC):
    """Base class for all Polsia AI agents — calls Claude Code CLI as subprocess."""

    def __init__(self, agent_id: int):
        self.agent_id = agent_id
        self.agent_type: Optional[str] = None

    @abstractmethod
    def build_prompt(self, task: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Build the Claude prompt for this agent type."""
        ...

    def run(self, task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute agent: build prompt → call Claude → return result."""
        prompt = self.build_prompt(task, context)
        logger.info(f"Agent {self.agent_type} (ID {self.agent_id}) calling Claude CLI")
        result = call_claude(prompt)
        return self.parse_result(result, task, context)

    def parse_result(self, raw: Dict[str, Any], task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Override to transform Claude output into structured result."""
        return raw
