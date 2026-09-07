# TEXT – HOBBYRAUM

STAND: 2026-09-07
STATUS: AKTIV / REPARATURKONZEPT EINGEFROREN / STEP04 FREIGEGEBEN

## EINZIGE ARBEITSWAHRHEIT

Ziel:
Den bewiesenen Produktionsstand `de21f6cd35c60849c551fd82f78e75ce57c99fab` reproduzierbar wiederherstellen und danach ausschließlich zwingende spätere Änderungen **einzeln** aufbauen.

Es gibt **kein alternatives Reparaturkonzept** und keinen parallelen Reparaturpfad.

## MASCHINELLER HOBBYRAUM-LOCK

```text
HOBBYROOM_WORK_LOCK_V1
STATUS: FIX_ALLOWED_FOR_CODEX_TEST
OFFICE: TEXT
MAIN_SHA: a9cde12a7d82ada06e88235f0ae7e774a013ac93
ACTIVE_BLOCKER: BOUND_REAL_PPM679_EXECUTION_ACTION_MISSING
PLAN_PHASE: STEP04_REAPPLY_PR126
RECOVERY_BASE_SHA: de21f6cd35c60849c551fd82f78e75ce57c99fab
RECOVERY_SEQUENCE: 1_GOLDMASTER_EXACT;2_REALTEST;3_ONE_MANDATORY_DELTA;4_REALTEST;5_PASS_FREEZE_OR_FAIL_FULL_REVERT;6_REPEAT
CANDIDATE_BRANCH: hobbyroom/step04-pr126-expose-real-ppm-handoff-20260907
CANDIDATE_HEAD_SHA: 988498c76b02b33ecd1ede5c986454ca55c2ba07
TECHNICAL_SCOPE_PREFIXES: control/startmaster0107/;control/single-door-boundary/;control/output-quarantine/;control/CURRENT_STARTMASTER.json
ALLOWED_PATH_PREFIXES: control/single-door-boundary/codex_current_action.py;control/startmaster0107/CURRENT_STATE.json;control/startmaster0107/PFERDE_ATELIER_START_HERE.json;control/startmaster0107/STEP_107007_RUN_NEW_ARTICLE_BATCH_NO_STOP.json
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
**Exakt den historischen B02-Worker-Binding-Kandidaten prüfen. Kein zweiter Kandidat, kein weiterer Fix.**

## AUTORITÄTEN

Stand → `CURRENT_STATE.md`  
Fehler → `protocol/PROJECT_MEMORY/FEHLERREGISTER.md` → Originalquelle  
Ziel → `protocol/PROJECT_MEMORY/ZIELVERTRAEGE/REGISTER.md`  
Paul → `PAUL_PIPELINE_AUDIT_20260906.md`  
Warum/Änderungen → `protocol/PROJECT_MEMORY/AENDERUNGSREGISTER.md`


## AKTUELLER EINZELKANDIDAT – B02

Realer Baseline-Fehler:
`BOUND_CURRENT_FACHWORKFLOW_EXECUTION_CONTEXT_MISSING`

Historischer Gegencheck:
- B02 wurde bereits früher mit der Current-Codex-Fachworkflow-Worker-Bindung überwunden;
- danach erreichte der reale Lauf den nächsten Blocker B01;
- Paul stuft B02 ausdrücklich als bereits real überwundenen Handoff-/Worker-Kontextfehler ein, nicht als neuen 41-Punkte-Fix.

Historische bewiesene Quelle:
`c8a96e7a2f598de69134d90b143257c3559bc98a`

Kandidat:
`hobbyroom/b02-historical-worker-binding-20260907`
Head:
`75c9c8a9a2c16b604b2b21aa4253fe20131ff37f`

Exakt vier zusammengehörige hashgebundene Dateien:
1. `control/single-door-boundary/codex_current_action.py`
2. `control/startmaster0107/CURRENT_STATE.json`
3. `control/startmaster0107/PFERDE_ATELIER_START_HERE.json`
4. `control/startmaster0107/STEP_107007_RUN_NEW_ARTICLE_BATCH_NO_STOP.json`

Verbot:
- keine fünfte Datei;
- kein neuer B02-Fix;
- kein Paul-Sammelfix;
- keine prophylaktische Änderung hinter B02.

Nach Merge zwingend sofort echter 7/7-Realtest.
Bei FAIL dieses Deltas: vollständiger Rückbau des gesamten B02-Blocks, kein Fix darauf.


## B02-KANDIDAT #152 – VERWORFEN

Kandidat:
`75c9c8a9a2c16b604b2b21aa4253fe20131ff37f`

Ergebnis:
- nicht gemergt;
- normaler hardlock FAIL;
- hardlock-base FAIL;
- erster Fehler in beiden: `INPUT_HASH_MISMATCH:1:control/output-quarantine/runtime_entry_gate.py`.

Ursache:
Der komplette historische B02-Dateisnapshot enthielt einen alten Hash des damaligen `runtime_entry_gate.py` und ist deshalb nicht unverändert auf den heutigen Goldmaster-Hybridstand übertragbar.

HARD RULE angewendet:
- #152 geschlossen;
- keine Reparatur auf #152;
- Kandidat vollständig verworfen;
- nächster zulässiger Schritt ist nur die Analyse des **eigentlichen historischen B02-Semantik-Deltas** gegen den aktuellen Hash-Stand.


## STEP 01 – ERSTER CHRONOLOGISCHER PFLICHTDELTA

Quelle:
PR #122 / Merge `93536d5a61d34d1b24d80d9341e1b437ed3774f5`

Bedeutung:
PPM-Stufe an das exakte PPM-6.7.9-Ergebnis binden.

Kandidat:
`hobbyroom/step01-ppm679-binding-pr122-20260907`
Head:
`2f5a71637ee750cf33c763e53c78d6815286105b`

Änderungen:
genau 4 Dateien, alle exakt auf dem PR-#122-Zielstand.
Der zugehörige Test `test_ppm679_current_action_binding.py` war auf current main bereits exakt auf diesem Zielstand und wird deshalb nicht verändert.

HARD RULE:
- kein Step 02 vor Realtest von Step 01;
- bei FAIL Step 01 vollständig zurück;
- kein Fix auf Step 01;
- erst nach PASS nächster chronologischer Pflichtblock.


## STEP 01 – MERGED / REALTEST

Merge:
`46a807ac8fbdce5d1d4cf96c7e02d2cd4c206d5d`

Status:
Step 01 ist integriert. Step 02 ist bis zum echten 7/7-Ergebnis technisch gesperrt.

NEXT ACTION:
Ausschließlich echter 7/7-Realtest auf `46a807ac…`.


## REALTEST-KRITERIUM FÜR ZWISCHENSCHRITTE

Nach **jedem** chronologischen Pflichtblock erfolgt ein echter Realtest.

Der Realtest dient zur Standortbestimmung:
- erster echter Blocker wird protokolliert;
- kein nächster Block wird vor diesem Test eingebaut;
- derselbe spätere Blocker darf bestehen bleiben, wenn der gerade eingebaute Pflichtblock nur eine notwendige Vorstufe ist;
- verworfen wird ein Block nur bei Hardlock-/Invarianten-FAIL oder wenn er einen neuen früheren Rückschritt erzeugt.

Der finale Produktionsbeweis bleibt unverändert: echter 7/7-Lauf bis 107008.


## STEP 01 – REALTESTERGEBNIS

Step 01 / PR #122:
- vorheriger Blocker verschwunden;
- neuer erster Blocker: `BOUND_REAL_PPM679_EXECUTION_ACTION_MISSING`;
- dieser entspricht exakt dem nächsten chronologischen Pflichtblock PR #124.

Daher Step 01 bleibt Bestandteil des eingefrorenen Aufbaupfads.

## STEP 02 – EINZELKANDIDAT

Quelle:
PR #124 / Merge `0fcc6f9515a7aa32b8be3465ecbb50501eb424cd`

Kandidat:
`hobbyroom/step02-real-ppm679-execution-pr124-20260907`
Head:
`e5fc1c88dfac81b3ef18ff9b02bf37a677b0185a`

Änderung:
genau 1 Datei:
`control/startmaster0107/fachworkflow_proof_handoff.py`

Datei ist exakt auf PR-#124-Zielstand.

HARD RULE:
kein Step 03 vor Realtest von Step 02.


## STEP 02 – MERGED / REALTEST

Merge:
`7df2008eab8839271230b5dbfc62d7404c6e52f4`

Step 03 ist bis zum Realtest-Ergebnis gesperrt.


## STEP 02 – REALTESTERGEBNIS

Step 02 / PR #124:
- HEAD korrekt `7df2008e…`;
- Cloud Entry PASS;
- Production Preflight PASS;
- Runtime Entry PASS;
- Current Action READY;
- erster Blocker bleibt `BOUND_REAL_PPM679_EXECUTION_ACTION_MISSING`.

Einordnung:
PR #124 macht den realen PPM-Executor im Handoff ausführbar, exponiert ihn aber noch nicht in der Current Action. Kein Rückschritt, kein Hardlock-FAIL.

## STEP 03 – EINZELKANDIDAT

Quelle:
PR #125 / Merge `592a026f5f561020431594c452198280f8dca583`

Kandidat:
`hobbyroom/step03-pr125-107008-envelope-20260907`
Head:
`d0bf2d6b33425a12bf6b9a57bb1819ac9d147458`

Änderungen:
genau 5 Dateien, alle exakt PR-#125-Zielstand.
`chat_delivery_payload.py` war bereits exakt auf PR-#125-Stand und wird nicht verändert.

HARD RULE:
kein Step 04 vor Realtest von Step 03.


## STEP 03 – MERGED / REALTEST

Merge:
`a9cde12a7d82ada06e88235f0ae7e774a013ac93`

Step 04 ist bis zum Realtest-Ergebnis gesperrt.


## STEP 03 – REALTESTERGEBNIS

Step 03 / PR #125:
- HEAD exakt `a9cde12a7d82ada06e88235f0ae7e774a013ac93`;
- Cloud Entry PASS;
- Production Preflight PASS;
- Runtime Entry PASS;
- Current Action READY;
- erster Blocker weiterhin `BOUND_REAL_PPM679_EXECUTION_ACTION_MISSING`;
- kein Rückschritt, kein Publish.

Chronologisch nächster Pflichtblock:
PR #126 – vorhandenen realen PPM-Handoff in der Current Action exponieren.

## STEP 04 – EINZELKANDIDAT

Quelle:
PR #126 / Merge `336c6fe87ed3d5c20c54e684b36e45edc7d7cc14`

Kandidat:
`hobbyroom/step04-pr126-expose-real-ppm-handoff-20260907`
Head:
`988498c76b02b33ecd1ede5c986454ca55c2ba07`

Änderungen:
genau 4 Dateien, alle 4 exakt PR-#126-Zielstand.

HARD RULE:
kein Step 05 vor Realtest von Step 04.
