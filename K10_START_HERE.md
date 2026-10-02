# K10 – Pferdeatelier

Eigenständiger Produktionsbereich für Konzept 10.

## Harte Trennung
- K9-Produktion bleibt auf `hallo-netizen/affiliate-pferdeportal` / `konzept9/greenfield-20260929`.
- K10 arbeitet ausschließlich auf `konzept10-rule-ledger-20261001`.
- K10 kennt K9 nur read-only über `K9_BASELINE_REFERENCE.json`.
- `publish_allowed=false`.

## Normaler Artikelstart
Bei einer beigefügten `PSERC_TEXTMACHINE_METADATA_BATCH_V2`-Datei ist der Auftrag **reale Artikelproduktion**, kein Systemtest.

Verbindliche Reihenfolge:
`Recherche -> Schreiben -> generischer K10-Produktionsworkflow -> LanguageTool/Regeln/PSERC/ENDSTEMPEL -> verifizierte WordPress-Importdatei -> STOP`.

Der Chat darf **nicht** nach dem Schreiben antworten. Er muss den geschriebenen Artikel zusammen mit dem echten Research-Paket unter `real_runs/production/<job-id>/` an den vorhandenen generischen K10-Workflow übergeben und dessen Ergebnis bis zum terminalen Status verfolgen.

Artikelbefunde dürfen durch Überarbeitung des Artikels geschlossen werden. K10-Engine, Regeln und Architektur werden im normalen Artikelauftrag nicht repariert oder verändert.

## K10-Prinzip
Eine harte Regel -> genau ein Owner -> genau eine harte Prüfung -> genau ein hashgebundener Receipt. Danach nur Integrität/Vollständigkeit/Unverändertheit.

## Aktuelle Autorität
`CURRENT_STATE.json`

## Produktionsanweisung
`K10_PRODUCTION_ENTRY.md`
