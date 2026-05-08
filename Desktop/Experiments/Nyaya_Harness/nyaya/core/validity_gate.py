from nyaya.schemas.validity import KaranataResult


class ValidityGate:
    """Phase 2+ placeholder."""

    def check(self, *_args, **_kwargs) -> KaranataResult:
        return KaranataResult(
            purvavartitva=True,
            purvavartitva_evidence="Phase 1 default",
            niyatatva=True,
            niyatatva_evidence="Phase 1 default",
            ananyathasiddhatva=True,
            ananyathasiddhatva_evidence="Phase 1 default",
        )
