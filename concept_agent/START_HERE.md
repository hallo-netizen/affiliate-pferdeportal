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
Ein neuer Lauf wird dort ausschließlich durch genau eine Datei unter `concept_agent/run_requests/` angestoßen.

## Harte Grenze

- Eingang ist ausschließlich der aktuelle `PSERC_TEXTMACHINE_METADATA_BATCH_V2` aus dem Metadaten-Snapshot.
- Recherche und Authoring-Bindungen werden vor dem Schreiben fest gebunden.
- Der Runner darf diese Bindungen nicht neu auswählen oder verändern.
- Batch, Reihenfolge, fünf Metadatenfelder und `plan_slot` bleiben unverändert.
- Nach Authoring bleiben LanguageTool 6.8, PPM 6.7.9, PSERC und ENDSTEMPEL unverändert zuständig.
- ENDSTEMPEL-Einstieg bleibt `concept_agent/endstempel_bridge.py`.
- Kein Publish.

Fehlt der aktuelle gebundene Arbeitsauftrag in GitHub oder stimmt dessen SHA-256 nicht: `BLOCKED`, kein Ersatzpfad.
