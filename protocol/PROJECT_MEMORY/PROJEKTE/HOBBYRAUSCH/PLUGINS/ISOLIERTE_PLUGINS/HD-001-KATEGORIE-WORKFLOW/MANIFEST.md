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

PRÜFEVIDENCE:
`SEO_KATEGORIEN/HD001_V1_14_3_RULE16_VISIBLE_FULL_LOCAL_HARDPASS_20261008.json`

ZIELPROFIL:
`profiles/hobby-depot-v1.json` im V1.14.3-Artefakt

ZIELPROFIL SHA-256:
`6578a1aa4dccf554bb685a36e564c32af897c85bb1aac06d0401c5fc683622b6`

HOBBY MASTER:
`profiles/hobby-master-v2-20261007.json` im V1.14.3-Artefakt

MASTER SHA-256:
`adf01a7ac9ae8a30813e9d27391d0732583671dd6c39b5cca19d33576dd8308f`

AKTUELLER LOKALER V1.14.3-SOLLSTAND:
- 855 kanonische Identitäten nach 5 Alias-Zusammenführungen;
- 332 finale CORE-Identitäten;
- 523 Editorial/Finder;
- 65 aktive Zwischenbereiche;
- 1.737 Logikknoten;
- 1.723 physische Zielobjekte;
- 408 Pages;
- 1.292 WordPress-category;
- 15 journal_cat;
- 8 hp_listing_category;
- 9 Relations;
- 102 Header-Navigationseinträge;
- 279/279 HOBBY_HUBs mit sichtbarer Content-Kategorieebene.

ABNAHME:
- PHP 33/33 PASS;
- ZIP-Integrität PASS;
- Migration gegen V1.14.1: 1.293 CREATE + 430 UPDATE + 27 ARCHIVE;
- 28 Legacy-Hobbyseiten identitätserhaltend migriert;
- Readback 1.723/1.723 COMPLETE;
- zweiter Dry-Run 1.723 UNCHANGED / 0 ARCHIVE;
- zweiter Sync 1.723 UNCHANGED / 0 ARCHIVE / 0 Writes;
- Frontend PASS;
- Header 102;
- lokale Welt-Kinder 7 / 11 / 11 / 5 / 10 / 7 / 8 / 8;
- 279/279 HOBBY_HUBs PASS;
- Negativsuite PASS/fail-closed.

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
