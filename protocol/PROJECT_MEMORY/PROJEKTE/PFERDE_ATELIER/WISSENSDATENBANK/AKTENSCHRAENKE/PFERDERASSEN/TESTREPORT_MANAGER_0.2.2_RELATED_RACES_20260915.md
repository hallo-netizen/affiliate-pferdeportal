# TESTREPORT – Pferderassen Manager 0.2.2 – ähnliche Rassen

Stand: 2026-09-15

## Ursache
Design 1.50.506 erwartet auf `pa_breed` das Meta-Feld `_prm_related_source_ids`. Manager 0.2.1 importierte dieses Feld nicht. Daher blieb der Slot „Ähnliche Rassen“ leer.

## Umsetzung 0.2.2
- Plugin-Stamm bleibt `pferde-rassen-manager/`; Update über 0.2.1 möglich.
- Version `0.2.2`.
- JSON-Feld `related_source_ids` wird normalisiert, maximal 3 eindeutige WDB-IDs.
- Selbstreferenz wird blockiert.
- unbekannte WDB-ID wird blockiert.
- explizite Relation darf nur auf eine bereits veröffentlichte `pa_breed`-Rasse zeigen.
- Speicherung in `_prm_related_source_ids`.
- WordPress-Readback prüft die gespeicherten Relations-IDs.
- neuer Backendpunkt `Pferderassen → Ähnliche Rassen`.
- Backfill ergänzt bei bestehenden veröffentlichten Rassen fehlende Relationen mit bis zu drei veröffentlichten Rassen derselben `pa_breed_group` und speichert die WDB-IDs fest.
- bereits vollständig gepflegte Relationen bleiben unangetastet.
- Draft-Hardlock bleibt unverändert (`post_status=draft`); kein Auto-Publish.
- Katalog bleibt 200 Einträge.

## Tests
- PHP-Lint Hauptdatei: PASS.
- PHP-Lint Managerklasse: PASS.
- Relations-Normalisierung 3 eindeutig: PASS.
- Selbstreferenz negativ: BLOCK/PASS.
- unbekannte Relations-ID negativ: BLOCK/PASS.
- Backfill nimmt drei veröffentlichte Gruppen-Peers: PASS.
- Backfill schließt eigene source_id aus: PASS.
- finale 13er-Datei gegen 0.2.2-Validator: PASS.
- unveröffentlichte Relation negativ: `RELATED_SOURCE_NOT_PUBLISHED` BLOCK/PASS.
- ZIP-Wurzel `pferde-rassen-manager/`: PASS.
- ZIP-Integrität: PASS.
- ZIP-Katalog 200: PASS.
- Draft-Hardlock im finalen ZIP: PASS.

## Artefakte
- `PFERDE_ATELIER_PFERDERASSEN_MANAGER_0.2.2_INSTALLIEREN.zip`
- SHA-256: `e0149a3ac3b0b4ef630fc587f26da06f8a89621b9c4d728d3357d4440727beb4`
- Finaler 13er-Batch: `pferderassen_FINAL_13_manager022.json`
- Batch SHA-256: `0b98a969bb107b4e014d73de5ca0a76f6dabf9f0fcdd9cd2c7ddbfca1d81bb95`
