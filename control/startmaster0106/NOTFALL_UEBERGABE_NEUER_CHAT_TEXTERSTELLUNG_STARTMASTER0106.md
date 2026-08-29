# NOTFALL-ÜBERGABE – NEUER CHAT MITTEN IN DER TEXTERSTELLUNG – STARTMASTER0106

## Zweck
Diese Übergabe gilt ausschließlich, wenn ein Chat während eines aktiven Beitragsbatches voll wird, abbricht oder gewechselt werden muss. Sie verhindert Neuinterpretation, Wiederholungsprüfungen und Rücksprünge.

## Im neuen Chat exakt so starten
1. GitHub-Repository `hallo-netizen/affiliate-pferdeportal` lesen.
2. `control/CURRENT_STARTMASTER.json` lesen. Erinnerung/Chat-Historie niemals als Navigationsquelle benutzen.
3. Daraus ROOT und CURRENT_STATE lesen und ausschließlich `next_allowed_step` akzeptieren.
4. Wenn CURRENT_STATE einen aktiven Textbatch nennt: dessen `BATCH_CHECKPOINT.json` lesen.
5. Batch-ID, gebundene Item-IDs und Input-Hashes gegen CURRENT_STATE prüfen.
6. `completed_item_ids` NICHT erneut bearbeiten, solange deren Inputs/Hashes unverändert sind.
7. Exakt bei `current_item_id/current_gate_id` bzw. `next_item_id` fortsetzen.
8. Den bindenden Prompt `control/startmaster0106/VERBINDLICHER_TEXTERSTELLUNGS_PROMPT_STARTMASTER0106.txt` weiterverwenden. Nicht erneut nach einem Prompt fragen.
9. Während des aktiven Batches keine Zwischenmeldung; interne Checkpoints still fortschreiben.
10. Erst nach vollständigem Batch-Ende eine Abschlussmeldung ausgeben.

## Verboten
- komplette MASTER-Historie neu untersuchen, wenn State/Checkpoint eindeutig ist;
- bereits bestandene unveränderte Gates erneut prüfen;
- aus Vorsicht einen früheren Workflowblock neu starten;
- neue Titel-/Keyword-/Qualitäts-/Designregeln erfinden;
- andere Artikel auswählen als im Batch gebunden;
- einen Nebenweg starten;
- Publish ohne bestehende Freigabe.

## Fail-closed
Fehlt der aktuelle Batch-Checkpoint oder passt sein Hash/Batch-ID nicht zum CURRENT_STATE: NICHT raten. Nur den konkreten Bindungsfehler melden. Keine Neuplanung.

## Qualitätsneutralität
Der Checkpoint enthält nur Ausführungszustand und Hashbindungen. Er enthält keine eigene Fachlogik. Alle Fach-/Inhalts-/Qualitätsgates bleiben unverändert im bestehenden Workflow.
