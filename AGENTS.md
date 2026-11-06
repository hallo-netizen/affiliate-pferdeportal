# Codex-Arbeitsbereich: Hobby Depot – nur isolierter Testzweig

## EINMALIGE BRANCH-GEBUNDENE AUSNAHME: Hobby Depot Bildtest

**Nur fuer den Pull Request #632** mit Head-Zweig `hobbyroom/hd003-category-tile-image-audit-20261106` gilt dieser Abschnitt als Startanweisung. Alle K0-/Pferdeatelier-Regeln darunter bleiben fuer alle anderen Zweige und Auftraege unveraendert gueltig.

Wenn und nur wenn der aktuelle Codex-Auftrag nachweislich zu diesem PR #632 und dessen Hobby-Depot-Head-Zweig gehoert:

1. **Keinen Pferdeatelier-Cloud-Startbefehl aufrufen.** Der bestehende `control/cloud-entry-gate/cloud_entry.py` ist exklusiv fuer Pferdeatelier. Seine Dateien, States, Workflows und die K0-Texterstellung duerfen weder ausgefuehrt, noch repariert oder veraendert werden. Das gilt auch fuer `control/`, `isolated_system4/`, `.pferde-capsule/` und alle Projektbereiche ausser Hobby Depot.
2. Ausschliesslich die Hobby-Depot-Aufgabe in `protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/DESIGN/CODEX_KATEGORIE_KACHELBILDER_20261106.md` und die zusaetzlichen Hobby-Regeln in `protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/DESIGN/AGENTS.md` bearbeiten.
3. **Schreibrechte nur im Hobby-Bereich** `protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/DESIGN/` fuer Protokolle, generierte Bilder und reine Staging-Dateien. Pruefskripte/CI fuer dieses Bildprojekt nur in `scripts/hobby_*` und `.github/workflows/hobby-*` ablegen. Der Original-Pluginstand `PLUGINS/ISOLIERTE_PLUGINS/HD-003-DESIGN-TEMPLATE-KIT/CURRENT.zip` ist **READ ONLY**.
4. Strikt verboten: Aenderungen an K0, Pferdeatelier-Branch, Campus-Main, fremden Portalen, Plugin-Quellcode, Root-AGENTS, `control/`, WordPress-Live-Instanz oder Produktionsdaten. Auch keine automatischen Merges.
5. Beim Bilderzeugen **keine externen OpenAI-API-Schluessel** verwenden: nur die eingebaute Codex-Bildgenerierung mit ChatGPT-Anmeldung. 20 Hobbys als 20 getrennte Bildauftraege, jedes genau eine durchgehende Szene, keine Collagen; technische und visuelle QA, Bildintegration nur als getestete Staging-Kopie.
6. Vor Ergebnis-Meldung mit `python3 scripts/hobby_codex_scope_guard.py` sicherstellen, dass wirklich keine Aenderung ausserhalb der Hobby-Freigabeliste vorliegt. Bei gesperrtem Imagegen oder anderen nicht behebbaren Hindernissen exakt BLOCKED mit Nachweis melden, ohne an Pferdeatelier auszuweichen.
7. Ergebnisse mit Belegen im PR #632 hinterlassen; die Live-Website bleibt unveraendert.

**Bei jeder anderen Branch-/PR-Zuordnung oder unsicherer Identitaet: STOP, nicht die Hobby-Ausnahme nutzen.** Fuer Pferdeatelier gelten unveraendert die bisherigen folgenden Regeln.

---

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
