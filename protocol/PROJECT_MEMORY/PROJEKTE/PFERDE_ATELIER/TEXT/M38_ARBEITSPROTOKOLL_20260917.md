# PFERDE ATELIER – TEXT – M38 ARBEITSPROTOKOLL

STAND: 2026-09-17
STATUS: HISTORY_AUTHORITY_MAINTENANCE / PRODUKTFIX VERBOTEN BIS HISTORY-BEWEIS

## REALBEFUND

Der erste frische Artikel erreichte nach realer LanguageTool-Reparatur den realen PPM-6.7.9-/PSERC-Handoff und stoppte mit:

`PPM679_REAL_EXECUTION_BLOCKED:PSERC_BRIDGE_PPM_PLAN_VERSION_MISMATCH`

107008 wurde nicht erreicht. Kein WordPress-Write, kein Publish.

## GEBUNDENE HISTORY-BASIS

Realtest-Baseline / current main:
`7533d99e306bb016c87c7c63e2c6103bf1010476`

Letzter belastbarer Recovery-Stand:
`bb005a5324a0a6270aacb52b5927613bde1ab4bc`

Maschinensoll: M01–M37 PASS, M38 erster neuer FAIL.
Kein Publish.

## M38

M38 registriert ausschließlich die Versionsbindung des current Fachworkflow-`production_plan_header` für `production_plan_v4`.

Die bestehende Abschlusslogik bindet:
- `plan_contract_version == "4.0.0"`
- `required_plugin_version == "6.7.9"`

History-Kandidat PR277 darf ausschließlich die bestehende Fehlermatrix und den bestehenden Regressionrunner ändern.

## MASCHINENBEWEIS VOR PRODUKTFIX

Erwartet:
1. current main: M01–M37 PASS;
2. M38: erster neuer FAIL;
3. History-Kandidat: bestehender History-Maschinenbeweis/hardlocks;
4. erst danach separater kleinstmöglicher Produktfix.

## VERBOTEN

Kein Handoff-/PPM-/PSERC-/PSTE-/Textmaschinen-/Fachregel-/SEO-/Link-/Design-/WordPress-/Publish-Fix in der History-Phase.
Kein neuer Runner, Gate, Controller oder Sidecar.
