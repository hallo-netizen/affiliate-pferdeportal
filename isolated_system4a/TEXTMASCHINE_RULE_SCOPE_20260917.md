# SYSTEM 4A — EXAKTE TEXTMASCHINEN-REGELMENGE

Stand: 17.09.2026
Branch: `hobbyroom/system4a-textmachine-final-pass-20260916`
Zweck: Punkt 1 des eingeschlossenen Hobbyraum-Arbeitsauftrags.

## Harte Abgrenzung

Als **Textmaschinenregel** zählt hier nur eine fachliche/inhaltliche Regel, die im echten `controller.cmd_fullcheck()` auf dem Artikel bzw. seinem Fact-Pack ausgeführt wird.

Die reale Reihenfolge ist:

1. `content_guard.validate_single_article()`
2. `design_guard.validate_design_neutrality()`
3. `production_checks.run_all()` mit
   - `no_external_links()`
   - realem LanguageTool 6.8
   - echtem PPM 6.7.9 Content Validator

Nicht in die fachliche Textmaschinen-Regelmenge eingerechnet werden technische Bindungs-/Integritätsregeln wie Authoring-Contract-Bindung, Draft-SHA, Package-/Jar-Hash, Ausführungsfehler, Legacy-Runtime-Sperre, Route/State, Batch, Release, WordPress und Handoff. Diese bleiben weiterhin harte fail-closed Voraussetzungen, sind aber keine fachlichen Textregeln.

## Exakte diskrete Projektregelmenge

### A. PPM 6.7.9 — 104 aktive Regel-Einträge

Aus dem unveränderten PPM-6.7.9-Register `contracts/hard-rule-registry-v1.json` gehören **104 aktive Einträge** direkt zu den im echten Content-Fullcheck verwendeten Validatoren:

- `includes/content-validator.php`: 52
- `includes/content-structure-language-gate.php`: 34
- `includes/known-error-gate.php`: 14
- kombiniert `includes/rendered-dom-validator.php; includes/content-structure-language-gate.php`: 4

Davon:
- 100 = `ACTIVE_VALIDATOR_BLOCKING_RULE` mit konkretem Fehlercode
- 4 = `WAVE4_EXACT_REQUIREMENT` ohne eigenen einzelnen Fehlercode, aber mit gebundenem Positiv-/Negativtest an denselben Textvalidatoren

### B. System-4 Content Guard — 31 diskrete Fullcheck-Fehlerregeln

`validate_single_article()` ruft `validate_fact_pack()` und `validate_article_fact_ids()` auf. Im tatsächlich erreichbaren Fullcheck-Pfad ergeben sich **31 eindeutige Fehlercode-Basen**:

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
24. `FACT_SOURCE_EVIDENCE_MISSING`
25. `FACT_EVIDENCE_NOT_IN_SOURCE`
26. `FACT_PACK_FACT_ID_DUPLICATE`
27. `FACT_PACK_CLAIM_SOURCE_URL_MISMATCH`
28. `ARTICLE_FACT_PACK_CLAIMS_MISSING`
29. `ARTICLE_FACT_IDS_MISSING`
30. `ARTICLE_UNKNOWN_FACT_ID`
31. `ARTICLE_FACT_TRACE_MISSING`

Die ersten 29 sind Fact-Pack-/Evidenz-Integrität und daher fail-closed. `ARTICLE_UNKNOWN_FACT_ID` und `ARTICLE_FACT_TRACE_MISSING` sind Draft-Realisation und damit writer-reparierbar.

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

Aktuell semantisch writer-reparierbar klassifiziert sind 9 davon: Body leer, Root fehlt, PPM-Klasse fehlt, Typklasse fehlt, Typattribut falsch, verschachteltes Article, beide Tabellenklassen sowie Beratung-Heading-Level. Die übrigen 7 bleiben Integritäts-/Sicherheits-Hard-Block.

### D. Externe Links — 2 diskrete Regeln

- `EXTERNAL_LINK_FORBIDDEN`
- `EXTERNAL_URL_FORBIDDEN`

Beide sind Draft-Realisation und gehen an `DRAFT_WORKER`.

### E. LanguageTool 6.8

LanguageTool ist ein **externer regelbasierter Prüfer mit dynamischen internen Rule-IDs**, kein Pferde-Atelier-Hard-Rule-Register. Deshalb werden seine internen Vendor-Regeln nicht künstlich als Projektregel-IDs dupliziert.

Der Projektvertrag ist genau einheitlich:
- 0 LT-Findings = PASS
- >=1 echtes LT-Finding = `RepairRequired("languagetool", ...)` -> `DRAFT_WORKER`
- LT/Jar/Worker/Execution-/Reportfehler = technischer HARD BLOCK, nicht Textreparatur

## Ergebnis Punkt 1

**Exakte diskrete Pferde-Atelier-Textmaschinen-Regelmenge = 153 Regeln:**

- 104 PPM
- 31 Content Guard
- 16 Design Guard
- 2 External-Link-Regeln

Zusätzlich ist LanguageTool 6.8 als externer dynamischer Regelprüfer vollständig im Fullcheck gebunden; seine Vendor-Rule-IDs sind nicht Teil der 153 Projektregeln.

## Bekannte Implementierungslücke für Punkt 4/5

Die Klassifikation für reparierbare Content-/Design-Guard-Fehler existiert bereits in `production_checks.guard_repair_finding()`. Der aktuelle `controller.cmd_fullcheck()` fängt `ContentGuardError` und `DesignGuardError` jedoch noch pauschal als `FULL_CHECK_HARD_BLOCK` ab. Damit ist Punkt 4/5 **noch nicht PASS**: die vorhandene Repair-Klassifikation muss im Controller tatsächlich verwendet und negativ getestet werden.

## NEXT ACTION

Punkt 2: Für alle 153 Projektregeln den vorhandenen realen Positivnachweis bestimmen. Parallel darf die oben dokumentierte Controller-Lücke erst in Punkt 7 minimal geschlossen werden; vorher keine vorgezogene Architekturänderung.