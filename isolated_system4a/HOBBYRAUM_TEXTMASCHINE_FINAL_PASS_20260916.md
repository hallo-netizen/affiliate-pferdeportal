# HOBBYRAUM — SYSTEM 4A TEXTMASCHINE FINAL PASS

Stand: 16.09.2026
Branch: `hobbyroom/system4a-textmachine-final-pass-20260916`
Basis-Head: `73d791fd8d9a988c3119db4b3d822b38e54302dd`
Status: **EINGESCHLOSSENER ARBEITSAUFTRAG / STÜCK-FÜR-STÜCK / KEIN NEBENPFAD**

## Harte Arbeitsregel für jeden Nachfolger

- Nur diese Liste abarbeiten.
- Strikt in Reihenfolge.
- `[x]` nur bei realem, hartem Beleg.
- `[ ]` bedeutet offen und ist die nächste Arbeit, sofern kein früherer offener Punkt existiert.
- Nach jedem erledigten Punkt diese Datei sofort aktualisieren und den Beleg direkt am Punkt ergänzen.
- Kein Überspringen, kein neuer Nebenpfad, keine neue Architektur.

## A. Textmaschine vollständig beweisen

- [ ] **1. Exakte Textmaschinen-Regelmenge bestimmen.** Nicht pauschal alle 557 PPM-Regeln übernehmen. Maschinenfest trennen: Textmaschine vs. Workflow/Persistenz/Release/sonstige technische Regeln.
- [ ] **2. Für jede Textmaschinenregel Positivnachweis bestimmen.** Echter Prüfer, reale Ausführung, erwartetes PASS.
- [ ] **3. Für jede Textmaschinenregel gezielten Negativnachweis bestimmen.** Genau diese Regel verletzen; erwarteter Prüfer und Fehlercode müssen erscheinen.
- [ ] **4. Für jede Textmaschinenregel Fehlerklasse festlegen.** `REPAIR_REQUIRED` oder terminaler `HARD BLOCK`.
- [ ] **5. Für jede reparierbare Regel vollständigen Rückweg beweisen.** Richtiger Owner -> gleicher Artikel -> gezielte Reparatur -> vollständige Textmaschine erneut -> PASS.
- [ ] **6. Für jede nicht reparierbare Regel Hard Block beweisen.** Kein falscher Repair-Pfad; terminal/fail-closed.
- [ ] **7. Nur tatsächlich fehlende Nachweise ergänzen.** Keine neuen Qualitätsregeln, keine zweite Textmaschine, keine abgeschwächten Prüfer.
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

- [x] **System-4A-Produktionsstraße festgelegt.** Eine Route: Machine/Point-0 -> Root -> Supervisor -> Worker -> Research/Facts -> Draft -> fullcheck -> Same-Article-Repair -> Batch -> Handoff.
  - Beleg: `isolated_system4/AGENTS.md` auf vorqualifiziertem System-4A-Stand.
- [x] **Codex-Rollentrennung festgelegt.** Codex macht Facharbeit: Research/Facts/Text und angeforderte Same-Article-Reparatur; Workflow, Textmaschine, Design, PASS und Route liegen außerhalb.
  - Beleg: `isolated_system4/AGENTS.md`.
- [x] **Repair-Owner-Mechanik grundsätzlich real getestet.** Reparierbare Befunde können zurücklaufen; technische/Integritäts-/Sicherheitsfehler bleiben fail-closed.
  - Beleg: Workflow `System 4A Repair Owner Contract`, Run `35105842615`, Head `531a40bedf6f4bd9c709d1ad36d4c46db966c166`, SUCCESS.
- [x] **Frühere 1-Artikel-Gesamtstrecke PASS auf vorqualifiziertem Head.** Dieser Beleg ersetzt Punkt 9 nicht, weil Punkt 9 nach Abschluss der Textmaschinen-Regelarbeit auf demselben finalen Head erneut laufen muss.
- [x] **Frühere 3-Artikel-Strecke mit Repair-Isolation PASS auf vorqualifiziertem Head.** Dieser Beleg ersetzt Punkt 10 nicht.
- [x] **Früherer 1..N-Handoff PASS auf vorqualifiziertem Head.** Dieser Beleg ersetzt Punkt 12 nicht.

## Aktueller Einstiegspunkt

**NEXT ACTION = Punkt 1.**

Exakte Menge der tatsächlich zur Textmaschine gehörenden Regeln aus den real gebundenen Prüfern, PPM-6.7.9-Registern und System-4A-Guards bestimmen. Ergebnis muss maschinenfest und nachvollziehbar sein. Erst danach Punkt 2.
