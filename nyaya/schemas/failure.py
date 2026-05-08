from enum import Enum
from typing import Literal, Optional

from pydantic import BaseModel


class FailureType(str, Enum):
    SAVYABHICARA = "savyabhicara"
    VIRUDDHA = "viruddha"
    SATPRATIPAKSHA = "satpratipaksha"
    ASIDDHA = "asiddha"
    BADHITA = "badhita"


class FailureRecord(BaseModel):
    """Complete record of what failed and how it was handled."""

    type: FailureType
    description: str
    evidence: str
    recovery_applied: Literal[
        "decompose_and_strengthen",
        "abandon_and_replan",
        "switch_pramana_and_gather",
        "go_upstream",
        "update_rule",
        "escalate_to_human",
    ]
    recovery_pramana: str
    recovery_outcome: str
    root_step: Optional[int] = None
    abandoned_udaharana: Optional[str] = None
    new_udaharana: Optional[str] = None
    falsified_rule: Optional[str] = None
    observation_override: Optional[str] = None
    cascade_affected_steps: Optional[list[int]] = None
    conflicting_evidence: Optional[dict] = None
    decomposed_into: Optional[list[str]] = None
