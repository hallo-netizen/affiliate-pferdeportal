# PFERDE ATELIER – TEXT – HOBBYRAUM

STAND: 2026-09-17
STATUS: AKTIV – M20 1..N CLEANUP + M38 HISTORY_AUTHORITY_MAINTENANCE

## AKTUELLE ARBEIT

Nur History-Phase des vorhandenen Maschinenwegs:
- den veralteten M20-Festvertrag `7 Artikel` auf die bereits integrierte 1..N-Mengenwahrheit korrigieren;
- M38 als reale fortlaufende History-Regression im selben bestehenden Matrix-/Runner-Kandidaten erhalten und maschinell beweisen.

Aktueller technischer Main/Baseline:
`54f0ee4efb91a50bbe05b5aafa4183cc1f526565`

Aktiver realer Blocker:
`PPM679_REAL_EXECUTION_BLOCKED:PSERC_BRIDGE_PPM_PLAN_VERSION_MISMATCH`

History-Kandidat:
- PR280;
- Branch: `hobbyroom/m20-history-1n-20260917`;
- Head: `bf194a887871021e5e7b5dfdd76ecf4abd1ad3ac`;
- erlaubt: ausschließlich bestehende Fehlermatrix + bestehender Regressionrunner;
- erwartet: unveränderter Main M01–M37 PASS; Kandidat M01–M37 PASS mit M20=1..N; danach erster neuer FAIL exakt M38;
- ausdrücklich kein Produktfix in dieser Phase.

Der Main enthält vorübergehend ausschließlich den nicht-ausführbaren Migrationstoken `EXACTLY_SEVEN_ARTICLES_REQUIRED`, damit der bisherige M20-Basistest während der kontrollierten History-Migration noch lesbar bleibt. Dieser Token ist keine Mengenlogik und wird unmittelbar nach Integration des korrigierten M20-Historyvertrags entfernt.

Die M38-Versionswerte sind gegen die vorhandene Abschlusslogik gebunden:
- `plan_contract_version == "4.0.0"`;
- `required_plugin_version == "6.7.9"`.

## NEXT ACTION

Bestehenden History-Maschinenbeweis / hardlock auf PR280 ausführen.
Nur bei `HOBBYROOM_HISTORY_MACHINE_PROOF_PASS:M38` plus zugehörigem Hardlock-PASS darf dieser History-Kandidat integriert werden.
Danach den temporären M20-Migrationstoken sofort entfernen; erst anschließend Phase 2 PRODUCT_FIX M38.

Kein Codex-Testlauf. Für diese Arbeit ausschließlich bestehende GitHub-Actions-Maschinenprüfungen verwenden.

## VERBOTEN

- History-Autorität und Produktfix in einem Kandidaten mischen;
- neuer Runner/Gate/Controller/Sidecar;
- PPM/PSERC/PSTE/Textmaschine/Fachregeln/Recherche/SEO/Links/Tabellen/Design verändern;
- geschützte `ENDSTEMPEL_*`-Dateien umgehen oder ändern;
- WordPress-Write;
- Publish.

HOBBYROOM_WORK_LOCK_V1
STATUS: FIX_ALLOWED_FOR_CODEX_TEST
OFFICE: TEXT
MAIN_SHA: 54f0ee4efb91a50bbe05b5aafa4183cc1f526565
ACTIVE_BLOCKER: PPM679_REAL_EXECUTION_BLOCKED
PLAN_PHASE: HISTORY_AUTHORITY_MAINTENANCE
RECOVERY_BASE_SHA: bb005a5324a0a6270aacb52b5927613bde1ab4bc
ACTIVE_HISTORY_CASE: M38
HISTORY_EXPECTED_FAIL: M38
CANDIDATE_BRANCH: hobbyroom/m20-history-1n-20260917
CANDIDATE_HEAD_SHA: bf194a887871021e5e7b5dfdd76ecf4abd1ad3ac
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
HISTORY_SOURCE_BLOB_SHA: dbc77c1eb820bdc91918b81d290fc46016faecf6
HISTORY_PROOF_RUNNER_REF: control/startmaster0107/HOBBYRAUM_M01_M33_REGRESSION.py
HISTORY_PROOF_RUNNER_BLOB_SHA: ee1701de79a577c611c0e55a5b76fe6d7837441a
PAUL_SOURCE_REF: protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/TEXT/PAUL_PIPELINE_AUDIT_20260906.md
PAUL_SOURCE_BLOB_SHA: 08fee3940a8f693ac6bb505df2e083b8515e2dd9
ERROR_SOURCE_REF: protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/TEXT/QUELLEN_AKTUELL/04_FEHLERLISTE_KOMPLETT_AKTUELL_20260911.md
ERROR_SOURCE_BLOB_SHA: f4dc0f0554d2ddc26ec69727656cad20c66e5fb4
CURRENT_STATE_REF: protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/TEXT/CURRENT_STATE.md
CURRENT_STATE_BLOB_SHA: 9eae2aa21f54e3764d5f31e4807aa3418d3d9ccc
DECISION_SOURCE_REF: protocol/PROJECT_MEMORY/AENDERUNGSREGISTER.md
DECISION_SOURCE_BLOB_SHA: 33b1191632a86a613cd4023c90deb257bb99e6ec
STANDARD_SOURCE_REF: protocol/PROJECT_MEMORY/BAUCONTAINER/HOBBYRAUM_STANDARD.md
STANDARD_SOURCE_BLOB_SHA: 8c90de4920ec81e10f3952bbd52208fad5a42367
PROTOCOL_SOURCE_REF: protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/TEXT/M38_ARBEITSPROTOKOLL_20260917.md
PROTOCOL_SOURCE_BLOB_SHA: 37956ecdeddea39c9dbc67eab49cb7a2a9bcc5fc
INTEGRATION_ALLOWED: true
END_HOBBYROOM_WORK_LOCK_V1

## VERWEISE

- CURRENT: `CURRENT_STATE.md` (Campus-Textstand; Produktions-`control/.../CURRENT_STATE.json` nicht manuell verändert)
- aktuelle Fehlerquelle: `QUELLEN_AKTUELL/04_FEHLERLISTE_KOMPLETT_AKTUELL_20260911.md`
- M38-Protokoll: `M38_ARBEITSPROTOKOLL_20260917.md`
- Standard: `protocol/PROJECT_MEMORY/BAUCONTAINER/HOBBYRAUM_STANDARD.md`
