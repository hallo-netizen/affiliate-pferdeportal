# Affiliate Router 6.72.166 – final combined release evidence

Date: 2026-09-29
Branch: affiliate-release-current
Workflow run: 36536649788
Tested head before release-binding-only commit: 7c48c10030d7cc6af4448902b83a7fcc718c6cdb
Source manifest SHA-256: e6b3b8f9307dda69f11804447d424922951c08b9b316c374d81f551b6e47fb4b
Final installer SHA-256: 08ba8f70fecd0b828a77dd5778886aa9095faf0ebf7102dc76035a51087f7da4
Final installer: release/affiliate-zentrale/artifacts/final/AFFILIATE_ZENTRALE_6.72.166.zip

## Current 6.72.166 combined gate

- Exact source binding: PASS
- Exact delta versus proven 6.72.165: PASS; only trait-ppar-ebay.php and pferdeportal-affiliate-router.php changed in runtime source.
- PHP lint: 21/21 PASS
- 6.72.166 performance-path assertions: PASS
- Existing provider / Awin / OTTO / banner regressions: PASS
- WordPress 7.1.2 + MariaDB activation: PASS
- 6.72.165 -> 6.72.166 query/function equivalence for bound changed paths: PASS
- Product deals + partner analytics real WordPress/MariaDB gate: PASS
- Universal manual import real WordPress/MariaDB positive/negative gate: PASS
- Frontend smoke: PASS
- Deterministic installer file count: 27 PASS
- Fresh unpack: PASS
- Source -> ZIP byte identity: 27/27 PASS
- Fresh-unpack PHP lint: 21/21 PASS

## Historical evidence reuse rule

Historical evidence is reused only where it remains an immutable factual baseline or where the relevant runtime dependency is hash-identical. Changed 6.72.166 paths are covered by the current direct equivalence/positive-negative gate. No historical source is used as the current source.
The historical gate name otto_awin_weighted_banner_distribution is retained only for governance compatibility. The current contract is relevance-first stable even distribution without fixed provider quotas or weekly rotation, and that current contract passed.
The historical 6.72.7 cleanup false-pass is not reused as release authority; the corrected 6.72.8 evidence and current regression are the authority for that behavior.

## Required-gate binding

