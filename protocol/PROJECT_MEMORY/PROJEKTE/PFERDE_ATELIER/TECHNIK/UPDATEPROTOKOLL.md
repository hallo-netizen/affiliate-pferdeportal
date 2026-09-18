# PFERDE-ATELIER / TECHNIK – UPDATEPROTOKOLL

STAND: 2026-09-16

## TECH-20260916-001 – Speicheranalyse / WPvivid-Restbestände

AUSGANGSLAGE:
All-in-One-WP-Migration-Export war ungewöhnlich groß. Read-only Speicheranalyse zeigte zunächst rund 29,4 GB Dateibestand, überwiegend lokale Backupbestände.

BEREINIGUNG VOR DIESEM TECHNIKSTAND:
Die großen All-in-One-WP-Migration-Backups wurden serverseitig entfernt.

NEUER READ-ONLY-SCAN:
- Gesamt: 6,381,645,438 Bytes;
- `wp-content/wpvividbackups`: 5,154,903,563 Bytes / 126 Dateien;
- `wp-content/uploads`: 813,137,355 Bytes;
- `wp-content/ai1wm-backups`: 675 Bytes.

BEFUND:
Der verbleibende Hauptballast liegt eindeutig in `wp-content/wpvividbackups`. Die WPvivid-Oberfläche zeigt nicht alle dort physisch vorhandenen Dateien.

## TECH-20260916-002 – WordPress Speicheranalyse 1.1.0

BASIS:
Vom Nutzer bereitgestelltes Original `WordPress Speicheranalyse 1.0.1` / `pa-speicheranalyse/pa-speicheranalyse.php`.

ÄNDERUNG:
Bestehende read-only Analyse beibehalten. Ergänzt wurde eine eng begrenzte manuelle Löschfunktion für ausgewählte reguläre Dateien direkt in `wp-content/wpvividbackups/`.

SICHERHEIT:
- `manage_options`;
- WordPress nonce;
- Pfad-Hardlock auf den exakten WPvivid-Backupordner;
- keine Unterordner;
- keine Symlinks;
- keine Pfadtraversal-Pfade;
- keine automatische Löschung;
- Texteingabe `LOESCHEN`;
- Browserbestätigung.

TESTS:
PHP-Syntax PASS; ZIP PASS; Positivtest PASS; Negativtests Traversal/Symlink/außerhalb Scope PASS.

ARTEFAKT:
`/Campus-Plugins/PFERDE_ATELIER/PPA-014/CURRENT.zip`

SHA-256:
`3acb62811ec8e7ea1940ec0968e5b51fc2cb0d1ae2f9e86eeeb6718c11873891`

STATUS:
LOCAL HARD PASS. WordPress-LIVE-Installation und realer Readback offen.
