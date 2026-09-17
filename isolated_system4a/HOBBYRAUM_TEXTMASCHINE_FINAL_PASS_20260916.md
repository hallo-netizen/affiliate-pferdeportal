# HOBBYRAUM — SYSTEM 4A TEXTMASCHINE FINAL PASS

Stand: 17.09.2026
Aktiver Arbeitsbranch: `hobbyroom/system4a-real-102-repair-matrix-clean-20260917`
Letzter geprüfter Arbeits-Head vor dieser Statuskorrektur: `2eba56cda276c67721577f0104ad89b65a2af890`
Status: **AKTIV / PUNKT 5 WIEDER OFFEN / KEIN GESAMT-PASS**

## Harte Arbeitsregel für jeden Nachfolger
- Nur diese Liste bzw. die hier benannte NEXT ACTION abarbeiten.
- `[x]` nur bei realem hartem Beleg.
- Kein PASS aus Testnamen, Mocks, Dokumentation oder Erinnerung ableiten.
- Keine Produktions-`CURRENT_STATE` manuell schreiben; deren Autorität bleibt `ENTRANCE_GATE_ONLY`.
- Kein Nebenpfad, keine neue Architektur.

## A. Textmaschine

- [x] **1. Regelmenge:** 151 erreichbare Projektregeln = 104 PPM + 30 Content Guard + 15 Design Guard + 2 External Links; LT 6.8 externer dynamischer Prüfer.
- [x] **2. Positivpfade:** 151/151 gebunden.
- [x] **3. Negativpfade:** 151/151 gebunden.
- [x] **4. Klassifikation:** 102 reparierbar / 49 terminal HARD_BLOCK.
- [ ] **5. Echter 102/102-Reparatur-Rundlauf.**
  - Früherer Run `35197259525` beweist Owner-Routing/Rückweg, **nicht** 102 reale Einzelreparaturen. Diese frühere PASS-Aussage ist für den neuen HARD RULE nicht ausreichend.
  - Neuer echter Harness: `isolated_system4/real_102_repair_matrix_v1.py` + `isolated_system4/real_102_repair_matrix_runner_v4.py`.
  - Workflow: `.github/workflows/system4a-real-102-repair-matrix.yml`.
  - Kein Mock erlaubt; Zielmarker erst bei echtem Erfolg: `TEXTMASCHINE_REAL_REPAIR_FULL_PASS:102/102`.
  - Bereits gefunden/korrigiert im Testweg: 3 W4-Heading-Regeln waren fälschlich HARD_BLOCK statt `DRAFT_WORKER`; aktuelle W4-Routing-Regression ist im Workflow gebunden.
  - Aktuelle Canonical-Mutationsserie auf heutiger grüner System-4A-Basis: 15/15 gezielte PPM-Mutationen erreichen ihren exakten Fehlercode.
  - Letzter echter Lauf: `35214897183`, Head `2eba56cda276c67721577f0104ad89b65a2af890`, **FAIL**.
  - Erster offener Fehler: Registry bindet **22 Content-Regeln** an `tests/test-historical-regressions.php`, aber diese Datei enthält nur 16 alte Infrastruktur-Incidents und startet später selbst an `Baseline gate must be green before state mutation`; die 22 erwarteten Content-Codes werden dort nicht emittiert.
  - Der Inspektionsschritt in Run `35214897183` hat zusätzlich gezeigt: Von diesen 22 Codes ist im vorhandenen PHP-Testbestand nur `BLOCKED_CONTENT_REQUIRED_BLOCK_MISSING` direkt in den drei `three-type-bundled-local/*-negative.php` Dateien vorhanden. Für die übrigen 21 wurde dort kein direkt gebundener Testtreffer gefunden.
  - **NEXT ACTION:** die 22 Registry-Bindungen fachlich korrekt auf echte gezielte Mutationen umstellen bzw. `tests/test-historical-regressions.php` als echten aktuellen Aggregator ergänzen; danach denselben 102er-Workflow wiederholen. Kein künstliches Echo der Fehlercodes.
- [x] **6. 49/49 terminal HARD_BLOCK** separat bewiesen.
- [x] **7. bisherige fehlende Nachweise geschlossen.**
- [ ] **8. `TEXTMASCHINE_REGELN_FULL_PASS` unter dem verschärften 102/102-HARD-RULE.** Der alte Marker bleibt historischer Beleg des damaligen Testumfangs; Gesamt-PASS erst nach Punkt 5 neu zulässig.

