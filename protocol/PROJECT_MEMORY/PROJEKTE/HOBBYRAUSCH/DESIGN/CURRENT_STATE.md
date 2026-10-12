# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-12
STATUS: **1.50.640 LOCAL HARD PASS / WORDPRESS-LIVE PILOT BUCH & PAPIER OFFEN**

## Kandidat
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.640_HOBBY_DEPOT_BUCH_PAPIER_BODY_ALIGN_FADE_BRUSH_LEVEL1_IMAGEFORMAT_LOCALPASS.zip`

SHA-256:
`588fa7fb961bc9cdf62a96f968a83034b072902c41eaddee5c92d09598ebe6bd`

Library:
`/hobby rausch/AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.640_HOBBY_DEPOT_BUCH_PAPIER_BODY_ALIGN_FADE_BRUSH_LEVEL1_IMAGEFORMAT_LOCALPASS.zip`

## Pilot-Scope
**Ausschließlich Hub2 `Buch & Papier`.**

Delta zu 1.50.639:
- Hero wieder exakt im normalen Body-Container ausgerichtet;
- Text- und Bildbereich teilen dieselbe linke/rechte Contentachse wie die folgenden Abschnitte;
- Claim `Papier kann mehr.` mit Handschrift-Fontstack und dynamischerem CSS-Pinselstrich mit mehr Abstand;
- Hero-Bild bleibt das bestehende Kategorieasset, kein neues Bild;
- Hero-Bild läuft links weich in Weiß aus;
- Hero-Bild hat festes 600:320-Verhältnis und wächst beim Öffnen des Aufklapptexts **nicht** mit;
- Kachelbilder übernehmen exakt das Bildformat der Ebene darüber:
  - Desktop 200×107;
  - Tablet 165×88;
  - Mobil 145×78;
- 3/2/1-Kachelraster bleibt;
- Produkte → 3 Beiträge → Banner → Werbeplatz bleibt;
- kein Seitenendtext.

## Freeze / unverändert
- Asset-Sammlung **852/852 byteidentisch zu 1.50.639**;
- keine neuen Bilder;
- Header/Nav unverändert;
- Ebene 1 unverändert;
- andere Hub2 unverändert;
- Produkt-/Banner-/Werbeplatzlogik unverändert;
- keine Taxonomie-/Architekturänderung.

## Lokal geprüft / simuliert
- PHP **34/34 PASS**;
- ZIP-Integrität PASS;
- 1440:
  - Hero-Left = Section-Left 120 px;
  - 3+2 Kacheln;
  - Kartenbild 200×107;
  - Overflow 0;
  - Hero-Bild vor/nach Aufklappen Δ 0×0;
- 1024:
  - Hero-Left = Section-Left 36 px;
  - 2+2+1 Kacheln;
  - Kartenbild 165×88;
  - Overflow 0;
  - Hero-Bild vor/nach Aufklappen Δ 0×0;
- 760:
  - Hero-Left = Section-Left 12 px;
  - 1-spaltig;
  - Kartenbild 145×78;
  - Overflow 0;
  - Hero-Bild vor/nach Aufklappen Δ 0×0;
- Assets geändert: **0**.

## EXAKT EINE NEXT ACTION
**1.50.640 installieren und live ausschließlich `Fertigen → Buch & Papier` prüfen.**
