# HD-001 – ISOLIERTES PLUGINARTEFAKT – MANIFEST

STAND: 2026-10-07
STATUS: V1.12.2 READ-ONLY DEPTH-KANDIDAT LOKAL VERIFIZIERT / GITHUB-CURRENT.zip BINARY_SYNC_BLOCKED

PLUGIN-ID:
`HD-001-KATEGORIE-WORKFLOW`

NAME:
`Affiliate-Portal Kategorie-Workflow`

NEUESTE LOKAL VERIFIZIERTE TECHNISCHE BASIS:
`1.12.2` (read-only V2-Tiefenprüfung; V1.12.0 bleibt Zielbaum-Baseline)

GEPRÜFTES ARTEFAKT:
`HD001_V1.12.2_V2_DATAFORSEO_DEPTH_READONLY_HARDPASS.zip`

SHA-256:
`233f3b5a71f6080d98e8748795cedb0b684c5e1a16407ec509919fa3d1f7e17f`

PRÜFBERICHT:
`HD001_V1.12.2_FINAL_LOCAL_POSNEG_REPORT.txt`

PRÜFBERICHT SHA-256:
`1e7197feb74e9b3a070a4201f79a0416f46dfef960fdab556d59f21c4cb55048`

PRÜFSTATUS:
- V1.12.1 realer Initial-Batch ausgeführt: 1 Overview / 106 von 263 returned / 0 Strukturwrites;
- V1.12.2 Fresh-Unpack PHP 62/62 PASS;
- Legacy Regression 270/270 PASS;
- V1.12 Positiv/Negativ + realer 908/844/841-Lauf PASS;
- echter Batch-001-Result-Readback PASS;
- V1.12.2 Follow-up-Plan: 37 Keyword Ideas + 1 Overview = 38 zusätzliche Calls PASS;
- DataForSEO-Failure fail-closed PASS;
- 0 Strukturwrites PASS;
- V1.12.2 ist Bewertungskandidat, KEIN Zielbaum-Deploymentkandidat.

CURRENT.zip:
In diesem Abschlusslauf NICHT synchronisiert.

GRUND:
Der aktive GitHub-Connector erlaubt Textupdates und Git-Blob-Erzeugung aus Stringinhalt, aber keinen direkten Binärtransfer des lokal verifizierten ZIP-Artefakts aus dem Container. Gemäß Artefaktregel wird daher kein Ersatz-`CURRENT.zip` erfunden und kein ungeprüftes Binärartefakt geschrieben.

NÄCHSTER ARTEFAKTSCHRITT:
Das installierbare V1.12.2-ZIP ist in der Hobbyrausch-Dateiablage vorhanden. Das isolierte GitHub-`CURRENT.zip` erst bei verfügbarem zulässigem Binär-Uploadweg bytegenau synchronisieren und erneut readback-prüfen.

AUTORITATIVE PLUGIN-WAHRHEIT:
`../../PLUGIN_AKTEN/HD-001-KATEGORIE-WORKFLOW/CURRENT.md`

Dieses Manifest ist nur Artefaktstatus, keine zweite Current-Wahrheit.
