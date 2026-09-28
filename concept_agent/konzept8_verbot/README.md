# K8 Verbot

Eigenständiger, hart isolierter Produktionslauf.

## Trennungsregel

K8 liest, importiert oder startet keinen anderen Konzept-Lauf. Kein anderer Konzept-Lauf wird von K8 als Fallback, Quelle, Controller oder Worker verwendet.

Der Live-Eingang darf ausschließlich in diesen K8-Namensraum führen. Gemeinsame fachliche Autoritäten außerhalb der Konzeptsteuerung bleiben nur die unveränderten, bereits bestehenden Qualitätsmaschinen und aktuellen gebundenen Produktionsdaten.

## Verbotsprinzip

- exakt der aktuelle checkpointgebundene Befehl: darf passieren;
- jeder andere, fehlende, alte oder erweiterte Befehl: keine Zustandsänderung;
- derselbe Checkpoint und dieselbe NEXT ACTION bleiben gültig;
- beschädigter Checkpoint: harter STOP statt Raten;
- Qualitätsregeln, Prüferfolge und Publish bleiben unverändert.

Die Trennung wird maschinell in beiden Richtungen geprüft.
