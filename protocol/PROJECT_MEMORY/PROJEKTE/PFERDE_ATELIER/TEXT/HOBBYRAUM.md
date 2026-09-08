# TEXT – HOBBYRAUM

STAND: 2026-09-08
STATUS: **BLOCKED – M35 ANALYSE**

## EINZIGE ARBEITSWAHRHEIT

Ziel:
`107008 – FINAL_NEW_ARTICLE_BATCH_REVIEW_AWAIT_USER_PUBLISH`

Current main:
`2325f6e18bcd8cbb491a604780ee5b65d4bbf8ea`

Aktueller erster echter Blocker:
`PPM679_REAL_EXECUTION_FAILED:SOURCE_HASH_BINDING_MISMATCH`

Fehler-ID:
`M35 – Fact-Pack source-hash binding parity`

Letzte real erfolgreiche Stelle:
- frischer `FACHWORKFLOW_HANDOFF_REQUEST.json` für Artikel 1;
- gebundener `fachworkflow_handoff.command`;
- echter PPM-6.7.9-Eingang;
- Stop erst bei Fact-Pack-Quellhashbindung.

Root Cause:
**noch nicht belegt**.

Kein Produktionskandidat aktiv.

## MASCHINELLER HOBBYRAUM-LOCK

Der frühere TEXT-Maschinenlock ist **eingefroren und keine aktuelle Reparaturautorität**.
Normale GitHub-Schutzchecks bleiben verbindlich.

```text
HOBBYROOM_WORK_LOCK_V1
STATUS: FIX_FORBIDDEN
OFFICE: TEXT
MAIN_SHA: 2325f6e18bcd8cbb491a604780ee5b65d4bbf8ea
ACTIVE_BLOCKER: PPM679_REAL_EXECUTION_FAILED:SOURCE_HASH_BINDING_MISMATCH
PLAN_PHASE: M35_PPM_INPUT_CONTRACT_ANALYSIS
RECOVERY_BASE_SHA: de21f6cd35c60849c551fd82f78e75ce57c99fab
ACTIVE_HISTORY_CASE: M35
HISTORY_EXPECTED_FAIL: NONE
RECOVERY_SEQUENCE: 1_ANALYSE_FULL_BOUNDED_CORRIDOR;2_PROVE_ROOT_CAUSE;3_ONE_KISS_CANDIDATE;4_HARDLOCKS;5_REALTEST
CANDIDATE_BRANCH: NONE
CANDIDATE_HEAD_SHA: NONE
TECHNICAL_SCOPE_PREFIXES: NONE
ALLOWED_PATH_PREFIXES: NONE
CHECK_PAUL: PASS
CHECK_HISTORY: PASS
CHECK_LAST_GOOD: PASS
CHECK_NEIGHBORS: PASS
CHECK_REPEAT_CLASS: PASS
CHECK_POS_NEG: PENDING
CHECK_INVARIANTS: PASS
HISTORY_SOURCE_REF: control/startmaster0107/HOBBYRAUM_KNOWN_ERROR_REGRESSION_MATRIX_M01_M33_20260904.md
HISTORY_SOURCE_BLOB_SHA: 9f88203bf4f97c538acf75bdecf8051df1c6b3c2
HISTORY_PROOF_RUNNER_REF: control/startmaster0107/HOBBYRAUM_M01_M33_REGRESSION.py
HISTORY_PROOF_RUNNER_BLOB_SHA: f8f85aa515bdf7a05c7e54ff7bdc03f2605b4db8
PAUL_SOURCE_REF: protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/TEXT/PAUL_PIPELINE_AUDIT_20260906.md
PAUL_SOURCE_BLOB_SHA: 08fee3940a8f693ac6bb505df2e083b8515e2dd9
ERROR_SOURCE_REF: protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/TEXT/QUELLEN_AKTUELL/04_FEHLERLISTE_KOMPLETT_AKTUELL_20260905.md
ERROR_SOURCE_BLOB_SHA: 6817cbcb403ebecd1527508a1f2f6d7476882399
CURRENT_STATE_REF: protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/TEXT/CURRENT_STATE.md
CURRENT_STATE_BLOB_SHA: 125bd683e155806e58c2016c7a9d4e1c35cf502e
DECISION_SOURCE_REF: protocol/PROJECT_MEMORY/AENDERUNGSREGISTER.md
DECISION_SOURCE_BLOB_SHA: bc7fa6f1bfa06f1a9f52440480f7b69037184f8e
STANDARD_SOURCE_REF: protocol/PROJECT_MEMORY/BAUCONTAINER/HOBBYRAUM_STANDARD.md
STANDARD_SOURCE_BLOB_SHA: ebc17644fa0793bace4b6c93408909df515d8792
PROTOCOL_SOURCE_REF: protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/TEXT/QUELLEN_AKTUELL/02_VOLLSTAENDIGES_PROTOKOLL_20260830_BIS_20260905.md
PROTOCOL_SOURCE_BLOB_SHA: de22532cb980630e6f7d9aa5001ed3412d8831a2
INTEGRATION_ALLOWED: false
END_HOBBYROOM_WORK_LOCK_V1
```

