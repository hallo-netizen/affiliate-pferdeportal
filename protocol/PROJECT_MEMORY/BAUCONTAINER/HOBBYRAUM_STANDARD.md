# CAMPUS – HOBBYRAUM-STANDARD

STAND: 2026-09-07
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
RECOVERY_BASE_SHA: <letzter real funktionierender / gebundener Ausgangsstand>
ACTIVE_HISTORY_CASE: <exakter Mxx-Test, der den aktuellen Realblocker reproduziert>
HISTORY_EXPECTED_FAIL: NONE | <exakter Mxx-Fehler nur bei HISTORY_AUTHORITY_MAINTENANCE>
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
HISTORY_SOURCE_REF: <autoritative historische Fehlermatrix>
HISTORY_SOURCE_BLOB_SHA: <Git-Blob der Matrix auf geprüftem main>
HISTORY_PROOF_RUNNER_REF: <bestehender Regression-Runner>
HISTORY_PROOF_RUNNER_BLOB_SHA: <Git-Blob des vertrauenswürdigen Base-Runners>
PAUL_SOURCE_REF: <autoritative Paul-Prüfkarte>
PAUL_SOURCE_BLOB_SHA: <Git-Blob der Paul-Prüfkarte auf offiziellem Campus>
ERROR_SOURCE_REF: <autoritative Fach-Fehlerquelle>
ERROR_SOURCE_BLOB_SHA: <Git-Blob der Fehlerquelle auf offiziellem Campus>
CURRENT_STATE_REF: <zuständige CURRENT_STATE>
CURRENT_STATE_BLOB_SHA: <Git-Blob der CURRENT_STATE auf offiziellem Campus>
DECISION_SOURCE_REF: <AENDERUNGSREGISTER / dauerhafte WAS-WARUM-Quelle>
DECISION_SOURCE_BLOB_SHA: <Git-Blob der Entscheidungsquelle auf offiziellem Campus>
STANDARD_SOURCE_REF: <zuständiger Hobbyraum-Standard>
STANDARD_SOURCE_BLOB_SHA: <Git-Blob des Standards auf offiziellem Campus>
PROTOCOL_SOURCE_REF: <autoritative vollständige Ausführungs-/Testchronik>
PROTOCOL_SOURCE_BLOB_SHA: <Git-Blob des Protokolls auf offiziellem Campus>
INTEGRATION_ALLOWED: true|false
END_HOBBYROOM_WORK_LOCK_V1
```

Harte Wirkung nach Aktivierung des bestehenden Security-Hardlocks:
- technische PR außerhalb des gebundenen Hobbyraumscopes: nicht betroffen;
- PR im gebundenen Scope bei `FIX_FORBIDDEN`: **BLOCK**;
- falscher Branch / Head / Base: **BLOCK**;
- stale `MAIN_SHA`: **BLOCK**;
- Datei außerhalb `ALLOWED_PATH_PREFIXES`: **BLOCK**;
- `INTEGRATION_ALLOWED=false`: **BLOCK**;
- geänderte/stale autoritative Fehler-, Paul- oder CURRENT_STATE-Quelle: **BLOCK**;
- fehlendes oder stale Ausführungs-/Testprotokoll: **BLOCK**;
- `ACTIVE_BLOCKER` nicht in Fehlerquelle oder CURRENT_STATE: **BLOCK**;
- kompletter vertrauenswürdiger historische Regression-Lauf vom PR-Base gegen einen Produktionskandidaten nicht GESAMT PASS: **BLOCK**;
- Lücke in der fortlaufenden Fehlerhistorie ab M01: **BLOCK**;
- historischer Runner und Matrix nicht exakt deckungsgleich: **BLOCK**;
- aktueller Blocker nicht eindeutig einem `ACTIVE_HISTORY_CASE` in der autoritativen Fehlerzeile zugeordnet: **BLOCK**;
- current main reproduziert `ACTIVE_HISTORY_CASE` nicht als ersten Regression-FAIL: **BLOCK**;
- Kandidat besteht danach nicht mit demselben vertrauenswürdigen Runner vollständig: **BLOCK**;
- `RECOVERY_BASE_SHA` ist kein realer Vorfahr des current main: **BLOCK**;
- autoritative Fehlerquelle und aktuell akzeptierte Historie nicht deckungsgleich: **BLOCK**;
- Matrix/Runner zusammen mit Produktionscode geändert: **BLOCK**.

Die sieben `CHECK_*`-Felder bleiben höchstens Arbeitsnotizen.
Sie erzeugen **keine Integrationsfreigabe** und dürfen einen fehlenden Maschinenbeweis niemals ersetzen.

Wartung von Fehlermatrix oder Regression-Runner:
- nur separat;
- kein Produktionsfix im selben PR;
- eigener Plan `HISTORY_AUTHORITY_MAINTENANCE`;
- `HISTORY_EXPECTED_FAIL` bindet exakt den aktuell realen Fehler Mxx;
- `HISTORY_EXPECTED_FAIL` muss dabei `ACTIVE_HISTORY_CASE` entsprechen;
- bestehende Historie darf niemals verkürzt werden;
- neue Fehler werden fortlaufend M34, M35, ... ergänzt, ohne Änderung des Security-Gates;
- autoritative Fehlerquelle wird zuerst um den neuen realen Fehler ergänzt;
- der vertrauenswürdige Base-Runner muss alle bisher akzeptierten Fehler weiterhin PASS halten;
- der neue Kandidaten-Runner muss auf dem **noch unreparierten** Stand exakt bei `HISTORY_EXPECTED_FAIL` als erstem Fehler FAIL liefern;
- erst danach darf der spätere Produktionsfix gebaut werden;
- der Produktionsfix muss anschließend die gesamte nun erweiterte Historie GESAMT PASS machen.

Nur bei exakt gebundenem Kandidat plus serverseitigem Maschinenbeweis:
`HOBBYROOM_HISTORY_MACHINE_PROOF_PASS`.

Der Lock enthält keine Fachregeln und trifft keine Fachentscheidung.
Er bindet nur die aktuellen autoritativen Quellen, den realen Fortschritt und den technischen Kandidaten fail-closed.

Damit bleibt:
**HOBBYRAUM = einzige aktuelle Arbeitswahrheit; Hardlock = technische Durchsetzung; Historie/Paul/Realstand = maschinell wiederverwendete Evidenz statt wiederholter Chat-Prüfung.**


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
### Maschinengehärtete Evidenzpflicht

Bei `FIX_ALLOWED_FOR_CODEX_TEST` reicht kein manuelles `CHECK_*: PASS`.

Der serverseitige Hardlock muss selbst belegen:

- `RECOVERY_BASE_SHA` ist ein gültiger Commit und in der zuständigen CURRENT_STATE als letzter funktionierender Stand belegt;
- mindestens M01–M33 und jeder später real aufgenommene M34/M35/... sind lückenlos in historischer Matrix, vertrauenswürdigem Runner **und** autoritativer Fach-Fehlerquelle vorhanden;
- `ACTIVE_BLOCKER` steht real in Fach-Fehlerquelle und CURRENT_STATE;
- `ACTIVE_HISTORY_CASE` zeigt auf genau die Fehlerzeile, die `ACTIVE_BLOCKER` enthält;
- current main muss vor dem Fix mit dem vertrauenswürdigen Runner exakt bei `ACTIVE_HISTORY_CASE` als erstem Fehler FAIL liefern;
- derselbe Runner muss nach dem Fix auf dem Kandidaten GESAMT PASS liefern;
- `MAIN_SHA` steht real in CURRENT_STATE;
- Pauls Kernregeln sind in der gebundenen Prüfkarte vorhanden: kein Sammelfix, historische Fehlerquelle gegenprüfen, bestehende Regression danach, echter 7/7-Lauf als Produktionsbeweis, Vertragskollision, Artefaktzustands-Parität, Hash-Semantik und Pre-/Post-Transformation;
- das Änderungs-/Erklärungsregister enthält die eingefrorene Recovery-Regel, den kausalen Corridor und die Maschinenbeweis-Entscheidung;
- der Hobbyraum-Standard enthält weiterhin vollständige Historienprüfung, letzten funktionierenden Stand, direkte Vor-/Nachstufe, Wiederholungsfehlerklasse, Positiv/Negativ und STOP ohne Reparatur im Realtest;
- das gebundene Ausführungs-/Testprotokoll enthält den aktuellen Realblocker, current main und `RECOVERY_BASE_SHA` sowie reale PASS-/FAIL-/Realtest-Ereignisse;
- der vertrauenswürdige M01–M33-Runner vom PR-Base/main läuft vollständig gegen den Kandidaten;
- Produktcode darf Matrix/Runner nicht im selben PR verändern.
- Neue reale Fehler dürfen nicht direkt repariert werden, wenn sie noch nicht als ausführbare Regression existieren: zuerst separater `HISTORY_AUTHORITY_MAINTENANCE`-Lauf mit exakter FAIL-Reproduktion, danach erst Produktionsfix;
- der Gate-Code führt seine eigenen Arbeitslock-/Evidenz-Selbsttests bei jedem serverseitigen `verify-pr` automatisch aus;


Fehlt nur ein Beleg oder driftet nur ein gebundener Git-Blob:
`FIX_FORBIDDEN`.

Die `CHECK_*`-Felder sind nur Arbeitsnotizen und niemals Freigabeautorität.

## 2026-09-08 – KISS-REAPPLY-REGEL

Bei Wiederherstellung eines älteren Commits, PRs oder Dateistands gilt campusweit:

1. **Keine alte Gesamtdatei blind zurückspielen.**
2. Vor einem Whole-File-Reapply den begrenzten Ein-/Ausgangskorridor gegen den heutigen Vertrag prüfen:
   - aktuelle Upstream-Eingaben;
   - aktuelle Downstream-Validatoren;
   - später bewiesene Fixes;
   - reale letzte PASS-Referenz.
3. Wenn ein Live-Fehler nach einem Reapply auftritt, zuerst prüfen, ob weitere bereits behobene Altsemantik mit zurückgekommen ist.
4. In diesem Fall **einmal den ganzen betroffenen Korridor prüfen**, statt Fehler für Fehler seriell zu flicken.
5. Daraus keine neue Gate-/Runner-/Sicherungsarchitektur bauen. KISS bleibt verbindlich.



## 2026-09-09 – Autoritative Evidence statt Worker-Selbstbeglaubigung

Allgemeingültig für technische Mehrstufen-Workflows:

Ein Stage-Name oder eine vom Worker selbst geschriebene Proof-Datei ist **kein** Ausführungsbeweis.

Für jede freigaberelevante Stufe muss vor einem Produktfix eindeutig feststehen:
1. vorhandene autoritative Ausführung bzw. vorhandener Validator;
2. exakter Input-Artefaktzustand;
3. exakter Output/Evidence-Zustand;
4. realer nächster Consumer;
5. mechanische Identitäts-/Hashbindung;
6. keine Fach-/Qualitätsentscheidung durch Chat oder Worker.

Verboten:
- `status=PASS` / `execution_performed=true` als alleinige Freigabe;
- einen fehlenden Prüfer oder eine unklare Stage-Bedeutung selbst definieren;
- historische Artefakte als aktuelle Produktionsquelle verwenden;
- bei wiederkehrender Bindungsklasse Stufe für Stufe Minifixes bauen.

Wenn eine benötigte bestehende Autorität nicht gefunden oder die Stage-Semantik nicht eindeutig belegt ist:
`FIX_FORBIDDEN`.

Das ist eine technische Evidenzregel, keine neue Fachlogik.
