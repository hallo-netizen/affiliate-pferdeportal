# CONCEPT AGENT — CURRENT STATUS

Status: SEVEN_ARTICLE_REAL_CHECKER_RUN_PASS / WORDPRESS_REDAKTIONSPLAN_UPLOAD_LOCAL_HARD_PASS

## 7-Artikel-Lauf
Writer: ChatGPT / GPT-5.6 Sol

- 7/7 LanguageTool 6.8 PASS
- 7/7 PPM 6.7.9 TECHNICAL_CHECK_OK
- 7/7 PPM 6.7.9 CONTENT_QUALITY_CHECK_OK
- 7/7 Fail-Closed-Aggregat PASS
- 0 exakte artikelübergreifende Satzdubletten, KI-Offenlegung ausgenommen

## WordPress-Grenze
Harte positive Referenz:
`GEN1_7_ARTIKEL_WORDPRESS_REDAKTIONSPLAN_UPLOAD_107008_PASS.json`

Direkter WordPress-Vertrag:
`PSERC_APPROVED_PRODUCTION_PACKAGE_V1` in der 107008-Redaktionsplan-Struktur, NICHT als ENDSTEMPEL-Wrapper.

Pflicht:
- `redaktionsplan_binding.contract = PSERC_TEXTMACHINE_METADATA_BATCH_V2`
- `redaktionsplan_binding.status = READY_FOR_WORDPRESS_DRAFT_IMPORT`
- `output_release.contract = PFERDE_ATELIER_OUTPUT_RELEASE_RECEIPT_V2`
- `output_release.status = OUTPUT_RELEASE_PASS_FINAL_REVIEW_AND_REARM_CONFIRMED`
- `final_review_sequence = 107008`
- `publish_allowed = false`
- korrekte Artikel-/Plan-/Paket-Hashes

## Lokaler Hardtest
POSITIV:
- historisch bekannte PASS-Struktur: PASS
- aktuelle 7er-Datei: PASS

NEGATIV:
- falscher Contract: BLOCK
- Count-Mismatch: BLOCK
- Planhash falsch: BLOCK
- Binding-Status falsch: BLOCK
- Artikelbyte manipuliert: BLOCK
- Pakethash falsch: BLOCK

## Harte Grenzen
- kein Codex
- kein Claude
- kein Publish
- kein WordPress-Write


## Redaktionelle Nachschärfung 2026-09-19
Dauerhaft fail-closed ergänzt:
- schwache/nackte Beratungstitel werden vor FINAL blockiert;
- natürliche Titelattribute (passend/geeignet/richtig/optimal/ideal) werden als zulässige Präsentationssprache behandelt;
- mechanische Beratung-H2 wie `Fliegenmasken am Pferd sicher beurteilen` werden blockiert;
- fehlendes Leerzeichen nach Inline-Link (`</a>Wort`) wird blockiert;
- positive/negative Regressionstests sind Bestandteil der Teststrecke.

Die zuerst erzeugten 7 Artikel sind durch Run 002 ersetzt. Run 002 ist nach Titel-, H2- und Inline-Link-Nachschärfung 7/7 LanguageTool 6.8 PASS, 7/7 PPM 6.7.9 PASS und gegen den echten PSERC-0.28.23-Importer positiv/negativ geprüft. Aktuelle WordPress-Datei: `SYSTEM4_WORDPRESS_HANDOFF_V1_CURRENT7_CORRECTED.json`, SHA-256 `28d26eeca17731e79764dc6886b5f7ded1c234d1c095559f1e7800fc575a20d1`. Beleg: `concept_agent/production_ready/REAL7_CHATGPT_RUN_002_CORRECTED_PROOF.json`.


### Präzisierung Titelregel
Nach Sichtprüfung des aktuellen 7er-Batches gilt: die vorhandenen natürlichen Titel bleiben erhalten. Insbesondere `So wählst du geeignete Fliegenmasken für Pferde` ist ausdrücklich zulässig. Im aktuellen Batch werden nur die nackten Aktions-Titel `Mistcontainer mit Deckel wählen` und `Pferdehaftpflicht mit Fremdreiter auswählen` als Titeloberflächen-Fehler behandelt. Die Guard-Regel wurde entsprechend eingeengt, damit gute Titel nicht unnötig umgeschrieben werden.
