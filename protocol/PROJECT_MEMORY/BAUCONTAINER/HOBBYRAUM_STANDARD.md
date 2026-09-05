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
