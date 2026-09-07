# CAMPUS – HOBBYRAUM-STANDARD

STAND: 2026-09-05
STATUS: VERBINDLICH

## Zweck

Ein Hobbyraum ist der einzige gebundene aktuelle Arbeitsraum eines Büros.

Er verhindert parallele, widersprüchliche Reparaturwege.

## Genau ein Hobbyraum pro Büro

Projektbüros haben genau:
`HOBBYRAUM.md`

Keine zweiten Neben-Hobbyräume für denselben Auftrag.

## Erlaubte Zustände

### FREI
Kein aktueller Auftrag gebunden.

### AKTIV
Genau ein Arbeitsweg/Branch/Auftrag ist gebunden.

Pflicht:
- aktueller Auftrag oder direkter Arbeitsweg;
- Branch, falls Arbeit auf Branch erfolgt;
- Rückgabeweg.

### BLOCKED
Der gebundene Auftrag kann wegen eines konkret benannten Blockers nicht weiterarbeiten.

## Kennwort

Es gibt **kein geheimes Passwort** im Campus.

Routing-Kennwort:
`Hobbyraum`

Beispiele:
- „Pferde-Atelier → TEXT → Hobbyraum“
- „Geh in den TEXT-Hobbyraum.“

Das Kennwort ist nur Navigation, keine Sicherheitsberechtigung.

Echte Befugnis entsteht durch:
- Rolle;
- gebundenen Auftrag;
- Branch-/Repository-Rechte;
- Zielvertrag;
- Fachregeln.

## Harte Grenzen

- Hobbyraum darf keine zweite Fachwahrheit erzeugen.
- Keine Fachregeln duplizieren, wenn ein autoritativer Vertrag/Originalquelle existiert.
- Kein veralteter Chatstatus als dauerhafte Belegung.
- Bei Abschluss: FREI oder ausdrücklich nächsten Auftrag binden.


## Direkteinstieg in Hobbyraum

Jeder Büro-`HOBBYRAUM.md` beginnt ebenfalls mit der 1-KLICK-ÜBERSICHT:
- WAS IST DAS?
- HIER BIST DU RICHTIG, WENN …
- DU DARFST …
- DU DARFST NICHT …
- ALS NÄCHSTES …

Damit bleibt auch ein direkter Link in den Hobbyraum selbsterklärend.


## Arbeitskontrollpunkt

Jeder Hobbyraum zeigt nur:
- Bürostand → CURRENT_STATE
- aktuelle Arbeit / NEXT ACTION → HOBBYRAUM selbst
- Fehler → FEHLERREGISTER → Originalquelle
- Ziel → Zielvertragsregister → Hauptquelle
- Begründung → AENDERUNGSREGISTER

Fachstand, Fehlertext und Zielinhalt werden dort nicht nochmals gepflegt.


## Dynamische Arbeitsbindung niemals aus Architekturannahme ändern

STATUS, Worker, Branch und NEXT ACTION sind dynamische Arbeitswahrheit.

Architektur-, Baucontainer- oder Hausmeisterarbeit darf diese Werte **nicht** umdeuten oder neu setzen, nur weil eine neue Rollenregel gebaut wird.

Änderung nur bei:
- ausdrücklicher neuer Nutzerzuweisung; oder
- frisch belegter autoritativer Arbeitszuweisung.

Fehlt dieser Beleg:
bestehende Arbeitsbindung erhalten und nur die Architektur-/Routingregel darum herum korrigieren.

Negativtest:
Ein Architekturfix darf niemals aus `WORKER = PAUL` still `WORKER = ARBEITSCHAT` machen oder umgekehrt.


## Automatische Paul-Bindung – einzige Auftragswahrheit bleibt der Hobbyraum

Ein Paul-Auftrag wird **nicht** als separater Prompt oder zweite Auftragsakte gepflegt.

Nur solange Paul tatsächlich gebunden ist, enthält genau der zuständige `HOBBYRAUM.md` zusätzlich diesen maschinenlesbaren Block:

```
<!-- PAUL_ASSIGNMENT_V1
STATUS: ACTIVE
WORKER: PAUL
ASSIGNMENT_ID: <eindeutige ID>
PAUL_BRANCH: paul/<auftrag>
TECHNICAL_BASE_SHA: <exakter 40-stelliger Ausgangscommit>
WRITE_SCOPE: <datei;verzeichnis/> oder READ_ONLY
TASK_SOURCE: <autoritative Problem-/Auftragsquelle>
TARGET_SOURCE: <autoritative Zielquelle>
RULES_SOURCE: <autoritative Hard-Rules-Quelle>
-->
```

Harte Regeln:
- ohne aktiven Block ist Paul **nicht beauftragt**;
- campusweit darf gleichzeitig höchstens **ein** `STATUS: ACTIVE / WORKER: PAUL`-Block existieren;
- mehrere aktive Paul-Blöcke = `PAUL_MULTIPLE_ASSIGNMENTS_BLOCKED`;
- Problem, Ziel und Regeln werden im Block **nicht kopiert**, sondern nur auf ihre autoritativen Quellen verwiesen;
- `WRITE_SCOPE` enthält nur technische Pfade; `protocol/PROJECT_MEMORY/**`, Security-/Workflowpfade und `AGENTS.md` sind für Paul niemals zulässiger Scope;
- `TECHNICAL_BASE_SHA` ist der Commit, auf dem Pauls Branch für genau diesen Auftrag basiert;
- bei Rückgabe/Beendigung wird der aktive Block aus dem Hobbyraum entfernt; Historie gehört ins Protokoll/Archiv, nicht in die aktuelle Arbeitsbindung.

Damit bleibt:
**HOBBYRAUM = eine aktuelle Auftragswahrheit.**


