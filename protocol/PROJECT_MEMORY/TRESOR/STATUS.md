# NOTFALL-TRESOR – STATUS

STAND: 2026-09-07

## AUFTRAG

**GITHUB ONLY**

Repository:
`hallo-netizen/affiliate-pferdeportal`

WordPress, Website-Backup und Projektarchiv gehören nicht zu diesem Auftrag.

## AKTUELLER GEPRÜFTER SNAPSHOT

GitHub Actions:
- Workflow: `Campus GitHub Complete Backup`
- Run: `34160894135`
- Attempt: `2`
- Ergebnis: `SUCCESS`
- Artifact ID: `10032706209`

Download-Datei:
`GITHUB_KOMPLETTBACKUP_2026-09-07_FINAL.zip`

SHA-256:
`b885d46a9ad7f9b521677da2cc4c0abcf6d9ecbf6356b83055fc18a6c1259a25`

Erzeugt:
`2026-09-07T20:58:14Z`

Point-in-time:
- main: `67143a95ee98d6a7ce15167dfd8103ceee087f2d`
- Campus-Branch im Paket: `52e2d49f63966fbc0e4ebc818c7ecc085637c2f1`
- Branches: 292
- Pull-Request-Refs: 174
- Tags: 1

## REALER RESTORE-NACHTEST

Exakt die erzeugte Download-Datei wurde separat erneut geprüft:

- äußerer SHA-256 → PASS;
- TAR lesbar → PASS;
- innerer SHA-256 → PASS;
- Release-Artefakt-Hash → PASS;
- Git-Bundle verify → PASS;
- Mirror-Clone → PASS;
- `git fsck --full --strict` → PASS.

Ergebnis:
`GITHUB_REPOSITORY_RESTORE_PASS`

## EXTERNE KOPIE

Zusätzlich außerhalb GitHubs abgelegt:

`/Campus-Tresor/GITHUB_KOMPLETTBACKUP_2026-09-07_FINAL.zip`

Pointer:
`/Campus-Tresor/LATEST_GITHUB_BACKUP.txt`

## AUTOMATIK

Wöchentlicher Lauf aktiv:
**Sonntag 03:17 Uhr Europe/Berlin.**

Regel:
Nur derselbe GitHub-only-Weg.
Bei FAIL wird die letzte funktionierende externe Kopie nicht ersetzt.

## NOCH OFFENE PROVIDERGRENZE

Mit dem normalen GitHub-Actions-`GITHUB_TOKEN` nicht lesbar:
- Actions Variables;
- Actions Permissions;
- Workflow Permissions;
- Actions Secret-Namen;
- Webhooks.

Diese Endpunkte liefern HTTP 403.

Aus den Workflowquellen ist der verwendete Secret-Name belegt:
`ENDSTEMPEL_PRIVATE_KEY`

GitHub gibt Secret-**Werte** nicht wieder heraus.

Darum Gesamtstatus korrekt:
`GITHUB_BACKUP_PREPASS`

Nicht behauptet:
`GITHUB_KOMPLETT_PASS`

## HARD RULE

Kein Rücksprung zu WordPress-/Website-/Projektarchiv-Backup.
