# SYSTEM 4A — PUNKT 5 REPAIR-RÜCKWEG

Stand: 17.09.2026
Aktiver Nachweisbranch: `hobbyroom/system4a-real-102-repair-matrix-clean-20260917`

## Aktueller Status

**PUNKT 5 = OFFEN unter dem verschärften HARD RULE.**

Der frühere Workflow `System 4A Repair Owner Contract`, Run `35197259525`, Head `475c57232b400a9f28523142863290866220a428`, SUCCESS, beweist die vollständige Regel->Owner-Zuordnung und die vier Owner-Routen. Er beweist jedoch **nicht**, dass jede der 102 reparierbaren Regeln einzeln real als Fehler ausgelöst, durch ihren Owner repariert und danach durch die komplette echte Textmaschine bis PASS geführt wurde.

Die frühere Formulierung `PUNKT 5 = PASS` war deshalb für den neuen HARD RULE zu weit.

## Unveränderte Klassifikation

102 reparierbare Regeln:

- 96 -> `DRAFT_WORKER`
- 3 -> `PARENT_TITLE_MACHINE`
- 2 -> `PORTAL_LINK_MACHINE`
- 1 -> `PARENT_CATEGORY_MACHINE`

49 weitere erreichbare Regeln bleiben terminal `HARD_BLOCK`.

## Neuer harter Nachweis

Ziel pro reparierbarer Regel:

`gezielter Fehler -> exakter Fehlercode -> richtiger Owner -> echte Reparatur -> vollständiger realer Fullcheck -> LT 6.8 PASS -> PPM 6.7.9 PASS -> erst dann Regel PASS`

Test-Harness:
- `isolated_system4/real_102_repair_matrix_v1.py`
- `isolated_system4/real_102_repair_matrix_runner_v4.py`
- `.github/workflows/system4a-real-102-repair-matrix.yml`

Mocks sind im Harness ausdrücklich verboten.

## Tatsächlich gefundene Fehler während des neuen Nachweises

1. Drei W4-Heading-Regeln wurden im Produktionsrouter fälschlich als `HARD_BLOCK` behandelt, obwohl sie reparierbar klassifiziert sind. Im Testweg wurde die korrekte Route `DRAFT_WORKER` hergestellt und als Regression in den Workflow aufgenommen.
2. Mehrere alte PPM-Testfixtures waren nicht mehr als heutige grüne Basis geeignet. Die 15 Canonical-PPM-Mutationen wurden deshalb auf den aktuell grünen System-4A-Artikel gebunden; 15/15 erreichen ihren exakten Ziel-Fehlercode.
3. Die Registry bindet 22 Content-Regeln an `tests/test-historical-regressions.php`. Diese Datei enthält tatsächlich nur 16 alte Infrastruktur-Incidents und emittiert diese 22 Content-Codes nicht. Der letzte echte Run `35214897183`, Head `2eba56cda276c67721577f0104ad89b65a2af890`, ist deshalb FAIL.
4. Der Inspektionsschritt desselben Runs fand im vorhandenen PHP-Testbestand für die 22 Codes nur für `BLOCKED_CONTENT_REQUIRED_BLOCK_MISSING` direkte aktuelle Negative-Tests (`three-type-bundled-local/*-negative.php`). Für die übrigen 21 gab es dort keinen direkten Treffer.

## NEXT ACTION

Die 22 veralteten/falschen Registry-Testbindungen mit **echten gezielten aktuellen Mutationen** schließen. Kein Echo und kein künstlicher PASS. Danach den Workflow erneut ausführen, bis der harte Marker real erscheint:

`TEXTMASCHINE_REAL_REPAIR_FULL_PASS:102/102`

Erst danach darf Punkt 5 wieder als PASS markiert werden. Danach folgt der separate globale Audit:

`Was behauptet jeder PASS – und was testet der Code wirklich?`
