# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-14
STATUS: **1.50.652 LETZTER BUILD / VISUAL FAIL / WIP 1.50.653 REAL / 65/65 HEROES + 65/65 KATEGORIEVORSCHAUEN + 75/328 KARTEN BELASTBAR / HERO-BLOCK ABGESCHLOSSEN / INSTALLPAKET KORRIGIERT / RELEASE-GATE FAIL / KEIN LIVE-PASS**

## Letzter paketierter Stand
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.652_HOBBY_DEPOT_HUB2_HERO_COMPACT_EXACT_SCENES_NOUPSCALE_LOCALPASS.zip`

SHA-256:
`c5c19f94b57c9dd95d88738f752e6e1ea5d880ea6d85ebc7bb31cfdd6b17234b`

1.50.652 bleibt der letzte freigegebene Paketstand. Die reale WIP-Basis 1.50.653 ist der aktuelle Arbeitsstand.

## Aktueller WIP 1.50.653

### Hero
- **65/65** Hero-Motive aktiv;
- alle exakt **600×220**;
- **65/65** Kategorievorschauen exakt **200×107**;
- die zuletzt offenen 6 Heroes sind geschlossen:
  - rollen-balance
  - wurf-ziel
  - team-wettkampf
  - geschick-tricks
  - werbung-design
  - werkzeuge-geraete
- Kategorievorschauen wurden jeweils aus derselben Hero-Bildquelle abgeleitet;
- keine falschen Fallbacks;
- Hero-Block vollständig abgeschlossen.

### Karten
- aktuell **75/328 Karten belastbar aktiv**;
- **253 Karten offen**;
- alle aktiven Karten exakt **200×107**;
- Kartenstand wurde beim Hero-Abschluss nicht verändert.

### Technische Prüfung
- korrigiertes Installationspaket basiert auf dem vollständigen 1.50.651-Pluginbaum;
- Plugin-Verzeichnis im ZIP wieder exakt `affiliate-portal-template-kit/`;
- **61/61 PHP-Dateien Syntax PASS**;
- Plugin-Version/Const auf **1.50.653**;
- Hero-Dateien: **65/65 korrekt 600×220**;
- Kategorievorschauen: **65/65 korrekt 200×107**;
- Karten: **75/75 korrekt 200×107**;
- ZIP-Integrität PASS;
- das zuvor ausgegebene `WIP_1.50.653_WORKING_65HEROES_75CARDS_NOT_RELEASE.zip` war als WordPress-Installationspaket falsch verpackt und darf nicht installiert werden.

## Eingefroren
- Textinhalt aus 1.50.650;
- Grundaufteilung aus 1.50.650;
- Buch & Papier 1.50.645 als visuelle Referenz;
- Header, Navigation, Ebene 1, Taxonomie, Architektur und Monetarisierungsreihenfolge.

## Exakte offene Bildliste
`protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/DESIGN/MISSING_IMAGE_WORKLIST_1.50.653.json`

- **0 fehlende Heroes**;
- **253 fehlende Karten**.

## EXAKT EINE NEXT ACTION
**Das korrigierte 1.50.653-Installationspaket in WordPress als Ersatz des bestehenden Affiliate Portal Template Kit installieren und aktivieren; danach Frontend-Sichtprüfung der Heroes/Kategorievorschauen.**

## Persistenter Zwischenstand
- korrigiertes Installationspaket: `AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.653_HOBBY_DEPOT_HERO_COMPLETE_FIXED_INSTALL.zip`;
- dauerhaft unter `/hobby rausch/WIP_1.50.653_WORKING/` gesichert;
- SHA-256: `c8b0a88d953279647bb61ea8f3801857bdefe7322039f617bf33d660fc70ff54`;
- kein finales Release-Artefakt; Installations-/Prüfstand.