## Exklusiver technischer Paul-Scope

Bei aktivem `PAUL_ASSIGNMENT_V1` gilt `WRITE_SCOPE` nicht nur als Pauls Schreibgrenze.

Er ist gleichzeitig eine **exklusive Sperrfläche**:
- Paul darf nur darin schreiben;
- jeder andere PR/Worker darf denselben Scope während der aktiven Paul-Bindung nicht verändern;
- Kollision → `PAUL_EXCLUSIVE_SCOPE_LOCKED`;
- unabhängige technische Pfade bleiben parallel erlaubt.

## Frischer Branch pro Paul-Auftrag

Jeder neue Paul-Auftrag erhält einen **frischen** `paul/*`-Branch direkt vom gebundenen `TECHNICAL_BASE_SHA`.

Kein Recycling eines alten Paul-Branches mit Commits aus einem vorherigen Auftrag.

Grund:
Altcommits könnten sonst bereits vor Arbeitsbeginn außerhalb des neuen Scopes liegen oder einen READ_ONLY-Auftrag unzulässig „vorbelasten“.


## Maschinenlesbarer Arbeits-Lock für normale Arbeitschats

Für technische Arbeiten kann ein Hobbyraum zusätzlich genau einen
`HOBBYROOM_WORK_LOCK_V1` enthalten.

Zweck:
Nicht der Chat entscheidet, ob ein Fix gebaut oder integriert werden darf.
Der Hobbyraum bindet den aktuellen Arbeitszustand; der bestehende Security-Hardlock prüft ihn serverseitig.

Schema:

```text
HOBBYROOM_WORK_LOCK_V1
STATUS: FIX_FORBIDDEN|FIX_ALLOWED_FOR_CODEX_TEST
OFFICE: <Büro>
MAIN_SHA: <40-stelliger aktueller main-Ausgangscommit>
ACTIVE_BLOCKER: <autoritativer Fehlercode>
PLAN_PHASE: <aktueller festgelegter Arbeitsplanpunkt>
CANDIDATE_BRANCH: <exakter Branch> oder NONE
CANDIDATE_HEAD_SHA: <exakter 40-stelliger Head> oder NONE
TECHNICAL_SCOPE_PREFIXES: <geschützter technischer Bereich>
ALLOWED_PATH_PREFIXES: <für Kandidat exakt erlaubte Pfade> oder NONE
CHECK_PAUL: PASS|PENDING|FAIL
CHECK_HISTORY: PASS|PENDING|FAIL
CHECK_LAST_GOOD: PASS|PENDING|FAIL
CHECK_NEIGHBORS: PASS|PENDING|FAIL
CHECK_REPEAT_CLASS: PASS|PENDING|FAIL
CHECK_POS_NEG: PASS|PENDING|FAIL
CHECK_INVARIANTS: PASS|PENDING|FAIL
INTEGRATION_ALLOWED: true|false
END_HOBBYROOM_WORK_LOCK_V1
```

Harte Wirkung nach Aktivierung des bestehenden Security-Hardlocks:
- technische PR außerhalb des gebundenen Hobbyraumscopes: nicht betroffen;
- PR im gebundenen Scope bei `FIX_FORBIDDEN`: **BLOCK**;
- PR bei fehlendem 7-Punkte-PASS: **BLOCK**;
- falscher Branch: **BLOCK**;
- falscher Kandidaten-Head: **BLOCK**;
- stale `MAIN_SHA`: **BLOCK**;
- Datei außerhalb `ALLOWED_PATH_PREFIXES`: **BLOCK**;
- `INTEGRATION_ALLOWED=false`: **BLOCK**.

Nur bei exakt gebundenem Kandidat und vollständigem PASS:
`HOBBYROOM_WORK_LOCK_PR_PASS`.

Der Lock enthält keine Fachregeln und trifft keine Fachentscheidung.
Er ist ausschließlich ein dummer technischer Scope-/Status-/Hash-Wächter.

Damit bleibt:
**HOBBYRAUM = einzige aktuelle Arbeitswahrheit; Hardlock = technische Durchsetzung.**


## Verbindlicher Pre-Fix-Ablauf für technische Hobbyräume

Für technische Reparaturarbeit gilt campusweit genau diese Reihenfolge:

A. Ausgangspunkt: current main, erster echter Liveblocker, letzter funktionierender Stand.
B. Vor jedem Kandidaten zwingend:
1. relevanten Paul-/Spezialreview prüfen, falls vorhanden;
2. gesamte bekannte Fehlerhistorie prüfen;
3. letzten funktionierenden Stand vergleichen;
4. unmittelbare Vor- und Nachstufe mit exaktem Artefaktzustand prüfen;
5. Wiederholungsfehlerklasse prüfen;
6. Positiv- und Negativtest des Kandidaten;
7. Qualität/Inhalt/Design/Sicherheit/Single Door/Zwangsjacke unverändert nachweisen.
C. Bei wiederholter Fehlerklasse: kein weiterer isolierter Minifix; gemeinsame Ursache im direkten Korridor bestimmen.
D. Genau einen KISS-Kandidaten binden.
E. Erst nach vollständigem Positiv/Negativ/Invarianten-PASS = `FIX_ALLOWED_FOR_CODEX_TEST`.
F. Realtest auf dem produktiven Weg; beim ersten echten Blocker STOP, keine Reparatur im laufenden Test.

Ein `FAIL`, `PENDING`, `UNKLAR` oder `NICHT BELEGT` in einem Pflichtpunkt bedeutet:
`FIX_FORBIDDEN`.

Wichtig:
Diese Reihenfolge enthält keine Fachregeln. Sie erzwingt nur, dass bekannte Fehler, Nachbarwirkungen und reale Tests vor einer technischen Änderung berücksichtigt werden.