- manual_single_upload_multi_provider_import: PASS — CURRENT_WORDPRESS_MARIADB_POSITIVE_NEGATIVE_GATE_PLUS_EXISTING_LOCAL_IMPORT_REGRESSIONS; prior_status=STALE_SOURCE_CHANGED; prior_evidence=release/affiliate-zentrale/evidence/manual_single_upload_multi_provider_import_20260902.txt
- explicit_scope_product_deals_partner_analytics: PASS — CURRENT_WORDPRESS_MARIADB_PROVIDER_NUMBERS_DEAL_POSITIVE_NEGATIVE_GATE; prior_status=PENDING; prior_evidence=NONE
- old_state_reproduction_negative: PASS — IMMUTABLE_HISTORICAL_NEGATIVE_BASELINE_REUSED_NO_RECONSTRUCTION; prior_status=STALE_SOURCE_CHANGED; prior_evidence=release/affiliate-zentrale/evidence/old_state_reproduction_negative_v6634_bound.txt
- same_state_rootfix_positive: PASS — HASH_IDENTICAL_EBAY_RUN_RECOVERY_CORE_REUSED_PLUS_CURRENT_FULL_GATE; prior_status=STALE_SOURCE_CHANGED; prior_evidence=release/affiliate-zentrale/evidence/same_state_rootfix_positive_v6638_fix1.txt
- counterstates_fail_closed: PASS — HASH_IDENTICAL_EBAY_RUN_RECOVERY_CORE_REUSED_PLUS_CURRENT_FAIL_CLOSED_REGRESSIONS; prior_status=STALE_SOURCE_CHANGED; prior_evidence=release/affiliate-zentrale/evidence/counterstates_fail_closed_v6638_fix1.txt
- complete_selection_materialization_public_gate: PASS — HISTORICAL_BOUND_E2E_REUSED_WITH_UNCHANGED_RECOVERY_CORE_AND_CURRENT_CHANGED_PATH_EQUIVALENCE; prior_status=STALE_SOURCE_CHANGED; prior_evidence=release/affiliate-zentrale/evidence/complete_selection_materialization_public_gate_v6638_fix1.txt
- relevant_historical_regressions: PASS — HISTORICAL_PASS_REUSED_WHERE_HASH_IDENTICAL_PLUS_CURRENT_PROVIDER_BANNER_QUERY_FRONTEND_REGRESSIONS; prior_status=STALE_SOURCE_CHANGED; prior_evidence=release/affiliate-zentrale/evidence/relevant_historical_regressions_v6638_fix1.txt
- real_wordpress_mariadb_persistence_same_uuid: PASS — HISTORICAL_REAL_DB_EVIDENCE_REUSED_FOR_HASH_IDENTICAL_RECOVERY_CORE_PLUS_CURRENT_WORDPRESS_MARIADB_GATE; prior_status=STALE_SOURCE_CHANGED; prior_evidence=release/affiliate-zentrale/evidence/real_wordpress_mariadb_persistence_same_uuid_v6638_fix1.txt
- recovery_retry_failure_paths: PASS — HASH_IDENTICAL_EBAY_RUN_RECOVERY_CORE_REUSED; prior_status=STALE_SOURCE_CHANGED; prior_evidence=release/affiliate-zentrale/evidence/recovery_retry_failure_paths_v6638_fix1.txt
- mutation_sabotage: PASS — CURRENT_MANIFEST_SOURCE_CHECK_PLUS_HISTORICAL_FAIL_CLOSED_MUTATION_EVIDENCE; prior_status=STALE_SOURCE_CHANGED; prior_evidence=release/affiliate-zentrale/evidence/mutation_sabotage_v6638_fix1.txt
- fresh_unpack_exact_installer: PASS — CURRENT_DETERMINISTIC_INSTALLER_FRESH_UNPACK_27_OF_27_PASS; prior_status=PENDING; prior_evidence=NONE
- source_zip_byte_identity: PASS — CURRENT_SOURCE_TO_ZIP_BYTE_IDENTITY_27_OF_27_PASS; prior_status=PENDING; prior_evidence=NONE
- final_sha256: PASS — CURRENT_FINAL_INSTALLER_SHA256_BOUND; prior_status=PENDING; prior_evidence=NONE
- otto_awin_automated_product_distribution: PASS — CURRENT_OTTO_AWIN_REGRESSION_GATE_PASS; prior_status=STALE_SOURCE_CHANGED; prior_evidence=release/affiliate-zentrale/evidence/otto_awin_productwissen_banner_contract_20260907.txt
- otto_awin_real_banner_source: PASS — CURRENT_REAL_BANNER_SOURCE_REGRESSION_GATE_PASS; prior_status=STALE_SOURCE_CHANGED; prior_evidence=release/affiliate-zentrale/evidence/otto_awin_banner_distribution_contract_20260907.txt
- otto_awin_weighted_banner_distribution: PASS — HISTORICAL_GATE_NAME_RETAINED_CURRENT_CONTRACT_IS_RELEVANCE_FIRST_STABLE_EVEN_DISTRIBUTION_NO_FIXED_QUOTAS_CURRENT_GATE_PASS; prior_status=STALE_SOURCE_CHANGED; prior_evidence=release/affiliate-zentrale/evidence/otto_awin_banner_distribution_contract_20260907.txt
- affiliate_6721_activation_smoke: PASS — HISTORICAL_GATE_NAME_SUPERSEDED_BY_CURRENT_6_72_166_WORDPRESS_ACTIVATION_PASS; prior_status=OBSOLETE_INVALID_VERSION_BELOW_LIVE_6_72_2; prior_evidence=release/affiliate-zentrale/evidence/affiliate-zentrale_v6.72.1_ACTIVATION_SMOKE_ONLY.txt
- affiliate_6723_activation_smoke: PASS — HISTORICAL_GATE_NAME_SUPERSEDED_BY_CURRENT_6_72_166_WORDPRESS_ACTIVATION_PASS; prior_status=STALE_SOURCE_CHANGED; prior_evidence=NONE
- otto_awin_real_account_joined: PASS — HISTORICAL_REAL_ACCOUNT_EVIDENCE_REUSED_PLUS_CURRENT_AWIN_IDENTITY_REGRESSION_PASS; prior_status=PASS_USER_SCREENSHOT; prior_evidence=NONE
- otto_awin_local_gate: PASS — HISTORICAL_LIVE_EVIDENCE_REUSED_PLUS_CURRENT_LOCAL_GATE_REGRESSION_PASS; prior_status=PASS_USER_SCREENSHOT; prior_evidence=NONE
- otto_awin_real_run_started: PASS — HISTORICAL_LIVE_RUN_EVIDENCE_REUSED_CURRENT_WORKER_REGRESSION_PASS; prior_status=PASS_USER_SCREENSHOT; prior_evidence=NONE
- otto_awin_offers_stage: PASS — HISTORICAL_LIVE_STAGE_EVIDENCE_REUSED_CURRENT_WORKER_REGRESSION_PASS; prior_status=PASS_USER_SCREENSHOT; prior_evidence=NONE
- otto_awin_feed_fail_closed: PASS — HISTORICAL_LIVE_FAIL_CLOSED_EVIDENCE_REUSED_CURRENT_SOURCE_GATE_REGRESSION_PASS; prior_status=PASS_USER_SCREENSHOT; prior_evidence=NONE
- otto_awin_first_functional_plugin_test: PASS — HISTORICAL_FAILURE_SUPERSEDED_BY_6_72_6_TO_6_72_8_FIX_EVIDENCE_AND_CURRENT_FULL_REGRESSION_PASS; prior_status=FAIL_INTEGRATION_DEFECT_DISCOVERED; prior_evidence=NONE
- otto_awin_large_feed_download: PASS — HISTORICAL_LIVE_DOWNLOAD_EVIDENCE_REUSED_CURRENT_WORKER_REGRESSION_PASS; prior_status=PASS_LIVE; prior_evidence=NONE
- awin_6725_progress_wpcron_rootfix: PASS — HISTORICAL_LIVE_PROGRESS_PASS_REUSED_CURRENT_AUTOMATION_REGRESSION_PASS; prior_status=STALE_SOURCE_CHANGED; prior_evidence=release/affiliate-zentrale/evidence/awin_6725_progress_wpcron_rootfix_20260908.txt
- otto_awin_6726_relevance_prefilter: PASS — HISTORICAL_POSITIVE_NEGATIVE_AND_LIVE_AUTOSTOP_EVIDENCE_REUSED_CURRENT_REGRESSION_PASS; prior_status=STALE_SOURCE_CHANGED; prior_evidence=release/affiliate-zentrale/evidence/awin_6726_otto_relevance_prefilter_20260908.txt
- otto_awin_6727_exact_run_cleanup: PASS — HISTORICAL_6_72_7_FALSE_PASS_NOT_REUSED_AS_FINAL_AUTHORITY; SUPERSEDED_BY_6_72_8_AND_CURRENT_TESTS; prior_status=STALE_SOURCE_CHANGED; prior_evidence=release/affiliate-zentrale/evidence/awin_6727_exact_run_cleanup_full_gate_20260908.txt
- otto_awin_6728_cleanup_provenance: PASS — HISTORICAL_CORRECTED_POSITIVE_NEGATIVE_EVIDENCE_PLUS_CURRENT_CLEANUP_REGRESSION_PASS; prior_status=STALE_SOURCE_CHANGED; prior_evidence=release/affiliate-zentrale/evidence/awin_6728_cleanup_provenance_full_local_gate_20260908.txt

## Result

FULL_COMBINED_RELEASE_GATE=PASS
RELEASE_CHECK_REQUIRED=YES
REAL_SERVER_READBACK_REQUIRED_AFTER_RELEASE=YES
