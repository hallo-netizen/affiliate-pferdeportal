# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-14
STATUS: **1.50.653 VERWORFEN / 1.50.654 LIVE FAIL / 1.50.655 SAFE-FIX LOKAL PASS / 65/65 HEROES + 65/65 KATEGORIEVORSCHAUEN + 75/328 KARTEN / KEIN LIVE-PASS**

## Bildstand
- **65/65** Hero-Motive vorhanden, exakt **600×220**;
- **65/65** Kategorievorschauen vorhanden, exakt **200×107**;
- **75/328** Kartenbilder vorhanden;
- **253** Karten offen.

## Verworfen
- `AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.653_HOBBY_DEPOT_HERO_COMPLETE_FIXED_INSTALL.zip`: Fatal wegen gebrochener Release-Kette.
- `AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.654_HOBBY_DEPOT_FATAL_FIX.zip`: **LIVE FAIL**. Auf `/gestalten/druck-foto/` erschien nach Installation nicht das eigene Hobby-Depot-Template, sondern der generische Theme-/Seitenstand. Deshalb verworfen.

## Exakt gefundene zusätzliche Fehler
1. Die 65 neuen 200×107-Kategorievorschauen lagen zwar im Assetbaum, wurden von `next_level_card_photo()` für Ebene 1 aber **gar nicht verwendet**. Der Code zeigte weiter den alten `v150617/subcategories/*-v150634.webp`-Bildsatz.
2. Der Pinselstrich unter dem Claim war zu lang, weil `.hd-bp-hero-copy` seit 1.50.651 ein Flex-Container ist und `.hd-bp-brush-claim` dadurch horizontal auf Spaltenbreite gestreckt wurde.
3. Die Hub2-Hero-Container verwendeten noch 600/320 bzw. mobil 16/8.4, obwohl der verbindliche Hero-Bildstand 600×220 ist.

## Aktueller Reparaturkandidat 1.50.655
Paket:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.655_HOBBY_DEPOT_SAFE_IMAGE_FIX.zip`

SHA-256:
`51042a8ed717603c88e10e7286c0e00514a450c19cf0f009746bcc2893f48c30`

### Sicherheitsprinzip
1.50.655 wurde **nicht** wieder mit neuer Profilklasse/neuen Templates gebaut. Basis ist der funktionierende 1.50.651-Code:
- aktive Profilklasse bleibt `Hobby_Depot_Profile_V150651`;
- aktive Templates bleiben `hobby-depot-front-v150651.php` und `hobby-depot-content-v150651.php`;
- beide aktiven Templates sind **byte-identisch** zum 1.50.651-Ausgangsstand;
- `is_owned_content_route()` und `route_template()` sind **byte-identisch** zu 1.50.651;
- geändert wurden nur Plugin-/Releaseversionsnummer, Bildquellenbindung, Ebene-1-Vorschaubildbindung, Unterstrich-Stretch-Fix und Hub2-Hero-Seitenverhältnis.

### Lokale Prüfung des exakten ZIPs
- ZIP-Integrität PASS;
- **58/58 PHP-Dateien Syntax PASS**;
- Hostsimulation `hobby-depot.de` → Profil `hobby_depot` PASS;
- Seitensimulation `/gestalten/druck-foto/` → Seitentyp `hub2` PASS;
- Routing → `templates/hobby-depot-content-v150651.php` PASS;
- 65/65 Hero-Dateien real vorhanden und 600×220;
- 65/65 Kategorievorschauen real vorhanden und 200×107;
- 65 Hero-Dateien exakt-dublettenfrei;
- 65 Vorschauen exakt-dublettenfrei;
- 75/75 gemappte Karten real vorhanden und 200×107;
- Ebene-1-Test `Druck & Fotografie` → `assets/hobby-depot-v150653/previews/druck-foto.webp` PASS;
- Hub2-Hero-Test `Druck & Fotografie` → `assets/hobby-depot-v150653/heroes/druck-foto.webp` PASS;
- Karten-Test `Cyanotypie` → `assets/hobby-depot-v150653/cards/druck-foto/cyanotypie.webp` PASS;
- Claim-Fix: `align-self:flex-start; width:max-content`;
- Hub2-Hero-Anzeigeverhältnis auf 600/220 vereinheitlicht.

## Eingefroren
- Textinhalt aus 1.50.650;
- Grundaufteilung aus 1.50.650;
- Buch & Papier 1.50.645 als visuelle Referenz;
- Header, Navigation, Ebene 1, Taxonomie, Architektur und Monetarisierungsreihenfolge.

## EXAKT EINE NEXT ACTION
**1.50.653 und 1.50.654 nicht mehr verwenden. 1.50.655 installieren/aktivieren und danach ausschließlich `/gestalten/druck-foto/` live prüfen. Erst bei realem Live-PASS weiterarbeiten.**

## Persistenter Zwischenstand
- `AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.655_HOBBY_DEPOT_SAFE_IMAGE_FIX.zip`;
- dauerhaft unter `/hobby rausch/WIP_1.50.653_WORKING/` gesichert;
- kein finales Release-Artefakt; Reparatur-/Prüfstand.
