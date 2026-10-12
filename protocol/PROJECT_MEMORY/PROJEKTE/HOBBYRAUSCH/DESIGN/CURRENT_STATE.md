# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-12
STATUS: **1.50.641 LOCAL HARD PASS / WORDPRESS-LIVE PILOT BUCH & PAPIER OFFEN**

## Kandidat
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.641_HOBBY_DEPOT_BRUSH_STROKE_2PX_FRAMES_LOCALPASS.zip`

SHA-256:
`b9acd0b3170782f5633d52d3200c58f9c798c48712d7bca36bcaed00c466b9b8`

Library:
`/hobby rausch/AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.641_HOBBY_DEPOT_BRUSH_STROKE_2PX_FRAMES_LOCALPASS.zip`

## Pilot-Scope
**Ausschließlich Hub2 `Buch & Papier`.**

Delta zu 1.50.640:
- Schriftgröße/-wirkung des Claims unverändert;
- Unterstrich auf Basis der freigegebenen Variante 1:
  - Beige/Sekundärfarbe;
  - länger und stärker geschwungen;
  - natürlicher echter Pinselcharakter;
  - mehr Abstand zur Schrift;
- Hero-Bild rechts: **2 px** Rundung nur an den rechten Ecken;
- Kategorie-Karten: maximal **2 px** Rundung;
- Kategorie-Bilder: **1 px** Innenrundung links, exakt innerhalb des Kartenrahmens;
- Bildformat bleibt Ebene-1-konform: 200×107 / 165×88 / 145×78;
- Aufklapptext verändert Hero-Bildgröße weiterhin nicht.

## Freeze / unverändert
- 852/852 vorhandene Assets aus 1.50.640 byteidentisch;
- genau 1 neues Brush-Asset (7.114 Bytes);
- Header/Nav unverändert;
- Ebene 1 unverändert;
- andere Hub2 unverändert;
- Produkt-/Banner-/Werbeplatzlogik unverändert;
- keine Taxonomie-/Architekturänderung.

## Lokal geprüft / simuliert
- PHP **37/37 PASS**;
- ZIP-Integrität PASS;
- 1440 / 1024 / 760:
  - Overflow 0;
  - Hero-Radius rechts 2 px;
  - Hero-Bild vor/nach Aufklappen Δ 0×0;
  - Kartenradius 2 px;
  - Kartenbild liegt mit 1 px Kartenborder exakt innen;
  - Bild füllt seinen Bildslot exakt, Δ 0×0;
- Brush-Asset lokal geladen, Pinselstrich-Abstand 20 px, Claim-Abstand 28/27/26 px.

## EXAKT EINE NEXT ACTION
**1.50.641 installieren und live ausschließlich `Fertigen → Buch & Papier` prüfen.**
