# ÜBERGABE – STARTMASTER0107 / SYSTEM4 / GLOBALE WERKSTATT

Datum: 2026-09-17

**Status dieses Dokuments:** Übergabe/Wegweiser. **Keine CURRENT_STATE, keine zweite NEXT-ACTION-Wahrheit.**

## 1. EXAKTER EINSTIEGSPUNKT

Der neue Chat beginnt zwingend hier:

`control/startmaster0107/PFERDE_ATELIER_START_HERE.json`
→ `control/startmaster0107/CURRENT_STATE.json`
→ **FRISCHECHECK gegen PR #275 / aktuellen Branch-Head**
→ ausschließlich die dortige `entry_for_continuation.next_action` ausführen.

Arbeitsbranch:
`hobbyroom/system4-chat-output-acceptance-v1`

PR:
`#275`

Wichtig: Der Branch-Head muss zu Beginn frisch gelesen werden. Dokumentations-/Statuscommits nach dem Runtime-Code ändern den Git-Head, aber nicht automatisch den geprüften Runtime-Logic-Stand.

## 2. VERBINDLICHER ZIELVERTRAG

Aktueller Zielvertrag:

`isolated_system4/ZIELVERTRAG_SYSTEM4_MACHINE_POINT0_WORKER_DISPATCH_20260916.md`

Globale verbindliche Workflow-Invariante:

`isolated_system4/GLOBAL_WORKSHOP_RULE_20260917.md`

Zielkette bleibt:

`Parent/Chat → Point-0 → Root → Supervisor → Worker-Dispatch → Research → Facts → Context → Draft → vollständige Textmaschine → Werkstatt/Repair wenn Fehler → vollständiger Recheck → Batch → Handoff → SYSTEM4_WORDPRESS_HANDOFF_V1.json`

**FEHLER → WERKSTATT. Immer.** Prüfer/Stufe/Finding-Anzahl sind egal. Die Werkstatt entscheidet erst dort reparierbar vs. objektiv nicht reparierbar. Kein lokaler Prüfer darf einen reparierbaren Fehler terminal beenden.

Textmaschine, Inhaltsqualität, PPM 6.7.9, LanguageTool 6.8, Design, Links, Facts und WordPress-Vertrag dürfen dafür nicht abgeschwächt oder verändert werden.

## 3. AKTUELLER STATUS QUO

Gesamtstatus: **BLOCKED – globale Werkstatt teilweise implementiert, aber noch nicht vollständig durch den Gesamtworkflow geführt und nicht auf dem aktuellen Runtime-Logic-Head vollständig abgenommen.**

Runtime-Logic-Head unter Prüfung:
`5391f6915ad5674264304cb7e33774bd9e338b2c`

Auf diesem Runtime-Logic-Head gibt es aktuell **keinen vollständigen Acceptance-/CI-PASS**.

Letzter vollständiger historischer Acceptance-PASS liegt auf älterem Head:
- Head `25f87b819a7d1b4a450565f0a46b1c07f6770802`
- Run `35203980166`
- Job `105145172825`
- Ergebnis SUCCESS

Dieser ältere PASS darf **nicht** als PASS der neuen Werkstatt-Implementierung verwendet werden.

## 4. REALE PRODUKTIONSLÄUFE

### Historischer 7er-System4-PASS

PR-Kommentar `5715449596`:
- 7/7 Artikel bis OUTPUT_GATE_REQUIRED;
- Batch PASS;
- WordPress-Handoff intern erzeugt;
- SHA256 `1a42251b9fe53b4679dbaf52f50afdb99929128d8ccc516c4958b9421276377e`;
- 195464 Bytes;
- kein Publish.

Nur historische Evidence.

### Jüngster frischer 7er-Lauf – aktueller Produktionsbefund

Startkommentar `5717159014`
Ergebniskommentar `5717369546`

- Parent-Start PASS für 7 Artikel;
- 7/7 Artikel bis Batch-Eingang verarbeitet;
- Batch FAIL: `BATCH_REPEATED_SENTENCE_TEMPLATE_BLOCKED:21>6`;
- Fehler ist fachlich reparierbar;
- alter Workflow beendete trotzdem terminal;
- keine WordPress-Datei;
- kein Publish.

Dieser Lauf ist der Auslöser der globalen Werkstatt-Arbeit.

## 5. WARUM DER MEHRARTIKELTEST DAS NICHT FAND

