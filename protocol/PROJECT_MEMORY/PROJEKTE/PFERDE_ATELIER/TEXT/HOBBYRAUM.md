# TEXT – HOBBYRAUM

STAND: 2026-09-09
STATUS: **AKTIV – M26 CONTEXT MARKER PRODUCT FIX TEST**

## EINZIGE ARBEITSWAHRHEIT

Ziel:
`107008 – FINAL_NEW_ARTICLE_BATCH_REVIEW_AWAIT_USER_PUBLISH`

Current main:
`a63c20100759b4e42d07f2e70a11ee9875709d37`

Aktueller Integrationsblocker:
`M26_CURRENT_FACHWORKFLOW_CONTEXT_NOT_BOUND:reale Nicht-PPM-Stage-Artefakte`

Aktive Fehler-ID:
`M26 – Bound Fachworkflow production context`

Bekannter realer Liveblocker danach:
`M35 – PPM679_REAL_EXECUTION_FAILED:SOURCE_HASH_BINDING_MISMATCH`

## ROOT CAUSE M26

Kein funktionaler Kontextverlust.

Gegenprüfung:
- Current-Action-Selftest PASS;
- aktueller Codex ist gebundener Fachworkflow-Worker;
- Handoff-Request-Vertrag PASS;
- STEP107007 enthält bereits die gleiche Semantik als `die realen Nicht-PPM-Stage-Artefakte und Proofs`;
- Runner erwartet exakt `reale Nicht-PPM-Stage-Artefakte`.

Ursache:
reiner Wortlaut-/Markerdrift `realen` → `reale`.

## KISS-KANDIDAT

Branch:
`hobbyroom/m26-context-marker-normalization-20260909`

Head:
`b55621e556eb25ec5bee4fd9b2f9662380575398`

Scope exakt 3 Dateien:
- STEP107007: nur Markerwortlaut normalisiert;
- CURRENT_STATE.json: nur daraus folgender Bundle-SHA;
- PFERDE_ATELIER_START_HERE.json: nur daraus folgender State-SHA.

Kein Fachverhalten, kein Runner, kein Gate, kein Contract, kein Executor geändert.

## BEREITS GEPRÜFT

- main: M26 exakter vierter Marker FAIL;
- Kandidat: alle vier Kontextmarker PASS;
- Worker-Bindung unverändert PASS;
- Handoff-Request unverändert vorhanden;
- No-Publish unverändert vorhanden;
- STEP107007 → CURRENT_STATE → START_HERE Hashkette nachgezogen.

## MASCHINELLER HOBBYRAUM-LOCK

