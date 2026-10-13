# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-13
STATUS: **1.50.652 LETZTER BUILD / VISUAL FAIL / WIP 1.50.653 HERO+KARTEN-AUDIT KOMPLETT / KEIN LIVE-PASS**

## Letzter autoritativer Build
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.652_HOBBY_DEPOT_HUB2_HERO_COMPACT_EXACT_SCENES_NOUPSCALE_LOCALPASS.zip`

SHA-256:
`c5c19f94b57c9dd95d88738f752e6e1ea5d880ea6d85ebc7bb31cfdd6b17234b`

1.50.652 bleibt der letzte paketierte Stand. Technisch lokal PASS, visuell nicht freigabefähig.

## Gesicherter WIP 1.50.653

Hero-Audit:
`protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/DESIGN/HERO_AUDIT_20261013.md`

Karten-Audit:
`protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/DESIGN/CARD_AUDIT_20261013.md`

### Hero
- 65/65 manuell visuell geprüft;
- 51 PASS;
- 14 MISSING/ERSETZEN;
- 51 PASS-Heroes lokal exakt 600×220 vorbereitet, ohne Hochskalierung;
- kein semantischer Hero-Fallback.

### Unterkategoriekarten
- 328/328 manuell mit tatsächlichem Mapping visuell geprüft;
- 82 PASS;
- 246 MISSING/ERSETZEN;
- nur die 82 eindeutig passenden Motive bleiben im WIP aktiv;
- kein Featured-Image-Fallback;
- kein Welt-Pool-Fallback;
- kein Icon-Fallback;
- fehlendes Bild bleibt im WIP sichtbar als `Bild fehlt` statt fachlich falsch aufgefüllt.

### Lokaler technischer Stand WIP 1.50.653
- 61/61 PHP-Dateien Syntax PASS;
- 82 aktive Kartenassets: Datei vorhanden / Mindestgröße PASS;
- 51 aktive Heroassets: exakt 600×220 PASS;
- Textinhalt + Grundaufteilung aus 1.50.650 bleiben eingefroren;
- Buch & Papier 1.50.645 bleibt visuelle Referenz;
- Header/Navigation/Ebene 1/Taxonomie/Architektur unverändert;
- noch kein ZIP und kein Release.

## Fehlbestand
- 14 Hero-Motive gezielt neu erstellen/ersetzen;
- 246 Kartenmotive gezielt neu erstellen/ersetzen.

## EXAKT EINE NEXT ACTION
**Fehlende 14 Hero- und 246 Kartenmotive gezielt fachlich passend neu erstellen/ersetzen. Danach komplette reale Render-Simulation Desktop/Tablet/Mobil + Regression. Erst danach neuen Kandidaten paketieren.**
