# NOTFALL-ÜBERGABE – NEUER CHAT MITTEN IN DER TEXTERSTELLUNG – STARTMASTER0107

## Zweck
Diese Übergabe ist ausschließlich für den Fall gedacht, dass ein Chat während eines aktiven Beitragsbatches voll wird, abbricht oder gewechselt werden muss. Sie verhindert, dass ein neuer Chat den Workflow neu interpretiert, alte Prüfungen wiederholt oder zu früheren Schritten zurückspringt.

## Im neuen Chat exakt so starten
1. GitHub-Repository `hallo-netizen/affiliate-pferdeportal` lesen.
2. `control/CURRENT_STARTMASTER.json` lesen. Keine Erinnerung/Chat-Historie als Navigationsquelle benutzen.
3. Daraus ROOT und CURRENT_STATE lesen und ausschließlich `next_allowed_step` akzeptieren.
4. Wenn CURRENT_STATE einen aktiven Textbatch nennt: dessen `BATCH_CHECKPOINT.json` lesen.
5. Prüfen, dass Batch-ID, gebundene Item-IDs und Input-Hashes zum CURRENT_STATE passen.
6. `completed_item_ids` NICHT erneut bearbeiten, solange deren Inputs/Hashes unverändert sind.
7. Exakt bei `current_item_id/current_gate_id` bzw. `next_item_id` fortsetzen.
8. Den verbindlichen Textprompt `VERBINDLICHER_TEXTERSTELLUNGS_PROMPT_STARTMASTER0107.txt` weiterverwenden. Nicht erneut nach einem Prompt fragen.
9. Während des aktiven Batches keine Zwischenmeldung; interne Checkpoints still fortschreiben.
10. Erst nach vollständigem Batch-Ende eine Abschlussmeldung ausgeben.

## Was ausdrücklich verboten ist
- komplette MASTER-Historie erneut untersuchen, wenn der aktuelle State/Checkpoint eindeutig ist;
- bereits bestandene unveränderte Gates erneut prüfen;
- aus Vorsicht einen früheren Workflowblock neu starten;
- neue Titel-/Keyword-/Qualitäts-/Designregeln erfinden;
- andere Artikel auswählen als im Batch gebunden;
- bei Unsicherheit einen Nebenweg starten;
- Publish ohne bestehende Freigabe.

## Fail-closed
Fehlt der aktuelle Batch-Checkpoint oder passt sein Hash/Batch-ID nicht zum CURRENT_STATE, NICHT raten. Nur diesen konkreten Bindungsfehler melden. Keine Neuplanung.

## Warum der Chatwechsel keinen Qualitätsverlust erzeugt
Der Checkpoint enthält nur Ausführungszustand und Hashbindungen. Er enthält keine eigene Fachlogik. Alle Fach-/Inhalts-/Qualitätsgates bleiben unverändert im bestehenden Workflow. Der neue Chat setzt deshalb nicht nach eigener Interpretation fort, sondern am exakt gespeicherten Gate.

## Unveränderliche Eingangstür
Ein neuer Chat darf die Sicherheitsschicht, AGENTS.md oder GitHub-Workflowdateien nicht ändern. Diese Pfade werden durch den base-branch Hardlock unabhängig vom PR-Inhalt blockiert. Der neue Chat liest ausschließlich aktuellen State und Checkpoint und setzt den vorgebundenen Schritt fort.
