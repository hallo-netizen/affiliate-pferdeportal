# Pferde Atelier — Konzept 5 / Concept Agent

Autoritativer Eingang für neue Artikel-Batches: `concept_agent/intake_bridge.py`.

## Vorbereitung

`python3 concept_agent/intake_bridge.py prepare <PSERC_METADATA_SNAPSHOT.json> <CONCEPT_AGENT_INTAKE.json>`

Nur `CONCEPT_AGENT_INTAKE_READY` erlaubt den nächsten Schritt.

## Feste Ausführung

Die Artikelproduktion selbst wird ausschließlich durch `concept_agent/runner.py` gesteuert.

Der Runner:
1. übernimmt den bereits gebundenen Arbeitsauftrag unverändert;
2. gibt immer nur den aktuellen Artikel an den Schreibagenten;
3. erlaubt bei einem Prüffehler nur die Reparatur desselben Artikels;
4. gibt den nächsten Artikel erst nach PASS frei;
5. erzeugt am Ende genau `CONCEPT_AGENT_CHAT_HANDOFF_V1.json`;
6. setzt niemals `publish_allowed=true`.

GitHub-Startpunkt: `.github/workflows/concept-agent-production.yml`.

Autoritativer Control-Status: `concept_agent/CONTROL_STATE.json`.

**Jeder neue Chat und jede Fortsetzung startet immer hier neu.** Der Chat darf keinen Zwischenstand selbst rekonstruieren und keine Workflow-Stufe auswählen. GitHub prüft den realen Stand von Stufe 0 an, fast-forwardet ausschließlich bereits nachgewiesene Stufen und erzeugt danach genau ein `CONCEPT_AGENT_STAGE_ROUTE_V1` für die einzige erlaubte nächste Stufe.

Chat-/GitHub-Kontrollbefehle:
- `/concept-agent simulate-all`
- `/concept-agent run-current`

## Übergabe / Chatwechsel

Eine Übergabe ist erst vollständig, wenn der exakt gebundene Arbeitsauftrag bytegenau unter `concept_agent/current/CONCEPT_AGENT_CURRENT_WORK_BINDING.json` auf dem Control-Zweig gespeichert wurde.

Die Speicherung läuft durch `concept_agent/binding_transport_gate.py` und akzeptiert nur:
- exakt den im Pointer erwarteten Datei-SHA-256;
- exakt den erwarteten internen `binding_sha256`;
- denselben Batch und dieselbe Artikelanzahl;
- `publish_allowed=false`.

Fehlt diese dauerhafte Datei oder stimmt ein Hash nicht: `BLOCKED`. Rekonstruktion, Ersatzdatei und freies Weiterarbeiten sind verboten.

Bei jedem neuen Chat oder jeder Fortsetzung läuft anschließend wieder der GitHub-Eingang: Stufe 0 prüfen → gültige erledigte Stufen nur durchwinken → genau eine nächste Stufe freigeben.

## Harte Grenze

- Eingang ist ausschließlich der aktuelle `PSERC_TEXTMACHINE_METADATA_BATCH_V2` aus dem Metadaten-Snapshot.
- Recherche und Authoring-Bindungen werden vor dem Schreiben fest gebunden.
- Der Runner darf diese Bindungen nicht neu auswählen oder verändern.
- Batch, Reihenfolge, fünf Metadatenfelder und `plan_slot` bleiben unverändert.
- Nach Authoring bleiben LanguageTool 6.8, PPM 6.7.9, PSERC und ENDSTEMPEL unverändert zuständig.
- ENDSTEMPEL-Einstieg bleibt `concept_agent/endstempel_bridge.py`.
- Kein Publish.

Fehlt der aktuelle gebundene Arbeitsauftrag in GitHub oder stimmt dessen SHA-256 nicht: `BLOCKED`, kein Ersatzpfad.
