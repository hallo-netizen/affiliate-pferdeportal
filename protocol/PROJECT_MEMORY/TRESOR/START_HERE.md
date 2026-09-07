# NOTFALL-TRESOR – START_HERE

STAND: 2026-09-07
STATUS: KISS-BACKUPKONZEPT VERBINDLICH

## WAS GILT?

Für das Pferde-Atelier gibt es genau **einen** Backupweg:

**GitHub komplett + WordPress komplett + Projektarchiv komplett → ein datiertes Sicherungspaket.**

Autorität:
`KONZEPT.md`

## HARTE REGEL

Keine neue Backup-Architektur daneben bauen.

Vorhandene Technik wird wiederverwendet:
- GitHub → Git-Mirror;
- WordPress → vorhandene Vollbackup-Lösung;
- Roh-/Masterdateien → Campus-Archiv.

## ERGEBNIS

Nur:
- `BACKUP_PASS`
- oder `BACKUP_FAIL:<GRUND>`

## NÄCHSTER SCHRITT

Aktuellen technischen Stand:
`STATUS.md`

Wiederherstellung:
`NOTFALL_WIEDERAUFBAU.md`

Alte V1/V2/V3/V4-Tresor-Kits und Ein-Datei-Experimente sind **nicht der verbindliche Nutzerweg**.
