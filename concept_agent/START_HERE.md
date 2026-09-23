# Pferde Atelier — aktueller Artikelstart

Einziger Start für neue Artikelaufträge: `text-start` mit `START:pferdeatelier`.

Der feste Empfänger auf `main` liest bei jedem Start automatisch genau den aktuellen Metadaten-Snapshot aus:

`concept-agent/production-control:concept_agent/current/PSERC_METADATA_SNAPSHOT.json`

Die Branch dient ausschließlich als **Datenablage für den aktuellen Auftrag**. Dort gibt es keinen Produktionsworkflow, keinen Runner, keine Run-Requests und keinen eigenen Produktionszustand.

## Verbindlicher Ablauf

1. `text-start` autorisiert ausschließlich das Projekt Pferdeatelier.
2. Der Empfänger ermittelt den **zu diesem Zeitpunkt aktuellen** Snapshot.
3. `concept_agent/intake_bridge.py` validiert exakt diesen Snapshot.
4. Die Artikelanzahl kommt ausschließlich aus dem Snapshot: **1..N**, niemals fest 7, 16 oder eine andere Zahl.
5. Erst für diesen einen Lauf werden Snapshot-Head und Batch-Hash eingefroren.
6. Vor `MACHINE_READY` darf ein technischer Fehlstart sauber wiederholt werden.
7. Nach `MACHINE_READY` ist ein zweiter Start desselben Batches gesperrt.

## Harte Grenzen

- Recherche bleibt artikelbezogen und wird vor dem Draft gebunden.
- Artikelinhalt und Qualitätsregeln bleiben unverändert.
- LanguageTool 6.8, PPM 6.7.9, PSERC und ENDSTEMPEL bleiben unverändert zuständig.
- Kein Publish.
- Alte `runtime_inbox/**`, `SOURCE_REQUESTS.json`, alte 7er-Artefakte, alte Control-Branch-Runner und alte Cross-Chat-Transporte sind **keine Start- oder Produktionsautorität**.
- Keine Alternativroute.

Bei jeder Abweichung: `BLOCKED`.
