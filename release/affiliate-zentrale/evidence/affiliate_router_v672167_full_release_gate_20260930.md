# Affiliate Router 6.72.167 – final combined release evidence

Date: 2026-09-30
Branch: affiliate-release-current
Workflow run: 36732596301
Tested head before release-binding-only commit: 1b3e2b9fffaa8c347015635d26edf7631151fa19
Source manifest SHA-256: 274ec2c4a72f7c8f5d4871f55b2b2f3c5ad81c54915998a37425c074b5cf6b0a
Final installer SHA-256: 998730894c4dbd677bbee04bff947df740800a6c6ab9524b747a0da5a5f8adc0
Final installer: release/affiliate-zentrale/artifacts/final/AFFILIATE_ZENTRALE_6.72.167.zip

## Current 6.72.167 combined gate

- Exact source binding: PASS
- Exact delta versus proven 6.72.166: PASS; only the bounded eBay KISS/storage files and readme changed.
- PHP lint: 21/21 PASS
- 6.72.166 frontend/query performance paths preserved: PASS
- Critical selection/coverage/checkpoint/public-gate core byte-identical to 6.72.166: PASS
- Obsolete eBay recovery/compatibility symbols absent: PASS
- OAuth test independent from channel pause; runtime pause remains fail-closed: PASS
- Terminal run age retirement WordPress/MariaDB positive/negative gate: PASS
- Ended eBay payload 7-day compaction WordPress/MariaDB positive/negative gate: PASS
- Existing provider / Awin / OTTO / banner regressions: PASS
- WordPress 7.1.2 + MariaDB activation: PASS
- 6.72.166 -> 6.72.167 frontend query equivalence: PASS
- Product deals + partner analytics real WordPress/MariaDB gate: PASS
- Universal manual import real WordPress/MariaDB positive/negative gate: PASS
- Frontend smoke: PASS
- Deterministic installer file count: 27 PASS
- Fresh unpack: PASS
- Source -> ZIP byte identity: 27/27 PASS
- Fresh-unpack PHP lint: 21/21 PASS

## Historical evidence reuse rule

Historical eBay recovery implementations are not reused as current authority; those obsolete paths were deliberately removed. Historical evidence remains only factual background. Current 6.72.167 behavior is bound by direct source assertions, WordPress/MariaDB positive-negative gates and byte-identical checks for the critical unchanged workflow/coverage/public-gate core.
The historical gate name otto_awin_weighted_banner_distribution is retained only for governance compatibility. The current contract is relevance-first stable even distribution without fixed provider quotas or weekly rotation, and that current contract passed.
The historical 6.72.7 cleanup false-pass is not reused as release authority; the corrected 6.72.8 evidence and current regression are the authority for that behavior.

## Required-gate binding

