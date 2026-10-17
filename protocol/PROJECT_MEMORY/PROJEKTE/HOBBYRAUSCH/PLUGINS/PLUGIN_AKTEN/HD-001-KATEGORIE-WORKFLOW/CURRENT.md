# HD-001 – KATEGORIE-WORKFLOW – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-17
STATUS: **LIVE 1.14.9 UNSICHER / 1.14.11 V7 MANUAL-ONLY LOCAL HARD PASS / ECHTER WORDPRESS-DRY-RUN OFFEN**

## Live

Vom Nutzer am 2026-10-17 direkt aus WordPress bestätigt:
`Affiliate-Portal Kategorie-Workflow 1.14.9` ist aktiv.

**1.14.9 ist verworfen.**
Ursache des Gateway Timeout:
- automatischer Final-Target-Bootstrap konnte nach Versionswechsel auf normalem WordPress-`init` anlaufen.

## Einziger Kandidat

`/hobby rausch/KATEGORIE_ZENTRALE/HD001_V1.14.11_HOBBY_DEPOT_V7_MANUAL_ONLY_LOCALPASS.zip`

SHA-256:
`d441f36899ce8ef6fd8a47051ea066e24aeb41ac6ec07f28c2cae5c11444311e`

Enthält exakt:
`HOBBY_DEPOT_TARGET_PROFILE_V7_CALIBRATED_ROLLOUT_20261017`

Profil-SHA:
`a36a7b1b3639b503028d2339c17fcc04ca349769c4f3d2d5dfdb11f8061325fc`

Profil:
- 3517 Zielknoten;
- 381 terminale Hobbys.

## Safety-QA

- PHP 33/33 PASS;
- ZIP 47/47 PASS;
- embedded TargetTree valid;
- 0 TargetTree Errors;
- 0 TargetTree Warnings;
- `APKW_TARGET_TREE_MANUAL_ONLY=true`;
- Target-Runner-init-hooks: 0;
- Installation/Aktivierung: 0 Writes / 0 Schedules / 0 Network;
- Final-Dry-Run ruft nur DryRun-Build auf;
- Apply/Sync ausschließlich separater bestätigungspflichtiger Adminweg.

## Betriebsregel

Installation/Aktivierung darf keinerlei Vollbaum-Verarbeitung starten.

Dry-Run:
- lesen/auflösen/vergleichen;
- keine Writes;
- kein DataForSEO-Pflichtaufruf;
- kein Apply.

## EXAKT EINE NEXT ACTION

**1.14.11 über die aktive 1.14.9 installieren. Danach nur den manuellen Finalen V7-Dry-Run starten; keinen Apply/Sync bestätigen.**
