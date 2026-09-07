# LOKALES BACKUP – TECHNISCHE UMSETZUNG

STAND: 2026-09-07
STATUS: KISS

Autorität:
\`KONZEPT.md\`

## EIN LAUF

Ein Lauf erzeugt:

\`PFERDE_ATELIER_BACKUP_YYYY-MM-DD_HHMM/\`

mit:

\`\`\`
GITHUB/
WORDPRESS/
PROJEKTARCHIV/
BACKUP_INFO.txt
\`\`\`

### GITHUB
\`git clone --mirror\` plus relevanter Metadatenexport.

### WORDPRESS
Frisches Vollbackup mit der bereits vorhandenen WordPress-Backuptechnik.

### PROJEKTARCHIV
Aktueller \`/Campus-Archiv/\`-Stand.

### ABSCHLUSS
Hashes/Manifest prüfen.
Nur bei vollständigem Erfolg \`BACKUP_PASS\`.

## SPEICHERUNG

Mindestens zwei unabhängige Kopien:
- externe SSD;
- zweite externe/offsite Kopie.

## RHYTHMUS

- wöchentlich automatisch;
- zusätzlich vor größeren Umbauten/Releases.

## AUFBEWAHRUNG

- 4 letzte Wochensicherungen;
- 3 letzte Monatssicherungen.

## HISTORISCHE TECHNIK

Frühere V1/V2/V3/V4-Mac-Kits, Ein-Datei-Kapseln und serverseitige Tresor-Prototypen sind nur Entwicklungsbelege.

Sie definieren **keinen** zweiten Backupweg.
