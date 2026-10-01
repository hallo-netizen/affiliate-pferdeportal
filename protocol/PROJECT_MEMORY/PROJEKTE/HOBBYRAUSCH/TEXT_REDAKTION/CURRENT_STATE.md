# HOBBYRAUSCH – TEXT_REDAKTION – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-01
STATUS: HD-001 PRODUKTIV LIVE PASS / HDTE 0.1.2 LIVE PORTALABGLEICH BLOCKED / HDTE 0.1.3 COMPLETE-WORKFLOW POS+NEG HARD PASS / LIVE-UPGRADE NÄCHSTES

## HD-001

Produktiver Buchbinden-Pilot:
- live deployed;
- Schreiben und Readback erfolgreich;
- nicht zurückrollen;
- 7 Owner;
- 11 ARTICLE_ONLY;
- 11/11 gebunden.

## HDTE Live

Installiert:
`Hobby Depot SEO Themenengine 0.1.2`

Auto-Owner-Handoff:
PASS.

Gesamtbestand:
erfasst.

Portalabgleich:
`BLOCKED · HDTE_CONTEXT_STAGE_PLAN_HASH_MISSING`

## Ursache

Ein bewusst nicht vorhandener Redaktionsplan wird im bestehenden Snapshot-Vertrag mit
`status=NOT_AVAILABLE`, `sha256=NOT_AVAILABLE`, `items=[]`
repräsentiert.

0.1.2 verwarf diesen gültigen Zustand fälschlich als fehlenden Hash.

## HDTE 0.1.3

Installer:
`HOBBY_DEPOT_SEO_THEMENENGINE_V0.1.3_PORTALABGLEICH_FULL_WORKFLOW_HARD_PASS.zip`

SHA:
`5b3063577beb3e5dfb03799b6245f2b9aaf90f338c70e86708674e5999762b2a`

Kompletter lokaler Workflow – nicht nur Teiltest:
- deployed HD-001 Handoff;
- Auto-Sync 7 Owner / 11 Assignments;
- Baseline;
- request-getrennter Portalabgleich;
- Context Index;
- finale Structure/Inventory/Plan-Gates;
- COMPLETE.

Exakter alte 0.1.2 BLOCKED-Zustand wurde persistiert und danach unter 0.1.3 ohne neue Baseline bis COMPLETE fortgeführt.

Zusätzlich 4-Themen-Stresslauf bis COMPLETE.

Negative Fälle:
not deployed / malformed NOT_AVAILABLE / Hash fehlt / Stage manipuliert / Live-Struktur driftet → jeweils BLOCKED.

Fresh Installer:
80/80 PHP PASS.
135/135 Dateiparität.

## NEXT ACTION

0.1.3 installieren und nur die Themenengine-Übersicht öffnen.

Der vorhandene BLOCKED-Job wird automatisch fortgesetzt.

Keine neue Bestandserfassung.
Kein neuer Handoff.
Keine DataForSEO-Recherche vor Portalabgleich COMPLETE.
