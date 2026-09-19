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


## Zwei Betriebsvarianten

### Variante A — vorhandene Plattform
- GitHub bleibt Kontroll- und Ablageort.
- Dieser Chat kann die fachlichen Agentenrollen für Entwicklung und Test ausführen.
- Codex bleibt optional und wird wegen Nutzungslimits nicht als zwingende Grundlage eingeplant.
- Diese Variante dient zuerst zum Beweis, dass die Agentenkette fachlich und technisch sauber funktioniert.
- Sie ist ohne zusätzliche KI-API nicht vollständig autonom.

### Variante B — Claude als externer Writer
- GitHub bleibt Kontroll- und Ablageort.
- Research/Facts können zunächst wie in Variante A bleiben.
- Der Writer Agent kann alternativ über genau eine Claude-API-Verbindung ausgeführt werden.
- Es wird keine eigene Verbindung pro Agent gebaut; alle Claude-Rollen würden denselben Adapter verwenden.
- Claude darf nur seine zugewiesene Rolle ausführen und erhält keinen Zugriff auf andere Konzepte.
- Der restliche Concept-Agent-Ablauf bleibt identisch.

## Entscheidungsregel
Zuerst wird Variante A vollständig isoliert stabilisiert und getestet.
Variante B wird erst danach als austauschbarer Writer-Zweig ergänzt.
