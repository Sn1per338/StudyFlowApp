# Klassen- und Moduluebersicht (aktueller Stand)

## 1. Domänenmodelle (`src/models`)

### `Studiengang`
- Datei: `src/models/studiengang.py`
- Aufgabe: Aggregiert Stammdaten und Semester.
- Wichtige Attribute: `name`, `abschlussart`, `regelstudienzeit`, `gesamt_ects`, `ziel_note`, `enddatum_studium`, `semester`.
- Wichtige Methoden: `alle_module()`, `ects_summe()`.

### `Semester`
- Datei: `src/models/semester.py`
- Aufgabe: Modelliert ein Semester mit zugeordneten Modulen.
- Wichtige Attribute: `nummer`, `startdatum`, `geplante_ects`, `module`.
- Wichtige Methoden: `ects_summe()`, `offene_module()`, `abgeschlossene_module()`.

### `Modul`
- Datei: `src/models/modul.py`
- Aufgabe: Repräsentiert ein Studienmodul inkl. Status.
- Wichtige Attribute: `modulcode`, `name`, `ects`, `modulart`, `schwierigkeitsgrad`, `status`, `pruefungsleistung`, `motivationsbewertung`.
- Wichtige Methoden: `ist_offen()`, `ist_abgeschlossen()`, `ist_in_bearbeitung()`, `abschliessen()`.

### `Pruefungsleistung`
- Datei: `src/models/pruefungsleistung.py`
- Aufgabe: Struktur fuer pruefungsbezogene Daten.
- Wichtige Attribute: `pruefungsform`, `note`, `abschlussdatum`.
- Wichtige Methoden: `ist_bewertet()`, `ist_bestanden()`.

### `Motivationsbewertung`
- Datei: `src/models/motivationsbewertung.py`
- Aufgabe: Struktur fuer motivationale Bewertung.
- Wichtige Attribute: `wert`, `kategorie`, `kommentar`.
- Wichtige Methoden: `ist_hoch()`, `ist_mittel()`, `ist_niedrig()`.

### `ModulEmpfehlung`
- Datei: `src/models/modul_empfehlung.py`
- Aufgabe: Value Object fuer Empfehlungsergebnisse.
- Attribute: `modul`, `score` (0..10), `begruendung`.
- Abgeleitetes Attribut: `score_prozent` (0..100) als `@property`.

### Enums (`aufzaehlungen.py`)
- `ModulStatus`: `OFFEN`, `IN_BEARBEITUNG`, `ABGESCHLOSSEN`
- `Pruefungsform`: `KLAUSUR`, `HAUSARBEIT`, `PORTFOLIO`, `PRAESENTATION`, `MUENDLICH`
- `Motivationskategorie`: `NIEDRIG`, `MITTEL`, `HOCH`

## 2. Repositories (`src/repositories`)

### `CsvStudienRepository`
- Datei: `src/repositories/csv_studien_repository.py`
- Aufgabe: Lädt Studiengangsdaten strikt aus CSV (ohne Ableitungen/Fallbacks).
- Methode: `lade()`.

### `CsvModulRepository`
- Datei: `src/repositories/csv_modul_repository.py`
- Aufgabe: Lädt alle Module aus CSV.
- Methode: `lade_alle_module()`.

### `JsonModulRepository`
- Datei: `src/repositories/json_modul_repository.py`
- Aufgabe: Persistiert abgeschlossene Module und Bewertungsdaten.
- Methoden: `lade_eintraege()`, `lade_abgeschlossene_modulcodes()`, `speichere_modulabschluss(...)`.

## 3. Services (`src/services`)

### `dashboard_metrics.py`
- Aufgabe: Zustandslose Fachlogik fuer Dashboard-Kennzahlen und Rankings.
- Kernfunktionen:
  - `berechne_ects_fortschritt(...)`
  - `berechne_motivationswert(...)`
  - `berechne_empfehlungsscore(...)`
  - `empfehlung_prozent_aus_score(...)`
  - `ermittle_offene_module(...)`, `zaehle_offene_module(...)`
  - `berechne_module_ranking(...)` -> `list[ModulEmpfehlung]`

## 4. UI-Komponenten (`src/ui`)

### `components.py`
- Aufgabe: Wiederverwendbare Renderer fuer HTML/CSS-nahe Ansichtskomponenten.
- Kernfunktionen:
  - `apply_css(...)`
  - `render_hero_panel(...)`
  - `render_section_heading(...)`
  - `render_kpi_card(...)`
  - `render_module_card(...)`
  - `render_scoring_top_card(...)`
  - `render_scoring_item(...)`

## 5. Einstiegspunkt

### `app.py`
- Aufgabe: Orchestriert Datenladen, KPI-Berechnung, Formular-Workflow, Persistenz und Scoring-Anzeige.
- Verwendet Repositories, Service-Funktionen und UI-Renderer.
