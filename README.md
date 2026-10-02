# K10 Rule Ledger

K10 ist der getrennte Entwicklungsbereich für die Regel-/Receipt-Architektur des Pferdeatelier-Textsystems.

## Einstieg
1. `K10_START_HERE.md` lesen.
2. Von dort genau eine Current-Autorität verwenden: `CURRENT_STATE.json`.
3. Frischecheck gegen Branch und relevante Workflow-Läufe durchführen.
4. Nur die dort gebundene NEXT ACTION ausführen.

## Architekturprinzip
Eine harte Regel hat genau einen fachlichen Owner, wird genau einmal inhaltlich geprüft und erzeugt genau einen hashgebundenen Receipt. Nachgelagerte Stufen prüfen nur Identität, Vollständigkeit, Hash-Bindung und Unverändertheit.

## Harte Trennung
K9 bleibt eigenständiges Produktionssystem. K10 darf K9 nicht verändern. Die K9-Baseline wird nur read-only referenziert.

Aktuelle Status-, Test-, Branch-, Blocker- und NEXT-ACTION-Wahrheit steht **ausschließlich** in `CURRENT_STATE.json`; dieses README enthält bewusst keine dynamischen Statuskopien.
