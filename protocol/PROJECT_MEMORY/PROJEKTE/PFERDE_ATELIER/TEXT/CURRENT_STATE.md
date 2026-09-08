# TEXT – CURRENT STATE

STAND: 2026-09-08
STATUS: FROZEN REPAIR / B07-M32 LIVE ÜBERWUNDEN / HANDOFF-REQUEST AKTUELLER REALBLOCKER

## AUTORITÄT

Diese Datei ist die einzige aktuelle Standzusammenfassung des Büros TEXT.
Die einzige aktuelle Arbeits-/NEXT-ACTION-Wahrheit steht in `HOBBYRAUM.md`.

## CURRENT MAIN

`914638e67a265cf2e8951b1177a7d80fdf904e98`

Letzter Merge:
`Merge history machine-proof runner bootstrap`

Maschinenbeweis-Runner:
- PR #159;
- eine Datei `control/startmaster0107/HOBBYRAUM_M01_M33_REGRESSION.py`;
- `hardlock` PASS;
- `hardlock-base` PASS;
- stale M26/M28/M31-Prüfungen korrigiert;
- M28-Negativ-Mutanten-Selbsttest eingebaut.

## EINGEFRORENER REPARATURWEG

Eine einzige maschinelle Reparaturstraße:

1. offizieller Hobbyraum bindet current main + ersten realen Blocker + exakten Kandidatenscope;
2. autoritative Fehlerquelle, CURRENT_STATE, Paul-Audit, M01–M33-Matrix und vertrauenswürdiger Base-Runner werden per Git-Blob gebunden;
3. Produktionskandidat darf Matrix/Runner nicht mitändern;
4. kompletter vertrauenswürdiger M01–M33-Lauf muss gegen den Kandidaten GESAMT PASS sein;
5. erst dann Merge;
6. danach genau ein echter 7/7-Realtest;
7. der erste neue reale Blocker wird alleinige neue Arbeitswahrheit;
8. kein Fix während des Realtests, kein Parallel-/Sammelfix.

Die bisherigen sieben manuellen `CHECK_*`-Felder sind keine Integrationsautorität mehr. Sie können den Maschinenbeweis nicht ersetzen.

## LETZTER SICHERER STAND

Goldmaster:
`de21f6cd35c60849c551fd82f78e75ce57c99fab`

Bewiesen:
7/7 + 107008 Review PASS; späterer Fehler erst im GitHub-Endstempel/Auth-Bereich.

Die motorrelevanten Cloud-Entry-Dateien wurden im Wiederaufbau exakt auf diesen Stand zurückgeführt.

## LETZTER REALTEST

Letzter echter Realtest lief auf `36d1ecb5…`:

PASS:
- Cloud Entry;
- Production Preflight;
- Runtime Entry;
- Current Action READY;
- Single Door READY.

B02:
`BOUND_CURRENT_FACHWORKFLOW_EXECUTION_CONTEXT_MISSING`
ist im aktuellen Realtest **überwunden**.

Erster echter Blocker dieses letzten Realtests:
`BOUND_REAL_PPM679_RUNTIME_PATH_NOT_EXPOSED_TO_SUBMISSION_COMMAND`

Konkret:
Der gebundene `fachworkflow_handoff.command` exponiert die erforderlichen Runtime-Pfade für
`PPM679_PACKAGE_ZIP` und `PSERC_FIX_ZIP` nicht.

## AKTUELLER REALTEST

Realtest auf current main `30e93335…`:
- `CODEX_CLOUD_ENTRANCE_PASS`;
- `CODEX_PRODUCTION_PREFLIGHT_PASS`;
- `OFFICIAL_RUNTIME_ENTRY_PASS`;
- `CURRENT_BOUND_ACTION_READY`;
- `PRODUCTIVE_SINGLE_DOOR_READY`;
- echter `fachworkflow_proof_handoff.py materialize` wurde gestartet.

Damit ist B07/M32 **real überwunden**.

Neuer erster echter Blocker:
`FACHWORKFLOW_PROOF_HANDOFF_BLOCKED`

Exakte Ursache:
die gebundene `FACHWORKFLOW_HANDOFF_REQUEST.json` für den ersten Artikel fehlt am erwarteten Quarantine-Pfad.

Nicht erreicht:
- 107007 Abschluss;
- 107008.

Keine Codeänderung, kein Publish, kein WordPress-Write.

Kein Publish, kein WordPress-Write, keine Codeänderung im Realtest.

## SCHUTZ / TESTGRENZE

Ruleset `Pferde Atelier Main Hardlock`:
- `hardlock` Pflicht;
- `hardlock-base` Pflicht;
- kein Bypass-Akteur.

