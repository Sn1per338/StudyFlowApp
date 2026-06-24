"""Hilfsfunktionen fuer Dashboard-Kennzahlen und Modullisten."""

from collections.abc import Iterable
from statistics import mean

from src.models import ModulEmpfehlung, ModulStatus


DEFAULT_PRUEFUNGSFORMEN = [
    "Klausur",
    "Hausarbeit",
    "Portfolio",
    "Projektpräsentation",
]


def berechne_ects_fortschritt(credits_ist: int | float, credits_soll: int | float) -> float:
    """Berechnet den ECTS-Fortschritt in Prozent."""
    if credits_soll <= 0:
        return 0.0
    return float(credits_ist) / float(credits_soll) * 100


def ermittle_offene_module(alle_module: Iterable) -> list:
    """Filtert alle noch offenen Module."""
    return [modul for modul in alle_module if modul.ist_offen()]


def zaehle_offene_module(alle_module: Iterable) -> int:
    """Zaehlt alle offenen Module."""
    return len(ermittle_offene_module(alle_module))


def ermittle_pruefungsformen(
    module: Iterable,
    fallback: list[str] | None = None,
) -> list[str]:
    """Liefert sortierte, eindeutige Pruefungsformen mit Fallback."""
    pruefungsformen = sorted({
        str(modul.pruefungsleistung).strip()
        for modul in module
        if modul.pruefungsleistung is not None and str(modul.pruefungsleistung).strip()
    })

    if pruefungsformen:
        return pruefungsformen

    if fallback is not None:
        return fallback

    return list(DEFAULT_PRUEFUNGSFORMEN)


def clamp_wert(wert: int | float, minimum: float = 0.0, maximum: float = 10.0) -> float:
    """Begrenzt einen numerischen Wert auf ein Intervall."""
    return max(minimum, min(float(wert), maximum))


def berechne_motivationswert(
    spassfaktor: int | float,
    verstaendniswert: int | float,
    wiederholungsbereitschaft: int | float,
    stressfaktor: int | float,
) -> float:
    """Berechnet den Motivationswert nach gewichteter Formel (Skala 0..10)."""
    motivationswert = (
        0.40 * clamp_wert(spassfaktor)
        + 0.30 * clamp_wert(verstaendniswert)
        + 0.20 * clamp_wert(wiederholungsbereitschaft)
        + 0.10 * (10.0 - clamp_wert(stressfaktor))
    )
    return clamp_wert(motivationswert)


def berechne_empfehlungsscore(
    modulart_aehnlichkeit: int | float,
    pruefungsform_aehnlichkeit: int | float,
    notenerfolg: int | float,
    motivationswert: int | float,
    studienrelevanz: int | float,
) -> float:
    """Berechnet den Empfehlungsscore nach gewichteter Formel (Skala 0..10)."""
    score = (
        0.30 * clamp_wert(modulart_aehnlichkeit)
        + 0.25 * clamp_wert(pruefungsform_aehnlichkeit)
        + 0.20 * clamp_wert(notenerfolg)
        + 0.20 * clamp_wert(motivationswert)
        + 0.05 * clamp_wert(studienrelevanz)
    )
    return clamp_wert(score)


def empfehlung_prozent_aus_score(empfehlungsscore: int | float) -> float:
    """Wandelt einen Empfehlungsscore (0..10) in Prozent (0..100) um."""
    return clamp_wert(empfehlungsscore) * 10.0


