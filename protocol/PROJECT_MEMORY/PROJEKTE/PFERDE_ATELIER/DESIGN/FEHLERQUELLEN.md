# PFERDE-ATELIER DESIGN – FEHLERQUELLEN

Keine zweite Fehlerwahrheit.

## V104 Tabellenabstand

GitHub-Autorität:
`design-baseline/2026-08-22/v101` bis `v104`

Lernkette:
- V101/V102/V103 = Zwischenstände;
- V104 = finaler nicht kollabierender Tabellenabstand-Fix mit HARD LOCAL QA/FULL CORPUS QA.

## Kategorietexte 1.50.470→1.50.472

GitHub:
`design-baseline/2026-08-31/`

Aktueller Endbeleg:
`v150472-category-intro-79/`

Wichtig:
Diese spätere Kette ändert laut MASTER_STATUS keine allgemeine Designregel, sondern nur Pferde-spezifische redaktionelle Kategorietexte/Loader.


## Kategorie-Reihenfolge 2026-09-07

STATUS:
**CLOSED / LIVE PASS**

AUFTRAG:
Auf der zentralen Kategorieebene sollten ausschließlich die **Affiliate-Produkte / Produktvorschläge** über die **Beitragsvorschau / Meistgelesen** gesetzt werden.

FEHLVERSUCHE:
- V1.50.473: REJECTED – Seitenstruktur unnötig umgebaut.
- V1.50.474: REJECTED – Artikel intern aufgeteilt.
- V1.50.475: REJECTED – falsche Elemente verschoben.
- V1.50.476: REJECTED – Affiliate-Banner statt Affiliate-Produkte verschoben.

URSACHE:
Der Auftrag wurde mehrfach interpretiert und erweitert, statt zwei exakt benannte bestehende Blöcke zu tauschen.

DAUERHAFTE REPARATUR DES ARBEITSWEGS:
Für lokale DESIGN-Miniänderungen ist der manuelle Patchweg gesperrt.
Verbindlich:
`MINIMAL_PATCH_RUNNER.py` + hashgebundener Job + Positiv-/Negativprüfung + Reversibilität.

FINALER JOB:
`DESIGN-ORDER-SWAP-002`

FINAL BESTÄTIGT:
- Affiliate-Produkte / Produktvorschläge stehen über der Beitragsvorschau.
- Affiliate-Banner bleibt unverändert.
- Artikel-/Verweisstruktur bleibt unverändert.
- Nutzer-LIVE-PASS auf „Gebisse“ am 2026-09-07.

TECHNISCHE ORIGINALBELEGE:
- `LIVE_PASS_DESIGN_ORDER_SWAP_002.md`
- `MINIMAL_PATCH_LAST_RECEIPT.json`
- historische Kandidatenbelege unter `design-baseline/2026-09-07/`

LEHRE:
**Bei Miniänderungen keine Interpretation: nur die ausdrücklich gebundene Transformation ausführen.**
