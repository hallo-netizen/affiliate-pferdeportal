# TEST VS. LIVE – WARUM TESTS PASSEN UND LIVE TROTZDEM SCHEITERT

## Belegter Befund

Die vorhandenen Tests prüfen überwiegend einzelne technische Eigenschaften, Dateien, Hashes und gezielte Fehlerklassen. Der echte Produktionslauf prüft zusätzlich die reale Verkettung derselben Komponenten mit realen Laufdaten.

Dadurch können alle Einzelteile grün sein, obwohl die Übergabe zwischen zwei Teilen falsch ist.

## Konkretes Beispiel

Der M01–M33-Runner enthält am Ende die kommentierte Regel „final re-check against the last real production regression“. Tatsächlich wird dort aber nur `m26()` erneut ausgeführt und anschließend `LAST_REGRESSION PASS ...` ausgegeben. Es findet kein echter Replay/Vergleich des letzten realen 7/7-Pfads statt.

Das erklärt, warum ein Runner „GESAMT PASS“ liefern kann, obwohl eine reale Produktionsfähigkeit wieder verloren gegangen ist.

## Konsequenz für Statusmeldungen

Künftig müssen drei Ebenen getrennt bleiben:

- **UNIT/REGRESSION PASS** – isolierte technische Regel bestanden.
- **PRINZIP PASS** – Komponentenkette synthetisch/isoliert bestanden.
- **LIVE 7/7 PASS** – echter produktiver Batch auf exakt diesem Stand bis 107008 bestanden.

Nur Ebene 3 ist ein Produktionsbeweis.