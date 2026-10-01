# Affiliate-Zentrale 6.72.173 – Dynamic eBay Portal Catalog Validation – Local Gate

Datum: 2026-10-01
Status: TARGETED LOCAL POSITIVE/NEGATIVE/PERFORMANCE PASS – FULL RELEASE GATE OPEN

## Ausgangsbasis
- frischer Branch-HEAD vor Source-Write: `00a204d3d60c60609f13cd6f4cefee142ec799c4`
- Basis: 6.72.172
- Basis-Source-Manifest: `286fcedf2e7fa1eca441abb52d46254bf39f0d0fd6c63daa81f032d8e605e33c`
- Performancebasis 6.72.171 bleibt ausdrücklich erhalten.
- 6.72.172 Housekeeping/Idealo-Temp-Fix bleibt ausdrücklich erhalten.

## Belegter Fehler
Der reale Katalog enthält 334 product_pages / 1149 article_categories bei 334 product_targets / 1149 article_targets.
Der alte Validator erwartete historisch fest 329/1124 und blockierte deshalb den aktuellen, source_sha256-gebundenen Katalog.

## KISS-Fix
Nur der Katalog-Integritätsblock in `includes/trait-ppar-ebay.php` wurde fachlich geändert.
- keine zweite Portalstruktur wird geladen oder geparst;
- vorhandener source_sha256-Abgleich bleibt unverändert;
- statt historischer Gesamtzahlen werden die vorhandenen Counts gegen die tatsächlich mitgelieferten Arrays geprüft;
- leere Kernarrays bleiben fail-closed;
- bestehende Produkt-/Artikel-/Bucket-/Content-Policy-Validierungen bleiben unverändert.

Zusätzlich nur Versionsmetadaten:
- `pferdeportal-affiliate-router.php`: 6.72.172 -> 6.72.173 (Header + Runtime-Konstante)
- `readme.txt`: neue 6.72.173-Zeile

## Lokale Positiv-/Negativsimulation (PHP)
Aktuelle reale Count-Topologie:
- alter Validator: FAIL
- neuer Validator: PASS

Negativfälle neuer Validator:
- product_pages-Metadatum 333 bei 334 product_targets: FAIL
- article_targets um 1 verkürzt: FAIL
- main_hubs-Metadatum 9 bei 8 search_rules: FAIL
- business_routable_concepts 379 statt 380: FAIL

## Performance-Mikromessung
PHP, 200.000 Validator-Aufrufe auf synthetischer Topologie mit denselben Arraygrößen:
- neuer Validator gesamt: 134 ms
- ca. 0,67 µs pro Aufruf

Der Fix fügt keine Datei-, DB-, Netzwerk-, Taxonomie- oder Portalstruktur-Abfrage hinzu. Er verwendet nur `count()` auf bereits geladenen Arrays innerhalb des bestehenden statischen Katalogpfads. Keine 6.72.171-Performancefunktion wurde ersetzt.

## Source-Identität
- trait-ppar-ebay.php SHA-256: `af9f8f1cfbb17f3794d65e5b53e62e329c7755f1162dc4794db1abfaf84701ce`
- pferdeportal-affiliate-router.php SHA-256: `68fd0cdd512cc24120ac0ec39390b38820e633bf618f752a84b046b883657ca5`
- readme.txt SHA-256: `c2745e0057ba338681be8d0c13503474d3deeb2eff0ba19037ad9f5084d1b6c6`
- CURRENT_SOURCE_SHA256 SHA-256: `e9c760bec991257fa99cc500e1dd305a5389de262baa714c1547ef036ccd821d`

## Offen
Kompletter gebundener Release-Gate-Zyklus + WordPress/MariaDB/Frontend-Regression. Kein Installer vor diesem Gate.


## CI-Readback auf aktuellem 6.72.173-Head

GitHub-Head nach Manifest-/Readme-Korrektur:
`b9c30106607d9b381f3ab6b2f6a2b46531b806fa`

Automatisch gestartete Alt-Workflows:
- Run 36866837262: Governance PASS, Source PASS, Tree PASS, Start PASS; danach Abbruch ausschließlich am fest codierten `grep Version: 6.72.171`.
- Run 36866837152: Source PASS; danach Abbruch ausschließlich am fest codierten `grep Version: 6.72.170`.

Damit ist belegt:
- aktuelles 6.72.173-Manifest ist vom Release-Guard konsistent lesbar;
- kein Source-/Governance-Fehler wurde durch den Fix erzeugt;
- die vorhandenen alten Workflows sind als 6.72.173-Full-Gate nicht verwendbar, weil ihre Versionsnummern hart verdrahtet sind.

Die Workflowdateien werden **nicht** als Workaround geändert, weil `.github/workflows/` im Release-Scope gesperrt ist und kein CI-Umbau Teil dieses Funktionsfixes ist.
