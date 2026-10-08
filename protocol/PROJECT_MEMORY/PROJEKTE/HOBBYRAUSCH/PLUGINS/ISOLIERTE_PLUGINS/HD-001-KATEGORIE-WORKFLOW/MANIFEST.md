# HD-001 – ISOLIERTES PLUGINARTEFAKT – MANIFEST

STAND: 2026-10-08
STATUS: V1.14.3 RULE16 VISIBLE FULL LOCAL HARD PASS / LIVE-DRY-RUN PENDING / KEIN LIVE-SYNC

PLUGIN-ID:
`HD-001-KATEGORIE-WORKFLOW`

NAME:
`Affiliate-Portal Kategorie-Workflow`

NEUESTE LOKAL VERIFIZIERTE BASIS:
`1.14.3`

GEPRÜFTES ARTEFAKT:
`HD001_V1.14.3_RULE16_VISIBLE_FINAL_HARDPASS.zip`

SHA-256:
`deaee48b4f7310d94a5975b3dd471b0374d369745b1b7dd48c512ae514d7c7de`

PRÜFBERICHT:
`HD001_V1.14.1_EXPANSION19_FINAL_POSNEG_REPORT.txt`

PRÜFBERICHT SHA-256:
`5298211f6a86d33813cce5184b8cc2ab94303955968ff17970c7cbec35a5755e`

ZIELPROFIL:
`profiles/hobby-depot-v1.json` im V1.14.1-Artefakt

ZIELPROFIL SHA-256:
`6578a1aa4dccf554bb685a36e564c32af897c85bb1aac06d0401c5fc683622b6`

HOBBY MASTER:
`profiles/hobby-master-v2-20261007.json` im V1.14.1-Artefakt

MASTER SHA-256:
`adf01a7ac9ae8a30813e9d27391d0732583671dd6c39b5cca19d33576dd8308f`

AKTUELLER LOKALER V1.14.1-SOLLSTAND:
- 860 Hobby-Identitäten;
- 359 CORE;
- 501 Finder/Editorial;
- 60 aktive Zwischenbereiche;
- 466 aktive Logikknoten;
- 457 physische Zielobjekte;
- 430 Pages;
- 4 WordPress-category;
- 15 journal_cat;
- 8 hp_listing_category;
- 9 Relations;
- 97 Header-Navigationseinträge.

ABNAHME:
- Fresh-ZIP PHP 33/33 PASS;
- ZIP-Integrität PASS;
- Fresh Dry-Run 457 CREATE / 0 Provider / 0 Writes;
- Fresh Sync 457/457 COMPLETE;
- zweiter Sync 457 UNCHANGED;
- V1.14.0→V1.14.1 Migration 20 CREATE + 437 UPDATE + 0 ARCHIVE / COMPLETE;
- 430/430 Page-Frontend PASS;
- Header 97/97 PASS;
- Magazin/Anbieter/Hobbywelten/Front/Footer PASS;
- Negativ- und Rollbacksuite PASS/fail-closed.

CURRENT.zip:
NICHT synchronisiert.

GRUND:
Kein byteidentisches GitHub-Binary erfinden.

NÄCHSTER ARTEFAKTSCHRITT:
V1.14.3 installieren → Finaler Zielbaum → genau einen read-only Live-Dry-Run → JSON prüfen.
Kein Sync vor Live-Dry-Run-Abnahme.

LOKALE V1.14.3-ABNAHME:
- 1.723 Zielobjekte;
- 1.293 CREATE + 430 UPDATE + 27 ARCHIVE gegen V1.14.1-Profil;
- Readback 1.723/1.723;
- zweiter Sync 1.723 UNCHANGED / 0 Writes;
- Frontend PASS;
- Negativsuite PASS;
- PHP 33/33 PASS.

AUTORITATIVE PLUGIN-WAHRHEIT:
`../../PLUGIN_AKTEN/HD-001-KATEGORIE-WORKFLOW/CURRENT.md`

Dieses Manifest ist nur Artefaktstatus, keine zweite Current-Wahrheit.
