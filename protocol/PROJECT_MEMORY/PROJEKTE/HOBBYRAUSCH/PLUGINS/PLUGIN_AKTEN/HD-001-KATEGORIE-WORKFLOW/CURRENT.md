# HD-001 – KATEGORIE-WORKFLOW – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-17
STATUS: **LIVE 1.14.8 UNVERÄNDERT / 1.14.9 VERWORFEN (AUTO-BOOTSTRAP/TIMEOUT) / 1.14.10 MANUAL-ONLY LOCAL HARD PASS / WORDPRESS-DRY-RUN OFFEN**

## Produktiver Live-Stand

Version:
`1.14.8`

Release:
`HD001_V1.14.8_RULE27_FINAL_VERIFIED_E2E_20261009.zip`

SHA-256:
`709134631895a901bcb4fc5f5d71889d317954d9928c0ed20700883990a5a52c`

Live-Revision:
`HD-TARGET-3P-RULE27-CATEGORY-GAPFIX-HOBBYFINDER-20261009+0f4dbf59238a7d83`

Live:
- 2357/2357;
- Frontend valid;
- 8 Welten;
- 330/330 Kategorie-Gate.

## Verworfen: 1.14.9

1.14.9 darf **nicht erneut installiert** werden.

Gefundene Ursache des Gateway Timeout:
- `APKW_TARGET_TREE_MANUAL_ONLY = false`;
- nach Versionswechsel konnte der Runner bereits auf normalem WordPress-`init` den Final-Target-Workflow automatisch anstoßen;
- dadurch konnte Installation/Aktivierung einen schweren Dry-Run/Sync-Pfad starten.

## Sicherer Kandidat 1.14.10

Artefakt:
`/hobby rausch/KATEGORIE_ZENTRALE/HD001_V1.14.10_MANUAL_ONLY_TIMEOUT_FIX_LOCALPASS.zip`

SHA-256:
`f9500d051249b239ca3215754eff54d37244fb80ef612ce54cfd5f722db7f243`

Sicherheitsänderung:
- Manual-only hart aktiv;
- kein automatischer WordPress-`init`-Bootstrap des Final-Target-Runners;
- Installation/Aktivierung lädt/verarbeitet nicht automatisch den Vollbaum;
- Dry-Run nur nach explizitem manuellen Start;
- Dry-Run startet keinen Sync;
- Apply/Sync bleibt separater bestätigungspflichtiger Weg.

Local QA:
- PHP 33/33 PASS;
- ZIP-Integrität PASS;
- Aktivierung/normaler Admin-Aufruf: 0 automatische Strukturarbeit;
- Dry-Run: 0 DataForSEO-Calls, 0 Writes;
- V3-Target Validator PASS.

## V3-Kategorienkandidat

Zentral:
`/hobby rausch/KATEGORIE_ZENTRALE/HOBBY_DEPOT_TARGET_PROFILE_AUDIT_CANDIDATE_V3_20261016.json`

- 2656 logische Knoten;
- 8 Hauptwelten unverändert;
- 370 terminale Hobbyseiten;
- 2160 unterste Inhaltskategorien;
- CREATE 282 / ADOPT 3 / UPDATE 2357 / ARCHIVE 0 im synthetischen Dry-Run.

## DataForSEO

Nur SEO-/Demand-/Intent-Evidence; keine Strukturautorität.

## EXAKT EINE NEXT ACTION

**Wenn der V3-Live-Dry-Run ausgeführt werden soll: ausschließlich HD-001 1.14.10 verwenden und zuerst nur den manuellen Finalen Delta-Dry-Run ausführen. Noch keinen Sync bestätigen.**
