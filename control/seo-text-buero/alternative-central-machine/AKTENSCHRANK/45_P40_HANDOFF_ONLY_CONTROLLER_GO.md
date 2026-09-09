# P40 – HANDOFF-ONLY CONTROLLER GO

Datum: 2026-09-09
Status: GO

## Ergebnis

Der dünne Controller akzeptiert als einzige Eingangswahrheit:
`FACHWORKFLOW_HANDOFF_REQUEST.json`

Kein zusätzliches Jobmanifest.
Kein zweites Handoff-Format.
Keine frei wählbare Route.

## Tests

7/7 PASS.

Positiv:
- exakte bestehende 16-Feld-Handoff-Datei -> PASS
- Inputtruth bleibt `FACHWORKFLOW_HANDOFF_REQUEST.json`
- prepare -> externe Signatur -> exakt ein Draft -> Readback
- publish_allowed=false

Negativ:
- Zusatzfeld -> BLOCKED
- fehlendes Feld -> BLOCKED
- production_plan_item-Identitätsdrift -> BLOCKED vor Adapter
- workflow_release_item-Identitätsdrift -> BLOCKED vor Adapter
- falsche PPM-Item-ID -> BLOCKED nach schreibfreiem prepare und vor Signatur/Write
- keine Jobmanifest-/Route-/Validator-/Engine-Auswahl-API vorhanden

## KISS-Folge

P36s signiertes Jobmanifest ist endgültig nur Laborwerkzeug.

Zielbetrieb:
`bestehende FACHWORKFLOW_HANDOFF_REQUEST.json -> dünner Controller`

## Noch offene Identitätsprüfung

canonical_article_id ist bis PPM prepare() gebunden.

Jetzt noch separat beweisen:
`plan_slot` muss ebenfalls exakt zum tatsächlich vorbereiteten PPM-Item gehören.

Keine neue Binding-Schicht.
Nur vorhandene Prepared-/Plan-Identität vollständig prüfen.
