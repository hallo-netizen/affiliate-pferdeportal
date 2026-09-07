# NOTFALL-TRESOR – STATUS

STAND: 2026-09-07

## AKTUELLER AUFTRAG

**GITHUB ONLY**

Repository:
`hallo-netizen/affiliate-pferdeportal`

WordPress, Website-Backup und Projektarchiv sind nicht Bestandteil dieses Auftrags.

## TECHNIK

Verbindlicher bestehender Weg:
Branch `tresor/build-20260905`
→ `.github/workflows/campus-tresor-snapshot.yml`

Aktuell gesichert:
- kompletter Git-Bestand;
- 291 Branches;
- 1 Tag;
- 173 Pull-Request-Refs;
- Issues + Kommentare + Events;
- Pull Requests + Reviews + Review-Kommentare;
- Releases + Release-Artefakte;
- Labels + Milestones;
- Rulesets;
- Workflows;
- Deployments;
- Environments, soweit lesbar;
- Collaborators, soweit lesbar;
- Wiki, falls initialisiert;
- Actions-/Webhook-/Variablen-/Secret-Namen-Einstellungen, soweit GitHub sie lesbar macht.

## REALER TEST

Aktueller Workflow-Lauf:
`34160894135`

Ergebnis:
`SUCCESS`

Zusätzlich exakt aus der erzeugten Download-Datei geprüft:
- äußerer SHA-256 → PASS;
- innerer SHA-256 → PASS;
- TAR lesbar → PASS;
- Git-Bundle verify → PASS;
- Mirror-Clone → PASS;
- `git fsck --full --strict` → PASS.

Ergebnis:
`GITHUB_REPOSITORY_RESTORE_PASS`

## AKTUELLER PREPASS

Aktuelles getestetes Paket enthält:
- main SHA zum Laufzeitpunkt;
- 291 Branches;
- 173 PR-Refs;
- 1 Release-Artefakt;
- vollständige exportierte Kollaborations-/Metadatenklassen laut Inhaltsvertrag.

## PROVIDERGRENZE – NOCH KEIN GITHUB_KOMPLETT_PASS

Mit dem normalen GitHub-Actions-`GITHUB_TOKEN` nicht lesbar:
- Actions Variables → HTTP 403;
- Actions Permissions → HTTP 403;
- Workflow Permissions → HTTP 403;
- Actions Secret-Namen → HTTP 403;
- Webhooks → HTTP 403.

Direkt aus den Workflows nachgewiesener verwendeter Secret-Name:
`ENDSTEMPEL_PRIVATE_KEY`

Secret-**Werte** sind von GitHub grundsätzlich nicht exportierbar.

Darum aktuell korrekt:
`GITHUB_BACKUP_PREPASS`

Nicht behauptet:
`GITHUB_KOMPLETT_PASS`

## NÄCHSTE AKTION

1. aktuelle Campus-Korrekturen vollständig abschließen;
2. denselben GitHub-only Workflow danach noch einmal frisch laufen lassen;
3. exakt dieses finale Paket erneut restore-prüfen;
4. finale Datei außerhalb GitHubs sichern;
5. Admin-/Secret-Grenze separat schließen oder ausdrücklich als Providergrenze dokumentiert akzeptieren.

## HARD RULE

Kein Rücksprung zu WordPress-/Website-/Projektarchiv-Backup.
