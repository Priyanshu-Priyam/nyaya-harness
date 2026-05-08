import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional

from nyaya.schemas.pancavayava import PancavayavaShell, PancavayavaStep
from nyaya.schemas.state import SessionState


class StateManager:
    def __init__(self, workspace: Path):
        self.workspace = workspace.resolve()
        self.nyaya_dir = self.workspace / ".nyaya"
        self.traces_dir = self.nyaya_dir / "traces"
        self.current_session_file = self.nyaya_dir / "current_session.json"
        self._ensure_dirs()
        self.session: Optional[SessionState] = None

    def _ensure_dirs(self) -> None:
        self.traces_dir.mkdir(parents=True, exist_ok=True)

    def _session_path(self, session_id: str) -> Path:
        return self.traces_dir / f"session_{session_id}.json"

    def new_session(self, goal: str) -> SessionState:
        session_id = uuid.uuid4().hex[:8]
        self.session = SessionState(session_id=session_id, goal=goal, workspace=str(self.workspace))
        self.save()
        return self.session

    def load_session(self, session_id: str | None = None) -> SessionState:
        if session_id is None:
            if self.current_session_file.exists():
                pointer = json.loads(self.current_session_file.read_text(encoding="utf-8"))
                session_id = pointer["session_id"]
            else:
                raise FileNotFoundError("No active session found")
        data = json.loads(self._session_path(session_id).read_text(encoding="utf-8"))
        self.session = SessionState.model_validate(data)
        return self.session

    def save(self) -> None:
        if not self.session:
            return
        self.session.updated_at = datetime.now()
        path = self._session_path(self.session.session_id)
        path.write_text(self.session.model_dump_json(indent=2), encoding="utf-8")
        self.current_session_file.write_text(
            json.dumps({"session_id": self.session.session_id}, indent=2),
            encoding="utf-8",
        )

    def set_plan(self, plan: list[PancavayavaShell]) -> None:
        assert self.session is not None
        self.session.plan = plan
        self.session.status = "executing"
        self.save()

    def get_current_step_shell(self) -> PancavayavaShell:
        assert self.session is not None
        if self.session.current_step >= len(self.session.plan):
            raise IndexError("No more steps")
        return self.session.plan[self.session.current_step]

    def commit_step(self, step: PancavayavaStep) -> None:
        assert self.session is not None
        self.session.trace.append(step)
        self.session.total_pramana_calls += len(step.pramana_calls)
        self.save()

    def advance(self) -> None:
        assert self.session is not None
        self.session.current_step += 1
        if self.session.current_step >= len(self.session.plan):
            self.session.status = "completed"
        self.save()

    def revise_step(self, step_id: int, new_nigamana: str, reason: str) -> None:
        assert self.session is not None
        for step in self.session.trace:
            if step.step_id == step_id:
                step.previous_nigamana = step.nigamana
                step.nigamana = new_nigamana
                step.revised = True
                step.revision_reason = reason
                step.revision_timestamp = datetime.now()
                step.status = "revised"
                break
        self.save()

    def replace_plan_from(self, step_id: int, new_steps: list[PancavayavaShell]) -> None:
        assert self.session is not None
        old_plan = self.session.plan.copy()
        self.session.plan = [s for s in self.session.plan if s.step_id < step_id] + new_steps
        self.session.plan_revisions.append(
            {
                "timestamp": datetime.now().isoformat(),
                "reason": f"replace_from_{step_id}",
                "old_plan": [p.model_dump() for p in old_plan],
                "new_plan": [p.model_dump() for p in self.session.plan],
            }
        )
        self.save()

    def insert_substeps(self, after_step_id: int, substeps: list[PancavayavaShell]) -> None:
        assert self.session is not None
        updated: list[PancavayavaShell] = []
        for shell in self.session.plan:
            updated.append(shell)
            if shell.step_id == after_step_id:
                updated.extend(substeps)
        self.session.plan = updated
        self.save()
