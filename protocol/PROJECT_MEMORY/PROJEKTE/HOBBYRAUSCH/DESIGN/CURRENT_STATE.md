# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-12
STATUS: **1.50.628 LOCAL HARD PASS / WORDPRESS-LIVE OFFEN**

## Kandidat
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.628_HOBBY_DEPOT_NAV_RAISE_LARGER_IMAGES_LINK_CLEANUP_LOCALPASS.zip`

SHA-256:
`2e875f7f235e84c211143a71f19a8519314160a96d2b917e5ebd751d4a0df49b`

Library:
`/hobby rausch/AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.628_HOBBY_DEPOT_NAV_RAISE_LARGER_IMAGES_LINK_CLEANUP_LOCALPASS.zip`

## Delta 1.50.628

Navigation:
- gleiche Einzeilen-/Baseline-Logik aus 1.50.627 bleibt;
- Navigation wird gegenüber 1.50.627 um 8 px angehoben;
- finale CSS-Bindung: `bottom:5px`;
- Sammeln bleibt auf exakt derselben Label-Baseline wie die übrigen sieben Welten.

Hub-Karten:
- keine neue Bildserie;
- akzeptierte klare 65 Motive bleiben;
- **sichtbare Bildfläche wird größer**, damit das Hauptmotiv in der Karte besser erkennbar ist:
  - Desktop 200×107;
  - Tablet 165×88;
  - Mobile 145×78.

Seitenendtexte:
- kritische Prüfung: bisher waren zu viele interne Links gesetzt;
- jetzt maximal **3 interne Links pro Hauptwelt**;
- genau maximal einer pro Zwischenabschnitt;
- alle übrigen Kategorienennungen bleiben natürlicher Klartext.

## Lokal
- PHP 10/10 PASS;
- ZIP PASS;
- V150628 Main/Klasse/Templates konsistent;
- alte aktive V150624–V150627-Klassenreferenzen 0;
- 65 Hubassets / 65 eindeutige SHA-256;
- Link-Render-Test: alle 8 Hauptwelten exakt 3 interne Links und 3 Zwischenüberschriften;
- DOM/CSS-Simulation 1600/1200/1024/900/800/761:
  - horizontaler Overflow 0;
  - alle 8 Navlabels gleiche Y-/Bottom-Koordinate;
  - Sammeln gleiche Baseline;
  - Abstand Nav-Unterkante zur Headerlinie 6 px;
- 760 Mobilepfad.

## EXAKT EINE NEXT ACTION
**1.50.628 installieren und live nur Navigation + Kartengröße + Seitenendtext prüfen.**
