# AKTENSCHRANK PFERDERASSEN_ARTIKEL

STATUS: AKTIV
STAND: 2026-09-14

## Zweck
Dieser Aktenschrank ist die dauerhafte Campus-Ablage der fertig geschriebenen Pferderassen-Artikel.

Er ist bewusst getrennt von `PFERDERASSEN/DATEN/`:
- `PFERDERASSEN/DATEN/` = freigegebene Fakten-/Rassendatensätze
- `PFERDERASSEN_ARTIKEL/` = tatsächlich formulierte Artikeltexte und Importbatches

## Verbindliche Regel
Jeder neue oder korrigierte Pferderassen-Artikel wird nach Erstellung und Gesamtprüfung zwingend hier gespeichert, bevor die Importdatei an den Nutzer ausgegeben wird.

Damit bleiben spätere Textkorrekturen möglich, ohne die Rohdaten oder die WordPress-Fassung als einzige Textquelle verwenden zu müssen.

## Autorität
Für die Texterstellung gilt weiterhin ausschließlich:
`PFERDERASSEN/DATEN/breed-*.json -> PFERDERASSEN/SCHREIBVERTRAG_PFERDERASSE.md -> fertiger Artikel`

Die hier gespeicherten Artikel sind kein Ersatz für die Rassendatensätze. Sie sind die archivierte redaktionelle Fassung.

## Ablagestruktur
- `BATCHES/` = vollständige maschinenlesbare Importbatches
- spätere Korrekturen ersetzen nicht stillschweigend die Historie; korrigierte Fassungen erhalten eine neue Batch-ID beziehungsweise klar dokumentierte Revision.

## Aktueller Bestand
Die bereits neu geschriebenen beziehungsweise überarbeiteten Artikelbatches werden hier nachgezogen. Ab diesem Zeitpunkt ist die Campus-Ablage zwingender Produktionsschritt.
