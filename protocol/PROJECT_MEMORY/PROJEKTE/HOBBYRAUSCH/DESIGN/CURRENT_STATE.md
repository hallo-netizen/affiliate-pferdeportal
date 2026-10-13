# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-13
STATUS: **1.50.651 LOCAL HARD PASS / WORDPRESS-LIVE HERO OFFEN**

## Kandidat
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.651_HOBBY_DEPOT_HUB2_HERO_LAYOUT_WIDE_SCENES_RESPONSIVE_LOCALPASS.zip`

SHA-256:
`ceed21dbc62fd207b891deb5272351c57f31079e22193804546e2dcf6d8f8427`

Library:
`/hobby rausch/AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.651_HOBBY_DEPOT_HUB2_HERO_LAYOUT_WIDE_SCENES_RESPONSIVE_LOCALPASS.zip`

## Live-Befund 1.50.650
Vom Nutzer bestätigt:
- Textinhalt PASS;
- Grundaufteilung PASS.

Beanstandet:
- Hero-Bilder teils zu nah / zu detailig;
- mittlere Bildschirmbreiten / Tablet: Text + Hero nebeneinander zu gequetscht;
- Kategoriekartenbilder weiterhin eigener offener Fehlerblock.

## 1.50.651 – Arbeitsschritt 1: alle Hub2-Heroes
Nur Hero-Bereich / Hero-Bildauswahl geändert. Kategoriekarten bleiben technisch exakt auf dem Stand 1.50.650 und werden erst im zweiten Arbeitsschritt korrigiert.

### Hero-Textaufbau
- 65/65 Hub2-Seiten behalten individuellen Brush-Claim + H1;
- 65/65 erhalten einen eigenen kurzen, direkten Einsteigertext;
- bestehender langer regelkonformer Hub2-Text inhaltlich unverändert;
- langer Text steht jetzt unter dem Hero:
  - sichtbarer Lead;
  - Rest über `Mehr zu <Kategorie> erfahren`;
- kein zweiter Zusatztextblock.

### Responsive
- >1100 px: kurzer Hero-Text links / Hero rechts, **38/62**;
- <=1100 px: Claim + H1 + kurzer Einstieg oben, Hero in voller Body-Breite darunter, langer Text danach;
- damit kein gequetschter Tablet-Split mehr;
- Hero bleibt im 600×320-Quellverhältnis, damit keine zusätzliche Crop-/Zoom-Vergrößerung entsteht.

### Hero-Bilder
- alle 65 Hero-Pfade erneut visuell über die vorhandenen Varianten geprüft;
- 65/65 deterministisch gebunden;
- 65/65 unterschiedliche Hero-Dateien;
- weiter gefasste vorhandene Varianten bevorzugt;
- v150631-Vignettenserie vollständig ausgeschlossen;
- `Papier & Dokumente` auf ein papier-/briefmarkenbezogenes Motiv ohne Münz-Hauptmotiv umgestellt;
- keine neuen Bildassets erzeugt.

## Lokal geprüft
- PHP **58/58 PASS**;
- ZIP PASS;
- Release-Kette vollständig V150651; aktive V150650-Bindung im aktiven Pfad: 0;
- Hero-Mappings: 65; unique: 65; Missing: 0; v150631: 0;
- individuelle Hero-Einstiege: 65/65;
- bestehender Langtext-Generator byte-/blockgleich zu 1.50.650;
- Karten-Map vollständig unverändert zu 1.50.650;
- echte Browser-CSS-Simulation bei 1440 / 1200 / 1100 / 1024 / 900 / 760 / 600:
  - Overflow 0;
  - >1100 Split;
  - <=1100 sauber gestapelt;
  - langer Text immer unterhalb des Hero;
- visuelle Renderprüfung u. a. `Papier & Dokumente` bei 1440 / 1200 / 1024 / 900 / 600.

## OFFEN – Arbeitsschritt 2
**Unterkategoriekartenbilder**:
- semantisch sauber Kategorie für Kategorie;
- weiter herausgezoomt / weniger voll;
- keine falschen Motive;
- keine doppelten Motive innerhalb der Seite;
- keine eingebrannten Rahmen.

## EXAKT EINE NEXT ACTION
**1.50.651 installieren und live nur den Hero-/Textbereich auf Desktop + Tablet + Mobil prüfen. Danach ohne Layoutumbau Arbeitsschritt 2: Kategoriekartenbilder.**
