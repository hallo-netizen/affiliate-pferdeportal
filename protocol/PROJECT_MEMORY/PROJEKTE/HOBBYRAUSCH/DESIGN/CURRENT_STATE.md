# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-16
STATUS: **1.50.650 GRUNDSTAND EINGEFROREN / 30/30 NEUE EINZELQUELLEN VISUAL PASS / IMAGE-ONLY-KANDIDAT TECHNISCH PASS / 1.50.660–1.50.663 NICHT VERWENDEN**

## Aktueller belastbarer Stand
- Affiliate Portal Template Kit **1.50.650** bleibt der eingefrorene Grundstand.
- Die 30 zuvor verworfenen Kategorien sind nach dem neuen Einzelquellen-Konzept jetzt **30/30 vollständig**.
- Für jede der 30 Kategorien existiert genau eine eigenständige neue Quelle.
- Alle 30 Quellen wurden als Vollbild sowie im realen Hero-Crop **600×320** und Preview-Crop **200×107** visuell geprüft.
- Ergebnis: **30/30 VISUAL PASS**.
- keine Collage-/Rasterquelle im Release;
- keine exakten Bilddubletten;
- Kollisionspaare fachlich getrennt;
- kein Upscaling.

## Finaler Image-only-Kandidat
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.650_HOBBY_DEPOT_NEW_IMAGES_30_VISUALPASS.zip`

SHA-256:
`cbc9789925660ada90a32e1d9726c4b6086c9d8308a8d097009573afab66ddc8`

Persistiert:
`/hobby rausch/releases/AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.650_HOBBY_DEPOT_NEW_IMAGES_30_VISUALPASS.zip`

Zusätzlich gesichert:
`/hobby rausch/releases/HOBBY_DEPOT_NEW_IMAGES_30_STAGE_FINAL.zip`
SHA-256:
`12d50d3f9bfc7e62b4f7f04a140c3e07e8e5d7dfdd49e1974187535acd788545`

## Lokale 1:1-Simulation auf echter 1.50.650-Basis
PASS:
- Dateien vorher/nachher: **981 / 981**;
- exakt **60** Bilddateien geändert;
- **0** Dateien hinzugefügt;
- **0** Dateien entfernt;
- **0** unerwartete Änderungen;
- 30 Heroes exakt **600×320**;
- 30 Previews exakt **200×107**;
- `hub2-image-map.json` byte-identisch;
- **55/55 PHP-Dateien byte-identisch**;
- **55/55 PHP-Syntax PASS**;
- ZIP-Roundtrip PASS;
- Negativsimulation fehlendes Ziel erkannt;
- Negativsimulation Mappingänderung erkannt.

Nachweis:
`NEW_CONCEPT_IMAGE_FINAL_QA_30OF30_20261016.md`

## Harte Abgrenzung
Nicht verwenden:
- 1.50.660;
- 1.50.661;
- 1.50.662;
- 1.50.663;
- die verworfene Collage-/Raster-Generierung.

Nicht geändert:
- PHP;
- Routing;
- Templates;
- CSS;
- Mapping;
- Kartenlogik;
- Architektur/System.

## Release-Einordnung
Der oben genannte ZIP ist für den **30-Kategorien-Image-only-Austausch auf 1.50.650** visuell und technisch PASS.
Das ist keine Aussage, dass sonstige unabhängige globale Karten-/Design-Backlogs abgeschlossen sind.

## EXAKT EINE NEXT ACTION
**Image-only-Kandidat 1.50.650 mit den 30 neuen Bildpaaren installieren und danach Live-Readback der 30 betroffenen Kategorien gegen den lokal geprüften Stand durchführen.**
