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
PLAN_PHASE: HISTORY_MACHINE_PROOF_HARDLOCK_INTEGRATION_BLOCKED
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

**Nur die serverseitige Einklinkung des Maschinenbeweises aus PR #160 lösen. Noch keinen M28-Produktionsfix bauen.**

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
- Head `947b56ad638c932a27cf66e77692914e83b09547`;
- exakt eine Datei: `control/paul-scope-gate/paul_scope_gate.py`;
- vorgesehen: History-Quelle + Paul-Quelle + vertrauenswürdigen Base-Runner per Git-Blob binden, Base-Runner-Selbsttest ausführen, danach denselben historischen Fall gegen den Kandidaten ausführen;
- Kandidat kann seinen eigenen Prüfer damit nicht selbst grünschreiben.

Aktueller Infrastrukturblocker:
`IMMUTABLE_SECURITY_PATH_CHANGE_BLOCKED`

Exakt:
Der bestehende `hardlock-base` blockiert jede Änderung unter `control/paul-scope-gate/` bereits vor Ausführung des geänderten Gate-Codes. Das Repository-Ruleset verlangt zugleich `hardlock` + `hardlock-base` und hat keinen Bypass-Akteur.

Nächste Prüfschwelle:
1. nur einen autorisierten Wartungsweg für genau PR #160 herstellen;
2. PR #160 unverändert integrieren und Schutz sofort wieder schließen;
3. erst danach M28-Produktionsfix bauen;
4. kein paralleler Produktionsfix.

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
