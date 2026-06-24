"""Aufzählungen/ Enumerations"""

from enum import Enum


class ModulStatus(Enum):
    """Bearbeitungsstatus eines Moduls."""

    OFFEN = "offen"
    IN_BEARBEITUNG = "in bearbeitung"
    ABGESCHLOSSEN = "abgeschlossen"

    @classmethod
    def aus_wert(cls, wert):
        """Normalisiert freie Statuswerte auf einen Enum-Eintrag."""
        if isinstance(wert, cls):
            return wert

        text = str(wert or "").strip().lower()
        mapping = {
            cls.OFFEN.value: cls.OFFEN,
            cls.IN_BEARBEITUNG.value: cls.IN_BEARBEITUNG,
            cls.ABGESCHLOSSEN.value: cls.ABGESCHLOSSEN,
        }

        if text not in mapping:
            erlaubte_werte = ", ".join(mapping.keys())
            raise ValueError(f"Ungültiger Status '{wert}'. Erlaubte Werte: {erlaubte_werte}.")

        return mapping[text]


class Pruefungsform(Enum):
    "Prüfungsform Enum eines Moduls"

    KLAUSUR = "Klausur"
    HAUSARBEIT = "Hausarbeit"
    PORTFOLIO = "Portfolio"
    PRAESENTATION = "Präsentation"
    MUENDLICH = "Mündliche Prüfung"

class Motivationskategorie(Enum):
    """Motivationskategorien für ein Modul"""

    NIEDRIG = "Niedrig"
    MITTEL = "Mittel"
    HOCH = "Hoch"
