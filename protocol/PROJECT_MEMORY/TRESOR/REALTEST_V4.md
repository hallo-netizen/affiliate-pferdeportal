# TRESOR – GITHUB-REALTEST

STAND: 2026-09-07
STATUS: AKTUELLER TESTBELEG

## Scope

Nur:
`hallo-netizen/affiliate-pferdeportal`

Kein WordPress.
Kein Website-Backup.
Kein Projektarchiv.

## Reale Ausführung

Workflow:
`Campus GitHub Complete Backup`

Run:
`34160894135`

Ergebnis:
`SUCCESS`

## Paketprüfung

Die tatsächlich erzeugte Datei wurde heruntergeladen und anschließend unabhängig erneut geprüft.

PASS:
- ZIP entpackbar;
- äußerer SHA-256 korrekt;
- `GITHUB_KOMPLETTBACKUP.tar.gz` lesbar;
- innerer SHA-256 korrekt;
- Git-Bundle verifiziert;
- Bundle als Mirror geklont;
- `git fsck --full --strict` bestanden;
- Release-Artefakt-Hash korrekt.

Ergebnis:
`GITHUB_REPOSITORY_RESTORE_PASS`

## Gesicherte Bestandszahlen dieses Laufs

- Branches: 291
- Tags: 1
- Pull-Request-Refs: 173
- Issues: 155
- Issue-Kommentare: 414
- Issue-Events: 703
- Pull Requests: 146
- Releases: 1
- Release-Artefakte: 1
- Labels: 9
- Milestones: 0
- Rulesets: 1
- Workflows: 70
- PR-Reviews: 1
- PR-Review-Kommentare: 1
- Deployments: 0
- Wiki: nicht initialisiert

## Noch nicht als Komplett-PASS bezeichnet

Nicht lesbare Admin-Endpunkte:
Actions Variables, Actions Permissions, Workflow Permissions, Actions Secret-Namen und Webhooks.

Verwendeter Secret-Name aus Workflowquellen:
`ENDSTEMPEL_PRIVATE_KEY`

Secret-Werte können aus GitHub nicht exportiert werden.

Darum:
`GITHUB_BACKUP_PREPASS`

Nicht:
`GITHUB_KOMPLETT_PASS`
