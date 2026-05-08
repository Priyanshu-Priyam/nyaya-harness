from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

from .pancavayava import PancavayavaShell, PancavayavaStep


class SessionState(BaseModel):
    """Complete harness state for a single task execution."""

    session_id: str
    goal: str
    workspace: str
    plan: list[PancavayavaShell] = Field(default_factory=list)
    current_step: int = 0
    status: Literal["planning", "executing", "recovering", "completed", "failed", "paused"] = "planning"
    trace: list[PancavayavaStep] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    total_pramana_calls: int = 0
    total_failures: int = 0
    total_recoveries: int = 0
    plan_revisions: list[dict] = Field(default_factory=list)
