# PFERDE ATELIER – TEXT – M38 ARBEITSPROTOKOLL

STAND: 2026-09-17
STATUS: HISTORY_AUTHORITY_MAINTENANCE / PRODUKTFIX VERBOTEN BIS HISTORY-BEWEIS

## REALBEFUND

Der erste frische Artikel erreichte nach realer LanguageTool-Reparatur den realen PPM-6.7.9-/PSERC-Handoff und stoppte mit:

`PPM679_REAL_EXECUTION_BLOCKED:PSERC_BRIDGE_PPM_PLAN_VERSION_MISMATCH`

107008 wurde nicht erreicht. Kein WordPress-Write, kein Publish.

## GEBUNDENE HISTORY-BASIS

Realtest-Baseline / current main:
`54f0ee4efb91a50bbe05b5aafa4183cc1f526565`

Letzter belastbarer Recovery-Stand:
`bb005a5324a0a6270aacb52b5927613bde1ab4bc`

Der aktuelle Main enthält den bereits geprüften 1..N-Finalizer und ausschließlich einen temporären, nicht-ausführbaren M20-Migrationstoken. Die aktive Mengenlogik bleibt 1..N.

Maschinensoll: Base M01–M37 PASS; kombinierter History-Kandidat korrigiert M20 auf 1..N und liefert M38 als ersten neuen FAIL.
Kein Publish.

## M38

M38 registriert ausschließlich die Versionsbindung des current Fachworkflow-`production_plan_header` für `production_plan_v4`.

Die bestehende Abschlusslogik bindet:
- `plan_contract_version == "4.0.0"`
- `required_plugin_version == "6.7.9"`.

History-Kandidat PR280 / Branch `hobbyroom/m20-history-1n-20260917` darf ausschließlich die bestehende Fehlermatrix und den bestehenden Regressionrunner ändern. Head: `424a6c5b418541ca2bbe89ca5cbfe233fd706e96`.

## MASCHINENBEWEIS VOR PRODUKTFIX

Erwartet:
1. current main: M01–M37 PASS;
2. Kandidat: M20 als 1..N-Regel, M01–M37 PASS;
3. M38: erster neuer FAIL;
4. History-Kandidat: bestehender History-Maschinenbeweis/hardlocks;
5. erst danach separater kleinstmöglicher Produktfix.

## VERBOTEN

Kein Handoff-/PPM-/PSERC-/PSTE-/Textmaschinen-/Fachregel-/SEO-/Link-/Design-/WordPress-/Publish-Fix in der History-Phase.
Kein neuer Runner, Gate, Controller oder Sidecar.
