"""Value Object für eine Modulempfehlung."""


class ModulEmpfehlung:
    """Speichert das Ergebnis einer Modulempfehlung."""

    def __init__(self, modul, score, begruendung):
        self.modul = modul
        self.score = float(score)
        self.begruendung = begruendung

    @property
    def score_prozent(self) -> float:
        """Leitet den Prozentwert aus dem Score (0..10) ab."""
        return max(0.0, min(self.score, 10.0)) * 10.0
