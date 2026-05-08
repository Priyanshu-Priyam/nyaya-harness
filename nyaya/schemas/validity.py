from pydantic import BaseModel


class KaranataResult(BaseModel):
    """Result of the three validity conditions check."""

    purvavartitva: bool
    purvavartitva_evidence: str
    niyatatva: bool
    niyatatva_evidence: str
    ananyathasiddhatva: bool
    ananyathasiddhatva_evidence: str

    @property
    def is_valid(self) -> bool:
        return (
            self.purvavartitva
            and self.niyatatva
            and self.ananyathasiddhatva
        )
