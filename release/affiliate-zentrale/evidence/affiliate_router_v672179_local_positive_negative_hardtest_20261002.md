# Affiliate Router 6.72.179 – local positive/negative hardtest

Date: 2026-10-02
Basis: 6.72.178 candidate
Version: 6.72.179
Source files: 27
Source manifest SHA-256: 5f868d91a174d54c4aca1bdd76cb17f3b56e3d03e478e34360b10fe02fb646b5
Locally packaged installer SHA-256: 97a8c00701b013ce69c944c55387d52691a40f0238bd1442efd9101f1190440a

## Root cause proven locally
The same real WordPress page crossed system layers with incompatible keys: output objects used page:<ID>, while campaigns/automation used page:<slug>. 6.72.178 added the central alias resolver and real WordPress URL confirmation.

The hard negative suite then found one additional ambiguity: hierarchical WordPress pages can share the same slug under different parents. A slug-only replacement could therefore validate the wrong real page.

## 6.72.179 hardening
- Manual/fixed slug target keys resolve only if exactly one real target matches.
- Duplicate slug aliases fail closed.
- Replan replacement must not only expose the expected target key; its published replacement campaign must carry the same real page_id as the source campaign.
- Existing ID and slug storage remain compatible.
- Real WordPress target URL confirmation from 6.72.178 remains unchanged.
- No frontend repair hook.

## Local test result
27/27 PASS.

Positive cases include:
- page:<ID> and page:<slug> alias same real target.
- real Schabracken target URL resolves and wins.
- independent Pferdedecken target URL resolves and wins.
- ID-stored stale object replans to slug-stored replacement.
- second unrelated page also replans.
- actual category slot selection returns product_after_category_tiles.
- actual hub2 slot selection returns hub_after_cards.

Negative cases include:
- foreign page ID rejected.
- foreign page slug rejected.
- fake local slug without matching real WordPress URL does not become READY.
- foreign partner target URL does not force an unrelated real page.
- genuine hub2 is untouched.
- foreign/mismatched stored target is untouched.
- wrong replacement target fails closed.
- frontend and admin-AJAX do not run the repair.
- same slug on a different real page_id fails closed.
- ambiguous manual/fixed slug target fails closed.

## Exact-code proof
The simulated replan body is normalized-text identical to the plugin method.
The category_large_banner_rule body used by the slot test is normalized-text identical to the plugin method.
PHP lint: 21/21 PASS.
Packaged ZIP re-extracted and rerun: 27/27 PASS, 21/21 lint PASS, 27 files.

## Performance preservation
Byte-identical to 6.72.177:
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

Changed plugin files only:
- includes/trait-ppar-output-objects.php
- pferdeportal-affiliate-router.php
- readme.txt

## Status
LOCAL POSITIVE/NEGATIVE HARDTEST PASS.
No release claim. WordPress/MariaDB full gate remains open.
