# Pferde Atelier — Konzept 5 / Concept Agent

Autoritativer Einstieg für neue Artikel-Batches: `concept_agent/intake_bridge.py`.

## Start

`python3 concept_agent/intake_bridge.py prepare <PSERC_METADATA_SNAPSHOT.json> <CONCEPT_AGENT_INTAKE.json>`

Nur `CONCEPT_AGENT_INTAKE_READY` erlaubt den nächsten Schritt.

## Harte Grenze

- Eingang ist ausschließlich der aktuelle `PSERC_TEXTMACHINE_METADATA_BATCH_V2` aus dem Metadaten-Snapshot.
- Der Concept Agent recherchiert artikelbezogen und bindet Quellen/Evidenz **vor** dem Draft.
- Alte `control/startmaster0107/runtime_inbox/**`-Zustände und `SOURCE_REQUESTS.json` sind **keine** Startvoraussetzung für Konzept 5 und dürfen einen neuen Concept-Agent-Lauf weder bestimmen noch blockieren.
- Batch, Reihenfolge, fünf Metadatenfelder und `plan_slot` bleiben unverändert.
- Kein Publish.
- Nach Authoring bleiben LT 6.8, PPM 6.7.9, PSERC und ENDSTEMPEL unverändert zuständig.
- ENDSTEMPEL-Einstieg bleibt `concept_agent/endstempel_bridge.py`; diese Datei ersetzt keine downstream Prüfung.

Bei jeder Abweichung: `BLOCKED`, kein Ersatzpfad.
