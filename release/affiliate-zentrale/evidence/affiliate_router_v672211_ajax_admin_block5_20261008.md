# Affiliate Router 6.72.211 – AJAX admin block 5 local hardtest

Date: 2026-10-08
Base manifest: fc302a4bc6a69ddafb30caa78a593f80833d3400c842bea2260a07f8cc067ab4
Candidate manifest: 7de4109b5ec8a5cbd610cd0a6fa608c188acd5d3b89571f9adf9e4b6b92bbd9f

## Scope

Incremental performance-only cleanup on unreleased 6.72.211.
Seven existing Affiliate files change only hook registration on admin-ajax.

## Local hardtest

Exact current source was reconstructed and hash-checked against the bound block-4 manifest before applying block 5.

- PHP lint: 22/22 PASS.
- Normal frontend: 142 -> 142 hooks; multiset identical.
- Normal admin: 207 -> 207 hooks; multiset identical.
- Foreign header AJAX: 94 -> 75 hooks.
- Real Affiliate eBay AJAX: 97 -> 78 hooks.
- Removed registrations: exactly 19.
- Added registrations on AJAX: 0.
- `wp_ajax_ppar_ebay_canonical_tick`: preserved.
- Foreign AJAX `init`: remains 2.
- Foreign AJAX `admin_init`: remains 0.
- Foreign AJAX `shutdown`: remains 1.

Removed from AJAX only:
- admin menus;
- admin-post handlers;
- one admin notice;
- Deal-Radar template_redirect click handler.

Preserved on AJAX:
- provider/custom filters and actions;
- option-update downstream hooks;
- search/query/HivePress hooks;
- cron callbacks;
- shortcode registration;
- real eBay AJAX endpoint and required schema guards.

No ranking, provider selection, slots, veto, publish, category, design, tracking, query filtering, HivePress visibility, schema/table definition or frontend output behavior changed.

## Result

LOCAL_POSITIVE_NEGATIVE_REGRESSION_PASS.
Combined foreign admin-ajax hook registration from released 6.72.210 baseline: 207 -> 75.
WORDPRESS_MARIADB_CURRENT_GATE_OPEN.
NO_RELEASE. NO_INSTALL.
