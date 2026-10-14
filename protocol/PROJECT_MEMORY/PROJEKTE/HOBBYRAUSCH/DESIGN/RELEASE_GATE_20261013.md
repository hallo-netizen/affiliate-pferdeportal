# HOBBYRAUSCH – DESIGN RELEASE GATE 2026-10-13

STATUS: AKTIV / REGELDEFINITION / KEINE CURRENT-WAHRHEIT

## Zweck
Ein technisch vorhandenes Bild darf nicht mehr als visueller PASS gelten. Das Gate trennt technische Existenz von echter visueller Freigabe.

## Harte Bedingungen vor ZIP
Ein neuer HD-003-Kandidat darf erst paketiert werden, wenn gleichzeitig gilt:

- Hero-Abdeckung 65/65;
- Hero-Audit 65/65 PASS nach realem 600×220-Crop;
- Karten-Abdeckung 328/328;
- Karten-Audit 328/328 PASS nach realem 200×107-Crop;
- kein fehlendes Bild;
- kein Featured-Image-Fallback für Hub2-Karten;
- kein Welt-Pool-/Universalbild-Fallback;
- kein Icon-Fallback für fehlende Hub2-Fotos;
- kein Hero-Weltfallback;
- keine exakten oder offensichtlichen Doppelbilder innerhalb derselben Hub2-Seite;
- aktive Hero-Dateien exakt 600×220 ohne Upscaling;
- aktive Kartenquellen mindestens 200×107;
- PHP/Release-Kette PASS;
- Regression gegen eingefrorenen Text/Grundaufteilung 1.50.650;
- visuelle Referenz Buch & Papier 1.50.645 unverändert.

## Statusquelle
Diese Datei definiert nur das Release-Gate. Den aktuellen PASS/FAIL-Stand, aktuellen Blocker und genau eine NEXT ACTION ausschließlich aus
`protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/DESIGN/CURRENT_STATE.md`
lesen.

## Regel
**Solange das Gate FAIL ist: kein ZIP, kein Kandidat, kein Live-Test.**
