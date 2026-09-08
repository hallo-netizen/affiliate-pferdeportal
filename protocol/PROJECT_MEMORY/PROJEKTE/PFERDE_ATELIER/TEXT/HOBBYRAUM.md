# TEXT – HOBBYRAUM

STAND: 2026-09-08
STATUS: AKTIV / REPARATURKONZEPT EINGEFROREN / FIX_FORBIDDEN

## EINZIGE ARBEITSWAHRHEIT

Ziel:
`107008 – FINAL_NEW_ARTICLE_BATCH_REVIEW_AWAIT_USER_PUBLISH`

Goldmaster:
`de21f6cd35c60849c551fd82f78e75ce57c99fab`

Aktueller main:
`2f3678aa495d40e5377881a6aa3655fb60e0c12e`

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
MAIN_SHA: 2f3678aa495d40e5377881a6aa3655fb60e0c12e
ACTIVE_BLOCKER: FACHWORKFLOW_PROOF_HANDOFF_BLOCKED
PLAN_PHASE: ONE_TIME_SECURITY_MAINTENANCE_PENDING
RECOVERY_BASE_SHA: de21f6cd35c60849c551fd82f78e75ce57c99fab
HISTORY_EXPECTED_FAIL: NONE
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
HISTORY_SOURCE_REF: control/startmaster0107/HOBBYRAUM_KNOWN_ERROR_REGRESSION_MATRIX_M01_M33_20260904.md
HISTORY_SOURCE_BLOB_SHA: 9f88203bf4f97c538acf75bdecf8051df1c6b3c2
HISTORY_PROOF_RUNNER_REF: control/startmaster0107/HOBBYRAUM_M01_M33_REGRESSION.py
HISTORY_PROOF_RUNNER_BLOB_SHA: f8f85aa515bdf7a05c7e54ff7bdc03f2605b4db8
PAUL_SOURCE_REF: protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/TEXT/PAUL_PIPELINE_AUDIT_20260906.md
PAUL_SOURCE_BLOB_SHA: 08fee3940a8f693ac6bb505df2e083b8515e2dd9
ERROR_SOURCE_REF: protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/TEXT/QUELLEN_AKTUELL/04_FEHLERLISTE_KOMPLETT_AKTUELL_20260905.md
ERROR_SOURCE_BLOB_SHA: e263de9d684e16c5ca95185079cbad1dd02fb26c
CURRENT_STATE_REF: protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/TEXT/CURRENT_STATE.md
CURRENT_STATE_BLOB_SHA: 203d30c28d37708d9f75ef42519ae851d65301b3
DECISION_SOURCE_REF: protocol/PROJECT_MEMORY/AENDERUNGSREGISTER.md
DECISION_SOURCE_BLOB_SHA: 572cb8d70a3365b48d95bf7c870cfa6fe329dc80
STANDARD_SOURCE_REF: protocol/PROJECT_MEMORY/BAUCONTAINER/HOBBYRAUM_STANDARD.md
STANDARD_SOURCE_BLOB_SHA: 910582ec4f834b4dc6f28351770965cadc36d5f7
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

**Maschinenbeweis zuerst fertigstellen. Produktionsfix bleibt gesperrt.**

Neue reale Fehler müssen zuerst als ausführbare Regression separat aufgenommen und auf dem unreparierten Stand exakt FAIL reproduziert werden. Erst danach ist ein Produktionsfix zulässig.

Gebundene Evidenz: M01–M33-Matrix + vertrauenswürdiger Runner + autoritative Fehlerquelle + CURRENT_STATE + Paul-Prüfkarte + Änderungs-/Erklärungsregister + Hobbyraum-Standard. Diese Quellen werden per Git-Blob und zusätzlich semantisch geprüft.

**Einmalige Security-Aktivierung von PR #160 vorbereiten/ausführen. Danach ausschließlich M28 reparieren. Kein weiterer Architekturumbau.**

Letzter Produktions-Realtest auf main `30e933357dd9e5d3dde7cbd361c930b2a0c352c1`:
- Cloud Entry PASS;
- Production Preflight PASS;
- Runtime Entry PASS;
- Current Action READY;
- Single Door READY;
- echter `fachworkflow_proof_handoff.py materialize` wurde erreicht;
- B07/M32 ist damit real überwunden;
- neuer erster Blocker: `FACHWORKFLOW_PROOF_HANDOFF_BLOCKED`, weil die gebundene `FACHWORKFLOW_HANDOFF_REQUEST.json` fehlt.

Maschinenbeweis-Bootstrap:
- PR #159 ist gemergt;
- current main `2f3678aa495d40e5377881a6aa3655fb60e0c12e`;
- `HOBBYRAUM_M01_M33_REGRESSION.py` enthält jetzt korrigierte M26/M28/M31-Prüfungen;
- M28 besitzt einen eigenen Negativ-Mutanten-Selbsttest und erkennt fehlende Request-Erzeugung, fehlendes Request-Schema und den widersprüchlichen Satz `kein Handoff-Request`.

Serverseitige Einklinkung:
- PR #160;
- Head `3fd7d6fd27c8f2d5770f081abd44136aa5620b53`;
- exakt eine Datei: `control/paul-scope-gate/paul_scope_gate.py`;
- bindet current main, CURRENT_STATE, autoritative Fehlerquelle, Paul-Audit, M01–M33-Matrix und vertrauenswürdigen Base-Runner;
- manuelle `CHECK_*`-Felder erzeugen keine Freigabe mehr;
- kompletter vertrauenswürdiger M01–M33-Lauf muss gegen jeden Produktionskandidaten bestehen;
- Matrix/Runner dürfen nicht mit Produktionscode gemischt werden;
- Kandidat kann seinen eigenen Prüfer nicht selbst grünschreiben.

Aktueller Infrastrukturblocker:
`IMMUTABLE_SECURITY_PATH_CHANGE_BLOCKED`

Exakt:
Der bestehende `hardlock-base` blockiert jede Änderung unter `control/paul-scope-gate/` bereits vor Ausführung des geänderten Gate-Codes. Das Repository-Ruleset verlangt zugleich `hardlock` + `hardlock-base` und hat keinen Bypass-Akteur.

Nächste Prüfschwelle:
1. genau einmal kontrollierten PR-only-Admin-Wartungsweg für PR #160 öffnen;
2. exakt PR #160 / aktuellen gebundenen Head integrieren;
3. Admin-Wartungsweg sofort wieder schließen;
4. neuen Maschinenbeweis mit einem echten M28-Kandidaten verwenden;
5. danach genau ein 7/7-Realtest; erster echter Blocker wird alleinige neue Arbeitswahrheit.

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
