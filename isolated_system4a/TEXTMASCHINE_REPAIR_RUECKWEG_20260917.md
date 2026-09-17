# SYSTEM 4A — PUNKT 5 REPAIR-RÜCKWEG

Stand: 17.09.2026
Branch: `hobbyroom/system4a-textmachine-final-pass-20260916`

## Ergebnis

**PUNKT 5 = PASS.**

Die in Punkt 4 bereits vollständig klassifizierten **102 reparierbaren Textmaschinenregeln** laufen über genau vier Owner-Routen:

- 96 -> `DRAFT_WORKER`
- 3 -> `PARENT_TITLE_MACHINE`
- 2 -> `PORTAL_LINK_MACHINE`
- 1 -> `PARENT_CATEGORY_MACHINE`
- Kontrollsumme: **102**

Die Regelabhängigkeit endet nach der hart bewiesenen Regel->Owner-Zuordnung aus Punkt 4. Der Rückweg selbst ist owner-gesteuert und für alle Regeln desselben Owners identisch. Deshalb wird der Rückweg nicht 102-mal künstlich dupliziert, sondern jede der vier tatsächlich verwendeten Owner-Routen hart geprüft.

## Bewiesene Rückweggrenze

Test: `isolated_system4/test_textmachine_repair_roundtrip_matrix.py`

Der Test beweist:

1. Kontrollsumme exakt 102 reparierbare Regeln.
2. `DRAFT_WORKER` -> derselbe Artikel bleibt gebunden -> `REPAIR_REQUIRED`.
3. `PARENT_TITLE_MACHINE` -> kontrollierter `PARENT_LAUNCH`, ohne stille Artikelmutation.
4. `PORTAL_LINK_MACHINE` -> kontrollierter `PARENT_LAUNCH`, ohne stille Artikelmutation.
5. `PARENT_CATEGORY_MACHINE` -> kontrollierter `PARENT_LAUNCH`, ohne stille Artikelmutation.
6. Nach erfolgter Reparatur muss der Artikel erneut durch den vollständigen Fullcheck-Pfad: Authoring Contract -> Content Guard -> Design Guard -> Production Checks; erst danach `OUTPUT_GATE_REQUIRED`.

Die bereits vorhandenen realen Repair-Nachweise bleiben Bestandteil der Kette, insbesondere Same-Article-Repair, Parent-Title-Repair, Parent-Metadata-Authority und Guard-Repair.

## Remote-Ausführung

Workflow: `System 4A Repair Owner Contract`
Run: `35197259525`
Head: `475c57232b400a9f28523142863290866220a428`
Ergebnis: **SUCCESS**

Der Run enthält zusätzlich weiterhin die komplette Negativ-/Hard-Block-Matrix einschließlich der 49 PPM-Gap-Nachweise.

## Harte Aussage

Für jede der **102 reparierbaren Regeln** ist über ihre bereits bewiesene Regel->Owner-Klassifikation und die vollständig bewiesene Owner-Rückwegmatrix gesichert:

`Fehler -> richtiger Owner -> keine stille Artikelersetzung -> kontrollierter Repair-Rückweg -> erneuter vollständiger Fullcheck -> erst bei PASS weiter`.

Terminale Regeln sind ausdrücklich nicht Bestandteil von Punkt 5; sie sind in Punkt 6 mit 49/49 fail-closed bewiesen.
