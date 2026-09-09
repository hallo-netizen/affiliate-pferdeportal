# P20 – EXISTIERENDE WRITE-GATE-/FINGERPRINT-STRUKTUR

Datum: 2026-09-08
Status: TEIL-GO / NORMAL-DRAFT-ADAPTER IST DER KISS-KANDIDAT

## Ergebnis

Der bestehende `PPM679_Stateful_Write_Gate` besitzt:
- schreibfreie Planvorbereitung
- `PASS_V31_WRITE_PLAN_PREPARED_NO_WRITE`
- `write_performed=false`
- identischen Dry-run-/Write-Fingerprint
- fail-closed bei Fingerprint-/Binding-Abweichung

Aber:
Seine sichtbare Planmethode ist auf
`prepare_single_faq_plan`
zugeschnitten.

Damit wird dieser alte Gate-Baustein NICHT ungeprüft auf den Normal-Draft-Weg übertragen.

## Entscheidender KISS-Befund im Normal-Draft selbst

`includes/normal-draft-adapter.php` besitzt bereits:

- `prepare(...)`
- `create_draft(...)`
- `issue_write_authorization(...)`
- `verify_write_authorization(...)`

Und `prepare(...)` erzeugt bereits:

- den späteren WordPress-Payload
- `planned_write_fingerprint`
- denselben Fingerprint in
  `payload.meta._ppm679_planned_write_fingerprint`

Damit existiert die gewünschte technische Trennstelle möglicherweise bereits direkt im Normal-Draft-Adapter.

## Noch nicht bewiesen

P20 beweist noch nicht:
- dass `prepare()` garantiert keinen Write ausführt
- dass `create_draft()` ohne gültige Autorisierung blockiert
- dass Payload-Mutation nach `prepare()` blockiert
- dass exakt derselbe vorbereitete Payload später geschrieben wird

## P21

Harter Positiv-/Negativtest genau dieser vorhandenen Schnittstelle:

1. `prepare()` -> kein WordPress-Write
2. vorbereitetes Ergebnis enthält stabilen Fingerprint
3. `create_draft()` ohne gültige Write-Autorisierung -> BLOCKED
4. mutierter Payload/Fingerprint -> BLOCKED
5. korrekt autorisierter unveränderter Payload -> Draft-only
6. Publish bleibt unmöglich

Wenn PASS:
Kein neuer Write-Gate-Baustein.
Die bestehende Normal-Draft-Adapter-Trennung wird als Signaturgrenze verwendet.

Keine PPM-Änderung.
Keine Textmaschinenänderung.
