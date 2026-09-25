# Pferde Atelier – KISS text-start closeout – 2026-09-25

Status dieses Dokuments: Historie/Nachweis und Übergabe-Wegweiser. **Keine CURRENT-Autorität und keine eigene NEXT-ACTION-Wahrheit.**

## Zielvertrag
GitHub ist ausschließlich Startknopf. Nach dem Start läuft der vorhandene interne Concept-Agent-Workflow weiter. Kein neuer Runner, kein API-/GitHub-Produktionsfortschritt, keine neue Architektur, keine Änderung an Artikel-, Qualitäts-, LT-6.8-, PPM-6.7.9-, PSERC-, ENDSTEMPEL- oder Publish-Regeln. Chat hat keine freie Navigations-/Manipulationsautorität.

## Tatsächlich erledigt
- Main vor Closeout: `710bb5d78b884b3e94d397dcba3eb0418b6fe98f`.
- PR #395 ist gemergt: GitHub-Durable-Event-/Produktionsfortschritt aus PR #389 wurde zurückgebaut.
- `concept_agent/durable_event_log.py` und dessen Protokoll wurden entfernt.
- Vor-#389-Versionen von `concept_agent/CONTROL_ENTRY_POINTER.json`, `concept_agent/START_HERE.md` und `concept_agent/tests/test_current_production_guards.py` wurden wiederhergestellt.
- Die vorhandene interne Produktionslogik bleibt unverändert: `production_bridge.py`, `progress_guard.py`, `universal_reentry_guard.py`, PSERC und ENDSTEMPEL.
- Obsolete Parallel-/Migrations-PRs #388, #392, #394 sowie Dubletten #397, #398, #400, #401 wurden geschlossen.
- Genau ein KISS-Kandidat bleibt: PR #399, Head `cf2494d83f3b71d8810692abaa455ca79ea8dd10`.
- PR #399 entfernt nur GitHub-Batch-Claim/`MACHINE_READY`/Issue-Fortschrittslogik aus dem Startreceiver und korrigiert die Concept-Agent-Bürotür auf Checkpoint-Reentry.
- Deterministic Entrance Gate für PR #399: Run `36116874815` = SUCCESS.

## Nicht erledigt / erster offener Blocker
PR #399 ist **nicht gemergt**.

Der Mergeversuch wurde von Ruleset `21788951` abgelehnt:
- Required status check: `hardlock-base`;
- Hardlock-Code blockiert jede Änderung unter `.github/workflows/**` als `IMMUTABLE_SECURITY_PATH_CHANGE_BLOCKED`;
- Ruleset ist aktiv;
- `bypass_actors=[]`;
- `current_user_can_bypass="never"`.

Damit ist der gewünschte KISS-Rückbau am echten Startworkflow unter der derzeitigen Schutzregel nicht mergebar, ohne diese Regel bzw. deren autorisierten Änderungsweg zu klären. Es wurde **kein** neuer Bypass und **keine** Ersatzroute gebaut.

## Tests
Belastbar vorhanden aus dem bestehenden Produktionskern:
- interne 1-/3-Artikel-Strecken und Same-Article-Repair sind historisch/evidenzseitig vorhanden;
- aktueller PR-#399-Entrance-Gate: PASS.

**Nicht ausgeführt nach dem heutigen Rückbau:**
- kompletter realer Startknopf -> interne Übergaben -> ausgelöste Folgeaktionen -> Repair-Rückführung -> PSERC -> ENDSTEMPEL -> Dateiausgabe;
- dazugehöriger positiver und negativer Gesamtstreckentest.

Deshalb: **kein Gesamt-PASS**.

## Current-/Frischecheck
Bürotür:
- `concept_agent/START_HERE.md`
- `concept_agent/CONTROL_ENTRY_POINTER.json`

Eine zuständige Current-Autorität:
- `control/startmaster0107/CURRENT_STATE.json` auf `main`.

