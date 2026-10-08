# Affiliate Router 6.72.211 – AJAX lifecycle block 4 local hardtest

Date: 2026-10-08
Base manifest: cbffca676d430dc2097c692cdd5231cd72b4787c17e5692d78db5ca3505f1d08
Candidate manifest: fc302a4bc6a69ddafb30caa78a593f80833d3400c842bea2260a07f8cc067ab4

## Scope

Incremental performance-only cleanup on the unreleased 6.72.211 candidate.
Only `pferdeportal-affiliate-router.php` changes in this block.

## Change

On admin-ajax requests, do not register hooks for WordPress lifecycles that admin-ajax does not execute:
- `rest_api_init`;
- `admin_post_*` / `admin_post_nopriv_*` routes owned by the main router;
- `wp_enqueue_scripts`, `wp_head`, `wp_footer`;
- `template_redirect` and `wp` routes owned by the main router.

Search/query visibility hooks (`pre_get_posts`, `the_posts`, HivePress query/template hooks), shortcode registration, the real eBay AJAX endpoint and Affiliate schema protection remain untouched.

## Local positive / negative / regression

Exact block-3 main source hash before patch: `46ab33e94c008d234c0bc86c5ff771c99701c30a21626959fdaea2ca0f334ad4`.
Block-4 main source hash: `a757295eba5cd6e6c75fb6d7d63982dbf332e14a74f1628f4c8130c068c0bb5c`.

Focused exact-main hook harness:
- PHP lint: PASS.
- Normal frontend: 142 -> 142; hook multiset identical.
- Normal admin: 207 -> 207; hook multiset identical.
- Foreign admin-ajax: 116 -> 99 in focused main-file harness; exactly 17 impossible-lifecycle registrations removed.
- Real Affiliate AJAX `ppar_ebay_canonical_tick`: 119 -> 102 in focused main-file harness; the real AJAX endpoint and its schema hooks remain registered.
- Removed hook families are limited to `rest_api_init`, main-router `admin_post*`, `wp_enqueue_scripts`, `wp_head`, `wp_footer`, `template_redirect`, `wp`.

Combined with bound block-2 and block-3 deltas, expected foreign-AJAX hook count becomes 111 -> 94 while `init` remains 2.

No ranking, provider selection, slots, veto, publish, category, design, tracking, query filtering, HivePress visibility, table/schema definition or frontend output logic changed.

## Status

LOCAL_POSITIVE_NEGATIVE_REGRESSION_PASS.
WORDPRESS_MARIADB_CURRENT_GATE_OPEN.
NO_RELEASE. NO_INSTALL.
