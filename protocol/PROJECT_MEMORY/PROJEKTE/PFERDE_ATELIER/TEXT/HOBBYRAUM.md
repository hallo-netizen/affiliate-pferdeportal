# TEXT – HOBBYRAUM

STAND: 2026-09-08
STATUS: FIX_FORBIDDEN

## EINZIGE ARBEITSWAHRHEIT

Ziel:
`107008 – FINAL_NEW_ARTICLE_BATCH_REVIEW_AWAIT_USER_PUBLISH`

Goldmaster:
`de21f6cd35c60849c551fd82f78e75ce57c99fab`

Aktueller main:
`2f3678aa495d40e5377881a6aa3655fb60e0c12e`

Aktueller erster echter Blocker:
`FACHWORKFLOW_PROOF_HANDOFF_BLOCKED`

Fehlerursache:
die gebundene `FACHWORKFLOW_HANDOFF_REQUEST.json` für den ersten Artikel fehlt am erwarteten Quarantine-Pfad.

B02 und B07/M32 sind im aktuellen Realtest überwunden.

## MASCHINELLER HOBBYRAUM-LOCK

```text
HOBBYROOM_WORK_LOCK_V1
STATUS: FIX_FORBIDDEN
OFFICE: TEXT
MAIN_SHA: 914638e67a265cf2e8951b1177a7d80fdf904e98
ACTIVE_BLOCKER: FACHWORKFLOW_PROOF_HANDOFF_BLOCKED
PLAN_PHASE: MACHINE_PROOF_GATE_M28_ROW_PARSER_BLOCKED
RECOVERY_BASE_SHA: de21f6cd35c60849c551fd82f78e75ce57c99fab
ACTIVE_HISTORY_CASE: M28
HISTORY_EXPECTED_FAIL: NONE
RECOVERY_SEQUENCE: 1_GOLDMASTER_EXACT;2_REALTEST;3_ONE_MANDATORY_DELTA;4_REALTEST;5_PASS_FREEZE_OR_FAIL_FULL_REVERT;6_REPEAT
CANDIDATE_BRANCH: hobbyroom/m28-handoff-request-current-main-20260908
CANDIDATE_HEAD_SHA: 78263594456bb58ae004b5b064816de0f3531720
TECHNICAL_SCOPE_PREFIXES: control/startmaster0107/;control/single-door-boundary/;control/output-quarantine/;control/CURRENT_STARTMASTER.json
ALLOWED_PATH_PREFIXES: control/single-door-boundary/codex_current_action.py;control/startmaster0107/STEP_107007_RUN_NEW_ARTICLE_BATCH_NO_STOP.json;control/startmaster0107/CURRENT_STATE.json;control/startmaster0107/PFERDE_ATELIER_START_HERE.json
CHECK_PAUL: PASS
CHECK_HISTORY: PASS
CHECK_LAST_GOOD: PASS
CHECK_NEIGHBORS: PASS
CHECK_REPEAT_CLASS: PASS
CHECK_POS_NEG: FAIL
CHECK_INVARIANTS: PASS
HISTORY_SOURCE_REF: control/startmaster0107/HOBBYRAUM_KNOWN_ERROR_REGRESSION_MATRIX_M01_M33_20260904.md
HISTORY_SOURCE_BLOB_SHA: 9f88203bf4f97c538acf75bdecf8051df1c6b3c2
HISTORY_PROOF_RUNNER_REF: control/startmaster0107/HOBBYRAUM_M01_M33_REGRESSION.py
HISTORY_PROOF_RUNNER_BLOB_SHA: f8f85aa515bdf7a05c7e54ff7bdc03f2605b4db8
PAUL_SOURCE_REF: protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/TEXT/PAUL_PIPELINE_AUDIT_20260906.md
PAUL_SOURCE_BLOB_SHA: 08fee3940a8f693ac6bb505df2e083b8515e2dd9
ERROR_SOURCE_REF: protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/TEXT/QUELLEN_AKTUELL/04_FEHLERLISTE_KOMPLETT_AKTUELL_20260905.md
ERROR_SOURCE_BLOB_SHA: e263de9d684e16c5ca95185079cbad1dd02fb26c
CURRENT_STATE_REF: protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/TEXT/CURRENT_STATE.md
CURRENT_STATE_BLOB_SHA: f1411091222090b7788d7859787a0e700d12eda7
DECISION_SOURCE_REF: protocol/PROJECT_MEMORY/AENDERUNGSREGISTER.md
DECISION_SOURCE_BLOB_SHA: f9757cb0c47df8184c3f64ffa45f63cdfe05efad
STANDARD_SOURCE_REF: protocol/PROJECT_MEMORY/BAUCONTAINER/HOBBYRAUM_STANDARD.md
STANDARD_SOURCE_BLOB_SHA: 62c723d1a147237050278f013c2a63d62f6d1115
PROTOCOL_SOURCE_REF: protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/TEXT/QUELLEN_AKTUELL/02_VOLLSTAENDIGES_PROTOKOLL_20260830_BIS_20260905.md
PROTOCOL_SOURCE_BLOB_SHA: cf1a96d4ef426ec529f78954dd4876e4599d954d
INTEGRATION_ALLOWED: false
END_HOBBYROOM_WORK_LOCK_V1
```

