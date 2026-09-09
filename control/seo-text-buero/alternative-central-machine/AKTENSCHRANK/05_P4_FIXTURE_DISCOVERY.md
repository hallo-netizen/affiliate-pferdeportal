# P4 – FIXTURE-DISCOVERY VOR ECHTEM PPM-LAUF

Datum: 2026-09-08
Status: DISCOVERY PASS, ECHTER PPM-LAUF FOLGT

## Befund

Im unveränderten, hashgebundenen PPM-6.7.9-Paket existieren bereits geeignete Originaltests.

Gefunden:
- positiver Normal-Draft-Test:
  `tests/normal-draft-production/test-01-positive-1-to-4.php`
- negativer Content/Link-Test:
  `tests/normal-draft-production/test-04-content-source-link-negative.php`

Beide rufen die reale PPM-Pipeline auf.
Der positive Test enthält die erwartete finale No-Publish-Statusprüfung.

## KISS-Entscheidung

Keine eigene Fixture bauen.
Keine Produktionsdaten erfinden.
Keine neue Testlogik für den Fachinhalt erfinden.

P4 verwendet exakt die bereits im Originalpaket vorhandenen Tests.

## Nächster Test innerhalb P4

1. PPM-Paketidentität erneut per SHA prüfen.
2. Originalpaket temporär entpacken.
3. positiven Originaltest ausführen.
4. negativen Content/Link-Originaltest ausführen.
5. nur wenn beide PASS: P4 GO/STOP bewerten.

Kein WordPress-Schreiben.
Kein Publish.
Keine Änderung an Textmaschine/PPM.
