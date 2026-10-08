# Affiliate Router 6.72.211 – AJAX lifecycle block 2 local hardtest

Date: 2026-10-08
Base: 6.72.211 candidate after AFF-ERR-064 / first AJAX reduction.

## Additional bounded performance delta

Only three additional existing runtime files changed:
- `includes/trait-ppar-idealo.php`
- `includes/trait-ppar-digistore24.php`
- `includes/class-ppar-deal-radar.php`

No workflow, architecture, ranking, provider selection, slot, veto, publish, category, design or tracking change.

## Positive / negative / regression

- Normal frontend hook multiset: 142 -> 142, identical: PASS.
- Normal admin hook multiset: 207 -> 207, identical: PASS.
- admin-ajax Affiliate hooks versus released 6.72.210: 207 -> 114.
- admin-ajax init hooks: 31 -> 5.
- admin-ajax admin_init hooks: 13 -> 0.
- admin-ajax shutdown hooks: 2 -> 1.
- existing `wp_ajax_ppar_ebay_canonical_tick`: preserved exactly once.
- Idealo upgrade/schedule/recovery init work no longer runs on unrelated AJAX.
- Deal-Radar schedule check no longer runs on unrelated AJAX.
- Digistore24 final-publication shutdown DB guard no longer runs on unrelated AJAX; normal frontend/admin behavior unchanged.
- AFF-ERR-064 renderer positive/negative/special-slot regression remains PASS.
- PHP lint: 22/22 PASS.
- Fresh-unpack PHP lint: 22/22 PASS.
- Source/ZIP byte identity: 28/28 PASS.

## Binding

- Candidate source manifest SHA-256: `13a63a5a6f3bbe968bbd5eed6d3310305c68f417d03e0b3741ab1d725b8514d8`.
- Local candidate ZIP SHA-256: `b2d4673db08572b8f5ca5705b5e29b5e8e05d2180784f32619fffc5d1b67addd`.
- Changed plugin files versus released 6.72.210: 4/28 total (main PHP + three lifecycle files).

## Gate status

LOCAL_POSITIVE_NEGATIVE_REGRESSION_PASS.
WORDPRESS_MARIADB_CURRENT_GATE_OPEN.
NO_RELEASE. NO_INSTALL.
