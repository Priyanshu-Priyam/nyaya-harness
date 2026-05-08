from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field

from .failure import FailureRecord
from .pramana import PramanaCall
from .validity import KaranataResult


class PancavayavaShell(BaseModel):
    """Plan-time step shell."""

    step_id: int
    pratijna: str
    udaharana: str


class PancavayavaStep(BaseModel):
    """Complete step record after execution."""

    step_id: int
    pratijna: str
    hetu: str
    udaharana: str
    upanaya: Optional[str] = None
    nigamana: Optional[str] = None
    verification: Optional[Literal["PASS", "FAIL"]] = None
    validity: Optional[KaranataResult] = None
    pramana_calls: list[PramanaCall] = Field(default_factory=list)
    failure: Optional[FailureRecord] = None
    revised: bool = False
    revision_reason: Optional[str] = None
    revision_timestamp: Optional[datetime] = None
    previous_nigamana: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    status: Literal["planned", "executing", "passed", "failed", "revised"] = "planned"
