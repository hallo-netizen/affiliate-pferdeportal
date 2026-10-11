# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-11
STATUS: **1.50.622 LOCAL HARD PASS / WORDPRESS-LIVE OFFEN**

## Kandidat
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.622_HOBBY_DEPOT_TWO_COLUMN_HEADER_LOCALPASS.zip`

SHA-256:
`0de280b67edb7dbfd4d3ee86415038f281885f881bafba41f8799a073d23b1bd`

Library:
`/hobby rausch/AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.622_HOBBY_DEPOT_TWO_COLUMN_HEADER_LOCALPASS.zip`

## Header 1.50.622
Bestätigte Geometrie:
- Logo links als eigener Block über Such- und Navigationszeile;
- Navigation NICHT unter dem Logo;
- Suchfeld rechts oben, vertikal auf HOBBY-DEPOT-Wortmarkenlinie;
- Navigation rechts darunter;
- Navigationsicons entfernt;
- Logoasset unverändert, intern mit mehr Abstand Bogen/dein → HOBBY DEPOT → Claim;
- Claim optisch leicht verbreitert.

## Lokale Simulation
Playwright mit echtem Plugin-CSS/HTML:
- 1600 px: 0 horizontaler Overflow; 1 Navzeile; alle 8 gleiche Baseline.
- 1200 px: 0 Overflow; 1 Navzeile.
- 1024 px: 0 Overflow; 1 Navzeile.
- 900 px: 0 Overflow; Navigation 4×2 im rechten Bereich neben Logo.
- 760 px: bestehender Mobilepfad.

Desktop 1600:
- Header 156 px;
- Logo links 220×146;
- Search 820×34;
- Nav nur rechte Spalte.

## Fresh
- PHP 10/10 PASS.
- ZIP-Integrität PASS.
- Plugin-/Klassenbindung 1.50.622 PASS.
- Logoasset unverändert.

## EXAKT EINE NEXT ACTION
**1.50.622 installieren und Header live ansehen.**
