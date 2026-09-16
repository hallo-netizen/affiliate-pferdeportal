# HOBBYRAUM — SYSTEM 4A TEXTMASCHINE FINAL PASS

Stand: 16.09.2026
Branch: `hobbyroom/system4a-textmachine-final-pass-20260916`
Basis-Head: `73d791fd8d9a988c3119db4b3d822b38e54302dd`
Status: **EINGESCHLOSSENER ARBEITSAUFTRAG / STÜCK-FÜR-STÜCK / KEIN NEBENPFAD**

## Zweck

Dieser Hobbyraum enthält ausschließlich die noch fehlenden Arbeiten bis zum vollständigen System-4A-PASS. Keine neue Architektur, kein paralleler Lösungsweg, kein Umbau außerhalb des bestehenden System-4A-Pfads.

## Harte Arbeitsregel

Die Punkte werden strikt in Reihenfolge abgearbeitet. Ein Punkt gilt erst als erledigt, wenn er real belegt ist. Danach wird genau dieser Status in dieser Datei fortgeschrieben. Kein Überspringen.

## A. Textmaschine vollständig beweisen

1. Exakte Menge der Regeln bestimmen, die tatsächlich zur Textmaschine gehören. Nicht pauschal alle 557 PPM-Regeln übernehmen.
2. Für jede Textmaschinenregel den echten Prüfer und den realen Positivnachweis bestimmen.
3. Für jede Textmaschinenregel einen gezielten Negativnachweis bestimmen: genau diese Regel verletzen, erwarteten Prüfer/Fehlercode erhalten.
4. Für jede Textmaschinenregel die Fehlerklasse festlegen: `REPAIR_REQUIRED` oder terminaler `HARD BLOCK`.
5. Für jede reparierbare Regel beweisen: richtiger Owner -> gleicher Artikel -> gezielte Reparatur -> vollständige Textmaschine erneut -> PASS.
6. Für jede nicht reparierbare Regel beweisen: kein falscher Repair-Pfad; terminal/fail-closed BLOCK.
7. Nur tatsächlich fehlende Nachweise ergänzen. Keine neuen Qualitätsregeln, keine zweite Textmaschine, keine abgeschwächten Prüfer.
8. Erst bei vollständiger maschinenfester Zuordnung darf `TEXTMASCHINE_REGELN_FULL_PASS` gemeldet werden.

## B. System-4A-Gesamtstrecke auf demselben finalen Head erneut beweisen

9. 1 Artikel komplett: Chat-Anstoß -> Point 0 -> Root/Supervisor -> Worker -> Research -> Facts -> Draft -> vollständige Textmaschine -> ggf. Repair -> PASS -> Batch -> Handoff.
10. 3 Artikel komplett mit absichtlich reparierbarem Fehler: genau ein Artikel zurück, gleiche Identität, Repair, vollständige Nachprüfung, PASS; andere Artikel unverändert.
11. Technischer/Integritäts-/Manipulationsfehler: terminal BLOCK.
12. 1..N / Batch / Identität / Reihenfolge / Hash-/Byte-Bindung: PASS.
13. Handoff/Parent-Chat: exakt dieselben Bytes/SHA zurück; keine Fake-PASS-Ausgabe.

## C. Kanonischer Abschluss

14. Den tatsächlich getesteten finalen 4A-Stand kanonisch binden.
15. 107008/Abschlusskette ausschließlich über den autorisierten Entrance-/Prebinding-Weg an diesen Stand binden.
16. Reale Abschlussstrecke ausführen: 107008 -> PSERC -> ENDSTEMPEL -> WordPress-Importformatprüfung.
17. Exakt dieselbe finale Importdatei byte-/SHA-identisch in den anfordernden Parent-Chat zurückgeben.
18. Erst nach realem Gesamt-PASS CURRENT_STATE / Eine Wahrheit auf den bewiesenen Endstand setzen.

## Bereits hart belegt vor Start dieses Hobbyraums

- System-4A-Produktionsstraße und Codex-Rollentrennung sind festgelegt: Codex ist fachlicher Worker für Research/Facts/Text und gezielte Same-Article-Reparatur; Workflow, Textmaschine, Design, PASS und Route liegen außerhalb.
- Repair-Owner-Mechanik ist real getestet; reparierbare Befunde laufen zurück, technische/Integritäts-/Sicherheitsfehler bleiben fail-closed.
- Komplette 1-Artikel- und 3-Artikel-Strecken sowie 1..N-Handoff wurden bereits auf vorqualifizierten Heads erfolgreich ausgeführt.
- Nicht hart belegt ist bisher die vollständige Regel-für-Regel-Abdeckung aller tatsächlich zur Textmaschine gehörenden Regeln.

## NEXT ACTION

**Punkt 1:** Exakte Textmaschinen-Regelmenge aus den real gebundenen Prüfern/PPM-6.7.9-Registern und System-4A-Guards bestimmen. Ergebnis muss maschinenfest und nachvollziehbar sein. Erst danach Punkt 2.
