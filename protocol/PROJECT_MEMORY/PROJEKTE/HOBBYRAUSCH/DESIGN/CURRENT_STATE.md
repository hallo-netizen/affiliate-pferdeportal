# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-14
STATUS: **1.50.652 LETZTER BUILD / VISUAL FAIL / WIP 1.50.653 REAL / 65/65 HEROES + 65/65 KATEGORIEVORSCHAUEN + 75/328 KARTEN BELASTBAR / HERO-BLOCK ABGESCHLOSSEN / RELEASE-GATE FAIL / KEIN LIVE-PASS**

## Letzter paketierter Stand
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.652_HOBBY_DEPOT_HUB2_HERO_COMPACT_EXACT_SCENES_NOUPSCALE_LOCALPASS.zip`

SHA-256:
`c5c19f94b57c9dd95d88738f752e6e1ea5d880ea6d85ebc7bb31cfdd6b17234b`

1.50.652 bleibt der letzte paketierte Build und ist visuell nicht freigabefähig. Die reale WIP-Basis 1.50.653 ist der aktuelle Arbeitsstand.

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
- belastbare Vorbasis nach Duplikatkorrektur: **68/328**;
- neuer geprüfter Block ergänzt:
  - terraristik / reptilienhaltung
  - ameisen-insekten / kaeferzucht
  - wetter-umwelt / private-wetterstation
  - keramik-glas / keramikglasuren
  - schmuck / schmuckherstellung
  - pilze-kulturen / speisepilzzucht
  - audio-hifi / lautsprecherbau
- `astronomie / teleskop-astronomie` wurde im selben Prüflauf wieder verworfen, weil der reale 200×107-Crop dem Astronomie-Hero zu ähnlich war;
- aktuell **75/328 Karten belastbar aktiv**;
- **253 Karten offen**;
- alle aktiven Karten exakt **200×107**;
- 0 exakte Karten-Doppelungen innerhalb derselben Seite;
- 0 Hero↔Karte-Gleichquellen innerhalb derselben Seite;
- Nah-Duplikatcheck: **0 Treffer**;
- alle 75 aktiven Karten-Mappings verwenden `source=v150653`;
- 75/75 gemappte Dateien real vorhanden.

### Technische Prüfung
- **61/61 PHP-Dateien Syntax PASS**;
- Hero-Dateien: **65/65 korrekt 600×220**;
- Kategorievorschauen: **65/65 korrekt 200×107**;
- Hero-Mapping: **65/65 vorhanden und auf reale Dateien gebunden**;
- exakte Hero-Duplikate: **0**;
- exakte Kategorievorschau-Duplikate: **0**;
- Karten: 75/75 korrekt 200×107 und gegenüber dem vorigen 75-Karten-Checkpoint bytegleich;
- Karten-Mapping gegenüber dem vorigen 75-Karten-Checkpoint unverändert;
- JSON/Mapping PASS;
- keine semantischen Hero-/Kartenfallbacks;
- neues WIP-Arbeits-ZIP erfolgreich getestet: ZIP-Struktur PASS;
- kein neues Release-ZIP.

## Eingefroren
- Textinhalt aus 1.50.650;
- Grundaufteilung aus 1.50.650;
- Buch & Papier 1.50.645 als visuelle Referenz;
- Header, Navigation, Ebene 1, Taxonomie, Architektur und Monetarisierungsreihenfolge.

## Exakte offene Bildliste
`protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/DESIGN/MISSING_IMAGE_WORKLIST_1.50.653.json`

- **0 fehlende Heroes**;
- **253 fehlende Karten**;
- fehlend bleibt fehlend, solange kein fachlich eindeutiges Motiv existiert.

## EXAKT EINE NEXT ACTION
**Hero-Arbeit beendet. Als nächster eigener Arbeitsblock bleiben ausschließlich die 253 offenen Karten; keine weitere Hero-Arbeit nötig. Kein Release-ZIP vor vollständigem Render-/Regressionstest und Release-Gate PASS.**

## Persistenter Zwischenstand
- aktuelles Arbeits-ZIP: `WIP_1.50.653_WORKING_65HEROES_75CARDS_NOT_RELEASE.zip`;
- dauerhaft unter `/hobby rausch/WIP_1.50.653_WORKING/` gesichert;
- SHA-256: `97469ea1156a0dce66fccf3b6036a5bea79e7709050f078d60f899b0cde864dd`;
- kein Release-Artefakt, nur Arbeitscheckpoint.
