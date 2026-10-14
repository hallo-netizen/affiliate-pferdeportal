# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-14
STATUS: **1.50.652 LETZTER BUILD / VISUAL FAIL / WIP 1.50.653 REAL REKONSTRUIERT / 59/65 HEROES + 59 KATEGORIEVORSCHAUEN + 75/328 KARTEN BELASTBAR / RELEASE-GATE FAIL / KEIN LIVE-PASS**

## Letzter paketierter Stand
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.652_HOBBY_DEPOT_HUB2_HERO_COMPACT_EXACT_SCENES_NOUPSCALE_LOCALPASS.zip`

SHA-256:
`c5c19f94b57c9dd95d88738f752e6e1ea5d880ea6d85ebc7bb31cfdd6b17234b`

1.50.652 bleibt der letzte paketierte Build und ist visuell nicht freigabefähig. Die reale WIP-Basis 1.50.653 ist aus der vorhandenen 1.50.651-Arbeitskopie plus den autoritativen Bild-Audits rekonstruiert und reproduzierbar.

## Aktueller WIP 1.50.653

### Hero
- **59/65** Hero-Motive aktiv;
- alle exakt **600×220**;
- **59/65** daraus abgeleitete Kategorievorschauen exakt **200×107**;
- 6 Heroes fehlen bewusst:
  - rollen-balance
  - wurf-ziel
  - team-wettkampf
  - geschick-tricks
  - werbung-design
  - werkzeuge-geraete
- keine falschen Fallbacks.

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
- Hero-Dateien: 59/59 korrekt 600×220;
- Kategorievorschauen: 59/59 korrekt 200×107;
- Karten: 75/75 korrekt 200×107;
- JSON/Mapping PASS;
- keine semantischen Hero-/Kartenfallbacks;
- aktiver WIP lokal als echter 1.50.653-Assetbaum + versionierte Profil-/Templatebindung rekonstruiert;
- kein neues Release-ZIP.

## Eingefroren
- Textinhalt aus 1.50.650;
- Grundaufteilung aus 1.50.650;
- Buch & Papier 1.50.645 als visuelle Referenz;
- Header, Navigation, Ebene 1, Taxonomie, Architektur und Monetarisierungsreihenfolge.

## Exakte offene Bildliste
`protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/DESIGN/MISSING_IMAGE_WORKLIST_1.50.653.json`

- 6 fehlende Heroes;
- 253 fehlende Karten;
- fehlend bleibt fehlend, solange kein fachlich eindeutiges Motiv existiert.

## EXAKT EINE NEXT ACTION
**Die 6 fehlenden Heroes nur mit fachlich eindeutigen neuen Motiven schließen. Parallel die 253 offenen Karten ausschließlich blockweise mit eindeutig passenden, eigenständigen Bildern ergänzen. Keine Fallbacks, kein falsches Auffüllen, kein Release-ZIP vor vollständigem Render-/Regressionstest und Release-Gate PASS.**

## Persistenter Zwischenstand
- echtes Arbeits-ZIP: `WIP_1.50.653_WORKING_75CARDS_NOT_RELEASE.zip`;
- dauerhaft unter `/hobby rausch/WIP_1.50.653_WORKING/` gesichert;
- SHA-256: `339eae7e58923324e56ada05df452c69212a788f21ac0ccca45934a74c4de889`;
- kein Release-Artefakt, nur Arbeitscheckpoint.
