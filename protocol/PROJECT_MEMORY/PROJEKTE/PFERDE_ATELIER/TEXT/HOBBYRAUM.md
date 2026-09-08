# TEXT – HOBBYRAUM

STAND: 2026-09-08
STATUS: **AKTIV – M34/M35 HISTORY AUTHORITY MAINTENANCE**

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
**Fehlerklasse belegt:** Der reale PPM-6.7.9-Vertrag trennt Forschungs-/Inhalts-Fact-Pack-Hash und PPM-Registry-Hash. `production_plan_item.source_hashes` muss den nach Import von PPM gespeicherten Registry-Hash für `source_snapshot_id` enthalten. Derselbe Hindernisstangen-Fall hat historisch exakt diese Verwechslung bereits real geblockt. Der aktuelle M35-Stop liegt an derselben Vertragsgrenze.

Kein Produktionskandidat aktiv.


## HISTORY-INTEGRATIONSBLOCKER

PR #196 / Head `655f83344b6ffd33b2a4fad0aed44f780e8f8cbd` ist der einzige aktuelle History-Authority-Kandidat.

Geprüft:
- M15 aktueller Request-first-Vertrag: PASS;
- M15 Negativ Reihenfolge: BLOCK;
- M15 Negativ alter Direkt-Submit-/No-Handoff-Weg: BLOCK;
- M35 Positivmodell: PASS;
- M35 Negativ fehlende Registry-Bindung: BLOCK;
- M35 Negativ Bindung nach Planaufbau: BLOCK;
- current main unter neuer M35-Regel: exakt `M35_PPM_REGISTRY_HASH_NOT_MATERIALIZED`.

Integrationsblocker:
`hardlock-base` verlangt vor Kandidatenauswertung einen Gesamt-PASS des alten Base-Runners. Dieser alte Runner stoppt stale bei M15 auf der vor M28 geltenden No-Handoff-Regel. Kein Produkt-, Gate-, Workflow- oder PPM/PSERC-Code wird zur Umgehung verändert.

NEXT ACTION:
PR #196 einmalig als reine History-Authority-Änderung durch Repository-Admin-PR-Bypass integrieren; danach Bypass wieder entfernen und erst dann separaten M35-Produktionskandidaten erzeugen.

## MASCHINELLER HOBBYRAUM-LOCK

Der frühere TEXT-Maschinenlock ist **eingefroren und keine aktuelle Reparaturautorität**.
Normale GitHub-Schutzchecks bleiben verbindlich.

```text
HOBBYROOM_WORK_LOCK_V1
STATUS: FIX_ALLOWED_FOR_CODEX_TEST
OFFICE: TEXT
MAIN_SHA: 2325f6e18bcd8cbb491a604780ee5b65d4bbf8ea
ACTIVE_BLOCKER: PPM679_REAL_EXECUTION_FAILED:SOURCE_HASH_BINDING_MISMATCH
PLAN_PHASE: HISTORY_AUTHORITY_MAINTENANCE
RECOVERY_BASE_SHA: de21f6cd35c60849c551fd82f78e75ce57c99fab
ACTIVE_HISTORY_CASE: M35
HISTORY_EXPECTED_FAIL: M35
RECOVERY_SEQUENCE: 1_ANALYSE_FULL_BOUNDED_CORRIDOR;2_PROVE_ROOT_CAUSE;3_ONE_KISS_CANDIDATE;4_HARDLOCKS;5_REALTEST
CANDIDATE_BRANCH: hobbyroom/m34-m35-history-authority-20260908
CANDIDATE_HEAD_SHA: 655f83344b6ffd33b2a4fad0aed44f780e8f8cbd
TECHNICAL_SCOPE_PREFIXES: control/startmaster0107/HOBBYRAUM_KNOWN_ERROR_REGRESSION_MATRIX_M01_M33_20260904.md;control/startmaster0107/HOBBYRAUM_M01_M33_REGRESSION.py
ALLOWED_PATH_PREFIXES: control/startmaster0107/HOBBYRAUM_KNOWN_ERROR_REGRESSION_MATRIX_M01_M33_20260904.md;control/startmaster0107/HOBBYRAUM_M01_M33_REGRESSION.py
CHECK_PAUL: PASS
CHECK_HISTORY: PASS
CHECK_LAST_GOOD: PASS
CHECK_NEIGHBORS: PASS
CHECK_REPEAT_CLASS: PASS
CHECK_POS_NEG: PASS
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
PROTOCOL_SOURCE_BLOB_SHA: 88436a5fb717f3094688414968939b8ea25e8b93
INTEGRATION_ALLOWED: true
END_HOBBYROOM_WORK_LOCK_V1
```

## AKTUELLE EINZIGE NEXT ACTION

**History Authority zuerst. Noch keine Produktionsreparatur.**

1. Im separaten Branch `hobbyroom/m34-m35-history-authority-20260908` ausschließlich die bestehende Fehlermatrix und den bestehenden Regression-Runner lückenlos um **M34 und M35** erweitern.
2. M34 muss auf current main PASS sein.
3. M35 muss auf dem noch unreparierten current main als **erster neuer Regression-FAIL** exakt den PPM-Registry-Source-Hash-Vertragsbruch reproduzieren.
4. Positiv-/Negativ-Selbsttest der M35-Regressionslogik ausführen.
5. Keine Produktionsdatei im selben Wartungs-PR ändern.
6. Erst nach integriertem History-Beweis: genau einen KISS-Produktionskandidaten definieren; bis dahin `FIX_FORBIDDEN`.

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
