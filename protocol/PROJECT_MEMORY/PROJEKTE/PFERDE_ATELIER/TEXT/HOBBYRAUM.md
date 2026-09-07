# TEXT – HOBBYRAUM

STAND: 2026-09-07
STATUS: AKTIV / REPARATURKONZEPT EINGEFROREN / FIX_FORBIDDEN

## EINZIGE ARBEITSWAHRHEIT

Ziel:
Den bewiesenen Produktionsstand `de21f6cd35c60849c551fd82f78e75ce57c99fab` reproduzierbar wiederherstellen und danach ausschließlich zwingende spätere Änderungen **einzeln** aufbauen.

Es gibt **kein alternatives Reparaturkonzept** und keinen parallelen Reparaturpfad.

## MASCHINELLER HOBBYRAUM-LOCK

```text
HOBBYROOM_WORK_LOCK_V1
STATUS: FIX_FORBIDDEN
OFFICE: TEXT
MAIN_SHA: 72dc4ad3d6898b23f1a7dda24427eef8a06fe2c5
ACTIVE_BLOCKER: BASELINE_REALTEST_PENDING
PLAN_PHASE: FROZEN_GOLDMASTER_BASELINE_REALTEST
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

## HARD RULE – EINGEFROREN

Diese Reihenfolge darf **nicht** geändert, erweitert, parallelisiert oder durch einen anderen Reparaturansatz ersetzt werden:

1. Goldmaster `de21f6…` als technische Funktionsreferenz.
2. Unveränderten Goldmaster-Motor real testen.
3. Erst nach ausgewertetem Realtest genau **eine** zwingend notwendige spätere Änderung auswählen.
4. Vor dem Einbau genau für diesen Korridor prüfen:
   - Pauls technische Prüfkarte;
   - Fehlerhistorie;
   - letzter funktionierender Stand;
   - direkte Vor-/Nachstufe.
5. Genau **eine** Änderung bauen.
6. Lokale Positiv-/Negativprüfung.
7. Echter 7/7-Realtest.
8. Ergebnis:
   - **PASS:** Änderung wird Bestandteil des neuen eingefrorenen Zwischenstands.
   - **FAIL:** genau diese Änderung vollständig zurückbauen. Kein Fix auf den fehlgeschlagenen Fix.
9. Erst danach nächste zwingende Änderung.
10. Wiederholen bis Ziel `107008 – FINAL_NEW_ARTICLE_BATCH_REVIEW_AWAIT_USER_PUBLISH`.

## VERBOTEN

- Konzeptwechsel während der Reparatur.
- Sammelfix.
- Zwei Änderungen zwischen zwei Realtests.
- Zweiter Fix auf einen fehlgeschlagenen Kandidaten.
- Prophylaktische Reparatur eines noch nicht real aufgetretenen Fehlers.
- LanguageTool-/PPM-/SEO-/Link-/Tabellen-/Design-/Security-Umbau außerhalb des gerade gebundenen Einzelkandidaten.
- neuer Runner, Gate, Executor oder Ersatzweg.
- Parallelbranch für einen anderen Reparaturansatz.
- Publish oder WordPress-Schreibvorgang.
- Änderung des Zielvertrags während der Reparatur.

## PAUL – VERBINDLICHE PRÜFLINSE, KEIN SAMMELFIX

Quelle:
`PAUL_PIPELINE_AUDIT_20260906.md`

Pauls Liste wird **vor jedem Einzelkandidaten** für den betroffenen Korridor geprüft.

Klassifikation eines Paul-Punkts:
1. bereits historisch behoben;
2. alt und nicht kausal;
3. erst durch spätere Pflichtänderung neu wirksam;
4. neuer reproduzierbarer Vertragskonflikt.

Nur Klasse 3 oder 4 darf nach einem **realen** passenden Fehler Reparaturkandidat werden.

Insbesondere:
- kein 41-Punkte-Sammelfix;
- kein Vorab-Fix von F2/A6/A12, F7/A7 oder A11 ohne realen passenden Fehler;
- der erste reale Fehler entscheidet.

## ZWINGENDE SPÄTERE ANFORDERUNGEN

Nach bestandenem Goldmaster-Baseline-Test werden nur Anforderungen aus dem gültigen Zielvertrag wieder eingeführt, einzeln und mit Realtest. Dazu gehören insbesondere:
- echter PPM-6.7.9-Lauf statt Selbstbehauptung;
- PPM-`content_hash == final_article_sha256`;
- korrekte Reihenfolge Fachoutput → realer PPM → erst danach PASS/Receipt;
- exakte PPM-/PSERC-Paket- und Hashbindung;
- SEO-Handoff exakt 5 Felder;
- kein Auto-Publish / kein WordPress-Schreiben im Test;
- bestehende Qualitätsregeln bleiben unverändert.

Die konkrete Reihenfolge der späteren Änderungen wird **nicht frei erfunden**, sondern aus Zielvertrag + Commit-/Fehlerhistorie bestimmt. Zwischen zwei Änderungen liegt immer ein echter Realtest.

## AKTUELLER STAND

Current main:
`72dc4ad3d6898b23f1a7dda24427eef8a06fe2c5`

Goldmaster-Motor auf current main hart geprüft:
- `.github/workflows/pferde-atelier-deterministic-entrance-gate.yml` = bytegleich `de21f6…`
- `control/cloud-entry-gate/cloud_entry.py` = bytegleich `de21f6…`
- `control/cloud-entry-gate/cloud_repo_ci_test.py` = bytegleich `de21f6…`

Ruleset:
- `hardlock` Pflicht
- `hardlock-base` Pflicht

Aktuelle einzige NEXT ACTION:
**Laufenden Goldmaster-Baseline-7/7-Realtest auswerten. Bis zum Ergebnis: FIX_FORBIDDEN, keine Reparatur.**

## AUTORITÄTEN

Stand → `CURRENT_STATE.md`  
Fehler → `protocol/PROJECT_MEMORY/FEHLERREGISTER.md` → Originalquelle  
Ziel → `protocol/PROJECT_MEMORY/ZIELVERTRAEGE/REGISTER.md`  
Paul → `PAUL_PIPELINE_AUDIT_20260906.md`  
Warum/Änderungen → `protocol/PROJECT_MEMORY/AENDERUNGSREGISTER.md`
