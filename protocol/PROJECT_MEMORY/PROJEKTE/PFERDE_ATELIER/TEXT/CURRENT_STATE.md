# TEXT – CURRENT STATE

STAND: 2026-09-08
STATUS: **BLOCKED – M35 PPM INPUT CONTRACT ANALYSIS**

## AUTORITÄT

Diese Datei enthält ausschließlich den belastbaren aktuellen TEXT-Stand.
Historie → vollständiges Protokoll.
Aktuelle Arbeitsanweisung → `HOBBYRAUM.md`.
Fehlerdetails → autoritative TEXT-Fehlerquelle.

## CURRENT MAIN

`2325f6e18bcd8cbb491a604780ee5b65d4bbf8ea`

PR #190 ist gemergt und entspricht diesem main.

## DISPATCHER / SCHUTZ

Permanenter Dispatcher PR #107:
- offen, **nicht mergen**;
- Head exakt `2325f6e18bcd8cbb491a604780ee5b65d4bbf8ea`.

GitHub Ruleset `Pferde Atelier Main Hardlock`:
- enforcement: active;
- bypass: leer;
- Required Checks: `hardlock`, `hardlock-base`.

## AKTUELLER REALBLOCKER

`PPM679_REAL_EXECUTION_FAILED:SOURCE_HASH_BINDING_MISMATCH`

Fehler-ID:
`M35 – Fact-Pack source-hash binding parity`.

Letzte erfolgreich erreichte Stelle im echten Realtest:
- frische `FACHWORKFLOW_HANDOFF_REQUEST.json` für Artikel 1 materialisiert;
- gebundener `fachworkflow_handoff.command` ausgeführt;
- echter PPM-6.7.9-Eingang erreicht;
- Stop erst bei Prüfung der Fact-Pack-Quellhashbindung.

Root Cause:
**noch nicht belegt**.

## REAL ÜBERWUNDEN AUF DEM AKTUELLEN WEG

- B02 / Fachworkflow-Worker-Kontext;
- B07/M32 / PPM-/PSERC-Runtime-Pfad;
- M28 / echter Request-first-Handoff;
- M34 / `CANONICAL_SLOT_MISSING` und zurückgerutschte Legacy-Handoff-Guards.

M34 wurde mit PR #190 als kompletter Handoff-Korridor auf den bewiesenen B01-Stand zurückgeführt.
Der nachfolgende Realtest kam real über Canonical/Slot hinaus.

## LETZTER SICHERER POSITIVER REFERENZSTAND

- `d841ed7590436ac100b98f15194874573e09bc03`: 7/7 frisch produziert;
- `de21f6cd35c60849c551fd82f78e75ce57c99fab`: 7/7 + 107008 Review PASS.

Diese Referenzen sind historische Vergleichsstände, **nicht** aktueller main.

## AKTIVER ARBEITSSTAND

Kein offener Produktions-Reparatur-PR.
PR #190: closed / merged.
PR #161: closed / merged.

Aktuell existiert **kein Produktionskandidat** für M35.

## TESTS – TATSÄCHLICH AUSGEFÜHRT

Auf PR #190:
- `hardlock`: PASS;
- `hardlock-base`: PASS;
- Scope: exakt 1 Datei;
- statischer Korridorcheck Request → PPM → PASS/Receipt → Submission → 107008: PASS.

Auf main `2325f6e1…`:
- echter STARTMASTER0107-Realtest gestartet;
- M28 real passiert;
- M34 / Canonical real passiert;
- erster Stop: M35 `SOURCE_HASH_BINDING_MISMATCH`.

## TESTS – OFFEN / NICHT BEHAUPTET

- kein 7/7-PASS auf aktuellem main;
- 107008 auf aktuellem main nicht erreicht;
- kein M35-Fix getestet;
- keine M35-Positiv-/Negativabnahme;
- kein Publish;
- keine WordPress-Schreibaktion.

## ZIEL

Unverändert:
`107008 – FINAL_NEW_ARTICLE_BATCH_REVIEW_AWAIT_USER_PUBLISH`.

Kein Auto-Publish.
Veröffentlichung nur nach ausdrücklicher Nutzerfreigabe.

## NEXT ACTION

Nicht hier dupliziert.
Ausschließlich `HOBBYRAUM.md` enthält die aktuelle NEXT ACTION.
