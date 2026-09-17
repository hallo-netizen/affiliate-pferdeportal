# HOBBYRAUM — SYSTEM 4A TEXTMASCHINE FINAL PASS

Stand: 17.09.2026
Branch: `hobbyroom/system4a-textmachine-final-pass-20260916`
Basis-Head: `73d791fd8d9a988c3119db4b3d822b38e54302dd`
Status: **EINGESCHLOSSENER ARBEITSAUFTRAG / STÜCK-FÜR-STÜCK / KEIN NEBENPFAD**

## Harte Arbeitsregel für jeden Nachfolger
- Nur diese Liste abarbeiten.
- Strikt in Reihenfolge.
- `[x]` nur bei realem, hartem Beleg.
- `[ ]` = offen.
- Nach jedem erledigten Punkt sofort aktualisieren.
- Kein Überspringen, kein Nebenpfad, keine neue Architektur.

## A. Textmaschine vollständig beweisen

- [x] **1. Exakte Textmaschinen-Regelmenge bestimmen.** Korrigiert maschinenfest: **152 im echten Fullcheck erreichbare Pferde-Atelier-Projektregeln** = 104 PPM + 30 Content Guard + 16 Design Guard + 2 External-Link-Regeln. LanguageTool 6.8 bleibt externer dynamischer Prüfer. `FACT_SOURCE_EVIDENCE_MISSING` wurde aus der ersten 153er-Zählung entfernt, weil dieser interne Code im echten Fullcheck nicht erreichbar ist.
  - Beleg: `isolated_system4a/TEXTMASCHINE_RULE_SCOPE_20260917.md`
- [x] **2. Für jede Textmaschinenregel Positivnachweis bestimmen.** 152/152 erreichbare Projektregeln haben einen gebundenen gültigen Positivpfad; LT 6.8 ist real mit 0 Findings PASS gelaufen.
  - Beleg: `isolated_system4a/TEXTMASCHINE_POSITIVBEWEIS_20260917.md`
  - Remote: `System 4A Real LT68 PPM679 Acceptance`, Run `35137504179`, Head `73d791fd8d9a988c3119db4b3d822b38e54302dd`, SUCCESS.
- [x] **3. Für jede Textmaschinenregel gezielten Negativnachweis prüfen.** Audit für 152/152 abgeschlossen. **65/152** besitzen bereits ausreichend exakten Negativbeleg; **87/152** sind echte Beweislücken und müssen ausschließlich in Punkt 7 ergänzt werden.
  - Beleg: `isolated_system4a/TEXTMASCHINE_NEGATIV_AUDIT_20260917.md`
- [x] **4. Für jede Textmaschinenregel Fehlerklasse festlegen.** **152/152 klassifiziert:** 102 reparierbar mit festem Owner, 50 terminal/fail-closed `HARD_BLOCK`. PPM-Verteilung korrigiert über reale Validator-`field_path`s: 83 Draft, 3 Parent-Title, 2 Portal-Link, 1 Parent-Category, 15 Hard. LanguageTool separat: echtes LT-Finding -> `DRAFT_WORKER`; LT-Hash-/Worker-/Execution-/Reportfehler -> `HARD_BLOCK`.
  - Beleg: `isolated_system4a/TEXTMASCHINE_FEHLERKLASSIFIKATION_20260917.md`
- [ ] **5. Für jede reparierbare Regel vollständigen Rückweg beweisen.** Richtiger Owner -> gleicher Artikel -> gezielte Reparatur -> vollständige Textmaschine erneut -> PASS.
  - Implementierungslücke geschlossen: reparierbare `content_guard`-/`design_guard`-Befunde laufen über `production_checks.guard_repair_finding()` an `DRAFT_WORKER -> REPAIR_REQUIRED`.
  - Neuer Regressionstest `isolated_system4/test_fullcheck_guard_repair_contract.py` lief remote zusammen mit den bestehenden Repair-Owner-Verträgen: Workflow `System 4A Repair Owner Contract`, Run `35194565815`, Head `66100241a2d90b09228ec004f7fa433502be152d`, SUCCESS.
  - Dieser Run beweist den Guard-Rückweg, gleiche Artikelidentität und Recheck-PASS sowie die bestehenden Owner-Verträge. **Noch kein `[x]`**, solange die 102 reparierbaren Regeln nicht vollständig gegen ihre Owner-Klasse und den Rückweg gebunden sind; die 87 Negativlücken aus Punkt 3 verhindern noch den vollständigen Einzelregelbeweis.
