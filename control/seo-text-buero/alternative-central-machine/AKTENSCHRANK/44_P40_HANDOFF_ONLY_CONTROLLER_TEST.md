# P40 – HANDOFF-ONLY THIN CONTROLLER

Datum: 2026-09-09
Status: ABGESCHLOSSEN – PASS

## KISS-Ergebnis

Einzige Produktions-Eingangswahrheit:
`FACHWORKFLOW_HANDOFF_REQUEST.json`

Kein zusätzliches Jobmanifest.
Kein zweites Handoff-Format.
Kein frei wählbarer Controllerpfad.

Positiv/negativ tatsächlich geprüft:
- exakte 16-Feld-Datei -> PASS
- falsches/zusätzliches Feld -> BLOCKED
- Item-/Release-Identitätsdrift -> BLOCKED
- falsches PPM-Item -> BLOCKED nach no-write prepare und vor Signatur/Write
- positive Identität -> prepare -> externe Signatur -> Draft -> Readback
- publish_allowed=false

Dauerhafter GO-Beleg:
`45_P40_HANDOFF_ONLY_CONTROLLER_GO.md`

P36s signiertes Jobmanifest bleibt ausschließlich Laborbeweis und gehört nicht ins Zielsystem.
