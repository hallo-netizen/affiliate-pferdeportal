# PFERDE ATELIER – TEXT – HOBBYRAUM

<!-- DERIVED_EXECUTION_SURFACE_V1 -->

> **NICHT CURRENT-AUTORITATIV.** Diese Datei ist nur die abgeleitete Ausführungsfläche für eine bereits von der zuständigen Current-Autorität freigegebene Arbeit.  
> Aktuellen Stand, Blocker und NEXT ACTION ausschließlich über `protocol/PROJECT_MEMORY/AUTORITAETSPLAN.json` aus der dort benannten Current-Autorität lesen.  
> Widerspruch oder stale Bindung = **BLOCKED**, niemals Hobbyraum gegen Current durchsetzen.

STAND: 2026-09-18
STATUS: AKTIV – PRE-CODEX FULL E2E FINALIZATION

## AKTUELLE ARBEIT

Ausschließlich den bereits funktional grünen Pre-Codex-Gesamttest integrieren und auf exaktem Main erneut beweisen.

Current technical main:
`508f9dbb3650c99e5d41dbab83086af46945e225`

Gebundener Kandidat:
- Branch: `hobbyroom/full-e2e-simulation-before-codex-20260918`
- Head: `b1c33ee8e800ccc5b542c077ffe825bd20871581`
- Acceptance: Run `35356394787` = **40/40 PASS**

Der Kandidat ändert ausschließlich:
- exakte 5-Feld-Identität vor Batch-`advance`;
- Negativtest für fehlende externe Point-0-Datei;
- simulierte echte `codex_entry.py worker-start`-Anbindung in der vorhandenen Vollstrecke;
- Testbindung der historischen M15–M38-Fehlerklassen an die heutigen System-4-Prüfer.

Keine Fachregel, kein Artikelinhalt, kein PPM-/PSERC-/PSTE-Regelwerk, kein neuer Runner/Gate/Controller und kein Publish.

## ABGELEITETE NEXT ACTION

1. Hardlock und Deterministic Entrance exakt auf dem gebundenen Kandidaten ausführen.
2. Nur bei PASS integrieren.
3. Danach vollständigen Acceptance-Lauf erneut auf dem resultierenden exakten Main ausführen.
4. Danach STOP direkt vor echtem Codex und Nutzerfreigabe abwarten.

## VERBOTEN

- echter Codex ohne ausdrückliche Nutzerfreigabe;
- Artikelproduktion vor Abschluss des exakten Main-Beweises;
- Artikel 2 vor echtem Artikel-1-PASS;
- neue Parallelroute;
- neuer Runner/Gate/Controller/Sidecar;
- Änderung von PPM/PSERC/PSTE/Textmaschine/Fachregeln;
- WordPress-Write;
- Publish.

HOBBYROOM_WORK_LOCK_V1
STATUS: FIX_ALLOWED_FOR_CODEX_TEST
OFFICE: TEXT
MAIN_SHA: 508f9dbb3650c99e5d41dbab83086af46945e225
ACTIVE_BLOCKER: PRE_CODEX_INTEGRATION_PROOF_PENDING
PLAN_PHASE: PRODUCT_FIX
RECOVERY_BASE_SHA: 508f9dbb3650c99e5d41dbab83086af46945e225
ACTIVE_HISTORY_CASE: M38
HISTORY_EXPECTED_FAIL: NONE
CANDIDATE_BRANCH: hobbyroom/full-e2e-simulation-before-codex-20260918
CANDIDATE_HEAD_SHA: b1c33ee8e800ccc5b542c077ffe825bd20871581
TECHNICAL_SCOPE_PREFIXES: control/startmaster0107/system4_107007_batch.py;isolated_system4/
ALLOWED_PATH_PREFIXES: control/startmaster0107/system4_107007_batch.py;isolated_system4/test_machine_route_lock_contract.py;isolated_system4/live_parity_v2.py;isolated_system4/test_root_entry.py;isolated_system4/test_acceptance_history_hardlock.py
CHECK_PAUL: PASS
CHECK_HISTORY: PASS
CHECK_LAST_GOOD: PASS
CHECK_NEIGHBORS: PASS
CHECK_REPEAT_CLASS: PASS
CHECK_POS_NEG: PASS
CHECK_INVARIANTS: PASS
HISTORY_SOURCE_REF: control/startmaster0107/HOBBYRAUM_KNOWN_ERROR_REGRESSION_MATRIX_M01_M33_20260904.md
HISTORY_SOURCE_BLOB_SHA: bdd041393d25f0f69a35c0e2d7a3b120b3aef178
HISTORY_PROOF_RUNNER_REF: control/startmaster0107/HOBBYRAUM_M01_M33_REGRESSION.py
HISTORY_PROOF_RUNNER_BLOB_SHA: c33a49bf1c44dd9e09c49eb8139568390317dc09
PAUL_SOURCE_REF: protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/TEXT/PAUL_PIPELINE_AUDIT_20260906.md
PAUL_SOURCE_BLOB_SHA: 08fee3940a8f693ac6bb505df2e083b8515e2dd9
ERROR_SOURCE_REF: protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/TEXT/QUELLEN_AKTUELL/04_FEHLERLISTE_KOMPLETT_AKTUELL_20260911.md
ERROR_SOURCE_BLOB_SHA: f4dc0f0554d2ddc26ec69727656cad20c66e5fb4
CURRENT_STATE_REF: protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/TEXT/CURRENT_STATE.md
CURRENT_STATE_BLOB_SHA: 4d9ae1d3f03ee9b996283e83b03e21bf6ec7fcb5
DECISION_SOURCE_REF: protocol/PROJECT_MEMORY/AENDERUNGSREGISTER.md
DECISION_SOURCE_BLOB_SHA: eefb9baa492bf510912212780face6afcf58d7aa
STANDARD_SOURCE_REF: protocol/PROJECT_MEMORY/BAUCONTAINER/HOBBYRAUM_STANDARD.md
STANDARD_SOURCE_BLOB_SHA: a1181437d8ab9e66b755d662f795417ca8127c5f
PROTOCOL_SOURCE_REF: protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/TEXT/M38_ARBEITSPROTOKOLL_20260917.md
PROTOCOL_SOURCE_BLOB_SHA: 230ec23e4d7aad60e752d5f681f4316291590b1b
INTEGRATION_ALLOWED: true
END_HOBBYROOM_WORK_LOCK_V1

## VERWEISE

- CURRENT: `CURRENT_STATE.md`
- Produktions-CURRENT: `control/startmaster0107/CURRENT_STATE.json`
- Acceptance-Run: `35356394787`
- aktueller Kandidat: `b1c33ee8e800ccc5b542c077ffe825bd20871581`
