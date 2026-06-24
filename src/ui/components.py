"""Wiederverwendbare UI-Renderer fuer die Streamlit-Oberflaeche."""

from datetime import datetime
from pathlib import Path
from html import escape

import streamlit as st


def _format_datum_de(wert: str) -> str:
    """Formatiert ein Datum für die Anzeige im deutschen Format TT.MM.JJJJ."""
    text = str(wert).strip()
    if not text:
        return text

    for format_string in ("%Y-%m-%d", "%d.%m.%Y"):
        try:
            datum = datetime.strptime(text, format_string)
            return datum.strftime("%d.%m.%Y")
        except ValueError:
            continue

    return text


def load_css(file_path: str) -> str:
    """Liest CSS-Inhalt aus einer Datei."""
    return Path(file_path).read_text(encoding="utf-8")


def apply_css(file_path: str) -> None:
    """Bindet eine CSS-Datei global in die Streamlit-Seite ein."""
    css = load_css(file_path)
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def render_hero_panel(
    studiengang_name: str,
    gesamt_ects: int | str,
    ziel_note: float | str,
    regelstudienzeit: int | str,
    abschlussart: str,
    enddatum_studium: str,
) -> None:
    """Rendert den Hero-Bereich mit Stammdaten des Studiengangs."""
    html = (
        '<div class="hero-panel">'
        '<div class="hero-kicker">Studienprofil</div>'
        f'<div class="hero-title">{escape(str(studiengang_name))}</div>'
        '<div class="hero-meta-row">'
        f'<span class="hero-chip">{escape(str(gesamt_ects))} ECTS</span>'
        f'<span class="hero-chip">Zielnote {escape(str(ziel_note))}</span>'
        f'<span class="hero-chip">{escape(str(regelstudienzeit))} Semester</span>'
        f'<span class="hero-chip">{escape(str(abschlussart))}</span>'
        f'<span class="hero-chip">Enddatum {escape(_format_datum_de(enddatum_studium))}</span>'
        "</div>"
        "</div>"
    )
    st.html(html)


def render_section_heading(
    title: str,
    subtitle: str | None = None,
    title_class: str = "section-heading",
    subtitle_class: str = "section-subtitle",
) -> None:
    """Rendert Abschnittstitel und optionalen Untertitel."""
    st.html(f'<div class="{escape(title_class)}">{escape(title)}</div>')
    if subtitle:
        st.html(f'<div class="{escape(subtitle_class)}">{escape(subtitle)}</div>')


def render_kpi_card(
    title: str,
    value: str,
    subtext: str,
    progress: float | None = None
) -> None:
    """Rendert eine KPI-Karte mit optionalem Fortschrittsbalken."""
    progress_html = ""

    if progress is not None:
        progress = max(0, min(progress, 100))
        progress_html = f"""
        <div class="progress-background">
            <div class="progress-fill" style="width: {progress:.0f}%;"></div>
        </div>
        """

    html = f"""
    <div class="kpi-card">
        <div class="kpi-title">{title}</div>
        <div class="kpi-value">{value}</div>
        {progress_html}
        <div class="kpi-subtext">{subtext}</div>
    </div>
    """

    st.html(html)


def render_module_card(name: str, status: str = "offen") -> None:
    """Rendert eine Modulkarte mit Status-Badge."""
    status_norm = str(status).strip().lower()

    if status_norm == "abgeschlossen":
        status_class = "module-status-done"
        status_label = "abgeschlossen"
    else:
        status_class = "module-status-open"
        status_label = "offen"

    html = f"""
    <div class="module-card">
        <div class="module-name">{escape(name)}</div>
        <span class="module-status {status_class}">{status_label}</span>
    </div>
    """

    st.html(html)


def render_scoring_top_card(score: int | float, modul_name: str, modulcode: str) -> None:
    """Rendert die Top-Score-Karte fuer das Modul-Ranking."""
    score_norm = max(0, min(float(score), 100))
    html = f"""
    <div class="scoring-top-card">
        <div class="scoring-top-kicker">Top-Score</div>
        <div class="scoring-top-value">{score_norm:.0f} %</div>
        <div class="progress-background">
            <div class="progress-fill" style="width: {score_norm:.0f}%;"></div>
        </div>
        <div class="scoring-top-subtext">Top-Modul: {escape(modul_name)} ({escape(modulcode)})</div>
    </div>
    """
    st.html(html)


def render_scoring_item(
    rank: int,
    modul_name: str,
    modulcode: str,
    score: int | float,
) -> None:
    """Rendert einen einzelnen Ranglisten-Eintrag im Scoring."""
    score_norm = max(0, min(float(score), 100))
    html = f"""
    <div class="scoring-item">
        <div class="scoring-item-head">
            <span class="scoring-rank">{int(rank)}.</span>
            <span class="scoring-name">{escape(modul_name)}</span>
            <span class="scoring-code">{escape(modulcode)}</span>
            <span class="scoring-score">{score_norm:.0f} %</span>
        </div>
        <div class="progress-background">
            <div class="progress-fill" style="width: {score_norm:.0f}%;"></div>
        </div>
    </div>
    """
    st.html(html)
