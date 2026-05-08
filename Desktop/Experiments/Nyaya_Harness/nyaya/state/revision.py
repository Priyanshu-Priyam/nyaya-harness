class RevisionTracker:
    """Track step revisions during recoveries."""

    def __init__(self) -> None:
        self._revisions: list[dict] = []

    def record_revision(
        self,
        step_id: int,
        original_nigamana: str,
        new_nigamana: str,
        reason: str,
        triggered_by_step: int,
    ) -> None:
        self._revisions.append(
            {
                "step_id": step_id,
                "original_nigamana": original_nigamana,
                "new_nigamana": new_nigamana,
                "reason": reason,
                "triggered_by_step": triggered_by_step,
            }
        )

    def get_revisions(self) -> list[dict]:
        return list(self._revisions)

    def was_revised(self, step_id: int) -> bool:
        return any(r["step_id"] == step_id for r in self._revisions)
