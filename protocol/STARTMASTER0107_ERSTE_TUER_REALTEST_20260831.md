# STARTMASTER0107 – Erste-Tür-Realtest 2026-08-31

## Auftrag

Produktionslauf ausschließlich über den aktuell gebundenen Single-Door-Einstieg beginnen. Vor erfolgreichem PASS der ersten Tür keine Facharbeit, keine Recherche, keine Fact-Packs, keine Artikeltexte, keine Produktionspakete, keine WordPress-Aktion und keine Ersatzlösung.

Zusätzlich: potentielle Fehlerquellen und Optimierungspotential protokollieren, ohne die bestehende Wächter-/Facharchitektur eigenmächtig zu verändern.

## Tatsächlich gelesener Autoritätszustand

`control/CURRENT_STARTMASTER.json`

- startmaster: `STARTMASTER0107`
- gate_ref: `control/single-door-boundary/project_single_door_entry.py`
- free_chat_execution_authority: `false`
- hard_worker: `CODEX_CLOUD`

## Aktueller Runtime-State

`control/startmaster0107/runtime_inbox/RUNTIME_INBOX_STATE.json`

- status: `BATCH_READY_PACKAGE_PENDING`
- generation: `1`
- batch_sha256: `7f2e3290b6ac78ac7df1644395e57ac72f02dc1373e390eb2e532e57a8ce916a`
- production_package_ref: leer
- production_package_sha256: leer
- publish_allowed: `false`

Der gebundene Runtime-Guard bildet diesen Zustand deterministisch auf `READY_WAITING_PACKAGE` ab.

## Erste Tür

Der aktuell gebundene Project-Entry routet `READY_WAITING_PACKAGE` ausschließlich nach:

- room_token: `R_PRE_001`
- action_token: `A_PRE_001`
- capability: `execute_bound_action`
- input_handle: `I_PRE_PACKAGE_001`
- receipt_token: `P_PRE_001`
- next_room_token nach PASS: `R_001`

Der Projektvertrag legt fest:

- authoritative_execution_origin: `SINGLE_DOOR_EXECUTOR_ONLY`
- accepted_artifact_contract: `PSERC_APPROVED_PRODUCTION_PACKAGE_V1`
- required_release_contract: `WORKFLOW_SUPERVISOR_RELEASE_V2_SIGNED`
- required_signature_algorithm: `ED25519`
- `production_plan_without_signed_package`: DENY
- `unsigned_package`: DENY

## Ergebnis des Realtests

Die erste Tür ist korrekt gefunden und eindeutig gebunden.

Der aktuelle Lauf kann sie jedoch noch nicht mit PASS verlassen, weil für `I_PRE_PACKAGE_001` aktuell kein gebundenes signiertes Produktionspaket existiert. Der Runtime-State bestätigt dies durch leere Felder `production_package_ref` und `production_package_sha256`.

Gemäß dem verbindlichen Erste-Tür-Einlass wurde deshalb KEINE Facharbeit gestartet und insbesondere NICHT erzeugt:

- keine Recherche
- keine Fact-Packs
- keine Artikeltexte
- kein Produktionsplan
- kein Produktionspaket
- keine WordPress-Aktion

Der Lauf bleibt fail-closed in `R_PRE_001`.

## Potentielle Fehlerquelle

Zwischen dem gewünschten Bedienprinzip „zuerst durch die erste Tür, erst danach Fachproduktion“ und dem aktuellen H7-Handoff besteht ein klarer Lebenszyklus-Konflikt:

`R_PRE_001` akzeptiert nur ein bereits vollständig signiertes `PSERC_APPROVED_PRODUCTION_PACKAGE_V1`.

Wenn dieses Paket erst durch Recherche/Text/Fachproduktion entstehen soll, kann es nicht gleichzeitig Voraussetzung sein, die erste Tür überhaupt zu passieren.

Dieser Konflikt ist genau die Stelle, an der ein freier Chat früher verleitet werden konnte, außerhalb des Wächterpfads vorzuarbeiten. Der neue harte Einlass verhindert dieses Verhalten jetzt zuverlässig, macht den bestehenden Lebenszyklus-Konflikt aber sichtbar statt ihn zu überbrücken.

## Optimierungspotential – NICHT IMPLEMENTIERT

Eine zukünftige technische Klärung muss genau eine eindeutige Autoritätsantwort liefern:

1. Entweder eine serverseitig gebundene Preproduction-Aktion erzeugt/autorisiert das notwendige Paket innerhalb der ersten Tür,
2. oder die fachliche Preproduction wird als ausdrücklich gebundene Vorstufe vor `R_PRE_001` definiert,
3. oder die Definition der „ersten Tür“ wird auf einen tatsächlich vor der Paketerzeugung liegenden Wächterraum verschoben.

Keine dieser Varianten wurde in diesem Realtest ausgewählt oder implementiert. Der Chat trifft keine Architekturentscheidung.

## Schutzwirkung des aktuellen Tests

PASS:

- kein Vorbeilaufen am Gate
- kein freies Schreiben von Artikeln
- kein Ersatzpaket
- keine Rekonstruktion alter Artefakte
- kein Rücksprung auf 107001–107006
- kein Auto-Publish

## Aktuell zulässiger Zustand

`R_PRE_001` / `READY_WAITING_PACKAGE`

Weiterarbeit erst mit dem vom bestehenden System autorisiert bereitgestellten, signierten Input für `I_PRE_PACKAGE_001` oder nach einer ausdrücklich autorisierten Änderung des gebundenen Lebenszyklus.
