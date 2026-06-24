"""Streamlit-Entry-Point fuer das StudyFlow Dashboard."""

from pathlib import Path
import streamlit as st

# Paket-API-Imports: app.py importiert nur ueber __init__.py,
# damit interne Modulpfade bei Umstrukturierungen stabil bleiben.
from src.repositories import CsvStudienRepository, CsvModulRepository, JsonModulRepository
from src.models import ModulStatus
from src.services import (
    berechne_module_ranking,
    berechne_ects_fortschritt,
    berechne_motivationswert,
    ermittle_offene_module,
    ermittle_pruefungsformen,
    zaehle_offene_module,
)
from src.ui import (
    apply_css,
    render_hero_panel,
    render_kpi_card,
    render_module_card,
    render_scoring_item,
    render_scoring_top_card,
    render_section_heading,
)


st.set_page_config(
    page_title="StudyFlow Dashboard",
    layout="wide"
)

# Globales Stylesheet einmalig laden und auf die gesamte Seite anwenden.
apply_css("assets/style.css")


try:
    # Stammdaten des Studiengangs laden und als Hero-Bereich visualisieren.
    repository = CsvStudienRepository(Path("data/studiengang.csv"))
    studiengang = repository.lade()
    
    render_hero_panel(
        studiengang_name=studiengang.name,
        gesamt_ects=studiengang.gesamt_ects,
        ziel_note=studiengang.ziel_note,
        regelstudienzeit=studiengang.regelstudienzeit,
        abschlussart=studiengang.abschlussart,
        enddatum_studium=studiengang.enddatum_studium,
    )
except Exception as e:
    st.error(f"Fehler beim Laden der Studiengangsdaten: {e}")
    st.stop()

try:
    # Modulstammdaten + Abschlussdaten laden und Status in-memory synchronisieren.
    csv_repository = CsvModulRepository(Path("data/studienmodule.csv"))
    json_repository = JsonModulRepository(Path("data/studienmodule_abgeschlossen.json"))

    alle_module = csv_repository.lade_alle_module()
    historien_eintraege = json_repository.lade_eintraege()
    abgeschlossene_codes = json_repository.lade_abgeschlossene_modulcodes()

    # CSV bildet die offenen Module ab; Einträge in JSON gelten als abgeschlossen.
    for modul in alle_module:
        if modul.modulcode in abgeschlossene_codes:
            modul.abschliessen()
except Exception as e:
    st.error(f"Fehler beim Laden der Module: {e}")
    st.stop()


# Datenbasis für KPI-Karten und weitere Dashboard-Bereiche.
offene_module = ermittle_offene_module(alle_module)
offene_module_anzahl = zaehle_offene_module(alle_module)
abgeschlossene_module = [modul for modul in alle_module if modul.ist_abgeschlossen()]
ranking = berechne_module_ranking(
    offene_module=offene_module,
    alle_module=alle_module,
    historien_eintraege=historien_eintraege,
)

# Abschnittsheader fuer die KPI-Uebersicht.
render_section_heading(
    title="Dashboard-Übersicht",
    subtitle="Fokus finden, Fortschritt sehen, offene Aufgaben gezielt abschließen.",
)


# Kennzahlen fuer KPI-Karten aus Live-Daten berechnen.
credits_ist = sum(float(getattr(modul, "ects", 0) or 0) for modul in abgeschlossene_module)
credits_soll = float(studiengang.gesamt_ects)
fortschritt = berechne_ects_fortschritt(credits_ist, credits_soll)

abgeschlossene_noten = []
for eintrag in historien_eintraege:
    if not isinstance(eintrag, dict):
        continue
    if str(eintrag.get("status", "")).strip().lower() != ModulStatus.ABGESCHLOSSEN.value:
        continue
    try:
        abgeschlossene_noten.append(float(eintrag.get("note")))
    except (TypeError, ValueError):
        continue

aktuelle_note = (
    sum(abgeschlossene_noten) / len(abgeschlossene_noten)
    if abgeschlossene_noten
    else float(studiengang.ziel_note)
)
ziel_note = float(studiengang.ziel_note)

if ranking:
    top_modul = ranking[0].modul
    top_empfehlung = top_modul.name
    empfehlung_score = ranking[0].score_prozent
else:
    top_empfehlung = "Keine offenen Module"
    empfehlung_score = 0.0


# KPI-Bereich in vier Spalten aufteilen und je Karte separat rendern.
col1, col2, col3, col4 = st.columns(4)

with col1:
    render_kpi_card(
        title="ECTS-Fortschritt",
        value=f"{credits_ist:.0f} / {credits_soll:.0f}",
        subtext=f"{fortschritt:.0f} % abgeschlossen",
        progress=fortschritt
    )

with col2:
    render_kpi_card(
        title="Notendurchschnitt",
        value=f"{aktuelle_note:.1f}",
        subtext=f"Zielnote: {ziel_note:.1f}"
    )

with col3:
    render_kpi_card(
        title="Module offen",
        value=str(offene_module_anzahl),
        subtext="noch nicht abgeschlossen"
    )

