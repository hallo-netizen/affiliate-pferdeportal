# P40 – HANDOFF-ONLY THIN CONTROLLER

Datum: 2026-09-09
Status: TEST AKTIV

## KISS-Ziel

Einzige Produktions-Eingangswahrheit:
`FACHWORKFLOW_HANDOFF_REQUEST.json`

Kein zusätzliches Jobmanifest.
Kein zweites Handoff-Format.
Kein frei wählbarer Controllerpfad.

## Zu beweisen

- exakte 16-Feld-Datei -> fester Ein-Item-Weg
- falsches/zusätzliches Feld -> BLOCKED
- Item-/Release-Identitätsdrift -> BLOCKED
- falsches PPM-Item -> BLOCKED nach no-write prepare und vor Signatur/Write
- positive Identität -> prepare -> externe Signatur -> Draft -> Readback
- publish_allowed=false

P36s signiertes Jobmanifest bleibt ausschließlich Laborbeweis und gehört nicht ins Zielsystem.
