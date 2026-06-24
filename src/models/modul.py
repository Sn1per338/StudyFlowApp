"""Klasse Modul fuer das StudyFlow Dashboard."""

from .aufzaehlungen import ModulStatus


class Modul:
    """
    Beschreibt ein Studienmodul.

    Attribute:
        modulcode: Eindeutiger Modulcode
        name: Name des Moduls
        ects: ECTS-Punkte des Moduls
        modulart: Art des Moduls
        schwierigkeitsgrad: Eingeschätzter Schwierigkeitsgrad
        status: Bearbeitungsstatus des Moduls
        pruefungsleistung: Optionale Prüfungsleistung
        motivationsbewertung: Optionale Motivationsbewertung
    """

    def __init__(
        self,
        modulcode,
        name,
        ects,
        modulart,
        schwierigkeitsgrad,
        status,
        pruefungsleistung=None,
        motivationsbewertung=None
    ):
        self.modulcode = modulcode
        self.name = name
        self.ects = ects
        self.modulart = modulart
        self.schwierigkeitsgrad = schwierigkeitsgrad
        self.status = status
        self.pruefungsleistung = pruefungsleistung
        self.motivationsbewertung = motivationsbewertung

    def __str__(self):
        return f"{self.modulcode}: {self.name} ({self.ects} ECTS, {self.status})"

    def __repr__(self):
        return self.__str__()

    @property
    def modulcode(self):
        """Gibt den Modulcode zurück."""
        return self._modulcode

    @modulcode.setter
    def modulcode(self, wert):
        if not wert:
            raise ValueError("Der Modulcode darf nicht leer sein.")
        self._modulcode = wert

    @property
    def name(self):
        """Gibt den Namen des Moduls zurück."""
        return self._name

    @name.setter
    def name(self, wert):
        if not wert:
            raise ValueError("Der Modulname darf nicht leer sein.")
        self._name = wert

    @property
    def ects(self):
        """Gibt die ECTS-Punkte des Moduls zurück."""
        return self._ects

    @ects.setter
    def ects(self, wert):
        wert = int(wert)

        if wert <= 0:
            raise ValueError("Die ECTS-Punkte müssen größer als 0 sein.")

        self._ects = wert

    @property
    def modulart(self):
        """Gibt die Modulart zurück."""
        return self._modulart

    @modulart.setter
    def modulart(self, wert):
        if not wert:
            raise ValueError("Die Modulart darf nicht leer sein.")
        self._modulart = wert

    @property
    def schwierigkeitsgrad(self):
        """Gibt den Schwierigkeitsgrad zurück."""
        return self._schwierigkeitsgrad

    @schwierigkeitsgrad.setter
    def schwierigkeitsgrad(self, wert):
        if not wert:
            raise ValueError("Der Schwierigkeitsgrad darf nicht leer sein.")
        self._schwierigkeitsgrad = wert

    @property
    def status(self):
        """Gibt den Modulstatus zurück."""
        return self._status.value

    @property
    def status_enum(self):
        """Gibt den Modulstatus als Enum zurück."""
        return self._status

    @status.setter
    def status(self, wert):
        if not wert:
            raise ValueError("Der Status darf nicht leer sein.")
        self._status = ModulStatus.aus_wert(wert)

    @property
    def pruefungsleistung(self):
        """Gibt die Prüfungsleistung zurück."""
        return self._pruefungsleistung

    @pruefungsleistung.setter
    def pruefungsleistung(self, wert):
        self._pruefungsleistung = wert

    @property
    def motivationsbewertung(self):
        """Gibt die Motivationsbewertung zurück."""
        return self._motivationsbewertung

    @motivationsbewertung.setter
    def motivationsbewertung(self, wert):
        self._motivationsbewertung = wert

    def hat_pruefungsleistung(self):
        """Prüft, ob eine Prüfungsleistung vorhanden ist."""
        return self.pruefungsleistung is not None

    def hat_motivationsbewertung(self):
        """Prüft, ob eine Motivationsbewertung vorhanden ist."""
        return self.motivationsbewertung is not None

    def ist_abgeschlossen(self):
        """Prüft, ob das Modul abgeschlossen ist."""
        return self.status_enum is ModulStatus.ABGESCHLOSSEN

    def ist_offen(self):
        """Prüft, ob das Modul noch offen ist."""
        return self.status_enum is ModulStatus.OFFEN

    def ist_in_bearbeitung(self):
        """Prüft, ob das Modul aktuell in Bearbeitung ist."""
        return self.status_enum is ModulStatus.IN_BEARBEITUNG

    def abschliessen(self):
        """Setzt das Modul auf abgeschlossen."""
        self.status = ModulStatus.ABGESCHLOSSEN

    def starte_bearbeitung(self):
        """Setzt das Modul auf in Bearbeitung."""
        self.status = ModulStatus.IN_BEARBEITUNG

    def oeffnen(self):
        """Setzt das Modul zurück auf offen."""
        self.status = ModulStatus.OFFEN
