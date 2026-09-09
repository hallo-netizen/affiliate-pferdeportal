# TEXT – HOBBYRAUM

STAND: 2026-09-09
STATUS: **AKTIV – M22 H8 PROVENANCE PRODUCT FIX TEST**

## EINZIGE ARBEITSWAHRHEIT

Ziel:
`107008 – FINAL_NEW_ARTICLE_BATCH_REVIEW_AWAIT_USER_PUBLISH`

Current main:
`7531154a6218a06e49d35b78062933df3c886625`

Aktueller Integrationsblocker:
`M22_INTERNAL_SIGNATURE_STILL_REQUIRED`

Aktive Fehler-ID:
`M22 – H8 Provenance / Integrität ohne interne Signatur`

Direkter Maschinenstop danach:
`M26_CURRENT_FACHWORKFLOW_CONTEXT_NOT_BOUND:reale Nicht-PPM-Stage-Artefakte`

Bekannter realer Liveblocker danach:
`M35 – PPM679_REAL_EXECUTION_FAILED:SOURCE_HASH_BINDING_MISMATCH`

## ROOT CAUSE M22

Autoritative TECH-KEYFLOW-001/B15-Regel:
- interner 107007-/H8-Vorlauf = Hash-/Batch-/Herkunftsbindung;
- keine interne ED25519-/Signer-Pflicht;
- externe kryptografische Release-Prüfung bleibt separat erhalten.

Current main ist an dieser Stelle auf die ältere Signed-H8-Semantik zurückgerutscht.

Bewiesene Referenz:
`7990029428399e8ba01d88a6543ce068812e9218`.

## KISS-KANDIDAT

Branch:
`hobbyroom/m22-h8-provenance-no-internal-signature-20260909`

Head:
`13d76a2b22b2794827f6a277f7d85ab1566e19d3`

Scope: 6 H8-Semantik/Test-Dateien + 4 reine bestehende Hash-/Pointer-Bindungen:
- `H8_PREPRODUCTION_BOOTSTRAP_BOUNDARY.json`;
- `preproduction_provenance_guard.py`;
- `single_door_bootstrap.py`;
- `single_door_preproduction_handoff.py`;
- `project_single_door_entry_v2.py`;
- `test_h8_preproduction_bootstrap.py`.

Kein neuer Runner, Gate, Contract, Signer, Executor oder Parallelweg.

M23 bleibt getrennt:
- interne H8-Prüfung nutzt `validate_production_package_integrity()`;
- externe Release-Prüfung nutzt weiterhin `validate_production_package()` + ED25519.

M35 bleibt unverändert geparkt:
`ef2ecebeb2992013873ba72100d79ffd7c48393c`.

## BEREITS GEPRÜFT

- current main → M22 FAIL;
- Kandidat → M22 PASS;
- Signer-/Trusted-Key-Abhängigkeit aus internem H8-Pfad entfernt;
- Codex-Capsule-Weg erhalten;
- H8-Test zustandsunabhängig;
- negative Hashprüfung vorhanden;
- externe M23-Signaturprüfung erhalten;
- Boundary-Hashbindung 11/11 PASS;
- bestehende H8→STEP107007→CURRENT_STATE→START_HERE/Pointer-Hashkette nachgezogen.

## MASCHINELLER HOBBYRAUM-LOCK

```text
HOBBYROOM_WORK_LOCK_V1
STATUS: FIX_ALLOWED_FOR_CODEX_TEST
OFFICE: TEXT
MAIN_SHA: 7531154a6218a06e49d35b78062933df3c886625
ACTIVE_BLOCKER: M22_INTERNAL_SIGNATURE_STILL_REQUIRED
PLAN_PHASE: PRODUCT_FIX
RECOVERY_BASE_SHA: de21f6cd35c60849c551fd82f78e75ce57c99fab
ACTIVE_HISTORY_CASE: M22
HISTORY_EXPECTED_FAIL: M26
RECOVERY_SEQUENCE: 1_ANALYSE_FULL_BOUNDED_CORRIDOR;2_PROVE_ROOT_CAUSE;3_ONE_KISS_CANDIDATE;4_HARDLOCKS;5_REALTEST
CANDIDATE_BRANCH: hobbyroom/m22-h8-provenance-no-internal-signature-20260909
CANDIDATE_HEAD_SHA: 13d76a2b22b2794827f6a277f7d85ab1566e19d3
TECHNICAL_SCOPE_PREFIXES: control/single-door-boundary/H8_PREPRODUCTION_BOOTSTRAP_BOUNDARY.json;control/single-door-boundary/preproduction_provenance_guard.py;control/single-door-boundary/single_door_bootstrap.py;control/single-door-boundary/single_door_preproduction_handoff.py;control/single-door-boundary/project_single_door_entry_v2.py;control/single-door-boundary/test_h8_preproduction_bootstrap.py;control/startmaster0107/STEP_107007_RUN_NEW_ARTICLE_BATCH_NO_STOP.json;control/startmaster0107/CURRENT_STATE.json;control/startmaster0107/PFERDE_ATELIER_START_HERE.json;control/CURRENT_STARTMASTER.json
ALLOWED_PATH_PREFIXES: control/single-door-boundary/H8_PREPRODUCTION_BOOTSTRAP_BOUNDARY.json;control/single-door-boundary/preproduction_provenance_guard.py;control/single-door-boundary/single_door_bootstrap.py;control/single-door-boundary/single_door_preproduction_handoff.py;control/single-door-boundary/project_single_door_entry_v2.py;control/single-door-boundary/test_h8_preproduction_bootstrap.py;control/startmaster0107/STEP_107007_RUN_NEW_ARTICLE_BATCH_NO_STOP.json;control/startmaster0107/CURRENT_STATE.json;control/startmaster0107/PFERDE_ATELIER_START_HERE.json;control/CURRENT_STARTMASTER.json
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
ERROR_SOURCE_BLOB_SHA: 027e34a7ef1464dbcf3180460d89eca43b192aa4
CURRENT_STATE_REF: protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/TEXT/CURRENT_STATE.md
CURRENT_STATE_BLOB_SHA: 8ec5921bae80f4df1dc43221fb91e265b5efc6d7
DECISION_SOURCE_REF: protocol/PROJECT_MEMORY/AENDERUNGSREGISTER.md
DECISION_SOURCE_BLOB_SHA: 7d8fca295939176076b8ed0dc0e5ab652f1023f5
STANDARD_SOURCE_REF: protocol/PROJECT_MEMORY/BAUCONTAINER/HOBBYRAUM_STANDARD.md
STANDARD_SOURCE_BLOB_SHA: ebc17644fa0793bace4b6c93408909df515d8792
PROTOCOL_SOURCE_REF: protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/TEXT/QUELLEN_AKTUELL/02_VOLLSTAENDIGES_PROTOKOLL_20260830_BIS_20260905.md
PROTOCOL_SOURCE_BLOB_SHA: 8106e3357c52926c6d22ac95523f4f6eeb6ae4fa
INTEGRATION_ALLOWED: true
END_HOBBYROOM_WORK_LOCK_V1
```

## AKTUELLE EINZIGE NEXT ACTION

**M22-Kandidat serverseitig gegen M01–M35 prüfen.**

1. PR gegen current main öffnen.
2. `hardlock` + `hardlock-base`.
3. Vorher: current main muss exakt M22 als ersten FAIL reproduzieren.
4. Nachher: M22 muss verschwunden sein; erster späterer FAIL muss exakt M26 sein.
5. Kein weiterer M22-Fix im laufenden Test.
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
