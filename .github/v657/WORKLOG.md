# Arbeitsprotokoll – V6.57 idealo Isolated Adapter Phase 1 – 27.08.2026

## Bindung
Priorität: MASTER > aktueller Source > belegte GitHub-Historie > Chat > Vermutung. Multi-Provider-Zielvertrag V1.0 bleibt bindend. eBay bleibt produktiv getrennt und unangetastet; Amazon folgt erst nach idealo.

## Reale iPN-Evidenz
- Adspace Pferde Atelier: `568313`.
- idealo DE Product Data Feed `2747` (Fashion, Sport, Outdoor).
- iPN UI zeigt systemgenerierten API-Key als aktiv und ohne Ablaufdatum.
- real heruntergeladener Feed: `productdata_2747.csv.gz`.
- 515.554 Produktzeilen, 22 Spalten, 0 strukturell fehlerhafte CSV-Zeilen.
- exakt relevante verifizierte Unterkategorien: Reitbekleidung 468, Reitstiefel 156, Reithelme 22, Pferdegerten 9 = 655.
- 653/655 mit GTIN/EAN; 130/655 mit ASIN.
- 655/655 Product-Deeplinks enthalten `!!TIME_STAMP!!`.

## Architekturentscheidung
Neue idealo-Logik wird als eigener Trait über die bereits vorhandenen Provider-Adapter-Hooks angebunden. Keine neue Monolith-Logik. Daten landen ausschließlich in der vorhandenen internen Provider-Prüfstufe (`network=idealo`). Der Import veröffentlicht nichts.

## Produktionsscope V6.57
Neu:
- `includes/trait-ppar-idealo.php`

Minimal geändert:
- `includes/trait-ppar-provider-registry.php`: idealo von prepared auf active, Fachseite + Credentials/Productfeed/Sync-Capabilities.
- `pferdeportal-affiliate-router.php`: Trait laden/verwenden, idealo-Option, Hook-Registrierung, Version 6.57.0.
- `readme.txt`: Version/Changelog.

Byteidentisch zu V6.56:
- eBay Providertrait
- eBay Run-Trait
- eBay Account-Deletion-Trait
- Output Objects
- Control Contract
- Creative Library
- frontend.css / frontend.js
- eBay-Katalog / Portalstruktur

## Phase-1-Funktionen
- API-Key, Adspace-ID und Feed-ID sicher speichern.
- optional die vom iPN selbst erzeugte Feed-Download-URL speichern; keine URL wird konstruiert oder geraten.
- `.csv` und `.csv.gz` als einmaligen realen Testfeed streamend einlesen.
- konfigurierbarer Unterkategorienfilter statt Pferde-Hardcoding im Parser.
- Remote-Feedpfad nur dann aktiv, wenn eine reale HTTPS-Feed-URL gespeichert wurde.
- kein Matching, keine öffentliche idealo-Ausgabe.

## Hardlocks
- kein Umbau des eBay-Runtimepfads.
- kein automatisches Veröffentlichen beim Import.
- kein eBay/idealo-Matching in Phase 1.
- keine Interpretation/Ersetzung von `!!TIME_STAMP!!` ohne belegte iPN-Regel.
- keine geratene API-Domain oder Feed-URL.

## Lokale Gates
- PHP-Lint: PASS.
- realer 515.554-Zeilen-GZIP-Feed vollständig gestreamt: PASS.
- 655 relevante Zeilen reproduzierbar: PASS.
- Fresh-Unpack Source-Parität: PASS.
- Installer ZIP-Test: PASS.
- geschützte eBay-/Frontend-Dateien byteidentisch: PASS.

## Artefakte
Installer SHA-256: `2fc86665ac0af1e901035c4eaa4f54ed0f2038d950117331c919729d66c5214c`
MASTER SHA-256: `1016c9a4fd41b1249f88ab0876f80010ceba651bb65cf49128adae5bedaef300`

## Live offen
- Installation V6.57.0 auf Pferde Atelier.
- API-Key nur im WordPress-Backend speichern; nicht in GitHub/Chat.
- realen Feed 2747 einmalig in die Prüfstufe importieren.
- erst danach Remote-URL/Tracking-Hardlock weiter bearbeiten.
