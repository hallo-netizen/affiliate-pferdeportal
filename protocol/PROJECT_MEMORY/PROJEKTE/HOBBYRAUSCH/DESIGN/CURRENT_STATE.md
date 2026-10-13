# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-13
STATUS: **1.50.652 LETZTER BUILD / VISUAL FAIL / WIP 1.50.653 BILDAUDIT KOMPLETT / 15 HERO-ERSATZQUELLEN + 20 KARTEN-ERSATZQUELLEN DAUERHAFT GESICHERT / RELEASE-GATE FAIL / KEIN LIVE-PASS**

## Letzter paketierter Stand
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.652_HOBBY_DEPOT_HUB2_HERO_COMPACT_EXACT_SCENES_NOUPSCALE_LOCALPASS.zip`

SHA-256:
`c5c19f94b57c9dd95d88738f752e6e1ea5d880ea6d85ebc7bb31cfdd6b17234b`

1.50.652 bleibt der letzte paketierte Build und ist visuell nicht freigabefähig.

## Gesicherter WIP 1.50.653

Hero-Audit:
`protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/DESIGN/HERO_AUDIT_20261013.md`

Karten-Audit:
`protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/DESIGN/CARD_AUDIT_20261013.md`

Harte Freigabesperre:
`protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/DESIGN/RELEASE_GATE_20261013.md`

### Finaler visueller Befund des Audits
- Hero: **65/65 geprüft; 50 PASS; 15 MISSING/ERSETZEN**;
- Karten: **328/328 geprüft; 46 PASS; 282 MISSING/ERSETZEN**;
- beide Prüfungen umfassen ausdrücklich den realen sichtbaren Crop: Hero 600×220, Karte 200×107;
- ähnliche/doppelte oder nur allgemein passende Motive wurden wieder aus PASS entfernt.

### Ersatzfortschritt nach dem Audit
- **15/15 fehlende Hero-Ersatzquellen neu erstellt und dauerhaft gesichert**;
- gespeichert unter `/hobby rausch/WIP_1.50.653_WORKING/generated/heroes/`;
- diese 15 sind noch **KANDIDATEN**, bis der echte 600×220-Crop geprüft und eingebaut ist;
- **20 Karten-Ersatzquellen neu erstellt und dauerhaft gesichert**;
- gespeichert unter `/hobby rausch/WIP_1.50.653_WORKING/generated/cards/`;
- erster Kartenblock umfasst Druck & Fotografie vollständig, Textilgestaltung vollständig, Miniaturen bemalen, Kalligrafie, Lettering sowie Collage, Origami, Paper Quilling und Scrapbooking;
- diese 20 sind noch **KANDIDATEN**, bis der echte 200×107-Crop geprüft und eingebaut ist.

### WIP-Sicherungen
- nur bestätigte Bilder aktiv;
- Hero-Fallback entfernt;
- Featured-Image-Fallback für Hub2-Karten entfernt;
- Welt-Pool-Fallback entfernt;
- Icon-Fallback entfernt;
- fehlende Bilder bleiben im Arbeitsstand sichtbar fehlend;
- 61/61 PHP-Dateien Syntax PASS;
- aktive Assets vorhanden und ausreichend groß;
- Release-Gate aktuell **FAIL** und blockiert absichtlich jedes neue ZIP;
- noch kein neues ZIP / kein Release.

## Eingefroren
- Textinhalt aus 1.50.650;
- Grundaufteilung aus 1.50.650;
- Buch & Papier 1.50.645 als visuelle Referenz;
- Header, Navigation, Ebene 1, Taxonomie, Architektur und Monetarisierungsreihenfolge.

## Fehlbestand / noch nicht freigegeben
- Hero: **15 Ersatzquellen vorhanden, aber noch Crop-/Einbauprüfung offen**;
- Karten: **20 Ersatzquellen vorhanden, Crop-/Einbauprüfung offen; 262 weitere Kartenmotive noch zu erstellen**.

## EXAKT EINE NEXT ACTION
**Zuerst die 15 bereits gesicherten Hero-Ersatzquellen in den WIP einbauen und jeden echten 600×220-Crop prüfen. Danach die 20 bereits gesicherten Karten-Ersatzquellen als 200×107 prüfen/einbauen. Erst danach die verbleibenden 262 Kartenmotive blockweise erstellen. Kein neues ZIP, solange das Release-Gate FAIL ist.**
