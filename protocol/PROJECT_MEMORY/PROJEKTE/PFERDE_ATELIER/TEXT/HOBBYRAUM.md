# TEXT – HOBBYRAUM

STAND: 2026-09-08
STATUS: AKTIV / REPARATURKONZEPT EINGEFROREN / FIX_FORBIDDEN

## EINZIGE ARBEITSWAHRHEIT

Ziel:
`107008 – FINAL_NEW_ARTICLE_BATCH_REVIEW_AWAIT_USER_PUBLISH`

Goldmaster:
`de21f6cd35c60849c551fd82f78e75ce57c99fab`

Aktueller main:
`36d1ecb52cf80c91e2f30f5a1eb7ecc1f14782c9`

Aktueller erster echter Blocker:
`BOUND_REAL_PPM679_RUNTIME_PATH_NOT_EXPOSED_TO_SUBMISSION_COMMAND`

Fehlerklasse:
bestehende B07/M32-Runtime-Paket-/Pfadbindung.

B02 ist im aktuellen Realtest überwunden.

## MASCHINELLER HOBBYRAUM-LOCK

```text
HOBBYROOM_WORK_LOCK_V1
STATUS: FIX_FORBIDDEN
OFFICE: TEXT
MAIN_SHA: 36d1ecb52cf80c91e2f30f5a1eb7ecc1f14782c9
ACTIVE_BLOCKER: BOUND_REAL_PPM679_RUNTIME_PATH_NOT_EXPOSED_TO_SUBMISSION_COMMAND
PLAN_PHASE: B07_M32_ANALYZE_ONLY
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
CHECK_REPEAT_CLASS: PASS
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

**Nur B07/M32 analysieren. Noch keinen Fix bauen.**

Konkret zu klären:
- wo der historisch funktionierende reale PPM-6.7.9-/PSERC-Runtime-Pfad gebunden war;
- warum der aktuelle `fachworkflow_handoff.command` `PPM679_PACKAGE_ZIP` und `PSERC_FIX_ZIP` nicht exponiert;
- Paul-Punkte für genau diesen Korridor;
- letzter funktionierender Stand und direkte Vor-/Nachstufe.

Erst wenn alle Pflichtchecks PASS sind, darf genau ein Kandidat gebunden werden.

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
