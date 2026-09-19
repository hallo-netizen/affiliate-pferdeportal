# CONCEPT AGENT — ISOLATION MANIFEST

## Erlaubter Schreibbereich
Nur:
`concept_agent/**`

## Verboten
- Änderungen außerhalb dieses Ordners durch den Concept-Agent-Fachweg;
- Imports/Aufrufe fremder Produktionscontroller als Runtime-Abhängigkeit;
- WordPress-Write;
- Publish;
- Merge;
- Rückschreiben in andere Konzepte;
- ungeprüfte externe Writer-Verbindung.

## Erlaubt
- READ-ONLY-Prüfung autoritativer Fremdquellen;
- Kopie eines Inputs für isolierte Tests;
- eigene Agenten, eigene Prüfer, eigene Verträge, eigene Outputs;
- lokal gespiegelte Prüfung des realen WordPress-Importvertrags.

Dynamischer Stand und NEXT ACTION stehen ausschließlich in:
`concept_agent/CURRENT_STATUS.md`
