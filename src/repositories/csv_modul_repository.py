"""Repository zum Laden von Modulen aus einer CSV-Datei."""

import csv
from pathlib import Path

from src.models import Modul, ModulStatus


class CsvModulRepository:
    """Lädt Module aus einer CSV-Datei."""

    def __init__(self, pfad: Path):
        self.pfad = pfad

    def lade_alle_module(self):
        """Lädt alle Module aus der CSV-Datei."""
        module = []

        with open(self.pfad, mode="r", newline="", encoding="utf-8") as csv_datei:
            reader = csv.DictReader(csv_datei)

            for zeile in reader:
                modul = Modul(
                    modulcode=zeile["modul_id"],
                    name=zeile["titel"],
                    ects=int(float(zeile["ects"].replace(",", "."))),
                    modulart=zeile["modulart"],
                    schwierigkeitsgrad="mittel",
                    status=ModulStatus.OFFEN,
                    pruefungsleistung=zeile.get("pruefungsleistung") or None,
                )

                module.append(modul)

        return module
