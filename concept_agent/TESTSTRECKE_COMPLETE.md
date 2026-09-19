# CONCEPT AGENT — KOMPLETTE TESTSTRECKE

## Phasen 1–10
Isolation → Eingang → Research → Facts → Writer → Artikelprüfung → Repair → Artikel-Preimport → 1..N → echte Qualitätsprüfer.

Verbindlich:
- LanguageTool 6.8 PASS
- PPM 6.7.9 PASS
- nach jeder Reparatur kompletter Recheck
- kein Publish
- kein WordPress-Write

## Phase 11 — WordPress Redaktionsplan Upload
Die WordPress-Uploaddatei ist NICHT der interne Concept-Agent-Handoff und NICHT der ENDSTEMPEL-Wrapper.

Harte positive Referenz:
`GEN1_7_ARTIKEL_WORDPRESS_REDAKTIONSPLAN_UPLOAD_107008_PASS.json`

Exakter Top-Level-Vertrag:
- `contract = PSERC_APPROVED_PRODUCTION_PACKAGE_V1`
- `source`
- `batch_sha256`
- `publish_allowed = false`
- `article_count`
- `production_plan_sha256`
- `production_plan`
- `redaktionsplan_binding`
- `output_release`
- `package_payload_sha256`

`redaktionsplan_binding`:
- `contract = PSERC_TEXTMACHINE_METADATA_BATCH_V2`
- `status = READY_FOR_WORDPRESS_DRAFT_IMPORT`
- `item_count = article_count`
- `publish_allowed = false`
- pro Artikel: article_type, category, plan_slot, canonical_article_id, target_keyword, title

`output_release`:
- `contract = PFERDE_ATELIER_OUTPUT_RELEASE_RECEIPT_V2`
- `status = OUTPUT_RELEASE_PASS_FINAL_REVIEW_AND_REARM_CONFIRMED`
- `final_review_sequence = 107008`
- `publish_allowed = false`

Alle Artikelbytes, Artikelhashes, Planhash und package_payload_sha256 müssen stimmen.

## Phase 12 — harte lokale Positiv-/Negativprüfung
Pflicht vor Chat-Ausgabe:
- bekannte 107008-PASS-Struktur: POSITIV PASS
- aktuelle Datei: POSITIV PASS
- falscher Contract: BLOCK
- falsche Artikelzahl: BLOCK
- falscher production_plan_sha256: BLOCK
- falscher Binding-Status: BLOCK
- veränderte Artikelbytes: BLOCK
- falscher package_payload_sha256: BLOCK

Implementierung:
- `concept_agent/wordpress_redaktionsplan_upload.py`
- `concept_agent/wordpress_output_contract.py`
- `concept_agent/wordpress_delivery.py`
- `concept_agent/tests/test_wordpress_redaktionsplan_upload.py`
- `concept_agent/tests/test_wordpress_output_contract.py`
- `concept_agent/tests/test_wordpress_delivery.py`

## Phase 13 — Chat-Ausgabe
Erst nach Positiv-/Negativ-PASS genau eine WordPress-Uploaddatei ausgeben:
`GEN1_7_ARTIKEL_WORDPRESS_REDAKTIONSPLAN_UPLOAD_107008_PASS.json`

Verboten als WordPress-Datei:
- `CONCEPT_AGENT_FINAL_ARTICLE_V1`
- `CONCEPT_AGENT_7_ARTICLE_CHAT_HANDOFF_V1`
- `SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2`
- ENDSTEMPEL-Signierauftrag
- ENDSTEMPEL-Wrapper

## Produktionsgrenze
Kein Publish.
Kein WordPress-Write.


## Phase 14 — Redaktionelle Natürlichkeit / HTML-Textfluss
Pflicht vor FINAL:
- Beratungstitel mit alter nackter Generatoroberfläche: BLOCK
- natürlich attributierter Beratungstitel: PASS
- mechanisch/bürokratisch klingende Beratung-H2: BLOCK
- natürliche, konkrete Beratung-H2: PASS
- `</a>Wort` ohne Leerzeichen: BLOCK
- `</a>,` bzw. `</a>.` mit Satzzeichen: PASS

Implementierung:
- `concept_agent/textmachine_guard.py`
- `concept_agent/tests/test_textmachine_snapshot.py`

Diese Stufe läuft vor jeder finalen Dateiausgabe und nach jeder Reparatur erneut.
