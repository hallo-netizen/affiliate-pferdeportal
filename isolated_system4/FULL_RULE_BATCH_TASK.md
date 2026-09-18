# SYSTEM 4 — REAL BOUND BATCH / POINT-0 V2

No merge. No publish. No signing.

## Vorbedingung durch Parent-Maschine

Vor Codex muss die Maschine den kompletten Batch vorbereiten:
1. exakten WordPress-Metadaten-Snapshot binden;
2. je Artikel einen eigenen Source-Request-Pool festlegen und technisch erwerben/verifizieren;
3. je Artikel die unveränderlichen Prewrite-Schienen aus dem gültigen Produktionsplan binden;
4. `SYSTEM4_POINT0_SNAPSHOT_V2` erzeugen;
5. für jeden Index `N` `root_entry.py start-point0 <point0> <workspace-N> N` erfolgreich ausführen;
6. erst danach `codex_entry.py worker-start <workspace-N>`.

Ein fehlender/abweichender Source-Pool, Index, Slot, Prewrite-Hash, Head oder Manifest ist ein Hardblocker vor Codex.

## Codex pro Artikel

Codex arbeitet ausschließlich im vom Supervisor freigegebenen Workspace:
- Research-Dokument = exakt der gebundene artikelbezogene Quellenpool;
- Facts = nur aus akzeptierter Research-Evidenz;
- Context = Fact-Pack plus Produktionsplan, wobei alle maschinengebundenen Rails exakt unverändert bleiben müssen;
- Draft = neuer deutscher Artikel nach unveränderter Textmaschine/Designvertrag;
- Prüfen ausschließlich über `controller.py fullcheck`;
- bei `REPAIR_REQUIRED` nur konkreten Fehler im selben Artikel über `controller.py repair` ändern und erneut `fullcheck`.

Codex darf keine URL ergänzen, keine freie Websuche ausführen, keine Kategorie/Links/Quality-Binding ändern und keinen PASS setzen.

## Abschluss

Erst wenn **alle** Snapshot-Artikel `OUTPUT_GATE_REQUIRED` und FULL_PRODUCTION PASS sind:

`python3 isolated_system4/batch_gate.py collect <SNAPSHOT> <OUTDIR> <state-0> ... <state-N>`

Danach genau einen `SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2` erzeugen, validieren, kanonisieren, inline packen und im Parent-Chat inline wieder auspacken. Bytegleichheit, Schema, SHA, Reihenfolge und Artikelanzahl sind Pflicht. Kein zweiter WordPress-Transformationsschritt.

## Skalierung

Keine feste Artikelzahl und keine Typ-Allowlist. `1..N` ist derselbe Pfad. Testzahlen wie 1, 3, 7, 25 oder 1000 sind nur Regressionen.
