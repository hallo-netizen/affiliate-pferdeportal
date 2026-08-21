# V6.50 LIVE ROOT-CAUSE / DECISION GATE

Status: BLOCKED – no production build.

## Binding inputs
- Exact V6.49 MASTER baseline remains binding.
- Live canonical run UUID: `110e36b0-ad6b-4202-96d6-43604da654b6`.
- V6.49 live terminal failure: `insufficient_safe_sources`, `coverage_verify`, public BUSINESS 91/311, 220 missing.
- User-provided completed provider discovery summary from the same UUID/build lineage.
- User-provided source_refresh: 2172 checked, 1337 available, 0 transient errors, 9 technical errors (all seller-type mismatch).
- User-provided provider test: BUSINESS pass, INDIVIDUAL pass.

## Deterministic live-data findings
The completed BUSINESS discovery summary contains exactly 311 exact concept profiles.
- 91 concepts have at least one accepted candidate.
- 220 concepts have zero accepted candidates.
- 126/220 received zero provider results.
- 94/220 received provider results, but none survived the existing acceptance contract.
- Rejected-result aggregate hard reasons for those 94 zero-accepted profiles:
  - `ebay_marketplace_mismatch`: 393
  - `ebay_toy_item_blocked`: 69
  - `ebay_business_seller_feedback_low`: 48
  - `ebay_business_reference_only_match`: 15
  - `ebay_business_seller_feedback_count_low`: 11
  - `ebay_image_missing`: 1
- Aggregate review reasons:
  - `ebay_business_concept_missing`: 230
  - `ebay_portal_topic_negative`: 92
  - `ebay_portal_topic_missing`: 12
- All 20 required `wissen` concepts have zero accepted candidates; all 20 received zero results in this run.

These counts exactly explain the terminal 91/311 + 220 missing state. This is not an unexplained count anymore.

## Proven technical inconsistencies that are NOT sufficient as the root fix
Every exact BUSINESS catalog profile is hard-coded with `page_limit=1`, although the settings snapshot reports `max_pages_per_profile=4` and the admin UI exposes that setting. However only 15 of the 220 zero-accepted profiles ended with `stopped_reason=profile_page_limit`, i.e. a provider next page was actually available. Therefore restoring the configured page limit can broaden only 15 known missing profiles and cannot by itself prove terminal 311/311. Shipping only that change would be symptom patching.

`business_recovery` intentionally excludes the coarse BUSINESS fallback profiles used by full scope. Broadening recovery queries could change discovery/product-selection semantics and is not proven to produce safe supply for the remaining 220.

## Root cause
The canonical release contract currently equates two different things:
1. workflow correctness / successful completion; and
2. current external provider supply for every one of 311 required concept families.

`ebay_run_tick_coverage()` converts any family that still has no safe public source after one bounded gap-fill into a terminal `insufficient_safe_sources` failure. Live provider evidence proves that under the unchanged safety/quality rules the current run has safe accepted supply for 91 families, not 311. Thus the current all-or-nothing terminal contract cannot be made reliable by an infrastructure-only patch.

This is an architectural contract problem, not a remaining proven persistence/CAS/coverage-bridge defect.

## Why no V6.50 code change is allowed yet
The binding MASTER explicitly forbids autonomous changes to:
- product/listing domain logic,
- existing release rules,
- thresholds,
- priorities.

The technically sound architectural repair requires changing at least the BUSINESS completion/release contract and possibly the required automatic eBay supply manifest. That is therefore a fachlogic decision and requires explicit authorization.

## Recommended authorized architecture
Keep every existing safety, seller-quality, concept, marketplace, image, source freshness and target rule unchanged.

Change only the orchestration contract:
- `safe source available` => family covered;
- `no safe source currently available` => durable evidence-backed coverage gap, never fabricated or relaxed;
- gaps are automatically retried on later provider discovery cycles;
- terminal canonical SUCCESS means every phase completed and every family is either safely covered or explicitly recorded as a current provider-supply gap;
- no unsafe/review item can satisfy coverage;
- public output remains fail-closed per family;
- current UUID recovery must preserve verified existing public supply and convert only the terminal all-or-nothing state into the new explicit gap ledger.

This does not loosen acceptance or publication quality. It separates provider availability from technical workflow failure.

No installer/build until this fachlogic change is explicitly authorized and then proven end-to-end through exact live-shaped state -> terminal SUCCESS, full regressions, Fresh-Unpack, WordPress/PHP/MariaDB real gates, final ZIP, counterproof, hashes and MASTER.
