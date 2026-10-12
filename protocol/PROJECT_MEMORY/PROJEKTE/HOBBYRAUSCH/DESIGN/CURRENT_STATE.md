# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-12
STATUS: **1.50.635 LOCAL HARD PASS / WORDPRESS-LIVE HUB2 OFFEN**

## Kandidat
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.635_HOBBY_DEPOT_HUB2_CONTENT_MONETIZATION_LOCALPASS.zip`

SHA-256:
`1cdeb892906e29505cf300125f051a68b7b7cd1ecc2099202e828a4276713615`

## Live bestätigt / eingefroren
- Ebene 1 wird vorerst akzeptiert; Kategorie-Vorschaubilder nicht perfekt, aber keine weitere Bildrunde jetzt;
- Hauptnavigation: PASS;
- Logo/Claim/Navigationslinie: PASS;
- Hero-Bilder Ebene 1: unverändert / nicht anfassen;
- Hero-Texte Ebene 1: PASS;
- Seitenendtexte Ebene 1 mit maximal drei internen Links: PASS.

## Delta 1.50.635 – nur Kategorieebene 2 / Hub2
Oben:
- Breadcrumb;
- H1 + kurzer Orientierungstext;
- **kein Hero-Foto**.

Danach feste Reihenfolge:
1. Verweise auf die reale nächste Ebene;
2. separater Affiliate-Banner;
3. passende Artikelvorschau;
4. konkrete Affiliate-Produkte für den aktuellen Hub2-Kontext;
5. genau ein direkt verkaufbarer Werbeplatz;
6. längerer redaktioneller Erklärungstext am Seitenende.

Monetarisierung:
- Hub2 verwendet die `category_product_1..3`-Slots statt der breiteren Hub1-Produkte;
- dadurch wird die Produktbelegung mit zunehmender Tiefe konkreter;
- Produkte stehen nicht im Unterkategorie-Raster;
- Banner steht als eigener Bereich nach der nächsten Ebene;
- öffentlich leere Affiliate-Slots bleiben unsichtbar, eingeloggte Vorschau bleibt möglich.

## Unverändert
- komplette Asset-Sammlung: **847/847 Dateien byteidentisch zu 1.50.634**;
- alle Hero-Dateien byteidentisch;
- Header-/Navigation-CSS unverändert;
- Ebene 1 unverändert;
- Taxonomie/Architektur/HD-001/HD-004 unverändert;
- Affiliate-Zentrale bleibt Slot-/Monetarisierungsautorität.

## Lokal geprüft / simuliert
- PHP: **19/19 PASS**;
- ZIP-Integrität PASS;
- aktive V150635-Klasse/Templates PASS;
- Hub2: 0 Hero-Fotos im simulierten Pfad;
- DOM-Reihenfolge 1440 / 1024 / 760 PASS:
  nächste Ebene → Banner → Beiträge → Produkte → Werbeplatz → Langtext;
- horizontaler Overflow: 0 bei 1440 / 1024 / 760;
- Asset-Regression: 847/847 byteidentisch;
- neue CSS-Regeln enthalten keine Header-/Nav-/Logo-/Hero-Selektoren.

## EXAKT EINE NEXT ACTION
**1.50.635 installieren und live eine reale Hub2-Seite prüfen. Bei PASS danach auf Kategorieebene 3 weitergehen.**