Frischecheck-Ergebnis:
- relevante Änderung seit der dort dokumentierten Wahrheit vorhanden;
- `CURRENT_STATE.json` behauptet noch `CONCEPT_AGENT_TEXT_START_1N_READY_NO_ACTIVE_PRODUCTION_RUN` / Blocker `RESOLVED`;
- das ist nach dem heutigen Delta nicht mehr belastbar, weil der endgültige Startknopf-Rückbau #399 ungemergt und der Gesamtstreckentest offen ist.

CURRENT_STATE wurde **nicht** isoliert verändert, weil seine Hash-Bindung an `control/startmaster0107/PFERDE_ATELIER_START_HERE.json` technisch mitgeführt werden muss und genau diese Datei vom selben `hardlock-base` geschützt ist. Eine einseitige Current-Änderung würde die vorhandenen Guards absichtlich brechen.

Ergebnis: **CURRENT-Autorität = BLOCKED / nicht synchronisierbar, bis der Hardlock-Konflikt auf dem bereits vorgesehenen autorisierten Weg gelöst ist.**

Zusätzlich ist die Concept-Agent-Bürotür bis zum Merge von PR #399 **BLOCKED**: Sie routet zwar eindeutig auf genau eine Current-Autorität, enthält auf main aber noch die überholte `MACHINE_READY`-/`kein zweites text-start`-Regel. PR #399 korrigiert genau dieses Delta. Die technisch hashgebundenen Felder in `control/startmaster0107/PFERDE_ATELIER_START_HERE.json` werden nicht entfernt, weil vorhandene Guards sie aktiv prüfen; sie sind keine separat erfundene Current-Autorität.

## Historisch damals gebundene NEXT ACTION — nicht Current
**Den bestehenden Hardlock-Konflikt für exakt PR #399 auf dem bereits autorisierten Repository-Regelweg lösen, ohne den Diff von PR #399 zu erweitern oder einen neuen Produktionsweg zu bauen. Danach #399 mergen und unmittelbar die vorhandene komplette positive/negative Strecke vom Startknopf bis zur Dateiausgabe ausführen.**

## Verbindlicher Arbeitsweg
- Keine neue Architektur.
- Kein neuer Runner.
- Kein GitHub-/API-Fortschrittslog.
- Kein alternativer Start.
- PR #399 ist der einzige aktuelle technische Kandidat.
- Nach Merge ausschließlich bestehende interne Strecke verwenden.
- Fehler/Repair: gleicher Artikel, zuständiger Owner, erneuter Prüflauf bis echter PASS; kein globaler Abbruch bei reparierbarem Fehler.
- Technische/Integritäts-/Manipulationsfehler bleiben fail-closed.
- Kein Publish.

## Nicht anfassen
- Artikel-/Qualitätsregeln;
- LanguageTool 6.8;
- PPM 6.7.9;
- PSERC;
- ENDSTEMPEL;
- bestehende Link-/Research-/Authoring-Bindungen;
- alternative historische System4-/GitHub-/Codex-Routen.

## Fehlerprotokoll dieses Chats
1. **PR #389 GitHub-Durable-Event-Produktionssteuerung**
   - Fehlerklasse: falscher GitHub-Einbau in Produktionsfortschritt.
   - Status: RESOLVED durch gemergten PR #395.

2. **GitHub Batch-Claim / MACHINE_READY / Issue-Fortschritt im text-start Receiver**
   - Fehlerklasse: GitHub über Startknopf hinaus.
   - Status: FIX PREPARED in PR #399; noch nicht gemergt.

3. **Mehrere konkurrierende Umbau-PRs**
   - Betroffen: #388, #392, #394, #397, #398, #400, #401.
   - Status: CLOSED / SUPERSEDED. #399 bleibt alleiniger Kandidat.

4. **hardlock-base blockiert den nötigen minimalen Workflow-Rückbau**
   - Fehlercode: `IMMUTABLE_SECURITY_PATH_CHANGE_BLOCKED`.
   - Mergefehler: Required status check `hardlock-base` failing.
   - Ruleset: `21788951`, aktiv, kein Bypass.
   - Status: OPEN / FIRST BLOCKER.

