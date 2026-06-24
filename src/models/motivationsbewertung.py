"""Modell fuer eine strukturierte Motivationsbewertung."""

from .aufzaehlungen import Motivationskategorie


class Motivationsbewertung:
    """Kapselt Motivationswert, Kategorie und optionalen Kommentar."""

    def __init__(self, wert, kategorie, kommentar=""):
        self.wert = wert
        self.kategorie = kategorie
        self.kommentar = kommentar

    @property
    def wert(self):
        """Gibt den Motivationswert zurück."""
        return self._wert
    
    @wert.setter
    def wert(self, wert):
        if wert < 1 or wert > 5:
            raise ValueError("Der Motivationswert muss zwischen 1 und 5 liegen.")
        self._wert = wert

    @property
    def kategorie(self):
        """Gibt die Motivationskategorie zurück."""
        return self._kategorie
    
    @kategorie.setter
    def kategorie(self, wert):
        if not isinstance(wert, Motivationskategorie):
            raise ValueError("Die Kategorie muss ein Wert aus Motivationskategorie sein.")
        self._kategorie = wert

    @property
    def kommentar(self):
        """Gibt den Kommentar zur Motivation zurück."""
        return self._kommentar

    @kommentar.setter
    def kommentar(self, wert):
        self._kommentar = wert if wert is not None else ""

    def ist_hoch(self):
        """Motivationswert hoch."""
        return self.kategorie == Motivationskategorie.HOCH

    def ist_mittel(self):
        """Motivationswert mittel."""
        return self.kategorie == Motivationskategorie.MITTEL

    def ist_niedrig(self):
        """Motivationswert niedrig."""
        return self.kategorie == Motivationskategorie.NIEDRIG
