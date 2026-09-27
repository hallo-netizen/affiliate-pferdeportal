# Affiliate Router 6.72.166 – bundled query/source-read performance evidence

Date: 2026-09-27
Branch: affiliate-release-current
Workstream: AFFILIATE_ZENTRALE
Source manifest SHA-256: e6b3b8f9307dda69f11804447d424922951c08b9b316c374d81f551b6e47fb4b
Baseline diagnosis SHA-256: f18b39751cb3183fa81d56cf2f6dd277b5c43dbb7cedf9bc198163b05c2f1f29

## Scope

Performance only. No content, design, ranking, provider, slot, veto, publish, category/structure or quality-rule change.

One bundled router step:
1. pre_get_posts private-eBay/HivePress logic receives a cheap relevance gate before term resolution / queried-object work.
2. ebay_enforce_private_visibility_ceiling() resolves explicit listing-category IDs once and reuses them instead of rescanning the same query.
3. BUSINESS eBay source-row batch and fallback reads select only the fields used by the public safety contract instead of full rows.
4. Plugin version is 6.72.166.

Changed runtime files:
- affiliate-portal-router/includes/trait-ppar-ebay.php
- affiliate-portal-router/pferdeportal-affiliate-router.php

## Measured reason for the change

The post-6.72.165 diagnosis still showed repeated router term-taxonomy lookup patterns on normal portal pages and sampled get_term work at the eBay query-context callsite. These checks are only capable of changing HivePress listing/category queries, yet the global pre_get_posts callbacks were entering the expensive term/query resolution path before proving that the current query was relevant.

The same diagnosis also showed the BUSINESS source cache using one large hash-batch query. The safety consumer needs only: source_state, policy_state, route_state, item_end_at, source_payload, title, short_description. Retained identity fields: id, item_id, seller_account_type, creative_identity_hash.

## Targeted hard test

PHP 8.4 standalone behavioral harness: PASS.

Cases:
- ordinary page query -> PASS; expensive parent-term/category-id/queried-object work = 0
- ordinary post query -> PASS; expensive work = 0
- unrelated taxonomy query -> PASS; expensive work = 0
- hp_listing query -> PASS; visibility ceiling behavior retained
- hp_listing singular -> PASS; allowed as before
- Private Anzeigen taxonomy -> PASS; allowed as before
- other hp_listing_category taxonomy -> PASS; visibility ceiling retained
- explicit hp_listing_category tax_query for Private Anzeigen -> PASS; allowed as before

Single-pass assertion:
- ebay_enforce_private_visibility_ceiling() contains exactly one call to ebay_query_listing_category_term_ids() -> PASS

Source-row projection assertion:
- all row fields consumed by ebay_public_content_policy_reason_from_source_row() and ebay_business_campaign_source_allows_delivery_base() are present in the narrowed SELECT projection -> PASS
- missing required fields -> 0

## Bound source hashes

- includes/trait-ppar-ebay.php: dcbfa1fa1aa3043c9bc631862fc1a33741103fd1af573800b5a038c50320cd91
- pferdeportal-affiliate-router.php: 4694fc62eec0af4955efa97145906fc71baf07b100747079d2552aafe6e3940c
- CURRENT_SOURCE_SHA256.txt: e6b3b8f9307dda69f11804447d424922951c08b9b316c374d81f551b6e47fb4b

## Status

TARGETED_HARD_LOCAL_PASS.

No installer/release ZIP is produced at this point. Per release governance, the next action is one combined full gate over the source-bound 6.72.166 candidate. Only after that PASS should one installer be built and one real server readback be run.
