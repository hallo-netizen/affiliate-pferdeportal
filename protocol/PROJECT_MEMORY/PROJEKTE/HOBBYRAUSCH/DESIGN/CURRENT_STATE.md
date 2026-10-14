# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-14
STATUS: **SEITE WIEDER ERREICHBAR / ARCHITEKTUR + RUNTIME EINGEFROREN / HERO-ONLY 1.50.659 VERWORFEN / HERO-REPLACE-ONLY 1.50.660 LOKAL PASS / LIVE-PRÜFUNG OFFEN**

## Harte Sperre
Keine Änderungen an:
- Template-Kit-PHP;
- Routing;
- Templates;
- CSS;
- Mapping;
- Karten;
- Seitenstruktur;
- Architektur/System.

## Fehler 1.50.659
1.50.659 ist verworfen, weil es entgegen der Vorgabe zusätzlich den `heroes`-Block in `hub2-image-map.json` geändert hat.
Das war keine reine Bilddatei-Ersetzung.

## Aktueller Kandidat
`HOBBY_DEPOT_HERO_REPLACE_ONLY_1.50.660.zip`

SHA-256:
`bd1bbd485763cbf72b07d284c5ca81664401397704dc73e310d9c4807fc3c9af`

## Was 1.50.660 exakt macht
- liest nur die 65 aktuell vorhandenen Hero-Zielpfade aus dem laufenden 1.50.650-Mapping;
- überschreibt ausschließlich genau diese 65 bestehenden WebP-Dateien mit den neuen 600×220-Hero-Pixeln;
- Mapping bleibt byte-identisch;
- 0 Änderungen an Template-Kit-PHP;
- 0 Änderungen an Templates;
- 0 Änderungen an Routing;
- 0 Änderungen an CSS;
- 0 Änderungen an Karten;
- 0 Änderungen an Architektur.

## Lokale Prüfung
Pristine 1.50.650:
- DIFF_COUNT = 65;
- EXPECTED_TARGETS = 65;
- ONLY_EXPECTED = true;
- MAP_UNCHANGED = true;
- PHP_CHANGED = 0;
- 65/65 Hero-Kopien SHA-identisch zum Payload;
- Helper-PHP Syntax PASS;
- ZIP PASS.

Zusätzlich mit bereits angewendetem 1.50.659-Zustand simuliert:
- 1.50.659-Patch zuerst angewendet: PASS;
- danach 1.50.660 angewendet: PASS;
- aktuelles Mapping 65 eindeutige Zielpfade;
- 65/65 aktuell gemappte Zielbilder danach SHA-identisch zum neuen Payload.

## EXAKT EINE NEXT ACTION
**1.50.659 nicht weiterverwenden. 1.50.660 installieren/aktivieren; es ersetzt nur die 65 aktuell gemappten Hero-Dateien. Danach eine Hub2-Seite hart neu laden und visuell prüfen.**
