# HD-001 – ISOLIERTES PLUGINARTEFAKT – MANIFEST

STAND: 2026-10-08
STATUS: V1.13.1 LIVE-DRYRUN POST-ROLLBACK PASS / ZIELPROFIL-KORREKTUR MATERIALKUNST ERFORDERLICH / BINARY-ARTEFAKT NOCH NICHT NEU GEBAUT / GITHUB-CURRENT.zip BINARY_SYNC_BLOCKED

PLUGIN-ID:
`HD-001-KATEGORIE-WORKFLOW`

NAME:
`Affiliate-Portal Kategorie-Workflow`

NEUESTE LOKAL VERIFIZIERTE BASIS:
`1.13.1`

GEPRÜFTES ARTEFAKT:
`HD001_V1.13.1_PRACTICAL_FINAL_TARGET_ONE_SYNC_HARDPASS.zip`

SHA-256:
`94dca6cfc6c792cf2b866fc76fef1bff12551f9b375b38a1a511a91876b1a7b5`

PRÜFBERICHT:
`HD001_V1.13.1_FINAL_LOCAL_POSNEG_REPORT.txt`

PRÜFBERICHT SHA-256:
`f2649cbd1f132b1e48dfcf95cd05db805e024bf3d29c8b0d4d3aebda0594cd2d`

ZIELPROFIL:
`HD001_V1.13.1_PRACTICAL_TARGET_PROFILE_20261008.json`

ZIELPROFIL SHA-256:
`f5c6d9e5be7ee6184c50ded9db40549f4b1e2d2a8c29672f4eb7aa172ea8e014`

FINALER ZIELSTAND:
- 841 eingefrorene Hobby-Identitäten;
- 340 CORE;
- 501 Finder/Editorial;
- 440 aufgelöste Logikknoten;
- 431 physische Zielobjekte;
- 404 Pages;
- 8 Hauptwelten als physische CORE-Roots;
- Hobbywelten nur View über 8 Relations.

LOKALE ABNAHME:
- Regression 270/270 PASS;
- Final Target 24/24 PASS;
- Baseline-Migration 11/11 PASS;
- Fresh ZIP PHP 33/33 PASS;
- Dry-Run 0 Provider-Calls / 0 Writes;
- Fingerprint-Recheck vor Apply;
- Live-Drift BLOCKED;
- Legacy-Nichttarget-Kategorie wird NICHT archiviert;
- echte obsolete Target-Bindings werden archiviert;
- foreign collision BLOCKED.

CURRENT.zip:
NICHT synchronisiert.

GRUND:
Der aktive GitHub-Connector kann Textstände aktualisieren, aber das lokal verifizierte ZIP nicht byteidentisch in das isolierte GitHub-`CURRENT.zip` übertragen. Deshalb wird kein Binary-Artefakt erfunden.

NÄCHSTER ARTEFAKTSCHRITT:
Maschinenlesbaren Ein-Knoten-Patch `SEO_KATEGORIEN/HD001_V1_13_1_TARGET_PROFILE_PATCH_001_20261008.json` auf das V1.13.1-Zielprofil anwenden → Artefakt neu bauen und lokal hart prüfen → frischen read-only Live-Dry-Run → JSON-Readback prüfen. Noch kein Final-Sync.

AUTORITATIVE PLUGIN-WAHRHEIT:
`../../PLUGIN_AKTEN/HD-001-KATEGORIE-WORKFLOW/CURRENT.md`

Dieses Manifest ist nur Artefaktstatus, keine zweite Current-Wahrheit.
