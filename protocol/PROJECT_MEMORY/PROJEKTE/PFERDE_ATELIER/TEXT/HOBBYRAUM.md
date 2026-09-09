# TEXT – HOBBYRAUM

STAND: 2026-09-09
STATUS: **AKTIV – M36 PRODUCT FIX TEST**

## EINZIGE ARBEITSWAHRHEIT

Ziel:
`107008 – FINAL_NEW_ARTICLE_BATCH_REVIEW_AWAIT_USER_PUBLISH`

Current main:
`239a64261c1fbaf467d0adbd5a2bb1ad2139eca4`

Aktueller Realblocker:
`H8_BOOTSTRAP_PROVENANCE_BINDING_NOT_CURRENT`

Aktive Fehler-ID:
`M36 – Persisted H8 legacy-binding compatibility after provenance migration`

## PRODUKTKANDIDAT

Branch:
`hobbyroom/m36-h8-legacy-provenance-alias-20260909`

Head:
`fceee7f1959ed2597489a86161b92a024d5a30fc`

Scope:
- 1 Logikdatei;
- 5 ausschließlich bestehende Hash-/Pointer-Bindungen.

KISS:
- aktueller H8-Provenance-Vertrag bleibt Soll;
- nur alter `PFERDE_ATELIER_H8_BOOTSTRAP_SIGNED_BINDING_V1` als read-only Alias;
- alter Binding-Hash muss gültig sein;
- room/receipt/generation/batch/snapshot/manifest/origin müssen exakt aktuell sein;
- unbekannter Vertrag BLOCK;
- keine interne Signaturpflicht;
- keine Paketmutation / Neusignierung.

## BEREITS GEPRÜFT

- main hat keinen Legacy-Alias → M36 erwartbar;
- echtes persistiertes Paket stimmt in allen sieben Provenienzidentitäten;
- falsche Generation → BLOCK;
- unbekannter Vertrag → BLOCK;
- Signer-Tokens im Provenance-Guard abwesend;
- H8 file_bindings 11/11 PASS;
- H8→STEP107007→CURRENT_STATE→START_HERE/Pointer-Hashkette nachgezogen.

## MASCHINELLER HOBBYRAUM-LOCK

```text
HOBBYROOM_WORK_LOCK_V1
STATUS: FIX_ALLOWED_FOR_CODEX_TEST
OFFICE: TEXT
MAIN_SHA: 239a64261c1fbaf467d0adbd5a2bb1ad2139eca4
ACTIVE_BLOCKER: H8_BOOTSTRAP_PROVENANCE_BINDING_NOT_CURRENT
PLAN_PHASE: PRODUCT_FIX
RECOVERY_BASE_SHA: de21f6cd35c60849c551fd82f78e75ce57c99fab
ACTIVE_HISTORY_CASE: M36
HISTORY_EXPECTED_FAIL: NONE
RECOVERY_SEQUENCE: 1_REALTEST_BLOCKER;2_HISTORY_AUTHORITY;3_PRODUCT_FIX;4_HARDLOCKS;5_REALTEST
CANDIDATE_BRANCH: hobbyroom/m36-h8-legacy-provenance-alias-20260909
CANDIDATE_HEAD_SHA: fceee7f1959ed2597489a86161b92a024d5a30fc
TECHNICAL_SCOPE_PREFIXES: control/single-door-boundary/preproduction_provenance_guard.py;control/single-door-boundary/H8_PREPRODUCTION_BOOTSTRAP_BOUNDARY.json;control/startmaster0107/STEP_107007_RUN_NEW_ARTICLE_BATCH_NO_STOP.json;control/startmaster0107/CURRENT_STATE.json;control/startmaster0107/PFERDE_ATELIER_START_HERE.json;control/CURRENT_STARTMASTER.json
ALLOWED_PATH_PREFIXES: control/single-door-boundary/preproduction_provenance_guard.py;control/single-door-boundary/H8_PREPRODUCTION_BOOTSTRAP_BOUNDARY.json;control/startmaster0107/STEP_107007_RUN_NEW_ARTICLE_BATCH_NO_STOP.json;control/startmaster0107/CURRENT_STATE.json;control/startmaster0107/PFERDE_ATELIER_START_HERE.json;control/CURRENT_STARTMASTER.json
CHECK_PAUL: PASS
CHECK_HISTORY: PASS
CHECK_LAST_GOOD: PASS
CHECK_NEIGHBORS: PASS
CHECK_REPEAT_CLASS: PASS
CHECK_POS_NEG: PASS
CHECK_INVARIANTS: PASS
HISTORY_SOURCE_REF: control/startmaster0107/HOBBYRAUM_KNOWN_ERROR_REGRESSION_MATRIX_M01_M33_20260904.md
HISTORY_SOURCE_BLOB_SHA: 647732791cdf764399164b471aa7fddc262d9296
HISTORY_PROOF_RUNNER_REF: control/startmaster0107/HOBBYRAUM_M01_M33_REGRESSION.py
HISTORY_PROOF_RUNNER_BLOB_SHA: a6d42c7f355b9ad23ff435a78ff7e74aee4dc8be
PAUL_SOURCE_REF: protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/TEXT/PAUL_PIPELINE_AUDIT_20260906.md
PAUL_SOURCE_BLOB_SHA: 08fee3940a8f693ac6bb505df2e083b8515e2dd9
ERROR_SOURCE_REF: protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/TEXT/QUELLEN_AKTUELL/04_FEHLERLISTE_KOMPLETT_AKTUELL_20260905.md
ERROR_SOURCE_BLOB_SHA: d67b0b2fd2a1bac37749c3909b6873d13241c83f
CURRENT_STATE_REF: protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/TEXT/CURRENT_STATE.md
CURRENT_STATE_BLOB_SHA: 70d2757c991e5a76bc8be3ae4302a212e7d1aced
DECISION_SOURCE_REF: protocol/PROJECT_MEMORY/AENDERUNGSREGISTER.md
DECISION_SOURCE_BLOB_SHA: 3bcbc27845d29e0e238f2582e22208ef84e6f17a
STANDARD_SOURCE_REF: protocol/PROJECT_MEMORY/BAUCONTAINER/HOBBYRAUM_STANDARD.md
STANDARD_SOURCE_BLOB_SHA: ebc17644fa0793bace4b6c93408909df515d8792
PROTOCOL_SOURCE_REF: protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/TEXT/QUELLEN_AKTUELL/02_VOLLSTAENDIGES_PROTOKOLL_20260830_BIS_20260905.md
PROTOCOL_SOURCE_BLOB_SHA: 5159eddb26e5aaeb358ae37a4581b61df9ed8b37
INTEGRATION_ALLOWED: true
END_HOBBYROOM_WORK_LOCK_V1
```

## AKTUELLE EINZIGE NEXT ACTION

1. Produkt-PR öffnen.
2. hardlock + hardlock-base.
3. Current main muss exakt M36 als ersten FAIL reproduzieren.
4. Kandidat muss M01–M36 vollständig GESAMT PASS liefern.
5. Kein weiterer Fix im laufenden Test.
6. Bei PASS und leerem Bypass regulär mergen.
7. Danach Dispatcher auf fresh main.
8. Danach echten 7/7-Realtest neu starten – ohne Reparatur im Lauf.
9. Kein Publish.

## NICHT ANFASSEN

- parallele Alternative / PR #195;
- SEO-/Textmaschine;
- Fachregeln;
- PPM-/PSERC-/PSTE-Regeln;
- Design;
- WordPress;
- Dispatcher #107 mergen.
