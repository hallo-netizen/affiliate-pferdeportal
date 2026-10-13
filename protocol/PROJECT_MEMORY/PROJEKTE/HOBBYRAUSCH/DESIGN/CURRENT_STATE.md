# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-13
STATUS: **1.50.652 LETZTER BUILD / VISUAL FAIL / WIP 1.50.653 REAL REKONSTRUIERT / 59/65 HEROES + 59 KATEGORIEVORSCHAUEN + 68/328 KARTEN BELASTBAR / RELEASE-GATE FAIL / KEIN LIVE-PASS**

## Letzter paketierter Stand
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.652_HOBBY_DEPOT_HUB2_HERO_COMPACT_EXACT_SCENES_NOUPSCALE_LOCALPASS.zip`

SHA-256:
`c5c19f94b57c9dd95d88738f752e6e1ea5d880ea6d85ebc7bb31cfdd6b17234b`

1.50.652 bleibt der letzte paketierte Build und ist visuell nicht freigabefähig. Die reale WIP-Basis 1.50.653 ist aus der vorhandenen 1.50.651-Arbeitskopie plus den autoritativen Bild-Audits rekonstruiert und reproduzierbar.

## Aktueller WIP 1.50.653

### Hero
- 59/65 Hero-Motive aktiv und real vorhanden;
- alle exakt 600×220;
- 59 daraus abgeleitete Kategorievorschauen exakt 200×107;
- 6 Heroes fehlen bewusst:
  - rollen-balance
  - wurf-ziel
  - team-wettkampf
  - geschick-tricks
  - werbung-design
  - werkzeuge-geraete
- keine falschen Fallbacks.

### Karten
- ursprünglicher Karten-Audit: 46 PASS / 282 ersetzen;
- nach zusätzlicher Seiten-Duplikatprüfung wurden 13 alte PASS-Karten erkannt, die dieselbe Ausgangsquelle wie ihr Hero verwendeten;
- 11 davon wurden auf vorhandene, fachlich passende und eigenständige Bildquellen umgestellt;
- 2 wurden mangels sauberer Alternative entfernt und bleiben bewusst offen:
  - wetter-umwelt / gewittertracking
  - messen-analysieren / bodenanalyse
- `3d-druck` und `wandern` wurden technisch korrigiert: Quellenkennung und Assetpfad sind rendererkompatibel;
- aktuell **68/328 Karten belastbar aktiv**;
- **260 Karten offen**;
- alle aktiven Karten exakt 200×107;
- 0 exakte Karten-Doppelungen innerhalb derselben Seite;
- 0 Hero↔Karte-Gleichquellen innerhalb derselben Seite;
- zusätzlicher Nah-Duplikatcheck: 0 Treffer;
- alle 68 aktiven Karten-Mappings verwenden `source=v150653`;
- 68/68 gemappte Dateien real vorhanden.

### Technische Prüfung
- **61/61 PHP-Dateien Syntax PASS**;
- Hero-Dateien: 59/59 korrekt 600×220;
- Kategorievorschauen: 59/59 korrekt 200×107;
- Karten: 68/68 korrekt 200×107;
- JSON/Mapping PASS;
- keine semantischen Hero-/Kartenfallbacks;
- reproduzierbarer Neuaufbau ergibt exakt wieder denselben Stand: **59 Heroes / 68 Karten**;
- kein neues Release-ZIP.

## Eingefroren
- Textinhalt aus 1.50.650;
- Grundaufteilung aus 1.50.650;
- Buch & Papier 1.50.645 als visuelle Referenz;
- Header, Navigation, Ebene 1, Taxonomie, Architektur und Monetarisierungsreihenfolge.

## Exakte offene Bildliste
`protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/DESIGN/MISSING_IMAGE_WORKLIST_1.50.653.json`

- 6 fehlende Heroes;
- 260 fehlende Karten;
- fehlend bleibt fehlend, solange kein fachlich eindeutiges Motiv existiert.

## EXAKT EINE NEXT ACTION
**Die 6 fehlenden Heroes nur mit fachlich eindeutigen neuen Motiven schließen. Parallel die 260 offenen Karten ausschließlich blockweise mit eindeutig passenden, eigenständigen Bildern ergänzen. Keine Fallbacks, kein falsches Auffüllen, kein Release-ZIP vor vollständigem Render-/Regressionstest und Release-Gate PASS.**
