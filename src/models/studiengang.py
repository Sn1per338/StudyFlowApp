"""Klasse Studiengang fuer das StudyFlow Dashboard."""


class Studiengang:
    """Beschreibt einen Studiengang mit Zielwerten und Semestern."""

    def __init__(
        self,
        name: str,
        abschlussart: str,
        regelstudienzeit: int,
        gesamt_ects: int,
        ziel_note: float,
        enddatum_studium: str,
        semester=None,
    ):
        """Initialisiert den Studiengang mit Basisdaten aus `data/studiengang.csv`.

        Erwartete CSV-Felder:
        - `name`: Bezeichnung des Studiengangs
        - `abschlussart`: z. B. Bachelor oder Master
        - `regelstudienzeit`: Anzahl Semester laut Studienordnung
        - `gesamt_ects`: Zielumfang in ECTS
        - `ziel_note`: gewünschter Abschlussdurchschnitt (1.0 bis 4.0)
        - `enddatum_studium`: geplantes Studienende (z. B. 2027-09-30)
        """
        self.name = name
        self.abschlussart = abschlussart
        self.regelstudienzeit = regelstudienzeit
        self.gesamt_ects = gesamt_ects
        self.ziel_note = ziel_note
        self.enddatum_studium = enddatum_studium
        self.semester = semester if semester is not None else []


    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, wert):
        if not wert:
            raise ValueError("Der Name des Studiengangs darf nicht leer sein.")
        self._name = wert

    @property
    def abschlussart(self):
        return self._abschlussart

    @abschlussart.setter
    def abschlussart(self, wert):
        if not wert:
            raise ValueError("Der Name der Abschlussart darf nicht leer sein.")
        self._abschlussart = wert

    @property
    def regelstudienzeit(self):
        return self._regelstudienzeit

    @regelstudienzeit.setter
    def regelstudienzeit(self, wert):
        if wert <= 0:
            raise ValueError("Die Regelstudienzeit muss größer als 0 sein.")
        self._regelstudienzeit = wert

    @property
    def gesamt_ects(self):
        return self._gesamt_ects

    @gesamt_ects.setter
    def gesamt_ects(self, wert):
        if wert <= 0:
            raise ValueError("Die Gesamtanzahl der ECTS muss größer als 0 sein.")
        self._gesamt_ects = wert

    @property
    def ziel_note(self):
        return self._ziel_note

    @ziel_note.setter
    def ziel_note(self, wert):
        if wert < 1.0 or wert > 4.0:
            raise ValueError("Die Zielnote muss zwischen 1.0 und 4.0 liegen.")
        self._ziel_note = wert

    @property
    def enddatum_studium(self):
        return self._enddatum_studium
    
    @enddatum_studium.setter
    def enddatum_studium(self, wert):
        if not wert:
            raise ValueError("Das Enddatum des Studiums darf nicht leer sein.")
        self._enddatum_studium = wert

    @property
    def semester(self):
        return self._semester

    @semester.setter
    def semester(self, wert):
        self._semester = wert if wert is not None else []


    ##### Abrufen aller Module aus CSV ####

    def alle_module(self):
        """Gibt alle Module aus allen Semestern zurück."""
        module = []

        for semester in self.semester:
            module.extend(semester.module)

        return module


    def ects_summe(self):
        """Berechnet die Summe aller ECTS-Punkte aus allen Modulen."""
        return sum(modul.ects for modul in self.alle_module())
