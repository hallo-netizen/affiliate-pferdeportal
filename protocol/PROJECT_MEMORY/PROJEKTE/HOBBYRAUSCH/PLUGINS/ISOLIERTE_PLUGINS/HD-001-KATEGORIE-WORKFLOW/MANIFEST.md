# HD-001 – ISOLIERTES PLUGINARTEFAKT – MANIFEST

STAND: 2026-10-07
STATUS: V1.12.3 RESUMABLE DEPTH-KANDIDAT LOKAL VERIFIZIERT / GITHUB-CURRENT.zip BINARY_SYNC_BLOCKED

PLUGIN-ID:
`HD-001-KATEGORIE-WORKFLOW`

NAME:
`Affiliate-Portal Kategorie-Workflow`

NEUESTE LOKAL VERIFIZIERTE TECHNISCHE BASIS:
`1.12.3` (resumable read-only V2-Tiefenprüfung; V1.12.0 bleibt Zielbaum-Baseline)

GEPRÜFTES ARTEFAKT:
`HD001_V1.12.3_V2_DATAFORSEO_RESUMABLE_TIMEOUTSAFE_HARDPASS.zip`

SHA-256:
`bcb33caa3f481661654460db21cc1d407eb020124e85ab5941094f89ce2827a3`

PRÜFBERICHT:
`HD001_V1.12.3_FINAL_LOCAL_POSNEG_REPORT.txt`

PRÜFBERICHT SHA-256:
`4b04319e0efc78d128af0d23141eff83751ed38256b9acdc81a8b9ef4977165e`

PRÜFSTATUS:
- V1.12.1 realer Initial-Batch ausgeführt: 1 Overview / 106 von 263 returned / 0 Strukturwrites;
- V1.12.2 fachlicher Depth-Plan korrekt, live aber Timeout wegen 38 Calls in einem Request;
- V1.12.3 Fresh-Unpack PHP 64/64 PASS;
- Legacy Regression 270/270 PASS;
- V1.12 Positiv/Negativ + realer 908/844/841-Lauf PASS;
- V1.12.1/V1.12.2 Regression PASS;
- voller 38-Call-Depth-Lauf in 20 kleinen HTTP-Schritten PASS;
- Checkpoint nach jedem erfolgreichen Paid Call PASS;
- simulierter Timeout + Resume ohne Verlust PASS;
- 0 Strukturwrites PASS;
- V1.12.3 ist Bewertungskandidat, KEIN Zielbaum-Deploymentkandidat.

CURRENT.zip:
In diesem Abschlusslauf NICHT synchronisiert.

GRUND:
Der aktive GitHub-Connector erlaubt Textupdates und Git-Blob-Erzeugung aus Stringinhalt, aber keinen direkten Binärtransfer des lokal verifizierten ZIP-Artefakts aus dem Container. Gemäß Artefaktregel wird daher kein Ersatz-`CURRENT.zip` erfunden und kein ungeprüftes Binärartefakt geschrieben.

NÄCHSTER ARTEFAKTSCHRITT:
Das installierbare V1.12.3-ZIP ist in der Hobbyrausch-Dateiablage vorhanden. Das isolierte GitHub-`CURRENT.zip` erst bei verfügbarem zulässigem Binär-Uploadweg bytegenau synchronisieren und erneut readback-prüfen.

AUTORITATIVE PLUGIN-WAHRHEIT:
`../../PLUGIN_AKTEN/HD-001-KATEGORIE-WORKFLOW/CURRENT.md`

Dieses Manifest ist nur Artefaktstatus, keine zweite Current-Wahrheit.