with col4:
    render_kpi_card(
        title="Top-Empfehlung",
        value=f"{empfehlung_score:.0f} %",
        subtext=top_empfehlung,
        progress=empfehlung_score
    )


st.divider()

# Linke/rechte Halbseite: links Eingabeformular, rechts Modul-Scoring.
col_links, col_rechts = st.columns(2)

with col_links:
    # Linke Spalte: Formularbereich.
    render_section_heading(
        title="Leistungs- und Motivations-Erfassung",
        subtitle="Wähle ein offenes Modul und erfasse die gewünschten Angaben.",
        title_class="module-input-title",
        subtitle_class="module-input-subtitle",
    )

    if offene_module_anzahl == 0:
        st.info("Aktuell sind keine offenen Module vorhanden.")
    else:
        # Prüfungsformen aus offenen Modulen ableiten; Fallback bei fehlenden Werten.
        pruefungsformen = ermittle_pruefungsformen(offene_module)

        with st.form("modul_erfassung_form"):
            ausgewaehltes_modul = st.selectbox(
                "Offenes Modul auswählen",
                options=offene_module,
                format_func=lambda modul: f"{modul.name} ({modul.modulcode})",
                key="offenes_modul_select"
            )

            note = st.number_input(
                "Note",
                min_value=1.0,
                max_value=5.0,
                value=2.0,
                step=0.1,
                format="%.1f",
                key="note_input"
            )

            pruefungsform = st.selectbox(
                "Prüfungsform",
                options=pruefungsformen,
                key="pruefungsform_select"
            )

            motivation = st.selectbox(
                "Motivation gesamt (Wertebereich 1 bis 10)",
                options=list(range(1, 11)),
                index=4,
                key="motivation_select"
            )

            spassfaktor = st.slider("Spaßfaktor (1 bis 10)", min_value=1, max_value=10, value=6, key="spassfaktor_slider")
            verstaendniswert = st.slider("Verständniswert (1 bis 10)", min_value=1, max_value=10, value=6, key="verstaendniswert_slider")
            wiederholungsbereitschaft = st.slider(
                "Wiederholungsbereitschaft (1 bis 10)",
                min_value=1,
                max_value=10,
                value=6,
                key="wiederholungsbereitschaft_slider",
            )
            stressfaktor = st.slider("Stressfaktor (1 bis 10)", min_value=1, max_value=10, value=5, key="stressfaktor_slider")

            motivationswert = berechne_motivationswert(
                spassfaktor=spassfaktor,
                verstaendniswert=verstaendniswert,
                wiederholungsbereitschaft=wiederholungsbereitschaft,
                stressfaktor=stressfaktor,
            )
            st.caption(f"Berechneter Motivationswert: {motivationswert:.1f} / 10")

            speichern = st.form_submit_button("Eingabe übernehmen")

        if speichern:
            # Persistenz + UI-Update: Abschluss speichern, lokalen Status setzen, Ansicht neu laden.
            json_repository.speichere_modulabschluss(
                modul=ausgewaehltes_modul,
                note=note,
                pruefungsform=pruefungsform,
                motivation=motivation,
                spassfaktor=spassfaktor,
                verstaendniswert=verstaendniswert,
                wiederholungsbereitschaft=wiederholungsbereitschaft,
                stressfaktor=stressfaktor,
                motivationswert=motivationswert,
            )

            ausgewaehltes_modul.abschliessen()

            st.success(
                f"Gespeichert für {ausgewaehltes_modul.name}: "
                f"Note {note:.1f}, Prüfungsform {pruefungsform}, "
                f"Motivationswert {motivationswert:.1f}/10"
            )
            st.rerun()

with col_rechts:
    # Rechte Spalte: Scoring-Bereich.
    render_section_heading(
        title="Motivations- & Empfehlungsranking",
        subtitle="Priorisierung offener Module nach Empfehlungsscore.",
        title_class="module-input-title",
        subtitle_class="module-input-subtitle",
    )

    if offene_module_anzahl == 0:
        st.info("Kein Scoring verfügbar, da aktuell keine offenen Module vorhanden sind.")
    else:
        top_eintrag = ranking[0]
        top_modul = top_eintrag.modul
        render_scoring_top_card(top_eintrag.score_prozent, top_modul.name, top_modul.modulcode)

        for index, eintrag in enumerate(ranking[:6], start=1):
            modul = eintrag.modul
            render_scoring_item(index, modul.name, modul.modulcode, eintrag.score_prozent)

render_section_heading(
    title="Module im Fokus",
    subtitle="Schnellansicht der ersten 12 Module mit aktuellem Bearbeitungsstatus.",
)

# Fokus-Module als kompakte 3-Spalten-Uebersicht (je 4 Karten) anzeigen.
col1, col2, col3 = st.columns(3)
module_anzeige = alle_module[:12]

with col1:
    for modul in module_anzeige[0:4]:
        render_module_card(modul.name, modul.status)

with col2:
    for modul in module_anzeige[4:8]:
        render_module_card(modul.name, modul.status)

with col3:
    for modul in module_anzeige[8:12]:
        render_module_card(modul.name, modul.status)
