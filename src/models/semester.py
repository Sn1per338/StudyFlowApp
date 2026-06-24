"""Klasse Semester fuer das StudyFlow Dashboard."""


class Semester:
    """
    Beschreibt ein Studiensemester.

    Attribute:
        nummer: Nummer des Semesters
        startdatum: Startdatum des Semesters
        geplante_ects: Geplante ECTS-Punkte für das Semester
        module: Liste der Module in diesem Semester
    """

    def __init__(self, nummer, startdatum, geplante_ects, module=None):
        self.nummer = nummer
        self.startdatum = startdatum
        self.geplante_ects = geplante_ects
        self.module = module if module is not None else []

    @property
    def nummer(self):
        """Gibt die Semesternummer zurück."""
        return self._nummer

    @nummer.setter
    def nummer(self, wert):
        if wert <= 0:
            raise ValueError("Die Semesternummer muss größer als 0 sein.")
        self._nummer = wert

    @property
    def startdatum(self):
        """Gibt das Startdatum des Semesters zurück."""
        return self._startdatum

    @startdatum.setter
    def startdatum(self, wert):
        self._startdatum = wert

    @property
    def geplante_ects(self):
        """Gibt die geplanten ECTS-Punkte zurück."""
        return self._geplante_ects

    @geplante_ects.setter
    def geplante_ects(self, wert):
        if wert < 0:
            raise ValueError("Die geplanten ECTS dürfen nicht negativ sein.")
        self._geplante_ects = wert

    @property
    def module(self):
        """Gibt die Modulliste des Semesters zurück."""
        return self._module

    @module.setter
    def module(self, wert):
        self._module = wert if wert is not None else []

    def ects_summe(self):
        """Berechnet die Summe der ECTS-Punkte aller Module im Semester."""
        return sum(modul.ects for modul in self.module)

    def offene_module(self):
        """Gibt alle noch nicht abgeschlossenen Module zurück."""
        return [
            modul for modul in self.module
            if not modul.ist_abgeschlossen()
        ]

    def abgeschlossene_module(self):
        """Gibt alle abgeschlossenen Module zurück."""
        return [
            modul for modul in self.module
            if modul.ist_abgeschlossen()
        ]
