# Affiliate Router 6.72.211 – frontend campaign query reuse block 6 local hardtest

Date: 2026-10-08
Base manifest: 7de4109b5ec8a5cbd610cd0a6fa608c188acd5d3b89571f9adf9e4b6b92bbd9f
Candidate manifest: 6db648e4651c81ca24608a47613fd2fb21c7ec7a651584f5b321a2f1860823b4

## Scope

One-file performance-only change in `pferdeportal-affiliate-router.php`.
`get_campaigns()` and `ranked_campaign_posts_snapshot()` use the same `ap_campaign` query arguments and ordering. On public frontend requests they now share the already existing request-local ranked post snapshot instead of issuing the identical `get_posts()` query twice.

Admin/Cron/REST/CLI/AJAX retain the historical `get_campaigns()` query path.

## Local positive / negative / regression

- PHP lint: 22/22 PASS.
- Exact query arguments before/after: identical.
- Public frontend, campaigns-first call order: `get_posts()` 2 -> 1.
- Public frontend, ranked-first call order: `get_posts()` 2 -> 1.
- Admin, campaigns-first: 1 -> 1.
- Admin, ranked-first: 1 -> 1.
- Two realistic campaign records: normalized campaign output identical before/after.
- Ranked post IDs/order identical before/after.
- Banner/product identity, placements, stored target keys and GTIN output identical before/after.

No ranking, ordering, provider, slot, veto, publish, category, design, tracking, schema or query arguments changed.

## Result

LOCAL_POSITIVE_NEGATIVE_REGRESSION_PASS.
ONE_DUPLICATE_FRONTEND_AP_CAMPAIGN_QUERY_REMOVED_WHEN_BOTH_PATHS_ARE_USED.
WORDPRESS_MARIADB_CURRENT_GATE_OPEN.
NO_RELEASE. NO_INSTALL.