- kompletter realer Acceptance-Korridor verwendete nur 1 bzw. 3 Artikel;
- Repetition-Guard kann erst ab 4 betroffenen Artikeln auslösen;
- 7/25/1000-Regressionen verwendeten künstlich eindeutige Texte (`unique...`) und testeten Batchgröße/Transport, nicht realistisches Writer-Repetition-Verhalten.

Daher fehlte genau ein realistischer ≥4-Artikel-Reparaturfall.

## 6. BEREITS ERLEDIGT – GLOBALE WERKSTATT

Dauerhafte Regel vorhanden:
`isolated_system4/GLOBAL_WORKSHOP_RULE_20260917.md`

Runtime-Implementierung bereits vorhanden:
- `isolated_system4/global_workshop.py` neu;
- `batch_repetition_guard.py` liefert konkrete Sätze + betroffene Artikel als strukturierte Findings;
- `batch_gate.py` routet Fehler in Global Workshop und kann betroffene Artikel auf `REPAIR_REQUIRED` setzen;
- `controller.py` routet aufgefangene Controller-/Production-Fehler in Global Workshop;
- `parent_start.py` führt auch Parent-Start-Fehler zuerst durch die Workshop-Klassifizierung;
- `repair_router.py` bewahrt alle Findings, Finding-Count und Findings-Hash in der Continuation;
- `codex_entry.py`-Writer-Anweisung sagt nicht mehr „first defect“, sondern alle Findings des zuständigen Owner/Targets;
- `test_global_workshop.py` vorhanden.

## 7. TATSÄCHLICH AUSGEFÜHRTE NEUE TESTS

Gezielte lokale Werkstattprüfung aus den aktuellen Kern-Dateien:
- `test_global_workshop.py`: **3/3 PASS**;
- 21 identische lange Sätze über 4 Artikel: exakter Fehler `21>6`, **21 Findings erhalten**, repairable, gezielte Artikelroute;
- Hash-/Integritätsfehler: erreicht Workshop, wird dort korrekt **NON_REPAIRABLE** klassifiziert.

**Nicht ausgeführt / daher OFFEN:**
- kompletter System4-Positiv-/Negativ-Schutzring auf Runtime-Logic-Head `5391f691...`;
- kompletter realer LT6.8/PPM6.7.9-Korridor auf diesem Head;
- echter ≥4-Artikel-End-to-End-Reparaturfall Werkstatt → Repair → Fullcheck → Batch;
- neuer Produktionslauf nach der Werkstatt-Änderung.

## 8. ERSTER OFFENER TECHNISCHER BLOCKER

`isolated_system4/full_route_start.py`

Der komplette Route-Runner behandelt die neue `BatchGateWorkshop`-/Workshop-Continuation noch nicht als Fortsetzung. Ein reparierbarer Batchfehler kann deshalb dort weiterhin als `SYSTEM4_FULL_ROUTE_FAIL` enden.

**Das ist der exakte nächste Code-Einstieg.**

## 9. ZWEITER OFFENER TECHNISCHER BLOCKER

`isolated_system4/repair_router.py`

Alle Findings werden inzwischen erhalten, aber bei einem gemischten Finding-Satz wird `owner`/`target` noch aus dem ersten Finding gewählt. Findings verschiedener Owner/Targets dürfen nicht zusammen in eine falsche Werkstatt geschickt werden.

Erforderlich:
- nach `(owner,target)` gruppieren;
- jede Gruppe an ihren autoritativen Owner geben;
- kein Finding verlieren;
- danach vollständiger Recheck.

Keine lokale Sonderregel pro Prüfer bauen.

## 10. DRITTER OFFENER BLOCKER – GESAMTWEG / HANDOFF

Nach `full_route_start.py` und Owner-Gruppierung prüfen, dass **auch Handoff-/Top-Level-Fehler** unter die eine globale FEHLER→WERKSTATT-Invariante fallen und kein reparierbarer Fehler daneben terminal endet.

Anschließend mindestens einen echten/realistischen ≥4-Artikel-Negativfall bauen, der den bekannten Batch-Repetition-Fehler erzeugt und beweist:

`Batch Finding → Global Workshop → betroffene Artikel → Repair → kompletter Artikel-Fullcheck → Batch erneut → PASS`

Die Qualitätsgrenze `MAX_MAJORITY_REPEATED_SENTENCES=6` bleibt unverändert.

## 11. DANACH ZWINGEND – VOLLSTÄNDIGE ABNAHME

