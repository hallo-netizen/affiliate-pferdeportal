# Affiliate Router 6.72.211 – frontend normalization reuse block 7 local hardtest

Date: 2026-10-08
Base manifest: 6db648e4651c81ca24608a47613fd2fb21c7ec7a651584f5b321a2f1860823b4
Candidate manifest: 3ac981ddd070120b687a6d8f33e3c3375630a4dd953c31ecd6385c270a4ede68

## Scope

One-file performance-only continuation of block 6.
On public frontend requests `get_campaigns()` now reuses the existing `ranked_campaign_from_post_cached()` normalization result for each campaign post instead of calling `campaign_from_post()` again.
Admin/Cron/REST/CLI/AJAX keep the historical uncached normalization path.

## Local positive / negative / regression

- PHP lint: 22/22 PASS.
- Two realistic campaigns, ranked-first: `get_post_meta()` 4 -> 2.
- Two realistic campaigns, campaigns-first: `get_post_meta()` 4 -> 2.
- `get_posts()` remains 1 -> 1 after block 6.
- Normalized campaign arrays: identical before/after.
- Ranked campaign arrays: identical before/after.
- Banner/product identity, network, placements, target keys and GTIN values: identical.

No ranking, ordering, provider, slot, veto, publish, category, design, tracking, schema or query semantics changed.

## Result

LOCAL_POSITIVE_NEGATIVE_REGRESSION_PASS.
DUPLICATE_FRONTEND_CAMPAIGN_META_NORMALIZATION_REMOVED.
WORDPRESS_MARIADB_CURRENT_GATE_OPEN.
NO_RELEASE. NO_INSTALL.
