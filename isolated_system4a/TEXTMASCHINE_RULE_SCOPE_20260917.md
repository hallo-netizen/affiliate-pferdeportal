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

Technische Bindungs-/Integritätsregeln (Authoring Contract, SHA/Hashes, Package/Jar, Execution, Route/State, Batch, Release, WordPress, Handoff) bleiben fail-closed Voraussetzungen außerhalb der fachlichen Textregelmenge.

## Exakte erreichbare Projektregelmenge

### A. PPM 6.7.9 — 104 aktive Regel-Einträge
- `includes/content-validator.php`: 52
- `includes/content-structure-language-gate.php`: 34
- `includes/known-error-gate.php`: 14
- `includes/rendered-dom-validator.php; includes/content-structure-language-gate.php`: 4

Davon 100 `ACTIVE_VALIDATOR_BLOCKING_RULE` mit Fehlercode und 4 `WAVE4_EXACT_REQUIREMENT` mit gebundenem Positiv-/Negativtest.

### B. System-4 Content Guard — 30 im Fullcheck erreichbare Fehlerregeln
1. `FACT_PACK_OBJECT_REQUIRED`
2. `FACT_PACK_CONTRACT_INVALID`
3. `FACT_PACK_NOT_PRODUCTION_READY`
4. `FACT_PACK_SOURCES_MISSING`
5. `FACT_PACK_SOURCE_OBJECT_REQUIRED`
6. `FACT_PACK_SOURCE_ID_INVALID`
7. `FACT_PACK_SOURCE_TITLE_INVALID`
8. `FACT_PACK_SOURCE_URL_INVALID`
9. `FACT_PACK_SOURCE_RETRIEVED_AT_INVALID`
10. `FACT_PACK_SOURCE_HASH_INVALID`
11. `FACT_PACK_SOURCE_TITLE_SYNTHETIC`
12. `FACT_PACK_SOURCE_EVIDENCE_INVALID`
13. `FACT_PACK_SOURCE_HASH_MISMATCH`
14. `FACT_PACK_SOURCE_ID_DUPLICATE`
15. `FACT_PACK_CLAIMS_TOO_LOW`
16. `FACT_PACK_CLAIM_OBJECT_REQUIRED`
17. `FACT_ID_INVALID`
18. `FACT_SOURCE_ID_INVALID`
19. `FACT_STATEMENT_INVALID`
20. `FACT_EVIDENCE_TEXT_INVALID`
21. `FACT_EVIDENCE_HASH_INVALID`
22. `FACT_SOURCE_NOT_IN_RESEARCH`
23. `FACT_EVIDENCE_HASH_MISMATCH`
24. `FACT_EVIDENCE_NOT_IN_SOURCE`
25. `FACT_PACK_FACT_ID_DUPLICATE`
26. `FACT_PACK_CLAIM_SOURCE_URL_MISMATCH`
27. `ARTICLE_FACT_PACK_CLAIMS_MISSING`
28. `ARTICLE_FACT_IDS_MISSING`
29. `ARTICLE_UNKNOWN_FACT_ID`
30. `ARTICLE_FACT_TRACE_MISSING`

**Korrektur gegenüber dem ersten Snapshot:** `FACT_SOURCE_EVIDENCE_MISSING` ist zwar ein interner `_claim_core()`-Fehlercode, aber im echten `validate_single_article() -> validate_fact_pack() -> _pack_sources() -> _pack_claims()` nicht erreichbar. Fehlende Source-Evidence wird bereits vorher durch `_research_source()` als `FACT_PACK_SOURCE_EVIDENCE_INVALID` blockiert. Deshalb darf dieser Code nicht als eigenständige Fullcheck-Regel gezählt werden.

Die ersten 28 sind Fact-Pack-/Evidenz-Integrität und fail-closed; `ARTICLE_UNKNOWN_FACT_ID` und `ARTICLE_FACT_TRACE_MISSING` sind Draft-Realisation und writer-reparierbar.

### C. System-4 Design Guard — 16 diskrete Regeln
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
15. `DESIGN_TABLE_INLINE_STYLE_FORBIDDEN`
16. `DESIGN_BERATUNG_HEADING_LEVEL_FORBIDDEN`

### D. Externe Links — 2 diskrete Regeln
- `EXTERNAL_LINK_FORBIDDEN`
- `EXTERNAL_URL_FORBIDDEN`

### E. LanguageTool 6.8
Externer dynamischer Regelprüfer; Vendor-Rule-IDs werden nicht künstlich als Pferde-Atelier-Projektregeln dupliziert.
- 0 Findings = PASS
- >=1 Finding = Draft-Repair
- Jar/Worker/Execution/Reportfehler = technischer HARD BLOCK

## Ergebnis Punkt 1

**Exakte im Fullcheck erreichbare diskrete Pferde-Atelier-Textmaschinen-Regelmenge = 152 Regeln:**
- 104 PPM
- 30 Content Guard
- 16 Design Guard
- 2 External-Link-Regeln

Zusätzlich: LanguageTool 6.8 als real gebundener dynamischer externer Regelprüfer.

## Bekannte Implementierungslücke für Punkt 4/5
Die Klassifikation reparierbarer Content-/Design-Guard-Fehler existiert in `production_checks.guard_repair_finding()`, der aktuelle `controller.cmd_fullcheck()` behandelt `ContentGuardError` und `DesignGuardError` jedoch noch pauschal als `FULL_CHECK_HARD_BLOCK`. Diese Lücke muss in Punkt 7 minimal geschlossen werden.

## NEXT ACTION
Punkt 3: für alle 152 erreichbaren Projektregeln den gezielten Negativnachweis am echten Prüfer/exakten Fehlercode belegen; nur echte Lücken anschließend in Punkt 7 ergänzen.
