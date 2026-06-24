# StudyFlow Dashboard

Streamlit-Dashboard zur Verwaltung von Studienmodulen mit:
- KPI-Uebersicht (ECTS, Notenschnitt, offene Module, Top-Empfehlung)
- Erfassungsformular fuer Modulabschluesse und Motivation
- Motivations- und Empfehlungsranking offener Module

## Offline-Installation und Offline-Nutzung (Windows)

### Voraussetzungen

- Python 3.10 oder neuer ist installiert (empfohlen: Python 3.11 oder 3.12).
- Das bereitgestellte Paket enthaelt den Ordner `wheelhouse` mit allen benoetigten Wheels.

## Installation (offline)

1. `install.bat` ausfuehren.
2. `start.bat` ausfuehren.

Hinweis:
- `install.bat` installiert ausschliesslich aus lokalen Wheels (`--no-index --find-links wheelhouse`).
- Auf dem Ziel-PC wird keine Internetverbindung benoetigt.
- Die App selbst nutzt keine externen APIs oder Online-Dienste.

## Nutzung (offline)

```bat
start.bat
```

Nach dem Start ist die Anwendung lokal im Browser erreichbar:
- `http://127.0.0.1:8501`

## Inhalt des Offline-Pakets

- Anwendungscode (`app.py`, `src/`, `assets/`)
- Daten (`data/`)
- Installer/Starter (`install.bat`, `start.bat`)
- Abhaengigkeiten (`requirements.txt`, `wheelhouse/`)

## Haeufige Fehler

- Fehler: `wheelhouse` fehlt
  -> Paket unvollstaendig. Vollstaendigen Projektordner inkl. `wheelhouse` bereitstellen.
- Fehler: Python nicht gefunden
  -> Python 3.10+ installieren und danach `install.bat` erneut ausfuehren.

## Datenquellen

- `data/studiengang.csv`: Stammdaten des Studiengangs
- `data/studienmodule.csv`: Modulkatalog
- `data/studienmodule_abgeschlossen.json`: persistierte Abschluesse und Motivationsdaten

Hinweis zu `studiengang.csv`:
- Die Spalten `name`, `abschlussart`, `regelstudienzeit`, `gesamt_ects`, `ziel_note`, `enddatum_studium` sind Pflichtfelder und werden ohne Fallback direkt eingelesen.
