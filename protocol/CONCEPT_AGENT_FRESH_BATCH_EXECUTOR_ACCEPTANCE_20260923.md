# Concept Agent Fresh-Batch Executor – Acceptance-Stand 2026-09-23

## Zielvertrag
Unverändert: `MAXIMIZE_MEDIUM_WITHOUT_ANY_GATE_OR_QUALITY_CHANGE`.

Nicht geändert:
- Artikelworkflow / Textmaschine
- LanguageTool 6.8
- PPM 6.7.9
- PSERC
- ENDSTEMPEL
- Plugins
- Qualitätsgrenzen
- Publish-Sicherheit (`publish_allowed=false`)

## Autoritativer Einstieg / Frischecheck
- Einstieg über `main:concept_agent/CONTROL_ENTRY_POINTER.json`.
- Current-Autorität: `concept-agent/production-control:concept_agent/CONTROL_STATE.json`.
- Frischecheck: Branch `concept-agent/production-control` stand unverändert exakt auf `bf528a17a1227e8c04ade631f85cdc39fe58c363`.
- Keine Vollrekonstruktion.
- Historischer fehlender Transport wurde nicht rekonstruiert.

## Bestätigte Root Cause
Der produktive Restart endete bisher bei:
`RESTART_BATCH_FROM_INTAKE -> CONCEPT_AGENT_INTAKE_READY -> PREPARE_INTAKE_ONLY -> STOP`.

Nur den STOP zu entfernen wäre unzureichend. Es fehlte produktiv:
`fresh intake -> real research binding -> real machine prewrite/link binding -> durable work binding -> resumable runner -> real System-4 fullcheck`.

## Fix-Branch
`concept-agent/fresh-batch-executor-fix-20260923`

Wesentliche Fixes:
- `concept_agent/fresh_batch_executor.py`: produktiver Fresh-Batch-Binder.
- `concept_agent/system4_checker.py`: Adapter auf den unveränderten System-4-`controller.py fullcheck`.
- `concept_agent/runner.py`: Reasoning `medium`; realer Checker erhält Batch- und Repair-Kontext.
- `concept_agent/resumable_runner.py`: persistiert Same-Article-Repair-Kontext für Re-Entry.
- Workflow-Fix: Restart läuft nach Intake in Binder -> dauerhafte Work-Binding -> resumable runner.

System-4-Produktionsdateien wurden zwischen `main` und Fix-Branch byte-/blobidentisch gegengeprüft:
`machine_point0.py`, `source_acquisition.py`, `content_guard.py`, `authoring_contract.py`,
`controller.py`, `controller_engine.py`, `production_checks.py`,
`production_checks_engine.py`, `LT68Worker.java` und das gebundene PPM-6.7.9-Paket.

## Reale Acceptance
Run: `35832352935`

Echter Request:
byteidentischer bereits gebundener 16er-Request-Blob; nur unter neuem Pfad zum Auslösen des Fix-Branch-Workflows referenziert.

PASS vor produktiver Modellarbeit:
- Request-Auflösung: PASS
- Request-Validierung: PASS
- exaktes LanguageTool 6.8 geladen und SHA geprüft: PASS
- bestehende Runner-Tests: PASS
- aktueller 16er Fresh-Binding-Regressionscheck: PASS
- exakt drei interne Links pro aktuellem 16er-Item gebunden: PASS
- Intake-Tamper negativ: BLOCKED wie erwartet
- Mid-Workflow Re-Entry positiv: PASS
- Mid-Workflow Re-Entry negativ / Manipulation: BLOCKED wie erwartet
- insgesamt 9 Unit-/Binding-Tests: PASS
- Stage 0: PASS bis `ARTICLE_PRODUCTION`
- Hardlock erkennt historischen Transport weiterhin als fehlend: PASS
- feste Aktion `RESTART_BATCH_FROM_INTAKE`: PASS
- echter Restart-Intake: `CONCEPT_AGENT_INTAKE_READY`, 16/16 PASS

## Erster aktueller Real-Blocker
`OPENAI_API_KEY_MISSING`

Beweis aus Run `35832352935`:
Der vorhandene Workflow-Eintrag `OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}` wurde leer aufgelöst.
`fresh_batch_executor.py` blockierte deshalb vor der ersten Web-Recherche / Modellarbeit fail-closed.

Wichtig:
Diese Abhängigkeit wurde durch den Fix nicht neu eingeführt. Der bestehende Concept-Agent-Production-Workflow und der bestehende produktive Runner erwarteten `OPENAI_API_KEY` bereits vorher. Der frühere `PREPARE_INTAKE_ONLY`-Stop verhinderte lediglich, dass dieser nächste Blocker sichtbar wurde.

## Status
- Fresh-Batch-Executor-Code: vorhanden auf Fix-Branch
- aktueller 16er statisch / negativ / Re-Entry: PASS
- echter Restart-Intake: PASS
- echte Modell-Recherche: 0/16, blockiert vor Start
- fertige Artikel: 0/16
- realer LT/PPM-Artikelcheck: 0/16
- PSERC: nicht erreicht
- ENDSTEMPEL: nicht erreicht
- finale Chat-Datei: nicht vorhanden
- Publish: false
- Gesamt-PASS: NICHT behauptet
- Merge in `concept-agent/production-control`: NICHT durchgeführt

## Nächste zulässige Aktion
Das bereits im Production-Workflow erwartete GitHub-Actions-Secret `OPENAI_API_KEY` muss vorhanden sein.
Danach exakt denselben autoritativen Request erneut ausführen. Keine Regel-, Workflow-, Qualitäts- oder Prüfänderung als Ersatz für das fehlende Secret.
