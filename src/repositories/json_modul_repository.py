"""Repository zum Speichern von Modulen in einer JSON-Datei."""

import json
from pathlib import Path

from src.models import ModulStatus


class JsonModulRepository:
    """Speichert Module als JSON-Datei."""

    def __init__(self, pfad: Path):
        self.pfad = pfad

    def schreibe_module_json(self, module):
        """Speichert eine Liste von Modulen als JSON."""
        daten = []

        for modul in module:
            daten.append({
                "modulcode": modul.modulcode,
                "name": modul.name,
                "ects": modul.ects,
                "modulart": modul.modulart,
                "schwierigkeitsgrad": modul.schwierigkeitsgrad,
                "status": modul.status
            })

        with open(self.pfad, mode="w", encoding="utf-8") as json_datei:
            json.dump(daten, json_datei, ensure_ascii=False, indent=4)

    def lade_abgeschlossene_modulcodes(self):
        """Lädt Modulcodes aus JSON, die als abgeschlossen gelten."""
        daten = self.lade_eintraege()

        abgeschlossene_codes = set()

        for eintrag in daten:
            if not isinstance(eintrag, dict):
                continue

            status = str(eintrag.get("status", "")).strip().lower()

            if status != ModulStatus.ABGESCHLOSSEN.value:
                continue

            code = eintrag.get("modulcode") or eintrag.get("modul_id")

            if code:
                abgeschlossene_codes.add(str(code).strip())

        return abgeschlossene_codes

    def lade_eintraege(self):
        """Lädt alle Einträge aus der JSON-Datei."""
        if not self.pfad.exists():
            return []

        try:
            with open(self.pfad, mode="r", encoding="utf-8") as json_datei:
                daten = json.load(json_datei)
        except json.JSONDecodeError:
            # Ungueltige/leer geschriebene Datei defensiv als leere Historie behandeln.
            return []

        if not isinstance(daten, list):
            return []

        return daten

    def speichere_modulabschluss(
        self,
        modul,
        note: float,
        pruefungsform: str,
        motivation: int,
        spassfaktor: int | None = None,
        verstaendniswert: int | None = None,
        wiederholungsbereitschaft: int | None = None,
        stressfaktor: int | None = None,
        motivationswert: float | None = None,
    ):
        """Speichert oder aktualisiert einen abgeschlossenen Moduleintrag."""
        daten = self.lade_eintraege()
        code = str(modul.modulcode).strip()

        neuer_eintrag = {
            "modul_id": code,
            "modulcode": code,
            "titel": modul.name,
            "name": modul.name,
            "ects": modul.ects,
            "modulart": modul.modulart,
            "pruefungsform": str(pruefungsform),
            "status": ModulStatus.ABGESCHLOSSEN.value,
            "note": float(note),
            "motivation": int(motivation),
            "spassfaktor": int(spassfaktor) if spassfaktor is not None else None,
            "verstaendniswert": int(verstaendniswert) if verstaendniswert is not None else None,
            "wiederholungsbereitschaft": int(wiederholungsbereitschaft) if wiederholungsbereitschaft is not None else None,
            "stressfaktor": int(stressfaktor) if stressfaktor is not None else None,
            "motivationswert": float(motivationswert) if motivationswert is not None else None,
        }

        aktualisiert = False

        for eintrag in daten:
            if not isinstance(eintrag, dict):
                continue

            vorhandener_code = eintrag.get("modulcode") or eintrag.get("modul_id")

            if str(vorhandener_code).strip() == code:
                eintrag.update(neuer_eintrag)
                aktualisiert = True
                break

        if not aktualisiert:
            daten.append(neuer_eintrag)

        with open(self.pfad, mode="w", encoding="utf-8") as json_datei:
            json.dump(daten, json_datei, ensure_ascii=False, indent=4)
