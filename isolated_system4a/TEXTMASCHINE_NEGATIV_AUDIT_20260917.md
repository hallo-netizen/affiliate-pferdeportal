# SYSTEM 4A — NEGATIVBEWEIS-AUDIT TEXTMASCHINE

Stand: 17.09.2026
Branch: `hobbyroom/system4a-textmachine-final-pass-20260916`
Zweck: Punkt 3 des eingeschlossenen Hobbyraum-Arbeitsauftrags.

## Ergebnis

Alle **152 im Fullcheck erreichbaren Projekt-Textmaschinenregeln** wurden gegen vorhandene Negativbelege geprüft.

Kriterium für `EXAKT_VORHANDEN`: der vorhandene Test/Mutationstest nennt bzw. erwartet den konkreten Fehlercode am echten Prüfer. Ein bloßer Registereintrag oder ein grüner Sammeltest reicht nicht.

**Bestand:**
- 65/152: exakter vorhandener Negativbeleg gefunden.
- 87/152: kein ausreichend exakter Einzelregel-Negativbeleg gefunden -> echte Lücke für Punkt 7.

Damit ist Punkt 3 als **Audit** abgeschlossen, aber der Negativbeweis selbst noch nicht vollständig PASS. Punkt 7 muss genau die 87 Lücken schließen.

## A. PPM 6.7.9 — 104 Regeln

### EXAKT_VORHANDEN: 55/104
- 35 Regeln: Registry-Feld `direct_negative_test_mentions_error_code=true`; der gebundene Negativtest nennt den exakten Fehlercode.
- 19 weitere Regeln: `tests/fixtures/wave2/mutations-index.json` bindet eine konkrete Mutation direkt an `expected_error_code`.
- 1 weitere Regel: `BLOCKED_CONTENT_REQUIRED_BLOCK_MISSING` wird in den realen Three-Type-Negativtests konkret erwartet.

