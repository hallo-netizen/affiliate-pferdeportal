# idealo Feed 2747 – Realprüfung 27.08.2026

Quelle: vom Nutzer direkt aus iPN geladene Datei `productdata_2747.csv.gz`.

## Datei
- gzip-komprimierte CSV
- Größe: 91.429.503 Bytes
- Datenzeilen: 515.554
- fehlerhafte CSV-Zeilen in der lokalen Vollprüfung: 0
- Hauptbereiche im Feed: `Mode & Accessoires` 283.608, `Sport & Outdoor` 231.946

## Reale Spalten
`id, product_title, product_description, price, image_url_1, product_deeplink, gtins_product, asins_product, ean, main_category, sub_category, brand_name, shop_name, image_url_2, image_url_3, shipping_costs, energy_class, top10_in_category, test_note, popularity_value, price_drop_percent, baseprice`

Damit sind die für den geplanten neutralen Produktkern entscheidenden Felder real vorhanden: idealo Produkt-ID, Titel, Preis, Bild, Tracking-/Deeplink, GTIN/EAN, ASIN soweit vorhanden, Kategorie, Marke und Shop.

## Reitsport-nahe Unterkategorien im Feed
Exakt im Feed vorhanden:
- Reitbekleidung: 468
- Reitstiefel: 156
- Reithelme: 22
- Pferdegerten: 9
- Summe dieser vier eindeutig relevanten Unterkategorien: 655 Produkte

Nicht als Reitsport werten: `Sattelstützen` ist Fahrradtechnik; `Wasseraufbereitung` ist kein Pferdeportal-Beleg.

## Feldabdeckung innerhalb der 655 eindeutig relevanten Produkte
- id: 655/655
- product_title: 655/655
- price: 655/655
- image_url_1: 655/655
- product_deeplink: 655/655
- brand_name: 655/655
- shop_name: 655/655
- shipping_costs: 655/655
- EAN/gtins_product: 653/655 = 99,69 %
- asins_product: 130/655 = 19,85 %

Damit ist EAN/GTIN für das spätere harte providerübergreifende Matching grundsätzlich sehr gut geeignet; ASIN ist nur Zusatzsignal und nicht flächendeckend.

## Shops innerhalb der 655 Reitsportprodukte – Beispiele aus der Vollzählung
- kavalio.de: 209
- eBay: 79
- loesdau.de: 72
- albenisa.de: 60
- kaufland.de: 47
- Amazon: 42
- wahl-reitsport.com: 39
- equiva.com: 25
- weitere Shops vorhanden

## Wichtiger Trackingbefund / aktueller Hardlock
Alle 655 geprüften Reitsport-`product_deeplink`-Werte laufen über `ipn.idealo.de` und enthalten im Parameter `tst` den Literalplatzhalter `!!TIME_STAMP!!`.
Auch `image_url_1` ist ein iPN-Tracking-/Redirectlink und enthält denselben Platzhalter.

Der bereitgestellte Quick Setup Guide erklärt nicht, wie `!!TIME_STAMP!!` korrekt ersetzt werden muss. Eine öffentliche offizielle idealo-Dokumentation hierzu konnte in der zusätzlich durchgeführten Websuche nicht belegt werden.

Deshalb gilt: keine produktive Linkgenerierung und kein Ersetzen des Platzhalters durch eine geratene Zeitdarstellung. Erst die reale iPN-Regel bzw. ein bereits fertig nutzbarer Feed-/Trackingweg muss verifiziert werden.

## Architekturentscheidung
PASS für den nächsten Entwicklungsschritt:
- idealo besitzt reale, strukturierte Produktdaten.
- die vorhandene Affiliate-Zentrale muss nicht neu aufgebaut werden.
- idealo wird als separater Adapter auf den vorhandenen neutralen Creative-/Outputkern gesetzt.
- eBay bleibt unangetastet.
- gemeinsame Multi-Button-Karten bleiben nachgelagert.

Noch OFFEN vor produktiver Automatisierung:
1. dauerhaft automatisierbarer Feed-Abrufweg / Download-URL
2. Authentifizierung des automatischen Abrufs
3. korrekte Behandlung des `!!TIME_STAMP!!`-Platzhalters
4. Bild-/Trackingnutzungsregel, soweit nicht durch den Feed selbst abschließend vorgegeben

Keine dieser offenen Angaben wird geraten.
