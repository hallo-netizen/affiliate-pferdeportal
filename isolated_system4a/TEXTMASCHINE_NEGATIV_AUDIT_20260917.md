# SYSTEM 4A — NEGATIVBEWEIS-AUDIT TEXTMASCHINE

Stand: 17.09.2026
Branch: `hobbyroom/system4a-textmachine-final-pass-20260916`
Zweck: Punkt 3/7 des eingeschlossenen Hobbyraum-Arbeitsauftrags.

## Aktueller harter Stand

Erreichbare Projektregeln: **151**.

Nach dem initialen Audit und dem real ausgeführten Guard-/Design-/External-Gap-Test:
- **102/151** besitzen jetzt einen exakten Negativbeweis am echten Prüfer/Fehlercode.
- **49/151** sind noch offen.
- Alle **49 offenen Regeln liegen ausschließlich im PPM-6.7.9-Anteil**.

Remote-Beleg für die 37 neu geschlossenen Nicht-PPM-Lücken und die korrigierte Erreichbarkeit:
- Workflow `System 4A Repair Owner Contract`
- Run `35195339914`
- Head `50b4502159b08196494e7da9f69ece26e81e8d6b`
- Ergebnis `SUCCESS`

Der vorherige rote Run `35195117339` bewies zusätzlich, dass `DESIGN_TABLE_INLINE_STYLE_FORBIDDEN` nicht als eigene Regel erreichbar ist; vorher greift `DESIGN_INLINE_STYLE_FORBIDDEN`. Daher lautet die echte Gesamtmenge 151 statt 152.

## A. PPM 6.7.9 — 104 Regeln

### Exakter Negativbeweis vorhanden: 55/104
### Noch offen: 49/104

45 aktive Blocking-Regeln:
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

4 WAVE4-Anforderungen:
- `W4::R8-0786`
- `W4::R8-0787`
- `W4::R8-0788`
- `W4::R8-0790`

## B. Content Guard — 30/30 exakt negativ bewiesen
- 5 waren bereits vorhanden.
- 25 fehlende Fälle wurden in `test_textmachine_negative_gap_guards.py` ergänzt und remote grün ausgeführt.

## C. Design Guard — 15/15 erreichbare Regeln exakt negativ bewiesen
- 5 waren bereits vorhanden.
- 10 fehlende erreichbare Fälle wurden ergänzt und remote grün ausgeführt.
- `DESIGN_TABLE_INLINE_STYLE_FORBIDDEN` ist keine eigene erreichbare Regel und wurde korrekt aus dem Scope entfernt.

## D. External Links — 2/2 exakt negativ bewiesen
`EXTERNAL_LINK_FORBIDDEN` und `EXTERNAL_URL_FORBIDDEN` werden im echten `no_external_links()` gezielt ausgelöst und geprüft.

## Summen
- PPM: 55 bewiesen / 49 offen
- Content Guard: 30 bewiesen / 0 offen
- Design Guard: 15 bewiesen / 0 offen
- External Links: 2 bewiesen / 0 offen
- **GESAMT: 102 bewiesen / 49 offen = 151**

## NEXT ACTION
Punkt 7: ausschließlich die hier gelisteten **49 PPM-Lücken** mit echten PPM-6.7.9-Prüfern/exakten Fehlercodes schließen.