- [x] **6. Für jede nicht reparierbare Regel Hard Block beweisen.** **50/50 terminale Regeln** sind in `isolated_system4/test_textmachine_hardblock_matrix.py` einzeln an die echte Klassifikations-/Controller-Grenze gebunden und dürfen nicht in `REPAIR_REQUIRED` fallen.
  - PPM: 15/15 terminale Regel-Einträge
  - Content Guard: 28/28 terminale Regeln
  - Design Guard: 7/7 terminale Regeln
  - Remote-Beleg: Workflow `System 4A Repair Owner Contract`, Run `35194863123`, Head `e56ef98aa89a35a313014c416ef9d129eea89743`, SUCCESS.
- [ ] **7. Nur tatsächlich fehlende Nachweise ergänzen.** Aktuell exakt **87 Negativbeweis-Lücken** aus Punkt 3. Keine neuen Qualitätsregeln, keine zweite Textmaschine, keine abgeschwächten Prüfer.
- [ ] **8. `TEXTMASCHINE_REGELN_FULL_PASS` beweisen.** Erst wenn 1–7 vollständig und maschinenfest abgeschlossen sind.

## B. System-4A-Gesamtstrecke auf demselben finalen Head erneut beweisen
- [ ] **9. 1 Artikel komplett.** Chat-Anstoß -> Point 0 -> Root/Supervisor -> Worker -> Research -> Facts -> Draft -> vollständige Textmaschine -> ggf. Repair -> PASS -> Batch -> Handoff.
- [ ] **10. 3 Artikel mit absichtlich reparierbarem Fehler.** Genau ein Artikel zurück, gleiche Identität, Repair, vollständige Nachprüfung, PASS; andere Artikel unverändert.
- [ ] **11. Technischer/Integritäts-/Manipulationsfehler.** Muss terminal BLOCK bleiben.
- [ ] **12. 1..N / Batch / Identität / Reihenfolge / Hash-/Byte-Bindung.** PASS.
- [ ] **13. Handoff/Parent-Chat.** Exakt dieselben Bytes/SHA zurück; keine Fake-PASS-Ausgabe.

## C. Kanonischer Abschluss
- [ ] **14. Finalen getesteten 4A-Stand kanonisch binden.**
- [ ] **15. 107008/Abschlusskette über autorisierten Entrance-/Prebinding-Weg binden.** Keine manuelle State-/Hash-Manipulation.
- [ ] **16. Reale Abschlussstrecke ausführen.** 107008 -> PSERC -> ENDSTEMPEL -> WordPress-Importformatprüfung.
- [ ] **17. Finale Importdatei byte-/SHA-identisch in den anfordernden Parent-Chat zurückgeben.**
- [ ] **18. CURRENT_STATE / Eine Wahrheit auf real bewiesenen Gesamt-PASS setzen.** Erst nach 1–17.

## Bereits bewiesene Voraussetzungen — NICHT Teil der offenen 1–18
- [x] System-4A-Produktionsstraße festgelegt.
- [x] Codex-Rollentrennung festgelegt.
- [x] Repair-Owner-Mechanik grundsätzlich real getestet: Run `35105842615`, Head `531a40bedf6f4bd9c709d1ad36d4c46db966c166`, SUCCESS.
- [x] Frühere 1-Artikel-Gesamtstrecke PASS (ersetzt Punkt 9 auf finalem Head nicht).
- [x] Frühere 3-Artikel-Strecke mit Repair-Isolation PASS (ersetzt Punkt 10 nicht).
- [x] Früherer 1..N-Handoff PASS (ersetzt Punkt 12 nicht).

## Aktueller Einstiegspunkt
**NEXT ACTION = Punkt 5 abschließen, technisch gebunden an Punkt 7.**

Die 102 reparierbaren Regeln sind klassifiziert und die Owner-Routen laufen remote. Jetzt ausschließlich die 87 echten Negativlücken aus Punkt 3 in Punkt 7 ergänzen; dadurch wird zugleich der noch fehlende Einzelregel-Rückweg für Punkt 5 geschlossen. Danach Punkt 5 und 7 abhaken und Punkt 8 ausführen.
