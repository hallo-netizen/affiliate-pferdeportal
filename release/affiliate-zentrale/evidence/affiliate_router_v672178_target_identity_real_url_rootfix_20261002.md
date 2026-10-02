# Affiliate Router 6.72.178 – target identity + real URL rootfix candidate

Date: 2026-10-02
Basis: 6.72.177
Candidate: 6.72.178
Source file count: 27
Source manifest SHA-256: e4343c221f37dda4653f3c9e339410b60940d97ff0fbc66c36a9de1ca09675cc
Local installer SHA-256: 125cb94c070973aa374d6caf1bf032c990e9e86cd3a53d2e5722580c96ed483a

## Proven root cause

The same real WordPress page was represented by two incompatible target-key forms:
- output objects: page:<ID>
- campaigns / automation / eBay target contracts: page:<slug>

6.72.177 compared these layers directly and even searched a stored output object for page:schabracken although the central local target catalog persists page:<ID>. Therefore a real target could be missed even when the page, slug and campaign were otherwise correct.

The local target catalog also did not use the real WordPress permalink when granting the strongest so-called target-URL evidence; a slug/string match could receive that bonus without first confirming the real portal URL.

## 6.72.178 rootfix

- Adds one central target-identity resolver. Existing page:<ID> storage remains compatible.
- page:<ID> and page:<slug> are aliases of the same real target only when they resolve to the same target object.
- Resolves the real WordPress public URL request-locally only for an already matching target candidate.
- Strong URL evidence is granted only when the real WordPress URL itself confirms the target slug.
- Replaces the Schabracken-hardcoded one-time repair with a generic bounded admin-only replan for stale hub_after_cards page banners whose real design type is category/leaf.
- The replan resolves the real page by campaign page_id and verifies both the old object and replacement through the central alias resolver.
- No frontend repair hook and no full-target permalink scan.

## Positive / negative proof

PASS:
- page:<ID> matches the same page target.
- page:<slug> matches the same page target.
- a foreign page slug is rejected.
- a second unrelated page resolves correctly.
- real public URL path is read and confirms its own slug.
- old page:schabracken hardcode is absent.
- generic replan remains bounded and admin-only.
- PHP lint 21/21.

## Performance preservation

Only these plugin files differ from 6.72.177:
- includes/trait-ppar-output-objects.php
- pferdeportal-affiliate-router.php
- readme.txt

Byte-identical:
- includes/trait-ppar-automation-suite.php
- includes/trait-ppar-ebay.php
- includes/trait-ppar-idealo.php
- includes/trait-ppar-housekeeping.php

Text-identical protected functions:
- render_banner()
- ranked_campaigns_request_cache_allowed()
- ranked_campaign_sanitize_key_request_cached()
- ranked_campaign_sanitize_text_request_cached()
- ranked_campaigns_request_cache_key()
- select_category_product_campaign_fast_v672171()
- ranked_campaign_candidate_pool()
- ranked_campaigns_for_slot()
- category_product_provider_mix_v672133()
- output_plan_creative()
- output_format_slot()
- output_object_upsert()
- output_save_local_campaign()

No eBay visual resize change. 6.72.176 eBay BUSINESS description-payload behavior is preserved.

## Status

LOCAL TARGETED POSITIVE/NEGATIVE PASS.
release_allowed=false until the bound WordPress/MariaDB full gate and release check are completed.
