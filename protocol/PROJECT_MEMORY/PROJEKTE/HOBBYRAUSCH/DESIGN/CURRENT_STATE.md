# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-12
STATUS: **1.50.634 LOCAL HARD PASS / WORDPRESS-LIVE BILDABNAHME OFFEN**

## Kandidat
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.634_HOBBY_DEPOT_CATEGORY_PREVIEWS_WIDER_CLEAR_NO_FRAME_LOCALPASS.zip`

SHA-256:
`b7347fd4925fb201165b8763ae8ae2f054811dfcb38a167cd6dee04b4f728b75`

Library:
`/hobby rausch/AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.634_HOBBY_DEPOT_CATEGORY_PREVIEWS_WIDER_CLEAR_NO_FRAME_LOCALPASS.zip`

## Live bestätigt / eingefroren
- Hauptnavigation: PASS;
- Logo/Claim/Navigationsstand aus 1.50.631: PASS, nicht weiter verändern;
- Hero-Bilder: nicht Teil dieser Korrektur, unverändert;
- Hero-Texte Ebene 1: PASS;
- Seitenendtexte Ebene 1 mit maximal drei internen Links: PASS.

## Letzter Live-Fehler
Kategorie-Vorschaubilder:
- sichtbarer Rahmen/Passepartout durch eingerückte Bildbox;
- Bildwirkung weiterhin teilweise zu nah und zu voll;
- 1.50.632 war kein belastbarer Bildfix.

## Delta 1.50.634
Nur Kategorie-Vorschaubilder Ebene 1:
- 65 kontrollierte aktive Vorschauassets;
- weiter gefasste, visuell geprüfte Szenen;
- klare Hauptmotive, weniger konkurrierende Randdetails;
- kein künstliches Bild-im-Bild / kein Canvas-Rahmen;
- finale CSS-Regel: Vorschau füllt ihren Bildslot ohne Margin/Padding/Border/Radius;
- Desktop 200×107, Tablet 165×88, Mobile 145×78;
- kein Hub1-Fallback auf alte WordPress Featured Images;
- Hero-Assets byte-identisch zu 1.50.631;
- Header-/Navigationsrendering gegenüber 1.50.631 unverändert bis auf Releasekennung.

## Lokal geprüft / simuliert
- PHP 16/16 PASS;
- ZIP-Integrität PASS;
- 65 aktive Kategorie-Vorschaubilder;
- 65/65 SHA-eindeutig;
- aktive Bildquellen: 48× v150629, 11× visuell geprüfte weitere v150623-Szenen, 6× v150616;
- kompletter Kartenbereich mit echten Assets simuliert:
  - 1440 px: 200×107, Rahmengeometrie 0;
  - 930 px: 165×88, Rahmengeometrie 0;
  - 760 px: 145×78, Rahmengeometrie 0;
- keine Änderung an Hero-Dateien.

## EXAKT EINE NEXT ACTION
**1.50.634 installieren und live nur die Kategorie-Vorschaubilder prüfen. Bei PASS direkt nächste Kategorieebene.**
