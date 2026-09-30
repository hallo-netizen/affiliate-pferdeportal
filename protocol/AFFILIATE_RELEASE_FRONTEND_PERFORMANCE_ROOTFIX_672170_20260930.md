# Affiliate-Zentrale 6.72.170 – Frontend-Performance Rootfix nach 6.72.169 Regression

Datum: 2026-09-30

## Auslöser

Die reale PASSIVE_NO_FILTERS-Messung nach 6.72.169 zeigt:
- Pferdesättel: 11.479722 s -> 20.231837 s
- Paddockbau: 3.550648 s -> 4.753882 s
- Trensen: 9.964452 s -> 10.001292 s

6.72.169 senkte zwar den Speicherverbrauch deutlich, führte aber im eBay-Exact-GTIN-Fallback einen ungeeigneten Frontendpfad ein: wiederholte unindizierte `source_payload LIKE '%GTIN%'`-Scans.

## Ziel

Schneller als 6.72.169, ohne Rückkehr zum alten Vollkampagnen-Scan und ohne Funktions-/Qualitätsverlust.

## Rootfix

1. Kein `source_payload LIKE '%GTIN%'` im öffentlichen Frontend.
2. Exact-GTIN-Angebote:
   - idealo / Awin-OTTO weiter über vorhandenen rohen Exact-Index.
   - eBay Altbestand nur aus dem bereits seiten-/slotbezogen relevanten Kandidatenpool bestimmen.
   - eBay-Quellzeilen für diese kleine Kandidatenmenge einmal gebündelt laden und im Request cachen.
   - exakte GTIN danach lokal aus den bereits geladenen Quellzeilen prüfen.
3. Ergebnis des Exact-GTIN-Pools request-lokal nach Kontext + Slot + GTIN cachen.
4. Neue/erneuerte eBay-BUSINESS-Produkte tragen GTIN künftig direkt in Creative/Campaign-Daten, damit der generische Exact-Index sie ohne Fallback findet.
5. Keine Frontend-Schreibmigration; bestehender Altbestand bleibt lesbar und wird beim regulären Provider-Refresh natürlich angereichert.

## Harte Nicht-Änderungen

Ranking, Relevanz, PRIVATE/BUSINESS, Source/Policy/Route, Coverage, Quality, Health, Veto, Affiliate-Tracking, Providerstrategie, Design, Veröffentlichungsregeln und Wartungswege bleiben unverändert.

## Pflichtabnahme vor Installer

- Positiv lokal WordPress 7.1.2 + MariaDB: exakter GTIN-Treffer über idealo/Awin/eBay bleibt gleich.
- Negativ lokal: falsche GTIN und falscher Seitenkontext liefern keinen eBay-Falschtreffer.
- Performance lokal: 6.72.170 darf bei großem synthetischem eBay-Bestand keinen payload-LIKE-Scan ausführen und muss den eBay-Fallback auf die kontextrelevante Kandidatenmenge begrenzen.
- Wiederholter Aufruf derselben Karte muss aus Request-Cache kommen.
- Vollständige bestehende Provider-/Banner-/Ranking-/Housekeeping-/Importer-Gates PASS.
- Erst danach Installer.
