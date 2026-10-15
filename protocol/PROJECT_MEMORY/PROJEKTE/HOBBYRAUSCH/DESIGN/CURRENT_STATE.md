# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-15
STATUS: **1.50.650 GRUNDSTAND EINGEFROREN / 65/65 HERO-FOTOS AUS 1.50.660 WIEDERHERGESTELLT UND TECHNISCH PASS / 1.50.661–1.50.663 NICHT VERWENDEN**

## Aktueller belastbarer Stand
- Affiliate Portal Template Kit **1.50.650** bleibt der eingefrorene Grundstand.
- Der bereits fertiggestellte Hero-Bildsatz wurde aus **HOBBY_DEPOT_HERO_REPLACE_ONLY_1.50.660.zip** wiederhergestellt.
- Das Paket enthält **65/65** aktuell gemappte Hub2-Hero-Bilder.
- Alle 65 Bilder sind exakt **600×220 WEBP**.
- Payload-Slugs und das aktive 1.50.650-Hero-Mapping stimmen **65/65** überein.
- Keine exakten Bilddubletten im Payload.
- Lokale 1:1-Simulation gegen die echte 1.50.650-Basis: exakt **65 Bilddateien geändert**, **0** Dateien hinzugefügt, **0** entfernt, **0** unerwartete Änderungen.
- Hero-Mapping bleibt byte-identisch.

## Verbindliches Artefakt
`HOBBY_DEPOT_HERO_REPLACE_ONLY_1.50.660.zip`

SHA-256:
`bd1bbd485763cbf72b07d284c5ca81664401397704dc73e310d9c4807fc3c9af`

Technischer Nachweis:
`HERO_1.50.660_RECOVERY_VALIDATION_20261015.md`

## Harte Sperre
Nicht verwenden:
- 1.50.651–1.50.659 als Ersatz für diesen wiederhergestellten Bildstand;
- **1.50.661–1.50.663**;
- die spätere 7/30-/13-Referenz-Rekonstruktionsschiene als aktuelle Wahrheit;
- neue Bildgenerierung für bereits im 1.50.660-Paket vorhandene Heroes.

Nicht anfassen:
- Template-Kit-PHP;
- Routing;
- Templates;
- CSS;
- Mapping;
- Kartenlogik;
- Architektur/System.

## Rolle von 1.50.660
1.50.660 ist ein **reiner Hero-Bildersatz** auf Basis 1.50.650.
Der Installer prüft vor Austausch:
- aktives Template Kit exakt 1.50.650;
- Hero-Map exakt 65 Einträge;
- Payload exakt 65 Dateien;
- jede Payload-Datei exakt 600×220;
- jedes bestehende Ziel vorhanden;
- keine doppelten Zielpfade;
- Hashgleichheit nach Staging und Austausch.

Bei Fehler wird abgebrochen bzw. aus Backup zurückgerollt.

## EXAKT EINE NEXT ACTION
**1.50.660 als wiederhergestellten vollständigen 65-Hero-Bildstand verwenden. Keine weitere Bildgenerierung und keine 7/30-Rekonstruktion. Danach ausschließlich Live-Readback der sichtbaren Hero-Bilder gegen diesen Stand; nur bei einem konkret sichtbaren Einzelmotivfehler genau dieses eine Motiv anfassen.**
