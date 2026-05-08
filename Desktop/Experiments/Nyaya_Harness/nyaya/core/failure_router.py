class FailureRouter:
    """Phase 3 placeholder."""

    def classify(self, *_args, **_kwargs):
        return {"type": "asiddha", "evidence": "Not implemented in Phase 1", "details": {}}

    def handle(self, *_args, **_kwargs):
        return {"action": "abort", "next": "abort"}
