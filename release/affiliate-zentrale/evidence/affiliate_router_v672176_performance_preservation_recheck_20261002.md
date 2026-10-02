# Affiliate Router 6.72.176 – Performance-Preservation Recheck

Date: 2026-10-02
Workstream: AFFILIATE_ZENTRALE
Branch: affiliate-release-current

## Authority / compared states

- Current authority: `control/release-governance/CURRENT_RELEASE.json`, generation 173.
- Current released version: `6.72.176`.
- Current source manifest SHA-256: `c01945cbd0e9aa4b107018260bfc833a8fc4f69aaee1f0e7a73f96391c2ffb4d`.
- Released 6.72.175 baseline commit used for direct source comparison: `32d61bce11161b339a360c4dec92be712f733424`.
- 6.72.176 functional source commit: `68e2e652cf88cd65eab0fb7e66e13790c1c704ed`.
- Current plugin source after release contains 27 files.

## Direct source delta recheck

Tree/blob comparison 6.72.175 -> current 6.72.176 shows exactly two changed plugin files:

1. `pferdeportal-affiliate-router.php`
2. `readme.txt`

All other 25 plugin files are blob-identical.

Explicit performance/runtime files rechecked byte-identical:

- `includes/trait-ppar-automation-suite.php` — identical.
- `includes/trait-ppar-output-objects.php` — identical.
- `includes/trait-ppar-ebay.php` — identical.
- `includes/trait-ppar-idealo.php` — identical.
- `includes/trait-ppar-housekeeping.php` — identical.

Within `pferdeportal-affiliate-router.php`, the following protected performance/ranking functions are text-identical to released 6.72.175:

- `ranked_campaigns_request_cache_allowed()`
- `ranked_campaign_sanitize_key_request_cached()`
- `ranked_campaign_sanitize_text_request_cached()`
- `ranked_campaigns_request_cache_key()`
- `select_category_product_campaign_fast_v672171()`
- `ranked_campaign_candidate_pool()`
- `ranked_campaigns_for_slot()`
- `category_product_provider_mix_v672133()`

The only functional main-router changes are:

- `render_banner()`: eBay BUSINESS product-card descriptions are omitted only for `category_product_1..3` and `hub_product_1..3`; source data remains unchanged.
- `auto_inject_template_affiliate_slots()`: the already selected `hub_after_cards` banner receives the missing real Hub-1/Hub-2 server mount, with duplicate/empty-slot guards.

No 6.72.171 request-local cache function, exact-GTIN path, provider-mix function, eBay cohort cache, Idealo cache, housekeeping logic, PRIVATE detail-content path, or non-eBay description path was replaced or rolled back.

## Executed gate evidence

Full gate run `36997283155`: SUCCESS.

Relevant successful steps:
- exact delta versus released 6.72.175;
- PHP syntax all current plugin files;
- preserve released performance and functionality hardlocks;
- existing provider and banner regressions;
- WordPress/MariaDB frontend equivalence 6.72.175 -> 6.72.176 within the intentional output scope;
- fresh installer verification;
- current frontend smoke;
- final release binding.

Targeted WordPress/MariaDB run `36997037385`: SUCCESS.

Relevant successful steps:
- real Hub-2 `hub_after_cards` mount;
- direct renderer contract;
- empty-slot negative guard;
- eBay card payload positive/negative regression;
- performance hardlocks.

## Result

PASS for preservation of all previously bound performance optimizations.

This is not a live-server wall-time claim for 6.72.176. The only current live gate remains the real WordPress readback of the released 6.72.176 installer, including:
1. Schabrackendesigner wide banner visibility.
2. No eBay BUSINESS long-description flash / unnecessary card payload.
