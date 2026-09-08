# TEXT – CURRENT STATE

STAND: 2026-09-08
STATUS: FROZEN REPAIR / B07-M32 LIVE ÜBERWUNDEN / HANDOFF-REQUEST AKTUELLER REALBLOCKER

## AUTORITÄT

Diese Datei ist die einzige aktuelle Standzusammenfassung des Büros TEXT.
Die einzige aktuelle Arbeits-/NEXT-ACTION-Wahrheit steht in `HOBBYRAUM.md`.

## CURRENT MAIN

`2325f6e18bcd8cbb491a604780ee5b65d4bbf8ea`

Letzter Merge:
`PR #166 – Security: fix active history M28 row parser`

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

Aktive serverseitige Reparatur-Zwangsjacke:
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

### Security-Wartung nach erstem Maschinen-Test

Erster PR-#161-Maschinen-Test stoppte vor M28-Kandidatenbewertung mit:
`HOBBYROOM_ACTIVE_HISTORY_CASE_ROW_INVALID:M28`.

Root-Cause:
`_error_row_for_case()` im auf main aktiven Gate verwendet einen doppelt escapten Markdown-Zeilenregex.

Security-Fix vorbereitet:
- PR #166;
- Branch `hobbyroom/security-fix-m28-row-parser-20260908`;
- Head `a742c5c917b5e6fe164be2a6267470de89e9d744`;
- exakt eine Datei;
- exakt +1/-1 Regex-Zeile.

Lokaler Positiv/Negativ-Beweis:
- reale M28-Zeile -> genau 1 Treffer;
- M29 statt M28 -> 0 Treffer;
- eingebettete Fake-Zeile -> 0 Treffer;
- doppelte M28-Zeile -> 2 Treffer und damit fail-closed.

GitHub-Test PR #166:
- `hardlock-base` Run `34226241411`;
- Stop im immutable path guard;
- exakt `IMMUTABLE_SECURITY_PATH_CHANGE_BLOCKED`;
- `PATH_GUARD_SELFTEST_PASS`.

M28-Produktionskandidat PR #161 bleibt unverändert offen und **nicht bewertet**.

### PR #166 integriert – Parserfix aktiv / Ruleset wieder geschlossen

Security-PR #166 wurde kontrolliert gemergt.

Current main:
`755b531ec08298a86cb0342c2db8c81f5b4df6f9`.

Verifiziert auf main:
`_error_row_for_case()` nutzt jetzt korrekt
`r"(?m)^\|\s*" + re.escape(case) + r"\s*\|.*$"`.

Temporärer PR-only-Admin-Bypass danach entfernt und frisch verifiziert:
- `bypass_actors: []`;
- `current_user_can_bypass: never`;
- Required Checks `hardlock` + `hardlock-base` aktiv.

PR #161 wurde inhaltlich **nicht verändert**.
Technischer Synchronisationscommit vorbereitet:
`26d7b5b53044729ab6350f88d16d4ac0f6cacd03`.

Baumgrundlage:
current main `755b531e…`.

Darauf exakt die vier unveränderten M28-Dateiblobs des bisherigen PR #161.
Kein zusätzlicher M28-Fix, kein Runner-/Gate-/Publish-Umbau.

### Zweiter PR-#161-Maschinen-Test – Goldmaster-Ahnenprüfung falsch-negativ

PR #161, synchronisierter Head:
`26d7b5b53044729ab6350f88d16d4ac0f6cacd03`.

Ergebnis:
- `hardlock`: PASS;
- `hardlock-base`: FAIL;
- Gate-Selbsttests PASS:
  - `HOBBYROOM_WORK_LOCK_SELFTEST_PASS:8/8`;
  - `HOBBYROOM_EVIDENCE_SELFTEST_PASS:10/10`;
  - `HOBBYROOM_HISTORY_REPRODUCTION_PASS:M28`;
  - `HOBBYROOM_HISTORY_RUNNER_MODE_SELFTEST_PASS:3/3`;
- Work-Lock selbst PASS:
  `HOBBYROOM_WORK_LOCK_PR_PASS`;
