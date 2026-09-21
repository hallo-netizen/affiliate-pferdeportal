# Affiliate-Zentrale 6.72.145 – Performance Batch-Read Rootfix

Stand: 2026-09-21
Basis: gesicherter live bestätigter 6.72.142-Goldmaster + bereits getesteter 6.72.144 request-local cache fix.
Bannerfix 6.72.143 bleibt geparkt und ist nicht Bestandteil dieses Kandidaten.

## Live-Befund nach 6.72.144
Performance Diagnose Safe 2.0.0, Datei performance-diagnose-safe-20260921-192905.json:
- Weide: ca. 2.23 s / 528 Queries
- Reitplatz: ca. 5.48 s / 1542 Queries
- Reitplatzboden: ca. 5.66 s / 1538 Queries
- Heuwaagen: ca. 6.43 s / 1702 Queries
Restmuster auf tiefen Seiten:
- 792 x eBay creative_identity_hash BUSINESS lookup
- 190–315 x control_decisions lookup
- 45–87 x creative_library identity lookup

Wichtig: Das Diagnoseplugin normalisiert Query-Parameter. Die Zahlen belegen gleiche SQL-Signaturen, nicht automatisch denselben Hash. 6.72.144 hatte Wiederholungen desselben Schlüssels bereits request-lokal dedupliziert. Der belegte nächste Schritt ist daher bounded Batch-Read für die bereits bekannte Request-Kandidatenmenge.

## 6.72.145 Minimaldelta
Keine Fachlogikänderung.

1. Control Decisions
- öffentliches Frontend lädt alle Entscheidungen des aktuellen Portals einmal request-lokal;
- vorhandene/missing keys werden danach ohne weitere DB-Reads bedient;
- Write/Reset löscht Portal-Batch-Markierung;
- direkter Account-Deletion-Pfad leert Cache weiterhin.

2. eBay BUSINESS source rows
- bereits bekannte request-lokale Kampagnenmenge liefert die benötigten creative_identity_hashes;
- BUSINESS-Zeilen werden in bounded IN-Batches (max. 1000 Hashes) geladen;
- ORDER BY id DESC; erster Treffer pro Hash entspricht weiter dem bisherigen ORDER BY id DESC LIMIT 1;
- fehlende BUSINESS-Zeilen werden als missing gecacht;
- PRIVATE/INDIVIDUAL kann BUSINESS niemals erfüllen;
- Admin/Cron/REST/WP-CLI/AJAX bleiben nicht gebatcht.

3. Creative Library
- identity_hash ist DB-UNIQUE;
- benötigte Hashes werden in bounded IN-Batches (max. 1000) geladen;
- fehlende Rows werden request-lokal als missing markiert;
- Admin/Cron/REST/WP-CLI/AJAX bleiben nicht gebatcht.

## Source-Scope
6.72.142 -> 6.72.145 geändert nur:
- includes/trait-ppar-control-contract.php
- includes/trait-ppar-ebay-account-deletion.php
- includes/trait-ppar-ebay.php
- includes/trait-ppar-output-objects.php
- pferdeportal-affiliate-router.php (Version)
- readme.txt

Awin automation/transport source remains byte-identical to 6.72.142.
Keine CSS/JS-/Renderer-/Produkt-/Bannerfachlogik geändert.

## Lokale Hardtests
PASS:
- 315 distinct control decisions -> 1 portal batch query
- 100 distinct missing control keys -> 0 extra queries after preload
- Veto preserved
- Write invalidates batch and fresh Veto is read
- Reset remains Automatic
- direct deletion clears portal batch cache
- 792 distinct eBay BUSINESS hashes -> 1 bounded IN query
- exact latest BUSINESS row preserved
- PRIVATE excluded
- 87 distinct creative hashes -> 1 bounded IN query
- unique creative identity preserved
- outside-snapshot hash falls back safely to exact lookup
- Admin eBay/Creative remains unbatched/uncached
- all 21 PHP files lint PASS

## GitHub Hobbyraum
Workflow: Affiliate Performance Batch Hardtest
Final run: 35646653332
Head commit: 9c084d95d8074e63129bd54a8836e93cb344d3cc
Conclusion: SUCCESS

PASS isolated-batch-contract:
- two-stage 6.72.144 + 6.72.145 delta reproducible
- exact four-code-file patch scope
- all PHP syntax PASS
- distinct-key positive/negative batch hardtest PASS
- existing banner distribution regression PASS

PASS real-wordpress-mariadb-batch:
- WordPress 7.1.1
- PHP 8.3
- MariaDB 10.11
- plugin activation PASS
- exact residual counts simulated:
  * 315 distinct control keys -> 1 DB query
  * 792 distinct eBay BUSINESS hashes -> 1 DB query
  * 87 distinct creative hashes -> 1 DB query
- Write invalidation PASS
- Veto PASS
- PRIVATE/BUSINESS fail-closed PASS
- REAL_WORDPRESS_MARIADB_PERFORMANCE_BATCH_PASS

A stale hardcoded Awin hash test from an older repo source was intentionally removed from the batch workflow after proving it was unrelated: direct 6.72.142->6.72.145 file comparison shows the real Awin automation source byte-identical. No Awin code was changed by 6.72.145.

## Package
AFFILIATE_ZENTRALE_V6.72.145_PERFORMANCE_BATCH_READ_ROOTFIX_HARDTEST.zip
SHA-256: a5d6bccb11d41005be0f0db40b2dcdb32b8e40e73a772411b44039adedc548de
ZIP integrity: PASS
Fresh unpack: 27/27 files byte-identical to tested worktree.

## Production gate
6.72.145 is not yet production PASS.
Required next step:
- install 6.72.145;
- run Performance Diagnose Safe 2.0.0 on the same pages: Heuwaagen, Reitplatzboden, Reitplatz, Weide;
- compare exact query signatures/counts and server time;
- content and affiliate decisions must remain identical.
On any regression: immediate rollback to separately secured 6.72.142 GOLDMASTER.
