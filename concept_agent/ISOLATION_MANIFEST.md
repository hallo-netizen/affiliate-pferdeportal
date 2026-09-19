# CONCEPT AGENT — ISOLATION MANIFEST V1

## Erlaubter Schreibbereich
Nur:
`concept_agent/**`

## Verboten
- Änderungen außerhalb dieses Ordners
- Imports aus anderen Konzepten
- Aufruf fremder Controller/Runner/Gates
- WordPress-Write
- Publish
- Merge
- Rückschreiben in Konzept 1/2/3/4/4A
- automatische Claude-Verbindung ohne eigenen späteren Freigabeschritt

## Erlaubt
- READ-ONLY-Inspiration aus bestehenden fachlichen Regeln
- Kopie eines Inputs für isolierte Tests
- eigene Agenten, eigene Prüfer, eigene Verträge, eigene Outputs

## Aktuelle Writer-Modi
1. interner deterministischer Testwriter
2. manueller Chat-Writer
3. Claude-Adapter: definiert, aber bewusst NICHT verbunden

## Aktueller Endvertrag
`CONCEPT_AGENT_FINAL_ARTICLE_V1`

Es entsteht genau eine finale Rückgabedatei je Artikel.
