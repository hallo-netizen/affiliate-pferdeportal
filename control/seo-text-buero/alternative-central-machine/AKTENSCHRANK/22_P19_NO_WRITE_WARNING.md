# P19 – NO-WRITE-/CHECK-ONLY-PRÜFUNG DES NORMAL-DRAFT-PFADS

Datum: 2026-09-08
Status: WARNUNG / P20 VOR ARCHITEKTURENTSCHEIDUNG

## Harte Befunde

Im exakten
`PPM679_Normal_Draft_Pipeline::execute_plan`
existiert eine interne Phase:

`normal_check_only`

Aber danach ruft derselbe Pfad zwingend auf:

`self::create_drafts(...)`

und darin:

`PPM679_Normal_Draft_Adapter::create_draft(...)`

## Konsequenz

Der Begriff `check_only` im aktuellen Normal-Draft-Pfad ist KEIN Beweis für einen eigenständigen schreibfreien Endpunkt.

Der heute geprüfte `execute_plan`-Gesamtpfad erzeugt anschließend WordPress-Drafts.

Damit kann dieser Pfad nicht ungeprüft 1:1 hinter folgendes Zielbild gesetzt werden:

geprüfte Datei
-> externe Signatur
-> WordPress-Verifikation
-> erst dann WordPress-Write

## Wichtig: vorhandener KISS-Kandidat im selben unveränderten PPM

Gefunden wurde außerdem:

`includes/stateful-write-gate.php`

Dort existieren bereits:
- Dry-run
- `PASS_V31_WRITE_PLAN_PREPARED_NO_WRITE`
- `write_performed=false`
- Pflicht, dass Dry-run und Write exakt denselben planned-write fingerprint verwenden
- BLOCKED bei Fingerprint-/Binding-Abweichung

Zusätzlich:
`contracts/stateful-e2e-write-gate-v3-1.json`
enthält:
`same_code_path_for_dry_run_and_write=true`

Das ist potentiell genau die bereits vorhandene Trennung, die wir brauchen.

## KISS-Entscheidung

NICHT:
- Normal-Draft-Pipeline verändern
- create_drafts herauspatchen
- neuen No-Write-Controller bauen
- Fachregeln kopieren

Sondern zuerst P20:
prüfen, ob der vorhandene stateful write gate den bereits geprüften Fachoutput schreibfrei bindet und später exakt denselben Payload zum Write zwingt.

## GO/STOP

P19 selbst:
KEIN FULL-GO für direkte 1:1-Nutzung von `execute_plan` als Vor-Signatur-Produzent.

GO zu P20 ausschließlich zur Prüfung des bereits vorhandenen Write-Gates.

Wenn P20 nicht ohne neue Sonderarchitektur an den validierten Fachoutput gebunden werden kann:
STOP.
