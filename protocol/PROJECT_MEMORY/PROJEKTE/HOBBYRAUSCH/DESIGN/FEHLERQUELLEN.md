# HOBBYRAUSCH – DESIGN – FEHLERQUELLEN

ROLLE: Fehlerhistorie. Aktueller Status/NEXT ACTION ausschließlich aus `CURRENT_STATE.md`.

## HRD-001 bis HRD-023
Bisherige Fehlerhistorie bleibt geschlossen bzw. unter Regression.

## HRD-024 – Navigation verschwand bei mittlerer Breite
STATUS: LOCAL CLOSED IN 1.50.617 / LIVE OFFEN

Ursache:
1.50.616 ersetzte die abgeschnittene Vollnavigation bei mittleren Breiten durch ein verstecktes Menü. Dadurch war die Kategorie-Navigation ohne zusätzlichen Klick faktisch weg.

Fix:
- >1180 px 8×1;
- 761–1180 px sichtbar 4×2;
- <761 px Hamburger.

## HRD-025 – Logo bei mittlerer Breite zu klein
STATUS: LOCAL CLOSED IN 1.50.617 / LIVE OFFEN

Fix:
Logo bleibt unverändertes Asset, wird aber wieder deutlich größer gerendert: lokal 278 px bei 1024 px Viewport.

## HRD-026 – Aufklapptext ohne Absatzrhythmus / wechselnde Farbboxen
STATUS: LOCAL CLOSED IN 1.50.617 / LIVE OFFEN

Fix:
- volle Inhaltsbreite;
- echter Absatzsplit;
- neutraler Hintergrund;
- `Was du hier findest` ohne eigene Farbbox.

## HRD-027 – Unterkategorie-Fotos uneinheitlich / Druck ohne Bild
STATUS: LOCAL CLOSED IN 1.50.617 / LIVE OFFEN

Fix:
- robuster Titel-/Slug-Match;
- Druck & Fotografie wieder bebildert;
- 7/7 unterschiedliche Motive;
- alle 600×320 / Querformat;
- 7er-Raster 3+2+2.

## HRD-028 – Affiliate wieder als externe Unterblöcke
STATUS: LOCAL CLOSED IN 1.50.617 / LIVE OFFEN

Fix:
Banner und Produktplätze werden innerhalb des Bereichs `Nächste Ebene` ausgegeben. Die späteren separaten Hub-Blöcke wurden entfernt.

## HRD-029 – Direktwerbung zu dunkel / CTA unleserlich
STATUS: LOCAL CLOSED IN 1.50.617 / LIVE OFFEN

Fix:
ein Foto, heller Brush, aufgehellter Bildbereich und weißer CTA mit dunkler Schrift.

## Aktuell erster Blocker
**Live-Abnahme 1.50.617.**
