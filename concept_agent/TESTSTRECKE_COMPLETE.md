# CONCEPT AGENT — KOMPLETTE TESTSTRECKE

## Produktionskette
Isolation → gebundener Eingang → Research → Facts → Writer → Handoffprüfung → redaktionelle Guards → Repair → kompletter Recheck → 1..N-Batchprüfung → WordPress-Direktimportdatei.

Verbindlich:
- LanguageTool 6.8 PASS / 0 Findings;
- PPM 6.7.9 TECHNICAL_CHECK_OK;
- PPM 6.7.9 CONTENT_QUALITY_CHECK_OK;
- Fail-Closed-Aggregat PASS;
- nach jeder Reparatur kompletter Recheck;
- kein Publish;
- kein WordPress-Write durch Concept Agent.

## Beitragsarten
Der gebundene `article_type` wird unverändert übernommen.
Gemischte 1..N-Batches sind zulässig.
Kein automatischer Fallback auf `Beratung`.
Typspezifische Regeln werden nur für den jeweiligen Typ angewendet.

## Redaktionelle Natürlichkeit / HTML-Textfluss
Pflicht vor FINAL:
- `<Keyword> wählen/auswählen/finden` als nackter Beratungstitel: BLOCK;
- `So findest du <Keyword>` ohne sinnvolle Ergänzung: BLOCK;
- bereits natürlicher Titel wie `So wählst du geeignete Fliegenmasken für Pferde`: PASS;
- mechanische Beratung-H2 wie `Fliegenmasken am Pferd sicher beurteilen`: BLOCK;
- natürliche konkrete H2: PASS;
- `</a>Wort`: BLOCK;
- `</a>,` / `</a>.`: PASS.

Implementierung:
- `concept_agent/textmachine_guard.py`
- `concept_agent/tests/test_textmachine_snapshot.py`

## WordPress-Grenze
Aktuell belegter Live-Vertrag:
`SYSTEM4_WORDPRESS_HANDOFF_V1`

Verifiziert gegen:
- Portal SEO Redaktionsplan Compiler 0.28.23
- Portal Production Machine 6.7.9

Top-Level-Pflicht:
- `contract`
- `batch_sha256`
- `publish_allowed=false`
- `signing_deferred=true`
- `batch_gate_status=SYSTEM4_BATCH_FULL_PASS_COLLECTED`
- `no_legacy_status=PASS`
- `test_suite_status=PASS`
- `wordpress_review`
- `articles`

Je Artikel müssen die Importer-Bindungen für Index, Titel, Keyword, Kategorie, Beitragsart, Plan-Slot, Body-Hash, Revision, Production Context, LanguageTool und PPM stimmen.

## Harte Positiv-/Negativprüfung vor Chat-Ausgabe
POSITIV:
- 1 Artikel;
- gemischter 1..N-Batch einschließlich mindestens eines Nicht-Beratung-Typs;
- aktueller Direktimportvertrag.

NEGATIV:
- alter `PSERC_APPROVED_PRODUCTION_PACKAGE_V1`-Pseudo-Direktvertrag: BLOCK;
- interner Handoff als WordPress-Datei: BLOCK;
- `publish_allowed=true`: BLOCK;
- Body-Tamper/Hash-Mismatch: BLOCK;
- LT Finding > 0: BLOCK;
- PPM nicht PASS: BLOCK;
- Produktionsbindung/Slug/Kategorie fehlerhaft: BLOCK.

## Chat-Ausgabe
Erst nach PASS genau eine Datei:
`SYSTEM4_WORDPRESS_HANDOFF_V1.json`

Kein fixer 7er-Dateiname. Derselbe Weg gilt für 1..N.
