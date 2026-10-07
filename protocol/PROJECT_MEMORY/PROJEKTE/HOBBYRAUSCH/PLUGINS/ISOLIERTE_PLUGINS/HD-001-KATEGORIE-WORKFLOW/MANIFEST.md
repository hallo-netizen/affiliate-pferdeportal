# HD-001 – ISOLIERTES PLUGINARTEFAKT – MANIFEST

STAND: 2026-10-07
STATUS: V1.12.6 STALE-EXPORT-FAILCLOSED LOKAL VERIFIZIERT / GITHUB-CURRENT.zip BINARY_SYNC_BLOCKED

PLUGIN-ID:
`HD-001-KATEGORIE-WORKFLOW`

NAME:
`Affiliate-Portal Kategorie-Workflow`

NEUESTE LOKAL VERIFIZIERTE TECHNISCHE BASIS:
`1.12.6` (read-only V2-KISS-Bewertung; V1.12.0 bleibt Zielbaum-Baseline)

GEPRÜFTES ARTEFAKT:
`HD001_V1.12.6_STALE_EXPORT_FAILCLOSED_HARDPASS.zip`

SHA-256:
`788b49529216555cba8cd74aae2a3a469f5f386e7ea2dc3d0449555910d55dca`

PRÜFBERICHT:
`HD001_V1.12.6_FINAL_LOCAL_POSNEG_REPORT.txt`

PRÜFBERICHT SHA-256:
`c9442f08b722e93a24fee697cec09d77e67f1ad9cd23cda9067a5185e90b042e`

REALER AUSGANGSBEFUND:
Der nach V1.12.5 hochgeladene Download war bytegleich mit dem alten V1.12.3-Ergebnis.
SHA-256:
`086456f70d8896c51a97a27f7dcdc29906ad90534f9322aa6f1f5a7b519d69ae`

ROOT CAUSE:
V1.12.5 recalculierte nur beim Rendern der Bewertungsseite. Der Download-Handler exportierte den gespeicherten Altstand ungeprüft.

V1.12.6:
- Download selbst recalculiert Altstand;
- fail-closed bei Recalc-Fehler;
- 0 Provider-Aufrufe;
- 0 neue Kosten;
- 0 Strukturwrites.

LOKALER TEST MIT EXAKTER REALDATEI:
- plugin_version 1.12.6;
- 34 ideale Leafs;
- 1 Hub-Kandidat;
- 1 Editorial-Kandidat;
- 5 Aggregation-Reviews;
- 3 Macro-Reviews;
- 6 Evidence-Required;
- 0 Zielbaum-Writes;
- idempotenter zweiter Export PASS;
- fehlendes Ergebnis BLOCKED PASS;
- PHP 31/31 PASS;
- ZIP-Integrität PASS.

CURRENT.zip:
In diesem Abschlusslauf NICHT synchronisiert.

GRUND:
Der aktive GitHub-Connector kann Textdateien aktualisieren, aber das lokal verifizierte ZIP nicht als byteidentisches Binärartefakt in das isolierte GitHub-`CURRENT.zip` schreiben. Deshalb wird kein Ersatzartefakt erfunden.

NÄCHSTER ARTEFAKTSCHRITT:
Das installierbare V1.12.6-ZIP liegt als geprüftes Gesprächs-/Library-Artefakt vor.
Das isolierte GitHub-`CURRENT.zip` erst bei verfügbarem zulässigem Binär-Uploadweg bytegenau synchronisieren und SHA/Version erneut readback-prüfen.

AUTORITATIVE PLUGIN-WAHRHEIT:
`../../PLUGIN_AKTEN/HD-001-KATEGORIE-WORKFLOW/CURRENT.md`

Dieses Manifest ist nur Artefaktstatus, keine zweite Current-Wahrheit.
