# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-12
STATUS: **1.50.625 LOCAL HARD PASS / WORDPRESS-LIVE OFFEN**

## Kandidat
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.625_HOBBY_DEPOT_SIMPLE_UNIQUE_HUB_IMAGES_NAV_BASELINE_LOCALPASS.zip`

SHA-256:
`6aab2195365375c30c4dfcc4558dd8aa62f912289df76544b6e0cb5529960e03`

Library:
`/hobby rausch/AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.625_HOBBY_DEPOT_SIMPLE_UNIQUE_HUB_IMAGES_NAV_BASELINE_LOCALPASS.zip`

## Root Cause aus dem Live-Readback 1.50.624

Die 65 lokalen Dateien waren zwar byte-eindeutig, wurden live aber teilweise gar nicht benutzt:
`next_level_card_photo()` gab vorhandenen WordPress-Featured-Images Vorrang.

Dadurch konnten mehrfach gepflegte alte Featured Images die kontrollierten Motive überstimmen.

## Korrektur 1.50.625

### Bilder
- kontrollierte 600×320-Hubmotive werden für die 65 direkten Welt-Unterkategorien jetzt **vor** WordPress Featured Images aufgelöst;
- 65/65 aktive Bildpfade;
- 65/65 unterschiedliche SHA-256;
- Perceptual-dHash Mindestabstand im Gesamtbestand: **96**;
- Bildprinzip auf alle 65 angewendet: engere, ruhigere, klarere Einzelmotive; keine Hero-/Parent-Wiederholung als Universalersatz.

### Navigation
- ab 761 px Flex-Zeile statt 4×2;
- alle 8 Welten exakt gleiche Item-/Labelhöhe;
- Submenu-Pfeil absolut positioniert und kann `Sammeln` nicht mehr vertikal verschieben;
- Navigation liegt bottom -1 px an der Headerkante.

### Monetarisierung
Unverändert aus 1.50.624:
- keine Produkte zwischen Kategorie-Reihen;
- Banner füllt nur freie Restbreite;
- Produkte außerhalb des Kategorienrasters.

## Lokaler Hardtest

PHP:
**10/10 PASS**

ZIP:
PASS

Bilder:
- 65 Dateien;
- 65× 600×320;
- 65 eindeutige SHA-256;
- dHash-Minimalabstand 96;
- zentraler Kategoriebaum: 65/65 direkte Kinder besitzen passendes v150625-Asset.

Featured-Image-Negativtest:
- simuliertes identisches WordPress-Featured-Image vorhanden;
- Renderer liefert trotzdem das kontrollierte `audio-hifi-v150625.webp`;
- PASS.

Navigation / Playwright:
- 1600 / 1200 / 1024 / 900 / 800 / 761 px:
  - horizontaler Overflow 0;
  - alle acht Labels exakt gleiche Y-/Bottom-Koordinate;
  - `Sammeln` exakt gleiche Baseline;
- 760 px: Mobilepfad;
- Sammeln-Flyout bei allen getesteten Desktop-/Tabletbreiten sichtbar und innerhalb des Viewports.

## EXAKT EINE NEXT ACTION

**1.50.625 installieren und Technik + Pflanzen live prüfen: Bildwiederholungen und Sammeln-Baseline.**
