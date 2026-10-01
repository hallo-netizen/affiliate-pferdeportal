# Affiliate-Zentrale – Plugin-wide Dead-Code Inventory

Date: 2026-10-01
Branch: affiliate-release-current
Candidate: 6.72.173
Source manifest: e9c760bec991257fa99cc500e1dd305a5389de262baa714c1547ef036ccd821d
Mode: READ_ONLY INVENTORY / NO SOURCE DELETE

## Method

Current source only.
All 21 PHP files in the current source manifest were checked.
Only private/protected methods whose method name occurs nowhere outside their own declaration in the complete current PHP source are retained as strong dead-code candidates.

Methods initially looking unused were removed from this list as soon as any current cross-trait/cross-file reference was found.

## Result

Strong dead-code candidates:
- 44 methods
- approx. 798 function lines
- approx. 55,580 bytes

### eBay-related: 27 methods / ~420 lines / ~30,294 bytes

Main router:
- ebay_product_cached_image_url
- ebay_business_diag_resolve_public_target

eBay core:
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

eBay run:
- ebay_run_context_active
- ebay_run_worker_transport_migration_key
- ebay_run_register_background_dispatch
- ebay_run_spawn_core_cron_handoff
- ebay_run_wait_for_cron_lock_resolution
- ebay_run_fail_background_dispatch
- ebay_run_pause_for_budget
- ebay_run_last_failure_entry
- ebay_run_business_materialization_error_is_proven_soft_v6440

### Non-eBay: 17 methods / ~378 lines / ~25,286 bytes

Main router:
- article_word_count
- article_banner_limit_for_words
- select_article_insertion_positions
- render_article_banner_at_position
- render_article_product_block
- category_large_banner_rotate_candidates
- find_group_by_id
- resolve_category_placeholder_image_id
- resolve_category_placeholder_image_url
- render_campaign_editor

Output objects:
- output_pferde_design_layout_width

Automation:
- automation_scheduled_partner_batch
- automation_has_due_adcell_promotions

Creative library:
- creative_library_remote_image_dimensions
- creative_library_parse_dimensions
- creative_library_deactivate_existing_campaigns

Idealo:
- idealo_cached_image_url

## Explicit false-positive exclusions

Examples that were NOT classified as dead after cross-file checking:
- article_plan_bump_campaign_revision
- article_plan_apply_to_content
- automation_campaign_exact_target_rank
- render_awin_programme_gate_section
- digistore24_register_hooks
- digistore24_manual_csv_source_bound
- digistore24_manual_csv_affiliation_gate
- awin_fetch_current_joined_programmes
- adcell_api_v2_programme
- adcell_api_v2_promotion_categories
- adcell_api_v2_promotion_items
- adcell_api_v2_validate_csv_url
- adcell_api_v2_validate_tracking_asset_url
- article_preview_for_post
- insert_at_offset
- creative_library_text
- creative_library_tokens
- output_finalize_digistore24_object

These remain in source because current callers exist.

## Cleanup rule

No mass deletion.
Recommended cleanup batches after the current release gate is executable:
1. eBay-run dead stubs/migration helpers only.
2. eBay old admin/repair helpers only.
3. eBay old selection/diagnostic helpers only.
4. non-eBay dead helpers by owning subsystem.

Every batch must prove:
- current source identity before write;
- no references before removal;
- no protected performance code touched;
- PHP lint;
- positive/negative functional regression;
- relevant WordPress/MariaDB test;
- performance no-regression;
- source manifest refresh;
- full gate before release.

This inventory is not release authorization.