Erst nach vollständiger Implementierung:

1. komplette System4 Unit-/Negativsuite;
2. vollständiger Repair-/Owner-/Continuation-Ring;
3. realer LanguageTool-6.8-Korridor;
4. realer PPM-6.7.9-Korridor;
5. vollständige Start-to-File-Acceptance mit deterministischem Testworker – **ohne Codex**;
6. WordPress-Handoff/SHA/Bytegleichheit;
7. negative Manipulations-/Hash-/Publish-Grenzen.

Alles auf **exakt demselben resultierenden Runtime-Head**.

Kein PASS aus Codeansicht.

## 12. 107007-BINDUNG – ERST NACH WERKSTATT-ABNAHME

Aktuelle tatsächliche Launch-Datei:
`isolated_system4/bound_launches/production_107007_batch_7_20260917.json`

Tatsächlicher SHA256:
`bf629ea68555f3a14166f1b10eb9ae5910a2e9ae06881aac48f9aa6a9f4f423e`

Git-Blob:
`42708d99a094f61e10bab3dac0bdb38e4fd060af`

`STEP_107007_RUN_NEW_ARTICLE_BATCH_NO_STOP.json` deklariert noch:
`1bfefd0370251ca45ba5868e80a244182da76a865f7713e0b3bde6d5ff492d59`

Daher aktuelle Bindung: **BLOCKED_MISMATCH**.

Diese Bindung **nicht jetzt isoliert flicken**. Erst Werkstatt vollständig + Acceptance grün, danach 107007-Launchbindung und komplette Vorgänger-/Hash-Kaskade frisch und zusammenhängend nachziehen.

## 13. EXAKTE NEXT ACTION FÜR DEN NEUEN CHAT

**OHNE CODEX.**

1. Einstieg über START_HERE → CURRENT_STATE → frischen PR-Head.
2. Prüfen, dass seit Runtime-Logic-Head `5391f691...` nur Status-/Protokoll-/Übergabeänderungen oder bekannte Runtime-Änderungen erfolgt sind; bei weiterer Runtime-Änderung neuen Runtime-Logic-Head bestimmen.
3. `isolated_system4/full_route_start.py` so anbinden, dass jede Workshop-Continuation als Fortsetzung behandelt wird und nicht terminal endet.
4. `repair_router.py` gemischte Findings nach Owner/Target gruppieren lassen.
5. Handoff-/Top-Level-Abdeckung derselben globalen Werkstatt schließen.
6. Harte positive/negative Tests einschließlich ≥4-Artikel-Repetition ausführen.
7. Danach vollständige Acceptance auf exakt dem finalen Runtime-Head.
8. Erst wenn alles PASS: 107007-Bindungskaskade reparieren und erneut prüfen.
9. Erst danach und **nur nach ausdrücklicher Nutzerfreigabe** Codex für einen neuen echten Artikelproduktionslauf verwenden.

## 14. CODEX – HARTE GRENZE

**Finger weg von Codex für diese Arbeit.**

Codex ausschließlich:
- echter gebundener Artikelproduktionslauf;
- nach ausdrücklicher Nutzerfreigabe für genau diesen Produktionslauf.

Codex verboten für:
- Implementierung;
- Tests;
- Diagnose;
- Architekturarbeit;
- Preflight-Reparatur;
- Handoff-/Ausgabeexperimente.

Autorität: `isolated_system4/AGENTS.md`.

## 15. NICHT ANFASSEN

- Textmaschine / Content-Regeln;
- PPM 6.7.9;
- LanguageTool 6.8;
- Design / Theme;
- WordPress-Plugin;
- bestehende Fach-/SEO-/Link-/Fact-Regeln;
- Legacy-/Fachworkflow-Ersatzroute;
- `publish_allowed=false`;
- historische Evidence als aktuelle CURRENT_STATE verwenden.

## 16. PLUGINS

Nicht betroffen. In diesem Arbeitsblock wurde kein WordPress-Plugin entwickelt oder aktualisiert.

## 17. EINE WAHRHEIT

Dynamischer Status ausschließlich:
`control/startmaster0107/CURRENT_STATE.json`

`control/startmaster0107/PFERDE_ATELIER_START_HERE.json` ist nur die Bürotür.
`isolated_system4/README.md` wurde auf Navigation-only zurückgebaut.
Dieses Übergabedokument ist nur Wegweiser/Evidence.
