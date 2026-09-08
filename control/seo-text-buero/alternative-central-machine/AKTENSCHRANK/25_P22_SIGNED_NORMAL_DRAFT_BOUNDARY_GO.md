# P22 – SIGNIERTE NORMAL-DRAFT-GRENZE

Datum: 2026-09-08
Status: GO

## Harte Ergebnisse

Der unveränderte Normal-Draft-Adapter wurde mit der bereits geprüften externen P7-Signaturgrenze verbunden.

Ablauf im isolierten Labor:

1. `PPM679_Normal_Draft_Adapter::prepare()`
2. schreibfreier Prepared-Datensatz
3. kanonisches Release
4. externe Ed25519-Signatur
5. Signatur-/Hash-/Schema-/No-Publish-Prüfung
6. Write-Input ausschließlich aus dem verifizierten signierten Release
7. `PPM679_Normal_Draft_Adapter::create_draft()`
8. exakter Draft-Readback

## PASS

- prepare_no_write = true
- planned_write_fingerprint vorhanden und im Payload gebunden
- externe Signatur verifiziert
- Write-Quelle ausschließlich VERIFIED_SIGNED_RELEASE_PAYLOAD_ONLY
- exakt ein Draft geschrieben
- Publish-Anzahl unverändert
- autoritativer Normal-Draft-Readback PASS
- Mutation nach Signatur BLOCKED
- Mutation + Neuberechnung des normalen Hashes trotzdem BLOCKED durch externe Signatur

## Architekturfolgerung

Die gewünschte Signaturgrenze ist ohne Änderung von PPM/Textmaschine möglich.

KISS-Zielpfad:

Fachproduktion / Prüfungen
-> Normal-Draft prepare()
-> kanonisches Prepared-Release
-> externe Signatur
-> verifizieren
-> exakt diesen signierten Prepared-Datensatz
-> create_draft()
-> Readback
-> kein Publish

Kein neuer Fachvalidator.
Kein interner Signer.
Kein privater Schlüssel im Produktionsworker.
Kein Chat-/Worker-Entscheid zwischen Signatur und Write.

## 0,0 Freiheit

PASS für diese Grenze.

Nach erfolgreichem prepare() kann ein Worker keine alternative Payload einschleusen:
jede Byte-/Inhaltsänderung zerstört Hash/Signatur.

## Regression

Im selben Lauf erneut PASS:
P0 bis P21 vollständig.

## Nächster Schritt P23

Zurück zum offenen Fachpfad:

`PPM679_Content_Validator::check`

Read-only prüfen, welche der 12 Pflichtgates dort bereits intern und fail-closed erzwungen werden.

Keine neue Fachlogik.