## AKTUELLE EINZIGE NEXT ACTION

**Keine Reparatur. Erst den kompletten begrenzten PPM-Eingangsvertrag hart klären.**

Read-only prüfen:

1. Welche Source-Refs und Source-Hashes erwartet der reale PPM-6.7.9-Vertrag exakt?
2. Welche Source-Struktur/Hashes erzeugt der frische aktuelle `fact_pack` tatsächlich?
3. Wie werden diese Werte im `FACHWORKFLOW_HANDOFF_REQUEST.json` weitergegeben?
4. Stimmen Algorithmus, Normalisierung, Ref-Pfad und Hashgegenstand zwischen:
   - aktuellem Fact-Pack;
   - aktuellem Handoff;
   - PPM-Paket;
   - Production-Plan;
   - letztem realen 7/7-Stand `d841ed…`;
   - letztem 7/7+107008-Stand `de21f6…`
   überein?
5. Erst wenn die **eine kausale Abweichung** belegt ist: genau einen KISS-Kandidaten definieren.

## VERBINDLICHER ARBEITSWEG

- KISS;
- großes Ganzes zuerst;
- bei vermutetem Reapply-/Paritätsfehler den gesamten betroffenen Korridor einmal prüfen;
- keine serielle Einzelflickerei;
- keine alte Gesamtdatei blind reapplyen;
- kein neuer Runner/Gate/Executor/Ersatzweg;
- Produktions-PR erst nach belegter Ursache;
- danach normale `hardlock` + `hardlock-base`;
- erst nach Merge echter 7/7-Realtest;
- im Realtest keine Reparatur.

## NICHT ANFASSEN

- SEO-Maschine / 5-Felder-Handoff;
- Textmaschine;
- Fachregeln;
- Tabellen-/Linkregeln;
- LanguageTool-Regeln;
- PPM-/PSERC-/PSTE-Fachregeln;
- Design;
- Signier-/WordPress-Publish-Grenze;
- Dispatcher PR #107 mergen;
- Auto-Publish / WordPress-Write.

## AUTORITÄTEN

Stand:
`CURRENT_STATE.md`

Fehler:
`protocol/PROJECT_MEMORY/FEHLERREGISTER.md` → autoritative TEXT-Fehlerquelle

Protokoll:
`QUELLEN_AKTUELL/02_VOLLSTAENDIGES_PROTOKOLL_20260830_BIS_20260905.md`

Paul:
`PAUL_PIPELINE_AUDIT_20260906.md`

Ziel:
`protocol/PROJECT_MEMORY/ZIELVERTRAEGE/REGISTER.md` → ZV-TEXT-001 → autoritativer Zielvertrag

Warum:
`protocol/PROJECT_MEMORY/AENDERUNGSREGISTER.md`
