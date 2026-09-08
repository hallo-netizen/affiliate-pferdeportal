# TEXT – HOBBYRAUM

STAND: 2026-09-08
STATUS: AKTIV / REPARATURKONZEPT EINGEFROREN / REALTEST_ONLY

## EINZIGE ARBEITSWAHRHEIT

Ziel:
`107008 – FINAL_NEW_ARTICLE_BATCH_REVIEW_AWAIT_USER_PUBLISH`

Goldmaster:
`de21f6cd35c60849c551fd82f78e75ce57c99fab`

Aktueller main:
`30e933357dd9e5d3dde7cbd361c930b2a0c352c1`

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
MAIN_SHA: 30e933357dd9e5d3dde7cbd361c930b2a0c352c1
ACTIVE_BLOCKER: BOUND_REAL_PPM679_RUNTIME_PATH_NOT_EXPOSED_TO_SUBMISSION_COMMAND
PLAN_PHASE: B07_M32_REALTEST_ONLY
RECOVERY_BASE_SHA: de21f6cd35c60849c551fd82f78e75ce57c99fab
RECOVERY_SEQUENCE: 1_GOLDMASTER_EXACT;2_REALTEST;3_ONE_MANDATORY_DELTA;4_REALTEST;5_PASS_FREEZE_OR_FAIL_FULL_REVERT;6_REPEAT
CANDIDATE_BRANCH: NONE
CANDIDATE_HEAD_SHA: NONE
TECHNICAL_SCOPE_PREFIXES: control/startmaster0107/;control/single-door-boundary/;control/output-quarantine/;control/CURRENT_STARTMASTER.json
ALLOWED_PATH_PREFIXES: NONE
CHECK_PAUL: PASS
CHECK_HISTORY: PASS
CHECK_LAST_GOOD: PASS
CHECK_NEIGHBORS: PASS
CHECK_REPEAT_CLASS: PASS
CHECK_POS_NEG: PASS
CHECK_INVARIANTS: PASS
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

**Nur echten 7/7-Realtest auf current main `30e93335…` ausführen. Kein weiterer Fix.**

Merge-Beleg:
- PR #158;
- Merge `30e933357dd9e5d3dde7cbd361c930b2a0c352c1`;
- vor Merge `hardlock` PASS + `hardlock-base` PASS.

Nächste Prüfschwelle:
1. exakt derselbe echte 7/7-Realtest auf current main;
2. B07/M32 muss real überwunden sein oder der Kandidat gilt nicht als PASS;
3. beim ersten echten Blocker STOP;
4. keine Reparatur im laufenden Test.

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
