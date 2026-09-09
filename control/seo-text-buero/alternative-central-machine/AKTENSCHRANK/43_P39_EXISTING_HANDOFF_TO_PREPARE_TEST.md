# P39 – BESTEHENDE HANDOFF-DATEI DIREKT AN PREPARE/SIGN-GRENZE

Datum: 2026-09-09
Status: TEST AKTIV

## KISS-Ziel

Keine neue Datei.
Kein neues Handoff-Format.
Kein neues Jobmanifest.
Kein neuer Fachworkflow.

Weiterhin genau:
`FACHWORKFLOW_HANDOFF_REQUEST.json`

## Zu beweisen

1. Der heutige `fachworkflow_proof_handoff.py materialize` erreicht den vollständigen PPM-Normal-Draft-Pfad und ist deshalb NICHT die richtige Vor-Signatur-Grenze.
2. Die bestehende 16-Feld-Handoff-Datei enthält bereits alle Identitäts-/Produktionskontexte für den schreibfreien PPM-`prepare()`-Punkt.
3. Der bereits bewiesene Ablauf bleibt:
   `prepare -> externe Signatur -> verifizierter Prepared-Payload -> create_draft -> readback`
4. Keine Mutation nach Signatur möglich.
5. publish_allowed=false.

## STOP-Regel

Falls dafür eine zweite Übergabedatei, ein zweites Jobmanifest oder ein weiterer Controller nötig wäre:
STOP.

Dann erst vorhandene Bausteine erneut prüfen.
