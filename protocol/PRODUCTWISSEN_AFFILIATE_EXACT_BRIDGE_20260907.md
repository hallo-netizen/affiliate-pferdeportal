# PRODUCTWISSEN ↔ AFFILIATE EXACT-PRODUCT BRIDGE

STAND: 2026-09-07
STATUS: ISOLIERTER BRÜCKENKANDIDAT / NICHT IN PRODUCTWISSEN-HAUPTBRANCH INTEGRIERT

## Zweck

Produktwissen/Produktvergleich bleibt fachliche Produktwahrheit.
Affiliate bleibt Commerce-Schicht für Angebot, Preis, Verfügbarkeit, Verkäufer und Tracking.

Die Brücke verbindet beide Systeme ausschließlich read-only über den bestehenden Affiliate-Filter:

`ppar_affiliate_exact_product_requirements`

## Arbeitsgrenze

Dieser Branch basiert auf:

`hobbyroom/productwissen-v1-prototype`
Head bei Abzweig:
`42ad7460a903a64c22fe4dec1c70b901a6ecdd12`

Der laufende Produktwissen-/Produktvergleich-Branch wurde nicht verändert.

## Umsetzung

1. Neue Klasse:
`universal-product-comparison/src/class-upc-affiliate-bridge.php`

2. UPC registriert den Filter-Producer.

3. Neue WordPress-Drafts speichern zusätzlich:
`_upc_comparison_id`

4. Alte Drafts werden nur über das streng definierte UPC-UID-Format
`UPC-000001`
aufgelöst.

5. Die Brücke liest den Comparison-Bundle über `upc_repository()`.

6. Für jedes Vergleichssubjekt werden nur die in Productwissen erlaubten stabilen Kennungen ausgegeben:
- GTIN
- EAN
- MPN
- MANUFACTURER_ARTICLE_NUMBER

7. Hat ein Vergleichssubjekt keine belastbare Exact-ID:
**keine Affiliate-Anforderung und kein Ersatzprodukt**.

## Keine Kopplung

Die Brücke:
- liest keine UPK-Tabellen direkt;
- liest keine Affiliate-Tabellen;
- schreibt keine Affiliate-Daten;
- schreibt keine Produktfakten;
- kennt keinen OTTO-Sonderfall.

Damit bleibt sie providerneutral und projektübergreifend.

## Prüfweg

Statischer Contract-Test:

`php universal-product-comparison/tests/affiliate-exact-bridge-contract.php`

Zusätzlich PHP-Syntax:

`php -l universal-product-comparison/universal-product-comparison.php`
`php -l universal-product-comparison/src/class-upc-affiliate-bridge.php`
`php -l universal-product-comparison/src/class-upc-wordpress-draft.php`

## Aktueller Prüfstatus

STATIC CONTRACT: PASS

NICHT AUSGEFÜHRT:
- exakter PHP-Test auf einem Checkout dieses Branches;
- WordPress/MariaDB-Smoke mit echtem Comparison-Draft;
- gemeinsamer End-to-End-Lauf mit Affiliate.

## Integrationsregel

Der Produktvergleich-/Produktwissen-Arbeitsweg entscheidet über die Übernahme dieses Brückenkandidaten.
Affiliate darf diesen Parallelbranch nicht selbst in den offiziellen Produktwissen-Stand mergen.

Erst nach Übernahme + gemeinsamem End-to-End-Test gilt Productwissen → Affiliate Exact Match als real integriert.
