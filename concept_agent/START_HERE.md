# Pferde Atelier — Konzept 5 / Concept Agent

Diese Datei ist nur die Bürotür.

## Einziger Einstieg

Immer zuerst:

`concept_agent/CONTROL_ENTRY_POINTER.json`

Der Pointer entscheidet die Phase **maschinell**. Der Chat darf sie nicht wählen.

### Vor MACHINE_READY

Autorität bleibt unverändert:

`control/startmaster0107/CURRENT_STATE.json`

`text-start` bleibt ausschließlich der Startknopf.

### Nach MACHINE_READY

Für den aktuellen Batch aus

`concept_agent/current/PSERC_METADATA_SNAPSHOT.json`

muss exakt ein GitHub-Issue

`TEXT_START_BATCH_CLAIM:<batch_sha256>`

existieren und darin exakt ein passender `TEXT_START_MACHINE_READY`-Beleg von
`github-actions[bot]`.

Sobald dieser Beleg existiert, ist ein zweites `text-start` verboten. Der veränderliche Produktionsfortschritt kommt danach **nicht mehr** aus `CURRENT_STATE.json`, sondern ausschließlich aus:

`concept_agent/durable_event_log.py`

Damit kann die alte Pre-MACHINE_READY-`next_action` in `CURRENT_STATE.json` nach einem erfolgreichen Start nicht wieder zur Produktionsentscheidung werden.

## Dauerhaftes Zickzack-Protokoll

Nach MACHINE_READY ist nur die append-only Ereigniskette im gebundenen Batch-Issue Fortschrittsautorität.

Ein gültiger Arbeitsschritt ist ausschließlich ein
`CONCEPT_AGENT_DURABLE_EVENT_V1`
von
`chatgpt-codex-connector[bot]`.

Jedes Event bindet:
- aktuellen Batch;
- fortlaufende Sequenz;
- Hash des vorherigen Events;
- exakt die vorher maschinell erlaubte Aktion;
- Ergebnisbytes bzw. Ergebnis-JSON;
- SHA-256 und Bytegröße;
- `publish_allowed=false`.

Nicht-Bot-Kommentare werden ignoriert und sind niemals Autorität.

Vor jeder produktiven Aktion muss `concept_agent/durable_event_log.py current`:
1. den aktuellen Batch aus dem hashgebundenen PSERC-Metadaten-Snapshot ableiten;
2. den exakten Batch-Claim finden;
3. den MACHINE_READY-Botbeleg prüfen;
4. die komplette Bot-Eventkette ab Event 1 hashverkettet wiederholen;
5. Research-Bindung, Produktions-Binding und Fortschritts-Checkpoint deterministisch rekonstruieren;
6. genau **eine** `allowed_action` ausgeben.

Der Worker darf ausschließlich diese Aktion ausführen und muss das Ergebnis mit dem passenden `seal-*`-Befehl als nächstes Event ausgeben.

Abbruchregel:
- Abbruch vor neuem Bot-Event → letzter sicherer Zustand bleibt aktuell;
- Abbruch nach neuem Bot-Event → ein neuer Worker rekonstruiert exakt daraus;
- fehlendes, manipuliertes, mehrdeutiges oder lückenhaftes Bot-Event → **STOP**.

Der Chat darf:
- Fortsetzung anstoßen;
- den maschinell abgeleiteten Zustand anzeigen.

Der Chat darf nicht:
- Stufe, Artikel, Prüfer oder Reparaturweg wählen;
- Produktionsfortschritt behaupten;
- ein autoritatives Event schreiben;
- aus Chat-Erinnerung rekonstruieren;
- alte Drafts/Recovery-Archive als NEW-Quelle verwenden;
- einen Ersatzweg suchen.

## Unveränderte Produktionsregeln

Nach gebundener Recherche bleibt
`concept_agent/production_bridge.py`
die Produktionsbindung.

Der Fortschritt bleibt
`concept_agent/progress_guard.py`
unter
`concept_agent/universal_reentry_guard.py`.

Unverändert:
- LanguageTool 6.8;
- PPM 6.7.9;
- bestehende Portal-Link-Bindungen;
- PSERC;
- ENDSTEMPEL;
- Artikel-/Qualitätsregeln;
- kein Publish.

Hart verboten:
- historische Produktionswege;
- alte oder Recovery-Artikel als Produktionsquelle;
- `pferde-atelier.de` und Subdomains als Recherchequelle;
- freie Regelsuche;
- freie Linkwahl;
- `GH_TOKEN`, `git push` oder `git remote` als Voraussetzung für Produktionsfortschritt;
- zweites `text-start` nach MACHINE_READY desselben Batches;
- Alternativroute.

Für einen bereits MACHINE_READY befindlichen Batch wird die aktuelle erlaubte Aktion ausschließlich aus der gültigen dauerhaften Ereigniskette abgeleitet.
