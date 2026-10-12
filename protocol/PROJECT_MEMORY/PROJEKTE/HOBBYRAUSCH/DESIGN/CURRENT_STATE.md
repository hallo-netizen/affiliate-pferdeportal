# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-12
STATUS: **1.50.624 LOCAL HARD PASS / WORDPRESS-LIVE OFFEN**

## Kandidat
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.624_HOBBY_DEPOT_NAV_BOTTOM_BANNER_FILL_NO_DUPLICATES_LOCALPASS.zip`

SHA-256:
`af8cb6a33c8da51d0153b9b22a7e6bb210e9cef4fe9e01545d9d31c33527b15c`

Library:
`/hobby rausch/AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.624_HOBBY_DEPOT_NAV_BOTTOM_BANNER_FILL_NO_DUPLICATES_LOCALPASS.zip`

## Delta 1.50.624

Navigation:
- Desktop/Tablet rechts neben Logo jetzt technisch **absolute bottom:0** an die untere Headerkante gebunden.
- keine weitere freie vertikale Interpretation.

Unterkategorie-Raster:
- keine Affiliate-Produkte mehr zwischen Kategorie-Reihen;
- Banner füllt nur die letzte unvollständige 3er-Reihe:
  - Rest 1 → Banner = 2 Kartenbreiten;
  - Rest 2 → Banner = 1 Kartenbreite;
  - Rest 0 → Banner volle eigene Zeile.
- Produkte werden außerhalb des Kategorie-Rasters als natives Empfehlungsmodul ausgegeben.

Bilder:
- 65/65 aktive erste Hub-Unterkategorien bebildert;
- 65/65 **unterschiedliche SHA-256-Bildhashes**;
- altes doppeltes Genuss/Essbare-Pflanzen-Motiv beseitigt;
- ungenutzte Alias-/Duplikatbilder entfernt.

## Lokal
- PHP 10/10 PASS;
- ZIP-Integrität PASS;
- 65/65 aktive Bildpfade;
- 65/65 eindeutige aktive Bildhashes;
- 65 vorhandene Subcategory-Assets / 65 eindeutige Hashes;
- Produkte werden in render_next_level/render_term_next_level nicht mehr eingefügt;
- Banner-Span-Regeln geprüft;
- statischer Layout-Render für 7 Kategorien + 2-Kartenbreiten-Banner erfolgreich.
- Chromium war in dieser Laufzeitumgebung nicht zuverlässig startbar; kein Browser-PASS erfunden.

## EXAKT EINE NEXT ACTION
**1.50.624 installieren und Technik/Gestalten live prüfen – besonders Navigation unten und Bannerfüllung.**
