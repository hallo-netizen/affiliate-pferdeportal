# TEXT – HOBBYRAUM

STAND: 2026-09-09
STATUS: **AKTIV – M22 / SEQUENTIAL HISTORY-GATE MAINTENANCE**

## EINZIGE ARBEITSWAHRHEIT

Ziel:
`107008 – FINAL_NEW_ARTICLE_BATCH_REVIEW_AWAIT_USER_PUBLISH`

Current main:
`6e650edce60b24baf7d7feef66e60cca2817e59e`

Aktueller Integrationsblocker:
`M17_HOST_FINALIZATION_NOT_FAIL_CLOSED`

Aktueller realer Liveblocker danach:
`PPM679_REAL_EXECUTION_FAILED:SOURCE_HASH_BINDING_MISMATCH`

Aktive Fehler-ID:
`M17 – 107008 fail-closed`

Letzte real erfolgreiche Stelle:
- frischer `FACHWORKFLOW_HANDOFF_REQUEST.json` für Artikel 1;
- gebundener `fachworkflow_handoff.command`;
- echter PPM-6.7.9-Eingang;
- Stop erst bei Fact-Pack-Quellhashbindung.

Root Cause:
**Fehlerklasse belegt:** Der reale PPM-6.7.9-Vertrag trennt Forschungs-/Inhalts-Fact-Pack-Hash und PPM-Registry-Hash. `production_plan_item.source_hashes` muss den nach Import von PPM gespeicherten Registry-Hash für `source_snapshot_id` enthalten. Derselbe Hindernisstangen-Fall hat historisch exakt diese Verwechslung bereits real geblockt. Der aktuelle M35-Stop liegt an derselben Vertragsgrenze.

Geparkter M35-Produktionskandidat:
- Branch `hobbyroom/m35-ppm-registry-hash-binding-20260909`;
- Head `ef2ecebeb2992013873ba72100d79ffd7c48393c`;
- unverändert; kein weiterer M35-Fix, bis M17 PASS ist.

## HISTORY AUTHORITY

PR #198 ist integriert.
- M16 aktueller Signer-Vertrag: PASS.
- M17 current main: reproduziert `M17_HOST_FINALIZATION_NOT_FAIL_CLOSED`.
- M17-Kandidat `66e9f24…`: M17 PASS, danach erster bekannter FAIL M22.
- M22-Orakel gegen TECH-KEYFLOW-001/B15 korrigiert: current main FAIL, bewiesener Stand `799002…` PASS.
- Wartung ändert keinen Produktionscode.

## MASCHINELLER HOBBYRAUM-LOCK

Der Lock bindet ausschließlich die notwendige M22-/Sequenz-Wartung an current main. Kein Produktionscode ist in diesem Kandidaten. Normale GitHub-Schutzchecks bleiben verbindlich.

