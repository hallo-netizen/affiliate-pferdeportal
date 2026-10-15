# HOBBYRAUSCH – DESIGN RELEASE GATE 2026-10-13

STATUS: AKTIV / REGELDEFINITION / KEINE CURRENT-WAHRHEIT

## Zweck
Ein technisch vorhandenes Bild darf nicht mehr als visueller PASS gelten. Das Gate trennt technische Existenz von echter visueller Freigabe.

## Harte Bedingungen vor ZIP
Ein neuer HD-003-Kandidat darf erst paketiert werden, wenn gleichzeitig gilt:

- Hero-Abdeckung 65/65;
- Hero-Audit 65/65 PASS nach realem 600×320-Crop;
- Karten-Abdeckung 328/328;
- Karten-Audit 328/328 PASS nach realem 200×107-Crop;
- kein fehlendes Bild;
- kein Featured-Image-Fallback für Hub2-Karten;
- kein Welt-Pool-/Universalbild-Fallback;
- kein Icon-Fallback für fehlende Hub2-Fotos;
- kein Hero-Weltfallback;
- keine exakten oder offensichtlichen Doppelbilder innerhalb derselben Hub2-Seite;
- aktive Hero-Dateien exakt 600×320 ohne Upscaling;
- aktive Kartenquellen mindestens 200×107;
- PHP/Release-Kette PASS;
- Regression gegen eingefrorenen Text/Grundaufteilung 1.50.650;
- visuelle Referenz Buch & Papier 1.50.645 unverändert.

## Aktueller 30er-Bildquellen-Untergate
Der laufende Nach-1.50.663-Reparaturblock umfasst **30 konkret verworfene/neu aufzubauende Hero-Quellen**. Für diesen Block gilt zusätzlich:
- 30/30 eigenständige neue Quellen bzw. freigegebene Motive;
- pro Kategorie dieselbe Quelle für Hero 600×320 und Preview 200×107;
- kein Panel aus Sammel-/Collagebildern als Releasequelle;
- kein alter 1.50.653–1.50.663-Bildbestand als Ersatz;
- erst nach 30/30 Motiv-PASS darf der einmalige reine 60-Dateien-Image-only-Kandidat gebaut werden.

Dieses 30er-Untergate ersetzt **nicht** das globale 65-Hero-/328-Karten-Gate; es ist der aktuell offene Reparaturblock darin.

## Statusquelle
Diese Datei definiert nur das Release-Gate. Den aktuellen PASS/FAIL-Stand, aktuellen Blocker und genau eine NEXT ACTION ausschließlich aus
`protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/DESIGN/CURRENT_STATE.md`
lesen.

## Regel
**Solange das Gate FAIL ist: kein ZIP, kein Kandidat, kein Live-Test.**
