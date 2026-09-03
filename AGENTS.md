# Pferde Atelier – verbindliche Codex-Cloud-Eingangstür

## Workstream-Router – ZUERST anwenden

Vor jeder Aktion muss der Arbeitsstrang bestimmt werden.

### AFFILIATE_ZENTRALE / eBay
Wenn der Auftrag Affiliate-Zentrale, eBay, Awin, ADCELL, idealo, Digistore24 oder Pfade unter `release/affiliate-zentrale/` bzw. `control/release-governance/` betrifft:

- **NICHT** `control/cloud-entry-gate/cloud_entry.py` starten.
- **NICHT** STARTMASTER, `control/CURRENT_STARTMASTER.json` oder `.pferde-capsule/` zur Navigation verwenden.
- Ausschließlich `release/affiliate-zentrale/AGENTS.md` und `control/release-governance/CURRENT_RELEASE.json` als Steuerung verwenden.
- Genau einen Affiliate-Arbeitsstrang bearbeiten.

### STARTMASTER / übrige Portalproduktion
Nur wenn der Auftrag **nicht** zum Affiliate-Workstream gehört, gilt die nachfolgende STARTMASTER-Eingangstür.

## Zwingender STARTMASTER-Start
Vor jeder Suche, Analyse, Dateiöffnung oder Änderung im STARTMASTER-Arbeitsstrang MUSS zuerst exakt dieser Befehl ausgeführt werden:

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

## Verbindlicher STARTMASTER-Step-Abschluss
Nach Ausführung des aktuellen Steps MUSS `.pferde-capsule/RECEIPT.json` exakt gemäß `.pferde-capsule/RECEIPT_SCHEMA.json` geschrieben werden.

Danach MUSS exakt ausgeführt werden:

`python3 control/cloud-entry-gate/cloud_entry.py complete .pferde-capsule/RECEIPT.json`

Nur die Eingangstür darf daraufhin den STARTMASTER-State verändern.

- Bei `STATE_ADVANCED_NEXT_STEP_READY`: ohne Zwischenmeldung sofort die neu materialisierte `.pferde-capsule/INSTRUCTION.txt` abarbeiten und denselben Abschlusszyklus fortsetzen.
- Bei `STEP_TERMINAL_NONPASS`: sofort mit dem dort gebundenen `BLOCKED` oder `USER_ACTION_REQUIRED` stoppen. Keine Alternativroute und keine eigene Lösung.
- Bei `FINAL_STEP_PASS`: am gebundenen finalen Endpunkt stoppen.
- Ein Chat-/Task-Neustart beginnt wieder ausschließlich mit `cloud_entry.py start`; bei unverändertem State wird dasselbe deterministische Ticket erzeugt und kein PASS-Step neu gebunden.

## Aktiver Textbatch / Chatwechsel
Wenn der aktuell gebundene STARTMASTER-Step einen Textbatch ausführt, gilt zusätzlich der bestehende Production-Continuity-Vertrag:
- vorhandenen gebundenen BATCH_CHECKPOINT zuerst verwenden;
- abgeschlossene unveränderte Items nicht erneut bearbeiten;
- exakt am ersten offenen Item/Gate fortsetzen;
- interne Checkpoints still fortschreiben;
- keine Zwischenmeldung während eines aktiven Batches, außer USER_ACTION_REQUIRED oder nicht lokal lösbarem Hard-Fail;
- ein finales Batch-Ergebnis ist nur gültig, wenn `control/production-continuity/production_continuity_guard.py finalize <checkpoint>` PASS liefert.

## WordPress-Prewrite-Hardlock – unmittelbar vor jedem Content-Write
Für jeden STARTMASTER-Schritt, der Artikelinhalt in WordPress schreiben würde, ist unmittelbar vor dem ersten WordPress-Content-Write zwingend genau dieser nachgelagerte Kontroll-Gate auszuführen:

`python3 control/wordpress-prewrite-gate/wordpress_prewrite_gate.py <APPROVED_ENVELOPE.json> <EXACT_WORDPRESS_CANDIDATE.json>`

Dabei gilt fail-closed:
- `<APPROVED_ENVELOPE.json>` muss das bereits im gebundenen Workflow freigegebene/hashgebundene Produktionspaket sein; keine freie Ersatzdatei.
- `<EXACT_WORDPRESS_CANDIDATE.json>` muss exakt das Artefakt enthalten, dessen Artikelkörper unmittelbar danach nach WordPress geschrieben würden; keine Vorschau und kein älterer Zwischenstand.
- Nur `status=PASS` und `wordpress_write_allowed=true` erlauben die Fortsetzung zum bestehenden WordPress-Schreibpfad.
- Bei `BLOCKED`, fehlendem Input, nicht auflösbarer Bindung oder technischem Fehler: sofort vor jedem WordPress-Content-Write stoppen. Keine Ersatzroute, kein Bypass.
- Der Gate ist ausschließlich read-only. Er darf Artikel, Links, Tabellen, Metadaten, Workflow-State oder Upstream-Textproduktion niemals reparieren, ergänzen oder umschreiben.
- Der Gate-PASS muss als Evidence des ausführenden Steps/Receipts erhalten bleiben.

Die Fachregeln dieses Hardlocks liegen ausschließlich in `control/wordpress-prewrite-gate/wordpress_prewrite_gate.py`: nachweisbare Herkunft aus dem freigegebenen Textprozess, vertraglich erforderliche Tabelle und ausschließlich gebundene Linkziele. Die Textproduktion selbst bleibt außerhalb dieses Gates und wird durch ihn nicht verändert.

## Trennung
Die Eingangstür und Continuity-Schicht sind rein technisch. Fach-, Inhalts-, Qualitäts-, Titel-, Keyword-, Design- und sonstige Portalregeln liegen ausschließlich im nachgelagerten Workflow und dürfen hier weder ersetzt noch dupliziert werden.

## Definition of Done
Für STARTMASTER muss vor einem terminalen Abschluss `python3 control/cloud-entry-gate/cloud_entry.py verify` PASS melden. Für Affiliate gilt stattdessen ausschließlich der Affiliate-Release-Guard gemäß `release/affiliate-zentrale/AGENTS.md`.
