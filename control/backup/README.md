# Pferde-Atelier – Komplettsicherung

Ein Vorgang, ein Paket, ein Ergebnis: **PASS oder FAIL**.

Das Skript sichert:
- GitHub vollständig als Git-Mirror inklusive Historie, Branches und Tags
- exportierbare GitHub-Repository-Einstellungen
- WordPress-Datenbank
- komplette WordPress-Dateien

Datei:
`pferde-atelier-komplettsicherung.sh`

Einmalig setzen:

```bash
export WP_MODE="ssh"
export WP_SSH="user@host"
export WP_PATH="/pfad/zur/wordpress-installation"
```

Es werden keine Passwörter oder Zugangsdaten im Repository gespeichert.

Start:

```bash
bash control/backup/pferde-atelier-komplettsicherung.sh
```

Ergebnis:

`~/PFERDE_ATELIER_BACKUPS/PFERDE_ATELIER_BACKUP_JJJJ-MM-TT_HH-MM-SS.tar.gz`

Nur wenn GitHub **und** WordPress vollständig vorhanden und geprüft sind, meldet das Skript **PASS**. Ein Teilbackup wird niemals als Komplettsicherung ausgegeben.
