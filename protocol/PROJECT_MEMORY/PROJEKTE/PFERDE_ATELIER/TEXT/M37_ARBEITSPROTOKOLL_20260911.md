# TEXT – M37 ARBEITSPROTOKOLL – 11.09.2026

ROLLE: PROTOKOLL / kein CURRENT_STATE / keine zweite Fehlerwahrheit.

## AUSGANGSSTAND

Current main:
`a2f2f1b4b7af1e905c6a0cb69c5389664b7c4ad6`

Recovery-/letzter belastbarer Live-Baseline-Stand:
`bb005a5324a0a6270aacb52b5927613bde1ab4bc`

Letzter echter frischer Realtest:
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
PR247 enthielt zunächst beides. Deshalb wird nicht am Hardlock vorbeigearbeitet, sondern der vorhandene Vertrag eingehalten.

## PHASE 1 – HISTORY AUTHORITY

Kandidat:
`hobbyroom/m37-history-authority-20260911`

Head:
`245b596f9d6dd67c759527a0f211dbe957f4e34f`

Erlaubter Diff:
- `control/startmaster0107/HOBBYRAUM_KNOWN_ERROR_REGRESSION_MATRIX_M01_M33_20260904.md`
- `control/startmaster0107/HOBBYRAUM_M01_M33_REGRESSION.py`

Soll:
- bestehender Main-Runner M01–M36: PASS;
- History-Kandidat: erster neue Fehler exakt M37 = FAIL;
- kein Produktfix;
- hardlock/hardlock-base müssen den vorhandenen Maschinenbeweis liefern.

Ein M37-FAIL in dieser Phase ist der gewünschte Reproduktionsbeweis, kein Produktionsfehler.

## PHASE 2 – PRODUCT FIX

Erst nach integrierter History-Autorität:
- separater Handoff-Kandidat;
- current main muss M37 als ersten FAIL reproduzieren;
- Kandidat muss denselben bestehenden Runner vollständig M01–M37 PASS bestehen;
- Positiv: vorhandener innerer nicht-reparierbarer PPM/PSERC-Grund wird sichtbar erhalten;
- Negativ: ohne vorhandenen inneren Grund wird nichts erfunden;
- Negativ: reparierbare Content-Codes bleiben RepairRequired;
- Hashkette + hardlock + hardlock-base auf demselben Head PASS.

## DANACH

Erst nach Phase-2-PASS genau ein frischer erster Artikel als Realtest bis zum echten PPM/PSERC-Handoff.
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
Main: `a2f2f1b4b7af1e905c6a0cb69c5389664b7c4ad6`
Recovery: `bb005a5324a0a6270aacb52b5927613bde1ab4bc`
