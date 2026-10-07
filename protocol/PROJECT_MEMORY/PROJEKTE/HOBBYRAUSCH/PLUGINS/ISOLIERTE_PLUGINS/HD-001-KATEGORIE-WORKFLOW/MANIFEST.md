# HD-001 – ISOLIERTES PLUGINARTEFAKT – MANIFEST

STAND: 2026-10-07
STATUS: BINARY_SYNC_BLOCKED / CURRENT.zip NICHT ERSETZT

PLUGIN-ID:
`HD-001-KATEGORIE-WORKFLOW`

NAME:
`Affiliate-Portal Kategorie-Workflow`

NEUESTE LOKAL VERIFIZIERTE TECHNISCHE BASIS:
`1.12.0`

GEPRÜFTES ARTEFAKT:
`HD001_V1.12.0_FIXED_THREE_PILLAR_TARGET_TREE_POSNEG_HARDPASS.zip`

SHA-256:
`f77f676ef4e8df8d44e3cf0d1e61b52883d402924cb8d14033c24dd6645c03d1`

PRÜFBERICHT:
`HD001_V1.12.0_FINAL_LOCAL_POSNEG_REPORT.txt`

PRÜFSTATUS:
- lokaler technischer POS/NEG-E2E: PASS;
- reales Hobby-Depot-LIVE: NICHT ABGENOMMEN;
- fachliches V1.12-Hobby-Profil inzwischen durch HOBBY_MASTER-V2-Integration fortgeschrieben und daher KEIN aktueller Deploymentkandidat.

CURRENT.zip:
In diesem Abschlusslauf NICHT synchronisiert.

GRUND:
Der aktive GitHub-Connector erlaubt Textupdates und Git-Blob-Erzeugung aus Stringinhalt, aber keinen direkten Binärtransfer des lokal verifizierten ZIP-Artefakts aus dem Container. Gemäß Artefaktregel wird daher kein Ersatz-`CURRENT.zip` erfunden und kein ungeprüftes Binärartefakt geschrieben.

NÄCHSTER ARTEFAKTSCHRITT:
Sobald ein zulässiger Binär-Uploadweg verfügbar ist, exakt das oben gehashte ZIP als `CURRENT.zip` synchronisieren und SHA/ZIP/Version erneut readback-prüfen.

AUTORITATIVE PLUGIN-WAHRHEIT:
`../../PLUGIN_AKTEN/HD-001-KATEGORIE-WORKFLOW/CURRENT.md`

Dieses Manifest ist nur Artefaktstatus, keine zweite Current-Wahrheit.
