# Affiliate-Zentrale 6.72.144 – Performance N+1 Request Cache Testnachweis

Stand: 2026-09-21
Basis: bytegenaue Arbeitskopie des gesicherten 6.72.142-Goldmasters
Banner-Arbeit 6.72.143: pausiert / nicht enthalten

## Ausgangsfehler
Performance Diagnose Safe 2.0.0:
- ca. 13.671 DB-Queries / ca. 10,3 s Serverzeit
- 11.297 wiederholte ppar_control_decisions-Lookups
- 1.484 wiederholte eBay-BUSINESS-Lookups
- 305 wiederholte Creative-Library-Lookups

## Minimaler Fix
Nur request-lokale Read-Deduplizierung:
1. control_get_decision(): Cache pro decision_key, inklusive Misses; Invalidierung nach Write/Reset sowie direktem Account-Deletion-Pfad.
2. ebay_business_campaign_source_row(): Cache pro BUSINESS|creative_identity_hash nur in read-only Frontend-Requests.
3. output_creative_row(): Cache pro identity_hash nur in read-only Frontend-Requests.

Admin, Cron, REST, WP-CLI und AJAX bleiben für eBay/Creative ungecached.
Keine fachliche Affiliate-Regel wurde geändert.

## Exakter 6.72.142 -> 6.72.144 Diff
Code geändert nur in:
- includes/trait-ppar-control-contract.php
- includes/trait-ppar-ebay-account-deletion.php
- includes/trait-ppar-ebay.php
- includes/trait-ppar-output-objects.php
Zusätzlich nur Versionskopf und Readme.
Alle übrigen Plugin-Dateien bleiben byteidentisch zu 6.72.142.
Awin-Transportdateien bleiben byteidentisch.

## Lokaler Hardtest auf echter 6.72.144-Source
PASS:
- 11.297 identische Control-Reads -> genau 1 DB-Read
- 1.000 fehlende Control-Reads -> genau 1 DB-Read
- verschiedene decision_keys kollidieren nicht
- Write -> Read liest frischen Veto-Status
- Reset -> Automatic bleibt korrekt
- direkter Account-Deletion-Pfad leert Control-Cache
- 1.484 identische eBay BUSINESS-Reads -> genau 1 DB-Read
- eBay Hash A/B kollidieren nicht
- Missing eBay wird sicher gecacht
- PRIVATE kann BUSINESS niemals erfüllen
- 305 identische Creative-Reads -> genau 1 DB-Read
- Creative Hash A/B kollidieren nicht
- Missing Creative wird sicher gecacht
- Admin eBay/Creative bleibt absichtlich ungecached
- alle 21 PHP-Dateien Syntax PASS
- Fresh-Unpack: 27/27 Dateien byteidentisch zum gebauten Arbeitsbaum

## GitHub Hobbyraum
Workflow: Affiliate Performance Cache Hardtest
Run: 35644557650
Commit: 8bd912dbb4b4774060ef2e9274bbcb44c239372d

PASS Job isolated-cache-contract:
- Patch reproduzierbar
- Patch-Scope exakt vier Cache-/Read-Pfade
- PHP-Syntax komplett PASS
- Positive/Negative N+1 Cache Hardtest PASS
- bestehender Banner-Distribution-Regressionstest PASS

PASS Job real-wordpress-mariadb:
- MariaDB 10.11
- PHP 8.3
- WordPress 7.1.1
- Plugin aktiviert
- Real-DB-Fixtures
- 11.297 Control-Reads -> 1 Query
- 1.484 eBay BUSINESS-Reads -> 1 Query
- 305 Creative-Reads -> 1 Query
- Missing-Fälle PASS
- Veto / Approved / Paused / Emergency Stop PASS
- Write-Invalidierung PASS
- BUSINESS/PRIVATE-Fail-Closed PASS
- REAL_WORDPRESS_MARIADB_PERFORMANCE_CACHE_PASS

## Paket
AFFILIATE_ZENTRALE_V6.72.144_PERFORMANCE_NPLUS1_REQUEST_CACHE_HARDTEST.zip
SHA-256: 6f5acfdfbbd9174a30104b93b8df1db149495e0876e74644eb47fd3fae0f8828
ZIP-Integrität: PASS

## Noch NICHT behauptet
6.72.144 ist noch kein Produktions-PASS.
Nächster Pflichtschritt ist Live-Installation als Testkandidat und erneute Messung derselben URLs mit Performance Diagnose Safe 2.0.0.
Abnahme nur wenn Query-Anzahl/Serverzeit massiv sinken und Inhalt/Freigaben/Vetos unverändert bleiben.
Bei jeder Regression sofort Rollback auf den separat gesicherten 6.72.142-Goldmaster.
