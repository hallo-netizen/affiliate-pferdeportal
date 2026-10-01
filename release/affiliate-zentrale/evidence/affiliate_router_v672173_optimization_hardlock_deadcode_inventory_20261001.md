# Affiliate-Zentrale – Optimization Hardlock + eBay Dead-Code Inventory

Date: 2026-10-01
Branch: affiliate-release-current
Current candidate: 6.72.173
Current source manifest SHA-256: e9c760bec991257fa99cc500e1dd305a5389de262baa714c1547ef036ccd821d

## Purpose

Read-only protection pass before any further eBay repair or plugin slimming.
No plugin source was changed by this audit.

## Protected optimization baseline

Verified directly against the current 6.72.173 committed source:

- `includes/trait-ppar-automation-suite.php` is byte-identical to the tested 6.72.171 performance source.
- `includes/trait-ppar-housekeeping.php` is byte-identical to the 6.72.172 housekeeping source.
- `includes/trait-ppar-ebay-run.php`, `includes/trait-ppar-idealo.php`, `includes/trait-ppar-provider-registry.php` and `includes/trait-ppar-network-sync.php` are byte-identical to the 6.72.172 basis.
- `pferdeportal-affiliate-router.php` differs from 6.72.172 only by 6.72.172 -> 6.72.173 version metadata.
- `includes/trait-ppar-ebay.php` differs from 6.72.172 only inside `ebay_portal_catalog()`.
- Outside `ebay_portal_catalog()`, the eBay trait is byte-identical to 6.72.172.
- The 6.72.171 request-local category-product, target-rank, control, health, image and eBay cohort/source caches remain present.
- The 6.72.170 exact-GTIN rootfix remains present; the unindexed `source_payload LIKE` path is absent.
- Historical numbers 329/1124 occur in the 6.72.173 validator only in a comment. The active validator uses the current catalog arrays/counts.

Hard rule for every following delta:
PERFORMANCE OR FUNCTIONAL REGRESSION = FAIL.
No rollback, no old source, no overwrite of 6.72.170/171/172 improvements.

## Current live performance baseline to preserve

Previously user-confirmed live readback under 6.72.171:
- Sattel: 8.85 s -> 2.31 s
- Pferdesättel: 9.09 s -> 4.63 s
- Trensen: 8.62 s -> 4.54 s
- Ausrüstung: 1.65 s -> 1.56 s
- HTTP 200 / no PHP errors / Affiliate Router active.

Known remaining performance potential:
- Pferdesättel and Trensen were still observed with about 320 DB queries each.
- No persistent object cache was detected in that readback.
These are optimization opportunities, not permission to change ranking or output semantics blindly.

## eBay dead-code inventory

Method:
- current 6.72.173 source only;
- all 21 current PHP files checked;
- private/protected eBay methods first identified where their name occurs only at their own declaration in the affected source set;
- all remaining current PHP files checked for external references;
- only methods with zero references outside their declaration are listed.

Result: 27 strong dead-code candidates, approx. 420 function lines / 30,294 bytes.

### Main router – 2 methods / ~97 lines / 6,356 bytes
- ebay_product_cached_image_url
- ebay_business_diag_resolve_public_target

### eBay core trait – 16 methods / ~266 lines / 20,466 bytes
- ebay_business_selection_plan
- ebay_private_selection_plan
- ebay_previewable_listing_post
- ebay_business_deactivate_existing_output
- ebay_business_restore_local_reclass_freshness
- ebay_mark_route_error
- ebay_refresh_reuse_classification
- ebay_business_local_reconcile_tick
- ebay_admin_progress_fingerprint
- ebay_admin_stall_guard
- ebay_private_reitstiefel_repair_needed
- ebay_start_reitstiefel_supply_repair_if_needed
- ebay_private_enrichment_needed
- ebay_start_private_enrichment_if_needed
- ebay_admin_nudge_open_jobs
- ebay_admin_bound_stale_jobs

### eBay run trait – 9 methods / ~57 lines / 3,472 bytes
- ebay_run_context_active
- ebay_run_worker_transport_migration_key
- ebay_run_register_background_dispatch
- ebay_run_spawn_core_cron_handoff
- ebay_run_wait_for_cron_lock_resolution
- ebay_run_fail_background_dispatch
- ebay_run_pause_for_budget
- ebay_run_last_failure_entry
- ebay_run_business_materialization_error_is_proven_soft_v6440

No deletion is authorized by this evidence alone.
Cleanup must be performed in small batches with source-identity guard, PHP lint, positive/negative functional tests and performance comparison.

## Open eBay/output defects – current read-only confirmation

### AF-078 PRIVATE counted but invisible
Current code still allows an empty/incomplete candidate map to skip published plugin-owned PRIVATE listings before ownership/source validation and may return PASS with public=0/invalid=[].
The checkpoint can then be committed with an empty `private_listing_ids` array.
This remains a reproducible code-path defect.

Rootfix boundary:
- never fail-open;
- a published plugin-owned valid PRIVATE listing outside the candidate set must create a candidate-gap and block checkpoint commit;
- genuinely stale/ended/policy/manual-blocked listings may remain outside the checkpoint;
- empty candidate may PASS only when no still-valid plugin-owned PRIVATE listing exists.

### AF-077 Banner automatic target classification
Current `output_classify_for_portal()` still applies `creative_domain_signal_missing` before real portal-target ranking.
Thus a strong real target such as Schabrackendesigner -> Schabracken can be stopped before its target evidence is evaluated.
Safety, negative evidence and veto must remain first and absolute.

### AF-079 BUSINESS
The symptom remains documented, but the first current live blocking state is not proven from public read-only data.
The plugin exposes admin-only read-only diagnostics, but no public read-only checkpoint/business diagnostic endpoint.
The public eBay REST endpoint is POST and advances the run; it was deliberately not called.

## Gate limitation

The current repository workflows for the prior releases hard-code 6.72.170 / 6.72.171.
The exact 6.72.173 current source cannot be claimed as full-gated through those workflows.
The existing 6.72.171 local A-B workflow does run PHP lint before its hard-coded version check, but it does not execute the functional A-B for 6.72.173.

Therefore:
- no false FULL PASS;
- no final installer;
- no source cleanup/fix should be called release-ready until the exact current source has completed the bound full functional gate.
