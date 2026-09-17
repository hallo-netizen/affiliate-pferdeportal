# STARTMASTER0107 – realer 107007 Produktionslauf – Protokoll

Datum: 2026-09-17
Branch: `hobbyroom/system4-chat-output-acceptance-v1`

Dieses Dokument ist **Protokoll/Evidence**, keine CURRENT_STATE und keine eigene NEXT-ACTION-Wahrheit. Operativer Stand ausschließlich über:
`control/startmaster0107/PFERDE_ATELIER_START_HERE.json` → `control/startmaster0107/CURRENT_STATE.json`.

## Gebundener 7er-Launch

`isolated_system4/bound_launches/production_107007_batch_7_20260917.json`

Tatsächlicher aktueller Datei-SHA256:
`bf629ea68555f3a14166f1b10eb9ae5910a2e9ae06881aac48f9aa6a9f4f423e`

Aktueller Git-Blob:
`42708d99a094f61e10bab3dac0bdb38e4fd060af`

`publish_allowed=false`.

## Historischer realer 7er-Lauf mit internem System4-PASS

PR-Kommentar `5715449596`:
- Parent-Start PASS, 7 Artikel;
- alle 7 Artikel erreichten `OUTPUT_GATE_REQUIRED`;
- Batch PASS;
- `SYSTEM4_WORDPRESS_HANDOFF_V1.json` intern erzeugt und bytegleich rekonstruiert;
- SHA256 `1a42251b9fe53b4679dbaf52f50afdb99929128d8ccc516c4958b9421276377e`;
- 195464 Bytes;
- kein Publish.

Dieser Lauf ist **historische Evidence**, nicht der aktuelle operative Produktionsstand, weil ein späterer frischer 7er-Lauf eine weitere Workflow-Lücke offengelegt hat.

## Jüngster frischer realer 7er-Lauf

Startkommentar: `5717159014`
Ergebniskommentar: `5717369546`

Ergebnis:
- `SYSTEM4_PARENT_START_PASS:POINT0_ROOT_DISPATCH_READY:ARTICLE_COUNT=7`;
- alle 7 Artikel wurden bis zum Batch-Eingang verarbeitet;
- Batch stoppte mit `SYSTEM4_BATCH_FAIL:BATCH_REPEATED_SENTENCE_TEMPLATE_BLOCKED:21>6`;
- kein WordPress-Handoff erzeugt;
- kein Repository-Output erzeugt;
- kein Publish.

## Warum der Lauf terminal stoppte

Der Batch-Wiederholungsprüfer erkannte einen **reparierbaren** Qualitätsbefund erst nach den Einzelartikel-Prüfungen. Die damalige Batch-Strecke konnte nur PASS oder STOP und hatte keine globale Rückgabe zur Reparatur. Zusätzlich gab der Prüfer beim Fehler nur die Summenzahl aus und nicht die konkreten Sätze/Artikel an die Reparaturroute weiter.

Die zuvor verwendeten Mehrartikeltests deckten diesen Fall nicht ab:
- der echte vollständige Testkorridor verwendete nur 1 bzw. 3 Artikel;
- der Repetition-Guard kann erst ab mindestens 4 betroffenen Artikeln auslösen;
- 7/25/1000-Regressionsfixtures verwendeten künstlich eindeutige Texte und testeten damit die Batchgröße, nicht realistisches Writer-Repetition-Verhalten.

## Dauerhafte Entscheidung – globale Werkstatt

Verbindliche Invariante:
`isolated_system4/GLOBAL_WORKSHOP_RULE_20260917.md`

**FEHLER → WERKSTATT.**

Kein Prüfer und keine Stufe darf einen Fehler eigenständig als terminalen Prozessabschluss behandeln. Jeder Fehler gelangt zuerst in die zentrale Werkstatt. Dort wird ausschließlich entschieden:
- reparierbar → autoritativer Owner/Target → Reparatur → vollständiger erforderlicher Recheck → normal weiter;
- objektiv nicht reparierbar → dokumentiert fail-closed blockieren.

Diese Entscheidung schwächt keine Inhalts-, Qualitäts-, LanguageTool-, PPM-, Link-, Fact-, Design-, Batch- oder WordPress-Regel.

## Stand der Implementierung

Bereits umgesetzt:
- `isolated_system4/global_workshop.py`;
- strukturierte konkrete Repetition-Findings in `batch_repetition_guard.py`;
- Workshop-Capture in `batch_gate.py`, `controller.py`, `parent_start.py`;
- targeted `REPAIR_REQUIRED` für betroffene Batch-Artikel;
- Repair-Continuation bewahrt alle Findings inklusive Hash/Count;
- Writer-Anweisung verlangt alle Findings und verbietet Reduktion auf `findings[0]`;
- `isolated_system4/test_global_workshop.py` vorhanden.

Noch nicht abgeschlossen:
- `full_route_start.py` führt globale Workshop-Continuation noch nicht zentral weiter; repairable Batch-Workshop kann dort noch terminal werden;
- gemischte Findings verschiedener Owner/Targets werden im Repair-Router noch nicht sauber getrennt, obwohl alle Findings erhalten bleiben;
- Handoff-/Top-Level-Abdeckung der globalen Regel ist noch nicht als Gesamtweg bewiesen;
- vollständiger Positiv-/Negativ-/Real-LT/PPM-Acceptance-Lauf fehlt auf dem aktuellen Runtime-Logic-Head `5391f6915ad5674264304cb7e33774bd9e338b2c`.

## Tatsächlich ausgeführte neue Prüfungen

Isoliert lokal aus den exakt aktuellen Werkstatt-Kern-Dateien ausgeführt:
- `test_global_workshop.py`: 3/3 PASS;
- synthetischer 21-Satz-Wiederholungsfall: exakter Fehler `21>6`, 21 Findings erhalten, reparierbar, gezielte Artikelroute;
- Hash-/Integritätsfall: Workshop wird betreten und korrekt als non-repairable klassifiziert.

Nicht ausgeführt / nicht als PASS zu werten:
- vollständiger Repository-/System4-Acceptance-Korridor auf Runtime-Logic-Head `5391f691...`;
- vollständiger realer LT6.8/PPM6.7.9-Korridor auf diesem Head;
- neuer Artikelproduktionslauf nach der Werkstatt-Teilimplementierung.

## Zusätzlich festgestellte 107007-Bindungsabweichung

Die tatsächliche Launch-Datei hat SHA256:
`bf629ea68555f3a14166f1b10eb9ae5910a2e9ae06881aac48f9aa6a9f4f423e`

`STEP_107007_RUN_NEW_ARTICLE_BATCH_NO_STOP.json` deklariert aktuell noch:
`1bfefd0370251ca45ba5868e80a244182da76a865f7713e0b3bde6d5ff492d59`

Damit bleibt 107007 bis zur sauberen Nachbindung BLOCKED. Diese Nachbindung darf erst nach abgeschlossener und grün abgenommener Werkstatt-Implementierung erfolgen; danach ist die gesamte Hash-/Vorgängerbindung frisch zu prüfen.

## Codex-Regel

Codex ist ausschließlich für **echte gebundene Artikelproduktion nach ausdrücklicher Nutzerfreigabe** zulässig. Nicht für Implementierung, Tests, Diagnose, Architektur, Preflight-Reparatur oder Handoff-Experimente.

## Aktueller Fortsetzungspunkt

Nicht aus diesem Protokoll ableiten. Verbindlich:
`control/startmaster0107/PFERDE_ATELIER_START_HERE.json` → `control/startmaster0107/CURRENT_STATE.json` → FRISCHECHECK → dortige NEXT ACTION.
