# Affiliate-Zentrale 6.72.144 – Performance N+1 Rootfix Hardtest

Stand: 2026-09-21
Basis: exakter separat gesicherter 6.72.142 Goldmaster
Goldmaster SHA-256: 8c25b833bb9c6a017cf83e767ac86bf221468c790445062077991f17462b5b6d

## Produktionsbefund vor Fix
Performance Diagnose Safe 2.0.0, problematische Seite:
- 13.671 DB-Queries
- ca. 10,323 s Serverzeit
- 11.297 identische ppar_control_decisions-Lookups
- 1.484 eBay BUSINESS-Lookups nach creative_identity_hash
- 305 Creative-Library-Lookups nach identity_hash

## Fix-Scope
Nur request-lokale Read-Deduplizierung:
1. control_get_decision(): decision_key Cache, inklusive Miss-Cache
2. control_set_decision(): zielgenaue Cache-Invalidierung nach Write
3. direkter eBay-Account-Deletion-Control-Delete: kompletter kleiner Decision-Cache wird geleert
4. ebay_business_campaign_source_row(): Frontend request-local Cache nach BUSINESS|creative_identity_hash
5. output_creative_row(): Frontend request-local Cache nach identity_hash
6. eBay-/Creative-Caches bleiben in Admin, REST, Cron, WP-CLI und AJAX deaktiviert

Keine Änderung an:
- Awin Transport
- Provider-/Partner-/Creative-/Target-/Slot-Entscheidungssemantik
- Veto/Approved/Paused/Emergency Stop
- eBay BUSINESS/PRIVATE-Regel
- idealo
- eBay Run
- CSS/JS
- Banner 6.72.143; dieser Arbeitsstrang bleibt separat pausiert

## Lokaler exakter 6.72.142-Goldmaster-Hardtest
- PHP Syntax: 21/21 PASS
- 11.297 identische Control Reads -> 1 DB Query: PASS
- 1.000 fehlende Control Reads -> 1 DB Query: PASS
- unterschiedliche Decision Keys kollidieren nicht: PASS
- Write -> Read sieht frischen Veto-Status: PASS
- Reset -> Read sieht automatic: PASS
- direkte Control-Löschung invalidiert Cache: PASS
- 1.484 identische eBay BUSINESS Reads -> 1 DB Query: PASS
- Hash A/B kollidieren nicht: PASS
- fehlender eBay BUSINESS Treffer wird sicher gecacht: PASS
- PRIVATE kann BUSINESS nicht erfüllen: PASS
- 305 identische Creative Reads -> 1 DB Query: PASS
- Creative Hash A/B kollidieren nicht: PASS
- fehlender Creative-Treffer wird sicher gecacht: PASS
- Admin eBay/Creative Reads bleiben uncached: PASS

## Diff gegen 6.72.142
27 Dateien gesamt.
21 Dateien byteidentisch.
Genau 6 Dateien geändert:
- includes/trait-ppar-control-contract.php
- includes/trait-ppar-ebay-account-deletion.php
- includes/trait-ppar-ebay.php
- includes/trait-ppar-output-objects.php
- pferdeportal-affiliate-router.php (nur Version 6.72.142 -> 6.72.144)
- readme.txt

Explizit byteidentisch zu 6.72.142:
- includes/trait-ppar-automation-suite.php
- includes/trait-ppar-awin-programme-gate.php
- includes/trait-ppar-idealo.php
- includes/trait-ppar-ebay-run.php
- assets/frontend.css
- assets/frontend.js

## GitHub Real WordPress/MariaDB Hardtest
Isolierter Branch:
affiliate-performance-cache-hardtest-20260921

GitHub Actions Run:
35643790349

Environment:
- WordPress 7.1.1
- PHP 8.3.33
- MariaDB 10.11
- normales Testplugin, kein MU-Plugin
- echter Frontend HTTP GET /?ppar_perf_cache_gate=1

Result:
REAL_WORDPRESS_MARIADB_PERFORMANCE_CACHE_PASS

Geprüft und PASS:
- 11.297 Control Reads -> exakt 1 DB Query
- Control approved Ergebnis unverändert
- Missing Control Miss-Cache
- unterschiedliche Control Keys
- Veto Write + frischer Read
- Reset
- Paused
- Emergency Stop an/aus
- direkte Control-Löschung
- 1.484 eBay BUSINESS Reads -> exakt 1 DB Query
- BUSINESS Result unverändert
- Missing BUSINESS
- PRIVATE blockiert
- 305 Creative Reads -> exakt 1 DB Query
- Creative Result unverändert
- Missing Creative

Bestehender Banner-Behavior-Gate im selben GitHub Run: PASS.
Alle 21 PHP-Dateien im GitHub-Kandidaten: Syntax PASS.

GitHub Artifact:
affiliate-performance-cache-hardtest
Artifact digest:
sha256:addf4e4d499890675261b8226d75e3846fa019db680f2a2e0c58cc4169d31bfc

## Neues Pluginpaket
Datei:
AFFILIATE_ZENTRALE_V6.72.144_PERFORMANCE_NPLUS1_ROOTFIX_HARDTEST.zip

SHA-256:
6f5acfdfbbd9174a30104b93b8df1db149495e0876e74644eb47fd3fae0f8828

Paketprüfung:
- ZIP integrity PASS
- fresh unpack PASS
- source -> ZIP -> fresh unpack byte identity 27/27 PASS
- Request-local cache test auf fresh unpack PASS

## Status
6.72.144 ist HARDTEST PASS und als separater Live-Testkandidat gebaut.
6.72.144 ist noch KEIN Produktions-PASS, bis dieselben URLs mit Performance Diagnose Safe 2.0.0 nach Installation erneut gemessen wurden.
6.72.142 bleibt unveränderlicher Rollback-Goldmaster.
Banner 6.72.143 bleibt pausiert und ist nicht Bestandteil von 6.72.144.
