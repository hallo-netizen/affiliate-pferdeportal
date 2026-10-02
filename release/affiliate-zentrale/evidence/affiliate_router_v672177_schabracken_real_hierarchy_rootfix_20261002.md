# Affiliate Router 6.72.177 – Schabrackendesigner real-hierarchy rootfix candidate

Date: 2026-10-02
Branch: affiliate-release-current
Basis: released 6.72.176
Candidate: 6.72.177
Source file count: 27
Source manifest SHA-256: 55d99bcefeb3e592e2b691269bce3e91c3cd1be3fd37b3d65f2ccc468a6f85cf
Local candidate ZIP SHA-256: 1082384d1e36744994e4d7044c95afc67bf6d4dc8c57af4efe290f97806eba04

## Live finding

User readback after 6.72.176:
- Schabrackendesigner: FAIL.
- eBay BUSINESS cards are visible and the former long-description flash appears to be gone; the card still changes size during design runtime. This visual resize is explicitly not a fix target unless a measurable performance regression is proven.

No claim is made that the eBay visual resize is a performance defect.

## Proven test defect in 6.72.175/176 acceptance

The targeted WordPress/MariaDB test used a synthetic Pferde_Template_Kit fixture that returned hub2 whenever the page slug was schabracken.

The real design contract does not classify by that hard-coded slug. It derives the page type from the real WordPress hierarchy:
- ancestor depth 0 with children -> hub1;
- ancestor depth 1 with children -> hub2;
- ancestor depth 2 -> category;
- ancestor depth >= 3 -> leaf.

The real Schabracken path is Ausrüstung -> Sattel -> Schabracken, therefore the real page type is category.

The canonical wide slot contract is:
- hub1/hub2 -> hub_after_cards;
- category/leaf -> product_after_category_tiles.

The real category renderer already requests product_after_category_tiles. No design-plugin change and no second renderer are required.

## Candidate rootfix

6.72.177 adds exactly one admin-only, one-time repair path:
- reads only published portal_banner objects for exact target page:schabracken still materialized on hub_after_cards;
- resolves the linked real page and asks the real design plugin for affiliate_page_type();
- acts only when the real type is category or leaf;
- requires the exact stored page slug/target key to match;
- reloads the exact active creative source row;
- re-runs the existing authoritative output_plan_creative() planner;
- accepts completion only after a published replacement object exists on product_after_category_tiles;
- does not rewrite source data directly;
- does not run on frontend requests.

If no exact stale mismatch exists, no materialization is changed.

## Local positive / negative proof

PASS:
- stale Schabracken category mismatch -> eligible for replan;
- stale leaf mismatch -> eligible for replan;
- real hub2 -> untouched;
- real hub1 -> untouched;
- already-correct category slot -> untouched;
- wrong target key -> untouched;
- inactive campaign -> untouched;
- non-page target -> untouched;
- PHP lint 21/21;
- plugin file count remains 27.

## Performance preservation hardlock

Only these source files differ from released 6.72.176:
- pferdeportal-affiliate-router.php
- readme.txt

The following performance/runtime files are byte-identical to 6.72.176:
- includes/trait-ppar-automation-suite.php
- includes/trait-ppar-output-objects.php
- includes/trait-ppar-ebay.php
- includes/trait-ppar-idealo.php
- includes/trait-ppar-housekeeping.php

Inside pferdeportal-affiliate-router.php the following protected functions are text-identical to 6.72.176:
- render_banner()
- ranked_campaigns_request_cache_allowed()
- ranked_campaign_sanitize_key_request_cached()
- ranked_campaign_sanitize_text_request_cached()
- ranked_campaigns_request_cache_key()
- select_category_product_campaign_fast_v672171()
- ranked_campaign_candidate_pool()
- ranked_campaigns_for_slot()
- category_product_provider_mix_v672133()

Therefore the 6.72.176 eBay BUSINESS payload change and the previously released request caches, GTIN paths, eBay cohort logic, Idealo paths, housekeeping, provider mix and ranking optimizations are not replaced or rolled back.

## Release status

LOCAL CANDIDATE PASS ONLY.

release_allowed=false.

A new final installer is deliberately not bound. The repository currently has no version-neutral exact 6.72.177 WordPress/MariaDB full-gate workflow; the existing current-branch workflows are version-hardcoded to older candidates, and workflow changes are forbidden by the current release scope.

Required next proof:
1. exact 6.72.177 WordPress/MariaDB positive/negative full gate;
2. release-check and exact final installer only after that gate;
3. install once;
4. live readback: Schabrackendesigner must appear on the real Schabracken category page through product_after_category_tiles.

No AF-078, AF-079 or dead-code cleanup before this live closeout.
