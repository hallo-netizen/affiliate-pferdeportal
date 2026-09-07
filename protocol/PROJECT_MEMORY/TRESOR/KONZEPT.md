# NOTFALL-TRESOR – GITHUB-KOMPLETTBACKUP

STAND: 2026-09-07
STATUS: GITHUB-ONLY / VERBINDLICH

## Ziel

Aus genau einer aktuellen Sicherungsdatei soll der gesicherte GitHub-Stand des Repositorys
`hallo-netizen/affiliate-pferdeportal`
so vollständig wie GitHub ihn exportierbar macht wiederaufbaubar sein.

## Inhalt

### Git vollständig
- komplette Commit-Historie;
- alle aktuellen Branches;
- alle Tags;
- GitHub-Pull-Request-Refs, damit auch PR-Commits nicht unnötig verloren gehen;
- Bundle-Manifest und Hashes.

### GitHub-Daten
- Repository-Metadaten;
- Branch-/Tag-Metadaten;
- Issues, Kommentare und Events;
- Pull Requests, Reviews und Review-Kommentare;
- Releases inklusive Release-Artefakten;
- Labels und Milestones;
- Rulesets;
- Workflows;
- Deployments;
- Environments, soweit lesbar;
- Collaborators, soweit lesbar;
- Actions-/Webhook-/Variablen-/Secret-Namen-Einstellungen, soweit GitHub sie der Backup-Identität lesbar macht;
- Wiki-Mirror, falls ein Wiki initialisiert ist.

## Eine Datei

Nutzerdownload:
`GITHUB_KOMPLETTBACKUP_YYYY-MM-DD.zip`

Die interne GitHub-Actions-Datei darf weitere Manifest-/Hashdateien enthalten; der Nutzer bekommt trotzdem genau einen Download.

## Prüfung vor Freigabe

Pflicht:
Git-Bundle erzeugen → Bundle verifizieren → isoliert klonen → `git fsck --full --strict` → Branch-Refs vergleichen → Metadaten prüfen → Release-Artefakte sichern → Archiv erneut lesen.

## Providergrenze

GitHub gibt **Secret-Werte** nicht wieder heraus.
Diese Werte können deshalb nicht durch einen GitHub-Export rekonstruiert werden.

Außerdem sind einzelne Admin-Einstellungen mit dem normalen `GITHUB_TOKEN` nicht lesbar.
Solange solche Einstellungen nicht lesbar oder als nicht relevant belegt sind, heißt der Gesamtstand:
`GITHUB_BACKUP_PREPASS`
und nicht `GITHUB_KOMPLETT_PASS`.

## Scope

**WordPress, Website-Backup und Projektarchiv gehören nicht in diesen GitHub-Backupauftrag.**
