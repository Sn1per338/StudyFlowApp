"""Repository zum Laden eines Studiengangs aus einer CSV-Datei."""

import csv
from pathlib import Path

from src.models import Studiengang


class CsvStudienRepository:
    """Lädt Studiengangsdaten aus einer CSV-Datei."""

    ERFORDERLICHE_SPALTEN = (
        "name",
        "abschlussart",
        "regelstudienzeit",
        "gesamt_ects",
        "ziel_note",
        "enddatum_studium",
    )

    def __init__(self, pfad: Path):
        self.pfad = pfad

    def lade(self):
        """Lädt den Studiengang ausschließlich aus der CSV-Datei."""
        with open(self.pfad, mode="r", newline="", encoding="utf-8") as csv_datei:
            reader = csv.DictReader(csv_datei)
            feldnamen = tuple(reader.fieldnames or ())
            fehlende_spalten = [spalte for spalte in self.ERFORDERLICHE_SPALTEN if spalte not in feldnamen]
            if fehlende_spalten:
                raise ValueError(
                    "Fehlende Spalten in studiengang.csv: "
                    + ", ".join(fehlende_spalten)
                )

            try:
                zeile = next(reader)
            except StopIteration as exc:
                raise ValueError("studiengang.csv enthält keine Datenzeile.") from exc

        for feld in self.ERFORDERLICHE_SPALTEN:
            if not str(zeile.get(feld, "")).strip():
                raise ValueError(f"Pflichtfeld '{feld}' ist in studiengang.csv leer.")

        return Studiengang(
            name=zeile["name"].strip(),
            abschlussart=zeile["abschlussart"].strip(),
            gesamt_ects=int(zeile["gesamt_ects"]),
            ziel_note=float(zeile["ziel_note"]),
            regelstudienzeit=int(zeile["regelstudienzeit"]),
            enddatum_studium=zeile["enddatum_studium"].strip(),
            semester=[]
        )
