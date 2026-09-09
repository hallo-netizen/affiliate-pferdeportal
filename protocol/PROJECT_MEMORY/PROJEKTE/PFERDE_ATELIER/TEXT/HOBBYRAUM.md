# TEXT – HOBBYRAUM

STAND: 2026-09-09
STATUS: **AKTIV – M16/M17 HISTORY AUTHORITY MAINTENANCE**

## EINZIGE ARBEITSWAHRHEIT

Ziel:
`107008 – FINAL_NEW_ARTICLE_BATCH_REVIEW_AWAIT_USER_PUBLISH`

Current main:
`d6de9265cddc1b2a011d707ad615c144cdd9d4ab`

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

PR #196 ist integriert. M01–M35 sind die akzeptierte Historie.
Aktuell wird ausschließlich das bestehende Runner-Orakel für M16/M17 an diese bereits dokumentierten Verträge angeglichen:
- M16 aktueller Signer-Vertrag PASS;
- M17 current main muss exakt `M17_HOST_FINALIZATION_NOT_FAIL_CLOSED` reproduzieren.

## MASCHINELLER HOBBYRAUM-LOCK

Der Lock bindet ausschließlich den isolierten M35-Kandidaten an current main und die integrierte M01–M35-Historie. Normale GitHub-Schutzchecks bleiben verbindlich.

```text
HOBBYROOM_WORK_LOCK_V1
STATUS: FIX_ALLOWED_FOR_CODEX_TEST
OFFICE: TEXT
MAIN_SHA: d6de9265cddc1b2a011d707ad615c144cdd9d4ab
ACTIVE_BLOCKER: M17_HOST_FINALIZATION_NOT_FAIL_CLOSED
PLAN_PHASE: HISTORY_AUTHORITY_MAINTENANCE
RECOVERY_BASE_SHA: de21f6cd35c60849c551fd82f78e75ce57c99fab
ACTIVE_HISTORY_CASE: M17
HISTORY_EXPECTED_FAIL: M17
RECOVERY_SEQUENCE: 1_ANALYSE_FULL_BOUNDED_CORRIDOR;2_PROVE_ROOT_CAUSE;3_ONE_KISS_CANDIDATE;4_HARDLOCKS;5_REALTEST
CANDIDATE_BRANCH: hobbyroom/m16-m17-history-authority-20260909
CANDIDATE_HEAD_SHA: 5ea8d5da54ca946dd99b3d85a2f3fb8488b7a7b8
TECHNICAL_SCOPE_PREFIXES: control/startmaster0107/HOBBYRAUM_M01_M33_REGRESSION.py
ALLOWED_PATH_PREFIXES: control/startmaster0107/HOBBYRAUM_M01_M33_REGRESSION.py
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
HISTORY_PROOF_RUNNER_BLOB_SHA: 583444719bfe8a94f2cf153cbe920c8ee11fad43
PAUL_SOURCE_REF: protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/TEXT/PAUL_PIPELINE_AUDIT_20260906.md
PAUL_SOURCE_BLOB_SHA: 08fee3940a8f693ac6bb505df2e083b8515e2dd9
ERROR_SOURCE_REF: protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/TEXT/QUELLEN_AKTUELL/04_FEHLERLISTE_KOMPLETT_AKTUELL_20260905.md
ERROR_SOURCE_BLOB_SHA: 473281fa16e2159991f8690f9d6e1757458dce45
CURRENT_STATE_REF: protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/TEXT/CURRENT_STATE.md
CURRENT_STATE_BLOB_SHA: 774a02d328bdfc7e81a850ee6e95f08874cb77d9
DECISION_SOURCE_REF: protocol/PROJECT_MEMORY/AENDERUNGSREGISTER.md
DECISION_SOURCE_BLOB_SHA: 34d62af8d924b7579c1d45fabec039b8e350d5b2
STANDARD_SOURCE_REF: protocol/PROJECT_MEMORY/BAUCONTAINER/HOBBYRAUM_STANDARD.md
STANDARD_SOURCE_BLOB_SHA: ebc17644fa0793bace4b6c93408909df515d8792
PROTOCOL_SOURCE_REF: protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/TEXT/QUELLEN_AKTUELL/02_VOLLSTAENDIGES_PROTOKOLL_20260830_BIS_20260905.md
PROTOCOL_SOURCE_BLOB_SHA: 1a268cc6fe264a786a30cd4453765cca20e2f8c2
INTEGRATION_ALLOWED: true
END_HOBBYROOM_WORK_LOCK_V1
```

## AKTUELLE EINZIGE NEXT ACTION

**M16/M17 History Authority zuerst; M35 bleibt eingefroren.**

1. Separaten History-PR `hobbyroom/m16-m17-history-authority-20260909` gegen current main öffnen.
2. M16 muss auf current main nach aktuellem Signer-Vertrag PASS sein.
3. M17 muss auf current main exakt `M17_HOST_FINALIZATION_NOT_FAIL_CLOSED` reproduzieren.
4. Kein Produktionscode im History-PR.
5. Danach separaten Ein-Datei-M17-Produktionskandidaten bauen.
6. Erst nach M17-Gesamt-PASS den unveränderten M35-Kandidaten erneut auf fresh main binden.

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
