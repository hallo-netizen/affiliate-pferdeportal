# P21 – NORMAL-DRAFT-ADAPTER: PREPARE/WRITE-VERTRAG

Datum: 2026-09-08
Status: GO ZU P22

## Harte Befunde

Der unveränderte Normal-Draft-Adapter besitzt exakt diese Methoden:

- prepare(candidate, plan_item, evidence, runtime, run_id, plan_hash, state_hash)
- issue_write_authorization(prepared)
- verify_write_authorization(auth, payload, consume)
- create_draft(prepared)

## prepare() erzwingt vor dem Write

- nur zertifizierte Normal-Draft-Artikeltypen
- TECHNICAL_CHECK_OK
- CONTENT_QUALITY_CHECK_OK
- beide auf exakt demselben content_hash
- servergebundene Runtime-Identität
- verifizierten User-Trigger / manage_options
- exakte Live-Kategorieauflösung
- vollständige kanonische Artikelidentität
- keine Canonical-ID-Dublette
- keine Slug-Dublette
- keine normalisierte Titel-Dublette

Erst danach wird der WordPress-Payload gebaut.

## Bereits vorhandene Schreibbindung

prepare() erzeugt:
- finalen payload
- planned_write_fingerprint
- denselben Fingerprint in payload.meta._ppm679_planned_write_fingerprint

create_draft() ist separat.

Die interne Write-Autorisierung:
- bindet den exakten Payload-Hash
- ist one-use
- zweite Verwendung wird abgelehnt

Bestehender Originaltest:
PASS_NORMAL_DRAFT_READBACK_AUTH_STATIC

Bewiesen:
- one-use authorization PASS
- zweite Nutzung FAIL
- exakter Draft-Readback PASS
- Publish-Mutation im Readback FAIL
- kein Publish registriert

## Wichtige Architekturregel

Die externe Signatur muss NACH prepare() und VOR create_draft() liegen.

Da create_draft() seine interne Einmal-Autorisierung selbst erzeugt, darf die Zentralmaschine create_draft() ausschließlich nach erfolgreicher externer Signaturprüfung des exakt vorbereiteten Datensatzes aufrufen.

Kein Chat-/Worker-Entscheid.

## P22

Laborintegration:
prepare
-> kanonisches Release
-> externe Ed25519-Signatur
-> Importverifikation
-> exakte Prepared-Payload-Bindung
-> create_draft

Negativ:
jede Mutation nach Signatur muss vor create_draft blockieren.

Keine Änderung an PPM.
