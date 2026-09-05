# DESIGN – CURRENT STATE

STAND: 2026-09-05

## Aktueller LIVE-Stand

**Pferde Atelier Design 1.50.472 / Contract V104**

Autoritative Live-Belege:
GitHub Branch:
`fix/category-intro-targeted-79-v150472-20260831`

Commit:
`f1e074b2e6dae9bec76ee8ab3f177080f69d2d41`

Live-Beleg:
`design-baseline/2026-08-31/v150472-category-intro-79/LIVE_PASS.md`

Dort ist Nutzerbestätigung nach Installation dokumentiert:
V1.50.472 / V104 / finaler 79/79-Kategorietext-Patch.

## Wichtige Abweichung zu main

Aktuelles `main` enthält weiterhin:
`pferde-template-kit_V1.50.421.php`
mit Pluginversion 1.50.421.

Daraus folgt:
**main ist für den aktuellen Pferde-Design-Live-Stand nicht die führende Release-Wahrheit.**

Nicht automatisch mergen oder main verändern.

## Übergebene Masterbasis

Vom Nutzer übergeben und vollständig archiviert:
- Plugin 1.50.469 / Contract V104;
- vollständiger Master 1.50.469 / Contract V104.

Diese beiden Dateien sind vollständige historische Basis für die spätere GitHub-Kette 1.50.470→1.50.472.

## Spätere GitHub-Kette

1.50.470:
gezielte 45 Kategorietextkorrekturen.

1.50.471:
gezielte Erweiterung auf 70.

1.50.472:
final 79/79 Audit-Scope.

MASTER_STATUS V1.50.472 sagt:
- vollständiger Master basiert ausdrücklich auf dem vollständigen 1.50.469/V104-Master;
- CURRENT_PLUGIN_SOURCE auf 1.50.472 aktualisiert;
- Installer 1.50.470/.471/.472 ergänzt;
- 388 Seitentexte + 1052 Leaftexte = 1440;
- allgemeiner und Pferde-V104-Vertrag byte-identisch zu 1.50.469;
- keine CSS/JS/Journal/Tabellen/Affiliate/Such/Breadcrumb/Bild/Karten/Publish-Änderung.

## QA V1.50.472

- Source ↔ finaler Installer: 498/498 PASS;
- 309/309 alte Seitentexte wertidentisch;
- 1052/1052 Leaftexte wertidentisch;
- 79/79 neue auditgebundene Seitentexte PASS;
- Search-Plugin-Quelle byte-identisch PASS;
- allgemeiner V104-Vertrag byte-identisch PASS;
- Pferde-V104-Vertrag byte-identisch PASS;
- Manifest-Readback/ZIP-Integrität PASS;
- LIVE PASS nach Nutzerbestätigung dokumentiert.

## Aktuelle Designregel

V104 bleibt unverändert.

1.50.469→1.50.472 ist ausschließlich Pferde-spezifische redaktionelle Kategorietext-/Loader-Entwicklung.

## Offene Archivlücke

Die exakten V1.50.472 Plugin-/Master-ZIPs liegen derzeit NICHT als vom Nutzer übergebene Rohdateien in der ChatGPT-Library.

Vorhanden:
- GitHub Status/QA/Live-Pass/Hashes;
- vollständige Rohbasis 1.50.469.

Daher:
aktueller Live-Stand bekannt, aber Roharchiv des finalen 1.50.472-Artefakts noch nicht vollständig.
