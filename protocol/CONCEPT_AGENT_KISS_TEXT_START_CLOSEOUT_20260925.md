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

## PR #417 — Frischer Batch vor Produktions-Checkpoint
- Historiennachweis, keine Current-Autorität.
- Funktionaler Minimalfix ausschließlich in `concept_agent/intake_bridge.py`: vorhandenen gültigen Produktions-Checkpoint fortsetzen; existiert vor Beginn der Produktion noch keiner, unmittelbar mit `RESEARCH_REQUIRED` fortsetzen. Nach begonnener Produktion bleibt fehlender Checkpoint fail-closed ohne Rekonstruktion.
- Keine neue Route, kein Runner, kein Workflow, kein Codex/API, keine Änderung an Artikel-/Qualitätsregeln, LT 6.8, PPM 6.7.9, PSERC, ENDSTEMPEL oder Publish.

## Abschluss-/Nachholprüfung 2026-09-26 — realer Worker-Fortsetzungsblocker

Status dieses Abschnitts: **Historie/Nachweis, keine CURRENT-Autorität, keine eigene NEXT ACTION.**

- Frisch geprüfter Main: `17e5e32c5303e6732bbab0845ae532900ac5f527`.
- PR #416 gemergt: Start-Intake bindet `BOUND_CHAT_WORKER`.
- PR #417 gemergt: frischer Batch darf vor Recherche ohne Produktions-Checkpoint mit `RESEARCH_REQUIRED` fortsetzen.
- Letzter realer Zentralstart: Run `36199051596` = SUCCESS.
- Letzter realer Pferdeatelier-Empfänger: Run `36199100455` = SUCCESS.
- Receipt des Empfängers: 16er-Batch, `CONCEPT_AGENT_INTAKE_READY`, `BOUND_CHAT_WORKER`, `continuation_required=true`, erste Aktion `RESEARCH_REQUIRED`, vor Recherche kein Produktions-Checkpoint erforderlich.
- Der Empfängerlauf endet danach mit Upload von Intake/Receipt. Für diesen Lauf wurde kein nachfolgender gültiger `CONCEPT_AGENT_CURRENT_PROGRESS_V1`-Checkpoint und kein späterer Artikelproduktionsfortschritt gefunden.
- Aktueller fachlicher Befund: reale Konsumption/Ausführung der nicht-terminalen Worker-Fortsetzung nach Intake ist weiterhin offen. Trigger-/Pflichtfelder sind kein Ausführungsnachweis.
- Der verlangte reale 1:1-Gesamtlauf über Start → echte Workeraktion → Rückgabe → nächste Aktion → Repair/Rückweg → PSERC → ENDSTEMPEL → vertraglichen STOP wurde **noch nicht ausgeführt**. Kein Gesamt-PASS.
- Die einzige Current-Autorität auf main ist nach #416/#417 und dem realen Lauf inhaltlich veraltet. Reiner Current-/Root-Sync wurde als PR #418 vorbereitet.
- PR #418 ist aktuell durch den bestehenden `hardlock-base` blockiert: `IMMUTABLE_SECURITY_PATH_CHANGE_BLOCKED` für `control/startmaster0107/PFERDE_ATELIER_START_HERE.json`. Ruleset 21788951 ist aktiv, `bypass_actors=[]`, `current_user_can_bypass=never`.
- Deshalb bleibt die operative Current-Wahrheit auf main bis zur autorisierten Root-/Current-Synchronisierung unverändert; dieser Protokollabschnitt ersetzt sie ausdrücklich nicht.
- Keine neue Architektur, kein Runner, kein Codex-/API-Weg, keine GitHub-Produktionssteuerung, keine Änderung an Artikel-/Qualitätsregeln, LT 6.8, PPM 6.7.9, PSERC, ENDSTEMPEL oder Publish.

