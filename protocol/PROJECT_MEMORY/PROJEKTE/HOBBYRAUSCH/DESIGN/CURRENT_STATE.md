# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-12
STATUS: **1.50.645 LOCAL HARD PASS / WORDPRESS-LIVE PILOT BUCH & PAPIER OFFEN**

## Kandidat
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.645_HOBBY_DEPOT_BP_EXACT_LEVEL1_CARDS_BANNER_CLEAN_IMAGES_CLAIM_FIX_LOCALPASS.zip`

SHA-256:
`03cacb5faebec8cd579b0050ce64be100819ca6e0bc861ef9bfe477f1105306c`

Library:
`/hobby rausch/AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.645_HOBBY_DEPOT_BP_EXACT_LEVEL1_CARDS_BANNER_CLEAN_IMAGES_CLAIM_FIX_LOCALPASS.zip`

## Delta 1.50.645
Nur die erneut beanstandeten Punkte:
- Unterstrich exakt auf den 1.50.643-PASS-Stand zurückgesetzt;
- Header-Claim real im Logoasset verdickt, ohne Größe/Lage der restlichen Logobestandteile zu ändern;
- fünf Pilot-Kategoriebilder von eingebrannten weißen/gerundeten Screenshot-Rändern bereinigt;
- Buch-&-Papier-Karten verwenden unverändert die vorhandenen Ebene-1-Klassen und -CSS;
- fünf Unterkategorien: erste Reihe 3; zweite Reihe 2 links + Affiliate-Banner im freien dritten Platz;
- kein separates Banner später noch einmal.

## Lokal geprüft
- PHP **49/49 PASS**;
- ZIP PASS;
- Browser-Simulation mit echter Plugin-CSS-Kaskade und echten Bildern:
  - 1440: 3 + 2 + Banner;
  - 1024: 3 + 2 + Banner;
  - 900: responsive 2-spaltig;
  - 760: 1-spaltig;
  - horizontaler Overflow überall 0;
- Bildwrapper/Card-Rahmen: Offset nach 1-px-Rahmen exakt 0;
- Bild/Wrapper: X/Y/Breite/Höhe jeweils Δ 0;
- Bild-Radius 0, Margin 0, Padding 0, object-fit cover;
- bereinigte Quellbilder: keine weißen/gerundeten Eckmasken mehr;
- Logo-Pixeldiff oberhalb Claim-Band: 0 sichtbare Pixel; Änderungen ausschließlich im Claim-Band.

## EXAKT EINE NEXT ACTION
**1.50.645 installieren und live nur Buch & Papier + Header-Claim prüfen.**
