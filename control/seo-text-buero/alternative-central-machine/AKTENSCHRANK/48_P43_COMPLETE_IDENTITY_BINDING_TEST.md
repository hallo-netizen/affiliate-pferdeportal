# P43 – VOLLSTÄNDIGE ITEMIDENTITÄT OHNE NEUE SCHICHT

Datum: 2026-09-09
Status: TEST AKTIV

## KISS-Korrektur

P42 hat gezeigt:
- extern/Handoff: plan_slot
- PPM: canonical_article_id + plan_item_key
- diese Identitäten sind NICHT dasselbe

P43 baut kein neues Gate.

Der bestehende P40-Controller prüft jetzt:
1. plan_slot bleibt in der vorhandenen Handoff-/PSERC-Grenze
2. canonical_article_id muss exakt zum Prepared-Payload passen
3. production_plan_item.plan_item_key muss exakt zum PPM-prepared plan_item_key passen
4. beide Mismatches blockieren nach no-write prepare und VOR Signatur/Write

Kein neues Feld.
Kein neues Format.
Kein neuer Controller.
Kein Jobmanifest.

## Negativfälle

- falscher plan_item_key -> BLOCKED vor Signatur/Write
- falsche canonical_article_id -> BLOCKED vor Signatur/Write
- fehlender plan_item_key -> BLOCKED vor Adapter
- bestehende Handoff-/Release-Identitätsdrifts bleiben BLOCKED

## Ziel

Nur wenn der komplette P0–P43-Lauf grün ist:
GO.
