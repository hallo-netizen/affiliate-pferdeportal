# TEXT – HOBBYRAUM

STAND: 2026-09-07
STATUS: AKTIV / FIX_ALLOWED_FOR_CODEX_TEST

## 1-KLICK-ÜBERSICHT

**WAS IST DAS?**  
Der einzige aktuelle Arbeitsraum des Büros TEXT.

**HIER BIST DU RICHTIG, WENN …**  
du den aktuell gebundenen TEXT-Arbeitsauftrag ausführst.

**DU DARFST …**  
nur den unten maschinenlesbar gebundenen Planpunkt und Scope bearbeiten.

**DU DARFST NICHT …**  
einen eigenen Prüfpfad, Minifix, Alternativweg, zweiten Branch, neuen Runner/Gate/Executor oder eine Fach-/Qualitäts-/Designregel erfinden.

**ALS NÄCHSTES …**  
ausschließlich die HARD RULE Goldmaster-Rekonstruktion in der festgelegten Reihenfolge abarbeiten.

## MASCHINELLER HOBBYRAUM-LOCK

```text
HOBBYROOM_WORK_LOCK_V1
STATUS: FIX_ALLOWED_FOR_CODEX_TEST
OFFICE: TEXT
MAIN_SHA: 457f33a09751db3acf78246ee394a59141d94d15
ACTIVE_BLOCKER: IMMUTABLE_BASE_HARDLOCK_WORKFLOW_NOT_TRIGGERING
PLAN_PHASE: HOBBYROOM_SECURITY_WORKFLOW_REACTIVATION
RECOVERY_BASE_SHA: de21f6cd35c60849c551fd82f78e75ce57c99fab
RECOVERY_SEQUENCE: 1_HARDEN_HOBBYROOM;2_COPY_GOLDMASTER;3_REAPPLY_MANDATORY_CHANGES_ONE_BY_ONE;4_REAL_TEST_AFTER_EACH_CHANGE
CANDIDATE_BRANCH: hobbyroom/goldmaster-main-reconstruction-20260907
CANDIDATE_HEAD_SHA: 482fa8ab71f4f180900707ca2309a5bd87727416
TECHNICAL_SCOPE_PREFIXES: control/startmaster0107/;control/single-door-boundary/;control/output-quarantine/;control/CURRENT_STARTMASTER.json
ALLOWED_PATH_PREFIXES: control/CURRENT_STARTMASTER.json;control/output-quarantine/output_release_gate.py;control/output-quarantine/runtime_entry_gate.py;control/single-door-boundary/codex_current_action.py;control/single-door-boundary/test_h8_preproduction_bootstrap.py;control/startmaster0107/CURRENT_STATE.json;control/startmaster0107/GITHUB_FINAL_RELEASE.py;control/startmaster0107/PFERDE_ATELIER_START_HERE.json;control/startmaster0107/STEP_107007_RUN_NEW_ARTICLE_BATCH_NO_STOP.json;control/startmaster0107/STEP_107008_FINAL_NEW_ARTICLE_BATCH_REVIEW_AWAIT_USER_PUBLISH.json;control/startmaster0107/codex-production-runtime/codex_environment_preflight.py;control/startmaster0107/codex-production-runtime/test_codex_environment_preflight.py;control/startmaster0107/fachworkflow_proof_handoff.py;control/startmaster0107/test_fachworkflow_proof_handoff.py
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

Bedeutung:
Solange `STATUS=FIX_FORBIDDEN` oder ein Pflichtcheck nicht PASS ist, gibt es **keine Integrationsfreigabe**.

Security-PR #137 ist **MERGED** auf current main `457f33a09751db3acf78246ee394a59141d94d15`.
Der eingebaute `HOBBYROOM_WORK_LOCK_V1` besitzt einen Positiv-/Negativ-Selbsttest `PASS 9/9`.
Noch offen: Im Ruleset `Pferde Atelier Main Hardlock` / ID `21788951` ist aktuell nur `hardlock` Pflichtcheck; `hardlock-base` muss nach der einmaligen Wartung wieder als Pflichtcheck hinzugefügt werden.
Bis dieser äußere Schutz wieder aktiv ist, bleibt `FIX_FORBIDDEN`.

## HARD RULE – GOLDMASTER-REKONSTRUKTION

**Diese Reihenfolge ist verbindlich und darf nicht übersprungen, umgestellt oder parallelisiert werden:**

1. Hobbyraum technisch dichtmachen.
2. `de21f6cd35c60849c551fd82f78e75ce57c99fab` als funktionierenden Goldmaster kopieren.
3. Nur zwingend notwendige spätere Änderungen einzeln nachrüsten.
4. Nach jedem einzelnen Einbau real testen.

Bis Schritt 1 technisch wirksam abgeschlossen ist:
- keine Goldmaster-Kopie;
- keine LanguageTool-Reparatur;
- kein anderer Minifix;
- keine Parallelreparatur;
- keine Integration.

Pauls/Claudes 41-Punkte-Audit ist dabei **Prüflinse**, kein 41-Punkte-Sammelfix.

## VERBINDLICHER ARBEITSPLAN – EINZIGE REIHENFOLGE

### A – Ausgangspunkt
- current main;
- erster echter Liveblocker;
- letzter echter 7/7-Stand;
- keine Produktionsänderung.

### B – Pflichtprüfung vor Kandidat
1. Paul-Befund zum betroffenen Korridor geprüft.
2. komplette Fehlerhistorie geprüft.
3. letzter funktionierender Stand verglichen.
4. unmittelbare Vor-/Nachstufe geprüft.
5. Wiederholungsfehlerklasse geprüft.
6. Positiv-/Negativtest auf dem Kandidaten.
7. Qualität/Inhalt/Design/Sicherheit/Single Door/Zwangsjacke unverändert.

Ein FAIL/UNKLAR = `FIX_FORBIDDEN`.

### C – Anti-Minifix
Bei wiederholter Fehlerklasse kein weiterer isolierter Minifix.
Gemeinsame Ursache im direkten Korridor bestimmen.

### D – genau ein KISS-Kandidat
Nur bestehende technische Bindungen korrekt verbinden.
Keine neue Fachlogik oder Architektur.

### E – lokale Freigabe
Positiv + Negativ + direkte Auswirkungen + historische Regression.
Nur dann:
`FIX_ALLOWED_FOR_CODEX_TEST`.

### F – Codex-Test
Exakt current main / bestehende eine Tür / dumme Wächter.
Beim ersten echten technischen Blocker STOP.
Keine Reparatur während des Laufs.

## AKTUELLE BINDUNG

Aktiver Arbeiter:
**normaler TEXT-Arbeitschat**

Paul:
**nicht gebunden**

Plan B / PR #143:
**separat eingefroren; für diese Arbeit nicht verwenden**

LanguageTool-Rebind-Branch:
`hobbyroom/languagetool-runtime-rebind-20260907`
**PARKPLATZ / NICHT INTEGRIEREN**

Aktueller Planpunkt:
**1 – HOBBYRAUM DICHTMACHEN / hardlock-base-WORKFLOW REAKTIVIEREN**

Aktuelle Entscheidung:
**Nur Kandidat `482fa8ab71f4f180900707ca2309a5bd87727416` ist freigegeben.**
14/14 geänderte TEXT-Korridor-Dateien sind bytegleich zu `de21f6…`.
Neue Security-/Campus-Zwangsjacke bleibt unangetastet.
Kein Publish.

Rückgabeweg:
1. Im Ruleset `Pferde Atelier Main Hardlock` `hardlock-base` wieder als Required Status Check hinzufügen.
2. Danach realen Hobbyraum-Lock gegen einen technischen Test-PR verifizieren.
3. Erst dann Goldmaster-Kopie von `de21f6…`; anschließend Pflichtänderungen einzeln und jeweils real testen.

## UNANTASTBAR

- genau eine Tür;
- dumme/fachblinde Wächter;
- Chat/Codex ohne freie Workflow-, Routing-, State-, Prüf-, Qualitäts-, Repair- oder Publishentscheidung;
- Qualität unverändert;
- Inhalt/Fachlogik unverändert;
- Design unverändert;
- PPM/PSERC/PSTE/LanguageTool/SEO/Tabellen/Links/Dubletten-/Kannibalisierungsschutz unverändert;
- kein Auto-Publish;
- keine zweite aktuelle Wahrheit.

## AUTORITATIVE QUELLEN

Stand:
`CURRENT_STATE.md`

Fehler:
`protocol/PROJECT_MEMORY/FEHLERREGISTER.md` → Originalquelle

Ziel:
`protocol/PROJECT_MEMORY/ZIELVERTRAEGE/REGISTER.md` → Hauptquelle

Paul:
`PAUL_PIPELINE_AUDIT_20260906.md`

Systemische technische Wirkungskarte:
`TECHNICAL_CORRIDOR_ROOTCAUSE_20260907.md`
`TECHNICAL_CORRIDOR_MATRIX_20260907.md`

Warum/Änderungen:
`protocol/PROJECT_MEMORY/AENDERUNGSREGISTER.md`


## AKTUELLER TECHNISCHER BLOCKER – hardlock-base STARTET NICHT

PR #148 wurde manuell geschlossen und wieder geöffnet.
Der normale `pull_request`-Workflow lief danach neu um 2026-09-07 19:34:31Z und ist PASS.
Der getrennte `pull_request_target`-Workflow `Pferde Atelier Immutable Base Hardlock` erzeugte dagegen keinen Lauf.
Der Ruleset verlangt `hardlock-base` weiterhin korrekt und blockiert den Merge deshalb fail-closed.

Folge:
- PR #148 bleibt offen und unverändert;
- kein Merge;
- kein Schritt 3;
- keine Reparatur am Goldmaster;
- zuerst den bestehenden Workflow in GitHub Actions reaktivieren/aktivieren.