## B. Bereits real bewiesene Gesamtstrecken

- [x] **9. 1 Artikel komplett:** Point 0 -> Root/Supervisor -> Worker -> Research -> Facts -> Draft -> Textmaschine -> Batch -> Handoff.
- [x] **10. 3 Artikel, genau ein Repair:** real PASS.
- [x] **11. Integritäts-/Manipulationsfehler terminal:** Run `35198908215`, Head `6b6f3ea789c795e3e8cc4ea3b13ff38400bd473d`, SUCCESS.
- [x] **12. 1..N / Identität / Reihenfolge / Hash-/Byte-Bindung:** kanonischer Binding-Beleg referenziert Runs `35199941338` und `35199941460`, beide SUCCESS.
- [x] **13. Handoff/Parent-Chat Byte-/SHA-Bindung:** im kanonischen Binding als PASS gebunden. Der frühere im Chat genannte konkrete Datei-SHA ist ohne erneute Artefaktberechnung nicht als harter Fakt zu verwenden.

## C. Kanonischer Abschluss

- [x] **14. Getesteten System-4A-Kandidaten kanonisch gebunden:** `control/startmaster0107/SYSTEM4A_CANONICAL_BINDING_V1.json`; State-Write ausdrücklich nicht durchgeführt.
- [x] **15. 107008 prebound:** `control/startmaster0107/SYSTEM4A_107008_PREBINDING_V1.json`; Aktivierung nur nach autorisiertem 107007-Abschluss durch `cloud_entry.complete`; `state_advance_performed=false`.
- [ ] **16. Reale Abschlussstrecke:** 107007 real abschließen -> 107008 -> PSERC -> ENDSTEMPEL -> WordPress-Importformatprüfung. Auf `main` sind 1..N-Post-107008-Komponenten integriert, aber das ist **kein realer Abschlusslauf**.
- [ ] **17. Finale Importdatei byte-/SHA-identisch in Parent-Chat zurückgeben.**
- [ ] **18. Produktions-`CURRENT_STATE` / Eine Wahrheit erst nach realem Gesamt-PASS über autorisierte Entrance-State-Schreibung aktualisieren.**

## Produktionswahrheit / Abgrenzung

Campus-Pflichtweg auf `main` bleibt:
`control/CURRENT_STARTMASTER.json` -> `control/startmaster0107/PFERDE_ATELIER_START_HERE.json` -> `control/startmaster0107/CURRENT_STATE.json`.

Die dortige `CURRENT_STATE.json` steht weiterhin auf Sequenz 107007 und wird ausschließlich von Entrance geschrieben. Sie ist **nicht** durch diesen Hobbyraumtest manuell zu verändern. Der Hobbyraum liefert nur den noch offenen Vorabbeweis für Punkt 5 und danach den PASS-Audit.

## EXAKTER EINSTIEGSPUNKT FÜR DEN NÄCHSTEN CHAT

1. `control/CURRENT_STARTMASTER.json`
2. `control/startmaster0107/PFERDE_ATELIER_START_HERE.json`
3. `control/startmaster0107/CURRENT_STATE.json` **nur lesen / FRISCHECHECK**
4. Danach für die aktuelle isolierte Arbeit exakt hier weiter:
   `isolated_system4a/HOBBYRAUM_TEXTMASCHINE_FINAL_PASS_20260916.md`
5. Arbeitsbranch frisch prüfen: `hobbyroom/system4a-real-102-repair-matrix-clean-20260917`
6. Neueste Workflow-Ausführung `System 4A Real 102 Repair Matrix` frisch prüfen.
7. **NEXT ACTION:** Punkt 5 fortsetzen: die 22 falsch/veraltet an `tests/test-historical-regressions.php` gebundenen Content-Regeln mit echten aktuellen Einzelmutationen belegen; danach 102er-Lauf bis `TEXTMASCHINE_REAL_REPAIR_FULL_PASS:102/102`.
8. **ERST DANACH:** HARD RULE `Was behauptet jeder PASS – und was testet der Code wirklich?` vollständig über alle bisherigen PASS-Belege ausführen.

## NICHT ANFASSEN

- `control/startmaster0107/CURRENT_STATE.json` nicht manuell schreiben.
- Keine 107008-Aktivierung ohne echten 107007-Receipt/Entrance.
- Kein ENDSTEMPEL-/Publish-Bypass.
- Keine Regel als PASS markieren, nur weil Registry/Testname sie behauptet.
- `publish_allowed=false` bleibt unverändert.
