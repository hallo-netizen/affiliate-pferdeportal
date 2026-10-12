# HOBBYRAUSCH – DESIGN – FEHLERQUELLEN

ROLLE: Fehlerhistorie. Aktueller Status/NEXT ACTION ausschließlich aus `CURRENT_STATE.md`.

## HRD-001 bis HRD-039
Historie bleibt bestehen; lokale Fixstände gelten erst nach Live-Readback als endgültig geschlossen.

## HRD-040 – Navigation noch nicht tief genug
STATUS: LOCAL CLOSED 1.50.620 / LIVE OFFEN

Fix:
Headerzeile erweitert; Navigation mit nur 2 px Unterabstand nahe an die Trennlinie gesetzt.

## HRD-041 – „Nächste Ebene“ zu technisch
STATUS: LOCAL CLOSED 1.50.620 / LIVE OFFEN

Fix:
Eyebrow komplett entfernt. Nur natürliche Überschrift `Weiter in …` / `Weitere Kategorien`.

## HRD-042 – Kartenuntertitel zu klein
STATUS: LOCAL CLOSED 1.50.620 / LIVE OFFEN

Fix:
Kartentitel 15 px, Untertitel 12 px; Taxonomie-Kurztext maximal 7 Wörter.

## Aktuell erster Blocker
**Live-Abnahme 1.50.624 – Navigation + Raster + Bildduplikate.**


## HRD-043 – Sammeln nicht exakt auf derselben Navigationslinie
STATUS: LOCAL CLOSED 1.50.621 / LIVE OFFEN

Fix:
alle acht Items erhalten identische feste Nav-Höhe/Baseline; Sammeln lokal gegen die übrigen sieben vermessen.

## HRD-044 – Header zu hoch trotz zu hoher Navigation
STATUS: LOCAL CLOSED 1.50.621 / LIVE OFFEN

Fix:
Header kompakter; Navigation trotzdem direkt an die untere Trennlinie.

## HRD-045 – Logo intern zu gequetscht / Suche nicht auf Wortmarkenlinie
STATUS: LOCAL CLOSED 1.50.621 / LIVE OFFEN

Fix:
unverändertes Logoasset wird nur für die Darstellung in drei Bereiche geclippt und mit mehr Abstand gesetzt; Suchfeld auf HOBBY-DEPOT-Linie verschoben.


## HRD-046 – Navigation trotz mehrerer Fixes live noch zu hoch
STATUS: LOCAL CLOSED 1.50.624 / LIVE OFFEN

Fix:
Nav im rechten Headerbereich nicht mehr über Padding/Rows angenähert, sondern final per `position:absolute; bottom:0` an die untere Headerkante gebunden.

## HRD-047 – Produkte zwischen Unterkategorie-Reihen
STATUS: LOCAL CLOSED 1.50.624 / LIVE OFFEN

Fix:
Produkte vollständig aus dem Unterkategorie-Raster entfernt. Nur Banner darf die letzte unvollständige 3er-Reihe füllen.

## HRD-048 – Doppelte Hub-Bilder
STATUS: LOCAL CLOSED 1.50.624 / LIVE OFFEN

Fix:
65 aktive direkte Hub-Bilder = 65 eindeutige SHA-256-Hashes. Genuss erhält eigenes Motiv; Alias-/Duplikatdateien bereinigt.
