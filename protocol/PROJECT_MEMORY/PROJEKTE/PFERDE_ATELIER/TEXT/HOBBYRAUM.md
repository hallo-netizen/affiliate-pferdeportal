# TEXT – HOBBYRAUM

STAND: 2026-09-08
STATUS: AKTIV / REPARATURKONZEPT EINGEFROREN / FIX_FORBIDDEN

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
STATUS: FIX_FORBIDDEN
OFFICE: TEXT
MAIN_SHA: 30e933357dd9e5d3dde7cbd361c930b2a0c352c1
ACTIVE_BLOCKER: FACHWORKFLOW_PROOF_HANDOFF_BLOCKED
PLAN_PHASE: HANDOFF_REQUEST_MISSING_ANALYZE_ONLY
RECOVERY_BASE_SHA: de21f6cd35c60849c551fd82f78e75ce57c99fab
RECOVERY_SEQUENCE: 1_GOLDMASTER_EXACT;2_REALTEST;3_ONE_MANDATORY_DELTA;4_REALTEST;5_PASS_FREEZE_OR_FAIL_FULL_REVERT;6_REPEAT
CANDIDATE_BRANCH: NONE
CANDIDATE_HEAD_SHA: NONE
TECHNICAL_SCOPE_PREFIXES: control/startmaster0107/;control/single-door-boundary/;control/output-quarantine/;control/CURRENT_STARTMASTER.json
ALLOWED_PATH_PREFIXES: NONE
CHECK_PAUL: PENDING
CHECK_HISTORY: PENDING
CHECK_LAST_GOOD: PENDING
CHECK_NEIGHBORS: PENDING
CHECK_REPEAT_CLASS: PENDING
CHECK_POS_NEG: PENDING
CHECK_INVARIANTS: PENDING
INTEGRATION_ALLOWED: false
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

**Nur `FACHWORKFLOW_PROOF_HANDOFF_BLOCKED` / fehlende `FACHWORKFLOW_HANDOFF_REQUEST.json` analysieren. Noch keinen Fix bauen.**

Realtest-Beleg auf current main `30e933357dd9e5d3dde7cbd361c930b2a0c352c1`:
- Cloud Entry PASS;
- Production Preflight PASS;
- Runtime Entry PASS;
- Current Action READY;
- Single Door READY;
- echter `fachworkflow_proof_handoff.py materialize` wurde erreicht;
- B07/M32 ist damit real überwunden;
- neuer erster Blocker: `FACHWORKFLOW_PROOF_HANDOFF_BLOCKED`, weil die gebundene `FACHWORKFLOW_HANDOFF_REQUEST.json` fehlt.

Nächste Prüfschwelle:
1. nur Historie/Paul/letzten funktionierenden Stand/direkte Vor- und Nachstufe für diesen neuen Blocker prüfen;
2. keine Codeänderung während der Analyse;
3. erst nach vollständigem Pflichtcheck genau einen KISS-Kandidaten binden.

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
