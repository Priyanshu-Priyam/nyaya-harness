from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class PramanaCall(BaseModel):
    """Record of a single epistemology tool call."""

    tool: str
    category: Literal["pratyaksha", "anumana", "upamana", "shabda"]
    input: dict
    output: str
    confidence: Literal["direct", "derived", "analogical", "authoritative"]
    used_for: Literal[
        "hetu_validation",
        "udaharana_confirmation",
        "upanaya",
        "nigamana",
        "verification",
        "failure_classification",
        "recovery",
    ]
    timestamp: datetime = Field(default_factory=datetime.now)
