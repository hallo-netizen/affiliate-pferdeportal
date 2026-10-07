# HD-001 – ISOLIERTES PLUGINARTEFAKT – MANIFEST

STAND: 2026-10-07
STATUS: V1.12.1 READ-ONLY BEWERTUNGSKANDIDAT LOKAL VERIFIZIERT / GITHUB-CURRENT.zip BINARY_SYNC_BLOCKED

PLUGIN-ID:
`HD-001-KATEGORIE-WORKFLOW`

NAME:
`Affiliate-Portal Kategorie-Workflow`

NEUESTE LOKAL VERIFIZIERTE TECHNISCHE BASIS:
`1.12.1` (read-only V2-Bewertung; V1.12.0 bleibt Zielbaum-Baseline)

GEPRÜFTES ARTEFAKT:
`HD001_V1.12.1_HOBBY_MASTER_V2_READONLY_ASSESSMENT_HARDPASS.zip`

SHA-256:
`959bc80217aac9b90ac107e6b315908b084704d09777ae9be990c2825245d33d`

PRÜFBERICHT:
`HD001_V1.12.1_FINAL_LOCAL_POSNEG_REPORT.txt`

PRÜFBERICHT SHA-256:
`3f34f58d0d7d35d0ac290e2926ac706f5fd6ff84e5a314d6ecde554204c89ac2`

PRÜFSTATUS:
- V1.12.1 Fresh-Unpack PHP 59/59 PASS;
- Legacy Regression 270/270 PASS;
- V1.12 Positiv/Negativ + realer 908/844/841-Lauf PASS;
- V2-Grenz-/Negativtests PASS;
- Bewertungslauf erzeugt 0 Strukturwrites;
- Target-Tree-Autorun und manueller Target-Tree-Refresh in V1.12.1 blockiert;
- reales Hobby-Depot-DataForSEO-Batch 001: NOCH NICHT AUSGEFÜHRT;
- V1.12.1 ist Bewertungskandidat, KEIN Zielbaum-Deploymentkandidat.

CURRENT.zip:
In diesem Abschlusslauf NICHT synchronisiert.

GRUND:
Der aktive GitHub-Connector erlaubt Textupdates und Git-Blob-Erzeugung aus Stringinhalt, aber keinen direkten Binärtransfer des lokal verifizierten ZIP-Artefakts aus dem Container. Gemäß Artefaktregel wird daher kein Ersatz-`CURRENT.zip` erfunden und kein ungeprüftes Binärartefakt geschrieben.

NÄCHSTER ARTEFAKTSCHRITT:
Das installierbare V1.12.1-ZIP ist in der Hobbyrausch-Dateiablage vorhanden. Das isolierte GitHub-`CURRENT.zip` erst bei verfügbarem zulässigem Binär-Uploadweg bytegenau synchronisieren und erneut readback-prüfen.

AUTORITATIVE PLUGIN-WAHRHEIT:
`../../PLUGIN_AKTEN/HD-001-KATEGORIE-WORKFLOW/CURRENT.md`

Dieses Manifest ist nur Artefaktstatus, keine zweite Current-Wahrheit.