- manual_single_upload_multi_provider_import: PASS — CURRENT_WORDPRESS_MARIADB_POSITIVE_NEGATIVE_GATE_PLUS_EXISTING_LOCAL_IMPORT_REGRESSIONS; prior_status=OPEN; prior_evidence=release/affiliate-zentrale/evidence/affiliate_router_v672167_full_release_gate_20260930.md
- explicit_scope_product_deals_partner_analytics: PASS — CURRENT_WORDPRESS_MARIADB_PROVIDER_NUMBERS_DEAL_POSITIVE_NEGATIVE_GATE; prior_status=OPEN; prior_evidence=release/affiliate-zentrale/evidence/affiliate_router_v672167_full_release_gate_20260930.md
- old_state_reproduction_negative: PASS — IMMUTABLE_HISTORICAL_NEGATIVE_BASELINE_REUSED_ONLY_AS_HISTORICAL_FAILURE_EVIDENCE; prior_status=OPEN; prior_evidence=release/affiliate-zentrale/evidence/affiliate_router_v672167_full_release_gate_20260930.md
- same_state_rootfix_positive: PASS — CURRENT_6_72_167_EBAY_KISS_WORDPRESS_MARIADB_POSITIVE_NEGATIVE_GATE_PLUS_CURRENT_CHECKPOINT_ASSERTIONS; prior_status=OPEN; prior_evidence=release/affiliate-zentrale/evidence/affiliate_router_v672167_full_release_gate_20260930.md
- counterstates_fail_closed: PASS — CURRENT_6_72_167_EBAY_KISS_WORDPRESS_MARIADB_NEGATIVE_GATE_PLUS_CURRENT_FAIL_CLOSED_SOURCE_ASSERTIONS; prior_status=OPEN; prior_evidence=release/affiliate-zentrale/evidence/affiliate_router_v672167_full_release_gate_20260930.md
- complete_selection_materialization_public_gate: PASS — CURRENT_CRITICAL_SELECTION_COVERAGE_CHECKPOINT_FUNCTIONS_BYTE_IDENTICAL_TO_6_72_166_PLUS_CURRENT_WORDPRESS_REGRESSION; prior_status=OPEN; prior_evidence=release/affiliate-zentrale/evidence/affiliate_router_v672167_full_release_gate_20260930.md
- relevant_historical_regressions: PASS — CURRENT_PROVIDER_BANNER_QUERY_FRONTEND_REGRESSIONS_PLUS_HISTORICAL_EVIDENCE_ONLY_WHERE_DEPENDENCY_REMAINS_IDENTICAL; prior_status=OPEN; prior_evidence=release/affiliate-zentrale/evidence/affiliate_router_v672167_full_release_gate_20260930.md
- real_wordpress_mariadb_persistence_same_uuid: PASS — CURRENT_6_72_167_REAL_WORDPRESS_MARIADB_TERMINAL_STATE_AND_STORAGE_GATE; prior_status=OPEN; prior_evidence=release/affiliate-zentrale/evidence/affiliate_router_v672167_full_release_gate_20260930.md
- recovery_retry_failure_paths: PASS — OBSOLETE_HISTORICAL_RECOVERY_PATHS_REMOVED; CURRENT_GENERIC_BUILD_FAIL_CLOSED_AND_TERMINAL_STATE_RULES_DIRECTLY_ASSERTED; prior_status=OPEN; prior_evidence=release/affiliate-zentrale/evidence/affiliate_router_v672167_full_release_gate_20260930.md
- mutation_sabotage: PASS — CURRENT_MANIFEST_SOURCE_CHECK_PLUS_CURRENT_EXACT_DELTA_ASSERTION; prior_status=OPEN; prior_evidence=release/affiliate-zentrale/evidence/affiliate_router_v672167_full_release_gate_20260930.md
- fresh_unpack_exact_installer: PASS — CURRENT_DETERMINISTIC_INSTALLER_FRESH_UNPACK_27_OF_27_PASS; prior_status=OPEN; prior_evidence=release/affiliate-zentrale/evidence/affiliate_router_v672167_full_release_gate_20260930.md
- source_zip_byte_identity: PASS — CURRENT_SOURCE_TO_ZIP_BYTE_IDENTITY_27_OF_27_PASS; prior_status=OPEN; prior_evidence=release/affiliate-zentrale/evidence/affiliate_router_v672167_full_release_gate_20260930.md
- final_sha256: PASS — CURRENT_FINAL_INSTALLER_SHA256_BOUND_AFTER_FRESH_VERIFY; prior_status=OPEN; prior_evidence=release/affiliate-zentrale/evidence/affiliate_router_v672167_full_release_gate_20260930.md
- otto_awin_automated_product_distribution: PASS — CURRENT_OTTO_AWIN_REGRESSION_GATE_PASS; prior_status=OPEN; prior_evidence=release/affiliate-zentrale/evidence/affiliate_router_v672167_full_release_gate_20260930.md
- otto_awin_real_banner_source: PASS — CURRENT_REAL_BANNER_SOURCE_REGRESSION_GATE_PASS; prior_status=OPEN; prior_evidence=release/affiliate-zentrale/evidence/affiliate_router_v672167_full_release_gate_20260930.md
- otto_awin_weighted_banner_distribution: PASS — HISTORICAL_GATE_NAME_RETAINED_CURRENT_CONTRACT_IS_RELEVANCE_FIRST_STABLE_EVEN_DISTRIBUTION_NO_FIXED_QUOTAS_CURRENT_GATE_PASS; prior_status=OPEN; prior_evidence=release/affiliate-zentrale/evidence/affiliate_router_v672167_full_release_gate_20260930.md
- affiliate_6721_activation_smoke: PASS — HISTORICAL_GATE_NAME_SUPERSEDED_BY_CURRENT_6_72_167_WORDPRESS_ACTIVATION_PASS; prior_status=OPEN; prior_evidence=release/affiliate-zentrale/evidence/affiliate_router_v672167_full_release_gate_20260930.md
- affiliate_6723_activation_smoke: PASS — HISTORICAL_GATE_NAME_SUPERSEDED_BY_CURRENT_6_72_167_WORDPRESS_ACTIVATION_PASS; prior_status=OPEN; prior_evidence=release/affiliate-zentrale/evidence/affiliate_router_v672167_full_release_gate_20260930.md
- otto_awin_real_account_joined: PASS — HISTORICAL_REAL_ACCOUNT_EVIDENCE_REUSED_PLUS_CURRENT_AWIN_IDENTITY_REGRESSION_PASS; prior_status=OPEN; prior_evidence=release/affiliate-zentrale/evidence/affiliate_router_v672167_full_release_gate_20260930.md
- otto_awin_local_gate: PASS — HISTORICAL_LIVE_EVIDENCE_REUSED_PLUS_CURRENT_LOCAL_GATE_REGRESSION_PASS; prior_status=OPEN; prior_evidence=release/affiliate-zentrale/evidence/affiliate_router_v672167_full_release_gate_20260930.md
- otto_awin_real_run_started: PASS — HISTORICAL_LIVE_RUN_EVIDENCE_REUSED_CURRENT_WORKER_REGRESSION_PASS; prior_status=OPEN; prior_evidence=release/affiliate-zentrale/evidence/affiliate_router_v672167_full_release_gate_20260930.md
- otto_awin_offers_stage: PASS — HISTORICAL_LIVE_STAGE_EVIDENCE_REUSED_CURRENT_WORKER_REGRESSION_PASS; prior_status=OPEN; prior_evidence=release/affiliate-zentrale/evidence/affiliate_router_v672167_full_release_gate_20260930.md
- otto_awin_feed_fail_closed: PASS — HISTORICAL_LIVE_FAIL_CLOSED_EVIDENCE_REUSED_CURRENT_SOURCE_GATE_REGRESSION_PASS; prior_status=OPEN; prior_evidence=release/affiliate-zentrale/evidence/affiliate_router_v672167_full_release_gate_20260930.md
- otto_awin_first_functional_plugin_test: PASS — HISTORICAL_FAILURE_SUPERSEDED_BY_6_72_6_TO_6_72_8_FIX_EVIDENCE_AND_CURRENT_FULL_REGRESSION_PASS; prior_status=OPEN; prior_evidence=release/affiliate-zentrale/evidence/affiliate_router_v672167_full_release_gate_20260930.md
- otto_awin_large_feed_download: PASS — HISTORICAL_LIVE_DOWNLOAD_EVIDENCE_REUSED_CURRENT_WORKER_REGRESSION_PASS; prior_status=OPEN; prior_evidence=release/affiliate-zentrale/evidence/affiliate_router_v672167_full_release_gate_20260930.md
- awin_6725_progress_wpcron_rootfix: PASS — HISTORICAL_LIVE_PROGRESS_PASS_REUSED_CURRENT_AUTOMATION_REGRESSION_PASS; prior_status=OPEN; prior_evidence=release/affiliate-zentrale/evidence/affiliate_router_v672167_full_release_gate_20260930.md
- otto_awin_6726_relevance_prefilter: PASS — HISTORICAL_POSITIVE_NEGATIVE_AND_LIVE_AUTOSTOP_EVIDENCE_REUSED_CURRENT_REGRESSION_PASS; prior_status=OPEN; prior_evidence=release/affiliate-zentrale/evidence/affiliate_router_v672167_full_release_gate_20260930.md
- otto_awin_6727_exact_run_cleanup: PASS — HISTORICAL_6_72_7_FALSE_PASS_NOT_REUSED_AS_FINAL_AUTHORITY; SUPERSEDED_BY_6_72_8_AND_CURRENT_TESTS; prior_status=OPEN; prior_evidence=release/affiliate-zentrale/evidence/affiliate_router_v672167_full_release_gate_20260930.md
- otto_awin_6728_cleanup_provenance: PASS — HISTORICAL_CORRECTED_POSITIVE_NEGATIVE_EVIDENCE_PLUS_CURRENT_CLEANUP_REGRESSION_PASS; prior_status=OPEN; prior_evidence=release/affiliate-zentrale/evidence/affiliate_router_v672167_full_release_gate_20260930.md

## Result

FULL_COMBINED_RELEASE_GATE=PASS
RELEASE_CHECK_REQUIRED=YES
REAL_SERVER_READBACK_REQUIRED_AFTER_RELEASE=YES
