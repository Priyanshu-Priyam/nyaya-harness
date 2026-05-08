from collections.abc import Iterator

from nyaya.schemas.pancavayava import PancavayavaStep
from nyaya.schemas.pramana import PramanaCall


class TraceQuery:
    """Query helpers over completed trace."""

    def __init__(self, trace: list[PancavayavaStep]):
        self.trace = trace

    def get_step(self, step_id: int) -> PancavayavaStep:
        for step in self.trace:
            if step.step_id == step_id:
                return step
        raise KeyError(f"Step {step_id} not found")

    def get_last_nigamana(self) -> str:
        if not self.trace:
            return ""
        return self.trace[-1].nigamana or ""

    def find_steps_with_udaharana(self, rule: str) -> list[int]:
        return [step.step_id for step in self.trace if step.udaharana == rule]

    def walk_upstream(self, from_step: int) -> Iterator[PancavayavaStep]:
        for step in reversed(self.trace):
            if step.step_id < from_step:
                yield step

    def get_all_pramana_calls(self) -> list[PramanaCall]:
        calls: list[PramanaCall] = []
        for step in self.trace:
            calls.extend(step.pramana_calls)
        return calls
