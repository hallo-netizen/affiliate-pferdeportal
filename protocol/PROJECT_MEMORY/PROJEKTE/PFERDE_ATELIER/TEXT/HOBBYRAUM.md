# TEXT – HOBBYRAUM

STAND: 2026-09-08
STATUS: AKTIV / REPARATURKONZEPT EINGEFROREN / FIX_FORBIDDEN

## EINZIGE ARBEITSWAHRHEIT

Es gibt ab hier **genau ein Reparaturkonzept**. Dieses Konzept darf während der Wiederherstellung nicht geändert, erweitert, parallelisiert oder durch einen anderen Ansatz ersetzt werden.

Ziel:
`107008 – FINAL_NEW_ARTICLE_BATCH_REVIEW_AWAIT_USER_PUBLISH`

Goldmaster:
`de21f6cd35c60849c551fd82f78e75ce57c99fab`

Aktueller main:
`67143a95ee98d6a7ce15167dfd8103ceee087f2d`

Aktueller erster echter Blocker:
`BOUND_CURRENT_FACHWORKFLOW_EXECUTION_CONTEXT_MISSING`

Aktueller Stand:
STEP 04 real getestet. Kein STEP 05 begonnen.

## MASCHINELLER HOBBYRAUM-LOCK

```text
HOBBYROOM_WORK_LOCK_V1
STATUS: FIX_ALLOWED_FOR_CODEX_TEST
OFFICE: TEXT
MAIN_SHA: 67143a95ee98d6a7ce15167dfd8103ceee087f2d
ACTIVE_BLOCKER: BOUND_CURRENT_FACHWORKFLOW_EXECUTION_CONTEXT_MISSING
PLAN_PHASE: B02_SINGLE_CANDIDATE_BOUND
RECOVERY_BASE_SHA: de21f6cd35c60849c551fd82f78e75ce57c99fab
RECOVERY_SEQUENCE: 1_GOLDMASTER_EXACT;2_REALTEST;3_ONE_MANDATORY_DELTA;4_REALTEST;5_PASS_FREEZE_OR_FAIL_FULL_REVERT;6_REPEAT
CANDIDATE_BRANCH: hobbyroom/b02-semantic-worker-binding-current-hash-20260908
CANDIDATE_HEAD_SHA: 562b71c726e2232539412376c1b0a047dbd3485d
TECHNICAL_SCOPE_PREFIXES: control/startmaster0107/;control/single-door-boundary/;control/output-quarantine/;control/CURRENT_STARTMASTER.json
ALLOWED_PATH_PREFIXES: control/single-door-boundary/codex_current_action.py;control/startmaster0107/STEP_107007_RUN_NEW_ARTICLE_BATCH_NO_STOP.json;control/startmaster0107/CURRENT_STATE.json;control/startmaster0107/PFERDE_ATELIER_START_HERE.json
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

Diese Reihenfolge ist verbindlich:

1. Goldmaster `de21f6…` ist die technische Funktionsreferenz.
2. Nur der **erste reale Blocker** wird bearbeitet.
3. Vor jedem Kandidaten werden genau vier Quellen geprüft:
   - Pauls technische Prüfkarte;
   - Fehlerhistorie;
   - letzter funktionierender Stand;
   - direkte Vor-/Nachstufe.
4. Genau **eine** zwingend notwendige Änderung wird gebaut.
5. Lokale Positiv-/Negativprüfung.
6. Danach echter 7/7-Realtest.
7. Ergebnis:
   - **PASS / Blocker wandert erwartbar weiter:** Änderung wird als neuer Zwischenstand eingefroren.
   - **Regression / neuer früherer Fehler / Hardlock-FAIL:** komplette Änderung zurückbauen.
8. **Kein Fix auf einen fehlgeschlagenen Fix.**
9. Erst danach darf die nächste Änderung beginnen.
10. Wiederholen bis 107008 erreicht ist; vor Publish stoppen.

## PAUL – VERBINDLICHE PRÜFLINSE

Quelle:
`protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/TEXT/PAUL_PIPELINE_AUDIT_20260906.md`

Pauls Liste ist Pflichtprüfung vor jedem Einzelkandidaten, aber **kein 41-Punkte-Sammelfix**.

Ein Paul-Punkt darf nur Kandidat werden, wenn er:
- zum aktuell real reproduzierten Fehler passt; und
- als neu wirksam oder reproduzierbarer Vertragskonflikt belegt ist.

Latente oder historisch bereits vorhandene Punkte werden nicht prophylaktisch repariert.

## VERBOTEN

- Konzeptwechsel.
- paralleler Reparaturpfad.
- Sammelfix.
- zwei Änderungen zwischen zwei Realtests.
- zweiter Fix auf einen fehlgeschlagenen Kandidaten.
- prophylaktische Reparatur späterer Fehler.
- neuer Runner, Gate, Executor oder Ersatzweg.
- LanguageTool-/PPM-/SEO-/Link-/Tabellen-/Design-/Security-Umbau außerhalb des aktuell real belegten Einzelkandidaten.
- Publish oder WordPress-Schreibvorgang.
- Änderung des Zielvertrags während dieser Wiederherstellung.

## AKTUELLE EINZIGE NEXT ACTION

**Nur `BOUND_CURRENT_FACHWORKFLOW_EXECUTION_CONTEXT_MISSING` analysieren.**

Fehlender aktuell gebundener R_001-Kontext laut STEP-04-Realtest:
- `fact_pack`
- `production_plan_item`
- `production_plan_header`
- `workflow_release_item`
- `workflow_release_metadata`
- reale Nicht-PPM-Pflichtstufen-Artefakte

Vor einem Kandidaten zwingend:
1. Paul-Prüfkarte gegen diesen Korridor;
2. Commit-/Fehlerhistorie;
3. letzter Stand, auf dem dieser Kontext real vorhanden war;
4. direkte Vor-/Nachstufe.

Prüfung abgeschlossen. Einziger gebundener Kandidat:
- Branch `hobbyroom/b02-semantic-worker-binding-current-hash-20260908`
- Head `562b71c726e2232539412376c1b0a047dbd3485d`
- 2 Semantikdateien + 2 reine Hashbindungsdateien
- historischer Beleg: `c8a96e…` beseitigte B02; danach kam erst `BOUND_WORDPRESS_CATEGORY_ID_MISSING_FOR_REAL_PPM679_EXECUTION`

Bis CI/Positiv-Negativ PASS: kein Merge. Nach Merge zwingend sofort echter Codex-7/7-Realtest.

## AUTORITÄTEN

Aktueller Stand → `CURRENT_STATE.md`

Aktuelle Arbeit / einzige NEXT ACTION → **diese Datei**

Paul-Prüflinse → `PAUL_PIPELINE_AUDIT_20260906.md`

Fehlerhistorie → `protocol/PROJECT_MEMORY/FEHLERREGISTER.md` → Originalquelle

Ziel → `protocol/PROJECT_MEMORY/ZIELVERTRAEGE/REGISTER.md`

Änderungs-/Verlaufsprotokoll → `protocol/PROJECT_MEMORY/AENDERUNGSREGISTER.md` und Git-/PR-Historie

Historische Kandidaten und alte NEXT-ACTION-Texte sind **keine Arbeitsanweisung** und werden nicht mehr im HOBBYRAUM fortgeschrieben.
