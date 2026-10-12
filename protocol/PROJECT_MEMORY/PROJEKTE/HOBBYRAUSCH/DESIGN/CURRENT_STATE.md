# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-12
STATUS: **1.50.639 LOCAL HARD PASS / WORDPRESS-LIVE PILOT BUCH & PAPIER OFFEN**

## Kandidat
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.639_HOBBY_DEPOT_BUCH_PAPIER_SPLIT_HERO_BRUSH_3COL_LOCALPASS.zip`

SHA-256:
`080b56efd53102de7fde5c01f75b0a9edb53c8a3f4123c1e204b2ded5b1955f2`

Library:
`/hobby rausch/AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.639_HOBBY_DEPOT_BUCH_PAPIER_SPLIT_HERO_BRUSH_3COL_LOCALPASS.zip`

## Pilot-Scope
**Ausschließlich Hub2 `Buch & Papier`.**

Delta zu 1.50.638:
- kompakter Split-Hero oben;
- links Claim/H1/Lead/Aufklapper, rechts vorhandenes Kategorie-Vorschaubild;
- **kein neues Hero-Bild erzeugt**: verwendet wird vorhandenes `buch-papier-v150629.webp`;
- Claim `Papier kann mehr.` mit CSS-Pinselstrich;
- Desktop: 3 Fotokacheln nebeneinander;
- Tablet: 2;
- Mobile: 1;
- Reihenfolge bleibt: Kategorien → Produkte → 3 Beiträge → Banner → Werbeplatz;
- weiterhin kein Seitenendtext.

## Performance
- Hero verwendet bestehendes 600×320-Asset, **45.934 Bytes**;
- keine neuen Bilddateien gegenüber 1.50.638;
- 5 Pilotkartenbilder bleiben zusammen ca. 66 KB und lazy geladen.

## Freeze / unverändert
- komplette Asset-Sammlung: **852/852 Dateien byteidentisch zu 1.50.638**;
- Header/Nav unverändert;
- Ebene 1 unverändert;
- alle anderen Hub2-Seiten unverändert;
- Produkt-/Banner-/Werbeplatzlogik unverändert;
- keine Taxonomie-/Architekturänderung.

## Lokal geprüft / simuliert
- PHP **31/31 PASS**;
- ZIP-Integrität PASS;
- aktive V150639-Klasse/Templates PASS;
- Pilot-Gate ausschließlich `buch-papier`;
- 1440 px:
  - 3 Kacheln;
  - Hero 2-spaltig;
  - horizontaler Overflow 0;
- 1024 px:
  - 2 Kacheln;
  - Hero 2-spaltig;
  - horizontaler Overflow 0;
- 760 px:
  - 1 Kachel;
  - Hero gestapelt;
  - horizontaler Overflow 0;
- Pinselstrich-Claim im Browser gerendert;
- bestehende Asset-Dateien geändert: **0**.

## EXAKT EINE NEXT ACTION
**1.50.639 installieren und live ausschließlich `Fertigen → Buch & Papier` prüfen.**
