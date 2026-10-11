# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-11
STATUS: **1.50.618 LOCAL STRUCTURAL HARD PASS / WORDPRESS-LIVE OFFEN**

## Kandidat
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.618_HOBBY_DEPOT_LIVE_LAYOUT_MONETIZATION_FIX_LOCALPASS.zip`

SHA-256:
`0498a836102540f02a890ac02e415a0bf60d33418d51a2385e15efb4543ee203`

Library:
`/hobby rausch/AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.618_HOBBY_DEPOT_LIVE_LAYOUT_MONETIZATION_FIX_LOCALPASS.zip`

## Korrekturen

Header:
- Logo natürliches Seitenverhältnis; keine Max-Height-Verzerrung;
- Logo linksbündig;
- Desktop-Logo 248 px breit;
- eigene 148-px-Logozeile + 48-px-Navigationszeile;
- Navigation dadurch real tiefer;
- Flyouts wieder am auslösenden Weltpunkt verankert statt links versetzt.

Hub1:
- Hero und Aufklapptext werden jetzt aus demselben Text **geteilt**;
- bereits im Hero sichtbarer Lead wird im Aufklapptext nicht erneut ausgegeben;
- Fold weiter full-width/neutral mit Absätzen.

Unterkategorien:
- 7 Gestalten-Motive unverändert eindeutig;
- Bildflächen jetzt kompakte einheitliche Querformat-Thumbnails 132×70 im Desktopkartenlayout;
- keine großflächigen 50%-Kartenbilder mehr.

Affiliate:
- Banner sitzt als volle Partnerzeile **im Kartenraster nach der ersten Kategoriezeile**;
- Produkte sitzen als native Partnerkarten im selben Raster;
- bei Gestalten (7 Kategorien) füllen im eingeloggten Leerzustand 2 Produktplätze die letzte Reihe zusammen mit Kategorie 7;
- keine separaten Affiliate-Blöcke danach.

Verkaufbare Werbung:
- neues Einzelfoto;
- dunkler Lesbarkeitsverlauf;
- türkisfarbener echter Brushstroke hinter der Headline;
- heller CTA.

## Lokale Prüfung
PASS:
- PHP 10/10;
- Fresh-Unpack PHP 10/10;
- ZIP-Integrität;
- Plugin-/Klassenbindung 1.50.618;
- Hero-Text kommt im Fold nicht erneut vor;
- 7 Kategorie-Karten;
- Affiliate-Banner und 2 Produktplätze direkte Kinder desselben Next-Level-Grids;
- keine Standalone-Affiliate-Sektionen;
- Rental genau ein Hintergrundbild;
- Logo-CSS ohne verzerrende Max-Höhe;
- Flyout-CSS relativ zum Weltpunkt.

Lokaler Browser-Screenshot konnte in dieser Laufzeitumgebung nicht zuverlässig gestartet werden; deshalb wird **kein Browser-PASS erfunden**.

## Erster offener Blocker
WordPress-Live-Abnahme 1.50.618.

## EXAKT EINE NEXT ACTION
**1.50.618 installieren und Gestalten live prüfen.**