```text
HOBBYROOM_WORK_LOCK_V1
STATUS: FIX_ALLOWED_FOR_CODEX_TEST
OFFICE: TEXT
MAIN_SHA: 6e650edce60b24baf7d7feef66e60cca2817e59e
ACTIVE_BLOCKER: M17_HOST_FINALIZATION_NOT_FAIL_CLOSED
PLAN_PHASE: HISTORY_AUTHORITY_MAINTENANCE
RECOVERY_BASE_SHA: de21f6cd35c60849c551fd82f78e75ce57c99fab
ACTIVE_HISTORY_CASE: M17
HISTORY_EXPECTED_FAIL: M17
RECOVERY_SEQUENCE: 1_ANALYSE_FULL_BOUNDED_CORRIDOR;2_PROVE_ROOT_CAUSE;3_ONE_KISS_CANDIDATE;4_HARDLOCKS;5_REALTEST
CANDIDATE_BRANCH: hobbyroom/m22-sequential-history-gate-20260909
CANDIDATE_HEAD_SHA: 90eb7e897897636d51bc13e8ad590fe5d953b0c3
TECHNICAL_SCOPE_PREFIXES: control/startmaster0107/HOBBYRAUM_KNOWN_ERROR_REGRESSION_MATRIX_M01_M33_20260904.md;control/startmaster0107/HOBBYRAUM_M01_M33_REGRESSION.py;control/paul-scope-gate/paul_scope_gate.py
ALLOWED_PATH_PREFIXES: control/startmaster0107/HOBBYRAUM_KNOWN_ERROR_REGRESSION_MATRIX_M01_M33_20260904.md;control/startmaster0107/HOBBYRAUM_M01_M33_REGRESSION.py;control/paul-scope-gate/paul_scope_gate.py
CHECK_PAUL: PASS
CHECK_HISTORY: PASS
CHECK_LAST_GOOD: PASS
CHECK_NEIGHBORS: PASS
CHECK_REPEAT_CLASS: PASS
CHECK_POS_NEG: PASS
CHECK_INVARIANTS: PASS
HISTORY_SOURCE_REF: control/startmaster0107/HOBBYRAUM_KNOWN_ERROR_REGRESSION_MATRIX_M01_M33_20260904.md
HISTORY_SOURCE_BLOB_SHA: b1fc329e2c440cfaba75aef6a6206666969802d6
HISTORY_PROOF_RUNNER_REF: control/startmaster0107/HOBBYRAUM_M01_M33_REGRESSION.py
HISTORY_PROOF_RUNNER_BLOB_SHA: 1ba35cc4738d8894ad76fdf97b71cbac43c80764
PAUL_SOURCE_REF: protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/TEXT/PAUL_PIPELINE_AUDIT_20260906.md
PAUL_SOURCE_BLOB_SHA: 08fee3940a8f693ac6bb505df2e083b8515e2dd9
ERROR_SOURCE_REF: protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/TEXT/QUELLEN_AKTUELL/04_FEHLERLISTE_KOMPLETT_AKTUELL_20260905.md
ERROR_SOURCE_BLOB_SHA: b502d5ec07b4f464f3c069b20d56c0bb8cab5c47
CURRENT_STATE_REF: protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/TEXT/CURRENT_STATE.md
CURRENT_STATE_BLOB_SHA: 76b667eb3713907c95ab7f5409e4a8358962856a
DECISION_SOURCE_REF: protocol/PROJECT_MEMORY/AENDERUNGSREGISTER.md
DECISION_SOURCE_BLOB_SHA: 4e261360bb768b98a1bf58ac0c8cf153f5bec10a
STANDARD_SOURCE_REF: protocol/PROJECT_MEMORY/BAUCONTAINER/HOBBYRAUM_STANDARD.md
STANDARD_SOURCE_BLOB_SHA: ebc17644fa0793bace4b6c93408909df515d8792
PROTOCOL_SOURCE_REF: protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/TEXT/QUELLEN_AKTUELL/02_VOLLSTAENDIGES_PROTOKOLL_20260830_BIS_20260905.md
PROTOCOL_SOURCE_BLOB_SHA: 49aa11a8aed3427f2a1ff39ce3fcd48e8f20f971
INTEGRATION_ALLOWED: true
END_HOBBYROOM_WORK_LOCK_V1
```

## AKTUELLE EINZIGE NEXT ACTION

**Nur die Zwangsjacke einmal KISS korrigieren, dann sofort zurück zu M17.**

1. Wartungs-PR `hobbyroom/m22-sequential-history-gate-20260909` gegen current main öffnen.
2. Scope exakt 3 bestehende Dateien: Matrix, Runner, `paul_scope_gate.py`.
3. M22-Orakel muss current main FAIL und bewiesenen B15-Stand `799002…` PASS liefern.
4. Sequenzregel muss M17→M22/M35 erlauben, M17→M17/früher/unbekannt blockieren; ohne Folgefehler Gesamt-PASS.
5. Kein Produktionscode im Wartungs-PR.
6. Nach Integration: Bypass sofort wieder entfernen.
7. M17-Kandidat #199 auf fresh main neu binden, `HISTORY_EXPECTED_FAIL: M22`, normal hardlock/hardlock-base.
8. Nach regulärem M17-Merge wird ausschließlich M22 repariert; M35 bleibt geparkt.

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