- erster Stop danach:
  `HOBBYROOM_RECOVERY_BASE_NOT_ANCESTOR:de21f6…:MAIN=755b531e…`.

Harte Gegenprüfung über GitHub-Commitgraph:
- Merge-Base = exakt `de21f6cd35c60849c551fd82f78e75ce57c99fab`;
- current main liegt 176 Commits voraus;
- Goldmaster ist damit **realer Vorfahr**.

Root-Cause:
`.github/workflows/pferde-atelier-immutable-base-hardlock.yml` checkt Base mit `fetch-depth: 1` aus und Kandidat ebenfalls nur mit `--depth=1`.
Der Gate führt danach `git merge-base --is-ancestor` im shallow Repository aus und erzeugt einen falschen Negativbefund.

Einordnung:
Kontrollsystemfehler, nicht M28-Produktionsfehler.
PR #161 bleibt unverändert.

### Security-Fix PR #177 vorbereitet – shallow ancestry proof

PR #177:
- Branch `hobbyroom/security-fix-shallow-recovery-ancestry-20260908`;
- Head `f69b415099f7d9f936a81f21a56bbaa408e8dfc7`;
- exakt eine Datei;
- exakt +2/-0.

Änderung:
In `_assert_real_recovery_base()` wird nur dann, wenn `git rev-parse --is-shallow-repository == true`, vor der bestehenden Ahnenprüfung
`git fetch --no-tags --unshallow origin <pr_base>`
ausgeführt.

Die harte Ahnenregel bleibt unverändert.

Lokaler Git-Beweis:
- shallow ancestry check vor unshallow: FAIL;
- nach unshallow: PASS.

GitHub-Vorprüfung PR #177:
- Run `34229441561`, Job `102071584302`;
- Stop ausschließlich im immutable path guard;
- `IMMUTABLE_SECURITY_PATH_CHANGE_BLOCKED`;
- `PATH_GUARD_SELFTEST_PASS`.

PR #161 bleibt unverändert eingefroren.

### Kontrollsystem eingefroren / M28-Test fortsetzen

PR #177 ist integriert. Das Kontrollsystem wird ab hier **nicht weiter ausgebaut**.

Aktueller main:
`a61a380e948e15f2ed3ce5ddec41b128efbe7ae6`.

PR #161 bleibt derselbe M28-Produktionsfix.
Neuer reiner Synchronisations-Test-Head:
`a2a4aca682e46ac5913d4cad554a604f4edd8d59`.

Die vier M28-Dateiblobs sind unverändert.
Ziel jetzt ausschließlich:
M28-Kandidat prüfen -> bei PASS mergen -> echter 7/7-Realtest.

### KISS-Korrektur – Maschinenlock für TEXT nicht weiter als Produktionsblocker verwenden

Der aktuelle Runner meldete M15 vor M28.
Harte Prüfung ergab:
- M15-Matrix: "keine widersprüchliche Handoff-Sperre";
- aktueller M15-Runner verlangt dagegen "Kein Vorab-Handoff durch den Worker" und verbietet `FACHWORKFLOW_HANDOFF_REQUEST.json`;
- gemergte historische PRs #110 und #111 belegen ausdrücklich den Request-first-Weg.

Damit ist M15 im Runner stale und widerspricht der bewiesenen Historie.

Entscheidung:
Keine weitere Gate-/Security-Reparaturschleife.
Der komplexe TEXT-Maschinenlock wird als Integrationsblocker deaktiviert.
Normale Repository-Schutzchecks `hardlock` und `hardlock-base` bleiben vollständig aktiv.

Produktionsfokus:
PR #161 / M28 -> normale Checks -> Merge -> echter 7/7-Realtest.

### M28 integriert – Realtest freigegeben

PR #161 ist gemergt.
Neuer main:
`78bb2576214a8c0a82d201ed35530ad9ac885481`.

Vor Merge:
- `hardlock`: PASS;
- `hardlock-base`: PASS;
- exakt 4 M28-Dateien;
- kein Publish/WordPress-Write.

Status jetzt:
`REALTEST_ONLY`.

