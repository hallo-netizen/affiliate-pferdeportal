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

## Reparaturkandidat 1.50.664 – Menü / Hauptweltkopf / Hero→Preview
Auf Basis des belastbaren 1.50.650-HRD-SCOPE13-Standes wurde ein eng begrenzter neuer Kandidat gebaut:

`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.664_HOBBY_DEPOT_MENU_HUB1_PREVIEW_LOCALPASS.zip`

SHA-256:
`73dfdc40792b1d550aaff6343aab9e9a4ca713988e0aa0c1957825b42ed4e2f9`

Geändert:
- Mega-Menü: gemeinsame sichtbare Zahl aus kleinstem Direktbestand; aktuell 5; größere Welten danach `Mehr Kategorien`; genau eine zusätzliche Orientierungsebene kompakt sichtbar;
- Hauptwelt-Hero/Textkopf: Desktop Text/Bild nebeneinander; <=1100 px sauber gestapelt; Mobil kompakt;
- 65/65 Kategorievorschauen neu direkt aus dem jeweils aktuellen Hub2-Hero abgeleitet.

Nicht geändert:
- Kategorienstruktur;
- Hero-Bilder selbst;
- Hub2-Bildmapping;
- redaktionelle Texte;
- Affiliate-/Routing-/Kartenlogik außerhalb dieses Darstellungsdeltas.

Local QA:
- Ausgang 981 Dateien → Kandidat 984 Dateien;
- 65 Preview-WEBP geändert;
- 0 Hero-WEBP geändert;
- Hauptplugin-Datei geändert;
- 3 neue versionsgebundene PHP-Dateien;
- PHP-Syntax 58/58 PASS;
- 65/65 Previews exakt 200×107;
- Hero→Preview Bildkorrelation min. 0,988 / Ø 0,996;
- Mega-Menü Desktop/Tablet: 8/8 gleiche Grundhöhe mit 5 sichtbaren Gruppen;
- ZIP-Integrität und Roundtrip PASS.

Kein Live-PASS.

## EXAKT EINE NEXT ACTION
**Kandidaten 1.50.664 installieren und live genau diese drei Punkte prüfen: Mega-Menü, Hauptwelt-Hero/Textkopf über Desktop/Tablet/Mobil sowie Hero→Kategorievorschau. Danach nächste Designebene festlegen.**
