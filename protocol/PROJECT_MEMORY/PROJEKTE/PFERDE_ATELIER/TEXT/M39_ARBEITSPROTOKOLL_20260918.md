# PFERDE ATELIER – TEXT – M39 ARBEITSPROTOKOLL

STAND: 2026-09-18
STATUS: HISTORY_AUTHORITY_MAINTENANCE / PRODUKTFIX GETRENNT

## REALBEFUND

Current main:
`e69cab0f0a96978b997bff7cbf1ab8af4587e772`

Letzter belastbarer Pre-Codex-Recovery-Stand:
`508f9dbb3650c99e5d41dbab83086af46945e225`

Aktueller technischer Blocker:
`CURRENT_7ER_BATCH_ALREADY_HAS_DURABLE_RELEASE_IDENTITY_COLLISION`

Der bestehende 7er-Batch besitzt bereits eine historische dauerhafte Endstempel-Ausgabe unter derselben Batch-ID. Ein neuer NEW-Lauf mit neuen Artikelbytes würde beim späteren Release an Replay-/Zielkollisionen stoßen.

## M39-SOLL

- logische Batch-ID bleibt unverändert;
- pro neuem Ausgabelauf separate technische Release-ID;
- Release-ID muss hashgebunden aus Batch-ID + aktuellem Worker-Receipt entstehen;
- gleiche Batch-ID + anderer frischer Worker-Receipt => andere Release-ID;
- sichtbare/dauerhafte Ausgabe und Chat-Rücktransport werden an diese Release-ID gebunden;
- signierter Inhalt behält die logische Batch-ID;
- manipulierte Release-ID blockiert fail-closed;
- alte Recovery-Artikel bleiben als Produktionsquelle verboten.

## HISTORY-KANDIDAT

Branch:
`hobbyroom/m39-release-identity-history-20260918`

Head:
`1d845b0427b0eb7486d7431b689e962de45ed867`

Erwartung:
1. current main: M01–M38 PASS;
2. M39 erster neuer FAIL;
3. Kandidat enthält nur Fehlermatrix + bestehenden Regressionrunner;
4. kein Produktfix in der History-Phase;
5. danach separater Produktfix.

## BEREITS VORLIEGENDER FUNKTIONSBEFUND

Der getrennte Pre-Codex-Produktkandidat erreichte zuvor Acceptance Run `35358268913` = 40/40 PASS. Dieser Befund ersetzt nicht den vorgeschriebenen History-Beweis.

Kein echter Codex. Kein WordPress-Write. Kein Publish.


## MASCHINENMARKER

Realtest: aktueller Main gegen M39-History.
PASS: M01–M38 müssen vor M39 bestehen.
FAIL: M39 muss auf dem History-Kandidaten der erste neue Fehler sein.
Kein Publish.
