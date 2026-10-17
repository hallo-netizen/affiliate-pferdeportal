# HD-001 – KATEGORIE-WORKFLOW – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-17
STATUS: **LIVE 1.14.9 UNSICHER / 1.14.12 V7.1 MANUAL-ONLY LOCAL HARD PASS / ECHTER WORDPRESS-DRY-RUN OFFEN**

## Live

Vom Nutzer direkt aus WordPress bestätigt:
`Affiliate-Portal Kategorie-Workflow 1.14.9` ist aktiv.

**1.14.9 ist verworfen.**
Ursache:
automatischer Final-Target-Bootstrap konnte nach Versionswechsel auf normalem WordPress-`init` anlaufen und Gateway Timeout verursachen.

## Einziger Kandidat

`/hobby rausch/KATEGORIE_ZENTRALE/HD001_V1.14.12_HOBBY_DEPOT_V7_1_MANUAL_ONLY_LOCALPASS.zip`

SHA-256:
`2a0ac6e936628baf7aff3b0ed67bdecd60a9ca9ba23d992396fa4d0abf2b0a5f`

Profil:
`HOBBY_DEPOT_TARGET_PROFILE_V7_1_DRYRUNFIX_20261017`

Profil-SHA:
`14b7b4b66310ccf19e51e9a4e403628af8705a5ae6f1e14e03f5c87f0991bc7e`

## Warum V7.1

Der erste echte Dry-Run-Test des V7-Profils blockierte korrekt, weil zwei historische Kontrollzähler noch auf dem alten 330er Stand standen.

V7.1 aktualisiert diese Kontrollzahlen auf den tatsächlich aufgelösten Bestand:
- 862 Entities;
- 383 CORE Entities;
- 381 terminale Hobby-Hubs;
- 2995 Content-Kategorien;
- 3487 physische Ziele.

Keine fachliche V7-Struktur wurde dadurch verändert.

## Safety-QA

- PHP 33/33 PASS;
- ZIP PASS;
- `APKW_TARGET_TREE_MANUAL_ONLY=true`;
- Target-Runner-init-hooks 0;
- Installation/Aktivierung: 0 Writes / 0 Schedules / 0 Network;
- echter Plugin-Resolver: 3517 Knoten / 862 Entities / 0 Errors / 0 Warnings;
- Dry-Run ruft keinen Apply auf;
- Apply/Sync bleibt separater bestätigungspflichtiger Adminweg.

## Echter Dry-Run-Simulations-PASS

Gegen simulierten alten Live-330er Zielbestand:
- CREATE 1128;
- ADOPT 3;
- UPDATE 2356;
- ARCHIVE 1;
- Errors 0;
- Provider Calls 0;
- WordPress Writes 0.

Audit:
`/hobby rausch/KATEGORIE_ZENTRALE/HOBBY_DEPOT_V7_1_ACTUAL_DRYRUN_SIM.json`

## EXAKT EINE NEXT ACTION

**1.14.12 über die aktive 1.14.9 installieren. Danach nur den manuellen Finalen Delta-Dry-Run starten; keinen Apply/Sync bestätigen.**
