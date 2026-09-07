# NOTFALL-TRESOR – EINFACHES BACKUPKONZEPT

STAND: 2026-09-07
STATUS: KISS-KONZEPT VERBINDLICH

## Ziel

Das Pferde-Atelier muss nach Datenverlust vollständig wiederherstellbar sein.

Dafür gibt es genau **einen** Backupweg.

## Die Komplettsicherung besteht aus 3 Blöcken

### 1. GitHub komplett
Gesichert werden:
- gesamtes Repository;
- komplette Git-Historie;
- alle Branches;
- alle Tags;
- relevante Repository-/Workflow-Einstellungen, soweit exportierbar.

Technik:
ein vollständiger Git-Mirror plus Metadatenexport.

### 2. WordPress komplett
Gesichert werden:
- Datenbank;
- komplette WordPress-Dateien;
- Uploads/Bilder;
- Plugins;
- Themes;
- relevante Konfiguration.

Regel:
Die bereits vorhandene WordPress-Backuptechnik wird genutzt.
**Kein zweiter WordPress-Backupmotor wird erfunden.**

### 3. Projektarchiv komplett
Gesichert werden nur die projektwichtigen Roh-/Masterdateien, die weder vollständig in GitHub noch im WordPress-Vollbackup enthalten sind.

Quelle:
\`/Campus-Archiv/\`

Dazu gehören auch notwendige Recovery-Informationen, soweit sie nicht anderweitig sicher wiederherstellbar sind.

## Ergebnis jedes Laufs

Alles kommt in genau **ein datiertes Sicherungspaket**:

\`PFERDE_ATELIER_BACKUP_YYYY-MM-DD_HHMM\`

Inhalt:

\`\`\`
GITHUB/
WORDPRESS/
PROJEKTARCHIV/
BACKUP_INFO.txt
\`\`\`

Optional kann dieses Paket anschließend als eine verschlüsselte Archivdatei gespeichert werden.
Die Verschlüsselung ändert nichts am einfachen Grundmodell.

## Speicherung

Von jedem gültigen Sicherungsstand existieren mindestens **2 unabhängige Kopien**:

1. externe SSD / lokaler unabhängiger Datenträger;
2. zweite Kopie außerhalb dieses Datenträgers, z. B. Cloud oder zweites Laufwerk an anderem Ort.

Die aktive Website, GitHub selbst oder die ChatGPT-Library zählen nicht als eine dieser beiden unabhängigen Sicherungskopien.

## Rhythmus

- automatisch **1× pro Woche**;
- zusätzlich **vor größeren Umbauten / Releases**.

Aufbewahrung:
- letzte 4 Wochensicherungen;
- zusätzlich letzte 3 Monatssicherungen.

Ältere gültige Sicherungen werden nie durch einen fehlerhaften neuen Lauf überschrieben.

## Prüfung

Jeder Lauf endet nur mit:

\`BACKUP_PASS\`
oder
\`BACKUP_FAIL:<GRUND>\`

Für \`BACKUP_PASS\` reicht die einfache technische Prüfung:

- Git-Mirror vorhanden und lesbar;
- WordPress-Vollbackup vorhanden;
- Projektarchiv vorhanden;
- Manifest/Hashes stimmen.

Zusätzlich wird regelmäßig und nach Änderungen am Backupweg ein echter Wiederherstellungstest durchgeführt.

## Wiederherstellung

Im Notfall:

1. GitHub aus dem Git-Mirror wiederherstellen;
2. WordPress aus dem Vollbackup wiederherstellen;
3. fehlende Roh-/Masterdateien aus dem Projektarchiv zurückspielen;
4. Manifest prüfen;
5. Projekt normal über den Campus starten.

## Harte Regeln

- **Ein Backupweg.**
- **Keine Parallelarchitektur.**
- **Keine neuen Backup-Tools, wenn vorhandene Technik den Zweck erfüllt.**
- **Kein Teilbackup darf als Komplettsicherung bezeichnet werden.**
- **Backup ist nie Arbeitsquelle.**
- **Fehlende historische Installer-ZIPs blockieren die Komplettsicherung nicht automatisch, wenn der aktuelle funktionsfähige Stand durch GitHub oder das WordPress-Vollbackup vollständig wiederherstellbar ist.**

## Nutzerweg

Der Nutzer soll im Normalbetrieb nichts zusammensetzen und keine Einzelarchive verwalten.

Ziel:
**ein aktuelles Sicherungspaket sehen → BACKUP_PASS → fertig.**
