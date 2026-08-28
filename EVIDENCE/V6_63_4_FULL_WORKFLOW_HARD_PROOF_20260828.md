# Affiliate-Zentrale V6.63.4 – Live-observed hard proof

**Status: PRE-RELEASE / NOT RELEASED**

## Exact live failure

- Canonical run UUID: `74b8372b-f481-493b-8485-1e98188ef02c`
- Read-only `external_tick_v2` terminal error: `business_safe_gap_proof_missing`
- Failed phase: `coverage_verify`
- Failure build: `6.63.0-private-public-tail-revalidation-rootfix-20260828`
- Admin live state at 20:59 MESZ: `resume_reason=private_public_revalidated`, selection `complete/complete`, `prepare_private_scanned=545`, `prepare_private_leaf_index=8`, public PRIVATE verified `250`, normal HivePress seen `55`, BUSINESS coverage `91/311`, missing `220`, last recovery reason `private_public_tail_revalidation`.

## Why V6.63.3 local PASS was insufficient

V6.63.3 required hidden bookkeeping fields (`private_public_revalidation.status`, `selection_scope`, `owner`) in its recovery gate. The local fixture assumed those fields. They are not the durable terminal invariant proved by the live state. Therefore V6.63.3 could pass its synthetic fixture while the real terminal state stayed failed.

The V6.63.4 test methodology is changed: the exact live-observed terminal state is now a first-class fixture, with the hidden fields deliberately absent.

## Negative / positive proof

**Negative V6.63.3:** exact live-observed fixture stays terminal failed and emits no bootstrap.

**Positive V6.63.4:** exact same fixture reopens only `gapfill_select`, preserves the same run UUID, discovery cursor and both candidate checkpoints, clears only mutable selection/stale proof, requires one fresh PRIVATE tail afterwards, emits exactly one `external_tick` bootstrap and is idempotent on a second `admin_init`.

Hard negatives also prove fail-closed behavior for wrong resume reason, incomplete selection, wrong selection phase, missing PRIVATE scan evidence, missing recovery history, wrong historical build, wrong failure phase/code, no gapfill attempt, mismatched missing scope, and disabled PRIVATE/BUSINESS routes.

## Full regression

- Source candidate: **40 suites / 619 PASS / 0 FAIL**
- Source PHP lint: **15/15 PASS**
- Installer roundtrip: **20/20 files byte-identical**
- Exact fresh-unpack candidate: **40 suites / 619 PASS / 0 FAIL**
- Fresh-unpack PHP lint: **15/15 PASS**
- Self-contained MASTER fresh replay: **40 suites / 619 PASS / 0 FAIL**
- MASTER integrity: **189/189 payload hashes PASS**

Installer SHA-256: `f2e3689714d70fffb08c7e953c899d4a84f78ca06d28c6d4b989f2ca27d1fe1f`

Self-contained MASTER SHA-256: `05e8a3c52501d56c7387542140198c067a422b235ab1319d2dab582173feabb8`

## Diff scope

V6.63.3 → V6.63.4 changes exactly:
- `includes/trait-ppar-ebay-run.php`
- `pferdeportal-affiliate-router.php`
- `readme.txt`

Released V6.62.0 → V6.63.4 changes four existing files plus the new Digistore trait; no files removed. Protected eBay provider fachlogic, eBay account deletion, idealo, provider registry, network sync, central automation, creative library, article plans, frontend CSS/JS, portal catalogs and portal structure remain byte-identical to V6.62.0.

## Release hardlock

Still **NOT RELEASED**. Live gates remain mandatory: same-run recovery → durable BUSINESS proof → fresh PRIVATE tail → coverage/public terminal PASS → new coverage export → Digistore marketplace live payload → approved vendor banner E2E → final exact installer/master regression.