### LÜCKE: 45 aktive Blocking-Regeln ohne ausreichend exakten Einzelregel-Negativbeleg
- `CODE::79ded7cc3da55813` — `BLOCKED_WAVE2_CONTRACT_MISSING`
- `CODE::6b168e832adc1a68` — `BLOCKED_WAVE2_INTERNAL_MARKER_MISSING`
- `CODE::0cc1b289fde9cc7c` — `BLOCKED_WAVE2_INTRO_NOT_FIRST`
- `CODE::4fb61887a06711b8` — `BLOCKED_WAVE2_HEADING_LENGTH`
- `CODE::59a6c4a25cf46eca` — `BLOCKED_WAVE2_LINK_REGISTRY_HASH`
- `CODE::7887c9aae2a9cc0e` — `BLOCKED_WAVE2_INTERNAL_LINK_COUNT`
- `CODE::6b5cb1d05ddcea8e` — `BLOCKED_WAVE2_INTERNAL_LINK_ROLE_MISSING`
- `CODE::63535e13beb64c8c` — `BLOCKED_WAVE2_BOUND_LINK_MISSING`
- `CODE::541bb2884cd6e949` — `BLOCKED_WAVE2_INTERNAL_LINK_TARGET`
- `CODE::bc0b298d4b3141ed` — `BLOCKED_WAVE2_FURTHER_INFORMATION_LINK`
- `CODE::e59d7668d197fd19` — `BLOCKED_WAVE2_LINKS_NOT_DISTRIBUTED`
- `CODE::3c00ae08a16fbb04` — `BLOCKED_MAINBLOCK1_LANGUAGE_DELTA_EVIDENCE`
- `CODE::80b908b0c053b899` — `BLOCKED_VALIDATION_CONTRACT_VERSION_UNKNOWN`
- `CODE::6345716fff5ece77` — `BLOCKED_CONTENT_TYPE_DEFINITION_MISSING`
- `CODE::7a360734cec5ed46` — `BLOCKED_CONTENT_HASH_MISMATCH`
- `CODE::2bbe9872d3d9b521` — `BLOCKED_CONTENT_TABLE_COUNT`
- `CODE::3d6a7e9146649e88` — `BLOCKED_CONTENT_VISIBLE_LINK_COUNT`
- `CODE::7df037dde178bd1c` — `BLOCKED_CONTENT_FAQ_TITLE_QUESTION_MARK`
- `CODE::d041791134eb51c2` — `BLOCKED_CONTENT_TITLE_COLON`
- `CODE::10b54313009ddbda` — `BLOCKED_CONTENT_TARGET_KEYWORD_TITLE`
- `CODE::3c26d1a0184264bf` — `BLOCKED_CONTENT_FORBIDDEN_MACHINE_STATUS_WORD`
- `CODE::fffed240ecd54156` — `BLOCKED_CONTENT_SOURCE_TRACE_COUNT`
- `CODE::03a92f3f0c73d6e3` — `BLOCKED_CONTENT_SOURCE_TRACE_FIELDS`
- `CODE::b0c5da00bb146141` — `BLOCKED_CONTENT_PLACEHOLDER_SOURCE_TITLE`
- `CODE::5ad7933f8fe0b5e2` — `BLOCKED_CONTENT_DUMMY_SOURCE_HASH`
- `CODE::088d091843ab8bd0` — `BLOCKED_CONTENT_REQUIRED_BLOCK_EMPTY`
- `CODE::fcfe56a35a6b7649` — `BLOCKED_CONTENT_SOURCE_LABEL_OPTION_MISMATCH`
- `CODE::1c2556fa5197bafe` — `BLOCKED_CONTENT_TRACE_FACT_BINDING`
- `CODE::6c2b5fd1d7d217b3` — `BLOCKED_VALIDATION_CONTRACT_VERSION_MISSING`
- `CODE::33582cf3a8c1b23e` — `BLOCKED_SECTION_REQUIREMENTS_HASH_MISMATCH`
- `CODE::cad611712c6fd66f` — `BLOCKED_VALIDATION_CONTRACT_VERSION_UNKNOWN`
- `CODE::5b2e6c92fd5d21f2` — `BLOCKED_CONTENT_SECTION_DUPLICATE`
- `CODE::15fb102d6ae830a9` — `BLOCKED_CONTENT_REQUIRED_SECTION_MISSING`
- `CODE::9523b761b0c32771` — `BLOCKED_CONTENT_SECTION_ORDER`
- `CODE::a9683c1aaff7bc84` — `BLOCKED_CONTENT_REQUIRED_SECTION_MISSING`
- `CODE::e720ceb321185ff4` — `BLOCKED_CONTENT_REQUIRED_SECTION_MISSING`
- `CODE::dffa4f864d58c10e` — `BLOCKED_CONTENT_REQUIRED_SECTION_MISSING`
- `CODE::57299a61510fe9f0` — `BLOCKED_CONTENT_REQUIRED_TABLE_MISSING`
- `CODE::5c01d193adf04de2` — `BLOCKED_CONTENT_FORBIDDEN_TABLE_PRESENT`
- `CODE::fe5bb9ad9627441c` — `BLOCKED_CONTENT_TABLE_STRUCTURE`
- `CODE::87c6e350736dda9d` — `BLOCKED_CONTENT_TABLE_STRUCTURE`
- `CODE::80149dc474a98868` — `BLOCKED_CONTENT_UNBOUND_INTERNAL_LINK`
- `CODE::cfb3979ec12847df` — `BLOCKED_CONTENT_BOUND_LINK_MISSING`
- `CODE::c64fe59d56bffb96` — `BLOCKED_KNOWN_ERROR_CONTRACT_MISSING`
- `CODE::bf51d9f9d16bd30f` — `BLOCKED_KNOWN_DUPLICATE_HEADING`

### LÜCKE: 4 WAVE4-Anforderungen ohne eigenen Einzel-Fehlercode
Die vier Regeln sind an einen Sammel-Mutationstest gebunden, besitzen aber keinen eigenen `error_code`; damit fehlt nach dem harten Kriterium der individuelle Negativbeweis:
- `W4::R8-0786`
- `W4::R8-0787`
- `W4::R8-0788`
- `W4::R8-0790`

PPM gesamt: **55 exakt vorhanden / 49 Lücken**.

## B. Content Guard — 30 erreichbare Regeln

Vorhandene konkrete Negativtests nennen fünf relevante Fehlercodes am echten Content Guard:
- `FACT_SOURCE_NOT_IN_RESEARCH`
- `FACT_EVIDENCE_NOT_IN_SOURCE`
- `FACT_PACK_SOURCES_MISSING`
- `FACT_PACK_SOURCE_EVIDENCE_INVALID`
- `ARTICLE_UNKNOWN_FACT_ID`

