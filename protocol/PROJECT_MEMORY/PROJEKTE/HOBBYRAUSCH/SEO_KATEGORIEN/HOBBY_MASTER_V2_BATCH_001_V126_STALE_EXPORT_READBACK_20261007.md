# HOBBY MASTER V2 – BATCH 001 – V1.12.6 STALE-EXPORT READBACK

STAND: 2026-10-07
STATUS: REALER USER-READBACK BEWEIST ALTEXPORT / V1.12.6 LOKAL HARD PASS / NEUER REALER EXPORT OFFEN

## Reale hochgeladene Datei

`hobby-master-v2-assessment-20261007-190209-utc.json`

SHA-256:
`086456f70d8896c51a97a27f7dcdc29906ad90534f9322aa6f1f5a7b519d69ae`

Interne Metadaten:
- plugin_version = 1.12.3
- result version = 1.1
- generated_at_utc = 2026-10-07T18:02:17+00:00
- DataForSEO paid_calls = 39
- total_cost_usd = 0.9738
- wordpress_structure_writes = 0
- summary = 0 Hub-Kandidaten / 2 ideale Leafs

Die Datei ist bytegleich mit dem bereits bekannten alten V1.12.3-Ergebnis.
Sie ist daher KEIN V1.12.5-Recalc-Readback.

## Root Cause

V1.12.5 recalculierte alte gespeicherte Ergebnisse nur beim Rendern der V2-Adminseite.

Der Download-Handler selbst:
- lud nur `last_result()`;
- serialisierte genau diesen gespeicherten Stand;
- führte vor dem Export keine KISS-Neuberechnung aus.

Dadurch konnte ein alter Browser-Tab bzw. ein direkter Download nach Plugin-Update weiterhin das unveränderte V1.12.3-Ergebnis exportieren.

## KISS-Fix V1.12.6

Der Download-Handler ist jetzt selbst fail-closed:

1. gespeichertes Ergebnis laden;
2. wenn `capacity_recalculation.version != 1.0`: kostenlose KISS-Neuberechnung ausführen;
3. neuen Stand speichern;
4. erst dann exportieren;
5. bei Fehler: Download BLOCKED statt stale JSON.

Keine Provider-Aufrufe.
Keine Provider-Kosten.
Keine Strukturwrites.

## Lokaler Test mit exakt der realen Datei

Direkter Download-Handler-Replay ergibt:
- plugin_version = 1.12.6
- result version = 1.3
- 16 Kandidaten
- 34 ideale Leafs
- 1 HOBBY_HUB_CANDIDATE
- 1 EDITORIAL_TOPIC_CANDIDATE
- 5 AGGREGATION_REVIEW
- 3 MACRO_REVIEW
- 6 EVIDENCE_REQUIRED
- target_tree_writes_allowed = 0
- provider_calls_added = 0
- provider_cost_added_usd = 0
- wordpress_structure_writes = 0

Idempotenter zweiter Download: PASS.
Kein gespeichertes Ergebnis: BLOCKED.

## Artefakt

`HD001_V1.12.6_STALE_EXPORT_FAILCLOSED_HARDPASS.zip`

SHA-256:
`788b49529216555cba8cd74aae2a3a469f5f386e7ea2dc3d0449555910d55dca`

Prüfbericht:
`HD001_V1.12.6_FINAL_LOCAL_POSNEG_REPORT.txt`

SHA-256:
`c9442f08b722e93a24fee697cec09d77e67f1ad9cd23cda9067a5185e90b042e`

## NEXT

V1.12.6 installieren und direkt `Ergebnis als JSON herunterladen` klicken.

Ein vorheriges Rendern/Neuladen der Bewertungsseite ist nicht mehr Voraussetzung.
Der Download selbst muss den alten Stand automatisch korrigieren.
