# NOTFALL-TRESOR – GITHUB-WIEDERAUFBAU

STAND: 2026-09-08
STATUS: VERBINDLICH

## QUELLE A – LOKALE AKTUELLE SICHERUNG

Datei:
`GITHUB_BACKUP_AKTUELL.zip`

Wiederaufbau:
1. ZIP entpacken.
2. enthaltene Datei `repository/affiliate-pferdeportal.bundle` verwenden.
3. Bundle in ein neues leeres Mirror-Repository klonen.
4. `git fsck --full --strict`.
5. gesicherte Refs gegen das Ref-Inventar prüfen.
6. Campus `protocol/PROJECT_MEMORY/**` gegen das Campus-Manifest vergleichen.

Der reale unabhängige Mac-Test dieses Weges hat am 2026-09-08
`NOTFALL_WIEDERAUFBAU_PASS`
geliefert.

## QUELLE B – AUTOMATISCHER EXTERNER TRESOR

Aktueller Pointer:
`/Campus-Tresor/LATEST_GITHUB_BACKUP.txt`

Dort genannte datierte Tresordatei herunterladen.

Bei der aktuellen Workflow-Struktur:
1. äußere ZIP entpacken;
2. enthaltenes `GITHUB_KOMPLETTBACKUP.tar.gz` entpacken;
3. Git-Bundle verifizieren;
4. Bundle in ein neues leeres Mirror-Repository klonen;
5. `git fsck --full --strict`;
6. Ref-Inventar und Manifest prüfen;
7. exportierte GitHub-Metadaten und Release-Artefakte als Wiederaufbauquelle verwenden.

Der automatische Tresorweg wurde am 2026-09-08 real bis
`TRESOR_AUTO_BACKUP_REALTEST_PASS`
geprüft.

## GITHUB-METADATEN

Gesicherte GitHub-Metadaten dienen als Rekonstruktionsquelle für:
Issues/Kommentare/Events, Pull Requests/Reviews, Releases, Labels, Milestones, Rulesets, Workflows, Deployments usw., soweit GitHub sie exportierbar liefert.

Ein vollständiger Neuaufbau all dieser Metadaten in einem leeren GitHub-Zielrepository wurde **noch nicht** end-to-end als 1:1-PASS nachgewiesen.

Darum:
Git-/Ref-/Campus-Restore = real PASS.
`GITHUB_KOMPLETT_PASS` = weiterhin OFFEN.

## PROVIDERGRENZE

GitHub gibt Secret-Werte nicht zurück.
Einzelne Admininformationen sind je nach Berechtigung nicht lesbar.
Providerinterne IDs/Zeitstempel können bei Neuaufbau nicht garantiert identisch reproduziert werden.

Diese Punkte dürfen niemals als 1:1-PASS behauptet werden.

## HARD RULE

Backup/Tresor/Mirror = READ / VERIFY / RESTORE ONLY.

Nach einem Restore zuerst einen frischen offiziellen Arbeits-Worktree außerhalb des Tresors herstellen und danach wieder den normalen Campus-/Projekt-Eingang verwenden.
