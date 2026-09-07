# GITHUB-BACKUP – NUTZERWEG

STAND: 2026-09-07
STATUS: KISS

## Nutzer

Nur:
**eine aktuelle geprüfte `GITHUB_KOMPLETTBACKUP_YYYY-MM-DD.zip` herunterladen und außerhalb GitHubs speichern.**

Keine Terminal-Kommandos.
Keine Teilarchive.
Kein WordPress-Plugin.
Kein WPVibe.

## Intern

Technischer Weg:
`tresor/build-20260905`
→ `.github/workflows/campus-tresor-snapshot.yml`

Der Workflow baut und prüft das GitHub-Backup serverseitig.

## Automatik

Ziel:
wöchentlich denselben bestehenden Workflow auslösen.
Keine zweite Backup-Engine.

## Aufbewahrung

Mindestens die letzte funktionierende lokale Kopie nicht überschreiben, bevor der neue Stand geprüft wurde.
