# Fehlerkatalog – V6.57 idealo Phase 1

## I1 – iPN Download-Button liefert im DOM nur `javascript:void(0)`
Kein belastbarer direkter Feedlink aus dem HTML. Konsequenz: keine Developer-Tools-/DOM-Konstruktion als Produktivlösung. Die produktive Remote-URL wird nur aus dem offiziellen Product-Data-Feed-Dialog übernommen.

## I2 – Alle getesteten idealo-Deeplinks enthalten `!!TIME_STAMP!!`
Realer Befund: 655/655 ausgewählte Produkte. Konsequenz: Phase 1 speichert/staged Daten, veröffentlicht aber keinen idealo-Link. Ersetzung wird erst nach eigenem iPN-Beleg freigegeben.

## I3 – Vollfeed ist groß
515.554 Zeilen. Konsequenz: streamender CSV/GZIP-Parser; keine Vollfeed-Memory-Ladung. Erst passende konfigurierbare Unterkategorien werden gesammelt.

## I4 – Providerfehler darf eBay nicht stoppen
idealo läuft als separater Adaptertrait. eBay-Provider-, eBay-Run- und Frontend-Dateien bleiben byteidentisch.

## I5 – API-Key ist Secret
Der Schlüssel wird weder in GitHub noch in MASTER/Testlogs geschrieben. Live-Eingabe ausschließlich in WordPress bzw. optional über `PPAR_IDEALO_API_KEY` in wp-config.php.
