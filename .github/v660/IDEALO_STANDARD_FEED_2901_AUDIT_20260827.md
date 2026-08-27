# Idealo Standard Feed 2901 – Vollkatalog-Audit 27.08.2026

## Reale Nutzerdateien
- Feed 2747: 515554 Produktzeilen, 22 Spalten.
- Feed 2901: 2041826 Produktzeilen, 14 Spalten, komprimierte Nutzerdatei 247666988 Bytes.

## Harte Mengenprüfung
- Alle 515554 Produkt-IDs aus Feed 2747 kommen auch in Feed 2901 vor.
- Überdeckung 2747 -> 2901: 515554 / 515554 = 100 %.
- Konsequenz: Feed 2747 ist für die dauerhafte Idealo-Architektur redundant. Der Standardfeed 2901 ist der einzige notwendige Idealo-Basisfeed; keine Multi-Feed-Dublettenlogik erforderlich.

## Reale Hauptkategorien im Standardfeed 2901
- Haus & Garten: 613660
- Mode & Accessoires: 307871
- Elektroartikel: 294549
- Sport & Outdoor: 259261
- Drogerie & Gesundheit: 181992
- Auto & Motorrad: 162078
- Gaming & Spielen: 106562
- Tierbedarf: 51748
- Essen & Trinken: 35642
- Baby & Kind: 28433

## Eindeutig pferde-/portalrelevante Unterkategorien, Beispiele
- Pferdefutter: 1434
- Pferdedecken: 1192
- Sattelzubehör: 851
- Pferdepflege: 524
- Pferde-Beinschutz: 491
- Pferdesättel: 47
- Sattelaufbewahrung: 28
- Reitbekleidung: 497
- Reitstiefel: 159
- Reithelme: 30
- Pferdegerten: 14
- Weidezaungeräte: 214
- Weidezäune: 175
- Futtertröge & Tränken: 338
- Anhängerzubehör: 845
- Anhängerkupplungen & Elektrosätze: 1743

## Datenqualität
- 2041826 Zeilen gelesen.
- 9191 Zeilen ohne EAN und ohne gtins_product; damit tragen >99,5 % mindestens einen der beiden GTIN/EAN-Felder.
- 30 offensichtlich fehlgeparste/verschobene Zeilen in main_category wurden im Audit erkannt; sie dürfen in der Produktzuordnung nicht freigegeben werden.

## Wichtiger Schemaunterschied
Feed 2901 in der tatsächlich heruntergeladenen Konfiguration enthält: id, brand_name, product_title, image_url, product_deeplink, ean, asins_product, gtins_product, main_category, sub_category plus Energy-Label-Felder. Er enthält in dieser Konfiguration NICHT price, image_url_1 oder shop_name. Der Importer darf daher nicht mehr starr das 2747-Schema verlangen. Preis ist laut Zielvertrag optional; idealo wird als Bezugsquelle dargestellt.

## Architekturentscheidung / KEEP IT SIMPLE
1. Dauerhaft nur Feed 2901 als Idealo-Basisfeed.
2. Feed 2747 nicht zusätzlich produktiv pflegen.
3. Standardfeed streamend lesen; nie 2 Mio. Produkte vollständig in WordPress materialisieren.
4. Relevanz ausschließlich gegen den bereits verbindlichen Portal-/BUSINESS-Katalog (59 Hub-Familien / 311 freigegebene Produktkonzepte bzw. dessen aktuelle kanonische Katalogrepräsentation) prüfen.
5. Nur fachlich sicher gematchte Produkte mit belastbarer Produktidentität (GTIN/EAN) in einen kleinen Idealo-Bestand übernehmen; Rest sofort verwerfen.
6. Mehrdeutige Matches fail-closed/überspringen.
7. eBay bleibt unabhängig und darf von Idealo-Import/Fehlern nicht beeinflusst werden.
8. Getrennte Ausgabe und gemeinsame Karte bleiben wie im Multi-Provider-Zielvertrag vorgesehen; gemeinsame Karte nur bei exakter GTIN.

## Konsequenz für V6.60
Die bisherige feste 2747-Unterkategorienliste (Reithelme/Reitstiefel/Pferdegerten/Reitbekleidung) ist nur ein erfolgreicher Proof-of-Concept und nicht der Endzustand. Vor dem nächsten Installer muss der Idealo-Importer auf Feed 2901 + vollständigen Portal-Katalog umgestellt und lokal gegen den gesamten Workflow regressionsgeprüft werden.
