# Affiliate Router 6.72.211 – cumulative local hardtest

Date: 2026-10-08
Released baseline: 6.72.210
Baseline installer SHA-256: 43ca6033a0f8dc929f777fc6580f2b41dfd711c6f561db99658f402cc5af88a1
Candidate source manifest SHA-256: 9f15bf679f44456c18c32aa6e04504e87248bc2748cfbca880532318915d311f
Candidate local ZIP SHA-256: dd38a9da9c54c60a9f805b8b6548680014adfc9bd5c6156a52adace5ff7cdef2
Candidate local ZIP bytes: 810227

## Exact source/package checks

- Baseline installer hash: exact PASS.
- Candidate source manifest: exact 28/28 PASS.
- Baseline PHP lint: 22/22 PASS.
- Candidate PHP lint: 22/22 PASS.
- Fresh-unpack candidate PHP lint: 22/22 PASS.
- Candidate source -> fresh ZIP byte identity: 28/28 PASS.
- Changed plugin files versus released 6.72.210: 8/28.

Changed files:
- pferdeportal-affiliate-router.php
- includes/class-ppar-admin-kiss.php
- includes/class-ppar-deal-radar.php
- includes/class-ppar-ds24-manual-downstream.php
- includes/class-ppar-partner-analytics.php
- includes/trait-ppar-digistore24.php
- includes/trait-ppar-idealo.php
- includes/trait-ppar-tariff-tools.php

## Cumulative AJAX regression

Hook-registration harness on exact baseline/candidate:

- Normal frontend: 142 -> 142, exact hook multiset identical.
- Normal admin: 207 -> 207, exact hook multiset identical.
- Foreign Header AJAX action `pftk_header_search_v150414`: 207 -> 75 Affiliate hook registrations.
- Foreign AJAX `init`: 31 -> 2.
- Foreign AJAX `admin_init`: 13 -> 0.
- Foreign AJAX `shutdown`: 2 -> 1.
- Existing `wp_ajax_ppar_ebay_canonical_tick`: preserved 1 -> 1.
- Real eBay AJAX retains required schema init hooks: candidate init=5.
- Public eBay/HivePress visibility hooks remain registered on foreign AJAX:
  - `the_posts -> ebay_filter_stale_posts`
  - `pre_get_posts -> ebay_expand_private_parent_listing_query`
  - `pre_get_posts -> ebay_enforce_private_visibility_ceiling`
  - HivePress listing query/template hooks.

Removed `pre_get_posts -> ebay_admin_filter_listing_query` is backend-list-only; its body requires admin main query and optional admin list GET filters. It is not the public HivePress visibility/search path.

## AFF-ERR-064

Exact extracted renderer negative/positive regression:
- 6.72.210 normal banner: undefined `$required_creative_type` warning reproduced.
- 6.72.211 normal banner: no warning and visible `Anzeige`.
- Product slots: no banner label.
- Glossary/breed/overview special output: byte-identical in harness.
- Unused category-large helper call removed from normal renderer.
- Result: PASS.

## Frontend duplicate-work reductions

Two realistic campaign records, both call orders:
- identical `ap_campaign` post load: 2 -> 1 `get_posts()`.
- duplicate campaign meta normalization: 4 -> 2 `get_post_meta()`.
- normalized campaign arrays: identical.
- ranked campaign arrays/order: identical.
- product/banner identity, network, placements, target keys and GTINs: identical.

Repeated content/category context fixture:
- returned content context: identical.
- returned category context: identical.
- post type/title/slug/terms/content resolution: 2 -> 1 per repeated identical content context.
- category ancestry calls across repeated content/category context: 4 -> 2.
- ancestor term resolution: 4 -> 2.
- context strip/tag work: 4 -> 2.
- admin path counts: exactly unchanged.

## Hard functional locks

No intended change to ranking, provider selection, slots, veto, publish, category, design, tracking, public query rules, HivePress visibility, schema/table definitions or automation semantics.

## Gate status

CUMULATIVE_LOCAL_POSITIVE_NEGATIVE_REGRESSION_PASS.
WORDPRESS_MARIADB_CURRENT_GATE_OPEN.
NO_RELEASE.
NO_INSTALL.
