# NOTFALL-TRESOR – KONZEPT

STAND: 2026-09-08
STATUS: VERBINDLICH

## ZIEL

Zwei voneinander unabhängige Sicherungen desselben GitHub-Projekts:

1. **Tresor automatisch und extern**
2. **lokales Backup manuell auf dem Mac**

Ein Ausfall des Macs darf den Tresor nicht verhindern.
Ein Ausfall des automatischen Tresorwegs darf die lokale Sicherung nicht verhindern.

## TRESOR – AUTOMATISCH

Quelle:
`hallo-netizen/affiliate-pferdeportal`

Technischer Weg:
`tresor/build-20260905`
→ `.github/workflows/campus-tresor-snapshot.yml`

Scheduler:
sonntags 03:17 Europe/Berlin.

Der Scheduler verändert nur
`control/tresor/AUTO_TRIGGER.txt`.
Der Push startet den bestehenden Backupworkflow.

Nach PASS:
neue datierte Sicherung unter
`/Campus-Tresor/`.

Pointer:
`/Campus-Tresor/LATEST_GITHUB_BACKUP.txt`

## LOKALES BACKUP

Auslöser:
Doppelklick auf
`GITHUB_BACKUP_STARTEN.command`.

Ergebnis:
`Schreibtisch/GitHub-Backup/GITHUB_BACKUP_AKTUELL.zip`.

## GEMEINSAMER SICHERUNGSUMFANG

Pflicht:
- komplette Git-Historie;
- Branches;
- Tags;
- Pull-Refs;
- sämtliche Repository-Dateien;
- kompletter Campus im Repository;
- exportierbare GitHub-Metadaten;
- Release-Artefakte soweit verfügbar;
- Manifest + Hashes;
- realer Git-Restore-Test.

## FAIL-CLOSED

Eine neue Sicherung ersetzt niemals den letzten gültigen Stand, wenn:
- Workflow fehlschlägt;
- Restore-Test fehlschlägt;
- Download/Upload fehlschlägt;
- die Sicherung nicht eindeutig dem neuen Lauf zugeordnet werden kann.

## GRENZE

GitHub kann Secret-Werte nicht zurückgeben.
Providerinterne IDs/Zeitstempel können bei einem kompletten GitHub-Neuaufbau nicht garantiert identisch reproduziert werden.