Vorbereitete serverseitige Reparatur-Zwangsjacke:
- PR #160;
- Head `a6f6240c05adb75883416440b4618a6ce428ecc6`;
- exakt eine Security-Datei: `control/paul-scope-gate/paul_scope_gate.py`;
- bindet current main, `RECOVERY_BASE_SHA`, CURRENT_STATE, autoritative Fehlerquelle, Paul-Audit, fortlaufende historische Fehlermatrix, vertrauenswürdigen Base-Runner, Änderungs-/Erklärungsregister, Hobbyraum-Standard und vollständiges Ausführungs-/Testprotokoll;
- historische Fehler müssen ab M01 lückenlos sein; mindestens M01–M33 bleiben Pflicht;
- Matrix, Runner und Fehlerquelle müssen dieselbe akzeptierte Historie tragen;
- `ACTIVE_BLOCKER` muss in Fehlerquelle und CURRENT_STATE real vorhanden sein;
- `MAIN_SHA` und letzter guter `RECOVERY_BASE_SHA` müssen in CURRENT_STATE real vorhanden sein;
- Pauls zentrale technische Regeln werden semantisch geprüft;
- Frozen-Recovery, kausaler Corridor und Maschinenbeweis-Entscheidung werden semantisch geprüft;
- der verbindliche Pre-Fix-Ablauf wird semantisch geprüft;
- das Ausführungs-/Testprotokoll muss current main, aktuellen Realblocker und letzten guten `RECOVERY_BASE_SHA` enthalten;
- `ACTIVE_HISTORY_CASE` bindet den aktuellen Realblocker an genau einen historischen Regressionstest;
- current main muss vor einem Produktionsfix exakt `ACTIVE_HISTORY_CASE` als ersten FAIL reproduzieren;
- derselbe vertrauenswürdige Runner muss danach auf dem Kandidaten die komplette Historie PASS machen;
- `RECOVERY_BASE_SHA` muss als realer Git-Commit existieren und Vorfahr des current main sein;
- Matrix/Runner-Wartung ist separat und darf nicht mit Produktionscode gemischt werden;
- neue reale Fehler müssen vor jedem Fix zuerst als ausführbare Regression aufgenommen werden;
- `HISTORY_EXPECTED_FAIL` zwingt den neuen/zu korrigierenden Regressionstest, auf dem noch unreparierten Stand exakt als erster Fehler FAIL zu liefern;
- danach erst darf ein Produktionsfix entstehen und muss die gesamte erweiterte Historie PASS machen;
- M34, M35, ... können dadurch ohne erneute Security-Gate-Änderung aufgenommen werden;
- manuelle `CHECK_*`-Felder sind ausdrücklich keine Freigabeautorität;
- Gate-Arbeitslock-/Evidenz-Selbsttests laufen bei jedem serverseitigen `verify-pr` automatisch;
- Kandidatenänderungen am Runner können den Produktionsbeweis nicht selbst fälschen.
Aktuell: `ACTIVE_HISTORY_CASE = M28`.

PR #160 ist **integriert**.
Merge/main: `914638e67a265cf2e8951b1177a7d80fdf904e98`.

Die serverseitige Reparatur-Zwangsjacke ist damit auf `main` aktiv.

Aktueller Sicherheitsstatus:
Der temporäre Ruleset-Bypass wurde entfernt und frisch verifiziert:
- `bypass_actors: []`;
- `current_user_can_bypass: never`;
- Required Checks `hardlock` + `hardlock-base` aktiv.

M28-Kandidat vorbereitet:
- Branch `hobbyroom/m28-handoff-request-current-main-20260908`;
- Head `78263594456bb58ae004b5b064816de0f3531720`;
- Base/current main `914638e67a265cf2e8951b1177a7d80fdf904e98`;
- exakt vier Dateien: Current Action, 107007-Bundle, CURRENT_STATE.json, PFERDE_ATELIER_START_HERE.json;
- Request-Schema exponiert;
- 107007 auf Request → vorhandenen Adapter → Submission umgestellt;
- Hashkette Current Action → 107007 → CURRENT_STATE → Root vollständig konsistent;
- statische M28-Positiv/Negativ-Vorprüfung PASS.

Nächster Beweis:
serverseitiger Hardlock muss current main zuerst exakt bei M28 FAIL reproduzieren und denselben vertrauenswürdigen Runner danach auf dem Kandidaten vollständig PASS prüfen.

Der B02-Kandidat `562b71c7…` hatte vor Merge:
- `hardlock` PASS;
- `hardlock-base` PASS.

Der danach auf dem permanenten Dispatcher-PR #107 ausgelöste `hardlock-base`-Lauf scheiterte separat an
`IMMUTABLE_SECURITY_PATH_CHANGE_BLOCKED`, weil PR #107 gegen seinen alten Dispatcher-Base historische immutable Änderungen enthält.
Das ist **kein TEXT-Produktionsblocker** und kein PASS-Beleg für den Produktionslauf.

## PAUL

`PAUL_PIPELINE_AUDIT_20260906.md` bleibt verpflichtende technische Prüflinse.
Kein 41-Punkte-Sammelfix.

## ZIEL

Unverändert:
`107008 – FINAL_NEW_ARTICLE_BATCH_REVIEW_AWAIT_USER_PUBLISH`

Kein Auto-Publish.

## NEXT ACTION

Nicht hier dupliziert.
Ausschließlich `HOBBYRAUM.md` ist die aktuelle NEXT-ACTION-Wahrheit.

### Erster Maschinen-Test M28 – FAIL im Gate vor Kandidatenbewertung

PR #161:
- Branch `hobbyroom/m28-handoff-request-current-main-20260908`;
- Head `78263594456bb58ae004b5b064816de0f3531720`.

Ergebnis:
- `hardlock`: PASS;
- `hardlock-base`: FAIL im Schritt `Enforce current Paul assignment and technical write scope`;
- Gate-Selbsttest: `HOBBYROOM_WORK_LOCK_SELFTEST_PASS:8/8`;
- erster echter Gate-Fehler: `HOBBYROOM_ACTIVE_HISTORY_CASE_ROW_INVALID:M28`.

Harte Ursachenprüfung auf current main:
`_error_row_for_case()` verwendet den Regex
`r"(?m)^\\|\\s*" ... r"\\s*\\|.*$"`
und sucht damit nicht korrekt die reale Markdown-Zeile `| M28 | ... |`.

Folge:
Der neue Vorher-FAIL/Nachher-PASS-Beweis wurde noch **nicht** erreicht.
Der M28-Produktionskandidat ist noch nicht bewertet.

Status:
`FIX_FORBIDDEN`.
Kein Merge, kein Realtest, kein Publish/WordPress-Write.

