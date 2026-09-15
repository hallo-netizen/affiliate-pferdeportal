# NOTFALL-TRESOR – START_HERE

STAND: 2026-09-08
STATUS: VERBINDLICH

## AUFTRAG

Der Tresor ist die **unabhängige automatische Notfallsicherung** von
`hallo-netizen/affiliate-pferdeportal`.

Er läuft unabhängig vom Nutzer-Mac.

## ZWEI SICHERUNGSWEGE

### 1. TRESOR – automatisch
GitHub → serverseitiger geprüfter Backup-Lauf → externer Speicher
`/Campus-Tresor/`

Zeitplan:
**sonntags 03:17 Europe/Berlin**

Auslöser:
geplanter Tresor-Autolauf aktualisiert
`control/tresor/AUTO_TRIGGER.txt`
auf Branch
`tresor/build-20260905`.

Dadurch startet der bestehende Workflow:
`.github/workflows/campus-tresor-snapshot.yml`

Nur bei erfolgreichem Workflow + Restore-Prüfung wird die neue datierte Sicherung nach
`/Campus-Tresor/`
übernommen und
`LATEST_GITHUB_BACKUP.txt`
aktualisiert.

### 2. LOKALES BACKUP – manuell
Nutzer doppelklickt:
`GITHUB_BACKUP_STARTEN.command`

Ergebnis:
`Schreibtisch/GitHub-Backup/GITHUB_BACKUP_AKTUELL.zip`

## HARD RULE

Tresor und lokales Backup sind **unabhängig**.
Wenn längere Zeit kein lokales Backup gemacht wird, läuft der Tresor trotzdem weiter.

Alte gültige Tresorstände werden bei FAIL niemals überschrieben oder gelöscht.

## INHALT

Kompletter Git-Bestand einschließlich Campus unter
`protocol/PROJECT_MEMORY/**`
plus exportierbare GitHub-Metadaten.

Providergrenzen:
GitHub-Secret-Werte und einzelne interne Admininformationen sind nicht exportierbar.

Aktueller Prüfstand:
`STATUS.md`.
