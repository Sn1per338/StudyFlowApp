"""Oeffentliche Paket-API fuer Service-Funktionen."""

from .dashboard_metrics import (
    berechne_empfehlungsscore,
    berechne_ects_fortschritt,
    berechne_module_ranking,
    berechne_motivationswert,
    ermittle_offene_module,
    empfehlung_prozent_aus_score,
    ermittle_pruefungsformen,
    zaehle_offene_module,
)

__all__ = [
	"berechne_ects_fortschritt",
	"berechne_empfehlungsscore",
	"berechne_module_ranking",
	"berechne_motivationswert",
	"ermittle_offene_module",
	"empfehlung_prozent_aus_score",
	"ermittle_pruefungsformen",
	"zaehle_offene_module",
]
