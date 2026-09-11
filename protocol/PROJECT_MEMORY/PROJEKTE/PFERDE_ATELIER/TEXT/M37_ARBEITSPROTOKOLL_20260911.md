# TEXT – M37 ARBEITSPROTOKOLL – 11.09.2026

ROLLE: PROTOKOLL / kein CURRENT_STATE / keine zweite Fehlerwahrheit.

## AUSGANGSSTAND

Recovery-/letzter belastbarer Live-Baseline-Stand:
`bb005a5324a0a6270aacb52b5927613bde1ab4bc`

Letzter echter frischer Realtest vor M37:
- Recherche: ausgeführt;
- erster Artikel: erzeugt;
- echter PPM-6.7.9-/PSERC-Handoff: erreicht;
- äußerer sichtbarer Stop: `PPM679_REAL_EXECUTION_BLOCKED`;
- konkreter innerer Grund: durch äußeren Handoff nicht erhalten;
- ursprünglicher Codex-Task später nicht mehr verfügbar;
- 107008: nicht erreicht;
- Kein Publish.

Produktions-Rootcause bleibt bis zu einem neuen echten Lauf UNKNOWN.

## WARUM M37 ZWEIPHASIG LÄUFT

Der vorhandene `hardlock-base` unterscheidet ausdrücklich:
- `HISTORY_AUTHORITY_MAINTENANCE`: Matrix/Runner als Fehlerhistorie ändern;
- `PRODUCT_FIX`: Produktcode ändern.

Eine Mischung beider Klassen in einem Kandidaten ist fail-closed verboten.
PR247 enthielt zunächst beides. Deshalb wurde nicht am Hardlock vorbeigearbeitet, sondern der vorhandene Vertrag eingehalten.

## PHASE 1 – HISTORY AUTHORITY – PASS / INTEGRIERT

History-Kandidat:
`hobbyroom/m37-history-authority-20260911`

Head:
`245b596f9d6dd67c759527a0f211dbe957f4e34f`

Maschinenbeweis:
- erlaubter Diff exakt Matrix + bestehender Runner;
- `HOBBYROOM_WORK_LOCK_PR_PASS`;
- `HOBBYROOM_HISTORY_REPRODUCTION_PASS:M37`;
- `HOBBYROOM_HISTORY_MACHINE_PROOF_PASS:M37`;
- hardlock PASS;
- hardlock-base PASS.

Integration:
- PR248 gemergt;
- neuer Main `f791dcc6c926f9c136faed29957e64786ffca08e`.

Damit ist M37 Bestandteil der bestehenden History-Autorität. Kein Produktfix wurde in Phase 1 integriert.

## PHASE 2 – PRODUCT FIX – AKTIV

Current main:
`f791dcc6c926f9c136faed29957e64786ffca08e`

Produktkandidat:
- PR247;
- Branch `hobbyroom/ppm-inner-reason-visibility-20260911`;
- Head `59ad44da3d89769c05f0725f9929135b0262f4dd`;
- Parent exakt current main;
- Diff exakt Handoff + bestehende STEP→CURRENT_STATE→START_HERE-Hashkette;
- Matrix und Runner unverändert aus Main.

Fix:
- bestehender Handoff bleibt fail-closed BLOCKED;
- bereits vorhandener erster innerer nicht-reparierbarer PPM/PSERC-Grund wird sichtbar erhalten;
- ohne vorhandenen konkreteren Grund wird nichts erfunden;
- reparierbare Content-Codes bleiben RepairRequired;
- keine Fach-/PPM-/PSERC-/PSTE-/Textmaschinen-/SEO-/Link-/Tabellen-/Design-/Publish-Regeländerung.

Pflichtbeweis:
- BEFORE: current main muss mit bestehendem M01–M37-Runner exakt M37 als ersten FAIL reproduzieren;
- AFTER: Produktkandidat muss mit demselben Runner vollständig `GESAMT PASS` liefern;
- `HOBBYROOM_HISTORY_MACHINE_PROOF_PASS:M37`;
- hardlock PASS;
- hardlock-base PASS;
- kein Bypass.

## DANACH

Erst nach Phase-2-PASS und Integration genau ein frischer erster Artikel als Realtest bis zum echten PPM/PSERC-Handoff.
Bei PASS weiter nach gebundenem Workflow; bei FAIL nur den ersten konkret sichtbaren inneren Grund übernehmen.
Keine Reparatur im laufenden Test.
Kein WordPress-Write.
Kein Publish.

## STATUSWÖRTER FÜR MASCHINENBEWEIS

Realtest
PASS
FAIL
Kein Publish

Aktiver äußerer Blocker: `PPM679_REAL_EXECUTION_BLOCKED`
Main: `f791dcc6c926f9c136faed29957e64786ffca08e`
Recovery: `bb005a5324a0a6270aacb52b5927613bde1ab4bc`
