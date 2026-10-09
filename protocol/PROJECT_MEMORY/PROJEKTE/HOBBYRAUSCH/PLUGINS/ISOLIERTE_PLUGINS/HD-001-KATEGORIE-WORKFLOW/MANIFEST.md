# HD-001 – ISOLIERTES PLUGINARTEFAKT – MANIFEST

STAND: 2026-10-09
STATUS: V1.14.4 FULL LOCAL HARD PASS / LIVE INSTALL + READBACK PENDING

PLUGIN-ID:
`HD-001-KATEGORIE-WORKFLOW`

NAME:
`Affiliate-Portal Kategorie-Workflow`

NEUESTE LOKAL VERIFIZIERTE BASIS:
`1.14.4`

GEPRÜFTES ARTEFAKT:
`HD001_V1.14.4_RULES_MAGAZIN_FULL_LOCAL_HARDPASS.zip`

SHA-256:
`9ec9b0d7b2776c59262aebbed9d3e9a88a533ce11084c4e66cd011a9126da06d`

PRÜFEVIDENCE:
`SEO_KATEGORIEN/HD001_V1_14_4_RULES_MAGAZIN_FULL_LOCAL_HARDPASS_20261009.json`

ZIELPROFIL:
`profiles/hobby-depot-v1.json` im V1.14.3-Artefakt

ZIELPROFIL SHA-256:
`08c1da1bb43add667b73ea02bbaab6d3ad3c3228de88673254d8d5ebbdb8996c`

HOBBY MASTER:
`profiles/hobby-master-v2-20261007.json` im V1.14.3-Artefakt

MASTER SHA-256:
`adf01a7ac9ae8a30813e9d27391d0732583671dd6c39b5cca19d33576dd8308f`

HISTORISCHER LOKALER V1.14.3-SOLLSTAND (ERSETZT):
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
V1.14.3-Zielbaum genau einmal live synchronisieren → Post-Sync-JSON herunterladen → 1.723/1.723 + Frontend/Header prüfen.
Kein zweiter Lauf vor dieser Prüfung.

LIVE-DRY-RUN 2026-10-09:
- PASS / valid=true;
- 1.293 CREATE + 430 UPDATE + 27 ARCHIVE;
- 0 Provider;
- 0 Writes;
- exakt lokales Migrationsdelta.

HISTORISCHE LOKALE V1.14.3-ABNAHME:
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

## CURRENT V1.14.4

Regelstand:
- Zielvertrag 2.6;
- Assessment Rules 1.6;
- 279 HOBBY_HUBs;
- 1.292 sichtbare Content-Kategorien;
- 0 autoritative Rule16-Capacity-Verstöße;
- keine Kategorie unter Kategorie;
- Magazin ohne Kopie des CORE-Hobbybaums.

Magazin:
- Hobby finden → Hobbyfinder / Hobbywelten;
- Nach Situation → 6 Leaf-Kategorien;
- Nach Jahreszeit → Winter / Sommer;
- Entdecken → 4 Leaf-Kategorien.

Lokaler Hardpass:
- 1.723/1.723 Readback COMPLETE;
- Header 102/102;
- Magazin 4/4;
- zweiter Sync 1.723 UNCHANGED / 0 Writes;
- Negativsuite fail-closed;
- PHP 33/33 Fresh-Unpack.

LIVE:
V1.14.3 ist nach realem Fehl-Sync vollständig ROLLED_BACK.
V1.14.4 ist noch NICHT live synchronisiert.

NEXT:
V1.14.4 installieren → Live-Dry-Run → ein kontrollierter Sync → Post-Sync-Readback.
