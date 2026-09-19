# CONCEPT AGENT — ZIELVERTRAG

## Ziel
Ein vollständig isolierter Prototyp für eine agentenbasierte Artikelproduktion.

## Eingang
Eine Kopie einer WordPress-/SEO-Auftragsdatei mit den bereits bekannten Vorgaben:
- Thema / Titel
- Keyword / Suchintention
- Artikeltyp / Kategorie
- interne Linkvorgaben
- weitere redaktionelle Vorgaben

Die echte WordPress-Quelle bleibt unangetastet.

## Agenten
1. Research Agent: sammelt ausschließlich Quellen und Belege.
2. Facts Agent: bildet ausschließlich belastbare Fakten aus den akzeptierten Belegen.
3. Writer Agent: schreibt ausschließlich aus Auftrag + akzeptiertem Fact-Pack.
4. Repair Agent: verändert ausschließlich konkret beanstandete Stellen desselben Artikels.

## Übergaben
Jede Übergabe erhält ein festes Schema und eine eigene Prüfung.
Kein Folge-Agent startet, solange die vorherige Übergabe nicht formal akzeptiert wurde.

## Ausgang
Genau eine finale Rückgabedatei je Artikel beziehungsweise ein klar definiertes 1..N-Paket.

## Isolation
Keine Runtime-Schnittstelle zu anderen Konzepten.
Keine Änderung fremder Dateien.
Keine Produktionswirkung.
Keine WordPress-Schreiboperation.
