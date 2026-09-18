# SYSTEM 4A — FEHLERKLASSIFIKATION TEXTMASCHINE

Stand: 17.09.2026
Branch: `hobbyroom/system4a-textmachine-final-pass-20260916`
Zweck: Punkt 4 des eingeschlossenen Hobbyraum-Arbeitsauftrags.

## Ergebnis

Alle **151 erreichbaren Projekt-Textmaschinenregeln** sind eindeutig klassifiziert:
- **102 reparierbar** -> definierter Repair-Owner
- **49 terminal/fail-closed** -> `HARD_BLOCK`
- LanguageTool 6.8 separat: echtes Sprachfinding -> `DRAFT_WORKER`; technische LT-Ausführungs-/Hash-/Reportfehler -> `HARD_BLOCK`.

## A. PPM 6.7.9 — 104/104
PPM: **89 Repair / 15 HARD_BLOCK**.

Repair-Verteilung:
- 83 -> `DRAFT_WORKER`
- 3 -> `PARENT_TITLE_MACHINE`
- 2 -> `PORTAL_LINK_MACHINE`
- 1 -> `PARENT_CATEGORY_MACHINE`

Terminal: Vertrags-, Hash-, Evidenz- und Validatorbindungsfehler einschließlich der 15 bereits festgelegten PPM-Hard-Regel-Einträge.

## B. Content Guard — 30/30
- **2 Repair -> DRAFT_WORKER:** `ARTICLE_UNKNOWN_FACT_ID`, `ARTICLE_FACT_TRACE_MISSING`
- **28 HARD_BLOCK**: Fact-Pack-/Evidenz-/Bindungsintegrität.

## C. Design Guard — 15/15 erreichbare Regeln
- **9 Repair -> DRAFT_WORKER:** `DESIGN_BODY_EMPTY`, `DESIGN_CANONICAL_ARTICLE_ROOT_MISSING`, `DESIGN_PPM_GENERATED_CLASS_MISSING`, `DESIGN_ARTICLE_TYPE_CLASS_MISSING`, `DESIGN_ARTICLE_TYPE_ATTRIBUTE_MISMATCH`, `DESIGN_NESTED_ARTICLE_FORBIDDEN`, `DESIGN_TABLE_SYSTEM129_CLASS_MISSING`, `DESIGN_TABLE_COMPARISON_CLASS_MISSING`, `DESIGN_BERATUNG_HEADING_LEVEL_FORBIDDEN`.
- **6 HARD_BLOCK:** `DESIGN_ARTICLE_TYPE_TOKEN_INVALID`, `DESIGN_ARTICLE_TYPE_MISSING`, `DESIGN_ACTIVE_OR_GLOBAL_HTML_FORBIDDEN`, `DESIGN_INLINE_STYLE_FORBIDDEN`, `DESIGN_EVENT_HANDLER_FORBIDDEN`, `DESIGN_JAVASCRIPT_URL_FORBIDDEN`.

`DESIGN_TABLE_INLINE_STYLE_FORBIDDEN` ist kein eigener erreichbarer Fehlerpfad, weil vorher bereits `DESIGN_INLINE_STYLE_FORBIDDEN` blockiert. Es wird daher nicht mehr gezählt.

## D. External Links — 2/2
- `EXTERNAL_LINK_FORBIDDEN` -> `DRAFT_WORKER`
- `EXTERNAL_URL_FORBIDDEN` -> `DRAFT_WORKER`

## Kontrollsumme
- PPM: 89 Repair + 15 Hard = 104
- Content Guard: 2 Repair + 28 Hard = 30
- Design Guard: 9 Repair + 6 Hard = 15
- External Links: 2 Repair = 2
- **Gesamt: 102 Repair + 49 Hard = 151**

## Remote Hard-Block-Beleg
`test_textmachine_hardblock_matrix.py` bindet alle **49/49 erreichbaren terminalen Regeln** an die echte Klassifikations-/Controller-Grenze.
Workflow `System 4A Repair Owner Contract`, Run `35195339914`, Head `50b4502159b08196494e7da9f69ece26e81e8d6b`, SUCCESS.

## NEXT ACTION
Punkt 5/7: die noch fehlenden 49 PPM-Negativbeweise schließen und damit die per-Regel-Owner/Rückweg-Bindung vervollständigen.