## PR #421 — Vollständiger Worker-Handoff-Regressionsnachweis
- Minimalfix bleibt ausschließlich die Wiederherstellung der bereits in PR #410 bewiesenen Regel: `CONCEPT_AGENT_INTAKE_READY` ist für den bereits aktiven Chat kein Stop-/Antwortpunkt; die exakt gebundene Aktion wird ohne Nutzer-Zwischenmeldung konsumiert.
- Test gegen die bytegenau per Git-Blob-Hash verifizierten aktuellen Handoff-Module des PR-Heads: `intake_bridge.py`, `full_workflow_gate.py`, `progress_guard.py`, `universal_reentry_guard.py`.
- Reales 16er-Start-Receipt aus Run 36199100455 stimmt exakt mit dem aktuellen `_start_receipt` überein.
- Ein zusammenhängender 16er-Handoff-Lauf konsumierte 62 nicht-terminale Übergaben, davon 55 Progress-Handoffs: Start → RESEARCH_REQUIRED → RESEARCH_BOUND → AUTHORING_BOUND → 16 Artikel → LT 6.8 → PPM 6.7.9 → erzwungener LT-Repair-Rückweg → Recheck → erzwungener PPM-Repair-Rückweg → LT-Recheck → PPM-Recheck → PSERC → ENDSTEMPEL → hashgebundene Finaldatei → terminales STOP.
- Negativ: manipulierter Checkpoint wurde fail-closed blockiert; terminales STOP erzeugte keinen weiteren Trigger.
- Teststatus: PASS. Keine Produktionslogik, Qualitätsregel, LT-6.8-, PPM-6.7.9-, PSERC-, ENDSTEMPEL- oder Publish-Änderung.

## Abschluss-/Nachholprüfung 2026-09-26 — PR #421 + jüngster Realstart + Execution-Workspace

Status dieses Abschnitts: **Historie/Nachweis, keine CURRENT-Autorität und keine eigene NEXT ACTION.**

### Frischecheck / Delta
- Bürotür `concept_agent/START_HERE.md` und Pointer `concept_agent/CONTROL_ENTRY_POINTER.json` routen weiterhin eindeutig auf genau eine Current-Autorität: `control/startmaster0107/CURRENT_STATE.json`.
- Autoritativer Zielvertrag unverändert: `control/startmaster0107/ZIELVERTRAG_REASONING_MEDIUM_MAX_STARTMASTER0107.json` mit Ziel `MAXIMIZE_MEDIUM_WITHOUT_ANY_GATE_OR_QUALITY_CHANGE`.
- Aktueller Main vor dieser Nachholsynchronisierung: `c2155b694dc46fc7120038d43d82e0b0faf73286`.
- Seit der bisher in Current gebundenen Live-Evidence `17e5e32...` lag relevantes Delta vor; deshalb wurde ausschließlich dieses Delta geprüft.

