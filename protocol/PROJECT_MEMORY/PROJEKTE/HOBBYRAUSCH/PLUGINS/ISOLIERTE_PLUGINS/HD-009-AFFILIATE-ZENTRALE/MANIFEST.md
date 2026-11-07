# HD009 – einziges aktuelles Affiliate-Plugin im Hobby-Depot-GitHub-Büro

**07.11.2026 · Hobby Depot Affiliate-Zentrale 0.1.17-dev · ein vollständiger Update-Kandidat.**
Noch **kein bestätigter WordPress-Live-Test**.

## Exakte aktuelle ZIP

- `CURRENT.zip` – **1.175.854 Bytes**
- SHA-256: `067a1b2532c2c2c476763269e80e4ccefacfdb073e55f02c182a2a85a43745ca`
- Git-Blob: `08cf7ede5d518064173c6a6da2c433faaa67d9d9`
- Unveränderter WordPress-Pluginordner: `affiliate-portal-router/`
- Unveränderte zentrale Architektur. **Kein zweites Plugin und keine zweite Kampagnenverwaltung.**

## CI-Vertrag und Einsatz

- **Eigenwerbung für Amazon:** Originales Hobby-Depot-Logo (aus HD003), Montserrat, warmes Beige, dunkle Schrift, petrolfarbener CTA, Kennzeichnung „Anzeige“.
- **Breiter Querbanner:** proportionaler 6:1-Banner, volle Breite des vorhandenen Contentbereichs; kein willkürlicher Beschnitt des gesamten Banners. Testseite: `https://hobby-depot.de/gestalten/malen-zeichnen/`.
- **Quadratbanner:** 1:1 für einzelne Hobbyregisterprofile (HD007) und Glossar-Einzelbeiträge (Desktop **und Mobil**), jeweils im bestehenden passenden Ausgabeplatz. Optional normale Beitragsplätze als breiter Banner.
- **Motive:** Es wird nur das zum jeweiligen Hobby passend vorhandene Bild verwendet. Direkte Originaldateien aus HD003 für „Malen & Zeichnen“ und „Modellbau“ unverändert integriert; HD007-Bildkarte für weitere Hobbyprofile aus tatsächlichem `canonical_name`, `registry_id`, `source`, `path`, einschließlich Ablehnung bekannter FAIL-/OPEN-Bildzuordnungen. Gibt es kein ausreichend passend freigegebenes Motiv, bleibt die Werbung leer.
- **Ziel:** Kontextbezogene Amazon-Suche nach Ausrüstung/Zubehör für das aktuelle Hobby mit der bereits im WordPress-Backend gespeicherten und geprüften `-21`-Trackingkennung. **Kein erfundenes Einzelprodukt, kein Preis und keine als Produktanzeige ausgegebene Mietwerbung.**
- **Native Auswahl hat Vorrang:** Bereits freigegebene, fachlich/technisch passende Amazon-/idealo-Kampagnen, Kategorien, Elternpfade, Bannerformat und manuelle Vetos bleiben unangetastet. Eigenbanner nur auf tatsächlich freien Plätzen, keine generische Anzeige für jedes Hobby.
- **Getrennt:** Die Original-Modellflugzeug-Grafik „Hier könnte Ihre Werbung stehen“ ist ausschließlich Mietwerbung im unveränderten HD003-Designplugin und **nicht** Teil der Affiliate-Anzeigen.

## Prüfnachweise

- Genau **24/24 PHP-Dateien** syntaxgeprüft, ZIP-CRC PASS.
- **11 echte PHP Positiv-/Negativfälle** zu Querbanner, Quadratformat, echtem Hobbybild, korrektem Amazon-Tracking und Ausgabesperren PASS.
- Original-Logo und zwei Original-Fotos mit vorhandener HD003-ZIP bitidentisch verglichen.
- Original-HD007-Register-Schema und Bildfreigaben direkt aus **HD007 CURRENT.zip** gelesen; `canonical_name`-/`source`-/`path`-Korrekturen vor Freigabe mit PHP-Regressionsprüfung bestätigt.
- Reale Chromium-Vorschau mit CSS und Originalbildern für breite und quadratische Banner PASS; `EVIDENCE/HD009_0117_BANNER_WIDE_CI_PREVIEW.jpg`, `EVIDENCE/HD009_0117_BANNER_SQUARE_CI_PREVIEW.jpg`.
- Endgültiger Prüfbericht: `EVIDENCE/HD009_0117_CI_SINGLE_RELEASE_REPORT.txt` mit exakt passender ZIP-Größe und Prüfsumme.
- **Grenze:** Eine Simulation, syntaktische Prüfung oder Browser-Vorschau ist keine Bestätigung der installierten Live-Version oder einer echten Amazon-Provision. Noch kein Live-PASS.

## Nächster genau EINER Schritt

Bestehendes Hobby-Depot-Affiliate-Plugin im WordPress-Backend **einmalig** mit dieser einzigen ZIP ersetzen, dann Querseite `/gestalten/malen-zeichnen/` und ein tatsächlich veröffentlichtes Hobbyregisterprofil, zum Beispiel `/hobbyregister/airbrush-modellbau/` (im HD007-Master belegt), auf korrekte thematische Banner, unverzerrte Formate, echte Ziele und fehlende Doppelungen prüfen. Kein weiteres Plugin und kein manueller Bannerimport.
