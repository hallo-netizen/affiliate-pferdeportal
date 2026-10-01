# K10 – Pferdeatelier

Eigenständiger Entwicklungsbereich für Konzept 10.

## Harte Trennung
- K9-Produktion bleibt auf `hallo-netizen/affiliate-pferdeportal` / `konzept9/greenfield-20260929`.
- K10 arbeitet ausschließlich auf `konzept10-rule-ledger-20261001` und in dessen K10-Dateibaum.
- K10 enthält keine K9-Artikel, keine K9-Runtime, keine K9-Warehouse-Produkte, keine K9-Submissions und keine K9-Workflows.
- K10 kennt K9 nur über `K9_BASELINE_REFERENCE.json`.
- `publish_allowed=false`.

## K10-Prinzip
Ein zentraler Regelkatalog. Jede harte Regel hat genau einen zuständigen Prüfer. Nach erfolgreicher Prüfung wird ein hashgebundener Receipt/Haken erzeugt. Nachgelagerte Stationen prüfen nur noch Receipt, Identität, Vollständigkeit und Unverändertheit. Dieselbe Regel wird nicht erneut inhaltlich geprüft.

## Aktuelle Autorität
`CURRENT_STATE.json`
