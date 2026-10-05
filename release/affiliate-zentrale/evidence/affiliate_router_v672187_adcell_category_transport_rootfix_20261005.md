# Affiliate Router 6.72.187 — ADCELL promotion-category transport rootfix

## Status
ROOT_CAUSE_PROVEN_FIX_IMPLEMENTED_TESTING_OPEN

## Real live proof before fix
Read-only live diagnosis on 2026-10-05T13:29:01Z against installed Router 6.72.186 proved:

- ADCELL programme 10787 / promo 322674 exists and is active.
- Promotion response contains `promotionCategoryId=14727` but an empty `promotionCategoryName`.
- Direct call through the existing `adcell_api_v2_promotion_categories()` path fails with `HTTP 405`.
- The same ADCELL credentials successfully return the promotion/banner list, so the proven failure is isolated to the category endpoint transport, not general ADCELL access.
- Existing Creative-Library row `banner-322674` is therefore stored as `banner_general_fallback` on `page:95` instead of an exact Reithelme edge.
- Guardian promo 185797 shows the same missing category-name condition and is also stored as general fallback.
- Existing 6.72.88 topic resync state is already `done`, therefore correcting only the HTTP transport would leave stale live rows unchanged.

## Root cause
`/affiliate/promotion/getPromoCategories` was routed through the generic ADCELL GET transport. The real endpoint rejects that method with HTTP 405. The promotion endpoints themselves continue to work with GET.

## 6.72.187 fix
1. ADCELL request adapter now binds HTTP method per endpoint:
   - program export: GET
   - CSV promotion: GET
   - banner promotion: GET
   - deeplink promotion: GET
   - promo categories: POST
2. Only `getPromoCategories` calls pass POST.
3. New one-time background resync `ppar_v672187_adcell_topic_resync` re-runs allowed ADCELL programmes after installation so stale category metadata and derived banner target edges are rebuilt.
4. No banner ranking change.
5. No frontend DB query added.
6. No frontend HTTP added.
7. No tracking URL is opened.
8. AWIN/eBay/other provider adapters remain unchanged.

## Source binding
- Candidate: 6.72.187
- Current source file count: 27
- Current source manifest SHA256: 8b0b896c162343e4503ccf8691432f83bce5acc553f7a1fd2cc58a5ee48b1551
- Active branch: affiliate-release-current
- Base live-failed candidate: 6.72.186

## First CI readback after source bind
Two observed failures are stale-gate/version bindings, not functional failures:
- Affiliate 6.72.170 Local Performance Simulation stopped at release guard because CURRENT_RELEASE still referenced the old manifest hash.
- TEMP Affiliate Banner Destination Library E2E 6.72.183 SOURCE stopped because the workflow hardcodes Version 6.72.183 before executing WordPress tests.

## Required next gate
Synchronize CURRENT_RELEASE to 6.72.187 and the exact manifest hash, then re-run/observe current applicable gates. Build no final installer and claim no live PASS until source/ZIP WordPress-MariaDB proof and real live readback complete.


## Targeted local red/green harness
A focused PHP harness using the exact 6.72.187 ADCELL transport contract and the real live IDs `program 10787 / promo 322674 / category 14727` passed 9/9:

- category GET rejected before HTTP;
- banner POST rejected, preserving existing banner GET contract;
- banner import remains technically valid;
- promo 322674 remains importable;
- category id 14727 preserved;
- category name `Reithelme` enters normalized row;
- title carries `Reithelme`;
- description carries `Werbemittelkategorie: Reithelme`;
- observed transport order is exactly banner GET then category POST.

This is a local wiring proof only. Real ADCELL POST success and the resulting live page selection remain release-blocking until installation/readback.
