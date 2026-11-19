# Pferdeatelier – Affiliate 6.72.360 Performance-Rootfix

Stand: 2026-11-19

## Scope
Es wurde ausschließlich der nachgewiesene Performance-Rückschritt im request-lokalen eBay-Provider-Cohort-Cache für `category_product_1..3` korrigiert.

## Ursache
6.72.171 hatte die teure Seller-/Titel-/Providerprüfung für identische geordnete Kategorie-Kandidaten request-lokal gemeinsam wiederverwendet. In 6.72.359 enthält der Cache-Schlüssel wieder den exakten Slotnamen. Dadurch werden `category_product_1`, `_2`, `_3` bei identischem Kandidateninput getrennt neu berechnet.

Der Live-Ursachenprofil-Lauf 6.0 zeigt gleichzeitig:
- Pferdesättel Ø 7373.52 ms gesamt
- `the_content` Ø 5394.826 ms
- DB Ø 728.92 ms
- externe HTTP-Aufrufe 0 ms
- OPcache ~99.11 %

## Änderung 6.72.360
Nur `ebay_filter_ranked_product_candidates_provider_cohort()` ändert seinen request-lokalen Cache-Key für `category_product_1..3`:
- gemeinsamer Scope `category_product`
- gleicher effektiver Ausgabemodus Pflicht
- kompletter geordneter Kandidatenpayload muss identisch sein

Alle Nicht-Kategorie-Slots verwenden exakt die 6.72.359-Cacheidentität.

## Funktionsschutz
- 1552 -> 1552 benannte Funktionen
- entfernt 0
- hinzugefügt 0
- 1551 Funktionskörper unverändert
- exakt 1 geänderter Funktionskörper
- Hooks 206 -> 206; entfernt 0; hinzugefügt 0
- 66 -> 66 Plugin-Dateien; 63 byteidentisch
- Hauptdatei nur Version 6.72.359 -> 6.72.360
- Readme nur Dokumentation/Version

Nicht verändert: Produktauswahl, Reihenfolge, Multi-Provider, Fallback, Veto, Health, Bildprüfung, Tracking, eBay-Quelle, idealo/Amazon/Otto/Awin, Template 1.50.616, DB, Diagnose 6.0.

## Semantiktests
- 12.000 Zufallssequenzen / 36.000 Alt-Neu-Aufrufe: 0 Output-Abweichungen.
- 2.500 absichtlich veränderte Kandidatenpayloads: keine unzulässige Wiederverwendung; Buildzahl Alt = Neu.
- 2.500 Nicht-Kategorie-Fälle: Buildzahl Alt = Neu.
- deterministische Randfälle für alle fünf Provider-Modi, Source-Block, doppelte Seller/Titel, Cohorts, verifiziertes Otto/Awin, Mode-Wechsel: alle Output Alt = Neu.
- vorhandener echter eBay-Trait-Fachtest: Alt 35/35 PASS, Neu 35/35 PASS, stdout identisch.

## Performance-A/B
Isolierter Original-Funktionspfad, 710 identische Kandidaten, category_product_1..3, 31 Wiederholungen:
- 6.72.359: Median 35.36076 ms, 3 Builds
- 6.72.360: Median 12.901894 ms, 1 Build
- -63.51 %
- Output-Hash identisch

Dies ist kein Full-Page-Liveversprechen; es beweist nur die Beseitigung der nachgewiesenen Dreifacharbeit ohne Outputänderung.

## Paket
- `PFERDEATELIER_AFFILIATE_6.72.360_PERFORMANCE_ROOTFIX_TEST.zip`
- SHA256 `98aa67f8c1b6378e016692641dbae3175d90395aec37a0067897a6f99b48344a`
- 66 Dateien
- PHP 23/23 PASS
- ZIP CRC PASS

## Governance
Installierbarer Testkandidat. Formaler `release/affiliate-zentrale/current`-Stand wird durch diese Evidenz **nicht** automatisch promoted.
