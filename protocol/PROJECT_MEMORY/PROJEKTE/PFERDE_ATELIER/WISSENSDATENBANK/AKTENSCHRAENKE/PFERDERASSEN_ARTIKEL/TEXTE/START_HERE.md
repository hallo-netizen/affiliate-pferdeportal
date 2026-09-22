# PFERDERASSEN_ARTIKEL – TEXTE

STATUS: VERBINDLICHER TEXT-AKTENSCHRANK
STAND: 2026-09-14

## Zweck
Hier werden die fertig geschriebenen Pferderassen-Artikel dauerhaft gespeichert – getrennt von den Fakten-Datensätzen im Aktenschrank `PFERDERASSEN/DATEN`.

Verbindliche Kette:
`PFERDERASSEN/DATEN/breed-*.json -> SCHREIBVERTRAG_PFERDERASSE.md -> fertiger Artikel -> PFERDERASSEN_ARTIKEL/TEXTE`

## Regeln
- Jeder fertige Artikelbatch muss hier gespeichert werden, bevor der Batch als abgeschlossen gilt.
- `source_id` verbindet fertigen Text eindeutig mit dem freigegebenen Fakten-Datensatz.
- Inhaltliche Korrekturen werden immer gegen den zugehörigen Fakten-Datensatz und den aktuellen Schreibvertrag geprüft.
- Keine freie Nachrecherche beim Korrigieren eines Textes.
- Importdatei und Campus-Archiv müssen denselben Artikelstand enthalten.
- Neue Artikel dürfen nicht nur im Chat oder nur als lokale Datei existieren.

## Ablageformat
Die vollständigen Batch-Dateien werden unter `TEXTE/BATCHES/` archiviert.

Für große bereits erzeugte Batches kann die vollständige JSON-Datei verlustfrei als `gzip + base64` in fortlaufenden `part-*.b64`-Dateien archiviert werden. Zum Wiederherstellen: Teile in Reihenfolge zusammenfügen, Base64 dekodieren, anschließend gzip entpacken. Der Inhalt ist bytegenau der gespeicherte JSON-Artikelbatch.

## Stand
- 60 korrigierte/fertige Artikel werden aus den bisherigen drei Produktionsdateien nacharchiviert.
- Noch offene Rassen laut Manager-Katalog nach diesen 60: 48.
- Weitere Produktion erfolgt in maximalen Batches: 25 + 23.