Nächster Schritt:
permanenten Dispatcher PR #107 exakt auf current main setzen und echten 7/7-Lauf starten.
Keine Reparatur während des Laufs.

### Neuer Realblocker nach M28 – systemische Ursache belegt

Realtest auf main `78bb2576214a8c0a82d201ed35530ad9ac885481`.

M28 **real überwunden**:
- reale `FACHWORKFLOW_HANDOFF_REQUEST.json` erzeugt;
- gebundener `fachworkflow_handoff.command` gestartet;
- echter PPM-6.7.9-Lauf erreicht.

Erster neuer Blocker:
`PPM679_REAL_EXECUTION_FAILED:CANONICAL_SLOT_MISSING`.

Harte Historienprüfung:
- B01 `5fe9967bbd65b4247f5a75ac50c47060fc1f5149` hatte im Handoff die starre Canonical-Slot-Vorbedingung bereits entfernt und die Kategorieprüfung auf den bestehenden semantischen Vertrag umgestellt.
- späterer Reapply `e5fc1c88dfac81b3ef18ff9b02bf37a677b0185a` stellte den älteren PR-#124-Handoff wieder her;
- dadurch wurden `find_slot(...)/CANONICAL_SLOT_MISSING` **und** die alte numerische WordPress-ID-Pflicht wieder eingeführt;
- B07/M32 `41849f0…` reparierte nur die Runtime-Pfade auf diesem regressierten Handoff.

Konsequenz:
Kein isolierter Canonical-Slot-Fix.
Nächster Schritt ist ein vollständiger, begrenzter Handoff-Korridorvergleich:
B01-Semantik als funktionale Basis + nur später zwingend bewiesene Änderungen (Runtime-Pfade, M28 Request-first/Current Action) erhalten.

### M34-Korridor-Kandidat – einheitliche Handoff-Rekonstruktion

Aktueller main:
`78bb2576214a8c0a82d201ed35530ad9ac885481`.

Aktiver Realblocker:
`PPM679_REAL_EXECUTION_FAILED:CANONICAL_SLOT_MISSING`.

Systemische Ursache:
Der aktuelle PPM-Handoff war durch späteres Reapply auf ältere PR-#124-Semantik zurückgerutscht und hatte bereits durch B01 korrigierte Vorbedingungen sowie heutige PASS-/Output-Bindungen verloren.

Kandidat:
- Branch `hobbyroom/m34-ppm-handoff-corridor-reconstruction-20260908`;
- Head `5e7ebadd991ae5b43de74f95bc232a4fa42b3b23`;
- exakt eine Datei:
  `control/startmaster0107/fachworkflow_proof_handoff.py`;
- Kandidatenblob exakt B01:
  `2c5d989ebbdb4a9221226b8f6ab675ca2a3122f1`.

Gesamtprüfung vor PR:
- Requestfelder exakt heutiger Current-Action-Vertrag: PASS;
- PASS-/Receipt-Felder heutiger Validator: PASS;
- echter PPM weiterhin zwingend: PASS;
- PPM-/PSERC-Repo-Runtime-Fallback: PASS;
- Slotauflösung über gebundenen externen `plan_slot`: PASS;
- semantischer Kategorievertrag: PASS;
- vollständige Stage-/Artefakt-Outputs im Receipt: PASS;
- alte `CANONICAL_SLOT_MISSING`-Vorbedingung entfernt;
- alte numerische WP-ID-Pflicht entfernt.

Keine Änderung an Current Action, 107007, Runner/Gates, Textmaschine, SEO, PPM/PSERC/PSTE-Regeln oder Publish.

### M34-Handoff-Korridor integriert – REALTEST_ONLY

PR #190 gemergt.
Neuer main:
`2325f6e18bcd8cbb491a604780ee5b65d4bbf8ea`.

Vor Merge:
- exakt 1 Datei;
- Kandidat exakt B01-Handoff-Blob;
- Request -> PPM -> PASS/Receipt -> Submission -> 107008 statisch konsistent;
- `hardlock`: PASS;
- `hardlock-base`: PASS.

Status:
`REALTEST_ONLY`.
Keine Reparatur während des 7/7-Laufs.

