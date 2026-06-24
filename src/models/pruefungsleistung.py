"""Modell fuer eine pruefungsbezogene Leistungsbewertung."""

from .aufzaehlungen import Pruefungsform


class Pruefungsleistung:
    """
    Beschreibt eine Prüfungsleistung eines Moduls.

    Attribute:
        pruefungsform: Form der Prüfung, z. B. Klausur oder Portfolio
        note: Erreichte Note
        abschlussdatum: Datum des Abschlusses
    """

    def __init__(self, pruefungsform, note=None, abschlussdatum=None):
        self.pruefungsform = pruefungsform
        self.note = note
        self.abschlussdatum = abschlussdatum

    @property
    def pruefungsform(self):
        return self._pruefungsform

    @pruefungsform.setter
    def pruefungsform(self, wert):
        if not isinstance(wert, Pruefungsform):
            raise ValueError("Die Prüfungsform muss ein Wert aus Pruefungsform sein.")
        self._pruefungsform = wert

    @property
    def note(self):
        return self._note

    @note.setter
    def note(self, wert):
        if wert is not None and (wert < 1.0 or wert > 5.0):
            raise ValueError("Die Note muss zwischen 1.0 und 5.0 liegen.")
        self._note = wert

    @property
    def abschlussdatum(self):
        return self._abschlussdatum

    @abschlussdatum.setter
    def abschlussdatum(self, wert):
        self._abschlussdatum = wert

    def ist_bewertet(self):
        return self.note is not None

    def ist_bestanden(self):
        return self.note is not None and self.note <= 4.0
