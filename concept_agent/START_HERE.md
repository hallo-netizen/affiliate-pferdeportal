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

Der automatische GitHub-Start liegt getrennt auf dem Ausführungszweig `concept-agent/production-control`.
Autoritativer Wegweiser auf `main`: `concept_agent/CONTROL_ENTRY_POINTER.json`.

**Jeder neue Chat und jede Fortsetzung muss vor jeder fachlichen Arbeit zuerst diesen Wegweiser lesen und den GitHub-Eingang auf `concept-agent/production-control` anstoßen.** Der Chat darf keinen Zwischenstand selbst rekonstruieren, keine Workflow-Stufe auswählen und keinen direkten Ersatzweg benutzen.

GitHub prüft den gespeicherten Workflow immer von Stufe 0 an, winkt nur bereits nachgewiesene Stufen durch und gibt danach genau eine nächste Stufe frei.

Eine Übergabe gilt erst als vollständig, wenn der exakt gebundene Arbeitsauftrag bytegenau dauerhaft in GitHub gespeichert und gegen Datei-SHA-256 sowie internen Binding-SHA-256 geprüft wurde. Fehlt diese Datei oder stimmt ein Hash nicht: `BLOCKED`, keine Rekonstruktion.

Ein neuer Lauf wird auf dem Control-Zweig ausschließlich durch genau eine Datei unter `concept_agent/run_requests/` angestoßen.

## Harte Grenze

- Eingang ist ausschließlich der aktuelle `PSERC_TEXTMACHINE_METADATA_BATCH_V2` aus dem Metadaten-Snapshot.
- Recherche und Authoring-Bindungen werden vor dem Schreiben fest gebunden.
- Der Runner darf diese Bindungen nicht neu auswählen oder verändern.
- Batch, Reihenfolge, fünf Metadatenfelder und `plan_slot` bleiben unverändert.
- Nach Authoring bleiben LanguageTool 6.8, PPM 6.7.9, PSERC und ENDSTEMPEL unverändert zuständig.
- ENDSTEMPEL-Einstieg bleibt `concept_agent/endstempel_bridge.py`.
- Kein Publish.

Fehlt der aktuelle gebundene Arbeitsauftrag in GitHub oder stimmt dessen SHA-256 nicht: `BLOCKED`, kein Ersatzpfad.
