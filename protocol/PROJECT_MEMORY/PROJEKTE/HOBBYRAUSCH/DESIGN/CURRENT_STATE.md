# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-12
STATUS: **1.50.644 LOCAL HARD PASS / WORDPRESS-LIVE PILOT BUCH & PAPIER OFFEN**

## Kandidat
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.644_HOBBY_DEPOT_LEVEL1_CARD_COPY_HEADER_CLAIM_UNDERLINE_LOCALPASS.zip`

SHA-256:
`da5be83cfab375759448e0ae995734e3cddf739241fad4ca5841c44b203da9c0`

Library:
`/hobby rausch/AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.644_HOBBY_DEPOT_LEVEL1_CARD_COPY_HEADER_CLAIM_UNDERLINE_LOCALPASS.zip`

## Live-Befund bis 1.50.643
- Unterstrich noch etwas zu tief;
- Header-Claim `Hobbys. Ideen. Möglichkeiten.` live noch nicht sichtbar kräftiger;
- Buch-&-Papier-Unterkategoriekarten wichen trotz vorheriger Versuche noch von der bereits korrekten Ebene-1-Bild-/Kartenlogik ab;
- 1.50.643 wurde deshalb verworfen.

## Delta 1.50.644
- Unterstrich 5 px höher gegenüber 1.50.643;
- Header-Claim ohne Größenänderung tatsächlich verdickt: Original-Sprite plus zwei deckungsgleiche, horizontal ±0,75 px versetzte Sprite-Lagen;
- Buch-&-Papier-Unterkategorien verwenden jetzt **keinen eigenen Karten-/Bild-Sonderweg mehr**;
- Markup und CSS-Pfad sind exakt die vorhandenen Ebene-1-Klassen:
  - `hd-next-grid`;
  - `hd-next-card has-photo`;
  - `hd-next-photo`;
  - `hd-next-card-body`;
  - `hd-next-copy`;
  - `hd-row-size-*`;
- damit werden Raster, Bildwrapper, Cropping, Overflow und responsive Verhalten 1:1 aus Ebene 1 übernommen.

## Lokal geprüft / simuliert
- PHP **46/46 PASS**;
- ZIP-Integrität PASS;
- aktive Version/Class/Templates intern konsistent auf 1.50.644;
- Browser-Render mit echten Plugin-CSS + echten Pilotbildern:
  - 1440: 3 + 2 Karten;
  - 900: 2 + 2 + 1 Karten;
  - 760: 1-spaltig;
  - 1440 / 1024 / 900 / 760: horizontaler Overflow 0;
- Bildwrapper gegen Kartenborder gemessen: links/oben exakt 0 px nach Abzug des 1-px-Kartenrahmens;
- Bild gegen Bildwrapper: Δ X/Y/Breite/Höhe jeweils 0;
- Foto-Margin 0, Padding 0, Radius 0, overflow hidden, object-fit cover;
- Claim-Verdickungs-Lagen im gerenderten CSS aktiv.

## Freeze
Alles außerhalb dieser drei Punkte bleibt unverändert:
- Unterstrich-Position;
- Header-Claim-Dicke;
- Buch-&-Papier-Unterkategoriekarten.

## EXAKT EINE NEXT ACTION
**1.50.644 installieren und live ausschließlich Buch & Papier + Header-Claim prüfen.**
