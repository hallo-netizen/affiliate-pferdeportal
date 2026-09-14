# BÜRO GLOSSAR – CURRENT_STATE

STAND: 2026-09-14
STATUS: LIVE TEILPASS / BREADCRUMB LIVE PASS / HERO LIVE FAIL / DESIGN 1.50.494 LOKAL HART POSITIV+NEGATIV PASS / AUTOMATION CORE 1.3.0 LIVE-SANDBOXPRUEFUNG OFFEN

## LIVE bestätigt – nicht regressieren

- Einzelbegriffe öffnen: **PASS**.
- Glossar-Fließtext: **0 Links – PASS**.
- rechte Ocker-Oberkante: **dünn – PASS**.
- Breadcrumb-Inhalt und Breadcrumb-Position/Abstand nach Design `1.50.493`: **LIVE PASS 2026-09-14**. Nicht mehr anfassen.

## Hero – aktueller LIVE-Befund

Nutzerreadback 2026-09-14 nach Design 1.50.493:
- weicher Übergang Fläche → Bild fehlt sichtbar;
- Bild ist in der Hero-Box zu schmal und soll breiter/präsenter werden.

### Nachgewiesene Ursache

Der 1.50.493-Hero verwendete `object-fit:contain` plus `transform:scale(.86)`. Dadurch war der reale Bildkörper bei 1180 px Referenzbreite nur ca. **440 px** breit und begann weit rechts. Der CSS-Verlauf lag zum großen Teil über leerem Raum und konnte deshalb den sichtbaren Bildanfang nicht weich überblenden.

### Design-Kandidat 1.50.494

Paket: `PFERDE_ATELIER_DESIGN_V1.50.494_HERO_BLEND_WIDE_INSTALLIEREN.zip`

SHA-256: `8bee0a958fb146e09bbb01319c22e34d70c34c5824153fc2050f4e4c00541643`

Fix:
- Hero-Bild füllt den rechten Medienbereich mit `object-fit:cover`;
- keine `.86`-Verkleinerung mehr;
- realer Bildkörper Referenzbreite ca. **767 px** statt ca. 440 px (= Faktor 1,74);
- Creme→Bild-Verlauf liegt direkt über dem realen Bild und endet transparent;
- Desktop-Masken-Konstrukt entfernt;
- Breadcrumb-/0-Link-/Ockerlinien-Code gegenüber 1.50.493 unverändert.

Hart lokal:
- PHP-Lint aller PHP-Dateien PASS;
- Positivvertrag Bildbreite/Fade PASS;
- Negativ `contain` wieder eingesetzt → Test erkennt Fehler;
- Negativ Fade-Ende entfernt → Test erkennt Fehler;
- Negativ `.86`-Shrink wieder eingesetzt → Test erkennt Fehler;
- Negativ Masken-Konstrukt wieder eingesetzt → Test erkennt Fehler;
- Regression: Breadcrumb-, 0-Link- und dünne-Ockerlinie-Anker PASS;
- Tree-Diff gegen installierbares 1.50.493: nur `pferde-template-kit.php` geändert;
- ZIP-Stamm `affiliate-portal-template-kit/` PASS;
- exakt gleicher 500-Dateien-Bestand wie 1.50.493 PASS;
- Version 1.50.494 PASS.

Marker: `DESIGN_150494_HERO_BLEND_WIDE_POS_NEG_PASS`.

## Core 1.3.0 – Automation

Core 1.3.0 bleibt unverändert. Die reale WordPress-Sandboxprüfung unter `Glossar -> Automation -> Sandbox hart testen` ist weiterhin offen. Auto-Publish bleibt AUS.

## Harte Grenze

**Hero 1.50.494 ist lokal hart geprüft, aber noch kein LIVE PASS.** Erst Installation + Nutzerreadback schließen den Hero.

## Nächster realer Schritt

1. Design `1.50.494` über 1.50.493 installieren.
2. Glossar-Startseite prüfen: Bild deutlich breiter + echter weicher Übergang.
3. Breadcrumb gegenprüfen: muss unverändert PASS bleiben.
4. Danach `Glossar -> Automation -> Sandbox hart testen`.
