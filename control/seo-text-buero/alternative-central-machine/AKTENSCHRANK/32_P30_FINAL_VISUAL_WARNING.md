# P30 – FINAL VISUAL ACCEPTANCE / FREIHEITSWARNUNG

Datum: 2026-09-08
Status: WARNUNG / P31 ZWINGEND

## Befund

P29 beweist maschinelle, deterministische DOM-/Style-Prüfung.

P30 zeigt zusätzlich im unveränderten PPM:

- `user_visual_inspection_status = REQUIRED_NOT_YET_COMPLETED`
- `user_visual_inspection_required_after_machine_dom = true`
- Capture-Aufträge für Desktop 1440x1200 und Mobile 390x844
- Capture-Quelle: `HTTP_RESPONSE_AFTER_WORDPRESS_RENDER`
- Capture muss an Post-ID + Readback-Hash gebunden sein
- lokaler Test darf Capture nicht fälschlich als ausgeführt behaupten
- zahlreiche historische Traceability-Einträge `USER_VISUAL_INSPECTION`

Gleichzeitig:
- Capture-Request selbst ist deterministisch gebunden
- kein AI-/LLM-Aufruf gefunden
- kein frei wählbarer Netzwerk-/Reviewerpfad im Rendered-DOM-Validator

## Kollision mit Zielanforderung

Falls `USER_VISUAL_INSPECTION` zwingende Voraussetzung für den automatischen Fachworkflow-/design_format-PASS ist:
Kollision mit
- 0,0 Entscheidungsfreiheit
- vollautomatischem Workflow
- Ergebnis unabhängig von Person/Ort/Chat

Ein freies menschliches „sieht gut aus“ darf kein Produktions-PASS bestimmen.

## Noch nicht bewiesen

P30 beweist NICHT, dass User Visual im aktuellen Normal-Draft-Produktions-PASS zwingend ist.

Der echte Normal-Draft-Test erreicht bereits:
`NORMAL_DRAFT_END_TO_END_READBACK_PASS_AWAITING_USER_CONTENT_REVIEW_NO_PUBLISH`
obwohl User Visual noch `REQUIRED_NOT_YET_COMPLETED` ist.

Daher P31:
exakt die Autoritätsgrenze prüfen.

## P31

Prüfen:
1. Blockiert fehlendes User Visual `CONTENT_QUALITY_CHECK_OK`?
2. Blockiert es `prepare()`?
3. Blockiert es `create_draft()`?
4. Blockiert es Normal-Draft-Endstatus?
5. Ist es Bestandteil des aktuellen 12-Gate-`design_format`-PASS oder separate User-Endabnahme?
6. Kann irgendein Human/User/Reviewer einen technischen FAIL zu PASS überstimmen?

Keine Regel ändern.
Keine User-Visual-Prüfung ersetzen.
