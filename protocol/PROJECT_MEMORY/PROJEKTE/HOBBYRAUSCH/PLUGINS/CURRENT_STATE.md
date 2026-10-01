# HOBBYRAUSCH – PLUGINS – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-01
STATUS: HD-001 V1.9.4 LIVE PASS · HD-002 V0.1.2 LIVE BLOCKED PLAN_HASH_MISSING · HD-002 V0.1.3 COMPLETE-WORKFLOW POS+NEG HARD PASS / LIVE-UPGRADE NÄCHSTES

## HD-001 – Kategorie-Workflow

`Affiliate-Portal Kategorie-Workflow V1.9.4`

Live:
- produktiver Buchbinden-Pilot deployed;
- Schreiben und Readback erfolgreich;
- Bestand bleibt stehen;
- Owner-Handoff 7 Owner / 11 ARTICLE_ONLY / 11 gebunden.

## HD-002 – Themenengine

Live:
`0.1.2`

Auto-Owner-Handoff und Baseline:
PASS.

Portalabgleich live:
`BLOCKED · HDTE_CONTEXT_STAGE_PLAN_HASH_MISSING`

Root Cause:
gültiger `NOT_AVAILABLE`-Redaktionsplan-Sentinel wurde als fehlender SHA behandelt.

## V0.1.3

Installer SHA:
`5b3063577beb3e5dfb03799b6245f2b9aaf90f338c70e86708674e5999762b2a`

Kompletter Workflow lokal simuliert:
- exakt liveähnlicher Zustand mit 0 Themen / 4 Kategorien / 1 Familie / kein Redaktionsplan → COMPLETE;
- alter 0.1.2-BLOCKED-Job → gleiche persistierte Daten unter 0.1.3 requestweise bis COMPLETE;
- Stresslauf 4 Themen → COMPLETE;
- vorhandener Redaktionsplan → COMPLETE.

Negativ:
- upstream not deployed;
- malformed NOT_AVAILABLE;
- fehlender echter Hash;
- staged artifact manipuliert;
- finale Struktur driftet;
→ jeweils fail-closed BLOCKED.

Paket:
- Source PHP 80/80;
- Fresh Installer PHP 80/80;
- Source↔Installer 135/135;
- 4 Dateien gegenüber 0.1.2 geändert;
- Storage/Safe-Migration/Owner-Handoff sonst unverändert.

## NEXT ACTION

HDTE 0.1.3 über 0.1.2 installieren → Themenengine-Übersicht öffnen → vorhandenen Job automatisch bis `Portalabgleich COMPLETE` laufen lassen.

Keine neue Bestandserfassung.
