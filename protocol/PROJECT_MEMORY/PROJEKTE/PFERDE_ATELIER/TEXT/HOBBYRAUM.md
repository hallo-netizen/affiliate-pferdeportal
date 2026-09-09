# TEXT – HOBBYRAUM

STAND: 2026-09-09
STATUS: **AKTIV – M17 KISS PRODUCT FIX TEST**

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
- M01–M35 bleiben die akzeptierte Historie.

## MASCHINELLER HOBBYRAUM-LOCK

Der Lock bindet ausschließlich den isolierten M35-Kandidaten an current main und die integrierte M01–M35-Historie. Normale GitHub-Schutzchecks bleiben verbindlich.

```text
HOBBYROOM_WORK_LOCK_V1
STATUS: FIX_ALLOWED_FOR_CODEX_TEST
OFFICE: TEXT
MAIN_SHA: 6e650edce60b24baf7d7feef66e60cca2817e59e
ACTIVE_BLOCKER: M17_HOST_FINALIZATION_NOT_FAIL_CLOSED
PLAN_PHASE: PRODUCT_FIX
RECOVERY_BASE_SHA: de21f6cd35c60849c551fd82f78e75ce57c99fab
ACTIVE_HISTORY_CASE: M17
HISTORY_EXPECTED_FAIL: NONE
RECOVERY_SEQUENCE: 1_ANALYSE_FULL_BOUNDED_CORRIDOR;2_PROVE_ROOT_CAUSE;3_ONE_KISS_CANDIDATE;4_HARDLOCKS;5_REALTEST
CANDIDATE_BRANCH: hobbyroom/m17-host-finalization-fail-closed-20260909
CANDIDATE_HEAD_SHA: 6dcf42daa1dfc0e7960a17da49f8ca2dfee2b5ba
TECHNICAL_SCOPE_PREFIXES: control/output-quarantine/runtime_entry_gate.py
ALLOWED_PATH_PREFIXES: control/output-quarantine/runtime_entry_gate.py
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
ERROR_SOURCE_BLOB_SHA: 5ac7af2d21ad4bb825d769ff0e7a4148cde45b92
CURRENT_STATE_REF: protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/TEXT/CURRENT_STATE.md
CURRENT_STATE_BLOB_SHA: 58014917e82ff0f63c0aeb528378a53ec03654e1
DECISION_SOURCE_REF: protocol/PROJECT_MEMORY/AENDERUNGSREGISTER.md
DECISION_SOURCE_BLOB_SHA: 34d62af8d924b7579c1d45fabec039b8e350d5b2
STANDARD_SOURCE_REF: protocol/PROJECT_MEMORY/BAUCONTAINER/HOBBYRAUM_STANDARD.md
STANDARD_SOURCE_BLOB_SHA: ebc17644fa0793bace4b6c93408909df515d8792
PROTOCOL_SOURCE_REF: protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/TEXT/QUELLEN_AKTUELL/02_VOLLSTAENDIGES_PROTOKOLL_20260830_BIS_20260905.md
PROTOCOL_SOURCE_BLOB_SHA: 8ae3424135d6b8ab81340fe26ef068a68782ecba
INTEGRATION_ALLOWED: true
END_HOBBYROOM_WORK_LOCK_V1
```

## AKTUELLE EINZIGE NEXT ACTION

**M17-Kandidat jetzt vollständig gegen M01–M35 prüfen.**

1. PR `hobbyroom/m17-host-finalization-fail-closed-20260909` gegen current main öffnen.
2. `hardlock` und `hardlock-base` müssen auf exakt Head `6dcf42daa1dfc0e7960a17da49f8ca2dfee2b5ba` laufen.
3. Trusted Runner muss current main zuerst exakt als M17 reproduzieren.
4. Derselbe Runner muss den Kandidaten M01–M35 vollständig PASS melden.
5. Kein weiterer Codefix im selben Kandidaten.
6. Repository-admin-PR-Bypass vor Produktionsmerge entfernen.
7. Erst nach regulärem M17-Merge M35 auf fresh main neu binden.

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
