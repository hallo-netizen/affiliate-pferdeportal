# TEXT – HOBBYRAUM

STAND: 2026-09-08
STATUS: AKTIV / REPARATURKONZEPT EINGEFROREN / FIX_ALLOWED_FOR_CODEX_TEST

## EINZIGE ARBEITSWAHRHEIT

Ziel:
`107008 – FINAL_NEW_ARTICLE_BATCH_REVIEW_AWAIT_USER_PUBLISH`

Goldmaster:
`de21f6cd35c60849c551fd82f78e75ce57c99fab`

Aktueller main:
`30e933357dd9e5d3dde7cbd361c930b2a0c352c1`

Aktueller erster echter Blocker:
`FACHWORKFLOW_PROOF_HANDOFF_BLOCKED`

Fehlerursache:
die gebundene `FACHWORKFLOW_HANDOFF_REQUEST.json` für den ersten Artikel fehlt am erwarteten Quarantine-Pfad.

B02 und B07/M32 sind im aktuellen Realtest überwunden.

## MASCHINELLER HOBBYRAUM-LOCK

```text
HOBBYROOM_WORK_LOCK_V1
STATUS: FIX_ALLOWED_FOR_CODEX_TEST
OFFICE: TEXT
MAIN_SHA: 30e933357dd9e5d3dde7cbd361c930b2a0c352c1
ACTIVE_BLOCKER: FACHWORKFLOW_PROOF_HANDOFF_BLOCKED
PLAN_PHASE: HISTORY_MACHINE_PROOF_BOOTSTRAP_BOUND
RECOVERY_BASE_SHA: de21f6cd35c60849c551fd82f78e75ce57c99fab
RECOVERY_SEQUENCE: 1_GOLDMASTER_EXACT;2_REALTEST;3_ONE_MANDATORY_DELTA;4_REALTEST;5_PASS_FREEZE_OR_FAIL_FULL_REVERT;6_REPEAT
CANDIDATE_BRANCH: hobbyroom/history-machine-proof-bootstrap-20260908
CANDIDATE_HEAD_SHA: c9644ccd0bdc2c8721acb9b13b73b534da9aa5e7
TECHNICAL_SCOPE_PREFIXES: control/startmaster0107/;control/single-door-boundary/;control/output-quarantine/;control/CURRENT_STARTMASTER.json
ALLOWED_PATH_PREFIXES: control/startmaster0107/HOBBYRAUM_M01_M33_REGRESSION.py
CHECK_PAUL: PASS
CHECK_HISTORY: PASS
CHECK_LAST_GOOD: PASS
CHECK_NEIGHBORS: PASS
CHECK_REPEAT_CLASS: PASS
CHECK_POS_NEG: PASS
CHECK_INVARIANTS: PASS
INTEGRATION_ALLOWED: true
END_HOBBYROOM_WORK_LOCK_V1
```

## EINGEFRORENER REPARATURALGORITHMUS

1. Nur den ersten realen Blocker bearbeiten.
2. Vor Kandidat: Paul-Prüfkarte, Fehlerhistorie, letzter funktionierender Stand, direkte Vor-/Nachstufe.
3. Genau eine zwingende Änderung.
4. Lokale Positiv-/Negativprüfung.
5. Echter 7/7-Realtest.
6. PASS bzw. erwartbares Weiterwandern → Zwischenstand einfrieren.
7. Regression / früherer neuer Fehler / Hardlock-FAIL → Änderung vollständig zurück.
8. Kein Fix auf einen fehlgeschlagenen Fix.
9. Kein zweiter Kandidat parallel.

## AKTUELLE EINZIGE NEXT ACTION

**Nur den Maschinenbeweis-Runner aus PR #159 integrieren. Noch keinen Produktionsfix für M28 bauen.**

Realtest-Beleg auf current main `30e933357dd9e5d3dde7cbd361c930b2a0c352c1`:
- Cloud Entry PASS;
- Production Preflight PASS;
- Runtime Entry PASS;
- Current Action READY;
- Single Door READY;
- echter `fachworkflow_proof_handoff.py materialize` wurde erreicht;
- B07/M32 ist damit real überwunden;
- neuer erster Blocker: `FACHWORKFLOW_PROOF_HANDOFF_BLOCKED`, weil die gebundene `FACHWORKFLOW_HANDOFF_REQUEST.json` fehlt.

Maschinenbeweis-Bootstrap:
- PR #159;
- Head `c9644ccd0bdc2c8721acb9b13b73b534da9aa5e7`;
- exakt eine Datei: `control/startmaster0107/HOBBYRAUM_M01_M33_REGRESSION.py`;
- M26/M28/M31 stale Prüfungen korrigiert;
- M28-Proof-Selbsttest reproduziert künstlich drei historische Fehlervarianten und blockiert sie;
- normaler `hardlock` auf dem Kandidaten PASS.

Nächste Prüfschwelle:
1. `hardlock-base` auf exakt diesem gebundenen Head PASS;
2. dann nur diesen Proof-Runner mergen;
3. anschließend Hardlock-Einklinkung des vertrauenswürdigen Base-Runners klären;
4. erst danach M28-Produktionsfix.

## VERBOTEN

- Konzeptwechsel;
- Parallelreparatur;
- Sammelfix;
- prophylaktischer LanguageTool-/SEO-/Link-/Tabellen-/Design-/Security-Fix;
- neuer Runner/Gate/Executor/Ersatzweg;
- Publish oder WordPress-Write.

## AUTORITÄTEN

Stand → `CURRENT_STATE.md`

Fehler → `protocol/PROJECT_MEMORY/FEHLERREGISTER.md` → autoritative TEXT-Fehlerquelle

Paul → `PAUL_PIPELINE_AUDIT_20260906.md`

Ziel → `protocol/PROJECT_MEMORY/ZIELVERTRAEGE/REGISTER.md`

Warum → `protocol/PROJECT_MEMORY/AENDERUNGSREGISTER.md`
