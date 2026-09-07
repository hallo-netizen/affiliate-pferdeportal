# NOTFALL-TRESOR – GITHUB-WIEDERAUFBAU

STAND: 2026-09-07
STATUS: GITHUB-ONLY

## Wiederaufbau

1. `GITHUB_KOMPLETTBACKUP_*.zip` entpacken.
2. enthaltenes `GITHUB_KOMPLETTBACKUP.tar.gz` entpacken.
3. Git-Bundle in ein neues leeres Repository spiegeln.
4. `git fsck --full --strict` ausführen.
5. Branches und Tags aus dem Manifest/Ref-Inventar prüfen.
6. GitHub-Metadaten als Wiederaufbauquelle verwenden:
   Issues/PRs/Releases/Labels/Milestones/Rulesets/Workflows usw.
7. Release-Artefakte wieder anbinden.
8. nicht exportierbare Secret-Werte aus ihrer separaten sicheren Recovery-Quelle neu setzen.

## PASS-GRENZE

Git-Restore:
`GITHUB_REPOSITORY_RESTORE_PASS`

Vollständiger GitHub-Neuaufbau:
erst nach realem Test eines leeren Zielrepositorys.

## HARD RULE

Das Backup ist READ/VERIFY/RESTORE ONLY und nie Arbeitsquelle.
