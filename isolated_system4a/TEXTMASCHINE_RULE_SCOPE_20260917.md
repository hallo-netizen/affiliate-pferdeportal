# SYSTEM 4A — EXAKTE TEXTMASCHINEN-REGELMENGE

Stand: 17.09.2026
Branch: `hobbyroom/system4a-textmachine-final-pass-20260916`
Zweck: Punkt 1 des eingeschlossenen Hobbyraum-Arbeitsauftrags.

## Harte Abgrenzung

Als **Textmaschinenregel** zählt nur eine fachliche/inhaltliche Regel, die im echten `controller.cmd_fullcheck()` auf Artikel bzw. Fact-Pack tatsächlich erreichbar ausgeführt wird.

Reale Reihenfolge:
1. `content_guard.validate_single_article()`
2. `design_guard.validate_design_neutrality()`
3. `production_checks.run_all()` mit External-Link-Prüfung, LanguageTool 6.8 und PPM 6.7.9 Content Validator.

Technische Bindungs-/Integritätsregeln bleiben fail-closed Voraussetzungen außerhalb der fachlichen Textregelmenge.

## Exakte erreichbare Projektregelmenge

### A. PPM 6.7.9 — 104 aktive Regel-Einträge
- `includes/content-validator.php`: 52
- `includes/content-structure-language-gate.php`: 34
- `includes/known-error-gate.php`: 14
- kombiniert Rendered-DOM/Content-Structure: 4

### B. System-4 Content Guard — 30 erreichbare Fehlerregeln
`FACT_PACK_OBJECT_REQUIRED`, `FACT_PACK_CONTRACT_INVALID`, `FACT_PACK_NOT_PRODUCTION_READY`, `FACT_PACK_SOURCES_MISSING`, `FACT_PACK_SOURCE_OBJECT_REQUIRED`, `FACT_PACK_SOURCE_ID_INVALID`, `FACT_PACK_SOURCE_TITLE_INVALID`, `FACT_PACK_SOURCE_URL_INVALID`, `FACT_PACK_SOURCE_RETRIEVED_AT_INVALID`, `FACT_PACK_SOURCE_HASH_INVALID`, `FACT_PACK_SOURCE_TITLE_SYNTHETIC`, `FACT_PACK_SOURCE_EVIDENCE_INVALID`, `FACT_PACK_SOURCE_HASH_MISMATCH`, `FACT_PACK_SOURCE_ID_DUPLICATE`, `FACT_PACK_CLAIMS_TOO_LOW`, `FACT_PACK_CLAIM_OBJECT_REQUIRED`, `FACT_ID_INVALID`, `FACT_SOURCE_ID_INVALID`, `FACT_STATEMENT_INVALID`, `FACT_EVIDENCE_TEXT_INVALID`, `FACT_EVIDENCE_HASH_INVALID`, `FACT_SOURCE_NOT_IN_RESEARCH`, `FACT_EVIDENCE_HASH_MISMATCH`, `FACT_EVIDENCE_NOT_IN_SOURCE`, `FACT_PACK_FACT_ID_DUPLICATE`, `FACT_PACK_CLAIM_SOURCE_URL_MISMATCH`, `ARTICLE_FACT_PACK_CLAIMS_MISSING`, `ARTICLE_FACT_IDS_MISSING`, `ARTICLE_UNKNOWN_FACT_ID`, `ARTICLE_FACT_TRACE_MISSING`.

`FACT_SOURCE_EVIDENCE_MISSING` wird nicht gezählt, weil im echten Fullcheck fehlende Source-Evidence bereits vorher als `FACT_PACK_SOURCE_EVIDENCE_INVALID` blockiert wird.

### C. System-4 Design Guard — 15 erreichbare Regeln
1. `DESIGN_ARTICLE_TYPE_TOKEN_INVALID`
2. `DESIGN_BODY_EMPTY`
3. `DESIGN_ARTICLE_TYPE_MISSING`
4. `DESIGN_ACTIVE_OR_GLOBAL_HTML_FORBIDDEN`
5. `DESIGN_INLINE_STYLE_FORBIDDEN`
6. `DESIGN_EVENT_HANDLER_FORBIDDEN`
7. `DESIGN_JAVASCRIPT_URL_FORBIDDEN`
8. `DESIGN_CANONICAL_ARTICLE_ROOT_MISSING`
9. `DESIGN_PPM_GENERATED_CLASS_MISSING`
10. `DESIGN_ARTICLE_TYPE_CLASS_MISSING`
11. `DESIGN_ARTICLE_TYPE_ATTRIBUTE_MISMATCH`
12. `DESIGN_NESTED_ARTICLE_FORBIDDEN`
13. `DESIGN_TABLE_SYSTEM129_CLASS_MISSING`
14. `DESIGN_TABLE_COMPARISON_CLASS_MISSING`
15. `DESIGN_BERATUNG_HEADING_LEVEL_FORBIDDEN`

**Nicht als eigene erreichbare Regel gezählt:** `DESIGN_TABLE_INLINE_STYLE_FORBIDDEN`. Der generische Prüfer `DESIGN_INLINE_STYLE_FORBIDDEN` läuft vorher und blockiert jedes Tabellen-`style=` bereits. Remote-Negativlauf `35195117339` hat diese Unreachable-Reihenfolge real offengelegt.

### D. Externe Links — 2 Regeln
- `EXTERNAL_LINK_FORBIDDEN`
- `EXTERNAL_URL_FORBIDDEN`

### E. LanguageTool 6.8
Externer dynamischer Regelprüfer; Vendor-Rule-IDs werden nicht als Pferde-Atelier-Projektregeln dupliziert.

## Ergebnis Punkt 1

**Exakte im Fullcheck erreichbare diskrete Pferde-Atelier-Textmaschinen-Regelmenge = 151 Regeln:**
- 104 PPM
- 30 Content Guard
- 15 Design Guard
- 2 External-Link-Regeln

Zusätzlich: LanguageTool 6.8 als real gebundener dynamischer externer Regelprüfer.

## Beleg für die Korrektur
- Roter Erkenntnislauf: `System 4A Repair Owner Contract`, Run `35195117339`, Head `9ce3bbac707227d2dd25b4540ce78f4edcf411eb`: erwartetes `DESIGN_TABLE_INLINE_STYLE_FORBIDDEN`, tatsächlich früheres `DESIGN_INLINE_STYLE_FORBIDDEN`.
- Korrigierter Lauf: Run `35195339914`, Head `50b4502159b08196494e7da9f69ece26e81e8d6b`, SUCCESS.

## NEXT ACTION
Punkt 7: ausschließlich die noch offenen 49 PPM-Negativbeweislücken schließen.
