# NOTFALL-TRESOR – EINFACHES BACKUPKONZEPT

STAND: 2026-09-07
STATUS: KISS-KONZEPT VERBINDLICH

## Ziel

Das Pferde-Atelier muss nach Totalausfall aus genau einem geprüften Sicherungsstand wiederherstellbar sein.

## Genau drei Inhalte

1. **GitHub komplett**
   - vollständiger Git-Mirror
   - gesamte Historie
   - alle Branches und Tags

2. **WordPress komplett**
   - vorhandenes vollständiges WordPress-Backup
   - Datenbank, Dateien, Uploads, Plugins, Themes, Konfiguration

3. **Projektarchiv komplett**
   - alle für Wiederaufbau benötigten Roh-/Masterdateien außerhalb von GitHub/WordPress

## Ergebnis

Ein verschlüsseltes Paket:

`PFERDE_ATELIER_BACKUP_YYYY-MM-DD_HHMMSS.zip.gpg`

Darin:

```
GITHUB/
WORDPRESS/
PROJEKTARCHIV/
BACKUP_INFO.txt
```

## Speicherort

**Nicht im öffentlichen Projekt-Repository.**

Jeder gültige Lauf erzeugt gleichzeitig:

1. eine aktuelle geschützte Kopie auf dem WordPress-/Backupserver für den Backend-Downloadknopf;
2. eine zweite unabhängige Kopie auf einem privaten externen/offsite Speicher.

Ohne erfolgreiche Offsite-Kopie gibt es kein `BACKUP_PASS`.

## Automatik

- einmal pro Woche automatisch;
- zusätzlich vor größeren Umbauten, sobald der Serverlauf eingebunden ist.

Der Lauf verwendet den bestehenden WordPress-Vollbackupstand und baut keinen zweiten WordPress-Backupmotor.

## WordPress-Backend

Unter **Werkzeuge → Komplettsicherung** steht:

- Status;
- Datum;
- Dateigröße;
- **Komplettsicherung herunterladen**.

Der Button liefert ausschließlich einen Stand mit `BACKUP_PASS` und prüft unmittelbar vor dem Download nochmals SHA-256.

## PASS

`BACKUP_PASS` nur wenn:

- Git-Mirror erstellt und `git fsck` bestanden;
- WordPress-Vollbackup vorhanden;
- Projektarchiv vorhanden;
- Paket verschlüsselt;
- SHA-256 erzeugt;
- unabhängige Offsite-Kopie erfolgreich geschrieben.

## Totalausfall

Für die Aussage **„1:1 wiederherstellbar“** reicht ein gebautes Backup allein nicht.

Ein echter leerer Wiederaufbau muss zusätzlich einmal vollständig bestanden werden:
Backup entschlüsseln → GitHub/Campus wiederherstellen → WordPress wiederherstellen → Projektarchiv prüfen.

Erst danach gilt:
`TOTALAUSFALL_RESTORE_PASS`.

## Hard Rules

- ein Backupweg;
- keine Parallelarchitektur;
- kein öffentliches Ablegen der Datenbank;
- vorhandene WordPress-Backuptechnik wiederverwenden;
- Backup nie als Arbeitsquelle;
- ein fehlendes historisches Einzel-ZIP ist kein automatischer Blocker, wenn der aktuelle funktionsfähige Stand vollständig wiederherstellbar gesichert ist.
