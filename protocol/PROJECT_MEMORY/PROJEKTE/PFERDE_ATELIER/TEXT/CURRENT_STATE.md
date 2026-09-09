# TEXT – CURRENT STATE

STAND: 2026-09-09
STATUS: **AKTIV – M26 CONTEXT MARKER NORMALIZATION UNDER TEST**

## AUTORITÄT

Diese Datei enthält ausschließlich den belastbaren aktuellen TEXT-Stand.
Historie → vollständiges Protokoll.
Aktuelle Arbeitsanweisung → `HOBBYRAUM.md`.
Fehlerdetails → autoritative TEXT-Fehlerquelle.

## CURRENT MAIN

`a63c20100759b4e42d07f2e70a11ee9875709d37`

PR #201 / M22 ist regulär über `hardlock` + `hardlock-base` gemergt.
M22 ist integriert behoben.

## DISPATCHER / SCHUTZ

Permanenter Dispatcher PR #107:
- offen, **nicht mergen**;
- Head exakt `a63c20100759b4e42d07f2e70a11ee9875709d37`.

GitHub Ruleset `Pferde Atelier Main Hardlock`:
- enforcement: active;
- Required Checks: `hardlock`, `hardlock-base`.

## AKTUELLER INTEGRATIONSBLOCKER

`M26_CURRENT_FACHWORKFLOW_CONTEXT_NOT_BOUND:reale Nicht-PPM-Stage-Artefakte`

Fehler-ID:
`M26 – Bound Fachworkflow production context`.

Gegenprüfung:
- Current-Action-Selftest PASS;
- gebundener Fachworkflow-Worker PASS;
- Handoff-Request-Vertrag PASS;
- STEP107007 enthält die geforderte Semantik bereits als `die realen Nicht-PPM-Stage-Artefakte und Proofs`;
- Ursache ist ausschließlich exakter Marker-/Wortlaut-Drift `reale` vs. `realen`;
- kein funktionaler Kontextverlust.

## AKTIVER M26-KANDIDAT

Branch:
`hobbyroom/m26-context-marker-normalization-20260909`

Head:
`b55621e556eb25ec5bee4fd9b2f9662380575398`

Scope exakt 3 Dateien:
- `control/startmaster0107/STEP_107007_RUN_NEW_ARTICLE_BATCH_NO_STOP.json` — nur `die realen ...` → `reale ...`;
- `control/startmaster0107/CURRENT_STATE.json` — nur Bundle-SHA;
- `control/startmaster0107/PFERDE_ATELIER_START_HERE.json` — nur State-SHA.

Keine Fachregel, kein Handoff-Verhalten, kein Runner/Gate/Contract/Executor geändert.

## PRÜFUNG – TATSÄCHLICH AUSGEFÜHRT

- main: drei M26-Kontextmarker PASS, exakter vierter Marker FAIL;
- Kandidat: alle vier Marker PASS;
- Worker-Bindung bleibt vorhanden;
- `FACHWORKFLOW_HANDOFF_REQUEST.json` bleibt vorhanden;
- No-Publish bleibt vorhanden;
- Instruction-Delta ausschließlich Wortlautnormalisierung, Länge -5 Zeichen;
- STEP107007/State/Root-Hashkette nachgezogen.

## NÄCHSTER BEKANNTER FEHLER DANACH

M35 bleibt der bekannte reale Liveblocker:
`PPM679_REAL_EXECUTION_FAILED:SOURCE_HASH_BINDING_MISMATCH`

Geparkter M35-Kandidat:
`ef2ecebeb2992013873ba72100d79ffd7c48393c`

## LETZTER SICHERER POSITIVER REFERENZSTAND

- `d841ed7590436ac100b98f15194874573e09bc03`: 7/7 frisch produziert;
- `de21f6cd35c60849c551fd82f78e75ce57c99fab`: 7/7 + 107008 Review PASS.

`RECOVERY_BASE_SHA = de21f6cd35c60849c551fd82f78e75ce57c99fab`.

## OFFEN / NICHT BEHAUPTET

- serverseitige Required Checks des M26-Kandidaten noch offen;
- kein neuer 7/7-Realtest;
- kein Publish;
- keine WordPress-Schreibaktion.

## ZIEL

Unverändert:
`107008 – FINAL_NEW_ARTICLE_BATCH_REVIEW_AWAIT_USER_PUBLISH`.

Kein Auto-Publish.
