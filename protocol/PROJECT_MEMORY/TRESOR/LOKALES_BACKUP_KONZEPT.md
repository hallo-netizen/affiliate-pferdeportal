# GITHUB-BACKUP – REGELMÄSSIGER EIN-KLICK-WEG

STAND: 2026-09-08
STATUS: VERBINDLICH

## Nutzerweg

Einmal Werkzeug ablegen.

Danach für jedes Backup nur:
**`GITHUB_BACKUP_STARTEN.command` doppelklicken.**

Keine GitHub CLI.
Kein WordPress.
Kein WPVibe.

## Aktuelle Datei

Fester Pfad:
`Schreibtisch/GitHub-Backup/GITHUB_BACKUP_AKTUELL.zip`

Diese Datei wird ausschließlich nach vollständigem PASS ersetzt.

Jeder erfolgreiche Lauf behält außerdem einen datierten Stand.

## Aktualitätsvertrag

Der Lauf bindet GitHub-Refs am Anfang und liest sie am Ende erneut.

Änderung während des Laufs:
`BACKUP_FAIL:GITHUB_WAEHREND_BACKUP_GEAENDERT`

Folge:
letzter gültiger aktueller Backupstand bleibt unverändert.

## Restore-Vertrag

PASS nur nach Restore aus der finalen ZIP selbst:

`ZIP → Bundle → Mirror → git fsck → Refvergleich → Campus-Blobvergleich`

PASS:
`GITHUB_DATEIEN_CAMPUS_1ZU1_RESTORE_PASS`

## Campus

Der Campus unter
`protocol/PROJECT_MEMORY/**`
wird auf allen enthaltenen Campus-Branches per Pfad + Git-Blob-Hash geprüft.

## Providergrenze

GitHub-Secret-Werte sind nicht exportierbar.
Providerinterne IDs/Zeitstempel sind nicht garantiert identisch reproduzierbar.

Diese Grenze ändert nichts am 1:1-Test der Git-Dateien und Campus-Dateien.