### Tatsächlich erledigt / nachgewiesen
- PR #421 ist gemergt: `c2155b694dc46fc7120038d43d82e0b0faf73286`.
- PR #421 ändert keine Produktions- oder Qualitätslogik. Er stellt die bereits vorhandene aktive Chat-Konsumption nach `CONCEPT_AGENT_INTAKE_READY` wieder her und ergänzt einen vollständigen Handoff-Regressionslauf.
- Der PR-#421-Test konsumiert die gebundene Kette durch Recherche-/Authoring-Handoffs, 16 Artikel, LT-/PPM-Reparaturrückwege, PSERC, ENDSTEMPEL, Finaldatei und terminales STOP. Das ist **Test-Evidence**, kein realer Produktions-E2E.
- Jüngster realer zentraler Start: `36233010823` = SUCCESS.
- Jüngster realer Receiver: `36233018969` = SUCCESS auf Main `c2155b69...`.
- Receiver-Receipt: Batch `df59b8428c5e3f0750c5523091c00a1172975109823ee816d2234cf9052505d0`, 16 Artikel, `CONCEPT_AGENT_INTAKE_READY`, `BOUND_CHAT_WORKER`, `continuation_required=true`, `fresh_batch_first_action=RESEARCH_REQUIRED`, `production_checkpoint_required_before_research=false`, `publish_allowed=false`.
- Für diesen Realstart wurde kein nachfolgender gültiger `CONCEPT_AGENT_CURRENT_PROGRESS_V1`-Checkpoint und kein vertraglicher STOP nachgewiesen.
- PR #422 (`Restore bound worker workspace in existing text-start handoff`) wurde geprüft und **geschlossen, nicht gemergt**. Grund: Er hätte die geschützte `.github/workflows/text-start-pferdeatelier.yml` verändert und damit genau den verbotenen GitHub-/Startworkflow-Transportweg geschaffen.
- Die aktuelle Chat-Ausführungsumgebung besitzt keinen gemounteten Current-Main-Repository-Checkout. Die gebundene PPM-6.7.9-ZIP liegt auf Main (Git-Blob `151e9d6f908453dfc5b4acb497c4927a3f03c940`, 1.614.485 Bytes, gebundener SHA-256 `acbda93bd1c4292de7aaf88db2195631103991ff508b36c88cb694714818abd1`), kann vom verfügbaren GitHub-Textconnector aber nicht als Binärbytes in den aktuellen Worker-Container materialisiert werden; direkter Raw-Netzabruf ist in dieser Ausführungsumgebung ebenfalls nicht verfügbar.
- Historische/diagnostische Läufe zeigen, dass der unveränderte LT-/PPM-Kern bei vorhandenem vollständigem Checkout ausführbar ist. Diese historischen Wege sind Evidence, **keine Current-/Produktionsroute**.

### Erster offener Fehler / Blocker
`BOUND_CHAT_WORKER_CANONICAL_EXECUTION_WORKSPACE_NOT_AVAILABLE`

Nicht der Handoff-Vertrag ist jetzt der erste belegte offene Punkt. PR #421 deckt dessen Semantik im Test ab. Offen ist die reale Ausführungsbindung: Der gebundene Chat-Worker benötigt den bestehenden kanonischen Repository-Arbeitsraum mit den unveränderten echten Prüfern, ohne dass dafür text-start oder GitHub zum Produktionscontroller umgebaut werden.

### Exakt eine fachliche NEXT ACTION
Die NEXT ACTION steht ausschließlich in `control/startmaster0107/CURRENT_STATE.json`. Dieses Protokoll wiederholt sie nicht als zweite Autorität.

### Nicht verändert
- keine neue Architektur;
- kein neuer Runner;
- kein Codex-/OpenAI-API-Produktionsweg;
- kein GitHub-Produktionsfortschritt;
- kein text-start-Workflow-Fix;
- keine Artikel-/Qualitätsregeln;
- kein LanguageTool-6.8-, PPM-6.7.9-, PSERC- oder ENDSTEMPEL-Code;
- kein Publish;
- keine Plugins.

### Tests / PASS
- PR #421 Handoff-Regressionskette: PASS als Test-Evidence.
- Jüngster echter Start/Receiver: PASS bis `CONCEPT_AGENT_INTAKE_READY`.
- Realer End-to-End-Lauf vom einmaligen Start über echte Workerarbeit, echte LT-/PPM-Reparaturkette, PSERC, ENDSTEMPEL bis STOP: **OFFEN**.
- Deshalb **kein Gesamt-PASS**.

### PROTOKOLLCHECK
- Fehler: NACHGEHOLT
- Protokoll: NACHGEHOLT
- Warum: PASS
- Current-Autorität: BLOCKED
- Bürotür/Einstiegspunkt: PASS
- Frischecheck: DELTA GEPRÜFT
- Hobbyraum: NICHT BETROFFEN
- Zielvertrag: PASS
- Archiv: NICHT BETROFFEN
- Eine Wahrheit: PASS
- Tests: OFFEN
- Plugins: NICHT BETROFFEN
- Paul/Worker: BOUND_CHAT_WORKER BETROFFEN; kein Parallelbranch als Current

