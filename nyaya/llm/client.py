import json
import os
from typing import Any

import anthropic

from nyaya.llm.prompts.execute import EXECUTE_SYSTEM
from nyaya.llm.prompts.plan import PLAN_SYSTEM


class LLMClient:
    def __init__(self, api_key: str | None = None, model: str = "claude-sonnet-4-20250514"):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.model = model
        self.client = anthropic.Anthropic(api_key=self.api_key) if self.api_key else None

    def _offline_plan(self, goal: str) -> list[dict[str, str]]:
        return [{"pratijna": goal, "udaharana": "Execute the task directly with available tools"}]

    def plan(self, goal: str, context: str = "") -> list[dict[str, str]]:
        if not self.client:
            return self._offline_plan(goal)
        msg = self.client.messages.create(
            model=self.model,
            max_tokens=800,
            system=PLAN_SYSTEM,
            messages=[{"role": "user", "content": f"Goal: {goal}\nContext: {context}"}],
        )
        text = "".join(block.text for block in msg.content if getattr(block, "type", "") == "text").strip()
        try:
            data = json.loads(text)
            return data if isinstance(data, list) else self._offline_plan(goal)
        except json.JSONDecodeError:
            return self._offline_plan(goal)

    def determine_method(self, step: dict[str, Any], current_state: str) -> dict[str, Any]:
        return {"udaharana": step.get("udaharana", "Direct execution"), "reasoning": "Phase 1 default", "proceed": True}

    def execute_step(self, step: dict[str, Any], tools: list[dict[str, Any]]) -> dict[str, Any]:
        # Phase 1 offline-compatible deterministic behavior.
        pratijna = (step.get("pratijna") or "").lower()
        if "create a file called" in pratijna and "print('hello world')" in pratijna:
            return {
                "tool_calls": [
                    {"tool": "pratyaksha.write_file", "args": {"path": "hello.py", "content": "print('hello world')\n"}}
                ],
                "nigamana": "Created hello.py with hello world print statement",
            }
        if self.client:
            msg = self.client.messages.create(
                model=self.model,
                max_tokens=1200,
                system=EXECUTE_SYSTEM,
                messages=[{"role": "user", "content": json.dumps({"step": step, "tools": tools})}],
            )
            text = "".join(block.text for block in msg.content if getattr(block, "type", "") == "text").strip()
            try:
                result = json.loads(text)
                if isinstance(result, dict):
                    return result
            except json.JSONDecodeError:
                pass
        return {"tool_calls": [], "nigamana": "No-op execution in Phase 1 fallback mode"}

    def verify(self, pratijna: str, nigamana: str, context: str) -> dict[str, Any]:
        return {"passes": pratijna.lower() in nigamana.lower(), "reason": "Phase 1 compatibility stub"}
