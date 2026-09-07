# TEXT – HOBBYRAUM

STAND: 2026-09-07
STATUS: AKTIV / FIX_FORBIDDEN

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
STATUS: FIX_FORBIDDEN
OFFICE: TEXT
MAIN_SHA: f14ccf187b94c4beab9a86d0c69144f792ba2f64
ACTIVE_BLOCKER: HOBBYROOM_TECHNICAL_ENFORCEMENT_INACTIVE
PLAN_PHASE: HARDEN_HOBBYROOM
RECOVERY_BASE_SHA: de21f6cd35c60849c551fd82f78e75ce57c99fab
RECOVERY_SEQUENCE: 1_HARDEN_HOBBYROOM;2_COPY_GOLDMASTER;3_REAPPLY_MANDATORY_CHANGES_ONE_BY_ONE;4_REAL_TEST_AFTER_EACH_CHANGE
CANDIDATE_BRANCH: NONE
CANDIDATE_HEAD_SHA: NONE
TECHNICAL_SCOPE_PREFIXES: control/startmaster0107/;control/single-door-boundary/;control/output-quarantine/;control/CURRENT_STARTMASTER.json
ALLOWED_PATH_PREFIXES: NONE
CHECK_PAUL: PASS
CHECK_HISTORY: PASS
CHECK_LAST_GOOD: PASS
CHECK_NEIGHBORS: PASS
CHECK_REPEAT_CLASS: PASS
CHECK_POS_NEG: PENDING
CHECK_INVARIANTS: PENDING
INTEGRATION_ALLOWED: false
END_HOBBYROOM_WORK_LOCK_V1
```

Bedeutung:
Solange `STATUS=FIX_FORBIDDEN` oder ein Pflichtcheck nicht PASS ist, gibt es **keine Integrationsfreigabe**.

Nach Aktivierung von Security-PR #137 wird dieser Lock vom bestehenden serverseitigen Hardlock geprüft.

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
**1 – HOBBYRAUM TECHNISCH DICHTMACHEN**

Aktuelle Entscheidung:
**Goldmaster-Rekonstruktion ist als Strategie gebunden.**
Noch **kein** Reparaturkandidat freigegeben.
`CHECK_POS_NEG=PENDING`
`CHECK_INVARIANTS=PENDING`

Rückgabeweg:
Erst technische Hobbyraum-Erzwingung aktivieren und positiv/negativ beweisen. Danach Goldmaster-Kopie von `de21f6…`; anschließend Pflichtänderungen einzeln und jeweils real testen.

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
