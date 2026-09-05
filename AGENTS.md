# Pferde Atelier – verbindliche Codex-Cloud-Eingangstür

Diese Datei gilt repositoryweit für Codex Cloud.

## Zwingender Start
Vor jeder Suche, Analyse, Dateiöffnung oder Änderung im Projekt MUSS zuerst exakt dieser Befehl ausgeführt werden:

`python3 control/cloud-entry-gate/cloud_entry.py start`

Wenn dieser Befehl BLOCKED meldet: sofort stoppen. Keine Alternativprüfung, kein Rücksprung, kein eigener Workflowpfad.

Wenn PASS gemeldet wird:
- ausschließlich `.pferde-capsule/INSTRUCTION.txt` als aktuellen Arbeitsauftrag verwenden;
- `TICKET.json`, `RECEIPT_SCHEMA.json` und `CAPSULE_MANIFEST.json` sind technisch bindend;
- die in `.pferde-capsule/inputs/` materialisierten Dateien sind die hashgebundenen Pflichtinputs;
- das Repository darf nur zur Ausführung des aktuell gebundenen Steps gelesen/geändert werden, wenn `repo_worktree_available_for_bound_step=true` ist;
- `control/CURRENT_STARTMASTER.json`, STARTMASTER-State, andere Step-Bundles, Protokolle und alte Historie dürfen vom Worker niemals zur Workflow-Navigation benutzt werden;
- keinen nächsten Workflow-Schritt auswählen, wiederholen, überspringen oder vorziehen;
- keine State- oder Workflowänderung eigenständig vornehmen;
- bereits bestandene unveränderte PASS-Stufen nicht erneut prüfen.

## Harte Arbeitsort-Sperre – Tresor/Archiv sind niemals Werkbank

Der Notfall-Tresor, Campus-Archiv, Git-Mirror, Backup-Bundles und daraus direkt geöffnete lokale Worktrees sind ausschließlich Sicherungs-/Beleg-/Restore-Quellen.

Verboten:
- Runner, Tests, Reparaturen oder Produktion direkt aus `Campus-Tresor` oder `Campus-Archiv` starten;
- einen Bare-Git-Mirror als Arbeitsrepository verwenden;
- einen Worktree mit lokalem Mirror als `origin` als offiziellen Arbeitsstand verwenden;
- Tresor/Archiv als Ersatzroute benutzen, wenn der normale gebundene Workflow BLOCKED ist.

`cloud_entry.py start`, `verify` und `complete` prüfen diese Grenze fail-closed.

Zulässige Wiederherstellung:
Backup/Mirror nur gemäß Tresor-Wiederaufbau lesen → in einen frischen Arbeits-Worktree außerhalb Tresor/Archiv wiederherstellen → offizielles GitHub-`origin` binden → normale Cloud-Eingangstür neu ausführen.

Ein Backup-PASS ist niemals ein Arbeits-PASS.

## Zusätzliche Pflicht auf `paul/*`-Branches

Die bestehende Cloud-Eingangstür bleibt immer Schritt 1.

Unmittelbar NACH einem erfolgreichen
`python3 control/cloud-entry-gate/cloud_entry.py start`
und VOR jeder Paul-Analyse oder Änderung muss der aktuelle Git-Branch geprüft werden.

Wenn er mit `paul/` beginnt, MUSS exakt ausgeführt werden:

`python3 control/paul-scope-gate/paul_scope_gate.py start`

Nur bei `PAUL_BOOTSTRAP_PASS` darf Paul weiterarbeiten.

Der Paul-Scope-Gate:
- liest die aktuelle Arbeitszuweisung frisch vom offiziellen Campus;
- blockiert ohne aktive Paul-Zuweisung mit `PAUL_NOT_ASSIGNED`;
- blockiert falschen Branch/technische Basis;
- bindet den ausdrücklich erlaubten Schreibbereich;
- materialisiert `.paul-capsule/` nur als temporären, hashgebundenen READ-ONLY-Snapshot.

WICHTIG:
`.pferde-capsule/INSTRUCTION.txt` bleibt die einzige Workflow-Instruktion.
`.paul-capsule/` ersetzt sie NICHT und wählt keinen Workflow-Schritt; sie begrenzt nur Pauls aktuelle Campus-Berechtigung und liefert den frisch gelesenen Kontext.

Vor jedem Paul-Abschluss und BEVOR `cloud_entry.py complete` ausgeführt wird, MUSS zusätzlich exakt ausgeführt werden:

`python3 control/paul-scope-gate/paul_scope_gate.py verify`

Bei `STALE_ASSIGNMENT_BLOCKED`, `PAUL_WRITE_SCOPE_BLOCKED` oder jedem anderen Nicht-PASS:
sofort stoppen; kein Receipt-/Workflow-Abschluss auf veraltetem oder unzulässigem Stand.

## Verbindlicher Step-Abschluss
Nach Ausführung des aktuellen Steps MUSS `.pferde-capsule/RECEIPT.json` exakt gemäß `.pferde-capsule/RECEIPT_SCHEMA.json` geschrieben werden.

Danach MUSS exakt ausgeführt werden:

`python3 control/cloud-entry-gate/cloud_entry.py complete .pferde-capsule/RECEIPT.json`

Nur die Eingangstür darf daraufhin den State verändern.

- Bei `STATE_ADVANCED_NEXT_STEP_READY`: ohne Zwischenmeldung sofort die neu materialisierte `.pferde-capsule/INSTRUCTION.txt` abarbeiten und denselben Abschlusszyklus fortsetzen.
- Bei `STEP_TERMINAL_NONPASS`: sofort mit dem dort gebundenen `BLOCKED` oder `USER_ACTION_REQUIRED` stoppen. Keine Alternativroute und keine eigene Lösung.
- Bei `FINAL_STEP_PASS`: am gebundenen finalen Endpunkt stoppen.
- Ein Chat-/Task-Neustart beginnt wieder ausschließlich mit `cloud_entry.py start`; bei unverändertem State wird dasselbe deterministische Ticket erzeugt und kein PASS-Step neu gebunden.

## Aktiver Textbatch / Chatwechsel
Wenn der aktuell gebundene Step einen Textbatch ausführt, gilt zusätzlich der bestehende Production-Continuity-Vertrag:
- vorhandenen gebundenen BATCH_CHECKPOINT zuerst verwenden;
- abgeschlossene unveränderte Items nicht erneut bearbeiten;
- exakt am ersten offenen Item/Gate fortsetzen;
- interne Checkpoints still fortschreiben;
- keine Zwischenmeldung während eines aktiven Batches, außer USER_ACTION_REQUIRED oder nicht lokal lösbarem Hard-Fail;
- ein finales Batch-Ergebnis ist nur gültig, wenn `control/production-continuity/production_continuity_guard.py finalize <checkpoint>` PASS liefert.

## Trennung
Die Eingangstür und Continuity-Schicht sind rein technisch. Fach-, Inhalts-, Qualitäts-, Titel-, Keyword-, Design- und sonstige Portalregeln liegen ausschließlich im nachgelagerten Workflow und dürfen hier weder ersetzt noch dupliziert werden.

## Definition of Done
Vor einem terminalen Abschluss muss `python3 control/cloud-entry-gate/cloud_entry.py verify` PASS melden. Ein Ergebnis ohne gültigen Receipt-Abschluss ist nicht workflowgültig.
