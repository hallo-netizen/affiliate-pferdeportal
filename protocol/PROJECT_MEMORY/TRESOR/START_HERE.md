# NOTFALL-TRESOR – START_HERE

STAND: 2026-09-07
STATUS: GITHUB-ONLY / VERBINDLICH

## AUFTRAG

Dieser Tresor sichert ausschließlich:
**GitHub für `hallo-netizen/affiliate-pferdeportal`.**

Dazu gehören der komplette Git-Bestand und die für Wiederaufbau relevanten GitHub-Daten.

## HARD SCOPE LOCK

Für diesen Auftrag verboten:
- WordPress;
- Website-Dateien oder Datenbank;
- Campus-Library/Projektarchiv als eigener Sicherungsblock;
- WP-Plugins als Backup-Runner;
- neue Parallelarchitektur.

Der Campus liegt im Repository und wird durch das GitHub-Backup automatisch mitgesichert.

## TECHNISCHE HAUPTQUELLE

Bestehender, real gelaufener Weg:
Branch `tresor/build-20260905`
→ `.github/workflows/campus-tresor-snapshot.yml`

## NUTZERWEG

Genau eine Handlung:
**neueste geprüfte `GITHUB_KOMPLETTBACKUP_*.zip` herunterladen und außerhalb GitHubs speichern.**

Aktueller Prüfstand:
`STATUS.md`.

Wiederaufbau:
`NOTFALL_WIEDERAUFBAU.md`.
