# PFERDE-ATELIER / TECHNIK – CURRENT_STATE

STAND: 2026-09-16
STATUS: BELASTBARER TECHNISCHER IST-STAND

## Aktueller Befund

Letzter vollständiger Speicher-Scan: 2026-09-16 15:22:56–15:23:24 UTC.

- Gesamt gescannt: `6,381,645,438` Bytes.
- `wp-content/wpvividbackups`: `5,154,903,563` Bytes / 126 Dateien.
- `wp-content/uploads`: `813,137,355` Bytes / 2.834 Dateien.
- `wp-content/ai1wm-backups`: nur noch 675 Bytes; die großen All-in-One-WP-Migration-Backups wurden entfernt.

Damit ist der aktuelle Hauptspeicherfresser eindeutig der physische Ordner `wp-content/wpvividbackups`.

WPvivid zeigt in seiner Oberfläche nur einen Teil der dort physisch vorhandenen Dateien. Der Scan belegt zusätzlich ältere SQL-/ZIP-Reste, u. a. aus August 2026. Keine pauschale Löschung ohne Sichtprüfung.

## Werkzeugstand

Plugin: **WordPress Speicheranalyse**

- bisher installiert/belegt: 1.0.1;
- neuer Installationskandidat: **1.1.0**;
- Plugin-Verzeichnis: `pa-speicheranalyse/`;
- Hauptdatei: `pa-speicheranalyse.php`;
- Plugin-ID im Pferde-Atelier-Pluginbüro: `PPA-014`;
- isolierte ZIP: `/Campus-Plugins/PFERDE_ATELIER/PPA-014/CURRENT.zip`;
- SHA-256: `3acb62811ec8e7ea1940ec0968e5b51fc2cb0d1ae2f9e86eeeb6718c11873891`.

1.1.0 ergänzt zur bestehenden read-only Analyse ausschließlich eine explizite, selektive Löschfunktion für reguläre Dateien direkt in `wp-content/wpvividbackups/`.

Lokale Prüfung 1.1.0:
- PHP-Syntax: PASS;
- ZIP-Integrität: PASS;
- Positivtest erlaubte Datei: PASS;
- Negativ Pfadtraversal: PASS;
- Negativ Symlink: PASS;
- Negativ Datei außerhalb des erlaubten Ordners: PASS.

## Statusgrenze

**Kein WordPress-LIVE-PASS für 1.1.0.**

Noch offen:
1. 1.1.0 im echten WordPress über 1.0.1 installieren;
2. physische WPvivid-Dateiliste im Plugin prüfen;
3. nur eindeutig entbehrliche Backup-Reste auswählen;
4. explizit löschen;
5. Speicheranalyse erneut laufen lassen und neuen Ist-Wert dokumentieren.

Keine Änderung an Beiträgen, Seiten, Kategorien, Medieninhalten, URLs, Design oder Datenbankstruktur ist Teil dieses Auftrags.
