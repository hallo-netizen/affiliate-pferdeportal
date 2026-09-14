# GLOSSAR – HOBBYRAUM

STAND: 2026-09-14
STATUS: HERO LIVE-READBACK OFFEN / AUTOMATION-SANDBOX LIVE-PRUEFUNG OFFEN

## LIVE PASS – NICHT ANFASSEN
- Einzelbegriffe öffnen.
- 0 Links im Glossar-Fließtext.
- dünne Ockerlinie rechts.
- Breadcrumb Inhalt + Position/Abstand nach Design 1.50.493.

## HERO – LIVE FAIL NACH 1.50.493

Nutzerreadback:
- Übergang Fläche → Bild fehlt sichtbar;
- Bild ist in der Hero-Box zu schmal.

Ursache:
`object-fit:contain` + `transform:scale(.86)` machte den realen Bildkörper nur ca. 440 px breit. Der Fade lag weitgehend vor leerem Raum statt über dem sichtbaren Bild.

## DESIGN 1.50.494 – LOKAL HART PASS

`PFERDE_ATELIER_DESIGN_V1.50.494_HERO_BLEND_WIDE_INSTALLIEREN.zip`

SHA-256: `8bee0a958fb146e09bbb01319c22e34d70c34c5824153fc2050f4e4c00541643`

- Bild füllt rechten Medienbereich (`object-fit:cover`).
- keine `.86`-Verkleinerung.
- reale Referenz-Bildbreite ca. 767 px statt ca. 440 px.
- echter Creme→Bild-Fade liegt direkt über dem realen Bild.
- kein Desktop-Masken-Konstrukt mehr.
- Breadcrumb-/0-Link-/Ockerlinien-Code unverändert.

Harte lokale Prüfung:
- PHP-Lint PASS;
- positiver Hero-Vertrag PASS;
- `contain` absichtlich zurück → rot;
- Fade-Ende absichtlich entfernt → rot;
- `.86`-Shrink absichtlich zurück → rot;
- alte Maske absichtlich zurück → rot;
- Regression Breadcrumb / 0 Links / dünne Ockerlinie PASS;
- nur Haupt-PHP gegenüber 1.50.493 geändert;
- WordPress-ZIP-Stamm korrekt;
- exakt gleicher 500-Dateien-Bestand wie installierbares 1.50.493.

Marker: `DESIGN_150494_HERO_BLEND_WIDE_POS_NEG_PASS`.

## AUTOMATION-SANDBOX – CORE 1.3.0

Unverändert. WordPress: `Glossar -> Automation`.

Realer nächster Automationsschritt nach Hero-Readback:
`Sandbox hart testen` → danach Pool aktualisieren → danach 1 echter Kandidat Ende-zu-Ende, Produktionsmodus AUS.

## HARTE GRENZE

Design 1.50.494 ist **lokal PASS, LIVE noch offen**. Auto-Publish bleibt AUS.
