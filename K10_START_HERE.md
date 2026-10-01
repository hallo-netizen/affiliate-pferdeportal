# K10 – Pferdeatelier

Eigenständiger Entwicklungsbereich für Konzept 10.

## Harte Trennung
- K9-Produktion bleibt unverändert auf `konzept9/greenfield-20260929`.
- K10 arbeitet ausschließlich auf `konzept10-rule-ledger-20261001`.
- Der K10-Dateibaum enthält keinen K9-Code, keine K9-Artikel, keine K9-Runtime und keine K9-Workflows.
- K9 wird nur read-only über den Baseline-Commit `2cc8167fa1e31b4ffa2ff76c9819314be4b98555` referenziert.
- `publish_allowed=false`.

## K10-Prinzip
Eine harte Regel wird genau einmal von genau einem Owner inhaltlich geprüft. Danach gilt nur noch der hashgebundene Receipt. Spätere Stationen prüfen Identität, Vollständigkeit, Katalog-Hash und Unverändertheit – nicht dieselbe Inhaltsregel erneut.
