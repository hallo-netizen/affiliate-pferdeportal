# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-16
STATUS: **1.50.650 GRUNDSTAND EINGEFROREN / 30ER-BILDSTAND ERHALTEN / HRD-SCOPE13 REPARATUR 13/13 LOCALPASS / ALLE ANDEREN KATEGORIEN GESPERRT**

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

## 30er-Neubild-Basis – erhalten, aber nicht mehr aktueller Installationskandidat
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

## HRD-SCOPE13 Reparatur
Verbindliche Sperre: ausschließlich 13 gemeldete Kategorien durften angefasst werden. Alle anderen Kategorien bleiben unverändert.

Ergebnis:
- 13/13 Kategorien repariert;
- vor Neugenerierung alte Bilder geprüft;
- **keine neue Bildgeneration notwendig**;
- 7 gute frühere Vollquellen wiederhergestellt;
- 2 gezielt auf bessere 1.50.625-Bilder zurückgesetzt;
- 4 gezielt auf bessere WIP-1.50.653-Bilder zurückgesetzt;
- keine Collage als Releasequelle;
- exakt 26 Bilddateien geändert;
- 0 sonstige Änderungen;
- 30er-Neubildbestand vollständig byte-identisch erhalten;
- Mapping byte-identisch;
- 55/55 PHP byte-identisch + Syntax PASS;
- ZIP-Roundtrip PASS.

Kandidat:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.650_HOBBY_DEPOT_HRD_SCOPE13_REPAIR_LOCALPASS.zip`
SHA-256:
`d32805e2747f9df25e722efc7242f4df820bd273f19db2e2b8b97e5b249e1bf4`

Nachweis:
`HRD_SCOPE13_IMAGE_REPAIR_20261016.md`

## HRD HARD RULE
**Nur die 13 Kategorien aus HRD_SCOPE13_IMAGE_REPAIR_20261016.md dürfen bei dieser Reparatur geändert werden. Alle anderen Kategorien FINGER WEG.**

## EXAKT EINE NEXT ACTION
**Den HRD-SCOPE13-Kandidaten installieren und danach Live-Readback ausschließlich der 13 reparierten Kategorien durchführen. Nur bei einem konkret sichtbaren Restfehler genau diese eine betroffene Kategorie ändern; alle übrigen Kategorien bleiben gesperrt.**
