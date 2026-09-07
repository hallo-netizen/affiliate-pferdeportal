# NOTFALL-TRESOR – PRÜFVERTRAG

STAND: 2026-09-07
STATUS: KISS / VERBINDLICH

## JEDER BACKUP-LAUF

Genau vier Prüfungen:

1. Git-Mirror vorhanden und lesbar.
2. WordPress-Vollbackup vorhanden und vollständig.
3. Projektarchiv vorhanden.
4. Manifest/Hashes stimmen.

Nur dann:

\`BACKUP_PASS\`

Sonst:

\`BACKUP_FAIL:<GRUND>\`

## WIEDERHERSTELLUNGSTEST

Ein echter Restore-Test wird durchgeführt:
- nach Einrichtung des Backupwegs;
- nach Änderungen am Backupweg;
- danach regelmäßig.

Der Restore-Test prüft:
- GitHub wiederherstellbar;
- WordPress wiederherstellbar;
- fehlende Projektrohdateien aus dem Archiv verfügbar.

## NEGATIVREGEL

Kein Teilbackup, kein alter Test und kein historischer PREPASS darf als aktueller \`BACKUP_PASS\` ausgegeben werden.
