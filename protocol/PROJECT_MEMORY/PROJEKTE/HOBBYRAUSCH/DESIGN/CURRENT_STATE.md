# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-13
STATUS: **1.50.652 LETZTER BUILD / VISUAL FAIL / WIP 1.50.653 REAL REKONSTRUIERT / 59/65 HEROES + 59 KATEGORIEVORSCHAUEN + 71/328 KARTEN LOKAL EINGEBAUT / RELEASE-GATE FAIL / KEIN LIVE-PASS**

## Letzter paketierter Stand
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.652_HOBBY_DEPOT_HUB2_HERO_COMPACT_EXACT_SCENES_NOUPSCALE_LOCALPASS.zip`

SHA-256:
`c5c19f94b57c9dd95d88738f752e6e1ea5d880ea6d85ebc7bb31cfdd6b17234b`

1.50.652 bleibt laut autoritativem Altstand der letzte paketierte Build und ist visuell nicht freigabefähig. Im aktuell zugänglichen Library-Bestand wurde das 1.50.652-ZIP nicht gefunden; die reale rekonstruierbare Arbeitsbasis ist das vorhandene 1.50.651-ZIP plus die autoritativen 1.50.652/1.50.653-Audits.

## Autoritative Audits

Hero-Audit:
`protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/DESIGN/HERO_AUDIT_20261013.md`

Karten-Audit:
`protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/DESIGN/CARD_AUDIT_20261013.md`

Harte Freigabesperre:
`protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/DESIGN/RELEASE_GATE_20261013.md`

Audit-Basis:
- Hero: **65/65 geprüft; 50 PASS; 15 MISSING/ERSETZEN**;
- Karten: **328/328 geprüft; 46 PASS; 282 MISSING/ERSETZEN**;
- reale Zielcrops: Hero 600×220, Karte 200×107.

## Korrigierter realer WIP 1.50.653

### Hero
- die 50 auditbestätigten Hero-Motive wurden aus der realen Arbeitsbasis übernommen und neu exakt auf **600×220** erzeugt;
- **9/15** tatsächlich fehlende Hero-Motive wurden durch neue fachlich passende Quellen ersetzt:
  - druck-foto
  - oberflaeche-deko
  - genuss
  - metall
  - schmuck
  - naturmaterial
  - funk
  - smart-home
  - papier-dokumente
- diese 9 neuen finalen 600×220-Crops wurden visuell geprüft;
- damit aktuell **59/65 Hero-Motive aktiv/verfügbar**;
- **6 Hero-Motive fehlen weiterhin bewusst**:
  - rollen-balance
  - wurf-ziel
  - team-wettkampf
  - geschick-tricks
  - werbung-design
  - werkzeuge-geraete
- vorhandene lokale Altvarianten dieser sechs Kategorien wurden im echten 600×220-Crop geprüft und als fachlich ungeeignet verworfen;
- sechs zusätzlich erzeugte, aber nicht zur tatsächlichen MISSING-Liste gehörende Quellen ersetzen keine bestehenden Hero-PASS-Zuordnungen.

### Kategorievorschauen
- verbindliche Regel umgesetzt: **Kategorievorschau und Hub2-Hero stammen aus derselben Bildquelle**;
- aus jedem vorhandenen Hero wird eine eigene Vorschau **200×107** abgeleitet;
- aktuell **59/65 Kategorievorschauen** vorhanden;
- dieselben sechs Kategorien wie bei Hero bleiben bewusst ohne falsches Ersatzbild.

### Karten
- 46 auditbestätigte PASS-Karten fachlich übernommen;
- 17 echte neue Karten-Ersatzkandidaten aus dem ersten neuen Kartenblock eingebaut;
- drei redundant erzeugte Quellen Batik, Origami und Lettering werden nicht verwendet, weil die bestehenden Zuordnungen bereits auditbestätigt PASS sind;
- zusätzlich acht vorhandene/neue Quellen nach sichtbarer 200×107-Prüfung fachlich exakt als Karten genutzt:
  - robotik-automation / robotik
  - mechanik-uhren / uhren-reparieren
  - essbare-pflanzen / gemueseanbau
  - ameisen-insekten / ameisenhaltung
  - audio-hifi / plattenspieler-restaurieren
  - digitale-fertigung / 3d-druck
  - outdoor / wandern
  - papier-dokumente / historische-postkarten
- ein danach geprüfter 10er-Kandidatenblock wurde bis auf `historische-postkarten` wieder verworfen, weil die übrigen Motive zu ähnlich, zu eng oder nicht eindeutig genug waren;
- **3d-druck** und **wandern** wurden zusätzlich technisch korrigiert: aktive Quellenkennung jetzt exakt `v150653`, Pfade normalisiert; beide werden vom Renderer tatsächlich akzeptiert;
- aktuell **71/328 Karten** im WIP gemappt;
- **257 Karten** bleiben bewusst ohne Bild;
- alle aktiven Kartenassets sind exakt **200×107**.

### Technische Prüfung des rekonstruierten WIP
- **61/61 PHP-Dateien Syntax PASS**;
- Hero-Dateien: **59**, alle exakt 600×220;
- Kategorievorschauen: **59**, alle exakt 200×107;
- Karten: **71**, alle exakt 200×107;
- alle **71/71 aktiven Karten-Mappings** verwenden die vom Renderer akzeptierte Quellenkennung `v150653`;
- **71/71 gemappte Kartendateien real vorhanden**;
- reproduzierbarer Neuaufbau aus der Arbeitsbasis ergibt semantisch identisch wieder **59 Heroes / 71 Karten**;
- JSON/Mapping: PASS;
- kein semantischer Hero-Fallback im aktiven Hub2-Hero-Pfad;
- kein Featured-Image-Fallback im aktiven Hub2-Kartenpfad;
- kein Welt-Pool-/Icon-/v150617-Fallback im aktiven Hub2-Kartenpfad;
- fehlend bleibt fehlend;
- noch kein neues Release-ZIP.

## Eingefroren
- Textinhalt aus 1.50.650;
- Grundaufteilung aus 1.50.650;
- Buch & Papier 1.50.645 als visuelle Referenz;
- Header, Navigation, Ebene 1, Taxonomie, Architektur und Monetarisierungsreihenfolge.

## Exakte offene Bildliste
`protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/DESIGN/MISSING_IMAGE_WORKLIST_1.50.653.json`

- 6 fehlende Heroes;
- 257 fehlende Karten;
- keine Ersatz-/Fallback-Zuordnung ohne fachlich eindeutiges Motiv.

## EXAKT EINE NEXT ACTION
**Die sechs noch fehlenden Hero-Motive fachlich passend beschaffen/erstellen und als 600×220 plus daraus abgeleitete 200×107-Kategorievorschau einbauen. Parallel nur bereits vorhandene fachlich eindeutige Quellen für die 257 offenen Karten weiterverwenden; kein falsches Ersatzbild, kein Fallback und kein Release-ZIP, solange das Release-Gate FAIL ist.**