5. **Current-Autorität nach Delta veraltet**
   - Ursache: Main kann den vorbereiteten Workflow-Rückbau nicht mergen; Current+Root-Hash dürfen nicht inkonsistent einzeln geändert werden.
   - Status: BLOCKED durch denselben ersten Blocker; nicht geraten, nicht einseitig verändert.

6. **Gesamtstreckentest nach Rückbau**
   - Status: OFFEN.
   - Kein PASS behauptet.

## PROTOKOLLCHECK
- Fehler: NACHGEHOLT
- Protokoll: NACHGEHOLT
- Warum: PASS
- Current-Autorität: BLOCKED
- Bürotür/Einstiegspunkt: BLOCKED
- Frischecheck: DELTA GEPRÜFT
- Hobbyraum: NICHT BETROFFEN
- Zielvertrag: PASS
- Archiv: NICHT BETROFFEN
- Eine Wahrheit: PASS
- Tests: OFFEN
- Plugins: NICHT BETROFFEN
- Paul/Worker: NICHT BETROFFEN

## Übergabe neuer Chat
EINSTIEGSPUNKT/BÜROTÜR
→ `concept_agent/START_HERE.md`
→ `concept_agent/CONTROL_ENTRY_POINTER.json`

ZUSTÄNDIGE EINE CURRENT-AUTORITÄT
→ `control/startmaster0107/CURRENT_STATE.json`

FRISCHECHECK-BEZUG
→ Main `710bb5d78b884b3e94d397dcba3eb0418b6fe98f`
→ PR #399 Head `cf2494d83f3b71d8810692abaa455ca79ea8dd10`
→ Entrance Gate Run `36116874815` SUCCESS
→ Ruleset `21788951` blockiert Merge wegen `hardlock-base`

AKTUELLER BELASTBARER STAND
→ GitHub-Durable-Event-Schicht aus PR #389 ist auf main zurückgebaut.
→ Minimaler Startknopf-Rückbau ist ausschließlich in PR #399 vorbereitet, noch nicht auf main.
→ Gesamt-E2E nach diesem Rückbau ist nicht gelaufen.

LETZTER SICHERER STAND
→ Main `710bb5d78b884b3e94d397dcba3eb0418b6fe98f`.

ERSTER OFFENER FEHLER/BLOCKER
→ `hardlock-base` / `IMMUTABLE_SECURITY_PATH_CHANGE_BLOCKED` verhindert Merge von PR #399.

EXAKT EINE NEXT ACTION
→ Hardlock-Konflikt für exakt PR #399 über den bereits autorisierten Repository-Regelweg lösen; Diff nicht erweitern. Danach mergen und sofort vollständigen positiven/negativen End-to-End-Test fahren.

VERBINDLICHER ARBEITSWEG
→ GitHub nur Startknopf.
→ Danach bestehender interner Concept-Agent-Workflow.
→ Übergaben müssen Folgeaktion auslösen.
→ Reparierbarer Fehler zurück zum zuständigen Owner, gleicher Artikel, erneut prüfen bis PASS.
→ Kein globaler Abbruch bei reparierbarem Fehler.
→ Kein Publish.

NICHT ANFASSEN
→ keine neue Architektur, kein neuer Runner, keine Alternativroute, keine Qualitäts-/LT-/PPM-/PSERC-/ENDSTEMPEL-Regeländerung.
## KISS Worker-Anschluss 2026-09-25
`RESUME_ALLOWED` ist nicht terminal. Der bereits gebundene Worker führt ausschließlich die hashgebundene `allowed_action` aus, gibt die Rückgabe unmittelbar an `concept_agent/progress_guard.py` zurück und setzt die daraus gebundene Folgeaktion ohne freie Auswahl bis `STOP` fort. Kein neuer Runner, keine Produktionssteuerung über GitHub, kein Publish.
Processanstoß-Fix: Jede gültige `allowed_action` erzeugt genau einen checkpointgebundenen Prozess-Trigger für den bestehenden gebundenen Worker; dessen Rückgabe muss in `concept_agent/progress_guard.py` zurücklaufen. `STOP` erzeugt keinen Trigger.

