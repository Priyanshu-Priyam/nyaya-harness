from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any

from nyaya.schemas.pramana import PramanaCall


class Tool(ABC):
    """Base interface for all pramana tools."""

    category: str
    name: str
    description: str
    confidence_level: str
    input_schema: dict[str, Any] = {}

    @abstractmethod
    def execute(self, **kwargs: Any) -> str:
        raise NotImplementedError

    def call(self, used_for: str, **kwargs: Any) -> PramanaCall:
        output = self.execute(**kwargs)
        return PramanaCall(
            tool=f"{self.category}.{self.name}",
            category=self.category,  # type: ignore[arg-type]
            input=kwargs,
            output=output,
            confidence=self.confidence_level,  # type: ignore[arg-type]
            used_for=used_for,  # type: ignore[arg-type]
            timestamp=datetime.now(),
        )

    def to_llm_tool_spec(self) -> dict[str, Any]:
        return {
            "name": f"{self.category}.{self.name}",
            "description": self.description,
            "input_schema": self.input_schema or {
                "type": "object",
                "properties": {},
                "required": [],
            },
        }
