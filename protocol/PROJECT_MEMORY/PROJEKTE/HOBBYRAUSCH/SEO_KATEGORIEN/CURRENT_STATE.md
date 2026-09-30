# HOBBYRAUSCH – SEO_KATEGORIEN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-09-30
STATUS: BUCHBINDEN RESEARCH COMPLETE / V1.9.2 LIVE READBACK FAIL / ROLLBACK PASS / LIVE-URSACHE OFFEN / DIAGNOSE POSITIV+NEGATIV PASS

## Harte Abnahmeregel

**Keine Datei, kein Pluginstand und kein Produktionsschritt gilt als abnahmefähig ohne dokumentierte lokale Positiv- UND Negativsimulation.**

Ein synthetischer Einzeltest reicht nicht: Für einen behaupteten Live-Fix muss der echte Produktionspfad mit dem echten Paket simuliert sein.

## Live-Befund

Auch V1.9.2 scheiterte live mit:

`Readback fehlgeschlagen: DEPLOY_READBACK_MISMATCH | Automatischer Rollback: PASS`

V1.9.2 ist damit nicht abgenommen.

## Tatsächlicher gebundener Ausgangszustand

Der bestehende Live-Research-Snapshot vor dem Write enthält keines der sieben Buchbinden-Zielobjekte.

Für den echten Kandidaten ergibt die lokale Preflight-Simulation deshalb:
- CREATE: 7;
- UPDATE: 0;
- ADOPT_EXISTING: 0.

Der frühere angenommene Existing-Parent-Fall war nicht der reale Livepfad.

## Exakte Produktionssimulation

Mit dem echten Buchbinden-READ_ONLY_PREVIEW und dem echten Research-Paket, lokal nur testseitig neu signiert:

- Validator PASS;
- Research-Binding PASS;
- Research-Evidence PASS;
- Comparator PASS;
- Deployment-Preflight: 7 CREATE;
- Apply + Readback: PASS.

Der Livefehler lässt sich im bisherigen WordPress-Mock deshalb noch nicht reproduzieren.

## Feldgenaue Diagnose

Ein diagnostischer V1.9.3-Stand speichert den fehlgeschlagenen Readback vor Rollback und nennt:
- konkreten node/path;
- erwartete Werte;
- tatsächliche Werte;
- abweichende Felder.

Positiv:
- echter 7-CREATE-Plan → PASS.

Negativ:
- Slug-Mutation → slug;
- Name-Mutation → name;
- Parent-Mutation → parent;
- concept_id-Mutation → concept_meta;
- logischer Parent mutiert → logical_parent_meta;
- jeweils automatischer Rollback PASS.

Gesamtregression:
251/251 PASS.
PHP-Lint PASS.

Dies ist ausdrücklich Diagnose, noch kein Live-Fix.

## Produktionsdatei

Der fachliche Buchbinden-READ_ONLY_PREVIEW bleibt unverändert.
Kein neuer Research-Lauf erforderlich.

## NEXT ACTION

**Nicht erneut deployen.**

Zuerst:
`Kategorien → Protokoll → Protokoll als JSON exportieren`

Die eine JSON hier bereitstellen.

Dann wird der bereits gelaufene echte Dry-Run/Fehlerzustand ausgewertet, ohne einen weiteren WordPress-Write auszulösen.
