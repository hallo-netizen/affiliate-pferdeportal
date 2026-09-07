# NOTFALL-TRESOR – PRÜFVERTRAG GITHUB

STAND: 2026-09-07
STATUS: VERBINDLICH

## JEDER LAUF

1. Alle Git-Branches/Tags/PR-Refs frisch abrufen.
2. Git-Bundle erzeugen und verifizieren.
3. Bundle isoliert als Mirror klonen.
4. `git fsck --full --strict`.
5. Quell-Branchrefs gegen Restore vergleichen.
6. Pflicht-Metadaten als gültiges JSON sichern.
7. Release-Artefakte tatsächlich herunterladen.
8. Endarchiv erzeugen und wieder lesen.
9. SHA-256 erzeugen.

## STATUS

`GITHUB_REPOSITORY_RESTORE_PASS`:
Git und die gesicherten Refs sind real wiederherstellbar geprüft.

`GITHUB_BACKUP_PREPASS`:
Repository-Restore PASS, aber mindestens eine für „alle GitHub-Einstellungen“ relevante Adminquelle ist nicht lesbar.

`GITHUB_KOMPLETT_PASS`:
zusätzlich alle erforderlichen exportierbaren GitHub-Einstellungen gesichert oder nachweislich nicht vorhanden/nicht relevant.

## HART

Kein WordPress-Test.
Kein Website-Test.
Kein Projektarchiv-Test.
Kein PASS aufgrund eines alten Backups.