## EINGEFRORENER REPARATURALGORITHMUS

1. Nur den ersten realen Blocker bearbeiten.
2. Vor Kandidat: Paul-Prüfkarte, Fehlerhistorie, letzter funktionierender Stand, direkte Vor-/Nachstufe.
3. Genau eine zwingende Änderung.
4. Lokale Positiv-/Negativprüfung.
5. Echter 7/7-Realtest.
6. PASS bzw. erwartbares Weiterwandern → Zwischenstand einfrieren.
7. Regression / früherer neuer Fehler / Hardlock-FAIL → Änderung vollständig zurück.
8. Kein Fix auf einen fehlgeschlagenen Fix.
9. Kein zweiter Kandidat parallel.

## AKTUELLE EINZIGE NEXT ACTION

**STOP nach erstem Maschinen-Test.**

Erster Test:
- `hardlock`: PASS;
- `hardlock-base`: FAIL;
- erster Gate-Fehler: `HOBBYROOM_ACTIVE_HISTORY_CASE_ROW_INVALID:M28`.

Ursache hart geprüft:
Der auf main aktive `_error_row_for_case()`-Regex ist doppelt escaped und erkennt die reale Markdown-M28-Zeile nicht.

Wichtig:
- M28-Kandidat selbst noch nicht bewertet;
- Vorher-M28-FAIL/Nachher-GESAMT-PASS noch nicht erreicht;
- kein zweiter Fix;
- kein Merge;
- kein Realtest;
- kein Publish/WordPress-Write.

Nächste Arbeit erst nach diesem Testpunkt:
ausschließlich den Gate-Parserfehler als Security-Wartung reparieren und danach **denselben PR #161** erneut testen.

## VERBOTEN

- Konzeptwechsel;
- Parallelreparatur;
- Sammelfix;
- prophylaktischer LanguageTool-/SEO-/Link-/Tabellen-/Design-/Security-Fix;
- neuer Runner/Gate/Executor/Ersatzweg;
- Publish oder WordPress-Write.

## AUTORITÄTEN

Stand → `CURRENT_STATE.md`

Fehler → `protocol/PROJECT_MEMORY/FEHLERREGISTER.md` → autoritative TEXT-Fehlerquelle

Paul → `PAUL_PIPELINE_AUDIT_20260906.md`

Ziel → `protocol/PROJECT_MEMORY/ZIELVERTRAEGE/REGISTER.md`

Warum → `protocol/PROJECT_MEMORY/AENDERUNGSREGISTER.md`