def berechne_module_ranking(
    offene_module: Iterable,
    alle_module: Iterable,
    historien_eintraege: Iterable[dict],
) -> list[ModulEmpfehlung]:
    """
    Erstellt ein Ranking offener Module auf Basis abgeschlossener Historie.

    Rueckgabe: sortierte Liste von ModulEmpfehlung-Objekten.
    """
    offene_liste = list(offene_module)
    if not offene_liste:
        return []

    alle_module_liste = list(alle_module)
    abgeschlossene = _filtere_abgeschlossene_eintraege(historien_eintraege)

    modulart_counts: dict[str, int] = {}
    pruefungsform_counts: dict[str, int] = {}
    note_scores_global: list[float] = []
    motivation_global: list[float] = []
    note_scores_modulart: dict[str, list[float]] = {}
    motivation_modulart: dict[str, list[float]] = {}

    for eintrag in abgeschlossene:
        modulart = _norm_text(eintrag.get("modulart"))
        pruefungsform = _kanonische_pruefungsform(eintrag.get("pruefungsform") or eintrag.get("pruefungsleistung"))

        if modulart:
            modulart_counts[modulart] = modulart_counts.get(modulart, 0) + 1

        if pruefungsform:
            pruefungsform_counts[pruefungsform] = pruefungsform_counts.get(pruefungsform, 0) + 1

        note_score = _note_zu_erfolgsscore(eintrag.get("note"))
        if note_score is not None:
            note_scores_global.append(note_score)
            if modulart:
                note_scores_modulart.setdefault(modulart, []).append(note_score)

        motivationswert = _motivationswert_aus_eintrag(eintrag)
        if motivationswert is not None:
            motivation_global.append(motivationswert)
            if modulart:
                motivation_modulart.setdefault(modulart, []).append(motivationswert)

    max_modulart_count = max(modulart_counts.values(), default=0)
    max_pruefungsform_count = max(pruefungsform_counts.values(), default=0)
    global_note = mean(note_scores_global) if note_scores_global else 5.0
    global_motivation = mean(motivation_global) if motivation_global else 5.0
    max_ects = max((float(getattr(modul, "ects", 0) or 0) for modul in alle_module_liste), default=0)

    ranking: list[ModulEmpfehlung] = []
    for modul in offene_liste:
        modulart = _norm_text(getattr(modul, "modulart", ""))
        pruefungsform = _kanonische_pruefungsform(getattr(modul, "pruefungsleistung", ""))

        if max_modulart_count > 0 and modulart:
            modulart_aehnlichkeit = (modulart_counts.get(modulart, 0) / max_modulart_count) * 10.0
        else:
            modulart_aehnlichkeit = 5.0

        if max_pruefungsform_count > 0 and pruefungsform:
            pruefungsform_aehnlichkeit = (pruefungsform_counts.get(pruefungsform, 0) / max_pruefungsform_count) * 10.0
        else:
            pruefungsform_aehnlichkeit = 5.0

        if modulart in note_scores_modulart and note_scores_modulart[modulart]:
            notenerfolg = mean(note_scores_modulart[modulart])
        else:
            notenerfolg = global_note

        if modulart in motivation_modulart and motivation_modulart[modulart]:
            motivationswert = mean(motivation_modulart[modulart])
        else:
            motivationswert = global_motivation

        ects = float(getattr(modul, "ects", 0) or 0)
        if max_ects > 0:
            studienrelevanz = (ects / max_ects) * 10.0
        else:
            studienrelevanz = 5.0

        score_0_10 = berechne_empfehlungsscore(
            modulart_aehnlichkeit=modulart_aehnlichkeit,
            pruefungsform_aehnlichkeit=pruefungsform_aehnlichkeit,
            notenerfolg=notenerfolg,
            motivationswert=motivationswert,
            studienrelevanz=studienrelevanz,
        )

        ranking.append(
            ModulEmpfehlung(
                modul=modul,
                score=score_0_10,
                begruendung="Automatisch berechnet aus Historie, Motivation und Studienrelevanz.",
            )
        )

    return sorted(ranking, key=lambda eintrag: eintrag.score_prozent, reverse=True)


def _norm_text(wert) -> str:
    """Normalisiert Text fuer robuste Vergleiche."""
    return str(wert or "").strip().lower()


def _kanonische_pruefungsform(wert) -> str:
    """Mappt freie Pruefungsform-Texte auf kanonische Kategorien."""
    text = _norm_text(wert)
    if not text:
        return ""
    if "klausur" in text:
        return "klausur"
    if "hausarbeit" in text:
        return "hausarbeit"
    if "portfolio" in text:
        return "portfolio"
    if "präsentation" in text or "praesentation" in text:
        return "praesentation"
    if "workbook" in text:
        return "workbook"
    return text


def _note_zu_erfolgsscore(note) -> float | None:
    """Wandelt eine Note (1.0..5.0) in einen Erfolgsscore (0..10) um."""
    if note is None:
        return None
    try:
        note_f = float(note)
    except (TypeError, ValueError):
        return None
    # Deutsche Notenskala: 1.0 (sehr gut) bis 5.0 (nicht bestanden).
    return clamp_wert((5.0 - note_f) / 4.0 * 10.0)


def _motivationswert_aus_eintrag(eintrag: dict) -> float | None:
    """Extrahiert einen Motivationswert aus einem Historien-Eintrag."""
    if not isinstance(eintrag, dict):
        return None

    hat_faktoren = any(
        schluessel in eintrag
        for schluessel in ("spassfaktor", "verstaendniswert", "wiederholungsbereitschaft", "stressfaktor")
    )

    if hat_faktoren:
        try:
            return berechne_motivationswert(
                spassfaktor=float(eintrag.get("spassfaktor", 5)),
                verstaendniswert=float(eintrag.get("verstaendniswert", 5)),
                wiederholungsbereitschaft=float(eintrag.get("wiederholungsbereitschaft", 5)),
                stressfaktor=float(eintrag.get("stressfaktor", 5)),
            )
        except (TypeError, ValueError):
            pass

    motivationswert = eintrag.get("motivationswert")
    if motivationswert is not None:
        try:
            return clamp_wert(float(motivationswert))
        except (TypeError, ValueError):
            pass

    motivation = eintrag.get("motivation")
    if motivation is not None:
        try:
            # Legacy-Feld wird als 1..10 interpretiert.
            return clamp_wert(float(motivation))
        except (TypeError, ValueError):
            return None

    return None


def _filtere_abgeschlossene_eintraege(historien_eintraege: Iterable[dict]) -> list[dict]:
    """Filtert nur abgeschlossene Eintraege aus der Historie."""
    return [
        eintrag
        for eintrag in historien_eintraege
        if isinstance(eintrag, dict) and _norm_text(eintrag.get("status")) == ModulStatus.ABGESCHLOSSEN.value
    ]