### Nachtrag — Current-Synchronisierung PR #423 blockiert
- Der Versuch, ausschließlich `CURRENT_STATE.json`, den dazugehörigen Root-Hash und dieses Protokoll konsistent nachzuziehen, wurde als PR #423 erstellt.
- Deterministic Entrance Gate Run `36235999525`: **PASS**.
- Immutable Base Hardlock Run `36235999516`: **FAIL**.
- Exakter Fehler: `IMMUTABLE_SECURITY_PATH_CHANGE_BLOCKED`.
- Betroffener immutable Pfad: `control/startmaster0107/PFERDE_ATELIER_START_HERE.json`.
- Ursache: `CURRENT_STATE.json` kann nicht isoliert geändert werden, weil dessen SHA-256 im Root gebunden ist; der notwendige Root-Hash darf unter der aktuellen Hardlock-Regel nicht geändert werden.
- Es wurde kein Bypass, keine einseitige Current-Änderung und keine Ersatz-Current erzeugt.
- Folge: Die einzige Current-Autorität auf `main` bleibt inhaltlich hinter dem frisch geprüften Delta zurück. Nach den Campusregeln ist der Abschlussstatus deshalb **CURRENT-AUTORITÄT BLOCKED**, bis der vorgesehene autorisierte Root-/Current-Synchronisationsweg wieder zulässig ist.
- Dieses Protokoll bleibt ausschließlich Evidence/Historie und ersetzt Current ausdrücklich nicht.

## Nachholung 2026-09-26 — bewiesene Workspace-Recovery im bestehenden Reentry wiederhergestellt

Ursache:
- Die bereits bewiesene Capsule-Recovery aus `c2bde4d8ab81d3786a474d18ae8958d369637377` wurde in `5d0b38dd367c47154bd6dedc3f59b05259857ad8` beim Binden des Outer-Gates ersetzt statt zusammengeführt.
- Dadurch blieb die äußere Checkpoint-/Stage-Bindung erhalten, aber die bestehende `SYSTEM4_WORKSPACE_RECOVERY_CAPSULE_V1`-Wiederaufnahme war im aktuellen Concept-Agent-Handoff nicht mehr vollständig transportiert.

Fix PR #426:
- heutige `CONCEPT_AGENT_UNIVERSAL_REENTRY_DECISION_V2`- und `full_workflow_gate`-Bindung unverändert beibehalten;
- bewiesene Workspace-Capsule-Validierung und Inner-Phase-Kontinuität wieder integriert;
- `START_BOUND_ARTICLE_WORKER` für den ersten gebundenen Artikel-Workspace wiederhergestellt;
- `RUN_CHECKER` und `REPAIR_DRAFT` fail-closed ohne verifizierte Workspace-Capsule;
- dieselbe Capsule wird im bestehenden `process_trigger` an denselben gebundenen Worker weitergereicht;
- Repair → Recheck bleibt derselbe Artikel/Workspace;
- bestehende gebundene PSERC-/ENDSTEMPEL-Aktionen bleiben im vorhandenen Outer-/Batch-Pfad;
- kein neuer Runner, kein neuer Controller, keine neue Produktionsroute.

Nicht verändert:
- text-start;
- LT 6.8;
- PPM 6.7.9;
- PSERC;
- ENDSTEMPEL;
- Text-/SEO-/Qualitätsregeln;
- Plugins;
- Publish-Regel.

Entwicklungsnachweis:
- temporärer, ausschließlich auf dem Reparaturbranch verwendeter Testworkflow wurde nach dem Test vollständig wieder entfernt;
- Reentry-Capsule-Regressionsmatrix: 4/4 PASS;
- Current-Production-Regression einschließlich 16 Artikel, LT-/PPM-Repair, Recheck, PSERC, ENDSTEMPEL und STOP: 13/13 PASS;
- Entwicklungs-Testlauf: `36239622721 = SUCCESS`;
- finaler Live-Code enthält daraus keinen neuen GitHub-Workflow, keine Codex-Abhängigkeit und keine API-Abhängigkeit.

