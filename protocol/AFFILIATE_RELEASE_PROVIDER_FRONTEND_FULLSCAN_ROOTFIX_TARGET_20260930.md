# Affiliate-Zentrale 6.72.169 – providerneutraler Frontend-Vollscan-Rootfix

Datum: 2026-09-30

## Ziel

Die Affiliate-Zentrale darf bei normalen öffentlichen Seitenaufrufen keinen vollständigen Kampagnenbestand normalisieren oder providerweite Quelldaten vorsorglich laden, wenn für die aktuelle Seite bereits ein enger Kandidatenbestand feststeht.

Der Fix gilt grundsätzlich und providerneutral. Er beseitigt nicht nur den beobachteten eBay-Effekt, sondern alle aktuell belegten Frontendpfade mit demselben Muster.

## Belegte Ursachen

1. eBay BUSINESS:
   - `ebay_prime_business_campaign_source_row_cache()` lädt über `get_campaigns()` den gesamten Kampagnenbestand, sobald ein eBay-Kandidat seine Quellzeile benötigt.
   - Das passiert obwohl `ranked_campaigns_for_slot()` bereits einen seiten-/slotbezogenen Kandidatenbestand gebildet hat.

2. Multiprovider / idealo-GTIN-Zusatzangebote:
   - `multiprovider_exact_gtin_candidate_pool()` ruft im öffentlichen Frontend erneut `get_campaigns()` auf und baut daraus einen vollständigen GTIN-Index.
   - eBay-Kandidaten können dabei zusätzlich ihre BUSINESS-Quelldaten laden.

## Grundregel des Fixes

- Öffentlich: erst billig und roh vorselektieren; nur verbleibende Kandidaten normalisieren/prüfen.
- Provider-Quelldaten nur für bereits verbleibende Kandidaten gebündelt vorladen.
- Kein `get_campaigns()`-Vollscan aus einem Provider-/Exact-Offer-Hotpath.
- Admin, Cron, REST, WP-CLI und bestehende Wartungs-/Materialisierungspfade bleiben fachlich unverändert.
- Keine Änderung an Ranking, Relevanz, PRIVATE/BUSINESS, Providerstrategie, GTIN-Identität, Coverage, Quality, Health, Veto, Affiliate-Tracking oder Design.

## Providerprüfung

Der aktuelle Quellstand wird auf denselben Fehler für eBay, idealo, Awin/OTTO, Adcell, Digistore24 und allgemeine Multiprovider-Ausgabe geprüft.

Nur tatsächlich belegte Frontend-Vollscan-Pfade werden geändert. Provider ohne diesen Fehler bleiben unverändert.

## Abnahme

- kein providerbedingter `get_campaigns()`-Vollscan mehr im öffentlichen Produktkartenpfad;
- eBay-Quellcache lädt nur noch den tatsächlich vorausgewählten Kandidatenbestand;
- Multiprovider-Exact-GTIN-Suche nutzt den vorhandenen rohen Request-Index statt vollständiger Kampagnennormalisierung;
- gleiche Kandidatenreihenfolge und gleiche fachlichen Gates wie vorher;
- Positiv-/Negativtests inklusive eBay, idealo und Awin/OTTO;
- WordPress 7.1.2 + MariaDB;
- bestehende Provider-/Banner-/Rankingregressionen PASS;
- finaler Installer erst nach Full Gate.
