# NOTFALL-TRESOR – INHALTSVERTRAG

STAND: 2026-09-07
STATUS: KISS / VERBINDLICH

Eine Pferde-Atelier-Komplettsicherung enthält genau drei Datenblöcke:

## A. GITHUB

Pflicht:
- vollständiger Git-Mirror;
- komplette Historie;
- alle Branches;
- alle Tags;
- relevante GitHub-/Workflow-Metadaten, soweit exportierbar.

## B. WORDPRESS

Pflicht:
- Datenbank;
- komplette WordPress-Dateien;
- Uploads;
- Plugins;
- Themes;
- relevante Konfiguration.

Vorhandene WordPress-Backuptechnik verwenden.
Keinen zweiten Backupmotor bauen.

## C. PROJEKTARCHIV

Pflicht:
- alle projektwichtigen Roh-/Masterdateien, die nicht bereits vollständig durch GitHub oder WordPress gesichert sind;
- notwendige Recovery-Informationen, soweit für Wiederherstellung erforderlich.

Quelle:
\`/Campus-Archiv/\`

## D. MANIFEST

Jedes Paket enthält \`BACKUP_INFO.txt\` mit:
- Datum/Zeit;
- Git-Stand;
- WordPress-Backupstand;
- Projektarchivstand;
- Hash-/Prüfergebnis;
- Gesamtstatus.

## HARTE REGEL

Vollständig bedeutet:
Der **aktuelle funktionsfähige Projektstand** kann wiederhergestellt werden.

Nicht erforderlich ist das künstliche Sammeln jeder historischen Zwischen-ZIP, wenn deren Inhalt für die Wiederherstellung des aktuellen Standes bereits vollständig durch GitHub, WordPress oder das Projektarchiv gesichert ist.
