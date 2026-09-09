# TEXT – HOBBYRAUM

STAND: 2026-09-09
STATUS: **AKTIV – M17 PRODUCT FIX TEST**

## EINZIGE ARBEITSWAHRHEIT

Ziel:
`107008 – FINAL_NEW_ARTICLE_BATCH_REVIEW_AWAIT_USER_PUBLISH`

Current main:
`462a67b4d25c6d1d7bf4cc1f010116c0017f7da6`

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

PR #200 ist integriert.
- M16 aktueller Signer-Vertrag: PASS.
- M17 current main reproduziert `M17_HOST_FINALIZATION_NOT_FAIL_CLOSED`.
- M17-Kandidat #199 / `45b3186…`: derselbe bewiesene Fix auf fresh main.
- M22-Orakel ist jetzt autoritativ: current main FAIL `M22_INTERNAL_SIGNATURE_STILL_REQUIRED`, bewiesener B15-Stand `799002…` PASS.
- Sequenzregel: M17 muss verschwinden; exakt M22 darf danach erster bekannter FAIL sein.

## MASCHINELLER HOBBYRAUM-LOCK

Der Lock bindet ausschließlich den isolierten M17-Kandidaten an fresh main und den bereits bekannten nächsten Fehler M22. Normale GitHub-Schutzchecks bleiben verbindlich.

```text
HOBBYROOM_WORK_LOCK_V1
STATUS: FIX_ALLOWED_FOR_CODEX_TEST
OFFICE: TEXT
MAIN_SHA: 462a67b4d25c6d1d7bf4cc1f010116c0017f7da6
ACTIVE_BLOCKER: M17_HOST_FINALIZATION_NOT_FAIL_CLOSED
PLAN_PHASE: PRODUCT_FIX
RECOVERY_BASE_SHA: de21f6cd35c60849c551fd82f78e75ce57c99fab
ACTIVE_HISTORY_CASE: M17
HISTORY_EXPECTED_FAIL: M22
RECOVERY_SEQUENCE: 1_ANALYSE_FULL_BOUNDED_CORRIDOR;2_PROVE_ROOT_CAUSE;3_ONE_KISS_CANDIDATE;4_HARDLOCKS;5_REALTEST
CANDIDATE_BRANCH: hobbyroom/m17-host-finalization-fail-closed-20260909
CANDIDATE_HEAD_SHA: 45b318673856ff45f42b292c04f56f06ddf76ab1
TECHNICAL_SCOPE_PREFIXES: control/output-quarantine/runtime_entry_gate.py;control/startmaster0107/STEP_107008_FINAL_NEW_ARTICLE_BATCH_REVIEW_AWAIT_USER_PUBLISH.json;control/startmaster0107/STEP_107007_RUN_NEW_ARTICLE_BATCH_NO_STOP.json;control/startmaster0107/CURRENT_STATE.json;control/startmaster0107/PFERDE_ATELIER_START_HERE.json;control/CURRENT_STARTMASTER.json
ALLOWED_PATH_PREFIXES: control/output-quarantine/runtime_entry_gate.py;control/startmaster0107/STEP_107008_FINAL_NEW_ARTICLE_BATCH_REVIEW_AWAIT_USER_PUBLISH.json;control/startmaster0107/STEP_107007_RUN_NEW_ARTICLE_BATCH_NO_STOP.json;control/startmaster0107/CURRENT_STATE.json;control/startmaster0107/PFERDE_ATELIER_START_HERE.json;control/CURRENT_STARTMASTER.json
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
ERROR_SOURCE_BLOB_SHA: e863891c7a510ad8af36ba011b3785456a647a5e
CURRENT_STATE_REF: protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/TEXT/CURRENT_STATE.md
CURRENT_STATE_BLOB_SHA: 9357fc9081ca0d860f500713857af86fb82a7e9a
DECISION_SOURCE_REF: protocol/PROJECT_MEMORY/AENDERUNGSREGISTER.md
DECISION_SOURCE_BLOB_SHA: 7d8fca295939176076b8ed0dc0e5ab652f1023f5
STANDARD_SOURCE_REF: protocol/PROJECT_MEMORY/BAUCONTAINER/HOBBYRAUM_STANDARD.md
STANDARD_SOURCE_BLOB_SHA: ebc17644fa0793bace4b6c93408909df515d8792
PROTOCOL_SOURCE_REF: protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/TEXT/QUELLEN_AKTUELL/02_VOLLSTAENDIGES_PROTOKOLL_20260830_BIS_20260905.md
PROTOCOL_SOURCE_BLOB_SHA: ecd9289dba4c922d24f16e12345eb634c144d567
INTEGRATION_ALLOWED: true
END_HOBBYROOM_WORK_LOCK_V1
```

## AKTUELLE EINZIGE NEXT ACTION

**M17 #199 jetzt gegen fresh main und den gebundenen nächsten Fehler M22 prüfen.**

1. `hardlock` + `hardlock-base` auf Head `45b318673856ff45f42b292c04f56f06ddf76ab1`.
2. Vorher: current main muss exakt M17 als ersten FAIL reproduzieren.
3. Nachher: M17 muss verschwunden sein; exakt M22 darf als neuer erster bekannter FAIL erscheinen.
4. Kein weiterer M17-Codefix.
5. Produktionsmerge erst, wenn der temporäre Repository-admin-Bypass wieder entfernt ist.
6. Nach regulärem M17-Merge ausschließlich M22 reparieren.
7. M35 bleibt separat geparkt.

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
