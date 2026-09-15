# LOKALES GITHUB-BACKUP

STAND: 2026-09-08
STATUS: VERBINDLICH

## ROLLE

Das lokale Backup ist die **zusätzliche manuelle Sicherung** auf dem Nutzer-Mac.

Es ist nicht vom Tresor abhängig.
Der Tresor läuft separat automatisch.

## AUSLÖSER

Nur:
`GITHUB_BACKUP_STARTEN.command` doppelklicken.

## ERGEBNIS

`Schreibtisch/GitHub-Backup/GITHUB_BACKUP_AKTUELL.zip`

Diese Datei wird nur nach vollständigem PASS ersetzt.

Jeder erfolgreiche Lauf behält zusätzlich einen datierten Stand.

## AKTUALITÄT

GitHub-Refs am Anfang binden.
Nach Erstellung und Restore-Test erneut lesen.

Änderung während des Laufs:
`BACKUP_FAIL:GITHUB_WAEHREND_BACKUP_GEAENDERT`

Dann bleibt der letzte gültige lokale Stand unverändert.

## RESTORE-PASS

Pflicht:
`ZIP → Hashprüfung → Bundle → Mirror → git fsck → Refvergleich → Campus-Blobvergleich`

PASS:
`GITHUB_DATEIEN_CAMPUS_1ZU1_RESTORE_PASS`

und

`AKTUELLITAET_PASS`

## CAMPUS

`protocol/PROJECT_MEMORY/**`
wird für die enthaltenen Campus-Branches per Pfad + Git-Blob-Hash geprüft.

## VERHÄLTNIS ZUM TRESOR

Tresor:
automatisch + extern + sonntags.

Lokales Backup:
manuell + Mac + Doppelklick.

Beide sichern denselben GitHub-Projektbestand, sind aber unabhängig voneinander.