## Abschlussdelta nach PR #405
- Main: `dee94c3ad5f709881da0efaa9da8e1ca3d00c3a5` (PR #405 gemergt).
- PR #405: exakt ein checkpointgebundener `process_trigger` pro nicht-terminaler `allowed_action`; `STOP` erzeugt keinen Trigger.
- Pflichtprüfungen am PR-Head `496fc76839570f4b9308af2e6f54a3e0dd0cc726`: Deterministic Entrance Gate Run `36136422220` PASS; Immutable Base Hardlock Run `36136418296` PASS.
- Offen: realer End-to-End-Nachweis, dass der bestehende gebundene Worker jeden Trigger tatsächlich konsumiert, genau den gebundenen Prozess startet, die Rückgabe an `progress_guard.py` zurückführt und die Kette bis `STOP` durchläuft.
- Kein Gesamt-PASS bis zu diesem realen Nachweis.
## PR #408 — Live Outer Worker Trigger
- Minimalfix ausschließlich im bestehenden Concept-Agent-Routing: jede nicht-terminale äußere Stufe bindet jetzt denselben BOUND_CHAT_WORKER mit genau einem hashgebundenen process_trigger, sofortiger Ausführungspflicht und verpflichtender Rückkehr in full_workflow_gate.py.
- Keine Änderung an Recherche-/Artikelregeln, LT 6.8, PPM 6.7.9, Repair, PSERC, ENDSTEMPEL oder Publish.


## PR #410 — Startpunkt unmittelbar vor RESEARCH_REQUIRED
- Ausschließlich Einstiegskorrektur: `CONCEPT_AGENT_INTAKE_READY` ist für den bereits aktiven Chat nicht terminal.
- Ohne Nutzer-Zwischenmeldung sofort `RESEARCH_REQUIRED`; danach bleibt die bestehende NO-STOP-/Worker-/Prüfkette unverändert.
- Keine Änderung an Übergaben, Workern, LT 6.8, PPM 6.7.9, Repair, PSERC, ENDSTEMPEL oder Publish.

## PR #412 — Gebundener Arbeitszettel im WRITE_DRAFT-Trigger
- Minimalfix ausschließlich an der bestehenden Chat-Worker-Übergabe: Bei `WRITE_DRAFT` wird genau das bereits maschinell gebundene aktuelle Work-Item mitgegeben.
- Keine freie Artikel-, Regel-, Link- oder Stufenauswahl; LT 6.8, PPM 6.7.9, Repair, PSERC, ENDSTEMPEL und Publish bleiben unverändert.

## Minimalfix Arbeitsstand + durchgehende Übergaben 2026-09-25
- Kein Architekturumbau, keine neue Route, kein neuer Runner.
- Ein bereits vorhandener gültiger Produktions-Checkpoint wird beim erneuten Einstieg weiterverwendet und nicht durch einen neuen Anfangs-Checkpoint ersetzt.
- Jede nicht-terminale Übergabe bleibt im selben bestehenden Ablauf; der gebundene Worker setzt vorwärts sowie nach Repair/Rückgabe unmittelbar mit der nächsten gebundenen Aktion fort.
- Nur der vorhandene terminale STOP beendet den Lauf.
- Fachlogik, Artikelregeln, LT 6.8, PPM 6.7.9, PSERC, ENDSTEMPEL und Publish bleiben unverändert.


## Nachholprüfung nach PR #413 — 2026-09-25

Status dieses Abschnitts: Historie/Nachweis. **Keine CURRENT-Autorität und keine eigene NEXT-ACTION-Wahrheit.**

- PR #413 `Restore current-state resume and no-stop handoffs` ist gemergt.
- Merge-Commit / aktuelles main: `20488acc7d371765df99573e74a04e519adaccdd`.
- Der Merge ist auf fünf Dateien begrenzt: `concept_agent/START_HERE.md`, `concept_agent/full_workflow_gate.py`, `concept_agent/production_bridge.py`, `concept_agent/progress_guard.py`, dieses Protokoll.
- Geschützte globale Start-/Root-Dateien wurden nicht verändert.
- Ein vorhandener gültiger Produktions-Checkpoint wird beim Wiedereinstieg weiterverwendet; kein Rückfall auf einen neuen Anfangs-Checkpoint.
- Jede nicht-terminale Übergabe bleibt im selben bestehenden Ablauf. Das gilt vorwärts sowie bei Repair/Rückgabe. Nur `STOP` ist terminal.
- Artikel-/Qualitätsregeln, LT 6.8, PPM 6.7.9, PSERC, ENDSTEMPEL und Publish wurden nicht geändert.

### Frischecheck nach Merge
- `concept_agent/START_HERE.md` und `concept_agent/CONTROL_ENTRY_POINTER.json` routen weiterhin eindeutig auf genau eine Current-Autorität: `control/startmaster0107/CURRENT_STATE.json`.
- Die technische Hashbindung zwischen `PFERDE_ATELIER_START_HERE.json` und `CURRENT_STATE.json` ist auf main weiterhin konsistent.
- Die Current-Autorität selbst enthält jedoch noch den Vor-PR-#413-Stand `CONCEPT_AGENT_PROCESS_TRIGGER_BOUND_EXECUTION_PROOF_OPEN` und die alte NEXT ACTION `PROVE_EXISTING_BOUND_PROCESS_TRIGGER_EXECUTION_END_TO_END`.
- Damit ist die Current-Autorität nach dem realen Merge #413 **inhaltlich veraltet**.
- Eine isolierte Änderung von `CURRENT_STATE.json` ist verboten, weil deren SHA-256 in der geschützten `PFERDE_ATELIER_START_HERE.json` gebunden ist. Beides muss gemeinsam konsistent bleiben; der geschützte Root-Pfad darf nicht durch eine Nebenroute umgangen werden.

### Erster offener Blocker
`CURRENT_AUTHORITY_NOT_SYNCED_AFTER_PR413`

Der fachliche Fix liegt auf main, aber die einzige Current-Autorität ist noch nicht auf diesen Stand nachgezogen.

### Historisch damals gebundene NEXT ACTION — nicht Current
Den gemergten PR-#413-Stand über den **bereits vorgesehenen autorisierten Current/Root-Synchronisationsweg** in die eine Current-Autorität nachziehen, ohne neuen Weg, neue Architektur, neue Produktionssteuerung oder einseitige Hash-Änderung. Erst danach darf die daraus neu gebundene NEXT ACTION ausgeführt werden.

### Tests / PASS
- Für PR #413 wurden keine zusätzlichen fachlichen Gesamtstreckentests angefordert oder ausgeführt.
- Der Merge selbst ist kein Gesamt-E2E-Nachweis.
- Deshalb kein neuer Gesamt-PASS behauptet.


## Current-Synchronisierung nach PR #413 — 2026-09-25

Status dieses Abschnitts: Historie/Nachweis. **Keine CURRENT-Autorität und keine eigene NEXT-ACTION-Wahrheit.**

- Current-Synchronisierung vorbereitet für den bereits gemergten PR #413.
- Einzige Current-Autorität bleibt `control/startmaster0107/CURRENT_STATE.json`.
- Root `control/startmaster0107/PFERDE_ATELIER_START_HERE.json` wird ausschließlich mit dem dazugehörigen neuen Current-SHA-256 nachgezogen; keine Startlogik wird verändert.
- Current nennt keinen geratenen Artikelstand. Der operative Laufstand darf ausschließlich aus einem vorhandenen gültigen `CONCEPT_AGENT_CURRENT_PROGRESS_V1`-Checkpoint stammen.
- Fehlt ein gültiger Checkpoint, gilt STOP/BLOCKED statt Rekonstruktion.
