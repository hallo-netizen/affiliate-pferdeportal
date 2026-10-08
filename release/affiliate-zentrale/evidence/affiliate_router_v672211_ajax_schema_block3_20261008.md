# Affiliate Router 6.72.211 – AJAX schema block 3 local hardtest

Date: 2026-10-08
Base manifest: 13a63a5a6f3bbe968bbd5eed6d3310305c68f417d03e0b3741ab1d725b8514d8
Candidate manifest: cbffca676d430dc2097c692cdd5231cd72b4787c17e5692d78db5ca3505f1d08

## Scope

Only `pferdeportal-affiliate-router.php` changes in this incremental block.
The existing 6.72.211 candidate remains unreleased.

## Proven precondition

`activate()` already calls all three schema installers:
- `maybe_install_control_contract_schema()`
- `maybe_install_output_objects_schema()`
- `maybe_install_ebay_schema()`

The init registrations remain active on normal frontend/admin requests and on the real Affiliate AJAX action `ppar_ebay_canonical_tick`.

## Local positive / negative / regression

Exact current main source hash before patch: `78e569550538e271ee3a9aaf8d17a8cae5c860bbcdee48851d5a23f449df448a`.
Candidate main source hash: `46ab33e94c008d234c0bc86c5ff771c99701c30a21626959fdaea2ca0f334ad4`.

- PHP lint: PASS.
- Activation schema binding: PASS.
- Normal frontend hook multiset: identical, 142 -> 142.
- Normal admin hook multiset: identical, 207 -> 207.
- Foreign admin-ajax: 119 -> 116 hooks in the focused exact-main harness.
- Foreign admin-ajax init: 9 -> 6 in the focused exact-main harness.
- Removed callbacks: exactly the three schema installers above.
- Real Affiliate AJAX `ppar_ebay_canonical_tick`: hook multiset identical, 119 -> 119.

Combined with already-bound 6.72.211 block-2 evidence (AJAX 207 -> 114, init 31 -> 5), this exact three-hook delta yields expected current foreign-AJAX target: AJAX hooks 114 -> 111 and init 5 -> 2, while the Affiliate AJAX path retains the schema installers.

No ranking, provider selection, slots, veto, publish, category, design, tracking, frontend HTTP, table definition or schema content changed.

## Status

LOCAL_POSITIVE_NEGATIVE_REGRESSION_PASS.
WORDPRESS_MARIADB_CURRENT_GATE_OPEN.
NO_RELEASE. NO_INSTALL.
