# TEXT – HOBBYRAUM

STAND: 2026-09-09
STATUS: **AKTIV – M35 FINAL KNOWN PRODUCT FIX TEST**

## EINZIGE ARBEITSWAHRHEIT

Ziel:
`107008 – FINAL_NEW_ARTICLE_BATCH_REVIEW_AWAIT_USER_PUBLISH`

Current main:
`d32e16cdf6b45ffa282e42fa78e07da84863e362`

Aktueller Integrations-/Realblocker:
`PPM679_REAL_EXECUTION_FAILED:SOURCE_HASH_BINDING_MISMATCH`

Aktive Fehler-ID:
`M35 – Fact-Pack source-hash binding parity`

M17, M22 und M26:
**integriert behoben**.

## ROOT CAUSE M35

Der echte PPM-6.7.9-Vertrag besitzt nach Fact-Pack-Import einen eigenen Registry-Hash.

Fehler:
- Research-/Content-Fact-Pack-Hash und PPM-Registry-Hash wurden gleichgesetzt;
- `production_plan_item.source_hashes` trägt vor dem PPM-Import den Research-/Content-Hash;
- der interne PPM-Plan muss nach Import den von `PPM679_Storage::fact_pack_hash(...)` gelieferten Registry-Hash verwenden.

## KISS-KANDIDAT

PR:
`#197 – M35: bind internal PPM plan to registry fact-pack hash`

Branch:
`hobbyroom/m35-ppm-registry-hash-binding-20260909`

Fresh Head:
`a611a5c150cc3d8f182ca9c1855339fb98fea0c2`

Scope exakt:
`control/startmaster0107/fachworkflow_proof_handoff.py`

Änderung:
- leerer Registry-Hash bleibt BLOCK;
- `$item['source_hashes']=[$expectedSource];`;
- erst danach PPM-Planaufbau.

Nicht geändert:
- Research-/Content-Evidence;
- SEO 5-Felder;
- Textmaschine;
- Fachregeln;
- LanguageTool;
- PPM-/PSERC-/PSTE-Regeln;
- Design;
- Publish.

## BEREITS GEPRÜFT

- M34 PASS;
- M35 positiv PASS;
- fehlende Registry-Bindung BLOCK;
- Registry-Bindung nach Planaufbau BLOCK;
- current main enthält den Fehler weiterhin;
- fresh Kandidat enthält exakt den bereits bewiesenen M35-Dateistand.

## MASCHINELLER HOBBYRAUM-LOCK

```text
HOBBYROOM_WORK_LOCK_V1
STATUS: FIX_ALLOWED_FOR_CODEX_TEST
OFFICE: TEXT
MAIN_SHA: d32e16cdf6b45ffa282e42fa78e07da84863e362
ACTIVE_BLOCKER: PPM679_REAL_EXECUTION_FAILED:SOURCE_HASH_BINDING_MISMATCH
PLAN_PHASE: PRODUCT_FIX
RECOVERY_BASE_SHA: de21f6cd35c60849c551fd82f78e75ce57c99fab
ACTIVE_HISTORY_CASE: M35
HISTORY_EXPECTED_FAIL: NONE
RECOVERY_SEQUENCE: 1_ANALYSE_FULL_BOUNDED_CORRIDOR;2_PROVE_ROOT_CAUSE;3_ONE_KISS_CANDIDATE;4_HARDLOCKS;5_REALTEST
CANDIDATE_BRANCH: hobbyroom/m35-ppm-registry-hash-binding-20260909
CANDIDATE_HEAD_SHA: a611a5c150cc3d8f182ca9c1855339fb98fea0c2
TECHNICAL_SCOPE_PREFIXES: control/startmaster0107/fachworkflow_proof_handoff.py
ALLOWED_PATH_PREFIXES: control/startmaster0107/fachworkflow_proof_handoff.py
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
ERROR_SOURCE_BLOB_SHA: e327a9561e65c13262f992651852a029a217242e
CURRENT_STATE_REF: protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/TEXT/CURRENT_STATE.md
CURRENT_STATE_BLOB_SHA: ee987a364f3e2a79c9e8931a30d5a3453315d6ab
DECISION_SOURCE_REF: protocol/PROJECT_MEMORY/AENDERUNGSREGISTER.md
DECISION_SOURCE_BLOB_SHA: 7d8fca295939176076b8ed0dc0e5ab652f1023f5
STANDARD_SOURCE_REF: protocol/PROJECT_MEMORY/BAUCONTAINER/HOBBYRAUM_STANDARD.md
STANDARD_SOURCE_BLOB_SHA: ebc17644fa0793bace4b6c93408909df515d8792
PROTOCOL_SOURCE_REF: protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/TEXT/QUELLEN_AKTUELL/02_VOLLSTAENDIGES_PROTOKOLL_20260830_BIS_20260905.md
PROTOCOL_SOURCE_BLOB_SHA: ec52624d8b91e707d8887f54f5d4109dc1904ece
INTEGRATION_ALLOWED: true
END_HOBBYROOM_WORK_LOCK_V1
```

## AKTUELLE EINZIGE NEXT ACTION

**M35-Kandidat vollständig gegen M01–M35 prüfen.**

1. `hardlock` + `hardlock-base` auf Head `a611a5c150cc3d8f182ca9c1855339fb98fea0c2`.
2. Current main muss exakt M35 als ersten FAIL reproduzieren.
3. Kandidat muss M01–M35 vollständig `GESAMT PASS` liefern.
4. Kein weiterer Fix im laufenden Test.
5. Ruleset-Bypass muss vor Merge leer sein.
6. Bei PASS PR #197 regulär mergen.
7. Danach Dispatcher #107 auf fresh main synchronisieren.
8. Danach echter 7/7-Realtest auf main – ohne Reparatur im Lauf.
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

- parallele Alternative / PR #195;
- SEO-Maschine / 5-Felder-Handoff;
- Textmaschine;
- Fachregeln;
- Tabellen-/Link-/LanguageTool-Regeln;
- PPM-/PSERC-/PSTE-Fachregeln;
- Design;
- WordPress-Publish-Grenze;
- Dispatcher PR #107 mergen;
- Auto-Publish / WordPress-Write.
