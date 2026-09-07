# LOKALES BACKUP – TECHNISCHE UMSETZUNG

STAND: 2026-09-07
STATUS: KISS / GETESTETER KANDIDAT

## AUTOMATISCHER LAUF

Bestehender Runner:
`control/tresor/build_tresor_release.sh`

Er benötigt nur fünf reale Bindungen:

- `WP_BACKUP_DIR`
- `PROJECT_ARCHIVE_DIR`
- `BACKUP_OUTPUT_DIR`
- `OFFSITE_DIR`
- `BACKUP_PASSPHRASE_FILE`

Danach erzeugt jeder Lauf automatisch:

`PFERDE_ATELIER_BACKUP_YYYY-MM-DD_HHMMSS.zip.gpg`

plus `latest.json`.

## WORDPRESS-KNOPF

Datei:
`control/tresor/pferde-atelier-backup-button.php`

Als MU-Plugin installieren und in `wp-config.php` einmal den geschützten Backupordner binden:

`PA_BACKUP_OUTPUT_DIR`

Danach:
**Werkzeuge → Komplettsicherung → Komplettsicherung herunterladen**

## SPEICHER

- aktuelle Serverkopie: nur für Status/Download;
- Offsite-Kopie: eigentliche unabhängige Katastrophensicherung;
- öffentlicher GitHub-Bereich: niemals Backup-Speicher.

## ZEITPLAN

Serverseitig einmal wöchentlich.
Vor größeren Umbauten kann derselbe Runner zusätzlich gestartet werden.

## REGEL

Ohne Offsite-Kopie kein `BACKUP_PASS`.