```text
HOBBYROOM_WORK_LOCK_V1
STATUS: FIX_ALLOWED_FOR_CODEX_TEST
OFFICE: TEXT
MAIN_SHA: a63c20100759b4e42d07f2e70a11ee9875709d37
ACTIVE_BLOCKER: M26_CURRENT_FACHWORKFLOW_CONTEXT_NOT_BOUND:reale Nicht-PPM-Stage-Artefakte
PLAN_PHASE: PRODUCT_FIX
RECOVERY_BASE_SHA: de21f6cd35c60849c551fd82f78e75ce57c99fab
ACTIVE_HISTORY_CASE: M26
HISTORY_EXPECTED_FAIL: M35
RECOVERY_SEQUENCE: 1_ANALYSE_FULL_BOUNDED_CORRIDOR;2_PROVE_ROOT_CAUSE;3_ONE_KISS_CANDIDATE;4_HARDLOCKS;5_REALTEST
CANDIDATE_BRANCH: hobbyroom/m26-context-marker-normalization-20260909
CANDIDATE_HEAD_SHA: b55621e556eb25ec5bee4fd9b2f9662380575398
TECHNICAL_SCOPE_PREFIXES: control/startmaster0107/STEP_107007_RUN_NEW_ARTICLE_BATCH_NO_STOP.json;control/startmaster0107/CURRENT_STATE.json;control/startmaster0107/PFERDE_ATELIER_START_HERE.json
ALLOWED_PATH_PREFIXES: control/startmaster0107/STEP_107007_RUN_NEW_ARTICLE_BATCH_NO_STOP.json;control/startmaster0107/CURRENT_STATE.json;control/startmaster0107/PFERDE_ATELIER_START_HERE.json
CHECK_PAUL: PASS
CHECK_HISTORY: PASS
CHECK_LAST_GOOD: PASS
CHECK_NEIGHBORS: PASS
CHECK_REPEAT_CLASS: PASS
CHECK_POS_NEG: PASS
CHECK_INVARIANTS: PASS
HISTORY_SOURCE_REF: control/startmaster0107/HOBBYRAUM_KNOWN_ERROR_REGRESSION_MATRIX_M01_M33_20260904.md
HISTORY_SOURCE_BLOB_SHA: a3c6a468dc1cf380c3a874ef86805d978d78e582
HISTORY_PROOF_RUNNER_REF: control/startmaster0107/HOBBYRAUM_M01_M33_REGRESSION.py
HISTORY_PROOF_RUNNER_BLOB_SHA: f7af847ed46fcae6527037eef06487b2f6d77786
PAUL_SOURCE_REF: protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/TEXT/PAUL_PIPELINE_AUDIT_20260906.md
PAUL_SOURCE_BLOB_SHA: 08fee3940a8f693ac6bb505df2e083b8515e2dd9
ERROR_SOURCE_REF: protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/TEXT/QUELLEN_AKTUELL/04_FEHLERLISTE_KOMPLETT_AKTUELL_20260905.md
ERROR_SOURCE_BLOB_SHA: 34c7eead18daa21772edd09ea73d13df6a3be78a
CURRENT_STATE_REF: protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/TEXT/CURRENT_STATE.md
CURRENT_STATE_BLOB_SHA: 2be3925b0d00971252c00be418ff626b84462b02
DECISION_SOURCE_REF: protocol/PROJECT_MEMORY/AENDERUNGSREGISTER.md
DECISION_SOURCE_BLOB_SHA: 7d8fca295939176076b8ed0dc0e5ab652f1023f5
STANDARD_SOURCE_REF: protocol/PROJECT_MEMORY/BAUCONTAINER/HOBBYRAUM_STANDARD.md
STANDARD_SOURCE_BLOB_SHA: ebc17644fa0793bace4b6c93408909df515d8792
PROTOCOL_SOURCE_REF: protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/TEXT/QUELLEN_AKTUELL/02_VOLLSTAENDIGES_PROTOKOLL_20260830_BIS_20260905.md
PROTOCOL_SOURCE_BLOB_SHA: fca477853c3aca006bcda5dc6ac80b360e27b099
INTEGRATION_ALLOWED: true
END_HOBBYROOM_WORK_LOCK_V1
```

## AKTUELLE EINZIGE NEXT ACTION

**M26-Kandidat serverseitig gegen M01–M35 prüfen.**

1. PR gegen current main.
2. `hardlock` + `hardlock-base`.
3. Vorher: current main muss exakt M26 als ersten FAIL reproduzieren.
4. Nachher: M26 muss verschwunden sein; erster späterer bekannter FAIL darf ausschließlich M35 sein.
5. Kein weiterer M26-Fix im laufenden Test.
6. Bei PASS regulär mergen.
7. Danach M35 auf fresh main neu binden.
8. Erst nach M35-Merge echter 7/7-Realtest.
9. Kein Publish.

## VERBINDLICHER ARBEITSWEG

- KISS;
- jeder Fehler gegen Historie, Paul, Gesamtworkflow und Nutzbarkeit;
- kein Sammelfix;
- keine neue Architektur;
- kein Fix auf einen fehlgeschlagenen Fix;
- Positiv/Negativ vor Integration;
- im Realtest keine Reparatur.

## NICHT ANFASSEN

- SEO-Maschine / 5-Felder-Handoff;
- Textmaschine;
- Fachregeln;
- Tabellen-/Linkregeln;
- LanguageTool-Regeln;
- PPM-/PSERC-/PSTE-Fachregeln;
- Design;
- WordPress-Publish-Grenze;
- Dispatcher PR #107 mergen;
- Auto-Publish / WordPress-Write.
