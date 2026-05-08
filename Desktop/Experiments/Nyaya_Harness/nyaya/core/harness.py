from datetime import datetime
from pathlib import Path

from nyaya.core.executor import execute_tool_calls
from nyaya.core.planner import build_shell_plan
from nyaya.llm.client import LLMClient
from nyaya.schemas.pancavayava import PancavayavaStep
from nyaya.state.manager import StateManager
from nyaya.state.trace import TraceQuery
from nyaya.tools.registry import ToolRegistry


class NyayaHarness:
    """Phase 1 orchestration loop."""

    def __init__(self, workspace: str, llm: LLMClient | None = None):
        self.workspace = Path(workspace).resolve()
        self.llm = llm or LLMClient()
        self.tools = ToolRegistry(str(self.workspace))
        self.state = StateManager(self.workspace)

    def run(self, goal: str):
        session = self.state.new_session(goal=goal)
        plan_rows = self.llm.plan(goal=goal, context=f"workspace={self.workspace}")
        shells = build_shell_plan(plan_rows)
        self.state.set_plan(shells)

        while session.current_step < len(session.plan):
            shell = self.state.get_current_step_shell()
            trace_query = TraceQuery(session.trace)
            previous_nigamana = trace_query.get_last_nigamana()

            step = PancavayavaStep(
                step_id=shell.step_id,
                pratijna=shell.pratijna,
                udaharana=shell.udaharana,
                hetu=previous_nigamana or "Initial workspace state",
                started_at=datetime.now(),
                status="executing",
            )

            method = self.llm.determine_method(step.model_dump(), current_state=session.model_dump_json())
            if not method.get("proceed", True):
                step.status = "failed"
                step.nigamana = "Execution halted by determine_method"
                self.state.commit_step(step)
                session.status = "failed"
                self.state.save()
                break
            step.udaharana = method.get("udaharana", step.udaharana)

            execution = self.llm.execute_step(step.model_dump(), self.tools.list_available())
            execute_tool_calls(step=step, tool_calls=execution.get("tool_calls", []), tools=self.tools)
            step.nigamana = execution.get("nigamana", "")
            step.verification = "PASS"
            step.status = "passed"
            step.completed_at = datetime.now()

            self.state.commit_step(step)
            self.state.advance()
            session = self.state.session  # refresh mutable reference
            assert session is not None

        assert self.state.session is not None
        return self.state.session
