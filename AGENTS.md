# Pferde Atelier – verbindliche Codex-Cloud-Eingangstür

Diese Datei gilt repositoryweit für Codex Cloud.

## Zwingender Start
Vor jeder Suche, Analyse, Dateiöffnung oder Änderung im Projekt MUSS zuerst exakt dieser Befehl ausgeführt werden:

`python3 control/cloud-entry-gate/cloud_entry.py start`

Wenn dieser Befehl BLOCKED meldet: sofort stoppen. Keine Alternativprüfung, kein Rücksprung, kein eigener Workflowpfad.

Wenn PASS gemeldet wird:
- ausschließlich die erzeugte `.pferde-capsule/INSTRUCTION.txt` abarbeiten;
- ausschließlich die in `.pferde-capsule/` materialisierten Eingaben als Arbeitskontext verwenden;
- keine alte MASTER-Historie, Protokolle oder andere Projektdateien zur Navigation heranziehen;
- keinen nächsten Workflow-Schritt auswählen, wiederholen, überspringen oder vorziehen;
- keine State- oder Workflowänderung eigenständig vornehmen;
- bereits gebundene PASS-Stufen nicht erneut prüfen;
- nur den aktuellen Step abschließen und dessen gefordertes Ergebnis/Receipt liefern.

## Aktiver Textbatch / Chatwechsel
Wenn der aktuelle State einen Textbatch bindet, gilt zusätzlich:
- den gebundenen BATCH_CHECKPOINT zuerst lesen;
- abgeschlossene unveränderte Items nicht erneut bearbeiten;
- exakt am ersten offenen Item/Gate fortsetzen;
- interne Checkpoints still fortschreiben;
- keine Zwischenmeldung während eines aktiven Batches, außer USER_ACTION_REQUIRED oder nicht lokal lösbarem Hard-Fail;
- ein finales Batch-Ergebnis ist nur gültig, wenn `control/production-continuity/production_continuity_guard.py finalize <checkpoint>` PASS liefert.

## Trennung
Die Eingangstür und Continuity-Schicht sind rein technisch. Fach-, Inhalts-, Qualitäts-, Titel-, Keyword-, Design- und sonstige Portalregeln liegen ausschließlich im nachgelagerten Workflow und dürfen hier weder ersetzt noch dupliziert werden.

## Definition of Done
Vor Abschluss jeder Codex-Aufgabe muss `python3 control/cloud-entry-gate/cloud_entry.py verify` PASS melden. Ein Ergebnis ohne diesen PASS ist nicht workflowgültig.

<!-- NEGATIVE SELFTEST ONLY: immutable path mutation must be blocked; never merge -->