Damit: **5 exakt vorhanden / 25 Lücken**.

Die 25 Lücken sind:
`FACT_PACK_OBJECT_REQUIRED`, `FACT_PACK_CONTRACT_INVALID`, `FACT_PACK_NOT_PRODUCTION_READY`, `FACT_PACK_SOURCE_OBJECT_REQUIRED`, `FACT_PACK_SOURCE_ID_INVALID`, `FACT_PACK_SOURCE_TITLE_INVALID`, `FACT_PACK_SOURCE_URL_INVALID`, `FACT_PACK_SOURCE_RETRIEVED_AT_INVALID`, `FACT_PACK_SOURCE_HASH_INVALID`, `FACT_PACK_SOURCE_TITLE_SYNTHETIC`, `FACT_PACK_SOURCE_HASH_MISMATCH`, `FACT_PACK_SOURCE_ID_DUPLICATE`, `FACT_PACK_CLAIMS_TOO_LOW`, `FACT_PACK_CLAIM_OBJECT_REQUIRED`, `FACT_ID_INVALID`, `FACT_SOURCE_ID_INVALID`, `FACT_STATEMENT_INVALID`, `FACT_EVIDENCE_TEXT_INVALID`, `FACT_EVIDENCE_HASH_INVALID`, `FACT_EVIDENCE_HASH_MISMATCH`, `FACT_PACK_FACT_ID_DUPLICATE`, `FACT_PACK_CLAIM_SOURCE_URL_MISMATCH`, `ARTICLE_FACT_PACK_CLAIMS_MISSING`, `ARTICLE_FACT_IDS_MISSING`, `ARTICLE_FACT_TRACE_MISSING`.

## C. Design Guard — 16 Regeln

Vorhandene konkrete Negativtests:
- `DESIGN_PPM_GENERATED_CLASS_MISSING`
- `DESIGN_TABLE_SYSTEM129_CLASS_MISSING`
- `DESIGN_BERATUNG_HEADING_LEVEL_FORBIDDEN`
- `DESIGN_INLINE_STYLE_FORBIDDEN`
- `DESIGN_ARTICLE_TYPE_CLASS_MISSING`

Damit: **5 exakt vorhanden / 11 Lücken**.

Lücken:
`DESIGN_ARTICLE_TYPE_TOKEN_INVALID`, `DESIGN_BODY_EMPTY`, `DESIGN_ARTICLE_TYPE_MISSING`, `DESIGN_ACTIVE_OR_GLOBAL_HTML_FORBIDDEN`, `DESIGN_EVENT_HANDLER_FORBIDDEN`, `DESIGN_JAVASCRIPT_URL_FORBIDDEN`, `DESIGN_CANONICAL_ARTICLE_ROOT_MISSING`, `DESIGN_ARTICLE_TYPE_ATTRIBUTE_MISMATCH`, `DESIGN_NESTED_ARTICLE_FORBIDDEN`, `DESIGN_TABLE_COMPARISON_CLASS_MISSING`, `DESIGN_TABLE_INLINE_STYLE_FORBIDDEN`.

## D. External-Link-Regeln — 2 Regeln

Kein vorhandener Einzeltest gefunden, der die beiden Fehlercodes explizit am echten `no_external_links()` erwartet:
- `EXTERNAL_LINK_FORBIDDEN`
- `EXTERNAL_URL_FORBIDDEN`

Damit: **0 exakt vorhanden / 2 Lücken**.

## Summen

- PPM: 55 vorhanden / 49 Lücken
- Content Guard: 5 vorhanden / 25 Lücken
- Design Guard: 5 vorhanden / 11 Lücken
- External Links: 0 vorhanden / 2 Lücken
- **GESAMT: 65 vorhanden / 87 Lücken = 152 geprüft**

LanguageTool 6.8 bleibt separater dynamischer Vendor-Prüfer: ein echtes Finding muss den Repair-Pfad auslösen; technische LT-Ausführungsfehler müssen HARD BLOCK bleiben. Dies wird in Punkt 4–6 separat klassifiziert/geprüft und nicht als zusätzliche Projektregel-ID gezählt.

## NEXT ACTION
Punkt 4: alle 152 Regeln semantisch exakt in `REPAIR_REQUIRED` oder terminal `HARD BLOCK` klassifizieren. Punkt 7 schließt anschließend ausschließlich die hier festgestellten 87 Negativbeweis-Lücken.
