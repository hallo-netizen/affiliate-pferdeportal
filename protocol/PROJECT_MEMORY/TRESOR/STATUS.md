# NOTFALL-TRESOR – STATUS

STAND: 2026-09-07

## KONZEPT

\`BACKUP_KONZEPT_PASS\`

Verbindlicher Weg:
**GitHub + WordPress + Projektarchiv → ein datiertes Sicherungspaket → zwei unabhängige Kopien.**

## VORHANDENE BAUSTEINE

- GitHub-Repository und Git-Historie: vorhanden.
- Git-/GitHub-Restore-Prüfung: bereits grundsätzlich belegt.
- WordPress-Vollbackup-Technik: vorhanden; auf dem Pferde-Atelier wurden bereits vollständige Backups mit vorhandenen WordPress-Backupwerkzeugen erzeugt.
- Campus-/Projektarchiv: vorhanden und bereits mit Hash-/Restore-Prüfungen bearbeitet.

## WAS NOCH FEHLT

Es fehlt nur noch die **Zusammenführung zu einem frischen aktuellen Komplettlauf nach dem neuen einfachen Konzept**:

1. frischen Git-Mirror erzeugen;
2. frisches WordPress-Vollbackup erzeugen;
3. aktuellen Campus-Archivstand dazunehmen;
4. Manifest/Hashes prüfen;
5. Paket auf zwei unabhängigen Speicherorten ablegen.

Bis dieser reale Lauf erfolgt ist:

\`BACKUP_REAL_RUN_OPEN\`

## WICHTIGE VEREINFACHUNG

Eine fehlende historische Einzel-ZIP blockiert das Backup nicht automatisch.

Entscheidend ist:
**Kann der aktuelle funktionsfähige Projektstand aus GitHub + WordPress-Vollbackup + Projektarchiv vollständig wiederhergestellt werden?**

Die frühere starre Forderung nach jeder einzelnen historischen Design-1.50.472-ZIP ist daher **kein eigenständiger Komplettbackup-Blocker mehr**, sofern der aktuelle installierte/gebundene Stand vollständig gesichert und wiederherstellbar ist.

## NICHT MEHR VERBINDLICH

Die früheren V1/V2/V3/V4-Mac-Kits, serverseitigen Ein-Datei-Experimente und mehrstufigen Tresorvarianten bleiben nur historische Entwicklungsbelege.

Sie dürfen keinen neuen Backupweg erzeugen.

## NEXT ACTION

Genau ein realer Komplettlauf nach \`KONZEPT.md\`.
