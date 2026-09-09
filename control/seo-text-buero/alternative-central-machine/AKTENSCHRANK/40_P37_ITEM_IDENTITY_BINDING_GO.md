# P37 – EXAKTE ITEM-ID-zu-PPM-BINDUNG

Datum: 2026-09-08
Status: GO

## Ergebnis

Der dünne Controller reicht die signierte Job-Identität jetzt bis zum bestehenden PPM-Adapter durch.

Harter Realtest:

- actual_ppm_plan_item_key = `canonical-faq-001`
- positive_signed_job_bound_to_exact_ppm_item = true
- controller_receipt_item_id_matches = true
- wrong_item_blocked_before_signing = true
- wrong_item_blocked_before_write = true
- prepare_remained_no_write_on_mismatch = true
- signed_wrong_job_blocked_by_controller = true
- route_runtime_selectable = false
- publish_allowed = false

## Bedeutung

Ein signiertes Job-Item kann nicht mehr nur „an der richtigen Stelle in der Reihenfolge“ stehen.

Es muss zusätzlich exakt zu dem PPM-Item passen, das tatsächlich vorbereitet wurde.

Damit wird verhindert:

- Job sagt Item A, PPM produziert Item B
- Prepared-Payload wird einem anderen Job-Item untergeschoben
- falsche Item-ID wird erst nach dem Write entdeckt

Mismatch wird direkt nach dem bereits schreibfreien `prepare()` blockiert.

Signatur startet nicht.
Write startet nicht.

## KISS

Kein neues Binding-Gate.

Die Prüfung sitzt im bereits vorhandenen Ein-Item-Adapter:
`expected signed item_id == prepared plan_item_key`

Der Controller kennt weiterhin keine alternative Route.

## Gesamtregression

P0 bis P37 gemeinsam PASS.
