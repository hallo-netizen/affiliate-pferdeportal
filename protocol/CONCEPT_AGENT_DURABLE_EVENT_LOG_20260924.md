# Concept Agent — append-only Unterbrechungszustand — 2026-09-24

Zweck: KISS-Fix ausschließlich für sicheren Wiedereinstieg nach Unterbrechung eines bereits MACHINE_READY befindlichen Concept-Agent-Batches.

## Problem

Der bisherige Fortschritts-Checkpoint konnte vollständige Draft-Bytes, Hash, Revision und erlaubte Folgeaktion enthalten, war aber nicht zuverlässig außerhalb des jeweiligen Workers dauerhaft vorhanden. Nach Worker-/Chat-Abbruch konnte deshalb der exakte Zustand fehlen.

## Lösung

Kein neuer Produktionsrunner und kein schreibender GitHub-State des Workers.

Nach MACHINE_READY:
1. aktueller Batch ausschließlich aus `concept_agent/current/PSERC_METADATA_SNAPSHOT.json`;
2. exakt zugehöriger `TEXT_START_BATCH_CLAIM:<batch_sha256>`;
3. exakt passender `TEXT_START_MACHINE_READY`-Beleg von `github-actions[bot]`;
4. danach append-only `CONCEPT_AGENT_DURABLE_EVENT_V1` ausschließlich von `chatgpt-codex-connector[bot]`;
5. jedes Event bindet Sequenz, Vorgängerhash, exakt erlaubte Aktion, Payload-Hash und Bytegröße;
6. `concept_agent/durable_event_log.py` rekonstruiert bei jedem Einstieg die komplette Kette und daraus Research-Bindung, Produktions-Binding und Fortschritts-Checkpoint;
7. nur die daraus abgeleitete eine `allowed_action` darf ausgeführt werden.

Nicht-Bot-Kommentare sind niemals Autorität.

## Unterbrechung

- Abbruch vor neuem Bot-Event: letzter sicherer Zustand bleibt gültig.
- Abbruch nach neuem Bot-Event: neuer Worker rekonstruiert exakt daraus.
- Lücke, Manipulation oder Mehrdeutigkeit in der Bot-Kette: STOP.
- Draft-/Repair-Bytes liegen im jeweiligen Event gzip+base64 vor und sind zusätzlich an SHA-256 und Bytegröße gebunden.

## Bewusst nicht verwendet

- kein `GH_TOKEN` als Produktionsfortschritts-Voraussetzung;
- kein `GITHUB_TOKEN`;
- kein `git push`;
- kein `git remote`;
- keine Runtime-State-Branch als Produktionsautorität;
- kein zweites `text-start`;
- keine Rekonstruktion aus Chat-Erinnerung;
- keine historischen/Recovery-Drafts als NEW-Quelle.

## Unverändert

- globales `control/startmaster0107/CURRENT_STATE.json` byte-identisch;
- `concept_agent/full_workflow_gate.py` byte-identisch;
- text-start;
- LanguageTool 6.8;
- PPM 6.7.9;
- PSERC;
- ENDSTEMPEL;
- Artikel-/Qualitätsregeln;
- Publish bleibt false.

## Tests

Ergänzte Regressionen:
- Unterbrechung unmittelbar nach Draft: frischer Replay rekonstruiert exakt dieselben Bytes und verlangt LT68;
- Unterbrechung bei `REPAIR_REQUIRED`: frischer Replay bleibt auf demselben Artikel; reparierter Draft führt zurück zu LT68;
- manipulierte Payload-Integrität blockiert.

Dieses Dokument ist nur Protokoll/CI-Trigger und keine zweite Current-/Next-Action-Autorität.
