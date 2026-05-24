"""Tests for base_agent.py — Polsia pattern."""
import json
import os
from app.agents.base_agent import call_claude, BasePolsiaAgent


class _TestAgent(BasePolsiaAgent):
    def __init__(self):
        super().__init__(agent_id=1)
        self.agent_type = "test"

    def build_prompt(self, task, context):
        return f"Test prompt for {task.get('title')}"


def test_call_claude_returns_mock():
    os.environ["CLAUDE_CLI_MOCK"] = "true"
    os.environ["CLAUDE_CLI_MOCK_RESPONSE"] = json.dumps({"result": "mocked"})
    result = call_claude("test prompt")
    assert result == {"result": "mocked"}


def test_agent_run_returns_result():
    agent = _TestAgent()
    result = agent.run({"title": "Test Task"}, {"context": "data"})
    assert "summary" in result or "result" in result


def test_build_prompt_works():
    agent = _TestAgent()
    prompt = agent.build_prompt({"title": "Hello"}, {})
    assert "Test prompt" in prompt
    assert "Hello" in prompt
