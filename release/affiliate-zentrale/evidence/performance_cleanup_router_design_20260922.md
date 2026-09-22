# Performance cleanup – Affiliate Router + Design menu

Stand: 2026-09-22

## Affiliate Router – combined cleanup PASS
Final combined GitHub run: 35693264536 – SUCCESS
Dedicated CPU run: 35693134066 – SUCCESS
Ranking memo run: 35693058767 – SUCCESS

Changes layered on the already live-tested 6.72.145 branch:
- exact-safe eBay title similarity prefilter; existing similar_text >= 92.0 rule remains authoritative
- title signatures precomputed once per title
- request-local memo for identical ranked_campaigns_for_slot() calls in public frontend
- admin/cron/REST/WP-CLI/AJAX excluded from ranking memo
- 6.72.145 batch DB contract preserved
- banner distribution regression preserved

Hard semantic proof:
- 53,361 old/new title-pair duplicate decisions identical
- full two-pass seller/diversity output order identical
- 792-title unique corpus produces no false duplicate
- deterministic exact-safe bound reduces possible full similar_text comparisons to 79 in the synthetic corpus
- first uncached ranking body remains byte-identical after wrapper extraction
- combined cleanup workflow PASS

Package:
AFFILIATE_ZENTRALE_V6.72.147_PERFORMANCE_CPU_RANKING_CLEANUP_HARDTEST.zip
SHA-256: 905f6db0941c04d0275aad3e63db8bdca80fb95f6659de2d2bb118359a9d72a5
Fresh unpack: 27/27 byte-identical
PHP lint: 21/21 PASS
Compared with 6.72.145 only runtime code files changed:
- includes/trait-ppar-ebay.php
- pferdeportal-affiliate-router.php
6.72.142 Goldmaster remains untouched rollback anchor.

## Design / Template Kit – global menu setup cleanup PASS
GitHub workflow: Design Brand Menu Performance Hardtest
Final run: 35693870974 – SUCCESS

The fix deliberately preserves both original wp_nav_menu() calls because desktop and mobile use different wp_nav_menu_objects transformations.
Only the expensive core wp_setup_nav_menu_item metadata setup is request-locally reused for the second render via official WordPress pre/post setup hooks.

Real WordPress 7.1.1 test with 120-menu-item fixture:
Baseline:
- desktop metadata hooks after first render: 2520
- total after second render: 5040
- second render: 2520

Cached:
- desktop metadata hooks after first render: 2520
- total after second render: 2880
- second render: 360

Reduction in second-render metadata hook load: 85.7%.

Semantic proof:
- desktop HTML SHA256 unchanged:
  24a4b427238a46cb5e91199518e2caf0dbe1fc7d89db6dbcabee35b345965891
- mobile HTML SHA256 unchanged:
  c789dfb6205e5e64ef04bed5778e77297b6f63787d2ad972f8ca9d8c2ab1839c
- desktop-specific menu object filter preserved
- mobile-specific menu object filter preserved
- both original wp_nav_menu calls preserved
- source patch contract PASS
- real WordPress menu comparison PASS

Important:
- this design cleanup is currently a semantic patch + hard proof, not an installable replacement package, because no stale historic full plugin package may overwrite the current live Design plugin.
- no Kubio or theme changes are part of this cleanup.
