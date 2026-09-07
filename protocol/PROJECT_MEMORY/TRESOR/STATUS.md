# NOTFALL-TRESOR – STATUS

STAND: 2026-09-07

## KONZEPT

`BACKUP_KONZEPT_PASS`

Verbindlich:
**GitHub + WordPress + Projektarchiv → ein verschlüsseltes Paket → lokale geschützte Kopie + unabhängige Offsite-Kopie.**

## TECHNIK

Umgesetzt im Hobbyraum:

- `control/tresor/build_tresor_release.sh`
  - bestehender komplexer Builder durch KISS-Lauf ersetzt;
  - Git-Mirror;
  - vorhandenes .wpress-Vollbackup;
  - Projektarchiv;
  - ZIP-Paket;
  - AES-256/GPG-Verschlüsselung;
  - SHA-256;
  - Offsite-Kopie Pflicht;
  - `latest.json` für WordPress.

- `control/tresor/pferde-atelier-backup-button.php`
  - WordPress-Backendseite;
  - nur Administrator;
  - zeigt letzten Status;
  - Download nur bei `BACKUP_PASS`;
  - SHA-256 wird vor Download erneut geprüft.

- `control/tresor/restore_check.sh`
  - Entschlüsselung;
  - Paketstruktur;
  - Git-Mirror;
  - WordPress-Backup;
  - Projektarchiv;
  - PASS-Markierung.

## HARTE TESTS

Lokaler Techniktest:

- vollständiger Testlauf → `BACKUP_PASS`;
- Paket entschlüsselt und Struktur geprüft → `RESTORE_STRUCTURE_PASS`;
- fehlender Offsite-Speicher → korrekt BLOCK;
- fehlendes WordPress-Vollbackup → korrekt BLOCK;
- falsches Passwort → Restore korrekt BLOCK.

## LIVE NOCH OFFEN

Noch nicht behauptet:

`TOTALAUSFALL_RESTORE_PASS`

Dafür fehlen auf dem echten System noch:

1. WordPress-/Hosting-Zugriff für Installation des Backendknopfs;
2. Bindung des realen aktuellen WordPress-Backupordners;
3. Bindung des realen Projektarchivordners;
4. Bindung eines unabhängigen privaten Offsite-Speichers;
5. Aktivierung des wöchentlichen Serverlaufs;
6. einmaliger echter leerer Gesamt-Restore.

Bis dahin:
`BACKUP_LIVE_NOT_CONNECTED`
