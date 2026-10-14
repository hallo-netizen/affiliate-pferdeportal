# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-14
STATUS: **1.50.652 LETZTER BUILD / VISUAL FAIL / WIP 1.50.653 BILDBASIS REAL / 65/65 HEROES + 65/65 KATEGORIEVORSCHAUEN + 75/328 KARTEN / 1.50.653 INSTALLPAKET VERWORFEN / 1.50.654 FATAL-FIX LOKAL PASS / KEIN LIVE-PASS**

## Letzter paketierter Stand
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.652_HOBBY_DEPOT_HUB2_HERO_COMPACT_EXACT_SCENES_NOUPSCALE_LOCALPASS.zip`

SHA-256:
`c5c19f94b57c9dd95d88738f752e6e1ea5d880ea6d85ebc7bb31cfdd6b17234b`

## Bildstand
- **65/65** Hero-Motive vorhanden, exakt **600×220**;
- **65/65** zugehörige Kategorievorschauen vorhanden, exakt **200×107**;
- **75/328** Kartenbilder vorhanden;
- **253** Karten offen;
- Kartenstand beim Hero-Abschluss unverändert.

## Fehler 1.50.653 – exakt gefunden
Das Paket `AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.653_HOBBY_DEPOT_HERO_COMPLETE_FIXED_INSTALL.zip` ist **verworfen**.

Ursache des Frontend-Fatals:
- Main-Plugin lud nur `Hobby_Depot_Profile_V150653`;
- die neu angelegten Templates `hobby-depot-front-v150653.php` und `hobby-depot-content-v150653.php` riefen aber weiterhin `Hobby_Depot_Profile_V150651::...` auf;
- dadurch konnte auf den gerouteten Hobby-Depot-Seiten die nicht geladene Klasse `Hobby_Depot_Profile_V150651` aufgerufen werden → Fatal Error / kritischer Fehler.

## Korrigierter Installationsstand 1.50.654
Paket:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.654_HOBBY_DEPOT_FATAL_FIX.zip`

SHA-256:
`65c21010a9f63a5742e2d16f4b1b8bfcafb80a9fa35df7d5c1ef3628384b3319`

Lokale Prüfung:
- vollständiger Pluginbaum mit Root `affiliate-portal-template-kit/`;
- Plugin-Version/Const **1.50.654**;
- Main-Plugin lädt `Hobby_Depot_Profile_V150654`;
- Front- und Content-Template rufen ausschließlich `Hobby_Depot_Profile_V150654` auf;
- alter fehlerhafter `V150651`-Klassenaufruf in den aktiven 1.50.654-Templates: **0**;
- PHP-Syntaxprüfung aller Dateien PASS;
- simuliertes Laden des Hauptplugins mit WordPress-Hook-Stubs: **ACTIVATION_INCLUDE_PASS**;
- Front-Template Klassenbindung PASS;
- Content-Template Klassenbindung PASS;
- ZIP-Integrität PASS;
- Bildassets bleiben im geprüften `hobby-depot-v150653`-Assetbaum und werden von 1.50.654 verwendet.

## Eingefroren
- Textinhalt aus 1.50.650;
- Grundaufteilung aus 1.50.650;
- Buch & Papier 1.50.645 als visuelle Referenz;
- Header, Navigation, Ebene 1, Taxonomie, Architektur und Monetarisierungsreihenfolge.

## EXAKT EINE NEXT ACTION
**1.50.653 nicht mehr verwenden. 1.50.654 als Ersatz des Affiliate Portal Template Kit installieren/aktivieren und danach genau eine Frontend-Seite prüfen. Erst nach realem Live-PASS weiterarbeiten.**

## Persistenter Zwischenstand
- `AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.654_HOBBY_DEPOT_FATAL_FIX.zip`;
- dauerhaft unter `/hobby rausch/WIP_1.50.653_WORKING/` gesichert;
- kein finales Release-Artefakt; Reparatur-/Prüfstand.
