<?php
/**
 * Plugin Name: Affiliate-Zentrale (Portal-kompatibel)
 * Description: Zentrale, allgemeingültige Verwaltung und automatische Zuordnung von Affiliate-Kampagnen für Portal-Slots. Das Designplugin bleibt getrennt.
 * Version: 6.64.2
 * Author: OpenAI
 * Requires at least: 6.0
 * Requires PHP: 7.4
 * Text Domain: pferdeportal-affiliate-router
 */

if (!defined('ABSPATH')) {
    exit;
}

require_once __DIR__ . '/includes/trait-ppar-article-plans.php';
require_once __DIR__ . '/includes/trait-ppar-network-sync.php';
require_once __DIR__ . '/includes/trait-ppar-provider-intake.php';
require_once __DIR__ . '/includes/trait-ppar-provider-registry.php';
require_once __DIR__ . '/includes/trait-ppar-creative-library.php';
require_once __DIR__ . '/includes/trait-ppar-automation-suite.php';
require_once __DIR__ . '/includes/trait-ppar-control-contract.php';
require_once __DIR__ . '/includes/trait-ppar-output-objects.php';
require_once __DIR__ . '/includes/trait-ppar-ebay.php';
require_once __DIR__ . '/includes/trait-ppar-ebay-run.php';
require_once __DIR__ . '/includes/trait-ppar-ebay-account-deletion.php';
require_once __DIR__ . '/includes/trait-ppar-awin-programme-gate.php';
require_once __DIR__ . '/includes/trait-ppar-idealo.php';
require_once __DIR__ . '/includes/trait-ppar-digistore24.php';
require_once __DIR__ . '/includes/trait-ppar-housekeeping.php';

final class Pferdeportal_Affiliate_Router {
    use PPAR_Article_Plans_Trait;
    use PPAR_Network_Sync_Trait;
    use PPAR_Provider_Intake_Trait;
    use PPAR_Provider_Registry_Trait;
    use PPAR_Creative_Library_Trait;
    use PPAR_Automation_Suite_Trait;
    use PPAR_Control_Contract_Trait;
    use PPAR_Output_Objects_Trait;
    use PPAR_Ebay_Trait;
    use PPAR_Ebay_Run_Trait;
    use PPAR_Ebay_Account_Deletion_Trait;
    use PPAR_Awin_Programme_Gate_Trait;
    use PPAR_Idealo_Trait;
    use PPAR_Digistore24_Trait;
    use PPAR_Housekeeping_Trait;
    const VERSION = '6.64.2';
    const EBAY_RUNTIME_BUILD = '6.63.8-self-driven-canonical-orchestrator-rootfix-20260829';
    const CONTRACT_VERSION = '1.0';
    const PROVIDER_CONTRACT_VERSION = '2.0';
    const CAMPAIGN_POST_TYPE = 'ap_campaign';

    const OPTION_ENABLED = 'ppar_enabled';
    const OPTION_AUTO_SLOTS = 'ppar_auto_slots';
    const OPTION_GROUPS_JSON = 'ppar_groups_json';
    const OPTION_DISCLOSURE = 'ppar_disclosure';
    const OPTION_DEBUG = 'ppar_debug';

    const OPTION_TEMPLATE_ENABLED = 'ppar_template_enabled';
    const OPTION_TEMPLATE_CONTEXTS = 'ppar_template_contexts';
    const OPTION_CATEGORY_ENABLED = 'ppar_category_enabled';
    const OPTION_CATEGORY_SLOTS = 'ppar_category_slots';
    const OPTION_TEMPLATE_RULES_JSON = 'ppar_template_rules_json';
    const OPTION_DESIGN_RULES_JSON = 'ppar_design_rules_json';

    const OPTION_CAMPAIGNS = 'ppar_campaigns_v2';
    const OPTION_CAMPAIGNS_MIGRATED = 'ppar_campaigns_v2_migrated';
    const OPTION_CPT_MIGRATED = 'ppar_campaigns_cpt_migrated_v2';
    const OPTION_PLACEHOLDER_SETTINGS = 'ppar_ad_placeholder_settings_v1';
    const OPTION_NETWORK_AWIN = 'ppar_network_awin_v1';
    const OPTION_NETWORK_ADCELL = 'ppar_network_adcell_v1';
    const OPTION_NETWORK_AWIN_PROGRAMMES = 'ppar_network_awin_programmes_v1';
    const OPTION_NETWORK_AWIN_FEEDS = 'ppar_network_awin_feeds_v1';
    const OPTION_AWIN_PROGRAMME_GATE = 'ppar_awin_programme_gate_v1';
    const OPTION_PARTNER_INTAKE = 'ppar_partner_intake_v1';
    const OPTION_PARTNER_PROFILES = 'ppar_partner_profiles_v1';
    const OPTION_CREATIVE_LIBRARY_SCHEMA_VERSION = 'ppar_creative_library_schema_version';
    const OPTION_FALSE_CREATIVE_CLEANUP_VERSION = 'ppar_false_creative_cleanup_version';
    const OPTION_AUTOMATION_SCHEMA_VERSION = 'ppar_automation_schema_version';
    const OPTION_BRIDGE_TOKENS = 'ppar_automation_bridge_tokens_v1';
    const OPTION_AUTOMATION_SETTINGS = 'ppar_automation_settings_v1';
    const OPTION_AUTOMATION_CURSOR = 'ppar_automation_cursor_v1';
    const OPTION_AUTOMATION_SAFETY_VERSION = 'ppar_automation_safety_version';
    const OPTION_AUTOMATION_LAST_DISPATCH = 'ppar_automation_last_dispatch_v1';
    const OPTION_AUTOMATION_CYCLE = 'ppar_automation_cycle_v1';
    const OPTION_ASSIGNMENTS = 'ppar_assignments_v1';
    const OPTION_HEALTH_SETTINGS = 'ppar_health_settings_v1';
    const OPTION_HEALTH_CURSOR = 'ppar_health_cursor_v1';
    const OPTION_HEALTH_SCHEMA_VERSION = 'ppar_health_schema_version';
    const OPTION_ARTICLE_HYBRID = 'ppar_article_hybrid_v1';
    const OPTION_ARTICLE_PREVIEW = 'ppar_article_preview_v1';
    const OPTION_ARTICLE_PLAN_REVISION = 'ppar_article_plan_revision_v1';
    const OPTION_ARTICLE_PLAN_LOG = 'ppar_article_plan_log_v1';
    const OPTION_ARTICLE_REBUILD_STATE = 'ppar_article_plan_rebuild_state_v1';
    const OPTION_ARTICLE_PRODUCTS_UPGRADE = 'ppar_article_products_upgrade_v1';
    const OPTION_OUTPUT_SCHEMA_VERSION = 'ppar_output_schema_version';
    const OPTION_CONTROL_SCHEMA_VERSION = 'ppar_control_schema_version';
    const OPTION_CONTROL_SETTINGS = 'ppar_control_settings_v1';
    const OPTION_PROVIDER_ACCESS_STATE = 'ppar_provider_access_state_v1';
    const OPTION_PORTAL_REGISTRY = 'ppar_portal_registry_v1';
    const OPTION_NETWORK_EBAY = 'ppar_network_ebay_v1';
    const OPTION_NETWORK_IDEALO = 'ppar_network_idealo_v1';
    const OPTION_EBAY_SCHEMA_VERSION = 'ppar_ebay_schema_version';
    const OPTION_EBAY_SYNC_JOB = 'ppar_ebay_sync_job_v1';
    const OPTION_EBAY_REFRESH_JOB = 'ppar_ebay_refresh_job_v1';
    const OPTION_EBAY_PRIVATE_STRUCTURE_VERSION = 'ppar_ebay_private_structure_version';
    const OPTION_EBAY_CONTENT_FILTER_STATE = 'ppar_ebay_content_filter_state_v1';
    const OPTION_EBAY_BUSINESS_MATCH_STATE = 'ppar_ebay_business_match_state_v1';
    const OPTION_EBAY_MAINTENANCE_STATE = 'ppar_ebay_maintenance_state_v2';
    const OPTION_EBAY_MEDIA_CLEANUP_STATE = 'ppar_ebay_media_cleanup_state_v1';
    const OPTION_EBAY_CURATION = 'ppar_ebay_curation_v1';
    const OPTION_EBAY_SELECTION_STATE = 'ppar_ebay_selection_state_v2';
    const OPTION_EBAY_RUN_STATE = 'ppar_ebay_run_state_v1';
    const OPTION_EBAY_DELETION_TOKEN = 'ppar_ebay_deletion_token_v1';
    const OPTION_EBAY_DELETION_STATE = 'ppar_ebay_deletion_state_v1';
    const OPTION_EBAY_DELETION_RECEIPTS = 'ppar_ebay_deletion_receipts_v1';
    const OPTION_HOUSEKEEPING_STATE = 'ppar_housekeeping_state_v1';
    const ARTICLE_PLAN_META = 'ppar_article_delivery_plan_v1';
    const ARTICLE_PLAN_SCHEMA = '1.2';
    const HEALTH_META = 'ppar_health_data_v1';
    const HEALTH_CRON_HOOK = 'ppar_daily_health_check';
    const ARTICLE_REBUILD_HOOK = 'ppar_article_plan_rebuild_worker';
    const AUTOMATION_CRON_HOOK = 'ppar_partner_automation_sync';
    const AUTOMATION_WORKER_HOOK = 'ppar_partner_automation_worker';
    const ASSET_VERIFY_HOOK = 'ppar_verify_creative_assets';
    const HEALTH_SCHEMA_VERSION = '2.1';
    const OPTION_SYNC_SCHEMA_VERSION = 'ppar_sync_schema_version';
    const SYNC_SCHEMA_VERSION = '1.0';
    const AUTOMATION_SCHEMA_VERSION = '1.2';
    const CREATIVE_LIBRARY_SCHEMA_VERSION = '3.0';
    const OUTPUT_SCHEMA_VERSION = '1.3';
    const CONTROL_SCHEMA_VERSION = '1.1';
    const CONTROL_CONTRACT_VERSION = '2.0';
    const PORTAL_ADAPTER_VERSION = '1.0';
    const EBAY_SCHEMA_VERSION = '2.1';
    const EBAY_CONTENT_POLICY_VERSION = '6.4';
    const EBAY_PRIVATE_CLASSIFIER_VERSION = '4.1';
    const EBAY_BUSINESS_CLASSIFIER_VERSION = '6.1';
    const EBAY_MAINTENANCE_CRON_HOOK = 'ppar_ebay_maintenance_v2';
    const EBAY_MEDIA_CLEANUP_HOOK = 'ppar_ebay_media_cleanup_v1';
    const EBAY_MEDIA_CLEANUP_VERSION = '1.1';
    const EBAY_CRON_HOOK = 'ppar_ebay_sync';
    const EBAY_WORKER_HOOK = 'ppar_ebay_sync_worker';
    const OPTION_EBAY_WORKER_HEARTBEAT = 'ppar_ebay_worker_heartbeat_v1';
    const OPTION_EBAY_WORKER_TRANSPORT_MIGRATION = 'ppar_ebay_worker_transport_migration_v6412';
    const OPTION_EBAY_EXTERNAL_TICK_KEY = 'ppar_ebay_external_tick_key_v1'; // legacy, no longer used for V6.55 heartbeat
    const OPTION_EBAY_EXTERNAL_TICK_RATE_LOCK = 'ppar_ebay_external_tick_rate_lock_v1';
    const EBAY_SELF_DRIVE_ACTION = 'ppar_ebay_canonical_self_drive';
    const EBAY_SELF_DRIVE_TOKEN_TTL = 180;
    const OPTION_EBAY_COMPONENT_STATE_MIGRATION = 'ppar_ebay_component_state_migration_v6413';
    const OPTION_EBAY_PROGRESS_CONTRACT_MIGRATION = 'ppar_ebay_progress_contract_migration_v6420';
    const OPTION_EBAY_PUBLIC_CHECKPOINT = 'ppar_ebay_public_checkpoint_v1';
    const OPTION_EBAY_RUN_HISTORY = 'ppar_ebay_run_history_v1';
    const EBAY_PROGRESS_CONTRACT_VERSION = '3.1';
    const EBAY_WORK_BLOCK_TICK_LIMIT = 60;
    const EBAY_WORK_BLOCK_SECONDS = 600;
    const EBAY_WORK_BLOCK_PAUSE_SECONDS = 1;
    const EBAY_REFRESH_CRON_HOOK = 'ppar_ebay_inventory_refresh';
    const EBAY_REFRESH_WORKER_HOOK = 'ppar_ebay_inventory_refresh_worker';
    const EBAY_DELETION_REST_NAMESPACE = 'affiliate-zentrale/v1';
    const EBAY_DELETION_REST_ROUTE = '/ebay/account-deletion';
    const EBAY_EXTERNAL_TICK_REST_NAMESPACE = 'affiliate-zentrale/v1';
    const EBAY_EXTERNAL_TICK_REST_ROUTE = '/ebay/tick';
    const HOUSEKEEPING_CRON_HOOK = 'ppar_affiliate_housekeeping_daily_v1';

    private static $instance = null;
    private $disclosure_printed = array();
    private $campaigns_request_cache = null;
    private $ebay_canonical_worker_active = false;
    private $ebay_worker_dispatch_registered = false;
    private $ebay_worker_dispatch_at = 0;
    private $ebay_run_settings_override = null;

    public static function instance() {
        if (self::$instance === null) {
            self::$instance = new self();
        }
        return self::$instance;
    }

    private function __construct() {
        $this->idealo_register_hooks();
        $this->digistore24_register_hooks();
        add_action('init', array($this, 'register_campaign_post_type'), 5);
        add_action('init', array($this, 'register_shortcodes'));
        add_action('init', array($this, 'maybe_upgrade_health_checker'), 6);
        add_action('init', array($this, 'ensure_health_cron_schedule'), 20);
        add_action('wp_enqueue_scripts', array($this, 'enqueue_frontend_assets'));
        // Muss auch ausserhalb des Adminbereichs erreichbar sein: eBay validiert
        // diesen HTTPS-Endpunkt per GET-Challenge und sendet danach signierte POSTs.
        add_action('rest_api_init', array($this, 'register_ebay_account_deletion_routes'));
        add_action('rest_api_init', array($this, 'register_ebay_external_tick_route'));
        add_action('admin_post_' . self::EBAY_SELF_DRIVE_ACTION, array($this, 'handle_ebay_self_drive_worker'));
        add_action('admin_post_nopriv_' . self::EBAY_SELF_DRIVE_ACTION, array($this, 'handle_ebay_self_drive_worker'));
        add_filter('the_content', array($this, 'filter_the_content'), 20);
        add_filter('pftk_hub_grid_affiliate_data', array($this, 'provide_hub_grid_affiliate_data'), 10, 3);
        add_filter('pftk_leaf_category_affiliate_slot_html', array($this, 'provide_leaf_category_affiliate_slot_html'), 10, 4);
        add_filter('pftk_leaf_page_affiliate_slot_html', array($this, 'provide_leaf_page_affiliate_slot_html'), 10, 4);
        add_filter('pftk_market_affiliate_slot_html', array($this, 'provide_market_affiliate_slot_html'), 10, 4);
        // V2.2.7: Der Bildendpunkt streamt die aktuelle Mediendatei selbst.
        // Dadurch kann weder ein alter Redirect noch ein Browser-/CDN-Cache auf
        // dem vorherigen Attachment haengen bleiben.
        add_action('admin_post_ppar_placeholder_image', array($this, 'handle_placeholder_image'));
        add_action('admin_post_nopriv_ppar_placeholder_image', array($this, 'handle_placeholder_image'));
        add_filter('affiliate_portal_integration_status', array($this, 'provide_integration_status'), 10, 2);
        add_action('loop_end', array($this, 'auto_inject_category_archive_slots'));
        add_action('template_redirect', array($this, 'handle_click_redirect'), 0);
        add_action(self::HEALTH_CRON_HOOK, array($this, 'run_scheduled_health_check'));
        add_action(self::AUTOMATION_CRON_HOOK, array($this, 'run_scheduled_partner_sync'));
        add_action(self::AUTOMATION_WORKER_HOOK, array($this, 'run_automation_worker'));
        add_action(self::ASSET_VERIFY_HOOK, array($this, 'run_creative_asset_verification_batch'));
        add_action(self::HOUSEKEEPING_CRON_HOOK, array($this, 'run_housekeeping'));
        add_action('init', array($this, 'ensure_housekeeping_schedule'), 27);
        add_filter('cron_schedules', array($this, 'automation_cron_schedules'));
        add_action('save_post_post', array($this, 'handle_article_plan_post_save'), 40, 3);
        add_action(self::ARTICLE_REBUILD_HOOK, array($this, 'run_article_plan_rebuild_worker'));
        add_action('init', array($this, 'maybe_apply_automation_safety_upgrade'), 7);
        add_action('init', array($this, 'maybe_install_control_contract_schema'), 8);
        add_action('init', array($this, 'maybe_install_output_objects_schema'), 9);
        add_action('init', array($this, 'maybe_install_ebay_schema'), 10);
        // Checkpoint contract: an open run from another runtime build is never
        // version-by-version recovered. It is closed fail-safe and the next run
        // starts with a new UUID from the last confirmed public checkpoint.
        add_action('init', array($this, 'maybe_adopt_stalled_zero_tick_ebay_run_v6638'), 3);
        add_action('init', array($this, 'maybe_close_incompatible_ebay_run_for_checkpoint_restart'), 4);
        add_action('init', array($this, 'maybe_enforce_ebay_deletion_compliance'), 11);
        add_action('init', array($this, 'ensure_automation_schedule'), 21);
        add_action('init', array($this, 'retire_ebay_legacy_cron_transport'), 22);
        add_action('init', array($this, 'ensure_ebay_maintenance_schedule'), 24);
        // Controlled rebuild: normal page requests must never migrate inventory or
        // start/continue PRIVATE/BUSINESS recovery. Legacy worker-state adoption is
        // state-only and occurs inside the canonical worker/start path, never here.
        // Taxonomy migration is explicit via the setup button. Legacy media cleanup
        // only schedules bounded background work.
        add_action('init', array($this, 'ensure_ebay_media_cleanup_schedule'), 26);
        // V6.54 KISS transport: no eBay fach work is owned by WP-Cron.
        // A provider-neutral authenticated REST heartbeat advances exactly one
        // canonical package per request. Legacy cron hooks are cleared on init.

        add_action(self::EBAY_MEDIA_CLEANUP_HOOK, array($this, 'run_ebay_media_cleanup_worker'));
        add_filter('cron_schedules', array($this, 'ebay_cron_schedules'));
        // eBay-Drafts bekommen eine eigene, nonce-geschützte Admin-Vorschau.
        // HivePress stellt für Draft-Listings keine native öffentliche Preview-Route
        // bereit; deshalb wird das reale listing_view_page-Template direkt gerendert.
        add_filter('preview_post_link', array($this, 'ebay_filter_preview_post_link'), 20, 2);
        // Remote-only eBay images: replace only the two HivePress image blocks
        // for listings carrying the private eBay marker. Native HivePress listings
        // continue to use their regular WordPress attachments unchanged.
        add_filter('hivepress/v1/templates/listing_view_block/blocks', array($this, 'ebay_remote_image_listing_view_block'), 1000, 2);
        add_filter('hivepress/v1/templates/listing_view_page/blocks', array($this, 'ebay_remote_image_listing_view_page'), 1000, 2);
        // V6.15: Runtime fallback at the actual HivePress Container boundary.
        // This path is also reached when HivePress renders a saved hp_template
        // instead of instantiating the default Listing_View_* template class.
        add_filter('hivepress/v1/blocks/container', array($this, 'ebay_remote_image_container_blocks'), 1000, 2);
        // Native WordPress-Preview-Queries can already be a 404 before template_redirect.
        // Run the same eBay-only preview gate once after the main query and again at
        // template_redirect; a successful render exits, so there is no double output.
        add_action('wp', array($this, 'ebay_handle_secure_listing_preview'), -100);
        add_action('template_redirect', array($this, 'ebay_handle_secure_listing_preview'), -100);
        // Published eBay singles are rendered from their exact canonical path only.
        // This eBay-only route does not depend on the current rewrite cache or on
        // HivePress recognising the single query first; ordinary listings are untouched.
        add_action('template_redirect', array($this, 'ebay_rescue_published_listing_route'), -90);
        add_action('template_redirect', array($this, 'ebay_redirect_legacy_private_category'), -85);
        add_filter('the_posts', array($this, 'ebay_filter_stale_posts'), 999, 2);
        // HivePress baut Listing-Kategorieabfragen selbst. Private Anzeigen muss alle
        // direkten fachlichen Unterkategorien mitaggregieren; Provider-Ebenen bleiben unsichtbar.
        add_action('hivepress/v1/models/listing/query', array($this, 'ebay_expand_private_parent_listing_query'), PHP_INT_MAX);
        add_action('hivepress/v1/models/listing/query', array($this, 'ebay_enforce_private_visibility_ceiling'), PHP_INT_MAX);
        // Fallback nach allen normalen pre_get_posts-Manipulationen, falls ein anderes
        // HivePress-Zusatzplugin die Taxonomie-Klausel später wieder verengt.
        add_action('pre_get_posts', array($this, 'ebay_expand_private_parent_listing_query'), PHP_INT_MAX);
        add_action('pre_get_posts', array($this, 'ebay_enforce_private_visibility_ceiling'), PHP_INT_MAX);
        // V5.14: Kein schreibender eBay-Lifecycle mehr auf normalen Frontend-Aufrufen.
        // Frische wird weiterhin fail-closed gefiltert; Statusmutationen erfolgen nur
        // in Sync/Admin-Lifecycle-Pfaden, niemals beim bloßen Seitenaufruf.

        if (is_admin()) {
            add_action('admin_menu', array($this, 'admin_menu'));
            add_action('admin_init', array($this, 'maybe_migrate_campaigns'));
            add_action('admin_init', array($this, 'maybe_apply_article_products_upgrade'));
            add_action('admin_init', array($this, 'maybe_cleanup_false_partner_creatives'));
            // V6.63: narrow state-only recovery for the proven PRIVATE public-gate tail defect.
            // It never restarts a run or mutates listings/campaigns on admin_init; it only
            // reopens the exact failed V6.62 run into a bounded PRIVATE-only selection tail.
            add_action('admin_init', array($this, 'maybe_recover_ebay_private_public_gate_v6630'));
            add_action('admin_init', array($this, 'maybe_recover_ebay_business_gap_proof_v6634'));
            add_action('admin_init', array($this, 'maybe_recover_ebay_private_public_freshness_v6635'));
            add_action('admin_init', array($this, 'maybe_recover_ebay_build_change_checkpoint_same_uuid_v6636'));
            add_action('admin_post_ppar_save_campaigns', array($this, 'handle_save_campaigns'));
            add_action('admin_post_ppar_save_campaign', array($this, 'handle_save_campaign'));
            add_action('admin_post_ppar_delete_campaign', array($this, 'handle_delete_campaign'));
            add_action('admin_post_ppar_save_central_settings', array($this, 'handle_save_central_settings'));
            add_action('admin_post_ppar_save_placeholder_settings', array($this, 'handle_save_placeholder_settings'));
            add_action('admin_post_ppar_save_networks', array($this, 'handle_save_networks'));
            add_action('admin_post_ppar_save_network', array($this, 'handle_save_network'));
            add_action('admin_post_ppar_save_assignment', array($this, 'handle_save_assignment'));
            add_action('admin_post_ppar_delete_assignment', array($this, 'handle_delete_assignment'));
            add_action('admin_post_ppar_test_network', array($this, 'handle_test_network'));
            add_action('admin_post_ppar_save_awin_programme_gate', array($this, 'handle_awin_programme_gate_save'));
            add_action('admin_post_ppar_run_health_check', array($this, 'handle_run_health_check'));
            add_action('admin_post_ppar_export_portal_coverage', array($this, 'handle_export_portal_coverage'));
            add_action('admin_post_ppar_save_health_settings', array($this, 'handle_save_health_settings'));
            add_action('admin_post_ppar_save_settings', array($this, 'handle_save_settings'));
            add_action('admin_post_ppar_save_article_hybrid', array($this, 'handle_save_article_hybrid'));
            add_action('admin_post_ppar_save_article_preview', array($this, 'handle_save_article_preview'));
            add_action('admin_post_ppar_rebuild_article_plans', array($this, 'handle_rebuild_article_plans'));
            add_action('admin_post_ppar_rebuild_single_article_plan', array($this, 'handle_rebuild_single_article_plan'));
            add_action('admin_post_ppar_run_network_sync', array($this, 'handle_run_network_sync'));
            add_action('admin_post_ppar_partner_intake_probe', array($this, 'handle_partner_intake_probe'));
            add_action('admin_post_ppar_partner_profile_save', array($this, 'handle_partner_profile_save'));
            add_action('admin_post_ppar_creative_library_import', array($this, 'handle_creative_library_import'));
            add_action('admin_post_ppar_creative_library_selection', array($this, 'handle_creative_library_selection'));
            add_action('admin_post_ppar_automation_full_sync', array($this, 'handle_automation_full_sync'));
            add_action('admin_post_ppar_automation_materialize', array($this, 'handle_automation_materialize'));
            add_action('admin_post_ppar_automation_save_settings', array($this, 'handle_automation_save_settings'));
            add_action('admin_post_ppar_automation_process_next', array($this, 'handle_automation_process_next'));
            add_action('admin_post_ppar_output_object_action', array($this, 'handle_output_object_action'));
            add_action('admin_post_ppar_control_save_global', array($this, 'handle_control_save_global'));
            add_action('admin_post_ppar_provider_access_save', array($this, 'handle_provider_access_save'));
            add_action('admin_post_ppar_control_save_decision', array($this, 'handle_control_save_decision'));
            add_action('admin_post_ppar_ebay_save_settings', array($this, 'handle_ebay_save_settings'));
            add_action('admin_post_ppar_ebay_setup_categories', array($this, 'handle_ebay_setup_categories'));
            add_action('admin_post_ppar_ebay_verify_catalog', array($this, 'handle_ebay_verify_catalog'));
            add_action('admin_post_ppar_ebay_test_connection', array($this, 'handle_ebay_test_connection'));
            add_action('admin_post_ppar_ebay_run_sync', array($this, 'handle_ebay_run_sync'));
            add_action('admin_post_ppar_ebay_run_refresh', array($this, 'handle_ebay_run_refresh'));
            add_action('admin_post_ppar_ebay_run_restart', array($this, 'handle_ebay_run_restart'));
            add_action('wp_ajax_ppar_ebay_canonical_tick', array($this, 'handle_ebay_canonical_tick'));
            add_action('admin_post_ppar_ebay_review_decision', array($this, 'handle_ebay_review_decision'));
            add_action('admin_post_ppar_ebay_business_curation', array($this, 'handle_ebay_business_curation'));
            add_action('admin_init', array($this, 'maybe_install_network_sync_schema'));
            add_action('admin_init', array($this, 'maybe_install_creative_library_schema'));
            add_action('admin_init', array($this, 'maybe_install_automation_schema'));
            add_action('admin_init', array($this, 'maybe_cleanup_removed_import_tokens'));
            add_action('admin_enqueue_scripts', array($this, 'admin_assets'));
            add_action('admin_notices', array($this, 'admin_notices'));
            add_filter('manage_hp_listing_posts_columns', array($this, 'ebay_admin_listing_columns'));
            add_action('manage_hp_listing_posts_custom_column', array($this, 'ebay_admin_listing_column_content'), 10, 2);
            add_filter('post_row_actions', array($this, 'ebay_admin_listing_row_actions'), 20, 2);
            add_action('restrict_manage_posts', array($this, 'ebay_admin_listing_filters'));
            add_action('pre_get_posts', array($this, 'ebay_admin_filter_listing_query'));
            // Workflow V2: opening admin screens is read-only for eBay lifecycle.
            add_action('add_meta_boxes', array($this, 'add_page_role_meta_box'));
            add_action('save_post_page', array($this, 'save_page_role_meta_box'));
        }

        if (defined('WP_CLI') && WP_CLI && class_exists('WP_CLI')) {
            $this->register_automation_cli();
        }
    }

    public static function activate() {
        if (get_option(self::OPTION_ENABLED, null) === null) {
            update_option(self::OPTION_ENABLED, '0', false);
        }
        if (get_option(self::OPTION_AUTO_SLOTS, null) === null) {
            update_option(self::OPTION_AUTO_SLOTS, array(), false);
        }
        if (get_option(self::OPTION_DISCLOSURE, null) === null) {
            update_option(self::OPTION_DISCLOSURE, 'Hinweis: Einige Links auf dieser Seite sind Affiliate-Links. Wenn Sie darüber kaufen, erhalten wir ggf. eine Provision. Für Sie entstehen keine Mehrkosten.', false);
        }
        if (get_option(self::OPTION_DEBUG, null) === null) {
            update_option(self::OPTION_DEBUG, '0', false);
        }
        if (get_option(self::OPTION_GROUPS_JSON, null) === null) {
            update_option(self::OPTION_GROUPS_JSON, self::default_groups_json(), false);
        }
        if (get_option(self::OPTION_TEMPLATE_ENABLED, null) === null) {
            update_option(self::OPTION_TEMPLATE_ENABLED, '0', false);
        }
        if (get_option(self::OPTION_TEMPLATE_CONTEXTS, null) === null) {
            update_option(self::OPTION_TEMPLATE_CONTEXTS, array(), false);
        }
        if (get_option(self::OPTION_CATEGORY_ENABLED, null) === null) {
            update_option(self::OPTION_CATEGORY_ENABLED, '0', false);
        }
        if (get_option(self::OPTION_CATEGORY_SLOTS, null) === null) {
            update_option(self::OPTION_CATEGORY_SLOTS, array(), false);
        }
        if (get_option(self::OPTION_TEMPLATE_RULES_JSON, null) === null) {
            update_option(self::OPTION_TEMPLATE_RULES_JSON, self::default_template_rules_json(), false);
        }
        if (get_option(self::OPTION_DESIGN_RULES_JSON, null) === null) {
            update_option(self::OPTION_DESIGN_RULES_JSON, self::default_design_rules_json(), false);
        }
        if (get_option(self::OPTION_CONTROL_SETTINGS, null) === null) {
            update_option(self::OPTION_CONTROL_SETTINGS, array('emergency_stop'=>0,'emergency_reason'=>'','updated_at'=>0,'updated_by'=>0), false);
        }
        if (get_option(self::OPTION_PROVIDER_ACCESS_STATE, null) === null) {
            update_option(self::OPTION_PROVIDER_ACCESS_STATE, array(), false);
        }
        if (get_option(self::OPTION_CAMPAIGNS, null) === null) {
            update_option(self::OPTION_CAMPAIGNS, array(), false);
            update_option(self::OPTION_CAMPAIGNS_MIGRATED, '0', false);
        }
        if (get_option(self::OPTION_CPT_MIGRATED, null) === null) {
            update_option(self::OPTION_CPT_MIGRATED, '0', false);
        }
        if (get_option(self::OPTION_PLACEHOLDER_SETTINGS, null) === null) {
            update_option(self::OPTION_PLACEHOLDER_SETTINGS, self::placeholder_defaults(), false);
        }
        if (get_option(self::OPTION_NETWORK_AWIN, null) === null) {
            update_option(self::OPTION_NETWORK_AWIN, self::network_awin_defaults(), false);
        }
        if (get_option(self::OPTION_NETWORK_ADCELL, null) === null) {
            update_option(self::OPTION_NETWORK_ADCELL, self::network_adcell_defaults(), false);
        }
        if (get_option(self::OPTION_NETWORK_AWIN_PROGRAMMES, null) === null) {
            update_option(self::OPTION_NETWORK_AWIN_PROGRAMMES, array(), false);
        }
        if (get_option(self::OPTION_NETWORK_AWIN_FEEDS, null) === null) {
            update_option(self::OPTION_NETWORK_AWIN_FEEDS, array(), false);
        }
        if (get_option(self::OPTION_AWIN_PROGRAMME_GATE, null) === null) {
            update_option(self::OPTION_AWIN_PROGRAMME_GATE, array(), false);
        }
        if (get_option(self::OPTION_PARTNER_INTAKE, null) === null) {
            update_option(self::OPTION_PARTNER_INTAKE, array(), false);
        }
        if (get_option(self::OPTION_PARTNER_PROFILES, null) === null) {
            update_option(self::OPTION_PARTNER_PROFILES, array(), false);
        }
        if (get_option(self::OPTION_NETWORK_EBAY, null) === null) {
            update_option(self::OPTION_NETWORK_EBAY, self::instance()->ebay_settings_defaults(), false);
        }
        if (get_option(self::OPTION_EBAY_CURATION, null) === null) {
            update_option(self::OPTION_EBAY_CURATION, array('version'=>'1.0','items'=>array(),'sellers'=>array(),'brands'=>array(),'learned_heads'=>array()), false);
        }
        if (get_option(self::OPTION_EBAY_DELETION_STATE, null) === null) {
            update_option(self::OPTION_EBAY_DELETION_STATE, array(), false);
        }
        if (get_option(self::OPTION_EBAY_DELETION_RECEIPTS, null) === null) {
            update_option(self::OPTION_EBAY_DELETION_RECEIPTS, array(), false);
        }
        self::instance()->ebay_deletion_verification_token();
        if (get_option(self::OPTION_AUTOMATION_SETTINGS, null) === null) {
            update_option(self::OPTION_AUTOMATION_SETTINGS, self::automation_settings_defaults(), false);
        }
        if (get_option(self::OPTION_ASSIGNMENTS, null) === null) {
            update_option(self::OPTION_ASSIGNMENTS, array(), false);
        }
        if (get_option(self::OPTION_HEALTH_SETTINGS, null) === null) {
            update_option(self::OPTION_HEALTH_SETTINGS, self::health_defaults(), false);
        }
        if (get_option(self::OPTION_HEALTH_CURSOR, null) === null) {
            update_option(self::OPTION_HEALTH_CURSOR, 0, false);
        }
        if (get_option(self::OPTION_HEALTH_SCHEMA_VERSION, null) === null) {
            update_option(self::OPTION_HEALTH_SCHEMA_VERSION, self::HEALTH_SCHEMA_VERSION, false);
        }
        if (get_option(self::OPTION_ARTICLE_HYBRID, null) === null) {
            update_option(self::OPTION_ARTICLE_HYBRID, self::article_hybrid_defaults(), false);
        }
        if (get_option(self::OPTION_ARTICLE_PREVIEW, null) === null) {
            update_option(self::OPTION_ARTICLE_PREVIEW, self::article_preview_defaults(), false);
        }
        if (get_option(self::OPTION_ARTICLE_PLAN_REVISION, null) === null) {
            update_option(self::OPTION_ARTICLE_PLAN_REVISION, 1, false);
        }
        if (get_option(self::OPTION_ARTICLE_PLAN_LOG, null) === null) {
            update_option(self::OPTION_ARTICLE_PLAN_LOG, array(), false);
        }
        if (get_option(self::OPTION_ARTICLE_REBUILD_STATE, null) === null) {
            update_option(self::OPTION_ARTICLE_REBUILD_STATE, array('status'=>'idle'), false);
        }
        self::instance()->maybe_install_network_sync_schema();
        self::instance()->maybe_install_creative_library_schema();
        self::instance()->maybe_install_control_contract_schema();
        self::instance()->maybe_install_output_objects_schema();
        self::instance()->maybe_install_ebay_schema();
        self::instance()->maybe_install_automation_schema();
        self::instance()->maybe_apply_automation_safety_upgrade();
        self::instance()->maybe_cleanup_false_partner_creatives();
        self::instance()->reschedule_health_cron(true);
        self::instance()->reschedule_automation_cron(true);
        self::instance()->reschedule_ebay_cron(true);
        self::instance()->reschedule_ebay_refresh_cron(true);
        self::instance()->reschedule_ebay_maintenance_cron(true);
        self::instance()->reschedule_ebay_media_cleanup(true);
    }

    public static function deactivate() {
        if (function_exists('wp_clear_scheduled_hook')) {
            wp_clear_scheduled_hook(self::HEALTH_CRON_HOOK);
            wp_clear_scheduled_hook(self::AUTOMATION_CRON_HOOK);
            wp_clear_scheduled_hook(self::AUTOMATION_WORKER_HOOK);
            wp_clear_scheduled_hook(self::EBAY_CRON_HOOK);
            wp_clear_scheduled_hook(self::EBAY_WORKER_HOOK);
            wp_clear_scheduled_hook(self::EBAY_REFRESH_CRON_HOOK);
            wp_clear_scheduled_hook(self::EBAY_REFRESH_WORKER_HOOK);
            wp_clear_scheduled_hook(self::EBAY_MAINTENANCE_CRON_HOOK);
            wp_clear_scheduled_hook(self::EBAY_MEDIA_CLEANUP_HOOK);
        }
        // Absichtlich keine Daten löschen.
    }

    public function register_campaign_post_type() {
        register_post_type(self::CAMPAIGN_POST_TYPE, array(
            'labels' => array('name' => 'Affiliate-Kampagnen', 'singular_name' => 'Affiliate-Kampagne'),
            'public' => false,
            'show_ui' => false,
            'show_in_menu' => false,
            'show_in_rest' => false,
            'exclude_from_search' => true,
            'supports' => array('title'),
            'capability_type' => 'post',
            'map_meta_cap' => true,
        ));
    }

    /**
     * V2.7.1 – liefert reale Banner-/Produkt-Slots für die benutzerdefinierte
     * unterste Kategorieebene. Der Designcode übergibt die echte Term-ID; die
     * Auswahl, Prüfung und Ausgabe bleiben vollständig in der Affiliate-Zentrale.
     */
    public function provide_leaf_category_affiliate_slot_html($html, $term_id, $slot_type, $design_context = array()) {
        $term_id = absint($term_id);
        $slot_type = sanitize_key((string) $slot_type);
        $allowed = ($slot_type === 'product_after_category_tiles' || preg_match('/^category_product_[123]$/', $slot_type));
        if (!$allowed || $term_id <= 0 || !$this->is_enabled()) {
            return '';
        }
        if (is_array($design_context)) {
            $requested_contract = (string) ($design_context['contract'] ?? '');
            if ($requested_contract !== '' && $requested_contract !== self::CONTRACT_VERSION) {
                return '';
            }
        }
        $term = get_term($term_id, 'category');
        if (!$term || is_wp_error($term) || empty($term->term_id)) {
            return '';
        }
        $context = $this->get_category_archive_context($term);
        return $this->render_affiliate_slot_for_context(
            'term_' . $term_id,
            $context,
            $slot_type,
            'portal_context',
            ''
        );
    }

    /**
     * V2.7.2 – reale Banner-/Produkt-Slots für die tatsächlich live verwendeten
     * Leaf-SEITEN. Der Designcode übergibt die echte Seiten-ID; dadurch hängt
     * die Ausgabe nicht von einem zufälligen globalen Beitragsobjekt ab.
     */
    public function provide_leaf_page_affiliate_slot_html($html, $page_id, $slot_type, $design_context = array()) {
        $page_id = absint($page_id);
        $slot_type = sanitize_key((string) $slot_type);
        $allowed = ($slot_type === 'product_after_category_tiles' || preg_match('/^category_product_[123]$/', $slot_type));
        if (!$allowed || $page_id <= 0 || !$this->is_enabled()) {
            return '';
        }
        if (is_array($design_context)) {
            $requested_contract = (string) ($design_context['contract'] ?? '');
            if ($requested_contract !== '' && $requested_contract !== self::CONTRACT_VERSION) {
                return '';
            }
        }
        $post = get_post($page_id);
        if (!$post instanceof WP_Post || $post->post_type !== 'page' || $post->post_status !== 'publish') {
            return '';
        }
        $context = $this->get_content_context($page_id);
        return $this->render_affiliate_slot_for_context(
            $page_id,
            $context,
            $slot_type,
            'portal_context',
            ''
        );
    }

    /**
     * V2.7.4 – expliziter Banner-Slot für die HivePress-Anzeigenstartseite.
     * Das Designplugin übergibt die echte Seiten-ID; dadurch wird kein zufälliger
     * Loop-Beitrag als Kontext verwendet. Öffentlich wird ausschließlich eine
     * reale, aktive Bannerkampagne ausgegeben.
     */
    public function provide_market_affiliate_slot_html($html, $page_id, $slot_type, $design_context = array()) {
        $page_id = absint($page_id);
        $slot_type = sanitize_key((string) $slot_type);
        if ($slot_type !== 'anzeigenmarkt_top_banner' || $page_id <= 0 || !$this->is_enabled()) {
            return '';
        }
        if (is_array($design_context)) {
            $requested_contract = (string) ($design_context['contract'] ?? '');
            if ($requested_contract !== '' && $requested_contract !== self::CONTRACT_VERSION) {
                return '';
            }
        }
        $post = get_post($page_id);
        if (!$post instanceof WP_Post || $post->post_type !== 'page' || $post->post_status !== 'publish') {
            return '';
        }
        $context = $this->get_content_context($page_id);
        return $this->render_affiliate_slot_for_context(
            $page_id,
            $context,
            'anzeigenmarkt_top_banner',
            'portal_context',
            ''
        );
    }

    public function provide_integration_status($status, $requested_contract = '') {
        $requested_contract = (string) $requested_contract;
        $compatible = ($requested_contract === '' || $requested_contract === self::CONTRACT_VERSION);
        return array(
            'connected' => true,
            'compatible' => $compatible,
            'router_version' => self::VERSION,
            'contract' => self::CONTRACT_VERSION,
            'enabled' => $this->is_enabled(),
            'message' => $compatible
                ? ($this->is_enabled() ? 'Automatische Bannerzuordnung ist aktiv.' : 'Verbindung steht; die Affiliate-Automatik ist zentral deaktiviert.')
                : 'Schnittstellenversion passt nicht. Aus Sicherheitsgründen wird keine sechste Kachel ausgegeben.',
        );
    }

    public function enqueue_frontend_assets() {
        if (is_admin()) {
            return;
        }
        wp_enqueue_style(
            'ppar-frontend',
            plugins_url('assets/frontend.css', __FILE__),
            array(),
            self::VERSION
        );
        wp_enqueue_script(
            'ppar-frontend',
            plugins_url('assets/frontend.js', __FILE__),
            array(),
            self::VERSION,
            true
        );
        wp_localize_script('ppar-frontend', 'pparFrontend', array(
            'adminPreview' => current_user_can('manage_options'),
        ));

        // V6.61.16: Providerbezeichnung nach der spaeten Design-DOM-Transformation
        // korrigieren. Ausschliesslich Text; keinerlei Layout-/Provider-/Rankinglogik.
        if (function_exists('wp_add_inline_script')) {
            $cta_script = <<<'JS'
(function(){
  'use strict';
  function labelForHref(href){
    href=String(href||''); if(!href)return '';
    try{
      var u=new URL(href,window.location.href),h=String(u.hostname||'').toLowerCase();
      if(h==='ipn.idealo.de'||h.slice(-10)==='.idealo.de')return 'Bei idealo vergleichen';
      if(h==='ebay.de'||h.slice(-8)==='.ebay.de'||h.indexOf('.ebay.')!==-1)return 'Bei eBay ansehen';
    }catch(e){}
    return '';
  }
  function scan(root){
    var scope=root&&root.querySelectorAll?root:document;
    scope.querySelectorAll('[data-pftk-affiliate-cta-v150414="1"]').forEach(function(cta){
      var label=labelForHref(cta.getAttribute('href'));
      if(label&&cta.textContent!==label){cta.textContent=label;cta.setAttribute('data-ppar-provider-cta-v66116','1');}
    });
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',function(){scan(document);},{once:true});else scan(document);
  if(window.MutationObserver)new MutationObserver(function(mutations){
    mutations.forEach(function(m){Array.prototype.forEach.call(m.addedNodes||[],function(n){if(n&&n.nodeType===1){if(n.matches&&n.matches('[data-pftk-affiliate-cta-v150414="1"]'))scan(n.parentNode||document);else scan(n);}});});
  }).observe(document.documentElement,{childList:true,subtree:true});
})();
JS;
            wp_add_inline_script('ppar-frontend', $cta_script, 'after');
        }
    }

    public function register_shortcodes() {
        add_shortcode('pp_affiliate_slot', array($this, 'shortcode_affiliate_slot'));
        add_shortcode('affiliate_portal_slot', array($this, 'shortcode_affiliate_slot'));
        add_shortcode('pp_portal_overview', array($this, 'shortcode_portal_overview'));
        add_shortcode('affiliate_portal_overview', array($this, 'shortcode_portal_overview'));
    }

    public function filter_the_content($content) {
        // Search/autocomplete AJAX requests are lookup traffic, not affiliate
        // rendering requests. V6.19 could make Relevanssi/live-search process
        // hundreds of campaign objects while building result snippets.
        if ((function_exists('wp_doing_ajax') && wp_doing_ajax()) || (defined('DOING_AJAX') && DOING_AJAX)) {
            return $content;
        }
        $content = $this->auto_inject_template_affiliate_slots($content);
        if ($this->article_hybrid_enabled()) {
            return $this->auto_inject_article_hybrid($content);
        }
        $content = $this->auto_inject_affiliate_slots($content);
        return $content;
    }

    /**
     * Liefert dem Designplugin genau eine strukturierte sechste Hub-Kachel.
     * Die Auswahl bleibt vollständig im zentralen Router: Gruppe -> Kontextmatching ->
     * Slot hub_grid_card -> Bannerpriorität. Das Designplugin pflegt keine Bannerinhalte.
     */
    public function provide_hub_grid_affiliate_data($data, $type, $design_context) {
        $data = is_array($data) ? $data : array();
        $requested_contract = is_array($design_context) ? (string) ($design_context['contract'] ?? '') : '';
        if ($requested_contract !== self::CONTRACT_VERSION) {
            return array_merge($data, array(
                'active' => false,
                'valid' => false,
                'contract' => self::CONTRACT_VERSION,
                'source' => 'contract-mismatch',
            ));
        }
        if (!in_array((string) $type, array('hub1', 'hub2', 'category'), true)) {
            return array_merge($data, array('active' => false, 'valid' => false, 'contract' => self::CONTRACT_VERSION, 'source' => 'unsupported-template'));
        }
        $slot = ((string) $type === 'category') ? 'product_after_category_tiles' : 'hub_grid_card';
        $placement_index = is_array($design_context) ? max(1, min(2, (int) ($design_context['placement_index'] ?? 1))) : 1;
        $placement_mode = is_array($design_context) ? sanitize_key((string) ($design_context['placement_mode'] ?? 'grid')) : 'grid';
        $allow_placeholder = !is_array($design_context) || !array_key_exists('allow_placeholder', $design_context)
            ? true
            : !empty($design_context['allow_placeholder']);

        $post_id = is_array($design_context) && !empty($design_context['object_id']) ? (int) $design_context['object_id'] : (int) get_the_ID();
        if ($post_id <= 0) {
            return array_merge($data, array('active' => false, 'valid' => false, 'contract' => self::CONTRACT_VERSION, 'source' => 'router-no-object'));
        }

        // Eindeutiger, admin-only Funktionstest ohne gespeicherte Kampagne.
        $diagnostic_test = current_user_can('manage_options')
            && isset($_GET['affiliate_test_banner'])
            && sanitize_text_field(wp_unslash((string) $_GET['affiliate_test_banner'])) === '1';
        if ($diagnostic_test) {
            return array_merge($data, array(
                'active' => true,
                'valid' => true,
                'contract' => self::CONTRACT_VERSION,
                'router_version' => self::VERSION,
                'label' => 'Anzeige - Test',
                'title' => $placement_mode === 'leaf_category' ? 'Testbanner ' . $placement_index . ' fuer die Endkategorie' : 'Testbanner fuer das 3/3-Raster',
                'text' => 'Nur fuer angemeldete Administratoren und nur mit dem Testparameter sichtbar.',
                'button' => 'Test oeffnen',
                'image' => '',
                'url' => home_url('/'),
                'target' => '_self',
                'source' => 'diagnostic-test-banner-' . $placement_index,
                'kind' => 'campaign',
                'match_reason' => 'admin-only URL test mode',
            ));
        }

        $context = $this->get_content_context($post_id);
        $campaign = null;
        $reason = '';
        $source = '';

        // Vorschau einer konkreten Kampagne vor der Aktivierung. Nur Administratoren,
        // keine Speicherung und keine Wirkung fuer normale Besucher.
        $preview_id = current_user_can('manage_options') && isset($_GET['affiliate_preview_campaign'])
            ? absint($_GET['affiliate_preview_campaign'])
            : 0;
        if ($preview_id > 0 && $placement_index === 1) {
            $preview = $this->campaign_from_post(get_post($preview_id));
            if ($preview && $this->campaign_is_complete($preview) && $this->campaign_slot_allowed($preview, $slot)) {
                $campaign = $preview;
                $reason = 'Administrator-Vorschau';
                $source = 'campaign-preview-' . sanitize_key((string) ($preview['id'] ?? 'campaign'));
            }
        }

        if (!$campaign) {
            if (!$this->is_enabled()) {
                return $allow_placeholder
                    ? $this->hub_placeholder_or_inactive($data, $type, 'router-disabled', $placement_index)
                    : array_merge($data, array('active' => false, 'valid' => false, 'contract' => self::CONTRACT_VERSION, 'source' => 'router-disabled', 'kind' => 'none'));
            }
            $selection = $this->select_campaign_for_slot_position($context, $slot, $placement_index);
            if (!$selection || empty($selection['campaign'])) {
                return $allow_placeholder
                    ? $this->hub_placeholder_or_inactive($data, $type, 'router-no-campaign', $placement_index)
                    : array_merge($data, array('active' => false, 'valid' => false, 'contract' => self::CONTRACT_VERSION, 'source' => 'router-no-campaign-' . $placement_index, 'kind' => 'none'));
            }
            $campaign = $selection['campaign'];
            $reason = (string) ($selection['reason'] ?? '');
            // V2.2.19: Ein allgemeiner Fallback darf die zentral gepflegte
            // Partner-Vorschau in den strukturellen Rasterplaetzen nicht mit
            // einem historischen Kampagnenbild ueberdecken. Exakt zugeordnete,
            // bereichsbezogene oder keywordbasierte Kampagnen behalten Vorrang.
            $assignment_mode = sanitize_key((string) ($campaign['assignment_mode'] ?? 'page_tree'));
            if ($allow_placeholder && strpos($placement_mode, 'balanced_') === 0 && $assignment_mode === 'fallback') {
                return $this->hub_placeholder_or_inactive($data, $type, 'router-generic-fallback-replaced', $placement_index);
            }
            // V2.2.21: Das historisch dokumentierte Wolfblur-Platzhalterbild kann
            // noch als alte Kampagnen-Grafik in der Datenbank liegen. Es ist keine
            // echte Partnerkampagne und darf die aktuell gewählte zentrale Vorschau
            // in Hub 1/2 oder Ebene 3 nicht überdecken. Andere, gezielt zugeordnete
            // Kampagnen bleiben vollständig unangetastet.
            if ($allow_placeholder && strpos($placement_mode, 'balanced_') === 0 && $this->is_legacy_placeholder_campaign($campaign)) {
                return $this->hub_placeholder_or_inactive($data, $type, 'router-legacy-placeholder-replaced', $placement_index);
            }
            $source = 'campaign-' . sanitize_key((string) ($campaign['id'] ?? 'campaign'));
        }

        $creative = $this->build_campaign_output($campaign, $post_id, $context, $slot, $preview_id <= 0);
        if (!$creative || empty($creative['valid'])) {
            return $allow_placeholder
                ? $this->hub_placeholder_or_inactive($data, $type, 'router-invalid-campaign', $placement_index)
                : array_merge($data, array('active' => false, 'valid' => false, 'contract' => self::CONTRACT_VERSION, 'source' => 'router-invalid-campaign-' . $placement_index, 'kind' => 'none'));
        }

        return array_merge($data, array(
            'active' => true,
            'valid' => true,
            'contract' => self::CONTRACT_VERSION,
            'router_version' => self::VERSION,
            'label' => $creative['label'],
            'title' => $creative['title'],
            'text' => $creative['text'],
            'button' => $creative['button'],
            'image' => $creative['image'],
            'url' => $creative['url'],
            'target' => $creative['target'],
            'source' => $source,
            'kind' => 'campaign',
            'placement_index' => $placement_index,
            'placement_mode' => $placement_mode,
            'campaign_id' => sanitize_key((string) ($campaign['id'] ?? '')),
            'match_reason' => $reason,
        ));
    }


    /**
     * Erkennt ausschließlich das im Fehlerregister belegte historische
     * Platzhalterbild. Keine allgemeine Kampagne wird anhand von Vermutungen
     * ersetzt; echte Partnerbilder behalten Vorrang.
     */
    private function is_legacy_placeholder_campaign($campaign) {
        if (!is_array($campaign)) { return false; }
        $url = trim((string)($campaign['image_url'] ?? ''));
        if ($url === '') { return false; }
        $path = function_exists('wp_parse_url') ? wp_parse_url($url, PHP_URL_PATH) : parse_url($url, PHP_URL_PATH);
        $basename = strtolower(rawurldecode(basename((string)$path)));
        return strpos($basename, 'wolfblur-horses-1414889_1920') !== false;
    }

    private function hub_placeholder_or_inactive($data, $type, $inactive_source, $placement_index = 1) {
        $settings = $this->get_placeholder_settings();
        $placement_index = max(1, min(2, intval($placement_index)));
        if ((string) $type === 'category') {
            $enabled_key = 'category_enabled';
        } else {
            $enabled_key = (string) $type === 'hub1' ? 'hub1_enabled' : 'hub2_enabled';
        }
        // V2.2.17: Alle Platzierungen verwenden dieselben zentralen Bilder.
        $primary_key = 'start_image_id';
        $secondary_key = 'start_image_b_id';
        // Slot B verwendet Bild B. Ist B noch nicht gepflegt, bleibt Bild A der
        // rueckwaertskompatible Fallback, damit kein reservierter Platz leer bleibt.
        $image_key = $placement_index === 2 && $this->placeholder_attachment_url($settings, $secondary_key) !== ''
            ? $secondary_key
            : $primary_key;
        $image = $this->placeholder_image_url($settings, $image_key);
        if (!empty($settings['enabled']) && !empty($settings[$enabled_key]) && $image !== '') {
            return array_merge(is_array($data) ? $data : array(), array(
                'active' => true,
                'valid' => true,
                'contract' => self::CONTRACT_VERSION,
                'router_version' => self::VERSION,
                'label' => '',
                'title' => '',
                'text' => '',
                'button' => '',
                'image' => $image,
                'url' => (string) $settings['url'],
                'target' => (string) $settings['target'],
                'source' => 'placeholder-' . sanitize_key($type) . '-' . $placement_index,
                'kind' => 'placeholder',
                'is_placeholder' => true,
                'render_mode' => 'image_only',
                'placement_index' => $placement_index,
                'match_reason' => 'Kein passender echter Banner; zentraler Werbeplatz-Platzhalter ' . $placement_index . '.',
            ));
        }
        return array_merge(is_array($data) ? $data : array(), array(
            'active' => false,
            'valid' => false,
            'contract' => self::CONTRACT_VERSION,
            'router_version' => self::VERSION,
            'source' => sanitize_key($inactive_source) . '-' . $placement_index,
            'kind' => 'none',
            'placement_index' => $placement_index,
        ));
    }

    private function build_campaign_output($campaign, $post_id, $context, $slot, $track_click = true) {
        list($group, $banner) = $this->campaign_to_group_banner($campaign);
        if (!$group || !$banner) {
            return false;
        }
        $subid = $this->build_subid($post_id, $context, $group, $slot);
        $replacements = array(
            '{post_id}' => (string) $post_id,
            '{category_slug}' => (string) ($context['primary_slug'] ?? ''),
            '{category_name}' => (string) ($context['primary_name'] ?? ''),
            '{group_id}' => (string) ($group['id'] ?? ''),
            '{slot}' => $slot,
            '{subid}' => $subid,
        );
        $destination = strtr((string) ($banner['url'] ?? ''), $replacements);
        $destination = $this->apply_subid_to_url($destination, $subid, $banner['subid_param'] ?? '');
        if (method_exists($this, 'multiprovider_runtime_tracking_url')) { $destination = $this->multiprovider_runtime_tracking_url($destination, (string)($campaign['network'] ?? '')); }
        $image = strtr((string) ($banner['image_url'] ?? ''), $replacements);
        if (method_exists($this, 'multiprovider_runtime_image_url')) { $image = $this->multiprovider_runtime_image_url($image, (string)($campaign['network'] ?? ''), absint($campaign['post_id'] ?? 0)); }
        $title = strtr((string) ($banner['title'] ?? ''), $replacements);
        $text = strtr((string) ($banner['description'] ?? ''), $replacements);
        $button = strtr((string) ($banner['button_text'] ?? ''), $replacements);
        $label = trim((string) ($banner['label'] ?? '')) ?: 'Anzeige';
        // V2.2.4: Kachel-Slots sind verbindlich bildbasiert. Eine Kampagne ohne
        // Bild darf dort nicht als Textkachel erscheinen. Sie gilt fuer diesen Slot
        // als unvollstaendig; der Provider liefert anschliessend den zentralen
        // bild-only Platzhalter. Andere Banner-/Content-Slots bleiben unveraendert.
        $grid_slot = in_array((string) $slot, array('hub_grid_card', 'product_after_category_tiles'), true);
        $creative_complete = $grid_slot ? trim($image) !== '' : (trim($title) !== '' || trim($image) !== '');
        $valid = trim($destination) !== '' && $creative_complete;
        if (!$valid) {
            return false;
        }
        $url = $destination;
        $campaign_post_id = (int) ($campaign['post_id'] ?? 0);
        if ($track_click && $campaign_post_id > 0) {
            $url = $this->build_click_tracking_url($campaign_post_id, (int) $post_id, $slot);
        }
        return array(
            'valid' => true,
            'label' => $label,
            'title' => $title,
            'text' => $text,
            'button' => trim($button) !== '' ? $button : 'mehr erfahren',
            'image' => $image,
            'url' => $url,
            'destination' => $destination,
            'target' => (($banner['target'] ?? '_blank') === '_self') ? '_self' : '_blank',
        );
    }

    private function click_signature($campaign_post_id, $source_post_id, $slot) {
        $payload = absint($campaign_post_id) . '|' . absint($source_post_id) . '|' . sanitize_key($slot);
        return hash_hmac('sha256', $payload, wp_salt('auth'));
    }

    private function build_click_tracking_url($campaign_post_id, $source_post_id, $slot) {
        return add_query_arg(array(
            'affiliate_click' => '1',
            'campaign' => absint($campaign_post_id),
            'source' => absint($source_post_id),
            'slot' => sanitize_key($slot),
            'sig' => $this->click_signature($campaign_post_id, $source_post_id, $slot),
        ), home_url('/'));
    }

    public function handle_click_redirect() {
        if (empty($_GET['affiliate_click'])) {
            return;
        }
        $campaign_post_id = isset($_GET['campaign']) ? absint($_GET['campaign']) : 0;
        $source_post_id = isset($_GET['source']) ? absint($_GET['source']) : 0;
        $slot = isset($_GET['slot']) ? sanitize_key(wp_unslash((string) $_GET['slot'])) : '';
        $sig = isset($_GET['sig']) ? sanitize_text_field(wp_unslash((string) $_GET['sig'])) : '';
        if ($campaign_post_id <= 0 || $source_post_id <= 0 || $slot === '' || !hash_equals($this->click_signature($campaign_post_id, $source_post_id, $slot), $sig)) {
            wp_die('Ungueltiger Affiliate-Link.', 'Affiliate-Link', array('response' => 400));
        }
        $campaign = $this->campaign_from_post(get_post($campaign_post_id));
        if (!$campaign || empty($campaign['active']) || !$this->campaign_is_complete($campaign) || !$this->rule_is_current($campaign) || !$this->campaign_program_allows_delivery($campaign) || !$this->campaign_control_allows_delivery($campaign, $slot) || !$this->campaign_health_allows_delivery($campaign) || !$this->campaign_slot_allowed($campaign, $slot)) {
            wp_die('Dieses Angebot ist nicht mehr aktiv.', 'Affiliate-Link', array('response' => 410));
        }
        $context = $this->get_content_context($source_post_id);
        $creative = $this->build_campaign_output($campaign, $source_post_id, $context, $slot, false);
        if (!$creative || empty($creative['destination'])) {
            wp_die('Das Ziel dieses Angebots ist nicht verfuegbar.', 'Affiliate-Link', array('response' => 410));
        }
        $this->record_campaign_click($campaign_post_id, $source_post_id, $slot);
        do_action('affiliate_portal_click_tracked', array(
            'campaign_post_id' => $campaign_post_id,
            'campaign_id' => (string) ($campaign['id'] ?? ''),
            'source_post_id' => $source_post_id,
            'slot' => $slot,
        ));
        nocache_headers();
        wp_redirect(esc_url_raw($creative['destination']), 302, 'Affiliate-Zentrale');
        exit;
    }

    private function record_campaign_click($campaign_post_id, $source_post_id, $slot) {
        $total = (int) get_post_meta($campaign_post_id, 'ppar_click_total', true);
        update_post_meta($campaign_post_id, 'ppar_click_total', $total + 1);

        $daily = get_post_meta($campaign_post_id, 'ppar_click_daily', true);
        $daily = is_array($daily) ? $daily : array();
        $day = current_time('Y-m-d');
        $daily[$day] = isset($daily[$day]) ? (int) $daily[$day] + 1 : 1;
        ksort($daily);
        if (count($daily) > 120) {
            $daily = array_slice($daily, -120, null, true);
        }
        update_post_meta($campaign_post_id, 'ppar_click_daily', $daily);

        $slots = get_post_meta($campaign_post_id, 'ppar_click_slots', true);
        $slots = is_array($slots) ? $slots : array();
        $slot = sanitize_key($slot);
        $slots[$slot] = isset($slots[$slot]) ? (int) $slots[$slot] + 1 : 1;
        update_post_meta($campaign_post_id, 'ppar_click_slots', $slots);

        $pages = get_post_meta($campaign_post_id, 'ppar_click_pages', true);
        $pages = is_array($pages) ? $pages : array();
        $key = (string) absint($source_post_id);
        $pages[$key] = isset($pages[$key]) ? (int) $pages[$key] + 1 : 1;
        arsort($pages);
        if (count($pages) > 100) {
            $pages = array_slice($pages, 0, 100, true);
        }
        update_post_meta($campaign_post_id, 'ppar_click_pages', $pages);
    }

    private function campaign_click_total($campaign) {
        $post_id = (int) ($campaign['post_id'] ?? 0);
        return $post_id > 0 ? (int) get_post_meta($post_id, 'ppar_click_total', true) : 0;
    }

    private function campaign_click_last_days($campaign, $days = 30) {
        $post_id = (int) ($campaign['post_id'] ?? 0);
        if ($post_id <= 0) {
            return 0;
        }
        $daily = get_post_meta($post_id, 'ppar_click_daily', true);
        if (!is_array($daily)) {
            return 0;
        }
        $min = strtotime('-' . max(1, (int) $days - 1) . ' days', current_time('timestamp'));
        $sum = 0;
        foreach ($daily as $date => $count) {
            $ts = strtotime((string) $date);
            if ($ts !== false && $ts >= $min) {
                $sum += (int) $count;
            }
        }
        return $sum;
    }

    /* ---------------------------------------------------------------------
     * Affiliate-Router fuer Beitraege
     * ------------------------------------------------------------------ */

    public function shortcode_affiliate_slot($atts) {
        $atts = shortcode_atts(array(
            'type' => 'mid_content',
            'intent' => 'primary_product',
            'group' => '',
        ), $atts, 'pp_affiliate_slot');

        $post_id = get_the_ID();
        if (!$post_id) {
            return '';
        }

        return $this->render_affiliate_slot($post_id, sanitize_key($atts['type']), sanitize_key($atts['intent']), sanitize_key($atts['group']));
    }

    private static function article_hybrid_defaults() {
        return array(
            'enabled' => true,
        );
    }

    private function article_hybrid_settings() {
        $saved = get_option(self::OPTION_ARTICLE_HYBRID, array());
        $saved = is_array($saved) ? $saved : array();
        return array(
            'enabled' => !empty($saved['enabled']),
        );
    }

    private function article_hybrid_enabled() {
        $settings = $this->article_hybrid_settings();
        return $this->is_enabled() && !empty($settings['enabled']);
    }


    /**
     * V6.36: article product delivery is part of the normal automated portal
     * workflow. Older installs inherited the historical opt-in default=false,
     * which meant a fully supplied BUSINESS catalog could still render zero
     * products in every article. Enable it once on upgrade, queue the plans, and
     * then respect any later explicit administrator change normally.
     */
    public function maybe_apply_article_products_upgrade() {
        $done = (string) get_option(self::OPTION_ARTICLE_PRODUCTS_UPGRADE, '');
        if ($done === '6.36.0') { return false; }
        $settings = get_option(self::OPTION_ARTICLE_HYBRID, array());
        $settings = is_array($settings) ? $settings : array();
        $settings['enabled'] = true;
        update_option(self::OPTION_ARTICLE_HYBRID, $settings, false);
        update_option(self::OPTION_ARTICLE_PRODUCTS_UPGRADE, '6.36.0', false);
        if (method_exists($this, 'article_plan_rebuild_request')) {
            $this->article_plan_rebuild_request('v636_article_products_upgrade', $this->article_plan_campaign_revision());
        }
        return true;
    }


    private static function article_preview_defaults() {
        return array(
            'enabled' => false,
            'post_id' => 0,
            'banner_campaign_ids' => array(),
            'product_campaign_ids' => array(),
            'product_preview_count' => 3,
        );
    }

    private function article_preview_settings() {
        $saved = get_option(self::OPTION_ARTICLE_PREVIEW, array());
        $saved = is_array($saved) ? $saved : array();
        $settings = wp_parse_args($saved, self::article_preview_defaults());
        $settings['enabled'] = !empty($settings['enabled']);
        $settings['post_id'] = absint($settings['post_id'] ?? 0);
        $settings['banner_campaign_ids'] = array_slice(array_values(array_filter(array_map('absint', (array)($settings['banner_campaign_ids'] ?? array())))), 0, 1);
        $settings['product_campaign_ids'] = array_slice(array_values(array_filter(array_map('absint', (array)($settings['product_campaign_ids'] ?? array())))), 0, 3);
        $settings['product_preview_count'] = max(0, min(3, absint($settings['product_preview_count'] ?? 3)));
        return $settings;
    }

    private function article_preview_for_post($post_id) {
        if (!current_user_can('manage_options')) {
            return null;
        }
        $settings = $this->article_preview_settings();
        if (empty($settings['enabled']) || absint($settings['post_id']) !== absint($post_id)) {
            return null;
        }
        return $settings;
    }

    private function article_preview_campaign_choices($creative_type) {
        $creative_type = $creative_type === 'product' ? 'product' : 'banner';
        $choices = array();
        foreach ($this->get_campaigns() as $campaign) {
            if (!is_array($campaign) || sanitize_key((string)($campaign['creative_type'] ?? 'banner')) !== $creative_type) {
                continue;
            }
            if (!$this->campaign_is_complete($campaign)) {
                continue;
            }
            $post_id = absint($campaign['post_id'] ?? 0);
            if ($post_id <= 0) {
                continue;
            }
            $choices[$post_id] = (string)($campaign['name'] ?? $campaign['title'] ?? ('Werbemittel ' . $post_id));
        }
        natcasesort($choices);
        return $choices;
    }

    private function article_normal_placement_count($creative_type, $slot_type) {
        $creative_type = $creative_type === 'product' ? 'product' : 'banner';
        $count = 0;
        foreach ($this->get_campaigns() as $campaign) {
            if (!is_array($campaign) || empty($campaign['active'])) {
                continue;
            }
            if (sanitize_key((string)($campaign['creative_type'] ?? 'banner')) !== $creative_type) {
                continue;
            }
            if (!$this->campaign_is_complete($campaign) || !$this->rule_is_current($campaign) || !$this->campaign_program_allows_delivery($campaign) || !$this->campaign_control_allows_delivery($campaign, $slot_type ?? '') || !$this->campaign_health_allows_delivery($campaign)) {
                continue;
            }
            if (!$this->campaign_slot_allowed($campaign, $slot_type)) {
                continue;
            }
            $count++;
        }
        return $count;
    }

    /**
     * Unicode-feste Wortzählung für deutschsprachige Beiträge.
     */
    private function article_word_count($content) {
        $text = strip_shortcodes((string) $content);
        $text = html_entity_decode(wp_strip_all_tags($text), ENT_QUOTES | ENT_HTML5, 'UTF-8');
        if (!preg_match_all('/[\p{L}\p{N}]+(?:[\'’\-][\p{L}\p{N}]+)*/u', $text, $matches)) {
            return 0;
        }
        return count($matches[0]);
    }

    /**
     * Verbindliche Obergrenze: pro Beitrag höchstens eine Banneranzeige.
     * Die Wortzahl erhöht die Bannerzahl nicht.
     */
    private function article_banner_limit_for_words($word_count) {
        return 1;
    }

    /**
     * Prüft den abgeschlossenen redaktionellen Inhalt unmittelbar vor einer
     * neuen Zwischenüberschrift. Generierte Artikel umschließen jeden Block
     * mit <section>. Diese strukturellen Schluss-Tags werden für die Prüfung
     * entfernt; Tabellen-/Listen-/Div-Enden bleiben bewusst bestehen und
     * sperren die Einfügung.
     */
    private function article_section_ends_with_paragraph($section_html) {
        $section_html = (string) $section_html;
        do {
            $before = $section_html;
            $section_html = preg_replace('/(?:\s|<!--.*?-->)+$/is', '', $section_html);
            $section_html = preg_replace('/<\/(?:section|article)>\s*$/is', '', $section_html);
        } while ($section_html !== $before);
        if ($section_html === '' || !preg_match('/(<p\b[^>]*>.*?<\/p>)$/is', $section_html, $match)) {
            return false;
        }
        $text = trim(wp_strip_all_tags(preg_replace('/<!--.*?-->/s', '', (string) $match[1])));
        return $text !== '';
    }

    /**
     * Bestimmt die echte Strukturgrenze vor der nächsten Überschrift.
     * Liegt die Überschrift am Anfang eines neuen <section>-Blocks, wird VOR
     * dessen öffnendem Tag eingefügt. Dadurch landet das Banner niemals
     * innerhalb des neuen Abschnitts zwischen <section> und <h2>/<h3>.
     */
    private function article_boundary_before_heading($content, $previous_heading_end, $heading_start) {
        $content = (string) $content;
        $previous_heading_end = max(0, (int) $previous_heading_end);
        $heading_start = max($previous_heading_end, (int) $heading_start);
        $between = substr($content, $previous_heading_end, $heading_start - $previous_heading_end);
        if (preg_match('/<section\b[^>]*>\s*$/is', $between, $match, PREG_OFFSET_CAPTURE)) {
            return array(
                'offset' => $previous_heading_end + (int) $match[0][1],
                'mode' => 'before_section',
            );
        }
        return array(
            'offset' => $heading_start,
            'mode' => 'before_heading',
        );
    }

    private function article_heading_is_excluded($heading_text) {
        return preg_match('/\b(?:fazit|zusammenfassung|quellen|faq|häufige\s+fragen|ähnliche\s+beiträge)\b/ui', (string) $heading_text) === 1;
    }

    /**
     * Sammelt sichere Abschnittsgrenzen. Es wird niemals innerhalb eines
     * Fließtextblocks und niemals zwischen Überschrift und Tabelle/Liste
     * eingefügt. Kandidat ist ausschließlich der Beginn einer späteren H2.
     */
    private function article_h2_insertion_candidates($content) {
        $content = (string) $content;
        $length = strlen($content);
        if ($length <= 0 || !preg_match_all('/<h([23])\b[^>]*>(.*?)<\/h\1>/is', $content, $headings, PREG_SET_ORDER | PREG_OFFSET_CAPTURE)) {
            return array();
        }
        $candidates = array();
        $count = count($headings);
        // Nie vor der ersten Zwischenüberschrift: Die Einleitung bleibt werbefrei.
        for ($i = 1; $i < $count; $i++) {
            $previous_markup = (string) $headings[$i - 1][0][0];
            $previous_start = (int) $headings[$i - 1][0][1];
            $previous_end = $previous_start + strlen($previous_markup);
            $previous_level = (int) $headings[$i - 1][1][0];
            $previous_text = trim(wp_strip_all_tags((string) $headings[$i - 1][2][0]));

            $next_start = (int) $headings[$i][0][1];
            $next_level = (int) $headings[$i][1][0];
            $next_text = trim(wp_strip_all_tags((string) $headings[$i][2][0]));
            if ($previous_text === '' || $next_text === '' || $this->article_heading_is_excluded($previous_text) || $this->article_heading_is_excluded($next_text)) {
                continue;
            }

            $boundary = $this->article_boundary_before_heading($content, $previous_end, $next_start);
            $boundary_offset = (int) ($boundary['offset'] ?? $next_start);
            if ($boundary_offset <= $previous_end || $boundary_offset > $next_start) {
                continue;
            }
            $section = substr($content, $previous_end, $boundary_offset - $previous_end);
            if (!$this->article_section_ends_with_paragraph($section)) {
                continue;
            }
            $ratio = $length > 0 ? $boundary_offset / $length : 0;
            $candidates[] = array(
                'offset' => $boundary_offset,
                'heading_offset' => $next_start,
                'boundary_mode' => sanitize_key((string) ($boundary['mode'] ?? 'before_heading')),
                'ratio' => $ratio,
                'heading' => $next_text,
                'heading_level' => $next_level,
                'previous_heading' => $previous_text,
                'previous_heading_level' => $previous_level,
            );
        }
        return $candidates;
    }

    private function nearest_article_candidate($candidates, $target, $min_ratio = 0.0, $max_ratio = 1.0) {
        $best = null;
        $best_distance = PHP_FLOAT_MAX;
        foreach ((array) $candidates as $candidate) {
            $ratio = (float) ($candidate['ratio'] ?? 0);
            if ($ratio < $min_ratio || $ratio > $max_ratio) {
                continue;
            }
            $distance = abs($ratio - (float) $target);
            if ($distance < $best_distance) {
                $best = $candidate;
                $best_distance = $distance;
            }
        }
        return $best;
    }

    /**
     * Höchstens ein Banner liegt an einer sicheren Abschnittsgrenze ungefähr
     * in der Artikelmitte.
     */
    private function select_article_insertion_positions($content, $limit) {
        if ((int) $limit <= 0) {
            return array();
        }
        $candidates = $this->article_h2_insertion_candidates($content);
        if (empty($candidates)) {
            return array();
        }
        $one = $this->nearest_article_candidate($candidates, 0.50, 0.0, 1.0);
        return $one ? array($one) : array();
    }

    /**
     * Hilfsfunktionen für die einzige zulässige Inline-Bannerposition.
     */
    private function article_banner_dimensions($banner) {
        $raw = trim((string)($banner['dimensions'] ?? ''));
        if ($raw !== '' && preg_match('/(\d{2,4})\s*[x×X]\s*(\d{2,4})/u', $raw, $m)) {
            return array(max(1, (int)$m[1]), max(1, (int)$m[2]), 'dimensions');
        }

        $html = (string)($banner['html'] ?? '');
        if ($html !== '') {
            // Breite/Höhe dürfen in beliebiger Attributreihenfolge stehen.
            if (preg_match('/<(?:img|iframe)\b([^>]*)>/is', $html, $tag)) {
                $attrs = (string)$tag[1];
                $width = 0;
                $height = 0;
                if (preg_match('/\bwidth\s*=\s*["\']?(\d{2,4})/i', $attrs, $m)) {
                    $width = (int)$m[1];
                }
                if (preg_match('/\bheight\s*=\s*["\']?(\d{2,4})/i', $attrs, $m)) {
                    $height = (int)$m[1];
                }
                if (($width <= 0 || $height <= 0) && preg_match('/\bstyle\s*=\s*["\']([^"\']+)["\']/i', $attrs, $m)) {
                    $style = (string)$m[1];
                    if ($width <= 0 && preg_match('/(?:^|;)\s*width\s*:\s*(\d{2,4})px/i', $style, $sm)) {
                        $width = (int)$sm[1];
                    }
                    if ($height <= 0 && preg_match('/(?:^|;)\s*height\s*:\s*(\d{2,4})px/i', $style, $sm)) {
                        $height = (int)$sm[1];
                    }
                }
                if ($width > 0 && $height > 0) {
                    return array($width, $height, 'html');
                }
            }
        }

        return array(728, 90, 'fallback');
    }

    /**
     * Administrator-Test: ausschließlich eine leere, dimensionsgetreue Fläche.
     * Kein Bild, kein Titel, kein Hinweis, kein Werbetext.
     */
    private function render_article_banner_test_surface($banner, $position) {
        list($width, $height, $dimension_source) = $this->article_banner_dimensions($banner);
        // Ausschließlich dokumentierte Creative-Maße oder HTML-Maße sind verbindlich.
        // Die natürliche Größe einer image_url ist kein belastbarer Bannermaß-Beleg
        // und darf die Prüffläche niemals nachträglich überschreiben.
        $style = '--ppar-test-banner-width:' . $width . 'px;--ppar-test-banner-ratio:' . $width . ' / ' . $height . ';';
        $out = '<div class="ppar-article-inline-banner ppar-article-banner-test-wrap" data-ppar-banner-position="1">';
        $out .= '<div class="ppar-article-banner-test-surface" style="' . esc_attr($style) . '"';
        $out .= ' data-ppar-banner-width="' . (int)$width . '"';
        $out .= ' data-ppar-banner-height="' . (int)$height . '"';
        $out .= ' data-ppar-dimension-source="' . esc_attr($dimension_source) . '"';
        $out .= '></div></div>';
        return $out;
    }

    private function render_article_banner_at_position($post_id, $position, $forced_campaign_post_id = 0) {
        $position = 1;
        $slot_type = 'post_inline_banner';
        $context = $this->get_content_context($post_id);
        $forced_campaign_post_id = absint($forced_campaign_post_id);
        $is_admin_test = $forced_campaign_post_id > 0 && current_user_can('manage_options');
        if ($is_admin_test) {
            $campaign = $this->campaign_from_post(get_post($forced_campaign_post_id));
            if (!$campaign || sanitize_key((string)($campaign['creative_type'] ?? 'banner')) !== 'banner' || !$this->campaign_is_complete($campaign)) {
                return '';
            }
        } else {
            $assigned = $this->assignment_selection_for_slot($context, $slot_type);
            if (!empty($assigned['handled'])) {
                if (!empty($assigned['disabled'])) {
                    return '';
                }
                $selection = $assigned['selection'] ?? null;
            } else {
                $selection = $this->select_campaign_for_slot_position($context, $slot_type, $position);
            }
            if (!$selection || empty($selection['campaign'])) {
                return '';
            }
            $campaign = $selection['campaign'];
        }
        list($group, $banner) = $this->campaign_to_group_banner($campaign);
        if (!$group || !$banner) {
            return '';
        }
        if ($is_admin_test) {
            return $this->render_article_banner_test_surface($banner, $position);
        }
        $campaign_post_id = (int) ($campaign['post_id'] ?? 0);
        if ($campaign_post_id > 0) {
            $banner['url'] = $this->build_click_tracking_url($campaign_post_id, (int) $post_id, $slot_type);
        }
        $html = $this->render_banner($banner, $post_id, $context, $group, $slot_type);
        if (trim((string) $html) === '') {
            return '';
        }
        $classes = array(
            'ppar-affiliate-slot',
            'ppar-slot-post_inline_banner',
            'ppar-article-inline-banner',
            'ppar-article-inline-banner-' . $position,
        );
        if (!empty($group['id'])) {
            $classes[] = 'ppar-group-' . sanitize_html_class($group['id']);
        }
        $label = !empty($banner['label']) ? sanitize_text_field($banner['label']) : '';
        $out = '<div class="' . esc_attr(implode(' ', $classes)) . '" data-ppar-slot="post_inline_banner" data-ppar-banner-position="' . $position . '">';
        $out .= $this->get_disclosure_html($post_id);
        if ($label !== '') {
            $out .= '<div class="ppar-affiliate-label">' . esc_html($label) . '</div>';
        }
        $out .= '<div class="ppar-affiliate-content">' . $html . '</div></div>';
        return $out . $this->debug_comment('affiliate_rendered', $post_id, $slot_type, $group['id'] ?? '', $banner['id'] ?? '');
    }

    private function render_article_product_block($post_id, $forced_campaign_post_ids = array(), $preview_count = 0) {
        $context = $this->get_content_context($post_id);
        $forced_campaign_post_ids = array_slice(array_values(array_filter(array_map('absint', (array)$forced_campaign_post_ids))), 0, 3);
        $preview_count = max(0, min(3, (int)$preview_count));
        $is_admin_test = current_user_can('manage_options') && $preview_count > 0;
        $campaigns = array();
        if (!empty($forced_campaign_post_ids) && current_user_can('manage_options')) {
            foreach ($forced_campaign_post_ids as $campaign_post_id) {
                $campaign = $this->campaign_from_post(get_post($campaign_post_id));
                if ($campaign && sanitize_key((string)($campaign['creative_type'] ?? 'banner')) === 'product' && $this->campaign_is_complete($campaign)) {
                    $campaigns[] = $campaign;
                }
            }
        } else {
            foreach (array_slice($this->ranked_campaigns_for_slot($context, 'post_bottom_products'), 0, 3) as $candidate) {
                if (!empty($candidate['campaign'])) {
                    $campaigns[] = $candidate['campaign'];
                }
            }
        }
        $cards = array();
        foreach ($campaigns as $campaign) {
            list($group, $banner) = $this->campaign_to_group_banner($campaign);
            if (!$group || !$banner) {
                continue;
            }
            $campaign_post_id = (int) ($campaign['post_id'] ?? 0);
            if ($campaign_post_id > 0) {
                $banner['url'] = $this->build_click_tracking_url($campaign_post_id, (int) $post_id, 'post_bottom_products');
            }
            $html = $this->article_plan_render_product_card_markup($banner, $post_id, $context, $group, 'post_bottom_products');
            if ($html !== '') {
                $cards[] = '<div class="ppar-article-product-card">' . $html . '</div>';
            }
        }
        if ($is_admin_test && count($cards) < $preview_count) {
            while (count($cards) < $preview_count) {
                $cards[] = '<div class="ppar-article-product-card ppar-article-product-test-surface" aria-hidden="true"></div>';
            }
        }
        if (empty($cards)) {
            return '';
        }
        $count = count($cards);
        $out = '<section class="ppar-article-product-block" data-ppar-product-count="' . $count . '">';
        if (!$is_admin_test) {
            $out .= $this->get_disclosure_html($post_id);
        }
        $out .= '<div class="ppar-article-section-label">Produktvorschläge</div>';
        $out .= '<div class="ppar-article-product-grid ppar-article-product-count-' . $count . '">' . implode('', $cards) . '</div></section>';
        return $out;
    }

    private function insert_at_offset($content, $insertion, $offset) {
        if (trim((string) $insertion) === '' || $offset <= 0 || $offset >= strlen($content)) {
            return $content;
        }
        return substr($content, 0, $offset) . "\n" . $insertion . "\n" . substr($content, $offset);
    }

    public function auto_inject_article_hybrid($content) {
        if (!$this->article_hybrid_enabled()) {
            return $content;
        }
        if (is_admin() || is_feed() || is_preview()) {
            return $content;
        }
        if (!is_singular('post') || !in_the_loop() || !is_main_query()) {
            return $content;
        }
        $post_id = get_the_ID();
        if (!$post_id || post_password_required($post_id)) {
            return $content;
        }
        $raw_post_content = (string) get_post_field('post_content', $post_id);
        if (has_shortcode($raw_post_content, 'pp_affiliate_slot') || has_shortcode($raw_post_content, 'affiliate_portal_slot')) {
            return $content;
        }
        return $this->article_plan_apply_to_content((string) $content, (int) $post_id);
    }

    public function auto_inject_affiliate_slots($content) {
        if (!$this->is_enabled()) {
            return $content;
        }
        if (is_admin() || is_feed() || is_preview()) {
            return $content;
        }
        if (!is_singular('post') || !in_the_loop() || !is_main_query()) {
            return $content;
        }

        $post_id = get_the_ID();
        if (!$post_id || post_password_required($post_id)) {
            return $content;
        }

        $auto_slots = $this->get_auto_slots();
        if (empty($auto_slots)) {
            return $content;
        }

        // Wenn der Beitrag bereits bewusst Slots enthält, keine Auto-Dopplung erzwingen.
        $raw_post_content = (string) get_post_field('post_content', $post_id);
        if (has_shortcode($raw_post_content, 'pp_affiliate_slot') || has_shortcode($raw_post_content, 'affiliate_portal_slot')) {
            return $content;
        }

        $result = $content;

        if ($this->auto_slot_enabled($auto_slots, array('post_after_intro', 'top_info'))) {
            $slot_type = in_array('post_after_intro', $auto_slots, true) ? 'post_after_intro' : 'top_info';
            $slot = $this->render_affiliate_slot($post_id, $slot_type, 'soft_hint', '');
            if ($slot !== '') {
                $result = $this->insert_after_paragraph($result, $slot, 1);
            }
        }

        if ($this->auto_slot_enabled($auto_slots, array('post_mid_content', 'mid_content'))) {
            $slot_type = in_array('post_mid_content', $auto_slots, true) ? 'post_mid_content' : 'mid_content';
            $slot = $this->render_affiliate_slot($post_id, $slot_type, 'primary_product', '');
            if ($slot !== '') {
                $paragraph_count = substr_count(strtolower($result), '</p>');
                $position = max(2, min(5, (int) ceil($paragraph_count * 0.35)));
                $result = $this->insert_after_paragraph($result, $slot, $position);
            }
        }

        if ($this->auto_slot_enabled($auto_slots, array('post_bottom_recommendation', 'bottom_recommendation'))) {
            $slot_type = in_array('post_bottom_recommendation', $auto_slots, true) ? 'post_bottom_recommendation' : 'bottom_recommendation';
            $slot = $this->render_affiliate_slot($post_id, $slot_type, 'primary_product', '');
            if ($slot !== '') {
                $result .= "\n" . $slot;
            }
        }

        return $result;
    }

    public function auto_inject_category_archive_slots($query) {
        if (!$this->is_enabled() || !$this->is_category_archive_enabled()) {
            return;
        }
        if (is_admin() || is_feed() || is_preview()) {
            return;
        }
        if (!is_category() || !($query instanceof WP_Query) || !$query->is_main_query()) {
            return;
        }

        $slots = $this->get_category_slots();
        if (empty($slots)) {
            return;
        }

        $term = get_queried_object();
        if (!$term || empty($term->term_id) || empty($term->slug)) {
            return;
        }

        // V2.7.3 – besitzt das Designplugin auf der untersten Kategorieebene
        // bereits die feste Positionshoheit, darf die alte Loop-End-Ausgabe
        // keinerlei zweiten oder falsch positionierten Block anhaengen.
        $design_owns_slots = (bool) apply_filters(
            'pftk_leaf_category_design_owns_affiliate_slots',
            false,
            (int) $term->term_id
        );
        if ($design_owns_slots) {
            return;
        }

        $context = $this->get_category_archive_context($term);
        foreach ($slots as $slot_type) {
            $html = $this->render_affiliate_slot_for_context('term_' . (int) $term->term_id, $context, $slot_type, 'primary_product', '');
            if (trim($html) !== '') {
                echo "\n" . $html . "\n";
            }
        }
    }

    private function render_affiliate_slot($post_id, $slot_type, $intent, $forced_group_id = '') {
        $context = $this->get_content_context($post_id);
        return $this->render_affiliate_slot_for_context($post_id, $context, $slot_type, $intent, $forced_group_id);
    }
    private function get_assignments() {
        $value = get_option(self::OPTION_ASSIGNMENTS, array());
        return is_array($value) ? $value : array();
    }

    private function assignment_for_context($context) {
        $post_id = absint($context['post_id'] ?? 0);
        if ($post_id <= 0) { return null; }
        $all = $this->get_assignments();
        if (!empty($all[$post_id]) && is_array($all[$post_id])) { return array('data'=>$all[$post_id],'source_id'=>$post_id,'source'=>'direkt'); }
        foreach ((array)($context['ancestor_ids'] ?? array()) as $ancestor_id) {
            $ancestor_id = absint($ancestor_id);
            if ($ancestor_id > 0 && !empty($all[$ancestor_id]['apply_descendants'])) {
                return array('data'=>$all[$ancestor_id],'source_id'=>$ancestor_id,'source'=>'vererbt');
            }
        }
        return null;
    }

    private function fixed_campaign_selection($post_id, $slot_type, $reason) {
        $campaign = $post_id > 0 ? $this->campaign_from_post(get_post($post_id)) : null;
        if (!$campaign || empty($campaign['active']) || !$this->campaign_is_complete($campaign) || !$this->rule_is_current($campaign) || !$this->campaign_program_allows_delivery($campaign) || !$this->campaign_source_allows_delivery($campaign) || !$this->campaign_control_allows_delivery($campaign, $slot_type) || !$this->campaign_health_allows_delivery($campaign)) { return null; }
        $required = $this->slot_required_creative_type($slot_type);
        if ($required !== '' && sanitize_key((string)($campaign['creative_type'] ?? 'banner')) !== $required) { return null; }
        if ($required === 'product' && !$this->product_campaign_public_image_ready($campaign)) { return null; }
        return array('campaign'=>$campaign,'specificity'=>1000,'matches'=>1,'priority'=>1000,'reason'=>$reason);
    }

    private function assignment_selection_for_slot($context, $slot_type) {
        $found = $this->assignment_for_context($context);
        if (!$found) { return array('handled'=>false); }
        $data = $found['data'];
        $suffix = $found['source'] . ' von „' . get_the_title((int)$found['source_id']) . '“';
        if ($this->slot_required_creative_type($slot_type) === 'banner') {
            $mode = sanitize_key((string)($data['banner_mode'] ?? 'automatic'));
            if ($mode === 'none') { return array('handled'=>true,'disabled'=>true,'reason'=>'Banner ausdrücklich deaktiviert (' . $suffix . ').'); }
            if ($mode === 'fixed') {
                return array('handled'=>true,'selection'=>$this->fixed_campaign_selection(absint($data['banner_id'] ?? 0), $slot_type, 'Fest zugeordnet, ' . $suffix . '.'));
            }
        }
        if ($this->slot_required_creative_type($slot_type) === 'product') {
            $mode = sanitize_key((string)($data['products_mode'] ?? 'automatic'));
            if ($mode === 'none') { return array('handled'=>true,'disabled'=>true,'reason'=>'Produkte ausdrücklich deaktiviert (' . $suffix . ').'); }
            if ($mode === 'fixed') {
                $index = max(1, $this->category_product_slot_index($slot_type));
                $ids = array_slice(array_pad(array_map('absint', array_values((array)($data['product_ids'] ?? array()))), 3, 0), 0, 3);
                if (method_exists($this, 'ebay_product_campaigns_share_provider_cohort')) {
                    $fixed_campaigns = array();
                    foreach (array_filter($ids) as $fixed_id) {
                        $fixed_campaign = $this->campaign_from_post(get_post($fixed_id));
                        if (is_array($fixed_campaign) && sanitize_key((string) ($fixed_campaign['creative_type'] ?? '')) === 'product') { $fixed_campaigns[] = $fixed_campaign; }
                    }
                    if (!$this->ebay_product_campaigns_share_provider_cohort($fixed_campaigns)) {
                        return array('handled'=>true,'disabled'=>true,'reason'=>'Feste Produktzuordnung mischt eBay- und Nicht-eBay-Inhalte; Ausgabe blockiert (' . $suffix . ').');
                    }
                }
                $id = $ids[$index-1] ?? 0;
                return array('handled'=>true,'selection'=>$this->fixed_campaign_selection($id, $slot_type, 'Produktposition ' . $index . ' fest zugeordnet, ' . $suffix . '.'));
            }
        }
        return array('handled'=>false);
    }
    private function render_affiliate_slot_for_context($content_id, $context, $slot_type, $intent, $forced_group_id = '') {
        if ($this->is_enabled()) {
            $assigned = $this->assignment_selection_for_slot($context, $slot_type);
            if (!empty($assigned['handled']) && !empty($assigned['disabled'])) {
                return $this->debug_comment('affiliate_assignment_disabled', $content_id, $slot_type, '', '');
            }
            $selection = !empty($assigned['handled']) ? ($assigned['selection'] ?? null) : $this->select_campaign_for_slot($context, $slot_type, $forced_group_id);
            if ($selection && !empty($selection['campaign'])) {
                list($group, $banner) = $this->campaign_to_group_banner($selection['campaign']);
                if ($group && $banner) {
                    $html = $this->render_banner($banner, $content_id, $context, $group, $slot_type);
                    if (trim($html) !== '') {
                        $classes = array('ppar-affiliate-slot', 'ppar-slot-' . sanitize_html_class($slot_type));
                        if (!empty($group['id'])) { $classes[] = 'ppar-group-' . sanitize_html_class($group['id']); }
                        if (!empty($context['post_type'])) { $classes[] = 'ppar-context-' . sanitize_html_class($context['post_type']); }
                        $label = !empty($banner['label']) ? sanitize_text_field($banner['label']) : '';
                        $disclosure = $this->get_disclosure_html($content_id);
                        $is_category_product_slot = preg_match('/^category_product_[123]$/', sanitize_key((string)$slot_type));
                        // V6.61.8: Provider labels must never change category-product card geometry.
                        // The provider remains represented by its offer button/link; the external
                        // label row is suppressed for these three fixed product slots only.
                        if ($is_category_product_slot) { $label = ''; }
                        if ($is_category_product_slot && $disclosure === '' && trim((string)get_option(self::OPTION_DISCLOSURE, '')) !== '') {
                            $disclosure = '<div class="ppar-affiliate-disclosure ppar-affiliate-disclosure--reserve" aria-hidden="true">&nbsp;</div>';
                        }
                        $category_product_slot_style = $is_category_product_slot
                            ? ' style="box-sizing:border-box!important;display:grid!important;grid-template-rows:56px minmax(360px,1fr)!important;width:100%!important;height:auto!important;min-height:416px!important;max-height:none!important;margin:0!important;padding:0!important;border:0!important;overflow:visible!important"'
                            : '';
                        $out = '<div class="' . esc_attr(implode(' ', $classes)) . '" data-ppar-slot="' . esc_attr($slot_type) . '" data-ppar-group="' . esc_attr($group['id'] ?? '') . '"' . $category_product_slot_style . '>';
                        $out .= $disclosure;
                        if ($label !== '') { $out .= '<div class="ppar-affiliate-label">' . esc_html($label) . '</div>'; }
                        $out .= '<div class="ppar-affiliate-content">' . $html . '</div></div>';
                        return $out . $this->debug_comment('affiliate_rendered', $content_id, $slot_type, $group['id'] ?? '', $banner['id'] ?? '');
                    }
                }
            }
        }
        // V2.4.0: Die fest definierten Banner-/Produktplätze der Produkt- und
        // Kategorieebene dürfen öffentlich niemals Platzhalter ausgeben.
        if ($slot_type === 'product_after_category_tiles' || preg_match('/^category_product_[123]$/', sanitize_key((string)$slot_type))) {
            return $this->debug_comment('affiliate_no_real_creative', $content_id, $slot_type, '', '');
        }
        $placeholder = $this->render_placeholder_slot($slot_type);
        if ($placeholder !== '') { return $placeholder . $this->debug_comment('placeholder_rendered', $content_id, $slot_type, 'placeholder', ''); }
        return $this->debug_comment('affiliate_no_matching_campaign', $content_id, $slot_type, '', '');
    }

    private function render_placeholder_slot($slot_type) {
        $settings = $this->get_placeholder_settings();
        if (empty($settings['enabled'])) { return ''; }

        $enabled_map = array(
            'start_after_topics' => 'start_enabled',
            'product_after_category_tiles' => 'category_enabled',
        );
        if (empty($enabled_map[$slot_type]) || empty($settings[$enabled_map[$slot_type]])) { return ''; }

        // V2.2.17: A/B sind global. Startseite, Hub und Ebene 3 zeigen deshalb
        // nach einem Bildwechsel garantiert dieselbe aktuelle Mediathek-Auswahl.
        $image_a = $this->placeholder_image_url($settings, 'start_image_id');
        $image_b = $this->placeholder_image_url($settings, 'start_image_b_id');
        if ($image_a === '' && $image_b === '') { return ''; }

        $url = trim((string) $settings['url']);
        $target = $settings['target'] === '_blank' ? '_blank' : '_self';
        $make_card = function($image, $position) use ($url, $target) {
            if ($image === '') { return ''; }
            // V2.2.24: Der Rahmenvertrag wird direkt mit der ausgegebenen
            // Kachel verankert. Damit kann weder eine alte gecachte CSS-Datei
            // noch eine allgemeinere Theme-Regel den sichtbaren Kartenrahmen
            // erneut entfernen. Die Geometrie entspricht den Portal-Kacheln:
            // 1 px Linienrahmen, keine obere Border, 5 px grauer Kurvenakzent.
            $inner = '<span class="ppar-start-partner-frame-accent" aria-hidden="true" style="position:absolute!important;left:0!important;right:0!important;top:0!important;height:5px!important;background:#a7a7a7!important;border-radius:22px 22px 55% 55%!important;z-index:3!important;pointer-events:none!important"></span>' .
                '<span class="ppar-banner-image-wrap"><img class="ppar-banner-image" src="' . esc_url($image) . '" alt="" loading="lazy"></span>';
            $class = 'ppar-start-partner-card ppar-start-partner-card-' . intval($position);
            $style = 'background-image:url("' . esc_url($image) . '");box-sizing:border-box!important;position:relative!important;padding:0!important;overflow:hidden!important;border:1px solid #e7ebe7!important;border-top:0!important;border-radius:22px!important;background-size:cover!important;background-position:center!important;background-repeat:no-repeat!important;line-height:0!important';
            if ($url !== '') {
                $rel = $target === '_blank' ? ' rel="noopener noreferrer"' : '';
                return '<a class="' . esc_attr($class) . '" style="' . esc_attr($style) . '" href="' . esc_url($url) . '" target="' . esc_attr($target) . '"' . $rel . '>' . $inner . '</a>';
            }
            return '<div class="' . esc_attr($class) . '" style="' . esc_attr($style) . '">' . $inner . '</div>';
        };

        if ($slot_type === 'start_after_topics') {
            // V2.2.25: Startseite zeigt drei gleich breite Werbevorschaukacheln.
            // Es existieren weiterhin nur die zentralen Bilder A und B. Fuer die
            // dritte Kachel wird A wiederverwendet, damit die Anordnung sauber,
            // symmetrisch und ohne neue Backend-Felder funktioniert.
            $first_image = $image_a !== '' ? $image_a : $image_b;
            $second_image = $image_b !== '' ? $image_b : $first_image;
            $third_image = $first_image !== '' ? $first_image : $second_image;
            $card_a = $make_card($first_image, 1);
            $card_b = $make_card($second_image, 2);
            $card_c = $make_card($third_image, 3);
            if ($card_a === '' || $card_b === '' || $card_c === '') { return ''; }
            return '<div class="ppar-affiliate-slot ppar-placeholder-slot ppar-slot-start_after_topics" data-ppar-slot="start_after_topics" data-ppar-placeholder="1" aria-label="Werbeplaetze">' .
                '<div class="ppar-start-partner-grid ppar-start-partner-count-3">' . $card_a . $card_b . $card_c . '</div></div>';
        }

        $image = $image_a !== '' ? $image_a : $image_b;
        $creative = $make_card($image, 1);
        return $creative !== ''
            ? '<div class="ppar-affiliate-slot ppar-placeholder-slot ppar-slot-' . esc_attr(sanitize_html_class($slot_type)) . '" data-ppar-slot="' . esc_attr($slot_type) . '" data-ppar-placeholder="1" aria-label="Werbeplatz"><div class="ppar-affiliate-content">' . $creative . '</div></div>'
            : '';
    }

    private function get_disclosure_html($post_id) {
        $text = trim((string) get_option(self::OPTION_DISCLOSURE, ''));
        if ($text === '') {
            return '';
        }

        if (isset($this->disclosure_printed[$post_id])) {
            return '';
        }
        $this->disclosure_printed[$post_id] = true;

        return '<div class="ppar-affiliate-disclosure">' . esc_html($text) . '</div>';
    }

    private function render_banner($banner, $post_id, $context, $group, $slot_type) {
        $mode = isset($banner['mode']) ? sanitize_key($banner['mode']) : 'image_link';
        $subid = $this->build_subid($post_id, $context, $group, $slot_type);
        $replacements = array(
            '{post_id}' => (string) $post_id,
            '{category_slug}' => $context['primary_slug'],
            '{category_name}' => $context['primary_name'],
            '{group_id}' => $group['id'] ?? '',
            '{slot}' => $slot_type,
            '{subid}' => $subid,
        );

        if ($mode === 'html') {
            $raw = isset($banner['html']) ? (string) $banner['html'] : '';
            $raw = strtr($raw, $replacements);
            return $this->filter_allowed_banner_html($raw);
        }

        $url = isset($banner['url']) ? strtr((string) $banner['url'], $replacements) : '';
        $url = $this->apply_subid_to_url($url, $subid, $banner['subid_param'] ?? '');
        if (method_exists($this, 'multiprovider_runtime_tracking_url')) { $url = $this->multiprovider_runtime_tracking_url($url, (string)($banner['network'] ?? '')); }
        $image_url = isset($banner['image_url']) ? strtr((string) $banner['image_url'], $replacements) : '';
        if (method_exists($this, 'multiprovider_runtime_image_url')) { $image_url = $this->multiprovider_runtime_image_url($image_url, (string)($banner['network'] ?? ''), absint($banner['campaign_post_id'] ?? 0)); }
        $title = isset($banner['title']) ? strtr((string) $banner['title'], $replacements) : '';
        $button = isset($banner['button_text']) ? strtr((string) $banner['button_text'], $replacements) : '';
        $description = isset($banner['description']) ? strtr((string) $banner['description'], $replacements) : '';
        $price = isset($banner['price']) ? trim(strtr((string)$banner['price'], $replacements)) : '';
        $currency = isset($banner['currency']) ? strtoupper(substr(sanitize_text_field((string)$banner['currency']), 0, 3)) : 'EUR';
        $availability = isset($banner['availability']) ? trim(strtr((string)$banner['availability'], $replacements)) : '';
        $creative_type = sanitize_key((string)($banner['creative_type'] ?? 'banner'));
        $category_product_slot = (bool) preg_match('/^category_product_[123]$/', sanitize_key((string)$slot_type));
        $category_product_wrap_attr = $category_product_slot
            ? ' data-ppar-category-product-image-frame="150" style="box-sizing:border-box!important;display:flex!important;flex:0 0 150px!important;align-items:center!important;justify-content:center!important;width:150px!important;height:150px!important;min-width:150px!important;min-height:150px!important;max-width:150px!important;max-height:150px!important;margin:0 auto!important;padding:0!important;overflow:hidden!important;background:#fff!important;line-height:0!important"'
            : '';
        $category_product_image_attr = $category_product_slot
            ? ' data-ppar-category-product-image-fit="contain" style="box-sizing:border-box!important;display:block!important;width:150px!important;height:150px!important;min-width:150px!important;min-height:150px!important;max-width:150px!important;max-height:150px!important;margin:0!important;padding:0!important;border-radius:0!important;object-fit:contain!important;object-position:center center!important"'
            : '';

        if ($url === '') {
            return '';
        }

        $target = (($banner['target'] ?? '_blank') === '_self') ? '_self' : '_blank';
        $rel = $target === '_blank' ? 'sponsored nofollow noopener noreferrer' : 'sponsored nofollow';
        $offers = array();
        if ($creative_type === 'product' && $category_product_slot && method_exists($this, 'multiprovider_matching_offers_for_banner')) {
            $offers = $this->multiprovider_matching_offers_for_banner($banner, $context, $slot_type);
        }
        $multi = count($offers) > 1;
        $category_product_link_attr = $category_product_slot
            ? ' data-ppar-category-product-card="1" style="box-sizing:border-box!important;display:grid!important;grid-template-rows:150px minmax(210px,1fr)!important;align-items:stretch!important;width:100%!important;height:auto!important;min-height:360px!important;max-height:none!important;overflow:hidden!important"'
            : '';
        $out = $multi
            ? '<span class="ppar-banner-link ppar-banner-link--multi"' . $category_product_link_attr . '>'
            : '<a class="ppar-banner-link"' . $category_product_link_attr . ' href="' . esc_url($url) . '" target="' . esc_attr($target) . '" rel="' . esc_attr($rel) . '">';
        if ($image_url !== '') {
            $out .= '<span class="ppar-banner-image-wrap"' . $category_product_wrap_attr . '><img class="ppar-banner-image"' . $category_product_image_attr . ' src="' . esc_url($image_url) . '" alt="' . esc_attr($title !== '' ? $title : $button) . '" width="150" height="150" loading="lazy" decoding="async"></span>';
        }
        if ($title !== '' || $description !== '' || $button !== '') {
            $category_product_text_attr = $category_product_slot
                ? ' data-ppar-category-product-text="1" style="box-sizing:border-box!important;display:flex!important;flex:1 1 auto!important;flex-direction:column!important;align-items:stretch!important;width:100%!important;min-height:152px!important"'
                : '';
            $out .= '<span class="ppar-banner-text"' . $category_product_text_attr . '>';
            if ($title !== '') { $out .= '<strong class="ppar-banner-title">' . esc_html($title) . '</strong>'; }
            if ($description !== '') { $out .= '<span class="ppar-banner-description">' . esc_html($description) . '</span>'; }
            if ($creative_type === 'product' && ($price !== '' || $availability !== '')) {
                $out .= '<span class="ppar-banner-meta">';
                if ($price !== '') { $out .= '<strong class="ppar-banner-price">' . esc_html($price . ($currency !== '' ? ' ' . $currency : '')) . '</strong>'; }
                if ($availability !== '') { $out .= '<span class="ppar-banner-availability">' . esc_html($availability) . '</span>'; }
                $out .= '</span>';
            }
            if ($multi && method_exists($this, 'multiprovider_render_offer_buttons')) {
                $out .= $this->multiprovider_render_offer_buttons($offers, 'banner');
            } elseif ($button !== '') {
                $out .= '<span class="ppar-banner-button">' . esc_html($button) . '</span>';
            }
            $out .= '</span>';
        }
        $out .= $multi ? '</span>' : '</a>';
        return $out;
    }

    private function filter_allowed_banner_html($html) {
        $allowed = array(
            'a' => array(
                'href' => true,
                'title' => true,
                'target' => true,
                'rel' => true,
                'class' => true,
                'id' => true,
                'data-*' => true,
            ),
            'img' => array(
                'src' => true,
                'alt' => true,
                'title' => true,
                'width' => true,
                'height' => true,
                'loading' => true,
                'decoding' => true,
                'class' => true,
                'id' => true,
                'data-*' => true,
            ),
            'div' => array('class' => true, 'id' => true, 'style' => true, 'data-*' => true),
            'span' => array('class' => true, 'id' => true, 'style' => true, 'data-*' => true),
            'p' => array('class' => true, 'id' => true, 'style' => true),
            'strong' => array('class' => true),
            'em' => array('class' => true),
            'br' => array(),
            'iframe' => array(
                'src' => true,
                'width' => true,
                'height' => true,
                'frameborder' => true,
                'scrolling' => true,
                'allow' => true,
                'allowfullscreen' => true,
                'class' => true,
                'id' => true,
            ),
        );

        $html = wp_kses($html, $allowed);
        $html = preg_replace('/<a\s(?![^>]*\brel=)/i', '<a rel="sponsored nofollow noopener" target="_blank" ', $html);
        return $html;
    }

    private function build_subid($post_id, $context, $group, $slot_type) {
        $parts = array(
            'post',
            (string) $post_id,
            sanitize_key($group['id'] ?? 'group'),
            sanitize_key($context['primary_slug'] ?: 'category'),
            sanitize_key($slot_type),
        );
        return substr(implode('_', array_filter($parts)), 0, 120);
    }

    private function apply_subid_to_url($url, $subid, $subid_param) {
        $url = trim($url);
        if ($url === '') {
            return '';
        }
        if (strpos($url, '{subid}') !== false) {
            return str_replace('{subid}', rawurlencode($subid), $url);
        }

        $subid_param = sanitize_key((string) $subid_param);
        if ($subid_param === '') {
            return $url;
        }

        return add_query_arg($subid_param, rawurlencode($subid), $url);
    }

    private function get_content_context($post_id) {
        $post_type = get_post_type($post_id);
        $slugs = array();
        $names = array();
        $ancestor_ids = array();
        $term_ids = array();
        $direct_term_slugs = array();
        $primary_slug = '';
        $primary_name = '';

        $title = (string) get_the_title($post_id);
        $post_slug = (string) get_post_field('post_name', $post_id);
        if ($post_slug !== '') {
            $slugs[] = $post_slug;
            $primary_slug = $post_slug;
        }
        if ($title !== '') {
            $names[] = $title;
            $primary_name = $title;
        }

        if ($post_type === 'post') {
            $terms = get_the_terms($post_id, 'category');
            if (!is_wp_error($terms) && is_array($terms)) {
                foreach ($terms as $term) {
                    $term_ids[] = (int) $term->term_id;
                    $direct_term_slugs[] = (string) $term->slug;
                    if ($primary_slug === '' || $primary_slug === $post_slug) {
                        $primary_slug = (string) $term->slug;
                        $primary_name = (string) $term->name;
                    }
                    $slugs[] = (string) $term->slug;
                    $names[] = (string) $term->name;

                    $ancestors = get_ancestors($term->term_id, 'category');
                    foreach ($ancestors as $ancestor_id) {
                        $term_ids[] = (int) $ancestor_id;
                        $ancestor = get_term($ancestor_id, 'category');
                        if ($ancestor && !is_wp_error($ancestor)) {
                            $slugs[] = (string) $ancestor->slug;
                            $names[] = (string) $ancestor->name;
                        }
                    }
                }
            }
        }

        if ($post_type === 'hp_listing' && taxonomy_exists('hp_listing_category')) {
            $terms = get_the_terms($post_id, 'hp_listing_category');
            if (!is_wp_error($terms) && is_array($terms)) {
                foreach ($terms as $term) {
                    $term_ids[] = (int) $term->term_id;
                    $direct_term_slugs[] = (string) $term->slug;
                    $slugs[] = (string) $term->slug;
                    $names[] = (string) $term->name;
                    if ($primary_slug === '' || $primary_slug === $post_slug) {
                        $primary_slug = (string) $term->slug;
                        $primary_name = (string) $term->name;
                    }
                    foreach ((array) get_ancestors($term->term_id, 'hp_listing_category') as $ancestor_id) {
                        $term_ids[] = (int) $ancestor_id;
                        $ancestor = get_term($ancestor_id, 'hp_listing_category');
                        if ($ancestor && !is_wp_error($ancestor)) {
                            $slugs[] = (string) $ancestor->slug;
                            $names[] = (string) $ancestor->name;
                        }
                    }
                }
            }
        }

        if ($post_type === 'page') {
            $ancestors = get_post_ancestors($post_id);
            if (is_array($ancestors)) {
                $ancestor_ids = array_values(array_unique(array_map('intval', $ancestors)));
                foreach ($ancestors as $ancestor_id) {
                    $ancestor_slug = (string) get_post_field('post_name', $ancestor_id);
                    $ancestor_title = (string) get_the_title($ancestor_id);
                    if ($ancestor_slug !== '') {
                        $slugs[] = $ancestor_slug;
                    }
                    if ($ancestor_title !== '') {
                        $names[] = $ancestor_title;
                    }
                }
            }
        }

        $content = get_post_field('post_content', $post_id);
        $haystack = strtolower(wp_strip_all_tags($title . ' ' . implode(' ', $slugs) . ' ' . implode(' ', $names) . ' ' . $content));

        return array(
            'slugs' => array_values(array_unique(array_map('sanitize_key', $slugs))),
            'names' => array_values(array_unique($names)),
            'primary_slug' => sanitize_key($primary_slug),
            'primary_name' => $primary_name,
            'post_type' => $post_type,
            'haystack' => $haystack,
            'post_id' => (int) $post_id,
            'ancestor_ids' => $ancestor_ids,
            'term_ids' => array_values(array_unique(array_map('intval', $term_ids))),
            'direct_term_slugs' => array_values(array_unique(array_map('sanitize_key', $direct_term_slugs))),
        );
    }

    private function get_category_archive_context($term) {
        $slugs = array((string) $term->slug);
        $names = array((string) $term->name);

        $ancestors = get_ancestors((int) $term->term_id, 'category');
        foreach ($ancestors as $ancestor_id) {
            $ancestor = get_term($ancestor_id, 'category');
            if ($ancestor && !is_wp_error($ancestor)) {
                $slugs[] = (string) $ancestor->slug;
                $names[] = (string) $ancestor->name;
            }
        }

        $description = isset($term->description) ? (string) $term->description : '';
        $haystack = strtolower(wp_strip_all_tags((string) $term->name . ' ' . (string) $term->slug . ' ' . implode(' ', $slugs) . ' ' . implode(' ', $names) . ' ' . $description));

        return array(
            'slugs' => array_values(array_unique(array_map('sanitize_key', $slugs))),
            'names' => array_values(array_unique($names)),
            'primary_slug' => sanitize_key((string) $term->slug),
            'primary_name' => (string) $term->name,
            'post_type' => 'category_archive',
            'haystack' => $haystack,
            'post_id' => 0,
            'ancestor_ids' => array(),
            'term_ids' => array_values(array_unique(array_map('intval', array_merge(array((int) $term->term_id), $ancestors)))),
            'direct_term_slugs' => array(sanitize_key((string) $term->slug)),
        );
    }

    private function find_matching_group($groups, $context) {
        $best = null;
        $best_score = -1;
        foreach ($groups as $group) {
            if (empty($group['active']) || empty($group['id']) || !$this->rule_is_current($group)) {
                continue;
            }
            $base_score = $this->score_match($group, $context);
            $score = ($base_score * 10000) + max(0, min(9999, (int) ($group['priority'] ?? 0)));
            if ($score > $best_score && $score > 0) {
                $best_score = $score;
                $best = $group;
            }
        }
        return $best;
    }

    private function rule_is_current($rule) {
        $today = function_exists('current_time') ? current_time('Y-m-d') : gmdate('Y-m-d');
        $start = isset($rule['start_date']) ? trim((string) $rule['start_date']) : '';
        $end = isset($rule['end_date']) ? trim((string) $rule['end_date']) : '';
        if ($start !== '' && $today < $start) {
            return false;
        }
        if ($end !== '' && $today > $end) {
            return false;
        }
        return true;
    }

    private function find_group_by_id($groups, $id) {
        foreach ($groups as $group) {
            if (!empty($group['active']) && isset($group['id']) && sanitize_key($group['id']) === sanitize_key($id)) {
                return $group;
            }
        }
        return null;
    }

    private function score_match($rule, $context) {
        $mode = isset($rule['match_mode']) ? sanitize_key((string) $rule['match_mode']) : 'auto';
        if (!in_array($mode, $this->allowed_match_modes(), true)) {
            $mode = 'auto';
        }

        $match_slugs = isset($rule['match_slugs']) && is_array($rule['match_slugs']) ? $rule['match_slugs'] : array();
        $match_keywords = isset($rule['match_keywords']) && is_array($rule['match_keywords']) ? $rule['match_keywords'] : array();
        $context_slugs = isset($context['slugs']) && is_array($context['slugs']) ? $context['slugs'] : array();
        $haystack = isset($context['haystack']) ? (string) $context['haystack'] : '';
        $match_post_ids = isset($rule['match_post_ids']) && is_array($rule['match_post_ids']) ? array_values(array_filter(array_map('intval', $rule['match_post_ids']))) : array();
        $match_term_ids = isset($rule['match_term_ids']) && is_array($rule['match_term_ids']) ? array_values(array_filter(array_map('intval', $rule['match_term_ids']))) : array();
        $context_post_id = isset($context['post_id']) ? (int) $context['post_id'] : 0;
        $context_ancestor_ids = isset($context['ancestor_ids']) && is_array($context['ancestor_ids']) ? array_map('intval', $context['ancestor_ids']) : array();
        $context_term_ids = isset($context['term_ids']) && is_array($context['term_ids']) ? array_map('intval', $context['term_ids']) : array();

        // Fallback-Regel: absichtlich niedrig, damit jeder echte Slug-/Keyword-Treffer gewinnt.
        if ($mode === 'fallback') {
            return 1;
        }

        $score = 0;
        if (!empty($match_post_ids)) {
            if ($context_post_id > 0 && in_array($context_post_id, $match_post_ids, true)) {
                $score += 300;
            }
            if (!empty($rule['match_descendants']) && !empty(array_intersect($match_post_ids, $context_ancestor_ids))) {
                $score += 220;
            }
        }
        if (!empty($match_term_ids) && !empty(array_intersect($match_term_ids, $context_term_ids))) {
            $score += 260;
        }
        if ($mode === 'auto' || $mode === 'exact_slug') {
            foreach ($match_slugs as $slug) {
                $slug = sanitize_key($slug);
                if ($slug !== '' && in_array($slug, $context_slugs, true)) {
                    $score += 100;
                }
            }
        }

        if ($mode === 'auto' || $mode === 'keyword') {
            foreach ($match_keywords as $keyword) {
                $keyword = strtolower(trim((string) $keyword));
                if ($keyword !== '' && strpos($haystack, $keyword) !== false) {
                    $score += 10;
                }
            }
        }

        return $score;
    }

    private function find_matching_banner($group, $context, $slot_type, $intent) {
        if (empty($group['banners']) || !is_array($group['banners'])) {
            return null;
        }

        $candidates = array();
        foreach ($group['banners'] as $banner) {
            if (empty($banner['active']) || !$this->rule_is_current($banner)) {
                continue;
            }

            $slots = isset($banner['slots']) && is_array($banner['slots']) ? array_map('sanitize_key', $banner['slots']) : array('*');
            $accepted_slots = $this->equivalent_slot_names($slot_type);
            if (!in_array('*', $slots, true) && empty(array_intersect($accepted_slots, $slots))) {
                continue;
            }

            $score = (int) ($banner['priority'] ?? 0);
            $score += $this->score_match($banner, $context);

            if (!empty($banner['intent']) && is_array($banner['intent'])) {
                $intents = array_map('sanitize_key', $banner['intent']);
                if (in_array(sanitize_key($intent), $intents, true)) {
                    $score += 20;
                }
            }

            $candidates[] = array('score' => $score, 'banner' => $banner);
        }

        if (empty($candidates)) {
            return null;
        }

        usort($candidates, function($a, $b) {
            if ($a['score'] === $b['score']) {
                return 0;
            }
            return ($a['score'] > $b['score']) ? -1 : 1;
        });

        return $candidates[0]['banner'];
    }

    private function get_groups() {
        $campaigns = $this->get_campaigns();
        if (is_array($campaigns)) {
            return $this->campaigns_to_groups($campaigns);
        }
        return $this->get_legacy_groups();
    }

    private function get_legacy_groups() {
        $json = (string) get_option(self::OPTION_GROUPS_JSON, '[]');
        $data = json_decode($json, true);
        return is_array($data) ? $data : array();
    }

    private function get_campaigns() {
        // V6.20 performance contract: affiliate slot rendering may ask for the
        // ranked campaign set several times in the same request (three product
        // slots, banners, category injections). Loading every ap_campaign post
        // from WordPress for each slot amplified the V6.19 BUSINESS inventory
        // growth into page/AJAX latency. Keep the existing campaign architecture,
        // but resolve it once per request and reuse the immutable snapshot.
        if (is_array($this->campaigns_request_cache)) {
            return $this->campaigns_request_cache;
        }
        if (!post_type_exists(self::CAMPAIGN_POST_TYPE)) {
            $this->register_campaign_post_type();
        }
        $posts = get_posts(array(
            'post_type' => self::CAMPAIGN_POST_TYPE,
            'post_status' => array('publish', 'draft', 'private'),
            'numberposts' => -1,
            'orderby' => array('menu_order' => 'ASC', 'title' => 'ASC'),
            'order' => 'ASC',
            'suppress_filters' => true,
        ));
        $campaigns = array();
        foreach ((array) $posts as $post) {
            $campaign = $this->campaign_from_post($post);
            if ($campaign) {
                $campaigns[] = $campaign;
            }
        }
        $this->campaigns_request_cache = $campaigns;
        return $this->campaigns_request_cache;
    }

    private function campaign_from_post($post) {
        if (!$post || empty($post->ID)) {
            return null;
        }
        $stored = get_post_meta((int) $post->ID, 'ppar_campaign_data', true);
        $stored = is_array($stored) ? $stored : array();
        $campaign = wp_parse_args($stored, $this->central_blank_campaign());
        $campaign['post_id'] = (int) $post->ID;
        $campaign['id'] = !empty($stored['id']) ? sanitize_key((string) $stored['id']) : sanitize_key((string) $post->post_name);
        $campaign['name'] = trim((string) $post->post_title) !== '' ? (string) $post->post_title : (string) ($campaign['name'] ?? $campaign['id']);
        $campaign['active'] = !empty($campaign['active']);
        $campaign['match_descendants'] = !empty($campaign['match_descendants']);
        $campaign['match_slugs'] = is_array($campaign['match_slugs']) ? array_values(array_filter(array_map('sanitize_key', $campaign['match_slugs']))) : array();
        $campaign['match_keywords'] = is_array($campaign['match_keywords']) ? array_values(array_filter(array_map('sanitize_text_field', $campaign['match_keywords']))) : array();
        $campaign['match_term_ids'] = isset($campaign['match_term_ids']) && is_array($campaign['match_term_ids']) ? array_values(array_filter(array_map('absint', $campaign['match_term_ids']))) : array();
        $campaign['automation_target_keys'] = isset($campaign['automation_target_keys']) && is_array($campaign['automation_target_keys']) ? array_values(array_unique(array_filter(array_map(array($this, 'automation_normalize_target_key'), $campaign['automation_target_keys'])))) : array();
        $campaign['placements'] = is_array($campaign['placements']) ? array_values(array_filter(array_map('sanitize_key', $campaign['placements']))) : array();
        $campaign['product_gtins'] = isset($campaign['product_gtins']) && is_array($campaign['product_gtins']) ? array_values(array_unique(array_filter(array_map('sanitize_text_field', $campaign['product_gtins'])))) : array();
        $campaign['product_asins'] = isset($campaign['product_asins']) && is_array($campaign['product_asins']) ? array_values(array_unique(array_filter(array_map('sanitize_text_field', $campaign['product_asins'])))) : array();
        return $campaign;
    }

    private function save_campaign_record($campaign, $post_id = 0) {
        $campaign = wp_parse_args(is_array($campaign) ? $campaign : array(), $this->central_blank_campaign());
        $name = trim((string) $campaign['name']) !== '' ? (string) $campaign['name'] : (string) ($campaign['title'] ?? 'Affiliate-Kampagne');
        $postarr = array(
            'post_type' => self::CAMPAIGN_POST_TYPE,
            'post_status' => 'publish',
            'post_title' => $name,
        );
        if ($post_id > 0) {
            $postarr['ID'] = $post_id;
            $result = wp_update_post($postarr, true);
        } else {
            $result = wp_insert_post($postarr, true);
        }
        if (is_wp_error($result) || !$result) {
            return $result;
        }
        $post_id = (int) $result;
        if (empty($campaign['id'])) {
            $campaign['id'] = sanitize_key((string) get_post_field('post_name', $post_id));
        }
        unset($campaign['post_id']);
        update_post_meta($post_id, 'ppar_campaign_data', $campaign);
        // A background materializer may create/update several campaigns inside
        // one request. Invalidate the request snapshot only after a real write.
        $this->campaigns_request_cache = null;
        return $post_id;
    }

    public function maybe_migrate_campaigns() {
        if (!current_user_can('manage_options')) {
            return;
        }
        if (!post_type_exists(self::CAMPAIGN_POST_TYPE)) {
            $this->register_campaign_post_type();
        }
        if (get_option(self::OPTION_CPT_MIGRATED, '0') === '1') {
            return;
        }
        $existing_posts = get_posts(array(
            'post_type' => self::CAMPAIGN_POST_TYPE,
            'post_status' => 'any',
            'numberposts' => 1,
            'fields' => 'ids',
            'suppress_filters' => true,
        ));
        if (!empty($existing_posts)) {
            update_option(self::OPTION_CPT_MIGRATED, '1', false);
            return;
        }

        $campaigns = get_option(self::OPTION_CAMPAIGNS, array());
        if (!is_array($campaigns) || empty($campaigns)) {
            $legacy = $this->get_legacy_groups();
            $campaigns = array();
            foreach ($legacy as $group) {
                $banners = isset($group['banners']) && is_array($group['banners']) ? $group['banners'] : array();
                foreach ($banners as $banner) {
                    $banner_slugs = isset($banner['match_slugs']) && is_array($banner['match_slugs']) ? array_values(array_filter($banner['match_slugs'])) : array();
                    $banner_keywords = isset($banner['match_keywords']) && is_array($banner['match_keywords']) ? array_values(array_filter($banner['match_keywords'])) : array();
                    $group_slugs = isset($group['match_slugs']) && is_array($group['match_slugs']) ? $group['match_slugs'] : array();
                    $group_keywords = isset($group['match_keywords']) && is_array($group['match_keywords']) ? $group['match_keywords'] : array();
                    $effective_slugs = !empty($banner_slugs) ? $banner_slugs : $group_slugs;
                    $effective_keywords = !empty($banner_keywords) ? $banner_keywords : $group_keywords;
                    $campaigns[] = array(
                        'id' => sanitize_key((string) (($group['id'] ?? 'campaign') . '_' . ($banner['id'] ?? 'banner'))),
                        'name' => trim((string) ($banner['title'] ?? '')) !== '' ? (string) $banner['title'] : (string) ($group['label'] ?? $group['id'] ?? 'Kampagne'),
                        'partner' => '',
                        'active' => !empty($group['active']) && !empty($banner['active']),
                        'assignment_mode' => (($group['match_mode'] ?? 'auto') === 'fallback') ? 'fallback' : ((!empty($effective_keywords) && empty($effective_slugs)) ? 'keywords' : 'page_tree'),
                        'page_id' => 0,
                        'match_descendants' => true,
                        'match_slugs' => $effective_slugs,
                        'match_keywords' => $effective_keywords,
                        'match_term_ids' => isset($group['match_term_ids']) && is_array($group['match_term_ids']) ? $group['match_term_ids'] : array(),
                        'priority' => (int) ($banner['priority'] ?? 10),
                        'start_date' => (string) ($banner['start_date'] ?? ''),
                        'end_date' => (string) ($banner['end_date'] ?? ''),
                        'placements' => isset($banner['slots']) && is_array($banner['slots']) ? $banner['slots'] : array('hub_grid_card'),
                        'label' => (string) ($banner['label'] ?? 'Anzeige'),
                        'title' => (string) ($banner['title'] ?? ''),
                        'description' => (string) ($banner['description'] ?? ''),
                        'button_text' => (string) ($banner['button_text'] ?? 'Mehr erfahren'),
                        'image_url' => (string) ($banner['image_url'] ?? ''),
                        'url' => (string) ($banner['url'] ?? ''),
                        'target' => (string) ($banner['target'] ?? '_blank'),
                        'subid_param' => (string) ($banner['subid_param'] ?? ''),
                        'source' => 'legacy-migration',
                        'external_id' => '',
                    );
                }
            }
        }

        foreach ($campaigns as $campaign) {
            if (!is_array($campaign)) {
                continue;
            }
            $campaign = wp_parse_args($campaign, $this->central_blank_campaign());
            if (!empty($campaign['active']) && !$this->campaign_is_complete($campaign)) {
                $campaign['active'] = false;
            }
            $this->save_campaign_record($campaign, 0);
        }
        update_option(self::OPTION_CPT_MIGRATED, '1', false);
        update_option(self::OPTION_CAMPAIGNS_MIGRATED, '1', false);
    }

    private function campaigns_to_groups($campaigns) {
        $groups = array();
        foreach ($campaigns as $campaign) {
            if (!is_array($campaign) || empty($campaign['id'])) {
                continue;
            }
            $mode = isset($campaign['assignment_mode']) ? sanitize_key((string) $campaign['assignment_mode']) : 'page_tree';
            $match_mode = $mode === 'fallback' ? 'fallback' : ($mode === 'keywords' ? 'keyword' : ($mode === 'exact_page' ? 'exact_slug' : 'auto'));
            $page_id = isset($campaign['page_id']) ? (int) $campaign['page_id'] : 0;
            $slugs = isset($campaign['match_slugs']) && is_array($campaign['match_slugs']) ? array_map('sanitize_key', $campaign['match_slugs']) : array();
            if ($page_id > 0) {
                $page_slug = sanitize_key((string) get_post_field('post_name', $page_id));
                if ($page_slug !== '') {
                    $slugs[] = $page_slug;
                }
            }
            $placements = isset($campaign['placements']) && is_array($campaign['placements']) ? array_map('sanitize_key', $campaign['placements']) : array('hub_grid_card');
            $groups[] = array(
                'id' => sanitize_key((string) $campaign['id']),
                'label' => (string) ($campaign['name'] ?? $campaign['id']),
                'active' => !empty($campaign['active']),
                'match_mode' => $match_mode,
                'match_post_ids' => $page_id > 0 ? array($page_id) : array(),
                'match_descendants' => !empty($campaign['match_descendants']),
                'match_slugs' => array_values(array_unique($slugs)),
                'match_keywords' => isset($campaign['match_keywords']) && is_array($campaign['match_keywords']) ? $campaign['match_keywords'] : array(),
                'match_term_ids' => isset($campaign['match_term_ids']) && is_array($campaign['match_term_ids']) ? $campaign['match_term_ids'] : array(),
                'priority' => (int) ($campaign['priority'] ?? 10),
                'start_date' => (string) ($campaign['start_date'] ?? ''),
                'end_date' => (string) ($campaign['end_date'] ?? ''),
                'workflow_status' => 'freigegeben',
                'workflow_note' => 'Zentral verwaltete Kampagne.',
                'banners' => array(array(
                    'id' => sanitize_key((string) $campaign['id']),
                    'label' => (string) ($campaign['label'] ?? 'Anzeige'),
                    'active' => !empty($campaign['active']),
                    'mode' => (string)($campaign['render_mode'] ?? 'image_link'),
                    'slots' => $placements,
                    'intent' => array('primary_product', 'fallback'),
                    'priority' => (int) ($campaign['priority'] ?? 10),
                    'match_mode' => 'fallback',
                    'match_slugs' => array(),
                    'match_keywords' => array(),
                    'start_date' => (string) ($campaign['start_date'] ?? ''),
                    'end_date' => (string) ($campaign['end_date'] ?? ''),
                    'url' => (string) ($campaign['url'] ?? ''),
                    'subid_param' => (string) ($campaign['subid_param'] ?? ''),
                    'image_url' => (string) ($campaign['image_url'] ?? ''),
                    'title' => (string) ($campaign['title'] ?? ''),
                    'description' => (string) ($campaign['description'] ?? ''),
                    'button_text' => (string) ($campaign['button_text'] ?? 'Mehr erfahren'),
                    'target' => (string) ($campaign['target'] ?? '_blank'),
                    'html' => (string)($campaign['html'] ?? ''),
                    'creative_type' => (string)($campaign['creative_type'] ?? 'banner'),
                    'network' => (string)($campaign['network'] ?? 'manual'),
                    'programme_name' => (string)($campaign['programme_name'] ?? ''),
                    'programme_status' => (string)($campaign['programme_status'] ?? 'unknown'),
                    'partner' => (string)($campaign['partner'] ?? ''),
                    'price' => (string)($campaign['price'] ?? ''),
                    'currency' => (string)($campaign['currency'] ?? 'EUR'),
                    'availability' => (string)($campaign['availability'] ?? ''),
                    'dimensions' => (string)($campaign['dimensions'] ?? ''),
                    'campaign_post_id' => absint($campaign['post_id'] ?? 0),
                    'product_gtins' => (array)($campaign['product_gtins'] ?? array()),
                    'product_asins' => (array)($campaign['product_asins'] ?? array()),
                    'product_identity_source' => (string)($campaign['product_identity_source'] ?? ''),
                )),
            );
        }
        return $groups;
    }

    private function campaign_slot_allowed($campaign, $slot_type) {
        $placements = isset($campaign['placements']) && is_array($campaign['placements']) ? array_map('sanitize_key', $campaign['placements']) : array();
        $accepted = $this->equivalent_slot_names($slot_type);
        return !empty(array_intersect($accepted, $placements)) || in_array('*', $placements, true);
    }

    private function campaign_match_rank($campaign, $context) {
        $mode = sanitize_key((string) ($campaign['assignment_mode'] ?? 'page_tree'));
        $post_id = isset($context['post_id']) ? (int) $context['post_id'] : 0;
        $ancestors = isset($context['ancestor_ids']) && is_array($context['ancestor_ids']) ? array_map('intval', $context['ancestor_ids']) : array();
        $slugs = isset($context['slugs']) && is_array($context['slugs']) ? array_map('sanitize_key', $context['slugs']) : array();
        $term_ids = isset($context['term_ids']) && is_array($context['term_ids']) ? array_map('intval', $context['term_ids']) : array();
        $haystack = strtolower((string) ($context['haystack'] ?? ''));
        $page_id = isset($campaign['page_id']) ? (int) $campaign['page_id'] : 0;

        if ($mode === 'fallback') {
            return array('specificity' => 10, 'matches' => 1, 'reason' => 'Allgemeiner Fallback.');
        }
        if (!empty($campaign['automation_target_keys']) && method_exists($this, 'automation_campaign_exact_target_rank')) {
            return $this->automation_campaign_exact_target_rank($campaign, $context);
        }
        if ($mode === 'exact_page') {
            return ($page_id > 0 && $post_id === $page_id)
                ? array('specificity' => 500, 'matches' => 1, 'reason' => 'Direkt ausgewählte Seite.')
                : null;
        }
        if ($mode === 'page_tree' || $mode === 'auto_topic') {
            $auto_label = sanitize_text_field((string)($campaign['auto_topic_label'] ?? ''));
            if ($page_id > 0 && $post_id === $page_id) {
                return array('specificity' => $mode === 'auto_topic' ? 480 : 500, 'matches' => 1, 'reason' => $mode === 'auto_topic' ? 'Automatisch erkannter Themenbereich „' . $auto_label . '“.' : 'Direkt ausgewählter Hub/Bereich.');
            }
            if ($page_id > 0 && !empty($campaign['match_descendants']) && in_array($page_id, $ancestors, true)) {
                return array('specificity' => $mode === 'auto_topic' ? 430 : 450, 'matches' => 1, 'reason' => $mode === 'auto_topic' ? 'Unterseite des automatisch erkannten Themenbereichs „' . $auto_label . '“.' : 'Unterseite des ausgewählten Hubs/Bereichs.');
            }
        }

        $wanted_terms = isset($campaign['match_term_ids']) && is_array($campaign['match_term_ids']) ? array_map('intval', $campaign['match_term_ids']) : array();
        $term_matches = count(array_intersect($wanted_terms, $term_ids));
        if ($term_matches > 0) {
            return array('specificity' => 400, 'matches' => $term_matches, 'reason' => 'Passende Kategorie oder Taxonomie.');
        }

        $wanted_slugs = isset($campaign['match_slugs']) && is_array($campaign['match_slugs']) ? array_map('sanitize_key', $campaign['match_slugs']) : array();
        $slug_matches = count(array_intersect($wanted_slugs, $slugs));
        if ($slug_matches > 0) {
            return array('specificity' => 350, 'matches' => $slug_matches, 'reason' => 'Passender Seiten- oder Bereichs-Slug.');
        }

        if ($mode === 'keywords') {
            $keyword_matches = 0;
            foreach ((array) ($campaign['match_keywords'] ?? array()) as $keyword) {
                $keyword = strtolower(trim((string) $keyword));
                if ($keyword !== '' && strpos($haystack, $keyword) !== false) {
                    $keyword_matches++;
                }
            }
            if ($keyword_matches > 0) {
                return array('specificity' => 200, 'matches' => $keyword_matches, 'reason' => 'Passender definierter Themenbegriff.');
            }
        }
        return null;
    }
    private function slot_required_creative_type($slot_type) {
        $slot_type = sanitize_key((string)$slot_type);
        if ($slot_type === 'category_product' || preg_match('/^(?:hub_product|category_product|journal_product)_[123]$/', $slot_type) || $slot_type === 'post_bottom_products') { return 'product'; }
        if (in_array($slot_type, array('product_after_category_tiles', 'post_inline_banner', 'anzeigenmarkt_top_banner', 'journal_banner'), true)) { return 'banner'; }
        return '';
    }

    private function category_product_slot_index($slot_type) {
        return preg_match('/^(?:hub_product|category_product|journal_product)_([123])$/', sanitize_key((string)$slot_type), $m) ? (int)$m[1] : 0;
    }


    /**
     * Resolve the active canonical eBay BUSINESS source row behind an output-object
     * product campaign. V6.18 remains untouched: pending rows may exist internally.
     * Public image validity is decided from the CURRENT source image response, not
     * from historical dimension/hash metadata stored during materialisation.
     */
    private function ebay_product_public_source_row($campaign) {
        if (!is_array($campaign)
            || sanitize_key((string)($campaign['creative_type'] ?? '')) !== 'product'
            || sanitize_key((string)($campaign['network'] ?? '')) !== 'ebay'
            || sanitize_key((string)($campaign['source'] ?? '')) !== 'output_object_v4') { return false; }

        $post_id = absint($campaign['post_id'] ?? 0);
        if ($post_id <= 0 || !function_exists('get_post_meta') || absint(get_post_meta($post_id, '_ppar_ebay_business_auto', true)) !== 1) { return false; }
        $identity = strtolower(sanitize_text_field((string)get_post_meta($post_id, '_ppar_creative_identity_hash', true)));
        if (!preg_match('/^[a-f0-9]{64}$/', $identity) || !method_exists($this, 'output_creative_row')) { return false; }
        $row = $this->output_creative_row($identity);
        if (!is_array($row)
            || sanitize_key((string)($row['provider'] ?? '')) !== 'ebay'
            || sanitize_key((string)($row['source_kind'] ?? '')) !== 'ebay_business_item'
            || sanitize_key((string)($row['source_status'] ?? 'active')) !== 'active'
            || sanitize_key((string)($row['availability_state'] ?? 'active')) !== 'active') { return false; }

        $row_image = esc_url_raw((string)($row['image_url'] ?? ''));
        if ($row_image === '' || stripos($row_image, 'https://') !== 0) { return false; }
        if (method_exists($this, 'ebay_remote_image_url_validate') && $this->ebay_remote_image_url_validate($row_image) === '') { return false; }
        // The materialized campaign may still carry yesterday's eBay CDN URL.
        // The active source row is canonical for the current image; requiring URL
        // equality here would preserve exactly the stale/broken-image failure.


        // V6.61.4: Do not re-introduce the V6.17/V6.18 blocker. A fresh eBay
        // BUSINESS row may legitimately be dimension_state=pending internally.
        // Public output performs its own current HTTP+image validation below.
        return $row;
    }

    /**
     * V6.61.5: Resolve the image URL used by a public eBay product card without
     * performing network I/O during page rendering. The active BUSINESS source
     * row is preferred so stale campaign CDN URLs cannot win. If a historical
     * campaign temporarily has no resolvable source row, its own URL remains a
     * compatibility fallback only when it still passes the eBay host validator.
     */
    private function ebay_product_public_image_url($campaign) {
        if (!is_array($campaign) || sanitize_key((string)($campaign['network'] ?? '')) !== 'ebay') { return ''; }
        if (sanitize_key((string)($campaign['source'] ?? '')) === 'output_object_v4') {
            $row = $this->ebay_product_public_source_row($campaign);
            if (is_array($row)) {
                $current = esc_url_raw((string)($row['image_url'] ?? ''));
                if ($current !== '' && stripos($current, 'https://') === 0
                    && (!method_exists($this, 'ebay_remote_image_url_validate') || $this->ebay_remote_image_url_validate($current) !== '')) {
                    return $current;
                }
            }
        }
        $fallback = esc_url_raw((string)($campaign['image_url'] ?? ''));
        if ($fallback === '' || stripos($fallback, 'https://') !== 0) { return ''; }
        if (method_exists($this, 'ebay_remote_image_url_validate') && $this->ebay_remote_image_url_validate($fallback) === '') { return ''; }
        return $fallback;
    }

    private function provider_product_image_extension($mime) {
        $mime = strtolower(trim((string)$mime));
        if (strpos($mime, ';') !== false) { $mime = trim(strtok($mime, ';')); }
        $map = array('image/jpeg'=>'jpg','image/jpg'=>'jpg','image/png'=>'png','image/webp'=>'webp','image/gif'=>'gif');
        return $map[$mime] ?? '';
    }

    /**
     * V6.61.4: eBay public cards use a locally cached copy of the CURRENT remote
     * image. Historical dimension/hash metadata is intentionally not a public
     * blocker because V6.18 permits fresh BUSINESS rows to start as pending.
     * A candidate is public only after the current response is a decodable image.
     */
    private function ebay_product_cached_image_url($campaign, $allow_fetch = true) {
        $row = $this->ebay_product_public_source_row($campaign);
        if (!is_array($row)) { return ''; }
        $identity = strtolower(sanitize_text_field((string)get_post_meta(absint($campaign['post_id'] ?? 0), '_ppar_creative_identity_hash', true)));
        $remote_url = esc_url_raw((string)($row['image_url'] ?? ''));
        if (!preg_match('/^[a-f0-9]{64}$/', $identity) || $remote_url === '') { return ''; }
        if (!function_exists('wp_upload_dir')) { return ''; }
        $uploads = wp_upload_dir(null, false);
        if (!is_array($uploads) || !empty($uploads['error']) || empty($uploads['basedir']) || empty($uploads['baseurl'])) { return ''; }
        $dir = rtrim((string)$uploads['basedir'], '/\\') . '/ppar-affiliate-product-images';
        $baseurl = rtrim((string)$uploads['baseurl'], '/') . '/ppar-affiliate-product-images';
        $url_hash = hash('sha256', $remote_url);
        $stem = 'ebay-' . substr($identity, 0, 20) . '-' . substr($url_hash, 0, 32);
        foreach (array('jpg','png','webp','gif') as $ext) {
            $candidate = $dir . '/' . $stem . '.' . $ext;
            if (is_file($candidate) && filesize($candidate) > 0) {
                return esc_url_raw($baseurl . '/' . basename($candidate));
            }
        }
        if (!$allow_fetch || !function_exists('wp_safe_remote_get')) { return ''; }

        $failure_key = 'ppar_ebay_img_fail_' . substr($url_hash, 0, 32);
        if (function_exists('get_transient') && get_transient($failure_key)) { return ''; }
        $response = wp_safe_remote_get($remote_url, array(
            'timeout'=>5,
            'redirection'=>3,
            'headers'=>array('Accept'=>'image/avif,image/webp,image/apng,image/*,*/*;q=0.8'),
            'limit_response_size'=>4194304,
        ));
        if (function_exists('is_wp_error') && is_wp_error($response)) {
            if (function_exists('set_transient')) { set_transient($failure_key, 1, HOUR_IN_SECONDS); }
            return '';
        }
        $code = function_exists('wp_remote_retrieve_response_code') ? absint(wp_remote_retrieve_response_code($response)) : 0;
        $body = function_exists('wp_remote_retrieve_body') ? (string)wp_remote_retrieve_body($response) : '';
        if ($code < 200 || $code >= 300 || $body === '' || strlen($body) > 4194304) {
            if (function_exists('set_transient')) { set_transient($failure_key, 1, HOUR_IN_SECONDS); }
            return '';
        }
        $size = function_exists('getimagesizefromstring') ? @getimagesizefromstring($body) : false;
        if (!is_array($size) || absint($size[0] ?? 0) <= 0 || absint($size[1] ?? 0) <= 0) {
            if (function_exists('set_transient')) { set_transient($failure_key, 1, HOUR_IN_SECONDS); }
            return '';
        }
        $actual_mime = strtolower((string)($size['mime'] ?? ''));
        if ($actual_mime === '' && function_exists('wp_remote_retrieve_header')) { $actual_mime = strtolower((string)wp_remote_retrieve_header($response, 'content-type')); }
        $ext = $this->provider_product_image_extension($actual_mime);
        if ($ext === '') {
            if (function_exists('set_transient')) { set_transient($failure_key, 1, HOUR_IN_SECONDS); }
            return '';
        }
        if (!is_dir($dir) && (!function_exists('wp_mkdir_p') || !wp_mkdir_p($dir))) { return ''; }
        $file = $dir . '/' . $stem . '.' . $ext;
        $tmp = $file . '.tmp-' . substr(hash('sha256', uniqid('', true)), 0, 12);
        $written = @file_put_contents($tmp, $body, LOCK_EX);
        if ($written !== strlen($body) || !@rename($tmp, $file)) { @unlink($tmp); return ''; }
        @chmod($file, 0644);
        if (function_exists('delete_transient')) { delete_transient($failure_key); }
        return esc_url_raw($baseurl . '/' . basename($file));
    }

    private function product_campaign_public_image_ready($campaign) {
        if (!is_array($campaign) || sanitize_key((string)($campaign['creative_type'] ?? '')) !== 'product') { return true; }
        $title = trim((string)($campaign['title'] ?? ''));
        $network = sanitize_key((string)($campaign['network'] ?? ''));
        $source = sanitize_key((string)($campaign['source'] ?? ''));
        $image = esc_url_raw((string)($campaign['image_url'] ?? ''));
        if ($network === 'idealo' && method_exists($this, 'multiprovider_runtime_image_url')) {
            $image = $this->multiprovider_runtime_image_url($image, 'idealo', absint($campaign['post_id'] ?? 0));
        } elseif ($network === 'ebay' && method_exists($this, 'ebay_product_public_image_url')) {
            $image = $this->ebay_product_public_image_url($campaign);
        }
        if ($title === '' || $image === '' || stripos($image, 'https://') !== 0) { return false; }
        if (function_exists('wp_http_validate_url') && !wp_http_validate_url($image)) { return false; }
        // V6.61.5: never remove a provider from the page because the WordPress
        // server cannot hot-fetch its image at render time. Candidate supply is
        // decided from canonical, provider-validated image URLs; browser loading
        // no longer controls whether eBay/idealo cards exist at all.
        return true;
    }

    private function ranked_campaigns_for_slot($context, $slot_type, $forced_campaign_id = '') {
        $candidates = array();
        foreach ($this->get_campaigns() as $campaign) {
            // Cheap eligibility/match checks first. V6.19 evaluated control and
            // health gates for the entire BUSINESS campaign inventory on every
            // product slot even when a campaign could not match the current page.
            // Preserve the same gates, but execute their DB/meta work only for
            // campaigns that are actually eligible for this context.
            if (!is_array($campaign) || empty($campaign['active']) || !$this->campaign_is_complete($campaign) || !$this->rule_is_current($campaign) || !$this->campaign_program_allows_delivery($campaign)) {
                continue;
            }
            if ($forced_campaign_id !== '' && sanitize_key((string) ($campaign['id'] ?? '')) !== sanitize_key($forced_campaign_id)) {
                continue;
            }
            if (!$this->campaign_slot_allowed($campaign, $slot_type)) { continue; }
            $required_type = $this->slot_required_creative_type($slot_type);
            if ($required_type !== '' && sanitize_key((string)($campaign['creative_type'] ?? 'banner')) !== $required_type) { continue; }
            $rank_context = $context;
            $rank_context['slot_type'] = sanitize_key((string) $slot_type);
            $rank = $this->campaign_match_rank($campaign, $rank_context);
            if (!$rank) { continue; }
            if (!$this->campaign_control_allows_delivery($campaign, $slot_type ?? '') || !$this->campaign_health_allows_delivery($campaign)) { continue; }
            $candidates[] = array(
                'campaign' => $campaign,
                'specificity' => (int) $rank['specificity'],
                'matches' => (int) $rank['matches'],
                'priority' => (int) ($campaign['priority'] ?? 0),
                'reason' => (string) $rank['reason'],
            );
        }
        usort($candidates, function($a, $b) {
            foreach (array('specificity', 'matches', 'priority') as $key) {
                if ($a[$key] !== $b[$key]) {
                    return ($a[$key] > $b[$key]) ? -1 : 1;
                }
            }
            return strcmp((string) ($a['campaign']['id'] ?? ''), (string) ($b['campaign']['id'] ?? ''));
        });
        if ($this->slot_required_creative_type($slot_type) === 'product' && method_exists($this, 'ebay_filter_ranked_product_candidates_provider_cohort')) {
            $candidates = $this->ebay_filter_ranked_product_candidates_provider_cohort($candidates);
        }
        if ($this->slot_required_creative_type($slot_type) === 'product' && method_exists($this, 'multiprovider_filter_candidates_by_strategy')) {
            $candidates = $this->multiprovider_filter_candidates_by_strategy($candidates);
        }
        // V6.61.5: verify structural image readiness only after final provider
        // strategy. This remains a cheap URL/source check: page rendering must not
        // hot-fetch provider images and thereby make whole eBay cohorts vanish.
        if ($this->slot_required_creative_type($slot_type) === 'product') {
            $image_ready = array();
            foreach ($candidates as $candidate) {
                $campaign = is_array($candidate) ? ($candidate['campaign'] ?? null) : null;
                if (!is_array($campaign) || !$this->product_campaign_public_image_ready($campaign)) { continue; }
                $image_ready[] = $candidate;
            }
            $candidates = $image_ready;
        }
        return $candidates;
    }
    private function select_campaign_for_slot($context, $slot_type, $forced_campaign_id = '') {
        $candidates = $this->ranked_campaigns_for_slot($context, $slot_type, $forced_campaign_id);
        if (empty($candidates)) { return null; }
        $index = $this->category_product_slot_index($slot_type);
        return $index > 0 ? ($candidates[$index - 1] ?? null) : $candidates[0];
    }

    /**
     * Liefert fuer Endkategorien die Kampagne an Position 1 oder 2 der zentralen
     * Prioritaetsreihenfolge. Dadurch werden niemals zwei identische Anzeigen ausgegeben.
     */
    private function select_campaign_for_slot_position($context, $slot_type, $position = 1) {
        $position = max(1, min(2, (int) $position));
        $candidates = $this->ranked_campaigns_for_slot($context, $slot_type);
        return $candidates[$position - 1] ?? null;
    }

    private function campaign_to_group_banner($campaign) {
        $groups = $this->campaigns_to_groups(array($campaign));
        if (empty($groups[0]['banners'][0])) {
            return array(null, null);
        }
        return array($groups[0], $groups[0]['banners'][0]);
    }

    private function get_auto_slots() {
        $slots = get_option(self::OPTION_AUTO_SLOTS, array());
        if (!is_array($slots)) {
            return array();
        }
        return array_values(array_intersect(array_map('sanitize_key', $slots), $this->allowed_auto_slots()));
    }

    private function allowed_auto_slots() {
        return array('top_info', 'mid_content', 'bottom_recommendation', 'post_after_intro', 'post_mid_content', 'post_bottom_recommendation');
    }

    private function is_category_archive_enabled() {
        return get_option(self::OPTION_CATEGORY_ENABLED, '0') === '1';
    }

    private function get_category_slots() {
        $slots = get_option(self::OPTION_CATEGORY_SLOTS, array());
        if (!is_array($slots)) {
            return array();
        }
        return array_values(array_intersect(array_map('sanitize_key', $slots), $this->allowed_category_slots()));
    }

    private function allowed_category_slots() {
        return array('category_recommendation');
    }

    private function auto_slot_enabled($active_slots, $aliases) {
        return !empty(array_intersect($active_slots, $aliases));
    }
    private function equivalent_slot_names($slot_type) {
        $slot_type = sanitize_key($slot_type);
        if (preg_match('/^category_product_[123]$/', $slot_type)) {
            return array($slot_type, 'category_product');
        }
        $groups = array(
            array('top_info', 'post_after_intro'),
            array('mid_content', 'post_mid_content', 'post_inline_banner'),
            array('bottom_recommendation', 'post_bottom_recommendation', 'post_bottom_products'),
            array('hub_top_cta', 'template_top', 'template_after_intro'),
            array('hub_after_cards', 'template_after_selected', 'template_mid'),
            array('hub_grid_card'),
            array('hub_mid_banner', 'template_mid_banner'),
            array('category_recommendation', 'produkt_recommendation', 'template_bottom', 'product_after_category_tiles'),
        );
        foreach ($groups as $group) { if (in_array($slot_type, $group, true)) { return $group; } }
        return array($slot_type);
    }

    private function allowed_match_modes() {
        return array('auto', 'exact_slug', 'keyword', 'fallback');
    }

    private function match_mode_label($mode) {
        $labels = array(
            'auto' => 'Automatisch: Slug + Keyword',
            'exact_slug' => 'Eng: nur exakter Slug',
            'keyword' => 'Breit: Keyword-Matching',
            'fallback' => 'Fallback: nur wenn nichts Spezifisches passt',
        );
        $mode = sanitize_key((string) $mode);
        return isset($labels[$mode]) ? $labels[$mode] : $labels['auto'];
    }

    private function allowed_workflow_statuses() {
        return array('offen', 'geprueft', 'ignorieren', 'fehler');
    }

    private function workflow_status_label($status) {
        $labels = array(
            'offen' => 'offen',
            'geprueft' => 'geprüft',
            'ignorieren' => 'ignorieren',
            'fehler' => 'Fehler',
        );
        $status = sanitize_key((string) $status);
        return isset($labels[$status]) ? $labels[$status] : $labels['offen'];
    }

    private function is_enabled() {
        return get_option(self::OPTION_ENABLED, '0') === '1' && (!method_exists($this, 'control_emergency_stop_active') || !$this->control_emergency_stop_active());
    }

    /* ---------------------------------------------------------------------
     * Portal-Template-Router fuer Startseite, Hubseiten, Produktseiten
     * ------------------------------------------------------------------ */

    public function shortcode_portal_overview($atts) {
        $atts = shortcode_atts(array(
            'context' => '',
            'part' => 'auto',
        ), $atts, 'pp_portal_overview');

        $post_id = get_the_ID();
        if (!$post_id) {
            return '';
        }

        $context = sanitize_key($atts['context']);
        if ($context === '') {
            $context = $this->get_current_template_context($post_id);
        }

        return $this->render_portal_template($post_id, $context, sanitize_key($atts['part']), true);
    }

    /**
     * Sichere Hub-/Startseiten-Affiliate-Ausgabe.
     * V0.7: Keine automatische Voll-Template-Injection mehr.
     * Der Design-Teil steuert Layout/Karten; der Router füllt nur Affiliate-Slots.
     */
    public function auto_inject_template_affiliate_slots($content) {
        if (!$this->is_enabled() || !$this->is_template_enabled()) {
            return $content;
        }
        if (is_admin() || is_feed() || is_preview()) {
            return $content;
        }
        if (!in_the_loop() || !is_main_query()) {
            return $content;
        }
        if (!is_singular('page') && !is_front_page()) {
            return $content;
        }

        $post_id = get_the_ID();
        if (!$post_id || post_password_required($post_id)) {
            return $content;
        }

        // V2.2.3: Automatisch vom Designplugin verwaltete Portal-Seiten duerfen
        // niemals zusaetzliche alte Template-Slots aus dem Router erhalten.
        // Die integrierten Rasterkarten werden ausschliesslich ueber den Datenfilter befuellt.
        if (class_exists('Pferde_Template_Kit') && is_callable(array('Pferde_Template_Kit', 'affiliate_page_type'))) {
            $design_type = (string) Pferde_Template_Kit::affiliate_page_type($post_id);
            if (in_array($design_type, array('start', 'hub1', 'hub2', 'category'), true)) {
                return $content . $this->debug_comment('design_auto_layout_protected', $post_id, $design_type, '', '');
            }
        }

        // Harte Schutzregel V0.7:
        // Wenn eine Seite bereits durch das Design-Plugin/Shortcodes gerendert wird,
        // darf der Affiliate-Router kein eigenes Hub-Layout injizieren. Die im Design
        // vorhandenen Slots rufen [pp_affiliate_slot] selbst auf.
        $raw_post_content = (string) get_post_field('post_content', $post_id);
        if ($this->content_has_design_template_shortcode($raw_post_content)) {
            return $content . $this->debug_comment('template_design_shortcode_protected', $post_id, '', '', '');
        }

        // Keine Dopplung, wenn bewusst einzelne Slots im Seiteninhalt stehen.
        if (has_shortcode($raw_post_content, 'pp_affiliate_slot') || has_shortcode($raw_post_content, 'affiliate_portal_slot')) {
            return $content;
        }

        $context = $this->get_current_template_context($post_id);
        if ($context === '') {
            return $content;
        }

        $enabled_contexts = $this->get_template_contexts();
        if (!in_array($context, $enabled_contexts, true)) {
            return $content;
        }

        $rules = $this->get_template_rules();
        $rule = isset($rules[$context]) && is_array($rules[$context]) ? $rules[$context] : array();
        if (empty($rule) || (isset($rule['active']) && empty($rule['active']))) {
            return $content;
        }

        $placements = !empty($rule['affiliate_slots']) && is_array($rule['affiliate_slots']) ? array_map('sanitize_key', $rule['affiliate_slots']) : array();
        if (empty($placements)) {
            return $content;
        }

        $result = $content;

        if (in_array('top_cta', $placements, true)) {
            $slot = $this->render_template_affiliate_slot($post_id, $context, $rule, 'top_cta');
            if ($slot !== '') {
                $result = $this->insert_after_paragraph($result, $slot, 1);
            }
        }
        if (in_array('after_selected', $placements, true)) {
            $slot = $this->render_template_affiliate_slot($post_id, $context, $rule, 'after_selected');
            if ($slot !== '') {
                $result .= "\n" . $slot;
            }
        }
        if (in_array('after_hint', $placements, true)) {
            $slot = $this->render_template_affiliate_slot($post_id, $context, $rule, 'after_hint');
            if ($slot !== '') {
                $result .= "\n" . $slot;
            }
        }
        if (in_array('bottom', $placements, true)) {
            $slot = $this->render_template_affiliate_slot($post_id, $context, $rule, 'bottom');
            if ($slot !== '') {
                $result .= "\n" . $slot;
            }
        }

        return $result;
    }

    private function content_has_design_template_shortcode($content) {
        $shortcodes = array(
            'pferde_startseite',
            'pferde_startseite_only',
            'pferde_hub_ebene_1',
            'pferde_hauptseite',
            'pferde_hub_ebene_2',
            'pferde_hub_auto',
            'affiliate_portal_startseite',
            'affiliate_portal_hub_1',
            'affiliate_portal_hub_2',
            'affiliate_portal_hub_auto',
            'affiliate_portal_kategorie',
            'affiliate_portal_produkt',
            'pferde_template_oben',
            'pferde_template_unten',
            'pferde_banner'
        );
        foreach ($shortcodes as $shortcode) {
            if (has_shortcode($content, $shortcode)) {
                return true;
            }
        }
        return false;
    }


    private function get_design_template_type_from_content($content) {
        $map = array(
            'start' => array('pferde_startseite', 'pferde_startseite_only', 'affiliate_portal_startseite'),
            'hub1' => array('pferde_hub_ebene_1', 'pferde_hauptseite', 'affiliate_portal_hub_1'),
            'hub2' => array('pferde_hub_ebene_2', 'pferde_hub_auto', 'affiliate_portal_hub_2', 'affiliate_portal_hub_auto'),
            'category' => array('affiliate_portal_kategorie', 'affiliate_portal_produkt'),
        );
        foreach ($map as $type => $shortcodes) {
            foreach ($shortcodes as $shortcode) {
                if (has_shortcode($content, $shortcode)) {
                    return $type;
                }
            }
        }
        return '';
    }

    private function is_design_slot_visible_for_content($content, $slot) {
        $type = $this->get_design_template_type_from_content($content);
        if ($type === '') {
            return false;
        }
        $prefix_map = array(
            'start' => 'pftk_start_blocks',
            'hub1' => 'pftk_hub1_blocks',
            'hub2' => 'pftk_hub2_blocks',
            'category' => 'pftk_category_blocks',
        );
        if (empty($prefix_map[$type])) {
            return false;
        }
        $option = get_option($prefix_map[$type], array());
        if (!is_array($option)) {
            $option = array();
        }
        $slot_key = 'show_slot_' . sanitize_key($slot);
        $default_on = in_array(sanitize_key($slot), array('hub_top_cta', 'hub_after_cards', 'category_recommendation', 'product_after_category_tiles'), true);
        $value = isset($option[$slot_key]) ? (string) $option[$slot_key] : ($default_on ? '1' : '0');
        return $value === '1';
    }

    public function auto_inject_template_blocks($content) {
        if (!$this->is_template_enabled()) {
            return $content;
        }
        if (is_admin() || is_feed() || is_preview()) {
            return $content;
        }
        if (!in_the_loop() || !is_main_query()) {
            return $content;
        }
        if (!is_singular('page') && !is_front_page()) {
            return $content;
        }

        $post_id = get_the_ID();
        if (!$post_id || post_password_required($post_id)) {
            return $content;
        }

        if (has_shortcode($content, 'pp_portal_overview')) {
            return $content;
        }

        $context = $this->get_current_template_context($post_id);
        if ($context === '') {
            return $content;
        }

        $enabled_contexts = $this->get_template_contexts();
        if (!in_array($context, $enabled_contexts, true)) {
            return $content;
        }

        $rules = $this->get_template_rules();
        $rule = isset($rules[$context]) && is_array($rules[$context]) ? $rules[$context] : array();
        if (isset($rule['active']) && empty($rule['active'])) {
            return $content;
        }

        $block = $this->render_portal_template($post_id, $context, 'auto', false);
        if (trim($block) === '') {
            return $content;
        }

        $insert_position = isset($rule['insert_position']) ? sanitize_key($rule['insert_position']) : 'after_intro';
        if ($insert_position === 'prepend') {
            return $block . "\n" . $content;
        }
        if ($insert_position === 'append') {
            return $content . "\n" . $block;
        }

        return $this->insert_after_paragraph($content, $block, 1);
    }

    private function get_current_template_context($post_id) {
        if (is_front_page()) {
            return 'startseite';
        }
        if (!is_singular('page')) {
            return '';
        }
        return $this->get_template_context_for_page_id($post_id, false);
    }

    /**
     * Admin-sichere Portalrollen-Erkennung.
     * V1.0: Das Kontrollzentrum darf nicht von Frontend-Conditionals wie is_singular() abhängen.
     */
    private function get_template_context_for_page_id($post_id, $is_front = false) {
        $post_id = (int) $post_id;
        if ($post_id <= 0) {
            return '';
        }
        if ($is_front) {
            return 'startseite';
        }
        if (get_post_type($post_id) !== 'page') {
            return '';
        }

        $manual_role = sanitize_key((string) get_post_meta($post_id, '_ppar_portal_role', true));
        if (in_array($manual_role, $this->allowed_template_contexts(), true)) {
            return $manual_role;
        }
        if ($manual_role === 'none') {
            return '';
        }

        $ancestors = get_post_ancestors($post_id);
        $depth = is_array($ancestors) ? count($ancestors) : 0;

        if ($depth === 0) {
            return 'haupt_hub_ebene_1';
        }
        if ($depth === 1) {
            return 'bereichs_hub_ebene_2';
        }
        return 'produktseite_ebene_3';
    }

    private function render_portal_template($post_id, $context, $part = 'auto', $shortcode_call = false) {
        $context = sanitize_key($context);
        if (!in_array($context, $this->allowed_template_contexts(), true)) {
            return '';
        }

        $rules = $this->get_template_rules();
        $rule = isset($rules[$context]) && is_array($rules[$context]) ? $rules[$context] : array();
        if (empty($rule)) {
            return $this->debug_comment('template_missing_rule', $post_id, $context, '', '');
        }
        if (!$shortcode_call && isset($rule['active']) && empty($rule['active'])) {
            return '';
        }

        $items = $this->get_template_items($post_id, $context, $rule);
        if (empty($items)) {
            return $this->debug_comment('template_no_items', $post_id, $context, '', '');
        }

        $selected_limit = isset($rule['selected_limit']) ? max(0, (int) $rule['selected_limit']) : 6;
        $selected = $this->select_template_items($items, $rule, $selected_limit);
        $has_more = count($items) > count($selected);
        $force_hint = !empty($rule['force_hint']);

        $show_selected = !isset($rule['show_selected']) || !empty($rule['show_selected']);
        $show_hint = (!isset($rule['show_hint']) || !empty($rule['show_hint'])) && ($has_more || $force_hint);
        $show_full = !empty($rule['show_full_overview']);

        if ($part === 'selected') {
            $show_hint = false;
            $show_full = false;
        } elseif ($part === 'hint') {
            $show_selected = false;
            $show_full = false;
        } elseif ($part === 'full') {
            $show_selected = false;
            $show_hint = false;
            $show_full = true;
        }

        if (!$show_selected && !$show_hint && !$show_full) {
            return '';
        }

        $anchor = $this->get_overview_anchor($post_id, $context, $rule);
        $out = '<section class="ppar-template-router ppar-template-' . esc_attr($context) . '" data-ppar-template-context="' . esc_attr($context) . '">';
        $out .= $this->render_template_affiliate_slot($post_id, $context, $rule, 'top_cta');

        if ($show_selected && !empty($selected)) {
            $heading = $this->replace_template_tokens((string) ($rule['selected_heading'] ?? 'Ausgewählte Themen'), $post_id, $context, $rule);
            $out .= '<div class="ppar-template-selected">';
            $out .= '<h2 class="ppar-template-heading">' . esc_html($heading) . '</h2>';
            $out .= '<div class="ppar-template-grid">';
            foreach ($selected as $item) {
                $out .= $this->render_template_item_card($item, $rule);
            }
            $out .= '</div>';
            $out .= '</div>';
            $out .= $this->render_template_affiliate_slot($post_id, $context, $rule, 'after_selected');
        }

        if ($show_hint) {
            $heading = $this->replace_template_tokens((string) ($rule['hint_heading'] ?? 'Weitere Themen entdecken'), $post_id, $context, $rule);
            $text = $this->replace_template_tokens((string) ($rule['hint_text'] ?? 'Die angezeigten Themen sind nur eine Auswahl.'), $post_id, $context, $rule);
            $button_text = $this->replace_template_tokens((string) ($rule['button_text'] ?? 'Zur vollständigen Übersicht'), $post_id, $context, $rule);
            $button_url = '#' . $anchor;
            if (!empty($rule['button_url'])) {
                $button_url = $this->replace_template_tokens((string) $rule['button_url'], $post_id, $context, $rule);
            }
            $out .= '<div class="ppar-template-hint">';
            $out .= '<h2 class="ppar-template-hint-heading">' . esc_html($heading) . '</h2>';
            if ($text !== '') {
                $out .= '<p>' . esc_html($text) . '</p>';
            }
            if ($button_text !== '') {
                $out .= '<a class="ppar-template-button" href="' . esc_url($button_url) . '">' . esc_html($button_text) . '</a>';
            }
            $out .= '</div>';
            $out .= $this->render_template_affiliate_slot($post_id, $context, $rule, 'after_hint');
        }

        if ($show_full) {
            $heading = $this->replace_template_tokens((string) ($rule['full_heading'] ?? 'Vollständige Übersicht'), $post_id, $context, $rule);
            $out .= '<div class="ppar-template-full" id="' . esc_attr($anchor) . '">';
            $out .= '<h2 class="ppar-template-heading">' . esc_html($heading) . '</h2>';
            $out .= '<ul class="ppar-template-list">';
            foreach ($items as $item) {
                $out .= $this->render_template_item_list_entry($item, $rule);
            }
            $out .= '</ul>';
            $out .= '</div>';
            $out .= $this->render_template_affiliate_slot($post_id, $context, $rule, 'after_full');
        }

        $out .= '</section>';
        $out .= $this->debug_comment('template_rendered', $post_id, $context, '', '');

        return $out;
    }

    private function get_template_items($post_id, $context, $rule) {
        if (!empty($rule['manual_items']) && is_array($rule['manual_items'])) {
            return $this->normalize_manual_items($rule['manual_items']);
        }

        $source = isset($rule['source']) ? sanitize_key($rule['source']) : '';
        if ($source === '') {
            $source = ($context === 'startseite') ? 'top_level_pages' : (($context === 'produktseite_ebene_3') ? 'related_categories' : 'child_pages');
        }

        if ($source === 'top_level_pages') {
            return $this->get_top_level_page_items($post_id, $rule);
        }
        if ($source === 'child_pages') {
            return $this->get_child_page_items($post_id, $rule);
        }
        if ($source === 'related_categories') {
            return $this->get_related_category_items($post_id, $rule);
        }
        if ($source === 'child_pages_then_categories') {
            $items = $this->get_child_page_items($post_id, $rule);
            if (!empty($items)) {
                return $items;
            }
            return $this->get_related_category_items($post_id, $rule);
        }

        return array();
    }

    private function normalize_manual_items($manual_items) {
        $items = array();
        foreach ($manual_items as $index => $item) {
            if (!is_array($item)) {
                continue;
            }
            $title = isset($item['title']) ? trim((string) $item['title']) : '';
            $url = isset($item['url']) ? trim((string) $item['url']) : '';
            if ($title === '' || $url === '') {
                continue;
            }
            $items[] = array(
                'title' => $title,
                'url' => $url,
                'description' => isset($item['description']) ? trim((string) $item['description']) : '',
                'slug' => isset($item['slug']) ? sanitize_key($item['slug']) : sanitize_key($title),
                'type' => isset($item['type']) ? sanitize_key($item['type']) : 'manual',
                'priority' => isset($item['priority']) ? (int) $item['priority'] : (1000 - (int) $index),
            );
        }
        return $this->sort_template_items($items);
    }

    private function get_top_level_page_items($current_post_id, $rule) {
        $pages = get_pages(array(
            'parent' => 0,
            'sort_column' => 'menu_order,post_title',
            'sort_order' => 'ASC',
            'post_status' => 'publish',
        ));
        if (!is_array($pages)) {
            return array();
        }

        $front_id = (int) get_option('page_on_front');
        $posts_id = (int) get_option('page_for_posts');
        $exclude_ids = array_filter(array($front_id, $posts_id));
        if (!empty($rule['exclude_page_ids']) && is_array($rule['exclude_page_ids'])) {
            foreach ($rule['exclude_page_ids'] as $id) {
                $exclude_ids[] = (int) $id;
            }
        }

        $items = array();
        foreach ($pages as $page) {
            if (in_array((int) $page->ID, $exclude_ids, true)) {
                continue;
            }
            $items[] = array(
                'title' => get_the_title($page->ID),
                'url' => get_permalink($page->ID),
                'description' => $this->get_page_excerpt($page->ID),
                'slug' => sanitize_key($page->post_name),
                'type' => 'page',
                'priority' => isset($page->menu_order) ? 1000 - (int) $page->menu_order : 0,
            );
        }
        return $this->sort_template_items($items);
    }

    private function get_child_page_items($post_id, $rule) {
        $pages = get_pages(array(
            'parent' => $post_id,
            'sort_column' => 'menu_order,post_title',
            'sort_order' => 'ASC',
            'post_status' => 'publish',
        ));

        if (empty($pages) && !empty($rule['include_all_descendants'])) {
            $pages = get_pages(array(
                'child_of' => $post_id,
                'sort_column' => 'menu_order,post_title',
                'sort_order' => 'ASC',
                'post_status' => 'publish',
            ));
        }

        if (!is_array($pages)) {
            return array();
        }

        $items = array();
        foreach ($pages as $page) {
            $items[] = array(
                'title' => get_the_title($page->ID),
                'url' => get_permalink($page->ID),
                'description' => $this->get_page_excerpt($page->ID),
                'slug' => sanitize_key($page->post_name),
                'type' => 'page',
                'priority' => isset($page->menu_order) ? 1000 - (int) $page->menu_order : 0,
            );
        }
        return $this->sort_template_items($items);
    }

    private function get_related_category_items($post_id, $rule) {
        $page_slug = sanitize_title((string) get_post_field('post_name', $post_id));
        $page_title_slug = sanitize_title((string) get_the_title($post_id));
        $explicit_slugs = !empty($rule['related_category_slugs']) && is_array($rule['related_category_slugs']) ? array_map('sanitize_key', $rule['related_category_slugs']) : array();

        $terms = get_categories(array(
            'hide_empty' => false,
            'orderby' => 'name',
            'order' => 'ASC',
            'number' => 500,
        ));
        if (!is_array($terms)) {
            return array();
        }

        $items = array();
        foreach ($terms as $term) {
            $slug = sanitize_key($term->slug);
            $matches = false;

            if (!empty($explicit_slugs) && in_array($slug, $explicit_slugs, true)) {
                $matches = true;
            }
            if (!$matches && $page_slug !== '' && strpos($slug, sanitize_key($page_slug)) !== false) {
                $matches = true;
            }
            if (!$matches && $page_title_slug !== '' && strpos($slug, sanitize_key($page_title_slug)) !== false) {
                $matches = true;
            }

            if (!$matches) {
                continue;
            }

            $url = get_category_link($term->term_id);
            if (is_wp_error($url)) {
                continue;
            }

            $items[] = array(
                'title' => $term->name,
                'url' => $url,
                'description' => trim((string) $term->description),
                'slug' => $slug,
                'type' => 'category',
                'priority' => 500,
            );
        }

        return $this->sort_template_items($items);
    }

    private function get_page_excerpt($page_id) {
        $excerpt = trim((string) get_post_field('post_excerpt', $page_id));
        if ($excerpt !== '') {
            return $excerpt;
        }
        $content = trim((string) get_post_field('post_content', $page_id));
        if ($content === '') {
            return '';
        }
        return wp_trim_words(wp_strip_all_tags($content), 22, ' …');
    }

    private function select_template_items($items, $rule, $limit) {
        if ($limit <= 0) {
            return array();
        }

        $selected_slugs = !empty($rule['selected_slugs']) && is_array($rule['selected_slugs']) ? array_map('sanitize_key', $rule['selected_slugs']) : array();
        if (!empty($selected_slugs)) {
            $by_slug = array();
            foreach ($items as $item) {
                $by_slug[$item['slug']] = $item;
            }
            $selected = array();
            foreach ($selected_slugs as $slug) {
                if (isset($by_slug[$slug])) {
                    $selected[] = $by_slug[$slug];
                }
                if (count($selected) >= $limit) {
                    break;
                }
            }
            if (!empty($selected)) {
                return $selected;
            }
        }

        return array_slice($items, 0, $limit);
    }

    private function sort_template_items($items) {
        usort($items, function($a, $b) {
            $pa = isset($a['priority']) ? (int) $a['priority'] : 0;
            $pb = isset($b['priority']) ? (int) $b['priority'] : 0;
            if ($pa !== $pb) {
                return $pb <=> $pa;
            }
            return strcasecmp($a['title'] ?? '', $b['title'] ?? '');
        });
        return $items;
    }

    private function render_template_item_card($item, $rule) {
        $design = $this->get_design_rules();
        $show_description = isset($rule['card_show_description']) ? !empty($rule['card_show_description']) : !empty($design['card_show_description']);
        $out = '<a class="ppar-template-card" href="' . esc_url($item['url']) . '">';
        $out .= '<span class="ppar-template-card-title">' . esc_html($item['title']) . '</span>';
        if ($show_description && !empty($item['description'])) {
            $limit = isset($design['card_description_words']) ? max(4, (int) $design['card_description_words']) : 14;
            $out .= '<span class="ppar-template-card-description">' . esc_html(wp_trim_words($item['description'], $limit, ' …')) . '</span>';
        }
        $out .= '</a>';
        return $out;
    }

    private function render_template_item_list_entry($item, $rule) {
        $design = $this->get_design_rules();
        $show_description = isset($rule['list_show_description']) ? !empty($rule['list_show_description']) : !empty($design['list_show_description']);
        $out = '<li class="ppar-template-list-entry ppar-template-item-' . esc_attr($item['type']) . '">';
        $out .= '<a href="' . esc_url($item['url']) . '">' . esc_html($item['title']) . '</a>';
        if ($show_description && !empty($item['description'])) {
            $limit = isset($design['list_description_words']) ? max(4, (int) $design['list_description_words']) : 16;
            $out .= '<span>' . esc_html(wp_trim_words($item['description'], $limit, ' …')) . '</span>';
        }
        $out .= '</li>';
        return $out;
    }

    private function render_template_affiliate_slot($post_id, $context, $rule, $placement) {
        $placements = !empty($rule['affiliate_slots']) && is_array($rule['affiliate_slots']) ? array_map('sanitize_key', $rule['affiliate_slots']) : array();
        if (!in_array(sanitize_key($placement), $placements, true)) {
            return '';
        }
        $forced_group = !empty($rule['affiliate_group']) ? sanitize_key($rule['affiliate_group']) : '';
        $slot_map = array(
            'top_cta' => 'hub_top_cta',
            'after_selected' => 'hub_after_cards',
            'after_hint' => 'hub_mid_banner',
            'bottom' => 'category_recommendation',
        );
        $slot_type = isset($slot_map[$placement]) ? $slot_map[$placement] : 'template_' . sanitize_key($placement);
        return $this->render_affiliate_slot($post_id, $slot_type, 'primary_product', $forced_group);
    }

    private function replace_template_tokens($text, $post_id, $context, $rule) {
        $site_name = get_bloginfo('name');
        $thema = ($context === 'startseite') ? 'Pferdeportal' : get_the_title($post_id);
        $replacements = array(
            '{thema}' => $thema,
            '{site_name}' => $site_name,
            '{context}' => $context,
        );
        return strtr($text, $replacements);
    }

    private function get_overview_anchor($post_id, $context, $rule) {
        if (!empty($rule['button_anchor'])) {
            return sanitize_title((string) $rule['button_anchor']);
        }
        return 'ppar-vollstaendige-uebersicht-' . sanitize_key($context) . '-' . (int) $post_id;
    }

    private function is_template_enabled() {
        return get_option(self::OPTION_TEMPLATE_ENABLED, '0') === '1';
    }

    private function get_template_contexts() {
        $contexts = get_option(self::OPTION_TEMPLATE_CONTEXTS, array());
        if (!is_array($contexts)) {
            return array();
        }
        return array_values(array_intersect(array_map('sanitize_key', $contexts), $this->allowed_template_contexts()));
    }

    private function allowed_template_contexts() {
        return array('startseite', 'haupt_hub_ebene_1', 'bereichs_hub_ebene_2', 'produktseite_ebene_3');
    }

    private function allowed_template_affiliate_placements() {
        return array('top_cta', 'after_selected', 'after_hint', 'bottom');
    }

    private function get_template_rules() {
        $json = (string) get_option(self::OPTION_TEMPLATE_RULES_JSON, self::default_template_rules_json());
        $data = json_decode($json, true);
        if (!is_array($data)) {
            return array();
        }
        return $data;
    }

    private function validate_template_rules($data) {
        if (!is_array($data)) {
            return false;
        }
        foreach ($data as $context => $rule) {
            if (!in_array(sanitize_key((string) $context), $this->allowed_template_contexts(), true)) {
                continue;
            }
            if (!is_array($rule)) {
                return false;
            }
            foreach (array('button_text', 'selected_heading', 'hint_heading', 'full_heading') as $key) {
                if (isset($rule[$key]) && trim((string) $rule[$key]) === 'Alle') {
                    return 'word_alle';
                }
            }
        }
        return true;
    }

    /* ---------------------------------------------------------------------
     * Gemeinsame Hilfen / Admin
     * ------------------------------------------------------------------ */

    private function insert_after_paragraph($content, $insertion, $paragraph_number) {
        if (trim($insertion) === '') {
            return $content;
        }

        $closing_p = '</p>';
        $paragraphs = explode($closing_p, $content);
        $count = count($paragraphs);

        if ($count <= 1) {
            return $content . "\n" . $insertion;
        }

        $output = '';
        foreach ($paragraphs as $index => $paragraph) {
            if ($paragraph === '' && $index === $count - 1) {
                continue;
            }
            $output .= $paragraph . $closing_p;
            if (($index + 1) === $paragraph_number) {
                $output .= "\n" . $insertion . "\n";
            }
        }

        return $output;
    }

    private function is_debug_enabled() {
        return get_option(self::OPTION_DEBUG, '0') === '1' && current_user_can('manage_options');
    }

    private function debug_comment($status, $post_id, $slot_type, $group_id, $banner_id) {
        if (!$this->is_debug_enabled()) {
            return '';
        }
        return "\n<!-- PPAR status=" . esc_html($status) . " post=" . esc_html((string) $post_id) . " slot=" . esc_html($slot_type) . " group=" . esc_html($group_id) . " banner=" . esc_html($banner_id) . " -->\n";
    }

    private function get_design_rules() {
        $json = (string) get_option(self::OPTION_DESIGN_RULES_JSON, self::default_design_rules_json());
        $data = json_decode($json, true);
        if (!is_array($data)) {
            return array();
        }
        return $data;
    }

    public function add_page_role_meta_box() {
        add_meta_box(
            'ppar_page_role',
            'Portal-Rolle',
            array($this, 'render_page_role_meta_box'),
            'page',
            'side',
            'default'
        );
    }

    public function render_page_role_meta_box($post) {
        wp_nonce_field('ppar_save_page_role', 'ppar_page_role_nonce');
        $value = sanitize_key((string) get_post_meta($post->ID, '_ppar_portal_role', true));
        $options = array(
            '' => 'Automatisch nach Seitenhierarchie',
            'none' => 'Keine automatische Portal-Ausgabe',
            'haupt_hub_ebene_1' => 'Haupt-Hub Ebene 1',
            'bereichs_hub_ebene_2' => 'Bereichs-Hub Ebene 2',
            'produktseite_ebene_3' => 'Produktseite Ebene 3',
        );
        echo '<p><select name="ppar_portal_role" style="width:100%">';
        foreach ($options as $key => $label) {
            echo '<option value="' . esc_attr($key) . '" ' . selected($value, $key, false) . '>' . esc_html($label) . '</option>';
        }
        echo '</select></p>';
        echo '<p class="description">Stabiler als reine Tiefen-Erkennung. Startseite wird weiterhin über WordPress-Startseite erkannt.</p>';
    }

    public function save_page_role_meta_box($post_id) {
        if (!isset($_POST['ppar_page_role_nonce']) || !wp_verify_nonce(sanitize_text_field(wp_unslash($_POST['ppar_page_role_nonce'])), 'ppar_save_page_role')) {
            return;
        }
        if (defined('DOING_AUTOSAVE') && DOING_AUTOSAVE) {
            return;
        }
        if (!current_user_can('edit_page', $post_id)) {
            return;
        }
        $role = isset($_POST['ppar_portal_role']) ? sanitize_key(wp_unslash($_POST['ppar_portal_role'])) : '';
        $allowed = array_merge(array('', 'none'), $this->allowed_template_contexts());
        if (!in_array($role, $allowed, true)) {
            $role = '';
        }
        if ($role === '') {
            delete_post_meta($post_id, '_ppar_portal_role');
        } else {
            update_post_meta($post_id, '_ppar_portal_role', $role);
        }
    }

    private function get_conflicting_template_plugins() {
        if (!function_exists('get_plugins')) {
            require_once ABSPATH . 'wp-admin/includes/plugin.php';
        }
        $active = (array) get_option('active_plugins', array());
        $plugins = function_exists('get_plugins') ? get_plugins() : array();
        $matches = array();
        foreach ($active as $plugin_file) {
            $name = isset($plugins[$plugin_file]['Name']) ? (string) $plugins[$plugin_file]['Name'] : $plugin_file;
            $haystack = strtolower($name . ' ' . $plugin_file);
            if (strpos($haystack, 'pferde startseite') !== false || strpos($haystack, 'pferde template') !== false || strpos($haystack, 'hubseite') !== false || strpos($haystack, 'affiliate template') !== false) {
                $matches[] = $name;
            }
        }
        return $matches;
    }

    public function admin_assets() {
        $page = isset($_GET['page']) ? sanitize_key((string) $_GET['page']) : '';
        if (!in_array($page, array('affiliate-portal-zentrale', 'affiliate-portal-creatives', 'affiliate-portal-campaign-edit', 'affiliate-portal-assignments', 'affiliate-portal-preview', 'affiliate-portal-ebay'), true)) {
            return;
        }
        if (function_exists('wp_enqueue_media')) {
            wp_enqueue_media();
        }
        if (function_exists('wp_add_inline_script')) {
            $script = <<<'JS'
jQuery(function($){
    $(document).on('click', '.ppar-select-image', function(e){
        e.preventDefault();
        var input = $(this).siblings('.ppar-image-url');
        var frame = wp.media({title:'Bannerbild auswählen', button:{text:'Bild verwenden'}, multiple:false});
        frame.on('select', function(){
            var attachment = frame.state().get('selection').first().toJSON();
            input.val(attachment.url).trigger('change');
        });
        frame.open();
    });
    $(document).on('click', '.ppar-placeholder-image-select', function(e){
        e.preventDefault();
        var field = String($(this).data('field') || '');
        if (!field) { return; }
        var frame = wp.media({title:'Platzhalterbild auswählen', button:{text:'Bild verwenden'}, multiple:false});
        frame.on('select', function(){
            var attachment = frame.state().get('selection').first().toJSON();
            $('#' + field).val(attachment.id || 0);
            $('#' + field + '_url').val(attachment.url || '');
            var previewUrl = attachment.url || '';
            if (previewUrl) { previewUrl += (previewUrl.indexOf('?') === -1 ? '?' : '&') + 'ppar_preview=' + Date.now(); }
            $('#' + field + '_preview').attr('src', previewUrl).show();
            $('#' + field + '_empty').hide();
        });
        frame.open();
    });
    $(document).on('click', '.ppar-placeholder-image-remove', function(e){
        e.preventDefault();
        var field = String($(this).data('field') || '');
        if (!field) { return; }
        $('#' + field).val('0');
        $('#' + field + '_url').val('');
        $('#' + field + '_preview').attr('src', '').hide();
        $('#' + field + '_empty').show();
    });
});
JS;
            wp_add_inline_script('jquery', $script);
        }
    }
    private function creative_counts() {
        $counts = array('all'=>0,'active'=>0,'banner'=>0,'product'=>0,'other'=>0);
        foreach ($this->provider_registry() as $provider_key => $provider) {
            $counts[$provider_key] = 0;
        }
        foreach ($this->get_campaigns() as $c) {
            $counts['all']++;
            if (!empty($c['active'])) { $counts['active']++; }
            $type = sanitize_key((string)($c['creative_type'] ?? 'banner'));
            if (isset($counts[$type])) { $counts[$type]++; }
            $network = sanitize_key((string)($c['network'] ?? 'manual'));
            if (isset($counts[$network])) { $counts[$network]++; }
            else { $counts['other']++; }
        }
        return $counts;
    }

    public function render_dashboard_page() {
        if (!current_user_can('manage_options')) { wp_die('Keine Berechtigung.'); }
        $counts = $this->creative_counts();
        $assignments = $this->get_assignments();
        $registry = $this->provider_registry();
        $external_provider_count = 0;
        foreach ($registry as $provider) {
            if ((string)($provider['access_owner'] ?? 'none') !== 'none') { $external_provider_count++; }
        }
        ?>
        <div class="wrap ppar-v500-dashboard">
            <style>.ppar-v500-dashboard{max-width:1180px}.ppar-kpis{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px;margin:20px 0}.ppar-kpi,.ppar-panel{background:#fff;border:1px solid #c3c4c7;border-radius:10px;padding:20px}.ppar-kpi strong{display:block;font-size:30px;color:#35422A}.ppar-panel-grid{display:grid;grid-template-columns:1.2fr .8fr;gap:18px}.ppar-actions{display:flex;flex-wrap:wrap;gap:10px}.ppar-provider-row{display:grid;grid-template-columns:minmax(120px,.8fr) minmax(160px,1fr) minmax(90px,.5fr) auto;gap:10px;align-items:center;padding:9px 0;border-bottom:1px solid #eee}.ppar-provider-row:last-child{border-bottom:0}@media(max-width:800px){.ppar-kpis,.ppar-panel-grid{grid-template-columns:1fr 1fr}.ppar-provider-row{grid-template-columns:1fr 1fr}}@media(max-width:520px){.ppar-kpis,.ppar-panel-grid,.ppar-provider-row{grid-template-columns:1fr}}</style>
            <h1>Affiliate-Zentrale</h1>
            <p><strong>Providervertrag V<?php echo esc_html(self::PROVIDER_CONTRACT_VERSION); ?>:</strong> Zugänge zentral, Provider-Fachlogik getrennt, Partner als skalierbare Datensätze. Chef-Veto bleibt auf jeder Ausgabestufe als letzte menschliche Stop-Instanz erhalten.</p>
            <div class="ppar-kpis">
                <div class="ppar-kpi"><span>Provider</span><strong><?php echo absint($external_provider_count); ?></strong></div>
                <div class="ppar-kpi"><span>Werbemittel</span><strong><?php echo absint($counts['all']); ?></strong></div>
                <div class="ppar-kpi"><span>Aktiv</span><strong><?php echo absint($counts['active']); ?></strong></div>
                <div class="ppar-kpi"><span>Zuordnungen</span><strong><?php echo count($assignments); ?></strong></div>
            </div>
            <div class="ppar-panel-grid">
                <section class="ppar-panel"><h2>Provider &amp; Zugänge</h2>
                    <?php foreach ($registry as $provider_key => $provider) : if ((string)($provider['access_owner'] ?? 'none') === 'none') { continue; } $snapshot=$this->provider_access_snapshot($provider_key); ?>
                        <div class="ppar-provider-row">
                            <strong><?php echo esc_html((string)$provider['label']); ?></strong>
                            <span><?php echo $this->provider_status_badge($snapshot); ?></span>
                            <span><?php echo absint($counts[$provider_key] ?? 0); ?> Objekte</span>
                            <span><?php if (!empty($provider['specialist_menu']) && !empty($provider['specialist_slug'])) : ?><a class="button button-small" href="<?php echo esc_url(admin_url('admin.php?page='.(string)$provider['specialist_slug'])); ?>">Fachseite</a><?php else : ?><span class="description">Adapterbereit</span><?php endif; ?></span>
                        </div>
                    <?php endforeach; ?>
                    <p style="margin-top:14px"><a class="button" href="<?php echo esc_url(admin_url('admin.php?page=affiliate-portal-networks')); ?>">Netzwerke &amp; API</a> <a class="button" href="<?php echo esc_url(admin_url('admin.php?page=affiliate-portal-health')); ?>">Prüfzentrum</a></p>
                </section>
                <section class="ppar-panel"><h2>Einheitlicher Ablauf</h2><ol><li>Providerzugang zentral verbinden.</li><li>Provider-Fachlogik konfigurieren.</li><li>Partner/Advertiser aufnehmen und Portalstatus prüfen.</li><li>Creatives/Produkte automatisch einlesen und bewerten.</li><li>Ziele und Slots automatisch planen oder manuell festlegen.</li><li>Ausgabe freigeben; Chef-Veto kann Provider, Partner, Creative, Ziel, Slot oder Ausgabe jederzeit stoppen.</li></ol></section>
            </div>
            <div class="ppar-panel" style="margin-top:18px"><h2>Direkt starten</h2><div class="ppar-actions"><a class="button button-primary" href="<?php echo esc_url(admin_url('admin.php?page=affiliate-portal-networks')); ?>">Netzwerke &amp; API</a><a class="button" href="<?php echo esc_url(admin_url('admin.php?page=affiliate-portal-partners')); ?>">Partner</a><a class="button" href="<?php echo esc_url(admin_url('admin.php?page=affiliate-portal-creative-library')); ?>">Import &amp; Auswahl</a><a class="button" href="<?php echo esc_url(admin_url('admin.php?page=affiliate-portal-outputs')); ?>">Ausgaben &amp; Freigabe</a><a class="button" href="<?php echo esc_url(admin_url('admin.php?page=affiliate-portal-control')); ?>">Steuerung &amp; Veto</a></div></div>
        </div><?php
    }

    public function render_creatives_page() {
        if (!current_user_can('manage_options')) { wp_die('Keine Berechtigung.'); }
        $type=sanitize_key((string)($_GET['creative_type'] ?? '')); $network=sanitize_key((string)($_GET['network'] ?? '')); $status=sanitize_key((string)($_GET['status'] ?? ''));
        $rows=array_filter($this->get_campaigns(), function($c) use($type,$network,$status){ if($type!==''&&sanitize_key((string)($c['creative_type']??'banner'))!==$type)return false; if($network!==''&&sanitize_key((string)($c['network']??'manual'))!==$network)return false; if($status==='active'&&empty($c['active']))return false; if($status==='inactive'&&!empty($c['active']))return false; return true; });
        $registry=$this->provider_registry();
        ?><div class="wrap"><h1 class="wp-heading-inline">Werbemittel</h1> <a class="page-title-action" href="<?php echo esc_url(admin_url('admin.php?page=affiliate-portal-campaign-edit')); ?>">Neu anlegen</a><hr class="wp-header-end">
        <div class="notice notice-info inline"><p><strong>Providerunabhängiger Ablauf:</strong> Jede Quelle läuft über denselben Sicherheits- und Chefsteuerungsvertrag. Neue Provider werden im Providerregister ergänzt; Werbemittel bleiben bis zur technischen und fachlichen Prüfung inaktiv.</p></div>
        <form method="get"><input type="hidden" name="page" value="affiliate-portal-creatives"><select name="creative_type"><option value="">Alle Arten</option><option value="banner" <?php selected($type,'banner'); ?>>Banner</option><option value="product" <?php selected($type,'product'); ?>>Produkte</option></select> <select name="network"><option value="">Alle Quellen</option><?php foreach($registry as $provider_key=>$provider_def): ?><option value="<?php echo esc_attr($provider_key); ?>" <?php selected($network,$provider_key); ?>><?php echo esc_html((string)$provider_def['label']); ?></option><?php endforeach; ?></select> <select name="status"><option value="">Alle Status</option><option value="active" <?php selected($status,'active'); ?>>Aktiv</option><option value="inactive" <?php selected($status,'inactive'); ?>>Inaktiv</option></select> <?php submit_button('Filtern','secondary','',false); ?></form>
        <table class="widefat striped" style="margin-top:16px"><thead><tr><th>Vorschau</th><th>Name</th><th>Art</th><th>Netzwerk / Partner</th><th>Zuordnung</th><th>Status</th><th>Klicks</th></tr></thead><tbody><?php if(!$rows): ?><tr><td colspan="7">Noch keine passenden Werbemittel.</td></tr><?php else: foreach($rows as $c): $edit=admin_url('admin.php?page=affiliate-portal-campaign-edit&campaign_id='.absint($c['post_id']??0)); $provider_key=sanitize_key((string)($c['network']??'manual')); ?><tr><td style="width:100px"><?php if(!empty($c['image_url'])): ?><img src="<?php echo esc_url($c['image_url']); ?>" alt="" style="max-width:90px;max-height:60px;object-fit:contain"><?php else: ?>—<?php endif; ?></td><td><strong><a href="<?php echo esc_url($edit); ?>"><?php echo esc_html((string)$c['name']); ?></a></strong><br><small><?php echo esc_html((string)($c['title']??'')); ?></small></td><td><?php echo esc_html(($c['creative_type']??'banner')==='product'?'Produkt':'Banner'); ?></td><td><?php echo esc_html($this->provider_label($provider_key).' · '.(string)($c['partner']??'')); ?></td><td><?php echo esc_html($this->campaign_match_reason($this->campaigns_to_groups(array($c))[0]??array(), $this->get_content_context(absint($c['page_id']??0)))); ?></td><td><?php echo !empty($c['active'])?'Aktiv':'Inaktiv'; ?></td><td><?php echo absint(get_post_meta(absint($c['post_id']??0),'ppar_click_total',true)); ?></td></tr><?php endforeach; endif; ?></tbody></table></div><?php
    }

    private function creative_dropdown($name, $type, $selected=0, $none='Automatisch auswählen') {
        echo '<select name="'.esc_attr($name).'"><option value="0">'.esc_html($none).'</option>';
        foreach ($this->get_campaigns() as $c) { if (sanitize_key((string)($c['creative_type']??'banner'))!==$type) continue; $id=absint($c['post_id']??0); echo '<option value="'.$id.'" '.selected($selected,$id,false).'>'.esc_html((string)$c['name'].(!empty($c['active'])?'':' [inaktiv]')).'</option>'; }
        echo '</select>';
    }

    public function handle_save_assignment() {
        if (!current_user_can('manage_options')) { wp_die('Keine Berechtigung.'); }
        check_admin_referer('ppar_save_assignment','ppar_assignment_nonce');
        $page_id=absint($_POST['page_id']??0); if($page_id<=0||get_post_type($page_id)!=='page'){wp_die('Ungültige Seite.');}
        $raw=is_array($_POST['ppar_assignment']??null)?wp_unslash($_POST['ppar_assignment']):array();
        $allowed=array('automatic','fixed','none');
        $banner_mode=in_array(sanitize_key((string)($raw['banner_mode']??'automatic')),$allowed,true)?sanitize_key((string)$raw['banner_mode']):'automatic';
        $products_mode=in_array(sanitize_key((string)($raw['products_mode']??'automatic')),$allowed,true)?sanitize_key((string)$raw['products_mode']):'automatic';
        $product_ids = array_map('absint', array_values((array)($raw['product_ids'] ?? array())));
        $product_ids = array_slice(array_pad($product_ids, 3, 0), 0, 3);
        $all=$this->get_assignments(); $all[$page_id]=array('banner_mode'=>$banner_mode,'banner_id'=>absint($raw['banner_id']??0),'products_mode'=>$products_mode,'product_ids'=>$product_ids,'apply_descendants'=>!empty($raw['apply_descendants']),'updated'=>time()); update_option(self::OPTION_ASSIGNMENTS,$all,false);
        wp_safe_redirect(add_query_arg(array('page'=>'affiliate-portal-assignments','page_id'=>$page_id,'ppar_assignment_saved'=>'1'),admin_url('admin.php'))); exit;
    }

    public function handle_delete_assignment() {
        if (!current_user_can('manage_options')) { wp_die('Keine Berechtigung.'); }
        $page_id=absint($_POST['page_id']??0); check_admin_referer('ppar_delete_assignment_'.$page_id,'ppar_assignment_delete_nonce'); $all=$this->get_assignments(); unset($all[$page_id]); update_option(self::OPTION_ASSIGNMENTS,$all,false); wp_safe_redirect(add_query_arg(array('page'=>'affiliate-portal-assignments','ppar_assignment_deleted'=>'1'),admin_url('admin.php'))); exit;
    }

    public function render_assignments_page() {
        if (!current_user_can('manage_options')) { wp_die('Keine Berechtigung.'); }
        $page_id = absint($_GET['page_id'] ?? 0);
        $search = sanitize_text_field(wp_unslash((string)($_GET['ppar_page_search'] ?? '')));
        $all = $this->get_assignments();
        $a = $page_id && isset($all[$page_id]) ? $all[$page_id] : array('banner_mode'=>'automatic','banner_id'=>0,'products_mode'=>'automatic','product_ids'=>array(),'apply_descendants'=>true);
        $results = array();
        if ($search !== '') {
            $q = new WP_Query(array(
                'post_type'=>'page','post_status'=>'publish','s'=>$search,
                'posts_per_page'=>50,'orderby'=>'title','order'=>'ASC','no_found_rows'=>true,
            ));
            $results = (array)$q->posts;
        }
        $auto_campaigns = array_filter($this->get_campaigns(), function($c){ return sanitize_key((string)($c['assignment_mode'] ?? '')) === 'auto_topic'; });
        ?>
        <div class="wrap"><h1>Zuordnungen</h1>
        <div class="notice notice-info inline"><p><strong>Normalfall:</strong> Banner und Produkte werden direkt am Werbemittel automatisch einem eindeutigen Hauptbereich und dessen Unterseiten zugeordnet. Diese Seite dient nur manuellen Ausnahmen. Das frühere Dropdown mit sämtlichen Portal-Seiten wurde entfernt.</p></div>
        <h2>Manuelle Ausnahme suchen</h2>
        <form method="get" style="display:flex;gap:8px;max-width:760px"><input type="hidden" name="page" value="affiliate-portal-assignments"><input type="search" name="ppar_page_search" value="<?php echo esc_attr($search); ?>" class="regular-text" placeholder="Seitentitel suchen, z. B. Regendecken" required><?php submit_button('Suchen','secondary','',false); ?></form>
        <?php if ($search !== '') : ?><div style="max-width:900px;margin-top:12px;background:#fff;border:1px solid #c3c4c7;padding:12px 18px"><strong>Treffer:</strong><?php if (!$results) : ?> keine<?php else : ?><ul><?php foreach($results as $result): ?><li><a href="<?php echo esc_url(admin_url('admin.php?page=affiliate-portal-assignments&page_id='.(int)$result->ID)); ?>"><?php echo esc_html((string)$result->post_title); ?></a> <span class="description">· <?php echo esc_html((string)$result->post_name); ?></span></li><?php endforeach; ?></ul><?php endif; ?></div><?php endif; ?>
        <?php if($page_id): ?><form method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>" style="max-width:850px;background:#fff;border:1px solid #c3c4c7;padding:22px;margin-top:18px"><input type="hidden" name="action" value="ppar_save_assignment"><input type="hidden" name="page_id" value="<?php echo $page_id; ?>"><?php wp_nonce_field('ppar_save_assignment','ppar_assignment_nonce'); ?><h2><?php echo esc_html(get_the_title($page_id)); ?></h2><table class="form-table"><tr><th>Affiliate-Banner</th><td><select name="ppar_assignment[banner_mode]"><option value="automatic" <?php selected($a['banner_mode'],'automatic'); ?>>Automatik verwenden</option><option value="fixed" <?php selected($a['banner_mode'],'fixed'); ?>>Fest auswählen</option><option value="none" <?php selected($a['banner_mode'],'none'); ?>>Nicht anzeigen</option></select><br><?php $this->creative_dropdown('ppar_assignment[banner_id]','banner',absint($a['banner_id']??0),'Banner auswählen'); ?></td></tr><tr><th>Produktvorschläge</th><td><select name="ppar_assignment[products_mode]"><option value="automatic" <?php selected($a['products_mode'],'automatic'); ?>>Automatik verwenden</option><option value="fixed" <?php selected($a['products_mode'],'fixed'); ?>>Fest auswählen</option><option value="none" <?php selected($a['products_mode'],'none'); ?>>Nicht anzeigen</option></select><p>Position 1: <?php $this->creative_dropdown('ppar_assignment[product_ids][]','product',absint($a['product_ids'][0]??0),'Produkt auswählen'); ?></p><p>Position 2: <?php $this->creative_dropdown('ppar_assignment[product_ids][]','product',absint($a['product_ids'][1]??0),'optional'); ?></p><p>Position 3: <?php $this->creative_dropdown('ppar_assignment[product_ids][]','product',absint($a['product_ids'][2]??0),'optional'); ?></p></td></tr><tr><th>Vererbung</th><td><label><input type="checkbox" name="ppar_assignment[apply_descendants]" value="1" <?php checked(!empty($a['apply_descendants'])); ?>> Auf strukturell untergeordnete Seiten anwenden</label></td></tr></table><?php submit_button('Ausnahme speichern'); ?></form><?php endif; ?>
        <h2 style="margin-top:30px">Automatisch erkannte Bereiche</h2>
        <table class="widefat striped"><thead><tr><th>Werbemittel</th><th>Erkannter Bereich</th><th>Score</th><th>Status</th><th>Begründung</th></tr></thead><tbody><?php if(!$auto_campaigns): ?><tr><td colspan="5">Noch keine Werbemittel mit automatischer Themenzuordnung.</td></tr><?php else: foreach($auto_campaigns as $c): ?><tr><td><a href="<?php echo esc_url(admin_url('admin.php?page=affiliate-portal-campaign-edit&campaign_id='.absint($c['post_id']??0))); ?>"><?php echo esc_html((string)($c['name']??'')); ?></a></td><td><?php echo esc_html((string)($c['auto_topic_label']??'')) ?: '—'; ?></td><td><?php echo absint($c['auto_topic_score']??0); ?></td><td><?php echo !empty($c['active'])?'aktiv':'inaktiv / prüfen'; ?></td><td><?php echo esc_html((string)($c['auto_topic_reason']??'')); ?></td></tr><?php endforeach; endif; ?></tbody></table>
        <?php if($all): ?><h2 style="margin-top:30px">Manuelle Ausnahmen</h2><table class="widefat striped"><thead><tr><th>Seite</th><th>Banner</th><th>Produkte</th><th>Vererbung</th><th></th></tr></thead><tbody><?php foreach($all as $id=>$row): ?><tr><td><a href="<?php echo esc_url(admin_url('admin.php?page=affiliate-portal-assignments&page_id='.absint($id))); ?>"><?php echo esc_html(get_the_title((int)$id)); ?></a></td><td><?php echo esc_html((string)($row['banner_mode']??'automatic')); ?></td><td><?php echo esc_html((string)($row['products_mode']??'automatic')); ?></td><td><?php echo !empty($row['apply_descendants'])?'ja':'nein'; ?></td><td><form method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>"><input type="hidden" name="action" value="ppar_delete_assignment"><input type="hidden" name="page_id" value="<?php echo absint($id); ?>"><?php wp_nonce_field('ppar_delete_assignment_'.absint($id),'ppar_assignment_delete_nonce'); ?><button class="button-link-delete">Löschen</button></form></td></tr><?php endforeach; ?></tbody></table><?php endif; ?></div><?php
    }

    public function render_preview_page() {
        if (!current_user_can('manage_options')) { wp_die('Keine Berechtigung.'); }
        $page_id=absint($_GET['page_id']??0); ?><div class="wrap"><h1>Seitenausgabe prüfen</h1><form method="get"><input type="hidden" name="page" value="affiliate-portal-preview"><?php wp_dropdown_pages(array('name'=>'page_id','selected'=>$page_id,'show_option_none'=>'Portal-Seite auswählen','option_none_value'=>'0','sort_column'=>'menu_order,post_title')); ?> <?php submit_button('Vorschau laden','secondary','',false); ?></form><?php if($page_id): ?><h2><?php echo esc_html(get_the_title($page_id)); ?></h2><p><a class="button" target="_blank" rel="noopener" href="<?php echo esc_url(get_permalink($page_id)); ?>">Öffentliche Seite öffnen</a> <a class="button" target="_blank" rel="noopener" href="<?php echo esc_url(add_query_arg('pftk_affiliate_preview','3',get_permalink($page_id))); ?>">Designvorschau 3 Produkte</a></p><div style="display:grid;gap:20px;max-width:1000px"><section style="background:#fff;border:1px solid #c3c4c7;padding:20px"><h3>Affiliate-Banner</h3><?php $html=$this->render_affiliate_slot($page_id,'product_after_category_tiles','portal_context',''); echo trim($html)!==''?$html:'<p>Nicht befüllt.</p>'; ?></section><?php for($i=1;$i<=3;$i++): ?><section style="background:#fff;border:1px solid #c3c4c7;padding:20px"><h3>Produktposition <?php echo $i; ?></h3><?php $html=$this->render_affiliate_slot($page_id,'category_product_'.$i,'portal_context',''); echo trim($html)!==''?$html:'<p>Nicht befüllt.</p>'; ?></section><?php endfor; ?></div><?php endif; ?></div><?php
    }
    /**
     * Bounded diagnostic campaign lookup. Productzuordnung must never hydrate the
     * complete campaign catalog: after a large BUSINESS reconcile this used to
     * turn a read-only admin page into hundreds/thousands of post/meta reads.
     * Only campaign IDs referenced by the 100 creatives on the current page are
     * loaded. Public routing is not changed by this helper.
     */
    private function ebay_business_diag_campaign_map($campaign_ids) {
        $campaign_ids = array_values(array_unique(array_filter(array_map('absint', (array) $campaign_ids))));
        if (!$campaign_ids) { return array(); }
        $posts = get_posts(array(
            'post_type' => self::CAMPAIGN_POST_TYPE,
            'post_status' => array('publish','draft','private'),
            'post__in' => $campaign_ids,
            'numberposts' => count($campaign_ids),
            'posts_per_page' => count($campaign_ids),
            'orderby' => 'post__in',
            'suppress_filters' => true,
            'no_found_rows' => true,
        ));
        $map = array();
        foreach ((array) $posts as $post) {
            $campaign = $this->campaign_from_post($post);
            if (!is_array($campaign)) { continue; }
            $post_id = absint($campaign['post_id'] ?? 0);
            if ($post_id > 0) { $map[$post_id] = $campaign; }
        }
        return $map;
    }

    private function ebay_business_diag_target_url($target_type, $target_key) {
        $target_type = sanitize_key((string) $target_type);
        $target_key = sanitize_text_field((string) $target_key);
        if ($target_type === 'page' && preg_match('/^page:(\d+)$/', $target_key, $m)) {
            $id = absint($m[1]);
            return $id > 0 ? esc_url_raw((string) get_permalink($id)) : '';
        }
        if ($target_type === 'category' && preg_match('/^category:(\d+)$/', $target_key, $m)) {
            $term = get_term(absint($m[1]), 'category');
            if ($term && !is_wp_error($term)) {
                $url = get_term_link($term, 'category');
                return is_wp_error($url) ? '' : esc_url_raw((string) $url);
            }
        }
        return '';
    }
    /**
     * Snapshot-only reason for the BUSINESS overview. This method deliberately
     * does not call the public router/source gate: doing that once per row caused
     * N additional ebay_items lookups on every page open. The table describes the
     * persisted source/creative/output snapshot; public delivery remains governed
     * by the unchanged frontend router.
     */
    private function ebay_business_diag_block_reason($row, $object, $campaign) {
        $payload = json_decode((string) ($row['payload'] ?? ''), true);
        $payload = is_array($payload) ? $payload : array();
        $source_status = sanitize_key((string) ($row['source_status'] ?? ''));
        $availability_state = sanitize_key((string) ($row['availability_state'] ?? ''));
        if ($source_status !== 'active' || $availability_state !== 'active') {
            $filter_state = sanitize_key((string) ($payload['_content_filter_state'] ?? ''));
            $filter_reason = sanitize_text_field((string) ($payload['_content_filter_reason'] ?? ''));
            if ($filter_state === 'blocked_toy_model' || $availability_state === 'blocked_content') {
                return 'BLOCKED – fachfremdes Spielzeug/Modell' . ($filter_reason !== '' ? ': ' . $filter_reason : '.');
            }
            if ($source_status !== 'active') { return 'eBay-Produktquelle ist nicht aktiv (Status: ' . $source_status . ').'; }
            return 'Produkt ist nicht verfügbar (Status: ' . $availability_state . ').';
        }
        $image_state = sanitize_key((string) ($payload['_dimension_state'] ?? 'pending'));
        if (!in_array($image_state, array('verified','mismatch'), true) || absint($row['width'] ?? 0) <= 0 || absint($row['height'] ?? 0) <= 0) {
            return $image_state === 'failed' ? 'Bildprüfung fehlgeschlagen: ' . sanitize_text_field((string) ($payload['_dimension_error'] ?? 'unbekannt')) : 'Bildprüfung noch offen.';
        }
        if (method_exists($this, 'ebay_business_product_contract') && !$this->ebay_business_product_contract($row)) {
            $slug = sanitize_title((string) ($payload['ebay_verified_product_slug'] ?? ''));
            $score = absint($payload['ebay_verified_score'] ?? 0);
            if ($slug === '') { return 'Kein verifiziertes Produktziel aus dem eBay-Katalog.'; }
            if ($score < 80) { return 'Produkt-Match unter Mindestscore 80 (aktuell ' . $score . ').'; }
            $contract = sanitize_key((string) ($payload['ebay_business_match_contract'] ?? ''));
            if ($contract !== 'concept_v3') { return 'BUSINESS-Konzeptklassifikation V3 ist noch nicht abgeschlossen.'; }
            return 'BUSINESS-Vertrag nicht vollständig erfüllt.';
        }
        if (!is_array($object)) { return 'Noch kein Ausgabeobjekt geplant.'; }
        $status = sanitize_key((string) ($object['status'] ?? 'review'));
        if ($status !== 'published') {
            $reason = sanitize_text_field((string) ($object['decision_reason'] ?? ''));
            return $reason !== '' ? $reason : 'Ausgabeobjekt steht auf ' . $status . '.';
        }
        if (!is_array($campaign)) { return 'Ausgabeobjekt veröffentlicht, aber Kampagne fehlt.'; }
        if (empty($campaign['active'])) { return 'Kampagne ist nicht aktiv.'; }
        return '';
    }

    /** Resolve a published page by its exact post_name, including hierarchical pages. */
    private function ebay_business_diag_page_by_slug($slug) {
        $slug = sanitize_title((string)$slug);
        if ($slug === '') { return null; }
        $post = function_exists('get_page_by_path') ? get_page_by_path($slug, OBJECT, 'page') : null;
        if ($post && sanitize_title((string)($post->post_name ?? '')) === $slug) { return $post; }
        if (!function_exists('get_posts')) { return null; }
        $matches = get_posts(array(
            'post_type'=>'page','post_status'=>'publish','name'=>$slug,
            'posts_per_page'=>2,'numberposts'=>2,'orderby'=>'ID','order'=>'ASC',
            'no_found_rows'=>true,'suppress_filters'=>true,
        ));
        $exact = array_values(array_filter((array)$matches, static function($candidate) use ($slug) {
            return is_object($candidate) && sanitize_title((string)($candidate->post_name ?? '')) === $slug;
        }));
        // Hierarchical slugs can legally be ambiguous below different parents.
        // A diagnostic reference must never guess which page was intended.
        return count($exact) === 1 ? $exact[0] : null;
    }

    private function ebay_business_diag_resolve_public_target($target_key) {
        $target_key = $this->automation_normalize_target_key($target_key);
        if ($target_key === '') { return null; }
        list($kind, $slug) = array_pad(explode(':', $target_key, 2), 2, '');
        $kind = sanitize_key((string) $kind);
        $slug = sanitize_key((string) $slug);
        if ($kind === 'page') {
            $post = $this->ebay_business_diag_page_by_slug($slug);
            if (!$post) { return null; }
            $page_id = absint($post->ID ?? 0);
            if ($page_id <= 0) { return null; }
            $page_type = '';
            if (class_exists('Pferde_Template_Kit') && is_callable(array('Pferde_Template_Kit','affiliate_page_type'))) {
                $page_type = sanitize_key((string) call_user_func(array('Pferde_Template_Kit','affiliate_page_type'), $page_id));
            }
            $slots = $page_type === 'hub1'
                ? array('hub_product_1','hub_product_2','hub_product_3')
                : array('category_product_1','category_product_2','category_product_3');
            return array('kind'=>'page','id'=>$page_id,'label'=>get_the_title($page_id),'url'=>get_permalink($page_id),'context'=>$this->get_content_context($page_id),'slots'=>$slots);
        }
        if ($kind === 'journal') {
            $post = $this->ebay_business_diag_page_by_slug($slug);
            if (!$post && $slug === 'journal') { $post = $this->ebay_business_diag_page_by_slug('journal'); }
            if (!$post) { return null; }
            $page_id = absint($post->ID ?? 0);
            if ($page_id <= 0) { return null; }
            return array('kind'=>'journal','id'=>$page_id,'label'=>get_the_title($page_id),'url'=>get_permalink($page_id),'context'=>$this->get_content_context($page_id),'slots'=>array('journal_product_1','journal_product_2','journal_product_3'));
        }
        if ($kind === 'category') {
            $term = get_term_by('slug', $slug, 'category');
            if (!$term || is_wp_error($term)) { return null; }
            $url = get_term_link($term, 'category');
            if (is_wp_error($url)) { return null; }
            return array('kind'=>'category','id'=>absint($term->term_id),'label'=>(string) $term->name,'url'=>$url,'context'=>$this->get_category_archive_context($term),'slots'=>array('category_product_1','category_product_2','category_product_3'));
        }
        return null;
    }
    /**
     * Bounded materialized references for the current 100-row overview page.
     * This replaces the old global router simulation which called
     * select_campaign_for_slot() for every campaign/target/slot and thereby
     * reloaded/scanned the complete campaign catalog repeatedly (quadratic cost).
     */
    private function ebay_business_diag_materialized_references($rows, $objects, $campaigns, $limit = 20) {
        $limit = max(1, min(20, absint($limit)));
        $refs = array();
        $seen = array();
        foreach ((array) $rows as $row) {
            $hash = sanitize_text_field((string) ($row['identity_hash'] ?? ''));
            $object = $hash !== '' && isset($objects[$hash]) && is_array($objects[$hash]) ? $objects[$hash] : null;
            if (!is_array($object) || sanitize_key((string) ($object['status'] ?? '')) !== 'published') { continue; }
            $campaign_id = absint($object['campaign_post_id'] ?? 0);
            $campaign = $campaign_id > 0 && isset($campaigns[$campaign_id]) && is_array($campaigns[$campaign_id]) ? $campaigns[$campaign_id] : null;
            if (!is_array($campaign) || empty($campaign['active'])) { continue; }
            $target_type = sanitize_key((string) ($object['target_type'] ?? ''));
            $target_key = sanitize_text_field((string) ($object['target_key'] ?? ''));
            $slot = sanitize_key((string) ($object['slot_id'] ?? ''));
            $key = $target_type . '|' . $target_key . '|' . $slot . '|' . $campaign_id;
            if (isset($seen[$key])) { continue; }
            $seen[$key] = true;
            $refs[] = array(
                'page_label'=>sanitize_text_field((string) ($object['target_label'] ?? '')),
                'url'=>$this->ebay_business_diag_target_url($target_type, $target_key),
                'slot'=>$slot,
                'product'=>sanitize_text_field((string) ($row['title'] ?? $campaign['title'] ?? $campaign['name'] ?? '')),
            );
            if (count($refs) >= $limit) { break; }
        }
        return $refs;
    }

    public function render_ebay_business_assignments_page() {
        if (!current_user_can('manage_options')) { wp_die('Keine Berechtigung.'); }
        global $wpdb;
        // Workflow V2: Diagnose ist strikt read-only. Datenkorrekturen laufen nur
        // im separaten stündlichen Maintenance-Job, niemals durch das Öffnen dieser Seite.
        $maintenance_state = method_exists($this, 'ebay_maintenance_state_load') ? $this->ebay_maintenance_state_load() : get_option(self::OPTION_EBAY_MAINTENANCE_STATE, array());
        $maintenance_state = is_array($maintenance_state) ? $maintenance_state : array();
        $creative_table = $this->creative_library_table();
        $output_table = $this->output_objects_table();
        $search = sanitize_text_field((string) ($_GET['s'] ?? ''));
        $concept_filter = sanitize_key((string) ($_GET['concept'] ?? ''));
        $concept_options = array();
        if (method_exists($this, 'ebay_portal_catalog')) {
            $catalog = $this->ebay_portal_catalog();
            if (!is_wp_error($catalog)) {
                foreach (array('business_concepts','business_hub_concepts') as $concept_group) {
                    foreach ((array) ($catalog[$concept_group] ?? array()) as $concept) {
                        if (!is_array($concept)) { continue; }
                        $cid=sanitize_key((string)($concept['id']??'')); if($cid===''){continue;}
                        $label=sanitize_text_field((string)($concept['title']??$cid));
                        if($concept_group==='business_hub_concepts'){$label.=' [Produktfamilie]';}
                        $concept_options[$cid]=$label;
                    }
                }
                asort($concept_options, SORT_NATURAL|SORT_FLAG_CASE);
            }
        }
        $candidate_rows = array();
        if ($concept_filter !== '' && method_exists($this, 'ebay_items_table')) {
            $item_table = $this->ebay_items_table();
            $like_concept = '%' . $wpdb->esc_like($concept_filter) . '%';
            $raw_candidates = (array) $wpdb->get_results($wpdb->prepare(
                "SELECT * FROM {$item_table} WHERE seller_account_type='BUSINESS' AND source_payload LIKE %s AND source_state='available' ORDER BY last_seen DESC,id DESC LIMIT 100",
                $like_concept
            ), ARRAY_A);
            foreach ($raw_candidates as $candidate_row) {
                $sp=json_decode((string)($candidate_row['source_payload']??''),true); $sp=is_array($sp)?$sp:array();
                $pc=is_array($sp['portal_classification']??null)?$sp['portal_classification']:array();
                if(sanitize_key((string)($pc['product_concept_id']??''))!==$concept_filter){continue;}
                $candidate_row['_quality']=is_array($sp['business_quality']??null)?$sp['business_quality']:array();
                $candidate_row['_selection']=is_array($sp['business_selection']??null)?$sp['business_selection']:array();
                $candidate_row['_classification']=$pc;
                $candidate_rows[]=$candidate_row;
            }
            usort($candidate_rows, static function($a,$b){
                $ap=!empty($a['_quality']['pinned'])?1:0; $bp=!empty($b['_quality']['pinned'])?1:0; if($ap!==$bp)return $ap>$bp?-1:1;
                $aq=absint($a['_quality']['overall']??0); $bq=absint($b['_quality']['overall']??0); if($aq!==$bq)return $aq>$bq?-1:1;
                return absint($a['last_seen']??0)>absint($b['last_seen']??0)?-1:1;
            });
            $candidate_rows=array_slice($candidate_rows,0,10);
        }
        $curation_state = method_exists($this, 'ebay_business_curation_state') ? $this->ebay_business_curation_state() : array('items'=>array(),'sellers'=>array(),'brands'=>array(),'learned_heads'=>array());
        $curation_entries = array();
        foreach ((array)($curation_state['items']??array()) as $key=>$entry) { if(is_array($entry)){$curation_entries[]=array('type'=>'Produkt','key'=>(string)$key,'status'=>(string)($entry['status']??''),'reason'=>(string)($entry['reason']??''),'operation'=>'item_clear','item_id'=>(string)$key); } }
        foreach ((array)($curation_state['sellers']??array()) as $key=>$entry) { if(is_array($entry)){$curation_entries[]=array('type'=>'Verkäufer','key'=>(string)$key,'status'=>(string)($entry['status']??''),'reason'=>(string)($entry['reason']??''),'operation'=>'seller_clear','seller'=>(string)$key); } }
        foreach ((array)($curation_state['brands']??array()) as $key=>$entry) { if(is_array($entry)){$curation_entries[]=array('type'=>'Marke','key'=>(string)$key,'status'=>(string)($entry['status']??''),'reason'=>(string)($entry['reason']??''),'operation'=>'brand_clear','brand'=>(string)$key); } }
        foreach ((array)($curation_state['learned_heads']??array()) as $cid=>$heads) { foreach((array)$heads as $head=>$entry){ if(is_array($entry)){$curation_entries[]=array('type'=>'Gelernte Fehlklasse','key'=>(string)$head,'status'=>'blocked','reason'=>(string)($entry['reason']??''),'operation'=>'learned_clear','concept'=>(string)$cid,'title'=>(string)$head); } } }
        $paged = max(1, absint($_GET['paged'] ?? 1));
        $per_page = 100;
        $where = "provider='ebay' AND source_kind='ebay_business_item' AND creative_type='product'";
        $args = array();
        if ($search !== '') {
            $like = '%' . $wpdb->esc_like($search) . '%';
            $where .= ' AND (title LIKE %s OR external_id LIKE %s OR partner_name LIKE %s OR payload LIKE %s)';
            $args = array($like, $like, $like, $like);
        }
        $count_sql = "SELECT COUNT(*) FROM {$creative_table} WHERE {$where}";
        $total = $args ? absint($wpdb->get_var($wpdb->prepare($count_sql, $args))) : absint($wpdb->get_var($count_sql));
        $offset = ($paged - 1) * $per_page;
        $rows_sql = "SELECT * FROM {$creative_table} WHERE {$where} ORDER BY (source_status='active' AND availability_state='active') DESC, last_seen DESC, id DESC LIMIT {$per_page} OFFSET {$offset}";
        $rows = $args ? $wpdb->get_results($wpdb->prepare($rows_sql, $args), ARRAY_A) : $wpdb->get_results($rows_sql, ARRAY_A);
        $rows = is_array($rows) ? $rows : array();

        $hashes = array_values(array_filter(array_map(function($row) { return sanitize_text_field((string) ($row['identity_hash'] ?? '')); }, $rows)));
        $objects = array();
        if ($hashes) {
            $placeholders = implode(',', array_fill(0, count($hashes), '%s'));
            $sql = "SELECT * FROM {$output_table} WHERE output_type='product_campaign' AND creative_identity_hash IN ({$placeholders}) ORDER BY id DESC";
            foreach ((array) $wpdb->get_results($wpdb->prepare($sql, $hashes), ARRAY_A) as $object) {
                $hash = (string) ($object['creative_identity_hash'] ?? '');
                if ($hash !== '' && !isset($objects[$hash])) { $objects[$hash] = $object; }
            }
        }
        // Productzuordnung is a bounded read-only overview. Hydrate only campaigns
        // referenced by the current 100 rows; never simulate the complete public
        // router during page render.
        $campaign_ids = array_values(array_unique(array_filter(array_map(static function($object) {
            return is_array($object) ? absint($object['campaign_post_id'] ?? 0) : 0;
        }, $objects))));
        $campaign_map = $this->ebay_business_diag_campaign_map($campaign_ids);
        $materialized_refs = $this->ebay_business_diag_materialized_references($rows, $objects, $campaign_map, 20);
        $pending_assets = method_exists($this, 'ebay_business_pending_asset_count') ? $this->ebay_business_pending_asset_count() : 0;

        $kpi = array('all'=>$total,'available'=>0,'blocked_content'=>0,'verified'=>0,'published'=>0,'attention'=>0);
        $kpi['available'] = absint($wpdb->get_var("SELECT COUNT(*) FROM {$creative_table} WHERE provider='ebay' AND source_kind='ebay_business_item' AND creative_type='product' AND source_status='active' AND availability_state='active'"));
        $kpi['blocked_content'] = absint($wpdb->get_var("SELECT COUNT(*) FROM {$creative_table} WHERE provider='ebay' AND source_kind='ebay_business_item' AND creative_type='product' AND (source_status='blocked' OR availability_state='blocked_content')"));
        $kpi['verified'] = absint($wpdb->get_var("SELECT COUNT(*) FROM {$creative_table} WHERE provider='ebay' AND source_kind='ebay_business_item' AND creative_type='product' AND source_status='active' AND availability_state='active' AND width>0 AND height>0 AND topic_status='auto_verified'"));
        $kpi['published'] = absint($wpdb->get_var("SELECT COUNT(DISTINCT creative_identity_hash) FROM {$output_table} WHERE provider='ebay' AND output_type='product_campaign' AND status='published'"));
        $kpi['attention'] = max(0, $kpi['available'] - $kpi['published']);
        $pages = max(1, (int) ceil($total / $per_page));
        ?>
        <div class="wrap ppar-ebay-business-diag">
            <style>
                .ppar-ebay-business-diag{max-width:1450px}.ppar-ebay-business-kpis{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:12px;margin:18px 0}.ppar-ebay-business-kpi,.ppar-ebay-business-box{background:#fff;border:1px solid #c3c4c7;border-radius:8px;padding:16px}.ppar-ebay-business-kpi strong{display:block;font-size:28px;color:#35422A}.ppar-ebay-business-ok{color:#187a36;font-weight:600}.ppar-ebay-business-warn{color:#9a6700;font-weight:600}.ppar-ebay-business-bad{color:#b32d2e;font-weight:600}.ppar-ebay-business-diag td{vertical-align:top}.ppar-ebay-business-diag code{white-space:nowrap}@media(max-width:900px){.ppar-ebay-business-kpis{grid-template-columns:1fr 1fr}}
            </style>
            <h1>eBay BUSINESS – Produktzuordnung</h1>
            <p>Diagnose der automatischen Kette: <strong>eBay BUSINESS → Produktkonzept → Produktpool → Bildprüfung → Portalziel → Designslot → aktive Kampagne</strong>. Keine HivePress-Ausgabe. Falsche oder mehrdeutige Matches bleiben fail-closed auf Review.</p>
            <div class="ppar-ebay-business-kpis">
                <div class="ppar-ebay-business-kpi"><span>BUSINESS-Produkte</span><strong><?php echo absint($kpi['all']); ?></strong></div>
                <div class="ppar-ebay-business-kpi"><span>Quelle aktiv</span><strong><?php echo absint($kpi['available']); ?></strong></div>
                <div class="ppar-ebay-business-kpi"><span>Fachfremd blockiert</span><strong><?php echo absint($kpi['blocked_content']); ?></strong></div>
                <div class="ppar-ebay-business-kpi"><span>Bild geprüft</span><strong><?php echo absint($kpi['verified']); ?></strong></div>
                <div class="ppar-ebay-business-kpi"><span>Ausgabe veröffentlicht</span><strong><?php echo absint($kpi['published']); ?></strong></div>
                <div class="ppar-ebay-business-kpi"><span>Aktiv noch offen</span><strong><?php echo absint($kpi['attention']); ?></strong></div>
            </div>
            <div class="ppar-ebay-business-box" style="margin-bottom:18px">
                <h2>Workflow-V2 Status (read-only)</h2>
                <p><strong>Policy:</strong> <?php echo esc_html((string) ($maintenance_state['policy_version'] ?? 'noch nicht gelaufen')); ?>
                · <strong>PRIVATE-Klassifikator:</strong> <?php echo esc_html((string) ($maintenance_state['private_classifier_version'] ?? 'noch nicht gelaufen')); ?>
                · <strong>BUSINESS-Klassifikator:</strong> <?php echo esc_html((string) ($maintenance_state['business_classifier_version'] ?? 'noch nicht gelaufen')); ?>.</p>
                <p><strong>Letzter Maintenance-Lauf:</strong> <?php echo absint($maintenance_state['last_run_at'] ?? 0) > 0 ? esc_html(wp_date('d.m.Y H:i:s', absint($maintenance_state['last_run_at']))) : 'noch nicht gelaufen'; ?>
                · <strong>Status:</strong> <?php echo !empty($maintenance_state['completed_at']) ? 'vollständiger lokaler Durchlauf abgeschlossen' : 'weitere veraltete Datensätze können offen sein'; ?>.</p>
                <?php $maint_stats = is_array($maintenance_state['last_stats'] ?? null) ? $maintenance_state['last_stats'] : array(); ?>
                <p class="description">Diese Diagnose verändert keine Produkte, Kampagnen oder Zuordnungen. Letzter Lauf: <?php echo absint($maint_stats['scanned'] ?? 0); ?> geprüft · <?php echo absint($maint_stats['ready_private'] ?? 0); ?> PRIVATE bereit · <?php echo absint($maint_stats['ready_business'] ?? 0); ?> BUSINESS bereit · <?php echo absint($maint_stats['review'] ?? 0); ?> Review · <?php echo absint($maint_stats['blocked'] ?? 0); ?> blockiert.</p>
            </div>

            <div class="ppar-ebay-business-box">
                <h2>Materialisierte Ziele dieser Seite</h2>
                <?php if (!$materialized_refs) : ?>
                    <p>Auf dieser Tabellenseite ist noch kein veröffentlichtes BUSINESS-Ausgabeobjekt materialisiert.</p>
                <?php else : ?>
                    <p>Bewusst begrenzte Übersicht der veröffentlichten Ausgabeobjekte auf dieser 100er-Seite. Der öffentliche Router wird beim Öffnen der Produktzuordnung nicht mehr vollständig simuliert.</p>
                    <table class="widefat striped"><thead><tr><th>Seite/Kategorie</th><th>Slot</th><th>Produkt</th></tr></thead><tbody>
                    <?php foreach ($materialized_refs as $ref) : ?><tr>
                        <td><?php if (!empty($ref['url'])) : ?><a target="_blank" rel="noopener" href="<?php echo esc_url($ref['url']); ?>"><strong><?php echo esc_html($ref['page_label']); ?></strong></a><?php else : echo esc_html($ref['page_label']); endif; ?></td>
                        <td><code><?php echo esc_html($ref['slot']); ?></code></td>
                        <td><?php echo esc_html($ref['product']); ?></td>
                    </tr><?php endforeach; ?>
                    </tbody></table>
                <?php endif; ?>
            </div>

            <div class="ppar-ebay-business-box" style="margin:18px 0">
                <h2>Aktive Qualitätssteuerungen</h2>
                <p class="description">Pins, Produkt-/Verkäufer-/Marken-Vetos und gelernte Fehlproduktklassen. Jede Regel kann hier wieder aufgehoben werden.</p>
                <?php if(!$curation_entries): ?><p>Keine manuellen Qualitätssteuerungen aktiv.</p><?php else: ?>
                <table class="widefat striped"><thead><tr><th>Art</th><th>Wert</th><th>Status</th><th>Grund</th><th></th></tr></thead><tbody>
                <?php foreach(array_slice($curation_entries,0,100) as $entry): ?><tr><td><?php echo esc_html($entry['type']); ?></td><td><code><?php echo esc_html($entry['key']); ?></code><?php if(!empty($entry['concept'])):?><br><small><?php echo esc_html($concept_options[$entry['concept']]??$entry['concept']); ?></small><?php endif; ?></td><td><?php echo esc_html($entry['status']); ?></td><td><?php echo esc_html($entry['reason']); ?></td><td><form method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>"><?php wp_nonce_field('ppar_ebay_business_curation'); ?><input type="hidden" name="action" value="ppar_ebay_business_curation"><input type="hidden" name="operation" value="<?php echo esc_attr($entry['operation']); ?>"><?php if(!empty($entry['item_id'])):?><input type="hidden" name="item_id" value="<?php echo esc_attr($entry['item_id']); ?>"><?php endif; ?><?php if(!empty($entry['seller'])):?><input type="hidden" name="seller" value="<?php echo esc_attr($entry['seller']); ?>"><?php endif; ?><?php if(!empty($entry['brand'])):?><input type="hidden" name="brand" value="<?php echo esc_attr($entry['brand']); ?>"><?php endif; ?><?php if(!empty($entry['concept'])):?><input type="hidden" name="concept" value="<?php echo esc_attr($entry['concept']); ?>"><?php endif; ?><?php if(!empty($entry['title'])):?><input type="hidden" name="title" value="<?php echo esc_attr($entry['title']); ?>"><?php endif; ?><button class="button button-small">Aufheben</button></form></td></tr><?php endforeach; ?>
                </tbody></table><?php endif; ?>
            </div>

            <form method="get" style="margin:18px 0;display:flex;gap:8px;align-items:center;flex-wrap:wrap"><input type="hidden" name="page" value="affiliate-portal-ebay-business"><input type="search" name="s" value="<?php echo esc_attr($search); ?>" class="regular-text" placeholder="Produkt, Item-ID oder Händler"><select name="concept"><option value="">Alle Produktkonzepte</option><?php foreach($concept_options as $cid=>$ctitle): ?><option value="<?php echo esc_attr($cid); ?>" <?php selected($concept_filter,$cid); ?>><?php echo esc_html($ctitle); ?></option><?php endforeach; ?></select><?php submit_button('Filtern','secondary','',false); ?></form>
            <?php if ($concept_filter !== '') : ?>
            <div class="ppar-ebay-business-box" style="margin-bottom:18px">
                <h2>Top-10 Vorauswahl: <?php echo esc_html($concept_options[$concept_filter] ?? $concept_filter); ?></h2>
                <p class="description">Automatik: 50 % Produktgenauigkeit · 25 % Verkäuferqualität · 15 % Angebotsqualität · 10 % Preisplausibilität. Sichtbar höchstens 3; dahinter 2 Reserven. Pins/Vetos ändern nur die Auswahl, nicht die Architektur.</p>
                <table class="widefat striped"><thead><tr><th>Produkt</th><th>Qualität</th><th>Verkäufer</th><th>Marke</th><th>Auswahl</th><th>Steuerung</th></tr></thead><tbody>
                <?php if(!$candidate_rows): ?><tr><td colspan="6">Keine qualifizierten Kandidaten in diesem Konzept.</td></tr><?php else: foreach($candidate_rows as $candidate):
                    $q=(array)($candidate['_quality']??array()); $sel=(array)($candidate['_selection']??array());
                    $rawp=json_decode((string)($candidate['source_payload']??''),true); $rawp=is_array($rawp)?$rawp:array(); $raw=is_array($rawp['raw']??null)?$rawp['raw']:array();
                    $seller=sanitize_text_field((string)($candidate['seller_username']??''));
                    $brand=sanitize_text_field((string)($raw['brand']??'')); if($brand===''){foreach((array)($raw['localizedAspects']??array()) as $asp){if(!is_array($asp))continue;$n=strtolower((string)($asp['name']??''));if(in_array($n,array('marke','brand','hersteller','manufacturer'),true)){$brand=sanitize_text_field((string)($asp['value']??''));break;}}}
                ?><tr>
                    <td style="min-width:260px"><?php if(!empty($candidate['image_url'])):?><img src="<?php echo esc_url($candidate['image_url']); ?>" alt="" style="width:64px;height:64px;object-fit:contain;background:#fff;border:1px solid #ddd;float:left;margin-right:9px"><?php endif; ?><strong><?php echo esc_html($candidate['title']); ?></strong><br><small><?php echo esc_html($candidate['item_id']); ?> · <?php echo esc_html($candidate['price_value'].' '.$candidate['currency']); ?></small></td>
                    <td><strong><?php echo absint($q['overall']??0); ?>/100</strong><br><small>Rel <?php echo absint($q['relevance']??0); ?> · Verk <?php echo absint($q['seller']??0); ?> · Ang <?php echo absint($q['offer']??0); ?> · Preis <?php echo absint($q['price']??0); ?></small><br><small><?php echo esc_html((string)($q['reason']??'')); ?></small></td>
                    <td><?php echo esc_html($seller); ?><br><small><?php echo esc_html(number_format((float)($q['seller_feedback_percentage']??0),1,',','.')); ?> % · <?php echo absint($q['seller_feedback_score']??0); ?> Bewertungen</small></td>
                    <td><?php echo $brand!==''?esc_html($brand):'—'; ?></td>
                    <td><strong><?php echo esc_html((string)($sel['role']??'candidate')); ?></strong><?php if(!empty($sel['rank'])):?><br>Rang <?php echo absint($sel['rank']); ?><?php endif; ?></td>
                    <td style="min-width:270px">
                        <form method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>" style="display:flex;gap:5px;flex-wrap:wrap;margin-bottom:5px"><?php wp_nonce_field('ppar_ebay_business_curation'); ?><input type="hidden" name="action" value="ppar_ebay_business_curation"><input type="hidden" name="item_id" value="<?php echo esc_attr($candidate['item_id']); ?>"><input type="hidden" name="seller" value="<?php echo esc_attr($seller); ?>"><input type="hidden" name="brand" value="<?php echo esc_attr($brand); ?>"><input type="hidden" name="concept" value="<?php echo esc_attr($concept_filter); ?>"><input type="hidden" name="title" value="<?php echo esc_attr($candidate['title']); ?>"><input type="text" name="reason" placeholder="Grund (optional)" style="width:160px"><button class="button button-small" name="operation" value="pin">Anpinnen</button><button class="button button-small" name="operation" value="item_clear">Pin/Veto lösen</button><button class="button button-small" name="operation" value="block_item">Produkt sperren</button><button class="button button-small" name="operation" value="block_item_learn">Sperren + lernen</button><?php if($seller!==''): ?><button class="button button-small" name="operation" value="block_seller">Verkäufer sperren</button><?php endif; ?><?php if($brand!==''): ?><button class="button button-small" name="operation" value="prefer_brand">Marke bevorzugen</button><button class="button button-small" name="operation" value="block_brand">Marke sperren</button><?php endif; ?></form>
                    </td>
                </tr><?php endforeach; endif; ?></tbody></table>
            </div>
            <?php endif; ?>
            <table class="widefat striped"><thead><tr><th>Produkt</th><th>eBay-Match</th><th>Bild</th><th>Portalziel</th><th>Designslot</th><th>Ausgabe</th><th>Warum nicht sichtbar?</th></tr></thead><tbody>
            <?php if (!$rows) : ?><tr><td colspan="7">Keine eBay-BUSINESS-Produkte gefunden.</td></tr><?php else : foreach ($rows as $row) :
                $hash = (string) ($row['identity_hash'] ?? '');
                $object = isset($objects[$hash]) && is_array($objects[$hash]) ? $objects[$hash] : null;
                $campaign_id = is_array($object) ? absint($object['campaign_post_id'] ?? 0) : 0;
                $campaign = $campaign_id > 0 && isset($campaign_map[$campaign_id]) ? $campaign_map[$campaign_id] : null;
                $payload = json_decode((string) ($row['payload'] ?? ''), true); $payload = is_array($payload) ? $payload : array();
                $slug = sanitize_title((string) ($payload['ebay_verified_product_slug'] ?? ''));
                $score = absint($payload['ebay_verified_score'] ?? 0);
                $image_state = sanitize_key((string) ($payload['_dimension_state'] ?? 'pending'));
                $reason = $this->ebay_business_diag_block_reason($row, $object, $campaign);
                $published = is_array($object)
                    && sanitize_key((string) ($object['status'] ?? '')) === 'published'
                    && is_array($campaign)
                    && !empty($campaign['active']);
                $target_url = is_array($object) ? $this->ebay_business_diag_target_url($object['target_type'] ?? '', $object['target_key'] ?? '') : '';
            ?><tr>
                <td style="min-width:240px"><?php if (!empty($row['image_url'])) : ?><img src="<?php echo esc_url($row['image_url']); ?>" alt="" style="width:70px;height:70px;object-fit:contain;float:left;margin:0 10px 6px 0;background:#fff;border:1px solid #ddd"><?php endif; ?><strong><?php echo esc_html((string) ($row['title'] ?? '')); ?></strong><br><small>Item <?php echo esc_html((string) ($payload['ebay_item_id'] ?? $row['external_id'] ?? '')); ?> · <?php echo esc_html((string) ($row['partner_name'] ?? '')); ?></small></td>
                <td><code><?php echo esc_html($slug !== '' ? $slug : '—'); ?></code><br>Score <?php echo absint($score); ?><br><small><?php echo esc_html(sanitize_key((string) ($payload['ebay_business_match_contract'] ?? 'review'))); ?></small></td>
                <td><?php echo esc_html($image_state); ?><br><small><?php echo absint($row['width'] ?? 0); ?>×<?php echo absint($row['height'] ?? 0); ?></small></td>
                <td><?php if (is_array($object) && !empty($object['target_label'])) : ?><?php if ($target_url !== '') : ?><a target="_blank" rel="noopener" href="<?php echo esc_url($target_url); ?>"><?php echo esc_html((string) $object['target_label']); ?></a><?php else : echo esc_html((string) $object['target_label']); endif; ?><?php else : ?>—<?php endif; ?></td>
                <td><?php echo is_array($object) && !empty($object['slot_id']) ? '<code>' . esc_html((string) $object['slot_id']) . '</code>' : '—'; ?></td>
                <td><?php if ($published) : ?><span class="ppar-ebay-business-ok">materialisiert</span><?php elseif (is_array($object)) : ?><span class="ppar-ebay-business-warn"><?php echo esc_html((string) ($object['status'] ?? 'review')); ?></span><?php else : ?><span class="ppar-ebay-business-warn">nicht geplant</span><?php endif; ?></td>
                <td><?php echo $reason === '' ? '<span class="ppar-ebay-business-ok">Basis bereit; öffentliche Auslieferung bleibt durch den unveränderten Frontend-Router geschützt.</span>' : esc_html($reason); ?></td>
            </tr><?php endforeach; endif; ?>
            </tbody></table>
            <?php if ($pages > 1) : ?><div class="tablenav"><div class="tablenav-pages"><?php echo wp_kses_post(paginate_links(array('base'=>add_query_arg(array('page'=>'affiliate-portal-ebay-business','s'=>$search,'paged'=>'%#%'), admin_url('admin.php')),'format'=>'','current'=>$paged,'total'=>$pages))); ?></div></div><?php endif; ?>
        </div>
        <?php
    }


    /**
     * V6.61.16 – read-only Portalabdeckung gegen den echten Live-Router.
     * Kein Feedlauf, keine Materialisierung und keinerlei Campaign-Schreibzugriff.
     */
    private function portal_coverage_snapshot() {
        $catalog = $this->ebay_portal_catalog();
        if (is_wp_error($catalog)) { return $catalog; }
        $targets = array_values((array) ($catalog['product_targets'] ?? array()));
        $concepts = array_values((array) ($catalog['business_concepts'] ?? array()));
        $contract = is_array($catalog['business_supply_contract'] ?? null) ? $catalog['business_supply_contract'] : array();
        $required_ids = array_values(array_unique(array_filter(array_map('sanitize_key', (array) ($contract['required_product_concept_ids'] ?? array())))));
        $required = array_fill_keys($required_ids, true);
        $excluded = array();
        foreach ((array) ($contract['excluded_concepts'] ?? array()) as $row) {
            if (!is_array($row)) { continue; }
            $id = sanitize_key((string) ($row['id'] ?? ''));
            if ($id !== '') { $excluded[$id] = sanitize_key((string) ($row['reason'] ?? 'excluded')); }
        }
        $concept_by_target = array();
        foreach ($concepts as $concept) {
            if (!is_array($concept)) { continue; }
            $cid = sanitize_key((string) ($concept['id'] ?? ''));
            foreach ((array) ($concept['target_pages'] ?? array()) as $page) {
                if (!is_array($page)) { continue; }
                $slug = sanitize_title((string) ($page['slug'] ?? ''));
                if ($slug === '') { continue; }
                if (!isset($concept_by_target[$slug])) { $concept_by_target[$slug] = array(); }
                $concept_by_target[$slug][] = array(
                    'id' => $cid,
                    'title' => sanitize_text_field((string) ($concept['title'] ?? '')),
                    'required' => isset($required[$cid]),
                    'excluded_reason' => $excluded[$cid] ?? '',
                );
            }
        }

        // Alle Seiten in einem Query laden; die 329 Ziele werden nicht einzeln aus der DB gesucht.
        $pages_by_slug = array();
        $page_posts = get_posts(array(
            'post_type' => 'page',
            'post_status' => array('publish','draft','private'),
            'numberposts' => -1,
            'orderby' => 'ID',
            'order' => 'ASC',
            'suppress_filters' => true,
        ));
        foreach ((array) $page_posts as $page_post) {
            if (!$page_post instanceof WP_Post) { continue; }
            $slug = sanitize_title((string) $page_post->post_name);
            if ($slug === '') { continue; }
            if (!isset($pages_by_slug[$slug]) || $page_post->post_status === 'publish') { $pages_by_slug[$slug] = $page_post; }
        }

        // Rohbestand je exaktem Produktziel: hilft zu unterscheiden, ob gar nichts
        // materialisiert wurde oder ob eine vorhandene Campaign spaeter an einem Gate scheitert.
        $targeted = array();
        foreach ($this->get_campaigns() as $campaign) {
            if (!is_array($campaign) || sanitize_key((string) ($campaign['creative_type'] ?? '')) !== 'product') { continue; }
            $network = sanitize_key((string) ($campaign['network'] ?? 'manual'));
            if (!in_array($network, array('ebay','idealo'), true)) { continue; }
            foreach ((array) ($campaign['automation_target_keys'] ?? array()) as $target_key) {
                $target_key = $this->automation_normalize_target_key($target_key);
                if (strpos($target_key, 'page:') !== 0) { continue; }
                $slug = sanitize_title(substr($target_key, 5));
                if ($slug === '') { continue; }
                if (!isset($targeted[$slug])) { $targeted[$slug] = array('ebay'=>array('active'=>0,'inactive'=>0),'idealo'=>array('active'=>0,'inactive'=>0)); }
                $bucket = !empty($campaign['active']) ? 'active' : 'inactive';
                $targeted[$slug][$network][$bucket]++;
            }
        }

        $rows = array();
        $summary = array(
            'product_targets' => count($targets),
            'required_concepts' => count($required_ids),
            'physical_target_pages' => 0,
            'excluded_information_pages' => 0,
            'published_target_pages' => 0,
            'missing_or_unpublished_pages' => 0,
            'covered_3' => 0,
            'partial_1_2' => 0,
            'empty_0' => 0,
            'pages_with_ebay_selected' => 0,
            'pages_with_idealo_selected' => 0,
            'pages_with_both_selected' => 0,
        );
        foreach ($targets as $target) {
            if (!is_array($target)) { continue; }
            $slug = sanitize_title((string) ($target['slug'] ?? ''));
            if ($slug === '') { continue; }
            $mapped = array_values((array) ($concept_by_target[$slug] ?? array()));
            $physical = false; $concept_ids = array(); $concept_titles = array(); $excluded_reason = '';
            foreach ($mapped as $m) {
                if (!is_array($m)) { continue; }
                $cid = sanitize_key((string) ($m['id'] ?? ''));
                if ($cid !== '') { $concept_ids[] = $cid; }
                $ct = sanitize_text_field((string) ($m['title'] ?? ''));
                if ($ct !== '') { $concept_titles[] = $ct; }
                if (!empty($m['required'])) { $physical = true; }
                if ($excluded_reason === '' && !empty($m['excluded_reason'])) { $excluded_reason = sanitize_key((string) $m['excluded_reason']); }
            }
            $concept_ids = array_values(array_unique($concept_ids));
            $concept_titles = array_values(array_unique($concept_titles));
            if ($physical) { $summary['physical_target_pages']++; } else { $summary['excluded_information_pages']++; }

            $page = $pages_by_slug[$slug] ?? null;
            $page_id = $page instanceof WP_Post ? absint($page->ID) : 0;
            $page_status = $page instanceof WP_Post ? sanitize_key((string) $page->post_status) : 'missing';
            if ($page_status === 'publish') { $summary['published_target_pages']++; }
            else { $summary['missing_or_unpublished_pages']++; }

            $slot_rows = array(); $providers = array();
            if ($page_id > 0 && $page_status === 'publish' && $this->is_enabled()) {
                $context = $this->get_content_context($page_id);
                for ($i = 1; $i <= 3; $i++) {
                    $slot_type = 'category_product_' . $i;
                    $assigned = $this->assignment_selection_for_slot($context, $slot_type);
                    if (!empty($assigned['handled']) && !empty($assigned['disabled'])) {
                        $slot_rows[] = array('slot'=>$i,'status'=>'disabled_by_assignment','provider'=>'','campaign_id'=>'','campaign_post_id'=>0,'name'=>'','source'=>'','image_url'=>'','reason'=>(string) ($assigned['reason'] ?? ''));
                        continue;
                    }
                    $selection = !empty($assigned['handled']) ? ($assigned['selection'] ?? null) : $this->select_campaign_for_slot($context, $slot_type);
                    $campaign = is_array($selection) ? ($selection['campaign'] ?? null) : null;
                    if (!is_array($campaign)) {
                        $slot_rows[] = array('slot'=>$i,'status'=>'empty','provider'=>'','campaign_id'=>'','campaign_post_id'=>0,'name'=>'','source'=>'','image_url'=>'','reason'=>'');
                        continue;
                    }
                    $network = sanitize_key((string) ($campaign['network'] ?? 'manual'));
                    if ($network !== '') { $providers[$network] = true; }
                    $slot_rows[] = array(
                        'slot' => $i,
                        'status' => 'selected',
                        'provider' => $network,
                        'campaign_id' => sanitize_key((string) ($campaign['id'] ?? '')),
                        'campaign_post_id' => absint($campaign['post_id'] ?? 0),
                        'name' => sanitize_text_field((string) ($campaign['name'] ?? $campaign['title'] ?? '')),
                        'source' => sanitize_key((string) ($campaign['source'] ?? '')),
                        'image_url' => esc_url_raw((string) ($campaign['image_url'] ?? '')),
                        'reason' => sanitize_text_field((string) ($selection['reason'] ?? '')),
                    );
                }
            }
            $selected_count = count(array_filter($slot_rows, static function($r){ return is_array($r) && ($r['status'] ?? '') === 'selected'; }));
            $raw = $targeted[$slug] ?? array('ebay'=>array('active'=>0,'inactive'=>0),'idealo'=>array('active'=>0,'inactive'=>0));
            $raw_active = absint($raw['ebay']['active'] ?? 0) + absint($raw['idealo']['active'] ?? 0);
            $raw_inactive = absint($raw['ebay']['inactive'] ?? 0) + absint($raw['idealo']['inactive'] ?? 0);
            if (!$physical) {
                $status = 'excluded';
                $diagnostic = 'Informatorische Grundlagen-Seite: außerhalb des 311er automatischen Produktvertrags.';
            } elseif ($page_status !== 'publish') {
                $status = 'page_missing';
                $diagnostic = 'Produktziel ist nicht als veröffentlichte WordPress-Seite verfügbar.';
            } elseif (!$this->is_enabled()) {
                $status = 'router_disabled';
                $diagnostic = 'Affiliate-Zentrale ist zentral deaktiviert.';
            } elseif ($selected_count >= 3) {
                $status = 'covered_3';
                $diagnostic = 'Drei auslieferbare Produktpositionen nach dem echten Live-Router.';
            } elseif ($selected_count > 0) {
                $status = 'partial';
                $diagnostic = $selected_count . '/3 auslieferbare Produktpositionen nach dem echten Live-Router.';
            } elseif ($raw_active > 0) {
                $status = 'gated';
                $diagnostic = 'Aktive eBay/idealo-Kampagnen sind auf dieses Ziel gebunden, erreichen aber die drei Live-Slots nach den aktuellen Gates/Providerregeln nicht.';
            } elseif ($raw_inactive > 0) {
                $status = 'inactive_only';
                $diagnostic = 'eBay/idealo-Kampagnen existieren für dieses Ziel, sind aber nicht aktiv.';
            } else {
                $status = 'not_materialized';
                $diagnostic = 'Keine materialisierte eBay-/idealo-Produktkampagne ist auf dieses Produktziel gebunden.';
            }
            if ($physical) {
                if ($selected_count >= 3) { $summary['covered_3']++; }
                elseif ($selected_count > 0) { $summary['partial_1_2']++; }
                else { $summary['empty_0']++; }
            }
            $has_ebay = isset($providers['ebay']); $has_idealo = isset($providers['idealo']);
            if ($physical && $has_ebay) { $summary['pages_with_ebay_selected']++; }
            if ($physical && $has_idealo) { $summary['pages_with_idealo_selected']++; }
            if ($physical && $has_ebay && $has_idealo) { $summary['pages_with_both_selected']++; }
            $rows[] = array(
                'slug' => $slug,
                'title' => sanitize_text_field((string) ($target['title'] ?? '')),
                'main_hub' => sanitize_text_field((string) ($target['main_hub'] ?? '')),
                'hub' => sanitize_text_field((string) ($target['hub'] ?? '')),
                'concept_ids' => $concept_ids,
                'concept_titles' => $concept_titles,
                'physical_contract' => $physical,
                'excluded_reason' => $excluded_reason,
                'page_id' => $page_id,
                'page_status' => $page_status,
                'status' => $status,
                'selected_count' => $selected_count,
                'providers_selected' => array_keys($providers),
                'slots' => $slot_rows,
                'targeted_campaigns' => $raw,
                'diagnostic' => $diagnostic,
            );
        }
        $rank = array('not_materialized'=>0,'gated'=>1,'inactive_only'=>2,'partial'=>3,'page_missing'=>4,'router_disabled'=>5,'covered_3'=>6,'excluded'=>7);
        usort($rows, static function($a,$b) use($rank){
            $ra=$rank[$a['status']??'']??99; $rb=$rank[$b['status']??'']??99;
            if($ra!==$rb){return $ra<=>$rb;}
            foreach(array('main_hub','hub','title') as $k){$c=strnatcasecmp((string)($a[$k]??''),(string)($b[$k]??''));if($c!==0)return $c;}
            return 0;
        });
        $expected = max(1, absint($summary['physical_target_pages']));
        $summary['full_coverage_percent'] = round((100 * absint($summary['covered_3'])) / $expected, 1);
        $summary['any_coverage_percent'] = round((100 * (absint($summary['covered_3']) + absint($summary['partial_1_2']))) / $expected, 1);
        return array(
            'schema' => '1.0',
            'generated_at' => gmdate('c'),
            'plugin_version' => self::VERSION,
            'mode' => 'read_only_live_router_audit',
            'router_enabled' => $this->is_enabled(),
            'catalog_source_sha256' => sanitize_text_field((string) ($catalog['source_sha256'] ?? '')),
            'summary' => $summary,
            'rows' => $rows,
        );
    }

    public function handle_export_portal_coverage() {
        if (!current_user_can('manage_options')) { wp_die('Keine Berechtigung.'); }
        check_admin_referer('ppar_export_portal_coverage');
        $snapshot = $this->portal_coverage_snapshot();
        if (is_wp_error($snapshot)) { wp_die(esc_html($snapshot->get_error_message())); }
        $filename = 'affiliate-portal-coverage-' . gmdate('Ymd-His') . '-utc.json';
        nocache_headers();
        header('Content-Type: application/json; charset=utf-8');
        header('Content-Disposition: attachment; filename="' . $filename . '"');
        echo wp_json_encode($snapshot, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE);
        exit;
    }

    public function render_portal_coverage_page() {
        if (!current_user_can('manage_options')) { wp_die('Keine Berechtigung.'); }
        $snapshot = $this->portal_coverage_snapshot();
        echo '<div class="wrap"><h1>Portalabdeckung</h1>';
        echo '<p><strong>Read-only.</strong> Diese Prüfung verwendet den echten Live-Router und startet weder eBay noch idealo, keinen Feedlauf und keine Materialisierung.</p>';
        if (is_wp_error($snapshot)) { echo '<div class="notice notice-error"><p>'.esc_html($snapshot->get_error_message()).'</p></div></div>'; return; }
        $s=(array)($snapshot['summary']??array());
        echo '<div style="display:flex;flex-wrap:wrap;gap:12px;margin:18px 0">';
        $cards=array(
            'Produktziele'=>absint($s['product_targets']??0),
            'Produktpflicht'=>absint($s['physical_target_pages']??0),
            '3/3 befüllt'=>absint($s['covered_3']??0),
            '1–2/3 befüllt'=>absint($s['partial_1_2']??0),
            '0/3 befüllt'=>absint($s['empty_0']??0),
            'bewusst ohne Produktpflicht'=>absint($s['excluded_information_pages']??0),
        );
        foreach($cards as $label=>$value){echo '<div style="min-width:150px;padding:12px 16px;background:#fff;border:1px solid #dcdcde"><strong style="font-size:22px">'.esc_html((string)$value).'</strong><br><span>'.esc_html($label).'</span></div>';}
        echo '</div>';
        echo '<p><strong>Vollabdeckung:</strong> '.esc_html((string)($s['full_coverage_percent']??0)).'% &nbsp; · &nbsp; <strong>mindestens ein Produkt:</strong> '.esc_html((string)($s['any_coverage_percent']??0)).'% &nbsp; · &nbsp; <strong>eBay ausgewählt:</strong> '.absint($s['pages_with_ebay_selected']??0).' Seiten &nbsp; · &nbsp; <strong>idealo ausgewählt:</strong> '.absint($s['pages_with_idealo_selected']??0).' Seiten.</p>';
        echo '<form method="post" action="'.esc_url(admin_url('admin-post.php')).'" style="margin:16px 0">';
        wp_nonce_field('ppar_export_portal_coverage');
        echo '<input type="hidden" name="action" value="ppar_export_portal_coverage"><button class="button button-primary">JSON-Prüfbericht herunterladen</button></form>';
        echo '<table class="widefat striped"><thead><tr><th>Status</th><th>Produktziel</th><th>Konzept</th><th>Live-Slots</th><th>Rohbestand idealo</th><th>Rohbestand eBay</th><th>Diagnose</th></tr></thead><tbody>';
        foreach((array)($snapshot['rows']??array()) as $row){
            $status=sanitize_key((string)($row['status']??''));
            $selected=absint($row['selected_count']??0);
            $slot_text=array(); foreach((array)($row['slots']??array()) as $slot){if(!is_array($slot))continue;$slot_text[]='#'.absint($slot['slot']??0).' '.(($slot['status']??'')==='selected' ? (($slot['provider']??'').' · '.($slot['name']??'')) : 'leer');}
            $i=(array)(($row['targeted_campaigns']['idealo']??array())); $e=(array)(($row['targeted_campaigns']['ebay']??array()));
            echo '<tr><td><strong>'.esc_html($status).'</strong><br>'.esc_html($selected.'/3').'</td><td><strong>'.esc_html((string)($row['title']??'')).'</strong><br><code>'.esc_html((string)($row['slug']??'')).'</code><br><small>'.esc_html((string)($row['main_hub']??'').' › '.(string)($row['hub']??'')).'</small></td><td>'.esc_html(implode(', ',(array)($row['concept_titles']??array()))).'<br><small>'.esc_html(implode(', ',(array)($row['concept_ids']??array()))).'</small></td><td>'.esc_html(implode(' | ',$slot_text)).'</td><td>aktiv '.absint($i['active']??0).' / inaktiv '.absint($i['inactive']??0).'</td><td>aktiv '.absint($e['active']??0).' / inaktiv '.absint($e['inactive']??0).'</td><td>'.esc_html((string)($row['diagnostic']??'')).'</td></tr>';
        }
        echo '</tbody></table></div>';
    }


    public function render_statistics_page() {
        if (!current_user_can('manage_options')) { wp_die('Keine Berechtigung.'); }
        ?><div class="wrap"><h1>Affiliate-Statistik</h1><p>Lokale Klickzahlen; Netzwerkumsätze werden erst nach gesonderter Transaktionsanbindung ergänzt.</p><table class="widefat striped"><thead><tr><th>Werbemittel</th><th>Art</th><th>Netzwerk</th><th>Klicks gesamt</th><th>Klicks 90 Tage</th></tr></thead><tbody><?php foreach($this->get_campaigns() as $c): $id=absint($c['post_id']??0); ?><tr><td><?php echo esc_html((string)$c['name']); ?></td><td><?php echo esc_html((string)($c['creative_type']??'banner')); ?></td><td><?php echo esc_html($this->provider_label((string)($c['network']??'manual'))); ?></td><td><?php echo absint(get_post_meta($id,'ppar_click_total',true)); ?></td><td><?php echo absint($this->campaign_click_last_days($c,90)); ?></td></tr><?php endforeach; ?></tbody></table></div><?php
    }
    public function admin_menu() {
        add_menu_page('Affiliate-Zentrale','Affiliate-Zentrale','manage_options','affiliate-portal-zentrale',array($this,'render_dashboard_page'),'dashicons-megaphone',59);
        add_submenu_page('affiliate-portal-zentrale','Übersicht','Übersicht','manage_options','affiliate-portal-zentrale',array($this,'render_dashboard_page'));
        add_submenu_page('affiliate-portal-zentrale','Import & Auswahl','Import & Auswahl','manage_options','affiliate-portal-creative-library',array($this,'render_creative_library_page'));
        add_submenu_page('affiliate-portal-zentrale','Ausgaben & Freigabe','Ausgaben & Freigabe','manage_options','affiliate-portal-outputs',array($this,'render_output_objects_page'));
        add_submenu_page('affiliate-portal-zentrale','Steuerung & Veto','Steuerung & Veto','manage_options','affiliate-portal-control',array($this,'render_control_page'));
        add_submenu_page('affiliate-portal-zentrale','Werbemittel','Werbemittel','manage_options','affiliate-portal-creatives',array($this,'render_creatives_page'));
        add_submenu_page('affiliate-portal-zentrale','Zuordnungen','Zuordnungen','manage_options','affiliate-portal-assignments',array($this,'render_assignments_page'));
        add_submenu_page('affiliate-portal-zentrale','Vorschau','Vorschau','manage_options','affiliate-portal-preview',array($this,'render_preview_page'));
        add_submenu_page('affiliate-portal-zentrale','eBay Produktzuordnung','eBay Produktzuordnung','manage_options','affiliate-portal-ebay-business',array($this,'render_ebay_business_assignments_page'));
        add_submenu_page('affiliate-portal-zentrale','Portalabdeckung','Portalabdeckung','manage_options','affiliate-portal-coverage',array($this,'render_portal_coverage_page'));
        add_submenu_page('affiliate-portal-zentrale','Einzelbeiträge','Einzelbeiträge','manage_options','affiliate-portal-article-hybrid',array($this,'render_article_hybrid_page'));
        add_submenu_page('affiliate-portal-zentrale','Netzwerke & API','Netzwerke & API','manage_options','affiliate-portal-networks',array($this,'render_networks_page'));
        $this->provider_register_admin_menus('affiliate-portal-zentrale');
        add_submenu_page('affiliate-portal-zentrale','Partner','Partner','manage_options','affiliate-portal-partners',array($this,'render_partner_directory_page'));
        add_submenu_page('affiliate-portal-zentrale','Synchronisierung','Synchronisierung','manage_options','affiliate-portal-sync',array($this,'render_network_sync_page'));
        add_submenu_page(null,'Awin-Partneraufnahme','Awin-Partneraufnahme','manage_options','affiliate-portal-partner-intake',array($this,'render_partner_intake_page'));
        add_submenu_page('affiliate-portal-zentrale','Automatisierung','Automatisierung','manage_options','affiliate-portal-automation',array($this,'render_automation_page'));
        add_submenu_page('affiliate-portal-zentrale','Statistik','Statistik','manage_options','affiliate-portal-stats',array($this,'render_statistics_page'));
        add_submenu_page('affiliate-portal-zentrale','Prüfzentrum','Prüfzentrum','manage_options','affiliate-portal-health',array($this,'render_health_center_page'));
        add_submenu_page(null,'Affiliate-Werbemittel bearbeiten','Affiliate-Werbemittel bearbeiten','manage_options','affiliate-portal-campaign-edit',array($this,'render_campaign_edit_page'));
        add_submenu_page(null,'Affiliate-Kampagnen Altansicht','Affiliate-Kampagnen Altansicht','manage_options','affiliate-portal-campaigns-legacy',array($this,'render_central_page'));
        add_submenu_page(null,'Affiliate Portal Router - Erweitert','Affiliate Portal Router - Erweitert','manage_options','pferde-affiliate-router',array($this,'render_admin_page'));
        add_submenu_page(null,'Affiliate Portal Prüfung','Affiliate Portal Prüfung','manage_options','affiliate-portal-router-check',array($this,'render_check_page'));
        add_submenu_page(null,'Affiliate Portal Kontrollzentrum','Affiliate Portal Kontrollzentrum','manage_options','affiliate-portal-kontrollzentrum',array($this,'render_control_center_page'));
    }

    public function admin_notices() {
        if (!current_user_can('manage_options')) {
            return;
        }
        if (isset($_GET['ppar_saved']) && $_GET['ppar_saved'] === '1') {
            echo '<div class="notice notice-success is-dismissible"><p>Affiliate-Zentrale: Technische Einstellungen gespeichert.</p></div>';
        }
        if (isset($_GET['ppar_campaigns_saved']) && $_GET['ppar_campaigns_saved'] === '1') {
            echo '<div class="notice notice-success is-dismissible"><p>Affiliate-Zentrale: Kampagnen gespeichert.</p></div>';
        }
        if (isset($_GET['ppar_settings_saved']) && $_GET['ppar_settings_saved'] === '1') {
            echo '<div class="notice notice-success is-dismissible"><p>Affiliate-Zentrale: Grundeinstellungen gespeichert.</p></div>';
        }
        if (isset($_GET['ppar_placeholders_saved']) && $_GET['ppar_placeholders_saved'] === '1') {
            echo '<div class="notice notice-success is-dismissible"><p>Affiliate-Zentrale: Werbeplatz-Platzhalter gespeichert.</p></div>';
        }
        if (isset($_GET['ppar_campaign_saved']) && $_GET['ppar_campaign_saved'] === '1') {
            echo '<div class="notice notice-success is-dismissible"><p>Affiliate-Zentrale: Kampagne gespeichert.</p></div>';
        }
        if (isset($_GET['ppar_networks_saved']) && $_GET['ppar_networks_saved'] === '1') { echo '<div class="notice notice-success is-dismissible"><p>Affiliate-Zentrale: Netzwerkzugänge gespeichert.</p></div>'; }
        if (!empty($_GET['ppar_network_saved'])) { echo '<div class="notice notice-success is-dismissible"><p>'.esc_html($this->provider_label(sanitize_key((string)$_GET['ppar_network_saved'])).': Zugangsdaten gespeichert.').'</p></div>'; }
        if (!empty($_GET['ppar_network_save_error'])) { echo '<div class="notice notice-error"><p>'.esc_html($this->provider_label(sanitize_key((string)$_GET['ppar_network_save_error'])).': Zugangsdaten konnten nicht sicher gespeichert werden.').'</p></div>'; }
        if (!empty($_GET['ppar_assignment_saved'])) { echo '<div class="notice notice-success is-dismissible"><p>Affiliate-Zentrale: Zuordnung gespeichert.</p></div>'; }
        if (!empty($_GET['ppar_assignment_deleted'])) { echo '<div class="notice notice-success is-dismissible"><p>Affiliate-Zentrale: Zuordnung gelöscht.</p></div>'; }
        if (!empty($_GET['ppar_network_test'])) {
            $network = sanitize_key((string)wp_unslash($_GET['ppar_network_test']));
            $status = sanitize_key((string)($_GET['ppar_network_status'] ?? 'unknown'));
            $label = $this->provider_exists($network) ? $this->provider_label($network) : 'Netzwerk';
            $class = $status === 'connected' ? 'notice-success' : (in_array($status, array('saved','not_configured'), true) ? 'notice-info' : 'notice-error');
            $message = $status === 'connected'
                ? 'Verbindungstest bestanden.'
                : ($status === 'saved'
                    ? 'Zugangsdaten gespeichert. Eine echte API-Verbindung wurde noch nicht bestätigt.'
                    : ($status === 'not_configured' ? 'Zugangsdaten fehlen.' : 'Verbindungstest fehlgeschlagen.'));
            echo '<div class="notice ' . esc_attr($class) . ' is-dismissible"><p>' . esc_html($label . ': ' . $message) . '</p></div>';
        }
        if (!empty($_GET['ppar_sync_network'])) {
            $sync_network = strtoupper(sanitize_key((string) $_GET['ppar_sync_network']));
            $sync_status = sanitize_key((string) ($_GET['ppar_sync_status'] ?? 'failed'));
            $sync_class = $sync_status === 'success' ? 'notice-success' : 'notice-error';
            echo '<div class="notice ' . esc_attr($sync_class) . ' is-dismissible"><p>' . esc_html($sync_network . ': Synchronisationslauf abgeschlossen. Details stehen unter „Synchronisierung“.') . '</p></div>';
        }
        if (isset($_GET['ppar_health_saved']) && $_GET['ppar_health_saved'] === '1') {
            echo '<div class="notice notice-success is-dismissible"><p>Affiliate-Zentrale: Prüfeinstellungen gespeichert.</p></div>';
        }
        if (isset($_GET['ppar_health_ran']) && $_GET['ppar_health_ran'] === '1') {
            echo '<div class="notice notice-success is-dismissible"><p>Affiliate-Zentrale: Gesundheitsprüfung abgeschlossen.</p></div>';
        }
        if (isset($_GET['ppar_campaign_deleted']) && $_GET['ppar_campaign_deleted'] === '1') {
            echo '<div class="notice notice-success is-dismissible"><p>Affiliate-Zentrale: Kampagne in den Papierkorb verschoben.</p></div>';
        }
        if (isset($_GET['ppar_campaign_blocked']) && $_GET['ppar_campaign_blocked'] === '1') {
            echo '<div class="notice notice-warning is-dismissible"><p>Die Kampagne war unvollständig und wurde sicherheitshalber inaktiv gespeichert.</p></div>';
        }
        if (!empty($_GET['ppar_campaigns_blocked'])) {
            $count = max(0, (int) $_GET['ppar_campaigns_blocked']);
            echo '<div class="notice notice-warning is-dismissible"><p>Affiliate-Zentrale: ' . esc_html((string) $count) . ' unvollständige Kampagne(n) wurden sicherheitshalber als inaktiv gespeichert.</p></div>';
        }
        if (isset($_GET['ppar_error']) && $_GET['ppar_error'] === 'json') {
            echo '<div class="notice notice-error"><p>Affiliate Portal Router: Das Gruppen-/Banner-JSON ist ungültig. Änderungen wurden nicht gespeichert.</p></div>';
        }
        if (isset($_GET['ppar_error']) && $_GET['ppar_error'] === 'template_json') {
            echo '<div class="notice notice-error"><p>Affiliate Portal Router: Das Template-Regel-JSON ist ungültig. Änderungen wurden nicht gespeichert.</p></div>';
        }
        if (isset($_GET['ppar_error']) && $_GET['ppar_error'] === 'template_word_alle') {
            echo '<div class="notice notice-error"><p>Affiliate Portal Router: Der einzelne Begriff „Alle“ ist als Button/Überschrift verboten. Bitte eindeutige Formulierung verwenden, z. B. „Alle Themen anzeigen“.</p></div>';
        }
        if (isset($_GET['ppar_error']) && $_GET['ppar_error'] === 'design_json') {
            echo '<div class="notice notice-error"><p>Affiliate Portal Router: Das Design-Regel-JSON ist ungültig. Änderungen wurden nicht gespeichert.</p></div>';
        }
        $conflicts = $this->get_conflicting_template_plugins();
        if (!empty($conflicts)) {
            echo '<div class="notice notice-warning"><p><strong>Affiliate Portal Router:</strong> Mögliche Template-Konflikte erkannt: ' . esc_html(implode(', ', $conflicts)) . '. Langfristig sollte nur eine Design-Instanz Startseite/Hubs steuern.</p></div>';
        }
    }
    private static function network_awin_defaults() {
        return array(
            'enabled' => false,
            'publisher_id' => '',
            'access_token' => '',
            'feed_api_key' => '',
            'product_feed_url' => '',
            'product_feed_partner_id' => '',
            'last_status' => 'not_configured',
            'last_checked' => 0,
            'last_message' => '',
            'programme_count' => 0,
            'feed_status' => 'not_configured',
            'feed_count' => 0,
            'last_saved' => 0,
        );
    }
    private static function network_adcell_defaults() {
        return array(
            'enabled' => false,
            'username' => '',
            'password' => '',
            'base_url' => 'https://www.adcell.de/api/v2/',
            'test_path' => '',
            'csv_feed_url' => '',
            'last_status' => 'not_configured',
            'last_checked' => 0,
            'last_message' => '',
            'last_saved' => 0,
        );
    }

    private function network_settings($network) {
        $network = sanitize_key((string)$network);
        if ($network === 'awin') {
            $value = get_option(self::OPTION_NETWORK_AWIN, array());
            return array_merge(self::network_awin_defaults(), is_array($value) ? $value : array());
        }
        $value = get_option(self::OPTION_NETWORK_ADCELL, array());
        return array_merge(self::network_adcell_defaults(), is_array($value) ? $value : array());
    }

    private function network_secret($network, $key, $settings) {
        $constant_map = array(
            'awin.access_token' => 'PPAR_AWIN_ACCESS_TOKEN',
            'awin.feed_api_key' => 'PPAR_AWIN_FEED_API_KEY',
            'adcell.username' => 'PPAR_ADCELL_API_USERNAME',
            'adcell.password' => 'PPAR_ADCELL_API_PASSWORD',
        );
        $map_key = sanitize_key((string)$network) . '.' . sanitize_key((string)$key);
        $constant = $constant_map[$map_key] ?? '';
        if ($constant !== '' && defined($constant) && trim((string)constant($constant)) !== '') {
            return trim((string)constant($constant));
        }
        return trim((string)($settings[$key] ?? ''));
    }
    private function clean_network_secret($value) {
        $value = is_scalar($value) ? (string) wp_unslash($value) : '';
        $value = trim($value);
        return str_replace(array("\0", "\r", "\n"), '', $value);
    }

    private function network_credentials_present($network, $settings = null) {
        $settings = is_array($settings) ? $settings : $this->network_settings($network);
        if ($network === 'awin') {
            return preg_replace('/[^0-9]/', '', (string)($settings['publisher_id'] ?? '')) !== ''
                && $this->network_secret('awin', 'access_token', $settings) !== '';
        }
        return $this->network_secret('adcell', 'username', $settings) !== ''
            && $this->network_secret('adcell', 'password', $settings) !== '';
    }

    private function masked_secret_label($value) {
        $value = trim((string)$value);
        if ($value === '') { return 'nicht gespeichert'; }
        $tail = function_exists('mb_substr') ? mb_substr($value, -3) : substr($value, -3);
        return 'gespeichert (…' . $tail . ')';
    }
    private function sanitize_network_awin($raw, $old) {
        $raw = is_array($raw) ? $raw : array();
        $old = is_array($old) ? $old : self::network_awin_defaults();
        $token = $this->clean_network_secret($raw['access_token'] ?? '');
        $feed = $this->clean_network_secret($raw['feed_api_key'] ?? '');
        if ($token === '') { $token = (string)($old['access_token'] ?? ''); }
        if ($feed === '') { $feed = (string)($old['feed_api_key'] ?? ''); }
        if (!empty($raw['remove_access_token'])) { $token = ''; }
        if (!empty($raw['remove_feed_api_key'])) { $feed = ''; }
        $product_feed_url = array_key_exists('product_feed_url', $raw)
            ? esc_url_raw(trim((string) wp_unslash($raw['product_feed_url'])))
            : (string) ($old['product_feed_url'] ?? '');
        if ($product_feed_url !== '') {
            $validated_feed_url = $this->network_sync_validate_feed_url('awin', $product_feed_url);
            if (is_wp_error($validated_feed_url)) {
                $product_feed_url = (string) ($old['product_feed_url'] ?? '');
            }
        }
        $product_feed_partner_id = array_key_exists('product_feed_partner_id', $raw)
            ? preg_replace('/[^0-9]/', '', (string) wp_unslash($raw['product_feed_partner_id']))
            : preg_replace('/[^0-9]/', '', (string) ($old['product_feed_partner_id'] ?? ''));
        if ($product_feed_url === '') {
            $product_feed_partner_id = '';
        }
        return array_merge($old, array(
            'enabled' => array_key_exists('enabled', $raw) ? !empty($raw['enabled']) : !empty($old['enabled']),
            'publisher_id' => array_key_exists('publisher_id', $raw) ? preg_replace('/[^0-9]/', '', (string)wp_unslash($raw['publisher_id'])) : (string)($old['publisher_id'] ?? ''),
            'access_token' => $token,
            'feed_api_key' => $feed,
            'product_feed_url' => $product_feed_url,
            'product_feed_partner_id' => $product_feed_partner_id,
            'last_saved' => time(),
        ));
    }
    private function sanitize_network_adcell($raw, $old) {
        $raw = is_array($raw) ? $raw : array();
        $old = is_array($old) ? $old : self::network_adcell_defaults();
        $old_username = (string)($old['username'] ?? '');
        $old_password = (string)($old['password'] ?? '');
        $old_test_path = (string)($old['test_path'] ?? '');
        $username = $this->clean_network_secret($raw['username'] ?? '');
        $password = $this->clean_network_secret($raw['password'] ?? '');
        if ($username === '') { $username = $old_username; }
        if ($password === '') { $password = $old_password; }
        if (!empty($raw['remove_username'])) { $username = ''; }
        if (!empty($raw['remove_password'])) { $password = ''; }
        $base = esc_url_raw(trim((string)wp_unslash($raw['base_url'] ?? 'https://www.adcell.de/api/v2/')));
        if (strpos($base, 'https://www.adcell.de/api/v2') !== 0) { $base = 'https://www.adcell.de/api/v2/'; }
        $test_path = $old_test_path;
        if (array_key_exists('test_path', $raw)) {
            $test_path = trim(sanitize_text_field(wp_unslash((string)$raw['test_path'])));
            $official_base = 'https://www.adcell.de/api/v2/';
            if (strpos($test_path, $official_base) === 0) {
                $test_path = substr($test_path, strlen($official_base));
            } elseif (strpos($test_path, '/api/v2/') === 0) {
                $test_path = substr($test_path, strlen('/api/v2/'));
            } elseif (strpos($test_path, 'api/v2/') === 0) {
                $test_path = substr($test_path, strlen('api/v2/'));
            }
            $test_path = ltrim($test_path, '/');
        }
        $csv_feed_url = array_key_exists('csv_feed_url', $raw)
            ? esc_url_raw(trim((string)wp_unslash($raw['csv_feed_url'])))
            : (string)($old['csv_feed_url'] ?? '');
        $credentials_present = trim($username) !== '' && trim($password) !== '';
        $verification_input_changed = $username !== $old_username
            || $password !== $old_password
            || $test_path !== $old_test_path;
        $last_status = sanitize_key((string)($old['last_status'] ?? 'not_configured'));
        $last_checked = absint($old['last_checked'] ?? 0);
        $last_message = sanitize_text_field((string)($old['last_message'] ?? ''));
        if (!$credentials_present) {
            $last_status = 'not_configured';
            $last_checked = 0;
            $last_message = 'API-Benutzername und API-Passwort fehlen.';
        } elseif ($verification_input_changed || in_array($last_status, array('not_configured','pending'), true)) {
            $last_status = 'credentials_saved';
            $last_checked = 0;
            $last_message = $test_path === ''
                ? 'API-Zugangsdaten gespeichert. Die Verbindung ist noch nicht mit einem dokumentierten read-only API-Pfad geprüft.'
                : 'API-Zugangsdaten und read-only Prüfpfad gespeichert. Verbindung noch nicht geprüft.';
        }
        return array_merge($old, array(
            'enabled' => array_key_exists('enabled', $raw) ? !empty($raw['enabled']) : !empty($old['enabled']),
            'username' => $username,
            'password' => $password,
            'base_url' => trailingslashit($base),
            'test_path' => $test_path,
            'csv_feed_url' => $csv_feed_url,
            'last_status' => $last_status,
            'last_checked' => $last_checked,
            'last_message' => $last_message,
            'last_saved' => time(),
        ));
    }
    private function persist_network_settings($network, $raw) {
        $network = sanitize_key((string)$network);
        $old = $this->network_settings($network);
        $new = $network === 'awin'
            ? $this->sanitize_network_awin($raw, $old)
            : $this->sanitize_network_adcell($raw, $old);
        $option = $network === 'awin' ? self::OPTION_NETWORK_AWIN : self::OPTION_NETWORK_ADCELL;
        update_option($option, $new, false);
        $saved = $this->network_settings($network);
        $keys = $network === 'awin' ? array('publisher_id','access_token','feed_api_key','product_feed_url','product_feed_partner_id') : array('username','password','test_path','csv_feed_url');
        foreach ($keys as $key) {
            if ((string)($saved[$key] ?? '') !== (string)($new[$key] ?? '')) {
                return new WP_Error('network_save_failed', 'Die Zugangsdaten konnten nicht vollständig zurückgelesen werden.');
            }
        }
        return $saved;
    }

    public function handle_save_network() {
        if (!current_user_can('manage_options')) { wp_die('Keine Berechtigung.'); }
        $network = sanitize_key((string)($_POST['network'] ?? ''));
        if (!in_array($network, array('awin','adcell'), true)) { wp_die('Unbekanntes Netzwerk.'); }
        check_admin_referer('ppar_save_network_' . $network, 'ppar_network_nonce');
        $posted = isset($_POST['ppar_network'][$network]) && is_array($_POST['ppar_network'][$network]) ? $_POST['ppar_network'][$network] : array();
        $saved = $this->persist_network_settings($network, $posted);
        $return_page = sanitize_key((string) ($_POST['return_page'] ?? 'affiliate-portal-networks'));
        $allowed_return_pages = array('affiliate-portal-networks','affiliate-portal-provider-awin','affiliate-portal-provider-adcell');
        if (!in_array($return_page, $allowed_return_pages, true)) { $return_page = 'affiliate-portal-networks'; }
        $args = array('page'=>$return_page);
        if (is_wp_error($saved)) {
            $args['ppar_network_save_error'] = $network;
        } else {
            $args['ppar_network_saved'] = $network;
            $mode = sanitize_key((string)($_POST['ppar_network_action'] ?? 'save'));
            if ($mode === 'save_test') {
                $result = $network === 'awin' ? $this->test_awin_connection() : $this->test_adcell_connection();
                $settings = $this->network_settings($network);
                $settings['last_status'] = (string)($result['status'] ?? 'failed');
                $settings['last_checked'] = time();
                $settings['last_message'] = sanitize_text_field((string)($result['message'] ?? ''));
                if ($network === 'awin') {
                    $settings['programme_count'] = absint($result['programme_count'] ?? 0);
                    $settings['feed_status'] = sanitize_key((string)($result['feed_status'] ?? 'not_configured'));
                    $settings['feed_count'] = absint($result['feed_count'] ?? 0);
                }
                update_option($network === 'awin' ? self::OPTION_NETWORK_AWIN : self::OPTION_NETWORK_ADCELL, $settings, false);
                $args['ppar_network_test'] = $network;
                $args['ppar_network_status'] = $settings['last_status'] === 'connected' ? 'connected' : (in_array($settings['last_status'], array('credentials_saved','pending'), true) ? 'saved' : ($settings['last_status'] === 'not_configured' ? 'not_configured' : 'failed'));
            }
        }
        wp_safe_redirect(add_query_arg($args, admin_url('admin.php')));
        exit;
    }

    public function handle_save_networks() {
        if (!current_user_can('manage_options')) { wp_die('Keine Berechtigung.'); }
        check_admin_referer('ppar_save_networks', 'ppar_networks_nonce');
        $posted = isset($_POST['ppar_network']) && is_array($_POST['ppar_network']) ? $_POST['ppar_network'] : array();
        $this->persist_network_settings('awin', $posted['awin'] ?? array());
        $this->persist_network_settings('adcell', $posted['adcell'] ?? array());
        wp_safe_redirect(add_query_arg('ppar_networks_saved', '1', admin_url('admin.php?page=affiliate-portal-networks')));
        exit;
    }

    public function handle_test_network() {
        if (!current_user_can('manage_options')) { wp_die('Keine Berechtigung.'); }
        $network = sanitize_key((string)($_POST['network'] ?? ''));
        check_admin_referer('ppar_test_network_' . $network, 'ppar_network_test_nonce');
        $result = $network === 'awin' ? $this->test_awin_connection() : ($network === 'adcell' ? $this->test_adcell_connection() : array('status'=>'failed','message'=>'Unbekanntes Netzwerk.'));
        $option = $network === 'awin' ? self::OPTION_NETWORK_AWIN : self::OPTION_NETWORK_ADCELL;
        $settings = $this->network_settings($network);
        $settings['last_status'] = (string)($result['status'] ?? 'failed');
        $settings['last_checked'] = time();
        $settings['last_message'] = sanitize_text_field((string)($result['message'] ?? ''));
        if ($network === 'awin') {
            $settings['programme_count'] = absint($result['programme_count'] ?? 0);
            $settings['feed_status'] = sanitize_key((string)($result['feed_status'] ?? $settings['feed_status'] ?? 'not_configured'));
            $settings['feed_count'] = absint($result['feed_count'] ?? $settings['feed_count'] ?? 0);
        }
        update_option($option, $settings, false);
        wp_safe_redirect(add_query_arg(array(
            'ppar_network_test' => $network,
            'ppar_network_status' => $settings['last_status'] === 'connected' ? 'connected' : (in_array($settings['last_status'], array('credentials_saved','pending'), true) ? 'saved' : ($settings['last_status'] === 'not_configured' ? 'not_configured' : 'failed')),
        ), admin_url('admin.php?page=affiliate-portal-networks')));
        exit;
    }

    private function api_response($response) {
        if (is_wp_error($response)) {
            return array('ok'=>false,'code'=>0,'body'=>'','message'=>$response->get_error_message());
        }
        $code = (int)wp_remote_retrieve_response_code($response);
        $body = (string)wp_remote_retrieve_body($response);
        return array('ok'=>$code >= 200 && $code < 300,'code'=>$code,'body'=>$body,'message'=>'HTTP ' . $code);
    }
    private function parse_awin_feed_list($body) {
        $body = trim((string)$body);
        if ($body === '') { return array(); }
        $lines = preg_split('/\r\n|\r|\n/', $body);
        if (!$lines || count($lines) < 1) { return array(); }
        $delimiter = substr_count((string)$lines[0], ';') > substr_count((string)$lines[0], ',') ? ';' : ',';
        $header = array_map('trim', str_getcsv((string)array_shift($lines), $delimiter));
        $feeds = array();
        foreach (array_slice($lines, 0, 3000) as $line) {
            if (trim((string)$line) === '') { continue; }
            $values = str_getcsv((string)$line, $delimiter);
            $row = array();
            foreach ($header as $i=>$key) {
                $key = sanitize_key(str_replace(array(' ','-'), '_', strtolower((string)$key)));
                if ($key !== '') { $row[$key] = sanitize_text_field((string)($values[$i] ?? '')); }
            }
            if ($row) { $feeds[] = $row; }
        }
        return $feeds;
    }
    private function test_awin_connection() {
        $settings = $this->network_settings('awin');
        $publisher = preg_replace('/[^0-9]/', '', (string)($settings['publisher_id'] ?? ''));
        $token = $this->network_secret('awin', 'access_token', $settings);
        if ($publisher === '' || $token === '') {
            return array('status'=>'pending','message'=>'Publisher-ID und API-Zugriffstoken fehlen.','programme_count'=>0,'feed_status'=>'not_configured','feed_count'=>0);
        }
        $url = 'https://api.awin.com/publishers/' . rawurlencode($publisher) . '/programmes?relationship=joined';
        $args = array('timeout'=>20,'redirection'=>2,'headers'=>array('Accept'=>'application/json','Authorization'=>'Bearer ' . $token),'limit_response_size'=>1048576);
        $parsed = $this->api_response(wp_remote_get($url, $args));
        if (!$parsed['ok'] && in_array($parsed['code'], array(401,403), true)) {
            $fallback = add_query_arg('accessToken', rawurlencode($token), $url);
            $parsed = $this->api_response(wp_remote_get($fallback, array('timeout'=>20,'redirection'=>2,'headers'=>array('Accept'=>'application/json'),'limit_response_size'=>1048576)));
        }
        if (!$parsed['ok']) {
            return array('status'=>'failed','message'=>'Programmliste nicht erreichbar: ' . $parsed['message'],'programme_count'=>0,'feed_status'=>'not_tested','feed_count'=>0);
        }
        $json = json_decode($parsed['body'], true);
        if (!is_array($json)) {
            return array('status'=>'failed','message'=>'Awin lieferte keine gültige JSON-Programmliste.','programme_count'=>0,'feed_status'=>'not_tested','feed_count'=>0);
        }
        $safe = array();
        foreach (array_slice(array_values($json), 0, 5000) as $programme) {
            if (!is_array($programme)) { continue; }
            $safe[] = array(
                'id' => absint($programme['id'] ?? $programme['advertiserId'] ?? 0),
                'name' => sanitize_text_field((string)($programme['name'] ?? $programme['advertiserName'] ?? '')),
                'relationship' => sanitize_key((string)($programme['relationship'] ?? 'joined')),
            );
        }
        update_option(self::OPTION_NETWORK_AWIN_PROGRAMMES, $safe, false);
        $feed_status = 'not_configured';
        $feed_count = 0;
        $feed_key = $this->network_secret('awin', 'feed_api_key', $settings);
        if ($feed_key !== '') {
            $feed_url = 'https://productdata.awin.com/datafeed/list/apikey/' . rawurlencode($feed_key);
            $feed = $this->api_response(wp_remote_get($feed_url, array('timeout'=>25,'redirection'=>2,'headers'=>array('Accept'=>'text/csv,text/plain'),'limit_response_size'=>2097152)));
            if ($feed['ok'] && trim($feed['body']) !== '') {
                $feeds = $this->parse_awin_feed_list($feed['body']);
                update_option(self::OPTION_NETWORK_AWIN_FEEDS, $feeds, false);
                $feed_count = count($feeds);
                $feed_status = 'connected';
            } else {
                $feed_status = 'failed';
            }
        }
        return array('status'=>'connected','message'=>'Awin-Programme und verfügbare Feedliste wurden read-only synchronisiert.','programme_count'=>count($safe),'feed_status'=>$feed_status,'feed_count'=>$feed_count);
    }

    private function test_adcell_connection() {
        $settings = $this->network_settings('adcell');
        $username = $this->network_secret('adcell', 'username', $settings);
        $password = $this->network_secret('adcell', 'password', $settings);
        $path = ltrim((string)($settings['test_path'] ?? ''), '/');
        if ($username === '' || $password === '') {
            return array('status'=>'not_configured','message'=>'API-Benutzername und API-Passwort fehlen.');
        }
        if ($path === '') {
            return array('status'=>'credentials_saved','message'=>'API-Zugangsdaten sind gespeichert. Eine echte Verbindung wird erst nach Prüfung eines dokumentierten read-only API-Pfads als „Verbunden“ bestätigt.');
        }
        $url = trailingslashit((string)$settings['base_url']) . $path;
        if (strpos($url, 'https://www.adcell.de/api/v2/') !== 0) {
            return array('status'=>'failed','message'=>'Unzulässige ADCELL-API-URL.');
        }
        $response = wp_remote_get($url, array(
            'timeout'=>20,
            'redirection'=>2,
            'headers'=>array('Accept'=>'application/json,application/xml,text/csv,text/plain','Authorization'=>'Basic ' . base64_encode($username . ':' . $password)),
            'limit_response_size'=>524288,
        ));
        $parsed = $this->api_response($response);
        if (!$parsed['ok']) {
            return array('status'=>'failed','message'=>'ADCELL-Testpfad nicht erreichbar: ' . $parsed['message']);
        }
        $body = trim($parsed['body']);
        if ($body === '' || stripos($body, 'API Benutzername') !== false || stripos($body, 'API Passwort') !== false) {
            return array('status'=>'failed','message'=>'ADCELL lieferte keine authentifizierte API-Antwort. Testpfad oder Zugangsdaten prüfen.');
        }
        return array('status'=>'connected','message'=>'ADCELL-API-v2-Testpfad erfolgreich authentifiziert.');
    }

    private function network_status_html($settings) {
        $settings = is_array($settings) ? $settings : array();
        $status = sanitize_key((string)($settings['last_status'] ?? 'not_configured'));
        $looks_like_adcell = array_key_exists('username', $settings) || array_key_exists('password', $settings);
        $saved_adcell_credentials = $looks_like_adcell
            && $this->network_secret('adcell', 'username', $settings) !== ''
            && $this->network_secret('adcell', 'password', $settings) !== '';
        if ($status === 'connected') { return '<span class="ppar-network-status ppar-network-ok">Verbunden</span>'; }
        if ($status === 'credentials_saved' || $status === 'pending' || ($status === 'not_configured' && $saved_adcell_credentials)) {
            return '<span class="ppar-network-status ppar-network-saved">Zugangsdaten gespeichert</span>';
        }
        if ($status === 'failed') { return '<span class="ppar-network-status ppar-network-failed">Prüfung fehlgeschlagen</span>'; }
        return '<span class="ppar-network-status ppar-network-neutral">Nicht eingerichtet</span>';
    }
    public function render_networks_page() {
        if (!current_user_can('manage_options')) { wp_die('Keine Berechtigung.'); }
        $awin = $this->network_settings('awin');
        $adcell = $this->network_settings('adcell');
        $ebay = method_exists($this, 'ebay_settings') ? $this->ebay_settings() : array();
        $ebay_snapshot = method_exists($this, 'provider_access_snapshot') ? $this->provider_access_snapshot('ebay') : array();
        $ebay_compliance = method_exists($this, 'ebay_deletion_compliance_snapshot') ? $this->ebay_deletion_compliance_snapshot() : array();
        $ebay_deletion_token = method_exists($this, 'ebay_deletion_verification_token') ? $this->ebay_deletion_verification_token() : '';
        $ebay_is_production = (string) ($ebay['environment'] ?? 'production') === 'production';
        $ebay_credentials_ready = trim((string) ($ebay['client_id'] ?? '')) !== ''
            && trim((string) ($ebay['client_secret'] ?? '')) !== ''
            && preg_match('/^\d{10}$/', (string) ($ebay['epn_campaign_id'] ?? ''));
        $ebay_enable_allowed = $ebay_credentials_ready && (!$ebay_is_production || (!empty($ebay_compliance['complete']) && (string) ($ebay_snapshot['status'] ?? '') === 'connected'));
        $ebay_oauth_allowed = !$ebay_is_production || !empty($ebay_compliance['challenge_answered']);
        $registry = method_exists($this, 'provider_registry') ? $this->provider_registry() : array();
        $awin_token_const = defined('PPAR_AWIN_ACCESS_TOKEN') && trim((string)PPAR_AWIN_ACCESS_TOKEN) !== '';
        $awin_feed_const = defined('PPAR_AWIN_FEED_API_KEY') && trim((string)PPAR_AWIN_FEED_API_KEY) !== '';
        $adcell_user_const = defined('PPAR_ADCELL_API_USERNAME') && trim((string)PPAR_ADCELL_API_USERNAME) !== '';
        $adcell_pass_const = defined('PPAR_ADCELL_API_PASSWORD') && trim((string)PPAR_ADCELL_API_PASSWORD) !== '';
        $ebay_client_const = defined('PPAR_EBAY_CLIENT_ID') && trim((string)PPAR_EBAY_CLIENT_ID) !== '';
        $ebay_secret_const = defined('PPAR_EBAY_CLIENT_SECRET') && trim((string)PPAR_EBAY_CLIENT_SECRET) !== '';
        $ebay_campaign_const = defined('PPAR_EBAY_EPN_CAMPAIGN_ID') && trim((string)PPAR_EBAY_EPN_CAMPAIGN_ID) !== '';
        $provider_notice = sanitize_key((string) ($_GET['ppar_provider_saved'] ?? ''));
        $provider_tested = sanitize_key((string) ($_GET['ppar_provider_tested'] ?? ''));
        $provider_error = sanitize_text_field(rawurldecode((string) ($_GET['ppar_provider_error'] ?? '')));
        ?>
        <div class="wrap ppar-v240"><style>
        .ppar-v240{max-width:1180px}.ppar-v240-grid{display:grid;grid-template-columns:1fr 1fr;gap:20px}.ppar-v240-card{background:#fff;border:1px solid #c3c4c7;border-radius:10px;padding:22px}.ppar-v240-card h2{margin-top:0}.ppar-v240-card input[type=text],.ppar-v240-card input[type=password],.ppar-v240-card input[type=url],.ppar-v240-card input[type=number]{width:100%}.ppar-v240-actions{display:flex;flex-wrap:wrap;gap:9px;margin-top:18px}.ppar-saved{display:inline-block;margin-left:8px;color:#1d6b2b;font-size:12px;font-weight:600}.ppar-network-status{display:inline-block;padding:4px 9px;border-radius:999px;font-size:12px;font-weight:700}.ppar-network-ok{background:#dff5e1;color:#006b1b}.ppar-network-pending,.ppar-network-saved{background:#e8f0f7;color:#135e96}.ppar-network-failed{background:#fde2e2;color:#9b1c1c}.ppar-network-neutral{background:#e8f0f7;color:#135e96}.ppar-secret-note{font-size:12px;color:#646970}.ppar-api-fields{margin:18px 0;padding:16px;border:1px solid #c3c4c7;border-radius:8px;background:#f6f7f7}.ppar-api-fields h3{margin:0 0 12px}.ppar-compliance-box{margin:18px 0;padding:16px;border:1px solid #c3c4c7;border-radius:8px;background:#f6f7f7}.ppar-compliance-box h3{margin:0 0 8px}.ppar-copy-row{display:grid;grid-template-columns:1fr auto;gap:8px;align-items:end}.ppar-copy-row .button{margin-bottom:1px}.ppar-compliance-status{margin:10px 0 0;padding-left:20px}.ppar-compliance-status li{margin:4px 0}.ppar-hard-block{color:#9b1c1c;font-weight:600}.ppar-ok-text{color:#006b1b;font-weight:600}@media(max-width:850px){.ppar-v240-grid{grid-template-columns:1fr}.ppar-copy-row{grid-template-columns:1fr}}
        </style>
        <h1>Netzwerke &amp; API</h1>
        <p><strong>Zentrale Zugangsebene.</strong> Hier liegen ausschließlich Providerzugänge, Aktivierung und Verbindungstests. Programme, Feeds, Abrufprofile, Verkäufer-/Partnerlogik und sonstige Betriebsregeln liegen auf der jeweiligen Provider-Fachseite. Neue Provider werden über den Provider-Vertrag <?php echo esc_html(self::PROVIDER_CONTRACT_VERSION); ?> registriert und erscheinen hier ohne Umbau des Steuerkerns.</p>
        <?php if ($provider_notice !== '') : ?><div class="notice notice-success inline"><p><?php echo esc_html($this->provider_label($provider_notice) . ': Zugangsdaten gespeichert.' . ($provider_tested === $provider_notice ? ' Verbindungstest ausgeführt.' : '')); ?></p></div><?php endif; ?>
        <?php if ($provider_error !== '') : ?><div class="notice notice-error inline"><p><?php echo esc_html($provider_error); ?></p></div><?php endif; ?>
        <div class="ppar-v240-grid">
          <form class="ppar-v240-card" method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>">
            <input type="hidden" name="action" value="ppar_provider_access_save"><input type="hidden" name="provider" value="awin"><?php wp_nonce_field('ppar_provider_access_awin','ppar_provider_nonce'); ?>
            <h2>Awin <?php echo $this->network_status_html($awin); ?> <?php echo $this->provider_control_badge('awin'); ?></h2>
            <p><label><input type="checkbox" name="ppar_provider[awin][enabled]" value="1" <?php checked(!empty($awin['enabled'])); ?>> Verbindung verwenden</label></p>
            <p><label>Publisher-ID<br><input type="text" inputmode="numeric" name="ppar_provider[awin][publisher_id]" value="<?php echo esc_attr((string)$awin['publisher_id']); ?>"></label></p>
            <p><label>API-Zugriffstoken <span class="ppar-saved"><?php echo esc_html($awin_token_const ? 'über wp-config.php' : $this->masked_secret_label((string)$awin['access_token'])); ?></span><br><input type="password" autocomplete="new-password" name="ppar_provider[awin][access_token]" value="" placeholder="leer lassen zum Beibehalten"></label></p>
            <p><label>Produktfeed-API-Schlüssel <span class="ppar-saved"><?php echo esc_html($awin_feed_const ? 'über wp-config.php' : $this->masked_secret_label((string)$awin['feed_api_key'])); ?></span><br><input type="password" autocomplete="new-password" name="ppar_provider[awin][feed_api_key]" value="" placeholder="optional; leer lassen zum Beibehalten"></label></p>
            <details><summary>Zugangsdaten entfernen</summary><p><label><input type="checkbox" name="ppar_provider[awin][remove_access_token]" value="1"> Token entfernen</label><br><label><input type="checkbox" name="ppar_provider[awin][remove_feed_api_key]" value="1"> Feed-Schlüssel entfernen</label></p></details>
            <p><strong>Programme:</strong> <?php echo absint($awin['programme_count']); ?> · <strong>Feeds:</strong> <?php echo absint($awin['feed_count']); ?><br><strong>Letzte Prüfung:</strong> <?php echo $awin['last_checked'] ? esc_html(wp_date('d.m.Y H:i',(int)$awin['last_checked'])) : 'nie'; ?><br><?php echo esc_html((string)$awin['last_message']); ?></p>
            <div class="ppar-v240-actions"><button class="button button-primary" name="ppar_provider_action" value="save">Speichern</button><button class="button" name="ppar_provider_action" value="save_test">Speichern &amp; Zugang prüfen</button><a class="button" href="<?php echo esc_url(admin_url('admin.php?page=affiliate-portal-provider-awin')); ?>">Awin-Fachseite</a><a class="button" href="<?php echo esc_url($this->provider_control_url('awin')); ?>">Chefsteuerung &amp; Veto</a></div>
          </form>

          <form class="ppar-v240-card" method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>">
            <input type="hidden" name="action" value="ppar_provider_access_save"><input type="hidden" name="provider" value="adcell"><?php wp_nonce_field('ppar_provider_access_adcell','ppar_provider_nonce'); ?>
            <h2>ADCELL <?php echo $this->network_status_html($adcell); ?> <?php echo $this->provider_control_badge('adcell'); ?></h2>
            <p><label><input type="checkbox" name="ppar_provider[adcell][enabled]" value="1" <?php checked(!empty($adcell['enabled'])); ?>> Verbindung verwenden</label></p>
            <p><label>API-Benutzername <span class="ppar-saved"><?php echo esc_html($adcell_user_const ? 'über wp-config.php' : $this->masked_secret_label((string)$adcell['username'])); ?></span><br><input type="password" autocomplete="new-password" name="ppar_provider[adcell][username]" value="" placeholder="leer lassen zum Beibehalten"></label></p>
            <p><label>API-Passwort <span class="ppar-saved"><?php echo esc_html($adcell_pass_const ? 'über wp-config.php' : $this->masked_secret_label((string)$adcell['password'])); ?></span><br><input type="password" autocomplete="new-password" name="ppar_provider[adcell][password]" value="" placeholder="leer lassen zum Beibehalten"></label></p>
            <input type="hidden" name="ppar_provider[adcell][base_url]" value="https://www.adcell.de/api/v2/">
            <div class="ppar-api-fields"><h3>API-Verbindung prüfen</h3><p><label>Dokumentierter read-only Prüfpfad<br><input type="text" name="ppar_provider[adcell][test_path]" value="<?php echo esc_attr((string)$adcell['test_path']); ?>" placeholder="ADCELL-API-v2-Restpfad"></label></p><p class="description">„Verbunden“ wird nur nach authentifizierter Antwort des dokumentierten API-Pfads gesetzt.</p></div>
            <details><summary>Zugangsdaten entfernen</summary><p><label><input type="checkbox" name="ppar_provider[adcell][remove_username]" value="1"> Benutzername entfernen</label><br><label><input type="checkbox" name="ppar_provider[adcell][remove_password]" value="1"> Passwort entfernen</label></p></details>
            <p><strong>Zugangsdaten:</strong> <?php echo $this->network_credentials_present('adcell', $adcell) ? 'gespeichert' : 'nicht vollständig gespeichert'; ?><br><strong>Letzte Prüfung:</strong> <?php echo $adcell['last_checked'] ? esc_html(wp_date('d.m.Y H:i',(int)$adcell['last_checked'])) : 'nie'; ?><br><?php echo esc_html((string)$adcell['last_message']); ?></p>
            <div class="ppar-v240-actions"><button class="button button-primary" name="ppar_provider_action" value="save">Speichern</button><button class="button" name="ppar_provider_action" value="save_test">Speichern &amp; API prüfen</button><a class="button" href="<?php echo esc_url(admin_url('admin.php?page=affiliate-portal-provider-adcell')); ?>">ADCELL-Fachseite</a><a class="button" href="<?php echo esc_url($this->provider_control_url('adcell')); ?>">Chefsteuerung &amp; Veto</a></div>
          </form>

          <form class="ppar-v240-card" method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>">
            <input type="hidden" name="action" value="ppar_provider_access_save"><input type="hidden" name="provider" value="ebay"><?php wp_nonce_field('ppar_provider_access_ebay','ppar_provider_nonce'); ?>
            <h2>eBay <?php echo $this->provider_status_badge($ebay_snapshot); ?> <?php echo $this->provider_control_badge('ebay'); ?></h2>
            <p><label><input type="checkbox" name="ppar_provider[ebay][enabled]" value="1" <?php checked(!empty($ebay['enabled'])); ?> <?php disabled(!$ebay_enable_allowed); ?>> Verbindung verwenden</label><?php if (!$ebay_enable_allowed && $ebay_is_production) : ?><br><span class="ppar-hard-block">Production-Aktivierung bleibt bis vollständigen Zugangsdaten (inkl. 10-stelliger EPN-Campaign-ID), Compliance + erfolgreichem OAuth-Test gesperrt.</span><?php endif; ?></p>
            <p><label>Umgebung<br><select name="ppar_provider[ebay][environment]"><option value="production" <?php selected($ebay['environment'] ?? 'production','production'); ?>>Produktion</option><option value="sandbox" <?php selected($ebay['environment'] ?? 'production','sandbox'); ?>>Sandbox</option></select></label></p>
            <?php if ($ebay_is_production) : ?>
            <div class="ppar-compliance-box">
              <h3>eBay Production-Compliance</h3>
              <p class="description">Marketplace Account Deletion/Closure ist ein nicht übersteuerbarer Hard-Safety-Pfad. Endpoint und Verification Token werden ausschließlich für eBays Pflicht-Validierung verwendet.</p>
              <div class="ppar-copy-row"><label>Notification Endpoint<br><input id="ppar-ebay-deletion-endpoint" type="url" readonly value="<?php echo esc_attr((string)($ebay_compliance['endpoint'] ?? '')); ?>"></label><button type="button" class="button" onclick="pparCopyField('ppar-ebay-deletion-endpoint',this)">Endpoint kopieren</button></div>
              <div class="ppar-copy-row" style="margin-top:10px"><label>Verification Token<br><input id="ppar-ebay-deletion-token" type="password" readonly autocomplete="off" value="<?php echo esc_attr($ebay_deletion_token); ?>"></label><button type="button" class="button" onclick="pparCopyField('ppar-ebay-deletion-token',this)">Token kopieren</button></div>
              <ul class="ppar-compliance-status">
                <li>HTTPS: <?php echo !empty($ebay_compliance['https']) ? '<span class="ppar-ok-text">bereit</span>' : '<span class="ppar-hard-block">nicht bereit</span>'; ?></li>
                <li>eBay-Challenge: <?php echo !empty($ebay_compliance['challenge_answered']) ? '<span class="ppar-ok-text">lokal korrekt beantwortet' . (!empty($ebay_compliance['challenge_answered_at']) ? ' · ' . esc_html(wp_date('d.m.Y H:i',(int)$ebay_compliance['challenge_answered_at'])) : '') . '</span>' : '<span class="ppar-hard-block">noch nicht eingegangen</span>'; ?></li>
                <li>Signierte Testbenachrichtigung: <?php echo !empty($ebay_compliance['signed_notification_verified']) ? '<span class="ppar-ok-text">kryptografisch verifiziert' . (!empty($ebay_compliance['last_notification_at']) ? ' · ' . esc_html(wp_date('d.m.Y H:i',(int)$ebay_compliance['last_notification_at'])) : '') . '</span>' : '<span class="ppar-hard-block">noch nicht verifiziert</span>'; ?></li>
                <?php if (empty($ebay_compliance['signed_notification_verified']) && !empty($ebay_compliance['last_error'])) : ?>
                  <li>Letzter eBay-Notification-Fehler: <span class="ppar-hard-block"><?php echo esc_html((string) $ebay_compliance['last_error']); ?></span></li>
                <?php endif; ?>
              </ul>
              <p class="description">Reihenfolge: Zugangsdaten speichern → Endpoint/Token bei eBay speichern → eBay-Challenge → OAuth prüfen → bei eBay Test Notification senden → Verbindung verwenden.</p>
            </div>
            <?php endif; ?>
            <p><label>Client-ID <span class="ppar-saved"><?php echo esc_html($ebay_client_const ? 'über wp-config.php' : ((string)($ebay['client_id'] ?? '') !== '' ? 'gespeichert' : 'nicht gespeichert')); ?></span><br><input type="text" autocomplete="off" name="ppar_provider[ebay][client_id]" value="<?php echo esc_attr($ebay_client_const ? '' : (string)($ebay['client_id'] ?? '')); ?>" placeholder="<?php echo esc_attr($ebay_client_const ? 'über wp-config.php gesetzt' : ''); ?>"></label></p>
            <p><label>Client-Secret <span class="ppar-saved"><?php echo esc_html($ebay_secret_const ? 'über wp-config.php' : $this->masked_secret_label((string)($ebay['client_secret'] ?? ''))); ?></span><br><input type="password" autocomplete="new-password" name="ppar_provider[ebay][client_secret]" value="" placeholder="leer lassen zum Beibehalten"></label></p>
            <p><label>EPN-Campaign-ID <span class="ppar-saved"><?php echo esc_html($ebay_campaign_const ? 'über wp-config.php' : ''); ?></span><br><input type="text" inputmode="numeric" maxlength="10" name="ppar_provider[ebay][epn_campaign_id]" value="<?php echo esc_attr($ebay_campaign_const ? '' : (string)($ebay['epn_campaign_id'] ?? '')); ?>" placeholder="10 Ziffern"></label></p>
            <p><label>Affiliate-Referenz<br><input type="text" name="ppar_provider[ebay][affiliate_reference_prefix]" value="<?php echo esc_attr((string)($ebay['affiliate_reference_prefix'] ?? 'pferde-atelier')); ?>"></label></p>
            <?php if (!$ebay_secret_const) : ?><details><summary>Zugangsdaten entfernen</summary><p><label><input type="checkbox" name="ppar_provider[ebay][remove_client_secret]" value="1"> Client-Secret entfernen</label></p></details><?php endif; ?>
            <p><strong>Letzte Zugangsprüfung:</strong> <?php echo !empty($ebay_snapshot['last_checked']) ? esc_html(wp_date('d.m.Y H:i',(int)$ebay_snapshot['last_checked'])) : 'nie'; ?><br><?php echo esc_html((string)($ebay_snapshot['message'] ?? '')); ?></p>
            <div class="ppar-v240-actions"><button class="button button-primary" name="ppar_provider_action" value="save">Speichern</button><button class="button" name="ppar_provider_action" value="save_test" <?php disabled(!$ebay_oauth_allowed); ?>>Speichern &amp; OAuth prüfen</button><a class="button" href="<?php echo esc_url(admin_url('admin.php?page=affiliate-portal-ebay')); ?>">eBay-Fachseite</a><a class="button" href="<?php echo esc_url($this->provider_control_url('ebay')); ?>">Chefsteuerung &amp; Veto</a></div>
          </form>
          <script>function pparCopyField(id,button){var f=document.getElementById(id);if(!f){return;}var done=function(){var old=button.textContent;button.textContent='Kopiert';setTimeout(function(){button.textContent=old;},1400);};if(navigator.clipboard&&window.isSecureContext){navigator.clipboard.writeText(f.value).then(done);return;}var type=f.type;f.type='text';f.focus();f.select();try{document.execCommand('copy');done();}catch(e){}f.type=type;window.getSelection&&window.getSelection().removeAllRanges();}</script>

          <?php foreach ($registry as $provider_key => $provider_def) : if (in_array($provider_key, array('awin','adcell','ebay','direct','manual'), true)) { continue; } $snapshot=$this->provider_access_snapshot($provider_key); ?>
          <section class="ppar-v240-card">
            <h2><?php echo esc_html((string)$provider_def['label']); ?> <?php echo $this->provider_status_badge($snapshot); ?> <?php echo $this->provider_control_badge($provider_key); ?></h2>
            <p>Provider ist im zentralen Register vorhanden. Zugangsfelder werden erst ausgegeben, wenn der konkrete Adapter seine dokumentierten Credentials und Verbindungstests registriert.</p>
            <?php do_action('ppar_affiliate_render_provider_access_card_' . $provider_key, $provider_key, $provider_def, self::PROVIDER_CONTRACT_VERSION); ?>
            <p><a class="button" href="<?php echo esc_url($this->provider_control_url($provider_key)); ?>">Chefsteuerung &amp; Veto</a><?php if (!empty($provider_def['specialist_menu']) && !empty($provider_def['specialist_slug'])) : ?> <a class="button" href="<?php echo esc_url(admin_url('admin.php?page=' . $provider_def['specialist_slug'])); ?>">Provider-Fachseite öffnen</a><?php endif; ?></p>
          </section>
          <?php endforeach; ?>
        </div>
        </div><?php
    }

    private static function health_defaults() {
        return array(
            'automatic_enabled' => true,
            'schedule' => 'daily',
            'batch_size' => 25,
            'timeout' => 8,
            'failure_threshold' => 3,
        );
    }

    private static function health_schedule_options() {
        return array(
            'daily' => 'Einmal täglich (empfohlen)',
            'twicedaily' => 'Alle 12 Stunden',
            'hourly' => 'Stündlich',
        );
    }

    private static function sanitize_health_schedule($schedule) {
        $schedule = sanitize_key((string) $schedule);
        return array_key_exists($schedule, self::health_schedule_options()) ? $schedule : 'daily';
    }

    private static function health_schedule_delay($schedule) {
        $schedule = self::sanitize_health_schedule($schedule);
        if ($schedule === 'hourly') {
            return defined('HOUR_IN_SECONDS') ? HOUR_IN_SECONDS : 3600;
        }
        if ($schedule === 'twicedaily') {
            return 12 * (defined('HOUR_IN_SECONDS') ? HOUR_IN_SECONDS : 3600);
        }
        return defined('DAY_IN_SECONDS') ? DAY_IN_SECONDS : 86400;
    }

    /**
     * V2.7.6: Der Prüfzeitplan ist innerhalb der Affiliate-Zentrale wählbar.
     * Bestehende V2.7.5-Installationen werden ressourcenschonend auf täglich
     * migriert. Die festen Sicherheitsstufen bleiben unverändert.
     */
    public function maybe_upgrade_health_checker() {
        $stored_version = (string) get_option(self::OPTION_HEALTH_SCHEMA_VERSION, '');
        if ($stored_version === self::HEALTH_SCHEMA_VERSION) {
            return;
        }
        $stored = get_option(self::OPTION_HEALTH_SETTINGS, array());
        $settings = wp_parse_args(is_array($stored) ? $stored : array(), self::health_defaults());
        $settings['automatic_enabled'] = !empty($settings['automatic_enabled']);
        $settings['schedule'] = self::sanitize_health_schedule($settings['schedule'] ?? 'daily');
        $settings['batch_size'] = max(1, min(100, (int) ($settings['batch_size'] ?? 25)));
        $settings['timeout'] = max(3, min(20, (int) ($settings['timeout'] ?? 8)));
        $settings['failure_threshold'] = 3;
        update_option(self::OPTION_HEALTH_SETTINGS, $settings, false);
        update_option(self::OPTION_HEALTH_SCHEMA_VERSION, self::HEALTH_SCHEMA_VERSION, false);
    }

    public function ensure_health_cron_schedule() {
        $this->reschedule_health_cron(false);
    }

    private function reschedule_health_cron($force = false) {
        if (!function_exists('wp_next_scheduled') || !function_exists('wp_schedule_event')) {
            return;
        }
        $settings = $this->health_settings();
        $next = wp_next_scheduled(self::HEALTH_CRON_HOOK);
        $current_schedule = $next && function_exists('wp_get_schedule') ? (string) wp_get_schedule(self::HEALTH_CRON_HOOK) : '';
        $desired_schedule = self::sanitize_health_schedule($settings['schedule']);

        if (empty($settings['automatic_enabled'])) {
            if ($next && function_exists('wp_clear_scheduled_hook')) {
                wp_clear_scheduled_hook(self::HEALTH_CRON_HOOK);
            }
            return;
        }
        if (!$force && $next && $current_schedule === $desired_schedule) {
            return;
        }
        if ($next && function_exists('wp_clear_scheduled_hook')) {
            wp_clear_scheduled_hook(self::HEALTH_CRON_HOOK);
        }
        wp_schedule_event(time() + self::health_schedule_delay($desired_schedule), $desired_schedule, self::HEALTH_CRON_HOOK);
    }

    private function health_settings() {
        $stored = get_option(self::OPTION_HEALTH_SETTINGS, array());
        $settings = wp_parse_args(is_array($stored) ? $stored : array(), self::health_defaults());
        $settings['automatic_enabled'] = !empty($settings['automatic_enabled']);
        $settings['schedule'] = self::sanitize_health_schedule($settings['schedule'] ?? 'daily');
        $settings['batch_size'] = max(1, min(100, (int) $settings['batch_size']));
        $settings['timeout'] = max(3, min(20, (int) $settings['timeout']));
        // Die Sicherheitsstufen 1/2/3 bleiben fest und sind nicht frei konfigurierbar.
        $settings['failure_threshold'] = 3;
        return $settings;
    }

    private function campaign_health_data($campaign) {
        $post_id = is_array($campaign) ? absint($campaign['post_id'] ?? 0) : absint($campaign);
        $stored = $post_id > 0 ? get_post_meta($post_id, self::HEALTH_META, true) : array();
        return wp_parse_args(is_array($stored) ? $stored : array(), array(
            'schema' => self::HEALTH_SCHEMA_VERSION,
            'state' => 'unknown',
            'previous_state' => 'unknown',
            'message' => 'Noch nicht geprüft.',
            'checked_at' => 0,
            'transition_at' => 0,
            'last_success_at' => 0,
            'last_failure_at' => 0,
            'http_code' => 0,
            'tracking_url' => '',
            'final_url' => '',
            'last_kind' => 'unknown',
            'consecutive_failures' => 0,
            'temporary_failures' => 0,
        ));
    }

    /**
     * Laufzeit-Vetogate. Ein Chef-Veto muss auch dann sofort greifen, wenn ein
     * bereits materialisiertes Ausgabeobjekt/Kampagne noch aktiv markiert ist.
     * Freigaben überschreiben dagegen niemals technische Sicherheitsprüfungen.
     */
    private function campaign_control_allows_delivery($campaign, $slot_type = '') {
        if (!is_array($campaign)) { return false; }
        if (method_exists($this, 'control_emergency_stop_active') && $this->control_emergency_stop_active()) { return false; }
        if (!method_exists($this, 'control_get_decision')) { return true; }
        $portal_key = method_exists($this, 'output_local_portal_key') ? sanitize_key((string) $this->output_local_portal_key()) : '';
        if ($portal_key === '') { return true; }
        $provider = sanitize_key((string) ($campaign['network'] ?? 'manual'));
        if ($provider !== '' && method_exists($this, 'control_provider_gate')) {
            $provider_gate = $this->control_provider_gate($provider, $portal_key);
            if (is_wp_error($provider_gate)) { return false; }
        }
        $partner_id = sanitize_text_field((string) ($campaign['advertiser_id'] ?? ''));
        if ($provider !== '' && $partner_id !== '' && method_exists($this, 'control_partner_gate')) {
            $partner_gate = $this->control_partner_gate(array('provider'=>$provider,'partner_external_id'=>$partner_id), array('key'=>$portal_key));
            if (is_wp_error($partner_gate)) { return false; }
        }
        $post_id = absint($campaign['post_id'] ?? 0);
        $creative_hash = $post_id > 0 ? strtolower(sanitize_text_field((string) get_post_meta($post_id, '_ppar_creative_identity_hash', true))) : '';
        if ($creative_hash !== '' && preg_match('/^[a-f0-9]{64}$/', $creative_hash)) {
            $creative_decision = $this->control_get_decision($portal_key, 'creative', $creative_hash);
            if (!empty($creative_decision['exists']) && (string) ($creative_decision['status'] ?? '') === 'veto') { return false; }
        }
        $output_id = $post_id > 0 ? absint(get_post_meta($post_id, 'ppar_output_object_id', true)) : 0;
        if ($output_id > 0 && method_exists($this, 'control_output_gate')) {
            $output_gate = $this->control_output_gate($portal_key, $output_id);
            if (is_wp_error($output_gate)) { return false; }
        }
        $targets = array_values(array_filter(array_map('sanitize_text_field', (array) ($campaign['automation_target_keys'] ?? array()))));
        if (count($targets) === 1 && method_exists($this, 'control_target_gate')) {
            $target_gate = $this->control_target_gate($portal_key, $targets[0]);
            if (is_wp_error($target_gate)) { return false; }
        }
        $slot_type = sanitize_key((string) $slot_type);
        if ($slot_type !== '' && method_exists($this, 'control_slot_gate')) {
            $slot_gate = $this->control_slot_gate($portal_key, $slot_type);
            if (is_wp_error($slot_gate)) { return false; }
        }
        return true;
    }

    /** Shared live source gate for every public campaign delivery path. */
    private function campaign_source_allows_delivery($campaign) {
        if (!is_array($campaign)) { return false; }
        if (method_exists($this, 'ebay_business_campaign_source_allows_delivery')) {
            return $this->ebay_business_campaign_source_allows_delivery($campaign);
        }
        return true;
    }

    private function campaign_program_allows_delivery($campaign) {
        $status = sanitize_key((string) ($campaign['programme_status'] ?? 'unknown'));
        if (in_array($status, array('paused', 'ended'), true)) {
            return false;
        }
        if (sanitize_key((string) ($campaign['network'] ?? '')) === 'awin') {
            $advertiser_id = absint($campaign['advertiser_id'] ?? 0);
            $portal_key = method_exists($this, 'output_local_portal_key') ? $this->output_local_portal_key() : '';
            return $this->awin_programme_gate_is_allowed($advertiser_id, $portal_key);
        }
        return true;
    }

    private function campaign_health_allows_delivery($campaign) {
        if (empty($campaign['health_check_enabled'])) {
            return true;
        }
        $health = $this->campaign_health_data($campaign);
        return !in_array(sanitize_key((string) ($health['state'] ?? 'unknown')), array('quarantine', 'critical'), true);
    }

    private function health_absolute_redirect($base, $location) {
        $location = trim((string) $location);
        if ($location === '') {
            return '';
        }
        if (preg_match('#^https?://#i', $location)) {
            return esc_url_raw($location);
        }
        $parts = wp_parse_url($base);
        if (!is_array($parts) || empty($parts['scheme']) || empty($parts['host'])) {
            return '';
        }
        if (strpos($location, '//') === 0) {
            return esc_url_raw($parts['scheme'] . ':' . $location);
        }
        $port = !empty($parts['port']) ? ':' . (int) $parts['port'] : '';
        $origin = $parts['scheme'] . '://' . $parts['host'] . $port;
        if (strpos($location, '/') === 0) {
            return esc_url_raw($origin . $location);
        }
        $path = isset($parts['path']) ? (string) $parts['path'] : '/';
        $dir = rtrim(str_replace('\\', '/', dirname($path)), '/');
        return esc_url_raw($origin . ($dir === '' ? '' : $dir) . '/' . $location);
    }

    private function health_transport_error_kind($error) {
        $message = is_wp_error($error) ? strtolower((string) $error->get_error_message()) : strtolower((string) $error);
        if (preg_match('/timed? out|timeout|temporar|connection reset|connection refused|couldn.t connect|too many requests|rate limit/u', $message)) {
            return 'temporary';
        }
        if (preg_match('/could not resolve|name or service not known|no such host|malformed|unsupported protocol|certificate.*expired|ssl certificate/u', $message)) {
            return 'hard';
        }
        // Unklare Transportfehler werden nicht vorschnell gesperrt.
        return 'temporary';
    }

    private function health_remote_step($url, $timeout) {
        $args = array(
            'timeout' => $timeout,
            'redirection' => 0,
            'user-agent' => 'Affiliate-Zentrale/' . self::VERSION . ' Linkprüfung',
            'headers' => array('Accept' => 'text/html,application/xhtml+xml,application/json;q=0.8,*/*;q=0.5'),
        );
        $response = wp_safe_remote_head($url, $args);
        if (is_wp_error($response)) {
            return array('error' => $response->get_error_message(), 'error_kind' => $this->health_transport_error_kind($response), 'code' => 0, 'location' => '');
        }
        $code = (int) wp_remote_retrieve_response_code($response);
        if ($code === 405 && function_exists('wp_safe_remote_get')) {
            $args['limit_response_size'] = 2048;
            $response = wp_safe_remote_get($url, $args);
            if (is_wp_error($response)) {
                return array('error' => $response->get_error_message(), 'error_kind' => $this->health_transport_error_kind($response), 'code' => 0, 'location' => '');
            }
            $code = (int) wp_remote_retrieve_response_code($response);
        }
        return array('error' => '', 'error_kind' => '', 'code' => $code, 'location' => (string) wp_remote_retrieve_header($response, 'location'));
    }

    private function health_follow_url($url, $timeout) {
        $current = esc_url_raw(trim((string) $url));
        if ($current === '' || !preg_match('#^https?://#i', $current)) {
            return array('kind' => 'immediate', 'code' => 0, 'final_url' => $current, 'message' => 'Ungültige oder fehlende HTTP(S)-URL.');
        }
        $visited = array();
        for ($i = 0; $i <= 5; $i++) {
            if (isset($visited[$current])) {
                return array('kind' => 'immediate', 'code' => 0, 'final_url' => $current, 'message' => 'Weiterleitungsschleife erkannt.');
            }
            $visited[$current] = true;
            $step = $this->health_remote_step($current, $timeout);
            if ($step['error'] !== '') {
                $kind = $step['error_kind'] === 'hard' ? 'hard' : 'temporary';
                return array('kind' => $kind, 'code' => 0, 'final_url' => $current, 'message' => 'Link nicht erreichbar: ' . $step['error']);
            }
            $code = (int) $step['code'];
            if ($code >= 300 && $code < 400) {
                $next = $this->health_absolute_redirect($current, $step['location']);
                if ($next === '') {
                    return array('kind' => 'immediate', 'code' => $code, 'final_url' => $current, 'message' => 'Weiterleitung ohne gültiges Ziel.');
                }
                $current = $next;
                continue;
            }
            if ($code >= 200 && $code < 300) {
                return array('kind' => 'ok', 'code' => $code, 'final_url' => $current, 'message' => 'Unabhängige Ziel-URL ist erreichbar.');
            }
            if (in_array($code, array(401, 403, 405, 408, 425, 429), true) || ($code >= 500 && $code <= 599)) {
                return array('kind' => 'temporary', 'code' => $code, 'final_url' => $current, 'message' => 'Vorübergehender oder blockierter Prüfzugriff (HTTP ' . $code . ').');
            }
            if (in_array($code, array(404, 410), true)) {
                return array('kind' => 'immediate', 'code' => $code, 'final_url' => $current, 'message' => 'Ziel nicht mehr vorhanden (HTTP ' . $code . ').');
            }
            return array('kind' => 'hard', 'code' => $code, 'final_url' => $current, 'message' => 'Fehlerhafte Antwort (HTTP ' . $code . ').');
        }
        return array('kind' => 'immediate', 'code' => 0, 'final_url' => $current, 'message' => 'Mehr als fünf Weiterleitungen.');
    }

    private function health_domain_allowed($final_url, $allowed_domains) {
        $allowed_domains = is_array($allowed_domains) ? $allowed_domains : array();
        if (empty($allowed_domains)) {
            return true;
        }
        $host = strtolower((string) wp_parse_url($final_url, PHP_URL_HOST));
        if ($host === '') {
            return false;
        }
        foreach ($allowed_domains as $allowed) {
            $allowed = strtolower(trim((string) $allowed));
            if ($allowed !== '' && ($host === $allowed || substr($host, -strlen('.' . $allowed)) === '.' . $allowed)) {
                return true;
            }
        }
        return false;
    }

    private function health_state_from_result($result, $previous) {
        $kind = sanitize_key((string) ($result['kind'] ?? 'temporary'));
        $hard_failures = max(0, (int) ($previous['consecutive_failures'] ?? 0));
        $temporary_failures = max(0, (int) ($previous['temporary_failures'] ?? 0));
        if ($kind === 'ok') {
            return array('state' => 'ok', 'hard_failures' => 0, 'temporary_failures' => 0);
        }
        if ($kind === 'temporary') {
            return array('state' => 'warning', 'hard_failures' => $hard_failures, 'temporary_failures' => $temporary_failures + 1);
        }
        if ($kind === 'immediate') {
            return array('state' => 'critical', 'hard_failures' => max(3, $hard_failures + 1), 'temporary_failures' => 0);
        }
        $hard_failures++;
        if ($hard_failures >= 3) {
            $state = 'critical';
        } elseif ($hard_failures === 2) {
            $state = 'quarantine';
        } else {
            $state = 'warning';
        }
        return array('state' => $state, 'hard_failures' => $hard_failures, 'temporary_failures' => 0);
    }

    private function evaluate_campaign_health($campaign) {
        $post_id = absint($campaign['post_id'] ?? 0);
        $previous = $this->campaign_health_data($campaign);
        $settings = $this->health_settings();
        $tracking_url = trim((string) ($campaign['url'] ?? ''));
        $destination_url = trim((string) ($campaign['destination_url'] ?? ''));
        if ($destination_url === '' && method_exists($this, 'creative_library_destination_from_tracking')) {
            $destination_url = (string) $this->creative_library_destination_from_tracking($tracking_url);
        }
        $result = array('kind' => 'temporary', 'code' => 0, 'final_url' => '', 'message' => 'Nicht automatisch prüfbar.');

        if (!$this->campaign_program_allows_delivery($campaign)) {
            $result = array('kind' => 'immediate', 'code' => 0, 'final_url' => $destination_url, 'message' => 'Partnerprogramm ist als pausiert oder beendet markiert.');
        } elseif ($tracking_url === '' || !wp_http_validate_url($tracking_url)) {
            $result = array('kind' => 'immediate', 'code' => 0, 'final_url' => '', 'message' => 'Originaler Trackinglink fehlt oder ist syntaktisch ungültig.');
        } else {
            $required = trim((string) ($campaign['required_url_fragment'] ?? ''));
            if ($required !== '' && strpos($tracking_url, $required) === false) {
                $result = array('kind' => 'immediate', 'code' => 0, 'final_url' => $destination_url, 'message' => 'Erforderliches Trackingmerkmal fehlt in der URL.');
            } elseif ($destination_url === '' || !wp_http_validate_url($destination_url)) {
                $result = array('kind' => 'temporary', 'code' => 0, 'final_url' => '', 'message' => 'Trackinglink ist syntaktisch gültig; eine unabhängig prüfbare Ziel-URL fehlt. Der Trackinglink wird nicht automatisiert aufgerufen.');
            } else {
                // Trackinglinks werden niemals automatisiert aufgerufen, damit die
                // technische Prüfung keine Affiliate-Klicks oder Netzwerkereignisse erzeugt.
                $result = $this->health_follow_url($destination_url, (int) $settings['timeout']);
                if ($result['kind'] === 'ok' && !$this->health_domain_allowed($result['final_url'], (array) ($campaign['allowed_domains'] ?? array()))) {
                    $result = array('kind' => 'immediate', 'code' => (int) $result['code'], 'final_url' => (string) $result['final_url'], 'message' => 'Ziel liegt außerhalb der erlaubten Domains.');
                }
                if ($result['kind'] === 'ok' && sanitize_key((string) ($campaign['network'] ?? '')) === 'amazon' && $required === '') {
                    $result = array('kind' => 'temporary', 'code' => (int) $result['code'], 'final_url' => (string) $result['final_url'], 'message' => 'Ziel erreichbar; für Amazon ist noch kein konkretes Trackingmerkmal hinterlegt.');
                }
            }
        }

        $transition = $this->health_state_from_result($result, $previous);
        $now = time();
        $state = $transition['state'];
        $previous_state = sanitize_key((string) ($previous['state'] ?? 'unknown'));
        $health = array(
            'schema' => self::HEALTH_SCHEMA_VERSION,
            'state' => $state,
            'previous_state' => $previous_state,
            'message' => (string) $result['message'],
            'checked_at' => $now,
            'transition_at' => $state !== $previous_state ? $now : (int) ($previous['transition_at'] ?? 0),
            'last_success_at' => $result['kind'] === 'ok' ? $now : (int) ($previous['last_success_at'] ?? 0),
            'last_failure_at' => $result['kind'] === 'ok' ? (int) ($previous['last_failure_at'] ?? 0) : $now,
            'http_code' => (int) $result['code'],
            'tracking_url' => $tracking_url,
            'final_url' => (string) $result['final_url'],
            'last_kind' => sanitize_key((string) $result['kind']),
            'consecutive_failures' => (int) $transition['hard_failures'],
            'temporary_failures' => (int) $transition['temporary_failures'],
        );
        if ($post_id > 0) {
            update_post_meta($post_id, self::HEALTH_META, $health);
        }
        if ($state !== $previous_state && method_exists($this, 'article_plan_log_event')) {
            $this->article_plan_log_event('health_state_changed', 0, array(
                'campaign_post_id' => $post_id,
                'from' => $previous_state,
                'to' => $state,
                'kind' => (string) $health['last_kind'],
            ));
        }
        return $health;
    }

    public function run_scheduled_health_check() {
        $settings = $this->health_settings();
        if (empty($settings['automatic_enabled'])) {
            return array('checked' => 0, 'ok' => 0, 'warning' => 0, 'quarantine' => 0, 'critical' => 0);
        }
        return $this->run_health_check_batch(false);
    }

    private function run_health_check_batch($force_all = false) {
        $settings = $this->health_settings();
        $campaigns = array_values(array_filter($this->get_campaigns(), function ($campaign) {
            return !empty($campaign['active']) && !empty($campaign['health_check_enabled']);
        }));
        $total = count($campaigns);
        $output_summary = method_exists($this, 'output_run_health_batch')
            ? $this->output_run_health_batch($force_all ? 25 : max(1, min(10, (int) $settings['batch_size'])))
            : array('checked'=>0,'ok'=>0,'warning'=>0,'quarantine'=>0);
        if ($total === 0) {
            return array(
                'checked'=>absint($output_summary['checked'] ?? 0),
                'ok'=>absint($output_summary['ok'] ?? 0),
                'warning'=>absint($output_summary['warning'] ?? 0),
                'quarantine'=>absint($output_summary['quarantine'] ?? 0),
                'critical'=>0,
            );
        }
        $limit = $force_all ? min(200, $total) : min((int) $settings['batch_size'], $total);
        $cursor = $force_all ? 0 : max(0, (int) get_option(self::OPTION_HEALTH_CURSOR, 0));
        $summary = array('checked' => 0, 'ok' => 0, 'warning' => 0, 'quarantine' => 0, 'critical' => 0);
        for ($i = 0; $i < $limit; $i++) {
            $campaign = $campaigns[($cursor + $i) % $total];
            $health = $this->evaluate_campaign_health($campaign);
            $state = sanitize_key((string) ($health['state'] ?? 'warning'));
            if (!isset($summary[$state])) {
                $state = 'warning';
            }
            $summary[$state]++;
            $summary['checked']++;
        }
        update_option(self::OPTION_HEALTH_CURSOR, ($cursor + $limit) % $total, false);
        foreach (array('checked','ok','warning','quarantine') as $key) {
            $summary[$key] += absint($output_summary[$key] ?? 0);
        }
        return $summary;
    }

    public function handle_run_health_check() {
        if (!current_user_can('manage_options')) {
            wp_die('Keine Berechtigung.');
        }
        check_admin_referer('ppar_run_health_check', 'ppar_health_nonce');
        $this->run_health_check_batch(true);
        wp_safe_redirect(add_query_arg(array('page' => 'affiliate-portal-health', 'ppar_health_ran' => '1'), admin_url('admin.php')));
        exit;
    }

    public function handle_save_health_settings() {
        if (!current_user_can('manage_options')) {
            wp_die('Keine Berechtigung.');
        }
        check_admin_referer('ppar_save_health_settings', 'ppar_health_settings_nonce');
        $raw = isset($_POST['ppar_health']) && is_array($_POST['ppar_health']) ? wp_unslash($_POST['ppar_health']) : array();
        $settings = array(
            'automatic_enabled' => !empty($raw['automatic_enabled']),
            'schedule' => self::sanitize_health_schedule($raw['schedule'] ?? 'daily'),
            'batch_size' => max(1, min(100, (int) ($raw['batch_size'] ?? 25))),
            'timeout' => max(3, min(20, (int) ($raw['timeout'] ?? 8))),
            'failure_threshold' => 3,
        );
        update_option(self::OPTION_HEALTH_SETTINGS, $settings, false);
        $this->reschedule_health_cron(true);
        wp_safe_redirect(add_query_arg(array('page' => 'affiliate-portal-health', 'ppar_health_saved' => '1'), admin_url('admin.php')));
        exit;
    }

    public function render_health_center_page() {
        if (!current_user_can('manage_options')) {
            wp_die('Keine Berechtigung.');
        }
        $checks = $this->run_diagnostic_checks();
        $system_counts = array('PASS'=>0, 'WARN'=>0, 'FAIL'=>0);
        foreach ($checks as $check) {
            $status = (string) ($check['status'] ?? 'FAIL');
            if (!isset($system_counts[$status])) { $status = 'FAIL'; }
            $system_counts[$status]++;
        }
        $settings = $this->health_settings();
        $rows = $this->get_campaigns();
        $counts = array('ok' => 0, 'warning' => 0, 'quarantine' => 0, 'critical' => 0, 'unknown' => 0);
        foreach ($rows as $row) {
            $state = sanitize_key((string) ($this->campaign_health_data($row)['state'] ?? 'unknown'));
            if (!isset($counts[$state])) { $state = 'unknown'; }
            $counts[$state]++;
        }
        ?>
        <div class="wrap"><h1>Prüfzentrum</h1>
        <section style="background:#fff;border:1px solid #c3c4c7;padding:20px;margin-bottom:20px;max-width:1180px">
            <h2>Systemprüfung</h2>
            <p>Read-only-Prüfung der Pluginversion, Sicherheitsgrenzen, Datenstrukturen und bestehenden Design-Schnittstellen. Es wird nichts angelegt oder verändert. <strong>Diese Systemprüfung ist keine WordPress-/HivePress-Frontend-End-to-End-Abnahme.</strong></p>
            <p><strong>Ergebnis:</strong> <?php echo absint($system_counts['PASS']); ?> PASS · <?php echo absint($system_counts['WARN']); ?> WARN · <?php echo absint($system_counts['FAIL']); ?> FAIL</p>
            <?php if ($system_counts['FAIL'] > 0) : ?><div class="notice notice-error inline"><p><strong>BLOCKED:</strong> Mindestens eine harte Systemprüfung ist fehlgeschlagen.</p></div><?php elseif ($system_counts['WARN'] > 0) : ?><div class="notice notice-warning inline"><p><strong>Harte Prüfungen bestanden.</strong> Warnungen betreffen die konkrete WordPress-Konfiguration oder noch fehlende Daten.</p></div><?php else : ?><div class="notice notice-success inline"><p><strong>PASS:</strong> Systemprüfung bestanden.</p></div><?php endif; ?>
            <details <?php echo $system_counts['FAIL'] > 0 ? 'open' : ''; ?>><summary>Einzelergebnisse anzeigen</summary><table class="widefat striped" style="margin-top:12px"><thead><tr><th>Status</th><th>Bereich</th><th>Prüfung</th><th>Details</th></tr></thead><tbody><?php foreach ($checks as $check) : ?><tr><td><strong><?php echo esc_html((string) $check['status']); ?></strong></td><td><?php echo esc_html((string) $check['area']); ?></td><td><?php echo esc_html((string) $check['label']); ?></td><td><?php echo esc_html((string) $check['details']); ?></td></tr><?php endforeach; ?></tbody></table></details>
        </section>
        <h2>Linkprüfung</h2>
        <p>Prüft aktive Werbemittel und unabhängig bekannte Ziel-URLs. Affiliate-Trackinglinks werden nur syntaktisch geprüft und niemals automatisiert aufgerufen. Das Design, HivePress und andere Plugins werden nicht verändert.</p>
        <div class="notice notice-info inline"><p><strong>Feste Regel:</strong> erster harter Fehler = Warnung; zweiter = Quarantäne und keine Ausspielung; dritter = kritische Sperre. HTTP 404/410 der unabhängigen Ziel-URL, ungültige URL, Weiterleitungsschleife, fehlendes Trackingmerkmal oder fremde Zieldomain werden sofort gesperrt. Timeouts, 5xx und blockierte Prüfanfragen bleiben vorübergehende Warnungen.</p></div>
        <p><strong>Status:</strong> OK <?php echo absint($counts['ok']); ?> · Warnung <?php echo absint($counts['warning']); ?> · Quarantäne <?php echo absint($counts['quarantine']); ?> · Kritisch <?php echo absint($counts['critical']); ?> · Ungeprüft <?php echo absint($counts['unknown']); ?></p>
        <div style="display:grid;grid-template-columns:minmax(280px,420px) 1fr;gap:20px;align-items:start">
        <?php
        $schedule_options = self::health_schedule_options();
        $runs_per_day = $settings['schedule'] === 'hourly' ? 24 : ($settings['schedule'] === 'twicedaily' ? 2 : 1);
        $daily_capacity = (int) $settings['batch_size'] * $runs_per_day;
        ?>
        <form style="background:#fff;border:1px solid #c3c4c7;padding:20px" method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>"><input type="hidden" name="action" value="ppar_save_health_settings"><?php wp_nonce_field('ppar_save_health_settings', 'ppar_health_settings_nonce'); ?><h2>Automatische Linkprüfung</h2><p><label><input type="checkbox" name="ppar_health[automatic_enabled]" value="1" <?php checked(!empty($settings['automatic_enabled'])); ?>> Automatische Linkprüfung aktivieren</label></p><p><label>Prüfrhythmus<br><select name="ppar_health[schedule]"><?php foreach ($schedule_options as $schedule_key => $schedule_label): ?><option value="<?php echo esc_attr($schedule_key); ?>" <?php selected($settings['schedule'], $schedule_key); ?>><?php echo esc_html($schedule_label); ?></option><?php endforeach; ?></select></label></p><p><label>Werbemittel je Lauf<br><input type="number" min="1" max="100" name="ppar_health[batch_size]" value="<?php echo esc_attr((string) $settings['batch_size']); ?>"></label></p><p><label>Zeitlimit je Anfrage in Sekunden<br><input type="number" min="3" max="20" name="ppar_health[timeout]" value="<?php echo esc_attr((string) $settings['timeout']); ?>"></label></p><p class="description">Empfohlen: einmal täglich. Mit der aktuellen Einstellung werden bis zu <?php echo absint($daily_capacity); ?> Werbemittel pro Tag geprüft. Weiterleitungen können mehrere HTTP-Anfragen pro Werbemittel auslösen. Kritische und quarantänisierte Links bleiben in der Prüfung, damit eine Wiederherstellung erkannt wird.</p><?php submit_button('Prüfeinstellungen speichern'); ?></form>
        <div><form method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>" style="margin-bottom:14px"><input type="hidden" name="action" value="ppar_run_health_check"><?php wp_nonce_field('ppar_run_health_check', 'ppar_health_nonce'); ?><button class="button button-primary">Bis zu 200 aktive Werbemittel jetzt prüfen</button></form><table class="widefat striped"><thead><tr><th>Werbemittel</th><th>Netzwerk / Programm</th><th>Prüfstatus</th><th>Letzte Prüfung</th><th>Ergebnis</th></tr></thead><tbody><?php if (!$rows): ?><tr><td colspan="5">Noch keine Werbemittel vorhanden.</td></tr><?php else: foreach ($rows as $campaign): $health = $this->campaign_health_data($campaign); $programme = sanitize_key((string) ($campaign['programme_status'] ?? 'unknown')); ?><tr><td><strong><?php echo esc_html((string) ($campaign['name'] ?? '')); ?></strong><br><?php echo !empty($campaign['active']) ? 'aktiv' : 'inaktiv'; ?></td><td><?php echo esc_html($this->provider_label((string)($campaign['network']??'manual'))); ?><br><?php echo esc_html((string) ($campaign['programme_name'] ?? $campaign['partner'] ?? '')); ?><?php if ($programme !== 'unknown'): ?><br>Programm: <?php echo esc_html($programme); ?><?php endif; ?></td><td><strong><?php echo esc_html(strtoupper((string) $health['state'])); ?></strong><br>Harte Fehler: <?php echo absint($health['consecutive_failures']); ?> · temporär: <?php echo absint($health['temporary_failures']); ?></td><td><?php echo !empty($health['checked_at']) ? esc_html(wp_date('d.m.Y H:i', (int) $health['checked_at'])) : 'nie'; ?></td><td><?php echo esc_html((string) $health['message']); ?><?php if (!empty($health['http_code'])): ?><br>HTTP <?php echo absint($health['http_code']); ?><?php endif; ?><?php if (!empty($health['final_url'])): ?><br><small>Endziel: <?php echo esc_html((string) $health['final_url']); ?></small><?php endif; ?></td></tr><?php endforeach; endif; ?></tbody></table></div></div></div><?php
    }

    private function central_placement_options() {
        return array(
            'product_after_category_tiles' => 'Produkt-/Kategorieseite: Affiliate-Banner',
            'category_product' => 'Produkt-/Kategorieseite: Produktvorschläge 1–3',
            'start_after_topics' => 'Startseite: nach den ausgewählten Themen',
            'anzeigenmarkt_top_banner' => 'Anzeigenstartseite: Partnerbanner über den Anzeigen',
            'journal_banner' => 'Journal: Partnerbanner',
            'journal_product_1' => 'Journal: Produktvorschlag 1',
            'journal_product_2' => 'Journal: Produktvorschlag 2',
            'journal_product_3' => 'Journal: Produktvorschlag 3',
            'hub_grid_card' => 'Hub-Raster: Partnerkachel',
            'hub_top_cta' => 'Hub: oberhalb der Kacheln',
            'hub_after_cards' => 'Hub: nach den Kacheln',
            'hub_mid_banner' => 'Hub: mittlerer Bannerblock',
            'category_recommendation' => 'Kategoriearchiv: Empfehlung',
            'post_inline_banner' => 'Einzelbeitrag-Hybrid: ein Banner im Inhalt',
            'post_bottom_products' => 'Einzelbeitrag-Hybrid: Produktvorschläge am Ende',
            'post_after_intro' => 'Beitrag: nach der Einleitung (Legacy)',
            'post_mid_content' => 'Beitrag: in der Mitte (Legacy)',
            'post_bottom_recommendation' => 'Beitrag: am Ende (Legacy)',
        );
    }

    private static function placeholder_defaults() {
        return array(
            'enabled' => false,
            'label' => '',
            'title' => '',
            'description' => '',
            'button_text' => '',
            'url' => '',
            'target' => '_self',
            'start_enabled' => true,
            'start_image_id' => 0,
            'start_image_url' => '',
            'start_image_b_id' => 0,
            'start_image_b_url' => '',
            'hub1_enabled' => true,
            'hub2_enabled' => true,
            'hub_image_id' => 0,
            'hub_image_url' => '',
            'hub_image_b_id' => 0,
            'hub_image_b_url' => '',
            'category_enabled' => true,
            'category_grid_image_id' => 0,
            'category_grid_image_url' => '',
            'category_grid_image_b_id' => 0,
            'category_grid_image_b_url' => '',
            'category_image_id' => 0,
            'category_image_url' => '',
            // V2.2.5: Bei jeder Speicherung neu gesetzt. Die Revision wird an
            // die Bild-URL angehaengt, damit Browser/CDN/Page-Cache kein altes
            // Platzhalterbild weiterverwenden koennen.
            'revision' => 0,
        );
    }

    private function get_placeholder_settings() {
        $stored = get_option(self::OPTION_PLACEHOLDER_SETTINGS, array());
        $settings = wp_parse_args(is_array($stored) ? $stored : array(), self::placeholder_defaults());
        foreach (array('enabled', 'start_enabled', 'hub1_enabled', 'hub2_enabled', 'category_enabled') as $key) {
            $settings[$key] = !empty($settings[$key]);
        }
        foreach (array('start_image_id', 'start_image_b_id', 'hub_image_id', 'hub_image_b_id', 'category_grid_image_id', 'category_grid_image_b_id', 'category_image_id') as $key) {
            $settings[$key] = absint($settings[$key]);
        }
        foreach (array('start_image_url', 'start_image_b_url', 'hub_image_url', 'hub_image_b_url', 'category_grid_image_url', 'category_grid_image_b_url', 'category_image_url') as $key) {
            $settings[$key] = esc_url_raw((string)($settings[$key] ?? ''));
        }
        // V2.2.8: Ebene 3 besitzt nur noch ein wirksames Kachelbild. ID und
        // direkte Mediathek-URL werden gemeinsam gespeichert, damit weder ein
        // historisches Aliasfeld noch ein abweichender Storage/CDN-Pfad die neue
        // Auswahl auf das alte Bild zuruecksetzt.
        // Installationen koennen das Bild noch im alten Fallback-Feld gespeichert
        // haben; beide Werte werden deshalb beim Lesen synchronisiert.
        if ($settings['category_grid_image_id'] <= 0 && $settings['category_image_id'] > 0) {
            $settings['category_grid_image_id'] = $settings['category_image_id'];
        }
        if ($settings['category_grid_image_id'] > 0) {
            $settings['category_image_id'] = $settings['category_grid_image_id'];
        }
        if ($settings['category_grid_image_url'] === '' && $settings['category_image_url'] !== '') {
            $settings['category_grid_image_url'] = $settings['category_image_url'];
        }
        if ($settings['category_grid_image_url'] !== '') {
            $settings['category_image_url'] = $settings['category_grid_image_url'];
        }
        // V2.2.17: Eine zentrale Bildquelle fuer alle Platzierungen. Die auf der
        // Startseite bereits funktionierende Auswahl A ist verbindlich. Nur bei
        // leerem A/B wird einmalig aus historischen Hub-/Kategorie-Feldern gelesen.
        if ($settings['start_image_id'] <= 0) {
            $settings['start_image_id'] = $settings['hub_image_id'] > 0
                ? $settings['hub_image_id']
                : ($settings['category_grid_image_id'] > 0 ? $settings['category_grid_image_id'] : 0);
        }
        if ($settings['start_image_b_id'] <= 0) {
            $settings['start_image_b_id'] = $settings['hub_image_b_id'] > 0
                ? $settings['hub_image_b_id']
                : ($settings['category_grid_image_b_id'] > 0 ? $settings['category_grid_image_b_id'] : 0);
        }
        if ($settings['start_image_url'] === '') {
            $settings['start_image_url'] = $settings['hub_image_url'] !== ''
                ? $settings['hub_image_url']
                : $settings['category_grid_image_url'];
        }
        if ($settings['start_image_b_url'] === '') {
            $settings['start_image_b_url'] = $settings['hub_image_b_url'] !== ''
                ? $settings['hub_image_b_url']
                : $settings['category_grid_image_b_url'];
        }
        $settings['revision'] = sanitize_key((string)($settings['revision'] ?? ''));
        // V2.2.3: Platzhalter sind ausnahmslos bild-only. Historisch gespeicherte Texte werden ignoriert.
        $settings['label'] = '';
        $settings['title'] = '';
        $settings['description'] = '';
        $settings['button_text'] = '';
        $settings['url'] = esc_url_raw((string) $settings['url']);
        $settings['target'] = $settings['target'] === '_blank' ? '_blank' : '_self';
        return $settings;
    }

    private function sanitize_placeholder_settings($raw) {
        $raw = is_array($raw) ? $raw : array();
        $out = self::placeholder_defaults();
        foreach (array('enabled', 'start_enabled', 'hub1_enabled', 'hub2_enabled', 'category_enabled') as $key) {
            $out[$key] = !empty($raw[$key]);
        }
        foreach (array('start_image_id', 'start_image_b_id', 'hub_image_id', 'hub_image_b_id', 'category_grid_image_id', 'category_grid_image_b_id', 'category_image_id') as $key) {
            $out[$key] = isset($raw[$key]) ? absint($raw[$key]) : 0;
        }
        foreach (array('start_image_url', 'start_image_b_url', 'hub_image_url', 'hub_image_b_url', 'category_grid_image_url', 'category_grid_image_b_url', 'category_image_url') as $key) {
            $out[$key] = isset($raw[$key]) ? esc_url_raw(trim((string)wp_unslash($raw[$key]))) : '';
        }
        $out['revision'] = isset($raw['revision']) ? sanitize_key((string)wp_unslash($raw['revision'])) : '';
        // Textfelder werden nicht mehr gespeichert: Platzhalter sind verbindlich bild-only.
        $out['label'] = '';
        $out['title'] = '';
        $out['description'] = '';
        $out['button_text'] = '';
        $out['url'] = isset($raw['url']) ? esc_url_raw(trim((string) wp_unslash($raw['url']))) : '';
        $out['target'] = isset($raw['target']) && (string) $raw['target'] === '_blank' ? '_blank' : '_self';
        return $out;
    }

    private static function placeholder_image_keys() {
        return array('start_image_id', 'start_image_b_id', 'hub_image_id', 'hub_image_b_id', 'category_grid_image_id', 'category_grid_image_b_id', 'category_image_id');
    }

    private static function placeholder_image_url_key($key) {
        $map = array(
            'start_image_id' => 'start_image_url',
            'start_image_b_id' => 'start_image_b_url',
            'hub_image_id' => 'hub_image_url',
            'hub_image_b_id' => 'hub_image_b_url',
            'category_grid_image_id' => 'category_grid_image_url',
            'category_grid_image_b_id' => 'category_grid_image_b_url',
            'category_image_id' => 'category_image_url',
        );
        return isset($map[$key]) ? $map[$key] : '';
    }

    /**
     * V2.2.7: Einheitliche Auswahl für das eine wirksame Ebene-3-Bild.
     * Unterstützt zugleich alte Formulare, die noch category_image_id senden.
     */
    private function resolve_category_placeholder_image_id($raw, $old_settings) {
        $raw = is_array($raw) ? $raw : array();
        $old_settings = is_array($old_settings) ? $old_settings : array();
        $raw_grid = isset($raw['category_grid_image_id']) ? absint($raw['category_grid_image_id']) : 0;
        $raw_legacy = isset($raw['category_image_id']) ? absint($raw['category_image_id']) : 0;
        $old_grid = absint($old_settings['category_grid_image_id'] ?? 0);
        $old_legacy = absint($old_settings['category_image_id'] ?? 0);
        if (array_key_exists('category_grid_image_id', $raw) && $raw_grid !== $old_grid) {
            return $raw_grid;
        }
        if (array_key_exists('category_image_id', $raw) && $raw_legacy !== $old_legacy) {
            return $raw_legacy;
        }
        if ($raw_grid > 0) { return $raw_grid; }
        if ($raw_legacy > 0) { return $raw_legacy; }
        return $old_grid;
    }

    private function resolve_category_placeholder_image_url($raw, $old_settings, $resolved_id) {
        $raw = is_array($raw) ? $raw : array();
        $old_settings = is_array($old_settings) ? $old_settings : array();
        $grid_url = isset($raw['category_grid_image_url']) ? esc_url_raw(trim((string)wp_unslash($raw['category_grid_image_url']))) : '';
        $legacy_url = isset($raw['category_image_url']) ? esc_url_raw(trim((string)wp_unslash($raw['category_image_url']))) : '';
        if ($grid_url !== '') { return $grid_url; }
        if ($legacy_url !== '') { return $legacy_url; }
        if ($resolved_id > 0 && function_exists('wp_get_attachment_image_url')) {
            $resolved = wp_get_attachment_image_url($resolved_id, 'full');
            if (is_string($resolved) && trim($resolved) !== '') { return esc_url_raw($resolved); }
        }
        return esc_url_raw((string)($old_settings['category_grid_image_url'] ?? $old_settings['category_image_url'] ?? ''));
    }

    private function placeholder_attachment_url($settings, $key) {
        if (!in_array((string) $key, self::placeholder_image_keys(), true)) { return ''; }
        $attachment_id = !empty($settings[$key]) ? absint($settings[$key]) : 0;
        // Die aktuelle Attachment-ID ist die verbindliche Quelle. Eine alte
        // gespeicherte URL darf ein neu ausgewaehltes Mediathekbild nie ueberstimmen.
        if ($attachment_id > 0 && function_exists('wp_get_attachment_image_url')) {
            $url = wp_get_attachment_image_url($attachment_id, 'full');
            if (is_string($url) && trim($url) !== '') { return esc_url_raw($url); }
        }
        $url_key = self::placeholder_image_url_key($key);
        return $url_key !== '' ? esc_url_raw((string)($settings[$url_key] ?? '')) : '';
    }

    private function placeholder_image_url($settings, $key) {
        if (!in_array((string) $key, self::placeholder_image_keys(), true)) { return ''; }
        $url = $this->placeholder_attachment_url($settings, $key);
        if ($url === '') { return ''; }
        $attachment_id = !empty($settings[$key]) ? absint($settings[$key]) : 0;
        $revision = sanitize_key((string)($settings['revision'] ?? '0')) ?: '0';
        if (function_exists('add_query_arg')) {
            return esc_url_raw(add_query_arg('ppar_v', $attachment_id . '-' . $revision, $url));
        }
        return $url;
    }

    public function handle_placeholder_image() {
        $key = isset($_GET['key']) ? sanitize_key(wp_unslash((string) $_GET['key'])) : '';
        if (!in_array($key, self::placeholder_image_keys(), true)) {
            if (function_exists('status_header')) { status_header(404); }
            exit;
        }
        $settings = $this->get_placeholder_settings();
        $url = $this->placeholder_attachment_url($settings, $key);
        if ($url === '') {
            if (function_exists('status_header')) { status_header(404); }
            exit;
        }

        if (function_exists('nocache_headers')) { nocache_headers(); }
        if (!headers_sent()) {
            header('Cache-Control: no-store, no-cache, must-revalidate, max-age=0');
            header('Pragma: no-cache');
            header('Expires: Wed, 11 Jan 1984 05:00:00 GMT');
            header('X-Robots-Tag: noindex, nofollow', true);
        }

        // V2.2.7: Lokale Mediathek-Dateien werden direkt gestreamt. Ein Browser
        // kann damit keinen alten Redirect auf die vorherige Attachment-URL merken.
        $attachment_id = !empty($settings[$key]) ? absint($settings[$key]) : 0;
        $file = $attachment_id > 0 && function_exists('get_attached_file') ? get_attached_file($attachment_id) : '';
        if (is_string($file) && $file !== '' && is_file($file) && is_readable($file)) {
            $mime = function_exists('get_post_mime_type') ? (string)get_post_mime_type($attachment_id) : '';
            if ($mime === '' && function_exists('wp_check_filetype')) {
                $checked = wp_check_filetype($file);
                $mime = is_array($checked) ? (string)($checked['type'] ?? '') : '';
            }
            if (!headers_sent()) {
                if ($mime !== '') { header('Content-Type: ' . $mime); }
                $size = filesize($file);
                if ($size !== false) { header('Content-Length: ' . (string)$size); }
                header('Content-Disposition: inline; filename="' . basename($file) . '"');
            }
            readfile($file);
            exit;
        }

        // Offloaded Media/CDN: nur wenn keine lokale Datei existiert, bleibt der
        // nicht cachebare Redirect als Fallback bestehen.
        if (function_exists('wp_redirect')) {
            wp_redirect($url, 302, 'Affiliate-Zentrale');
        } else {
            header('Location: ' . $url, true, 302);
        }
        exit;
    }

    /**
     * V2.2.7: Platzhalterbilder werden in gecachten Frontends sonst oft erst
     * Stunden spaeter sichtbar. Nur beim bewussten Speichern der Platzhalter
     * werden verbreitete Cache-Systeme gezielt geleert.
     */
    private function purge_placeholder_frontend_caches() {
        if (function_exists('wp_cache_flush')) { wp_cache_flush(); }
        if (function_exists('rocket_clean_domain')) { rocket_clean_domain(); }
        if (function_exists('w3tc_flush_all')) { w3tc_flush_all(); }
        do_action('litespeed_purge_all');
        do_action('cache_enabler_clear_complete_cache');
        do_action('wpfc_clear_all_cache');
        do_action('ppar_placeholder_images_updated');
    }

    private function render_placeholder_image_field($key, $label, $description, $settings) {
        $field_id = 'ppar_placeholder_' . sanitize_key($key);
        $attachment_id = !empty($settings[$key]) ? absint($settings[$key]) : 0;
        $direct_url_key = self::placeholder_image_url_key($key);
        $direct_url = $direct_url_key !== '' ? esc_url_raw((string)($settings[$direct_url_key] ?? '')) : '';
        $url = $this->placeholder_image_url($settings, $key);
        echo '<tr><th scope="row">' . esc_html($label) . '</th><td>';
        echo '<input type="hidden" id="' . esc_attr($field_id) . '" name="ppar_placeholder[' . esc_attr($key) . ']" value="' . esc_attr((string) $attachment_id) . '">';
        echo '<input type="hidden" id="' . esc_attr($field_id) . '_url" name="ppar_placeholder[' . esc_attr($direct_url_key) . ']" value="' . esc_attr($direct_url) . '">';
        echo '<div style="margin-bottom:10px;max-width:520px;">';
        echo '<img id="' . esc_attr($field_id) . '_preview" src="' . esc_url($url) . '" alt="" style="display:' . ($url !== '' ? 'block' : 'none') . ';max-width:100%;height:auto;border:1px solid #dcdcde;border-radius:6px;">';
        echo '<span id="' . esc_attr($field_id) . '_empty" class="description" style="display:' . ($url === '' ? 'inline' : 'none') . ';">Noch kein Bild ausgewählt.</span>';
        echo '</div>';
        echo '<button type="button" class="button ppar-placeholder-image-select" data-field="' . esc_attr($field_id) . '">Aus Mediathek wählen</button> ';
        echo '<button type="button" class="button-link-delete ppar-placeholder-image-remove" data-field="' . esc_attr($field_id) . '">Bild entfernen</button>';
        echo '<p class="description">' . esc_html($description) . '</p></td></tr>';
    }

    private function central_blank_campaign() {
        return array(
            'post_id' => 0,
            'id' => '',
            'name' => '',
            'partner' => '',
            'creative_type' => 'banner',
            'network' => 'manual',
            'advertiser_id' => '',
            'programme_name' => '',
            'programme_status' => 'unknown',
            'programme_status_source' => '',
            'programme_status_checked_at' => 0,
            'quality_manual_status' => 'unknown',
            'quality_note' => '',
            'render_mode' => 'image_link',
            'html' => '',
            'price' => '',
            'currency' => 'EUR',
            'availability' => '',
            'dimensions' => '',
            'last_synced' => 0,
            'active' => false,
            'assignment_mode' => 'page_tree',
            'page_id' => 0,
            'auto_topic_label' => '',
            'auto_topic_score' => 0,
            'auto_topic_reason' => '',
            'match_descendants' => true,
            'match_slugs' => array(),
            'match_keywords' => array(),
            'match_term_ids' => array(),
            'automation_target_keys' => array(),
            'priority' => 50,
            'start_date' => '',
            'end_date' => '',
            'placements' => array('hub_grid_card'),
            'label' => 'Anzeige',
            'title' => '',
            'description' => '',
            'button_text' => 'Mehr erfahren',
            'image_url' => '',
            'url' => '',
            'target' => '_blank',
            'subid_param' => '',
            'required_url_fragment' => '',
            'allowed_domains' => array(),
            'health_check_enabled' => true,
            'source' => 'manual',
            'external_id' => '',
            'product_gtins' => array(),
            'product_asins' => array(),
            'product_identity_source' => '',
            'product_provider' => '',
        );
    }
    private function campaign_is_complete($campaign) {
        if (!is_array($campaign)) { return false; }
        $type = sanitize_key((string)($campaign['creative_type'] ?? 'banner'));
        $network = sanitize_key((string)($campaign['network'] ?? 'manual'));
        $mode = sanitize_key((string)($campaign['render_mode'] ?? 'image_link'));
        // DS24-Hardlock: Digistore24 is banner-only and may only leave the
        // shared campaign runtime through a validated Digistore tracking URL.
        // This covers manual, legacy and injected campaigns in addition to the
        // provider-specific output-object planner.
        if ($network === 'digistore24') {
            if ($type !== 'banner' || $mode !== 'image_link') { return false; }
            if (!$this->digistore24_tracking_url_allowed((string)($campaign['url'] ?? ''))) { return false; }
            if (!$this->digistore24_is_https_url((string)($campaign['image_url'] ?? ''))) { return false; }
        }
        $url_ok = trim((string)($campaign['url'] ?? '')) !== '' || ($mode === 'html' && trim((string)($campaign['html'] ?? '')) !== '');
        if ($mode === 'html') {
            $creative_ok = trim((string)($campaign['html'] ?? '')) !== '';
        } elseif ($type === 'product') {
            // V6.61.4: Produktkampagnen brauchen strukturell Titel + Bildquelle.
            // Die tatsaechliche aktuelle Bildfaehigkeit wird spaeter nach finaler
            // Rang-/Providerauswahl geprueft; defekte Kandidaten fallen dort heraus
            // und der naechste gerankte Kandidat rueckt nach.
            $creative_ok = trim((string)($campaign['title'] ?? '')) !== '' && trim((string)($campaign['image_url'] ?? '')) !== '';
        } else {
            $creative_ok = trim((string)($campaign['image_url'] ?? '')) !== '' || trim((string)($campaign['title'] ?? '')) !== '';
        }
        $placements_ok = !empty($campaign['placements']) && is_array($campaign['placements']);
        $assign_mode = sanitize_key((string)($campaign['assignment_mode'] ?? 'page_tree'));
        if ($assign_mode === 'fallback') { $assignment_ok = true; }
        elseif ($assign_mode === 'keywords') { $assignment_ok = !empty($campaign['match_keywords']); }
        elseif ($assign_mode === 'exact_page') { $assignment_ok = !empty($campaign['page_id']); }
        elseif ($assign_mode === 'auto_topic') { $assignment_ok = !empty($campaign['page_id']) && !empty($campaign['auto_topic_label']); }
        elseif ($assign_mode === 'page_tree') { $assignment_ok = !empty($campaign['page_id']) || !empty($campaign['match_slugs']) || !empty($campaign['match_term_ids']) || !empty($campaign['automation_target_keys']); }
        else { $assignment_ok = false; }
        $start = trim((string)($campaign['start_date'] ?? ''));
        $end = trim((string)($campaign['end_date'] ?? ''));
        return $url_ok && $creative_ok && $placements_ok && $assignment_ok && !($start !== '' && $end !== '' && $start > $end);
    }

    /**
     * V2.4.2: Generische, konservative Themenzuordnung ohne 1000er-Dropdown.
     * Die Profile entstehen aus den realen Hub-1-Seiten und deren veroeffentlichten
     * Unterseiten. Es wird nur automatisch zugeordnet, wenn genau ein Profil mit
     * ausreichendem Abstand gewinnt. Mehrdeutige oder schwache Treffer bleiben
     * fail-closed und werden nicht oeffentlich aktiviert.
     */
    private function auto_topic_stopwords() {
        return array(
            'aber','alle','alles','auch','auf','aus','bei','das','dein','deine','deiner','dem','den','der','des','die','dies','diese','dieser','ein','eine','einer','eines','fuer','für','hier','ihre','ihren','im','in','ist','mit','nach','oder','ohne','partner','produkt','produkte','shop','online','angebot','angebote','banner','werbung','werbemittel','und','unsere','unser','von','vor','zur','zum'
        );
    }

    private function auto_topic_tokens($text) {
        $text = function_exists('remove_accents') ? remove_accents((string)$text) : (string)$text;
        $text = strtolower($text);
        $text = preg_replace('/[^a-z0-9]+/u', ' ', $text);
        $parts = preg_split('/\s+/', trim((string)$text));
        $stop = array_fill_keys($this->auto_topic_stopwords(), true);
        $out = array();
        foreach ((array)$parts as $part) {
            $part = sanitize_key((string)$part);
            if ($part === '' || strlen($part) < 4 || isset($stop[$part])) { continue; }
            $out[$part] = true;
        }
        return array_keys($out);
    }

    private function auto_topic_profiles() {
        $groups = $this->central_hub_pages();
        $profiles = array();
        foreach ((array)($groups['hub1'] ?? array()) as $hub) {
            if (!$hub instanceof WP_Post) { continue; }
            $texts = array((string)$hub->post_title, (string)$hub->post_name);
            $children = get_pages(array(
                'child_of' => (int)$hub->ID,
                'post_status' => 'publish',
                'sort_column' => 'menu_order,post_title',
                'sort_order' => 'ASC',
            ));
            foreach ((array)$children as $child) {
                if (!$child instanceof WP_Post) { continue; }
                $texts[] = (string)$child->post_title;
                $texts[] = (string)$child->post_name;
            }
            $profiles[] = array(
                'page_id' => (int)$hub->ID,
                'label' => (string)$hub->post_title,
                'tokens' => $this->auto_topic_tokens(implode(' ', $texts)),
            );
        }
        return $profiles;
    }

    private function auto_topic_campaign_text($campaign) {
        $parts = array(
            (string)($campaign['name'] ?? ''),
            (string)($campaign['partner'] ?? ''),
            (string)($campaign['title'] ?? ''),
            (string)($campaign['description'] ?? ''),
            (string)($campaign['url'] ?? ''),
            implode(' ', (array)($campaign['match_keywords'] ?? array())),
        );
        return implode(' ', $parts);
    }

    private function auto_topic_score($source_tokens, $profile_tokens) {
        $score = 0;
        $hits = array();
        foreach ((array)$source_tokens as $source) {
            foreach ((array)$profile_tokens as $profile) {
                if ($source === $profile) {
                    $score += 4;
                    $hits[$source] = true;
                    break;
                }
                $min = min(strlen($source), strlen($profile));
                if ($min >= 5 && (strpos($source, $profile) === 0 || strpos($profile, $source) === 0)) {
                    $score += 2;
                    $hits[$source . '~' . $profile] = true;
                    break;
                }
            }
        }
        return array('score'=>$score,'hits'=>array_keys($hits));
    }

    private function auto_assign_campaign_topic($campaign) {
        $source_tokens = $this->auto_topic_tokens($this->auto_topic_campaign_text($campaign));
        $ranked = array();
        foreach ($this->auto_topic_profiles() as $profile) {
            $result = $this->auto_topic_score($source_tokens, $profile['tokens']);
            if ($result['score'] <= 0) { continue; }
            $ranked[] = array_merge($profile, $result);
        }
        usort($ranked, function($a,$b){
            if ((int)$a['score'] !== (int)$b['score']) { return (int)$a['score'] > (int)$b['score'] ? -1 : 1; }
            return strcmp((string)$a['label'], (string)$b['label']);
        });
        $best = $ranked[0] ?? null;
        $second = $ranked[1] ?? null;
        if (!$best || (int)$best['score'] < 6 || ($second && ((int)$best['score'] - (int)$second['score']) < 3)) {
            return array(
                'page_id'=>0,
                'label'=>'',
                'score'=>$best ? (int)$best['score'] : 0,
                'reason'=>$best ? 'Mehrdeutiger oder zu schwacher Themenvorschlag; keine automatische Ausspielung.' : 'Kein belastbarer Themenbezug erkannt; keine automatische Ausspielung.',
            );
        }
        return array(
            'page_id'=>(int)$best['page_id'],
            'label'=>(string)$best['label'],
            'score'=>(int)$best['score'],
            'reason'=>'Eindeutiger Treffer im realen Portalbaum: ' . implode(', ', array_slice((array)$best['hits'],0,5)) . '.',
        );
    }

    private function sanitize_campaign_rows($rows, &$blocked_count) {
        $blocked_count = 0;
        if (!is_array($rows)) {
            return array();
        }
        $allowed_modes = array('auto_topic', 'page_tree', 'exact_page', 'keywords', 'fallback');
        $allowed_placements = array_keys($this->central_placement_options());
        $out = array();
        $used_ids = array();

        foreach ($rows as $row) {
            if (!is_array($row) || !empty($row['delete'])) {
                continue;
            }
            $name = isset($row['name']) ? sanitize_text_field(wp_unslash($row['name'])) : '';
            $title = isset($row['title']) ? sanitize_text_field(wp_unslash($row['title'])) : '';
            $url = isset($row['url']) ? esc_url_raw(trim((string) wp_unslash($row['url']))) : '';
            $image_url = isset($row['image_url']) ? esc_url_raw(trim((string) wp_unslash($row['image_url']))) : '';
            $page_id = isset($row['page_id']) ? absint($row['page_id']) : 0;
            $keywords = $this->admin_list_to_array(isset($row['match_keywords']) ? wp_unslash($row['match_keywords']) : '', false);
            $slugs = $this->admin_list_to_array(isset($row['match_slugs']) ? wp_unslash($row['match_slugs']) : '', true);
            $term_ids = isset($row['match_term_ids']) ? array_values(array_filter(array_map('absint', (array) wp_unslash($row['match_term_ids'])))) : array();

            // Vollständig leere neue Zeile ignorieren.
            if ($name === '' && $title === '' && $url === '' && $image_url === '' && $page_id === 0 && empty($keywords) && empty($slugs) && empty($term_ids)) {
                continue;
            }

            $raw_id = isset($row['id']) ? sanitize_key(wp_unslash($row['id'])) : '';
            $id = $raw_id !== '' ? $raw_id : sanitize_key($name !== '' ? $name : $title);
            if ($id === '') {
                $id = 'kampagne_' . (count($out) + 1);
            }
            $base_id = $id;
            $suffix = 2;
            while (isset($used_ids[$id])) {
                $id = $base_id . '_' . $suffix;
                $suffix++;
            }
            $used_ids[$id] = true;

            $mode = isset($row['assignment_mode']) ? sanitize_key(wp_unslash($row['assignment_mode'])) : 'page_tree';
            if (!in_array($mode, $allowed_modes, true)) {
                $mode = 'page_tree';
            }
            $placements = isset($row['placements']) && is_array($row['placements']) ? array_map('sanitize_key', wp_unslash($row['placements'])) : array();
            $placements = array_values(array_intersect($placements, $allowed_placements));
            $posted_type = isset($row['creative_type']) && sanitize_key(wp_unslash($row['creative_type'])) === 'product' ? 'product' : 'banner';
            if (empty($placements)) {
                $placements = $posted_type === 'product' ? array('category_product') : array('product_after_category_tiles');
            }
            $priority = isset($row['priority']) ? max(0, min(1000, (int) $row['priority'])) : 50;
            $start_date = isset($row['start_date']) && preg_match('/^\d{4}-\d{2}-\d{2}$/', (string) $row['start_date']) ? (string) $row['start_date'] : '';
            $end_date = isset($row['end_date']) && preg_match('/^\d{4}-\d{2}-\d{2}$/', (string) $row['end_date']) ? (string) $row['end_date'] : '';

            $campaign_network = isset($row['network']) ? sanitize_key(wp_unslash($row['network'])) : 'manual';
            if (!$this->provider_exists($campaign_network)) { $campaign_network = 'manual'; }

            $campaign = array(
                'id' => $id,
                'name' => $name !== '' ? $name : ($title !== '' ? $title : $id),
                'partner' => isset($row['partner']) ? sanitize_text_field(wp_unslash($row['partner'])) : '',
                'creative_type' => isset($row['creative_type']) && sanitize_key(wp_unslash($row['creative_type'])) === 'product' ? 'product' : 'banner',
                'network' => $campaign_network,
                'advertiser_id' => isset($row['advertiser_id']) ? sanitize_text_field(wp_unslash($row['advertiser_id'])) : '',
                'programme_name' => isset($row['programme_name']) ? sanitize_text_field(wp_unslash($row['programme_name'])) : '',
                'programme_status' => isset($row['programme_status']) && in_array(sanitize_key(wp_unslash($row['programme_status'])), array('unknown','active','paused','ended'), true) ? sanitize_key(wp_unslash($row['programme_status'])) : 'unknown',
                'programme_status_source' => isset($row['programme_status_source']) ? sanitize_text_field(wp_unslash($row['programme_status_source'])) : '',
                'programme_status_checked_at' => isset($row['programme_status_checked_at']) ? absint($row['programme_status_checked_at']) : 0,
                'quality_manual_status' => isset($row['quality_manual_status']) && in_array(sanitize_key(wp_unslash($row['quality_manual_status'])), array('unknown','approved','rejected'), true) ? sanitize_key(wp_unslash($row['quality_manual_status'])) : 'unknown',
                'quality_note' => isset($row['quality_note']) ? sanitize_textarea_field(wp_unslash($row['quality_note'])) : '',
                'render_mode' => isset($row['render_mode']) && sanitize_key(wp_unslash($row['render_mode'])) === 'html' ? 'html' : 'image_link',
                'html' => isset($row['html']) ? $this->filter_allowed_banner_html(wp_unslash($row['html'])) : '',
                'price' => isset($row['price']) ? sanitize_text_field(wp_unslash($row['price'])) : '',
                'currency' => isset($row['currency']) ? strtoupper(substr(sanitize_text_field(wp_unslash($row['currency'])),0,3)) : 'EUR',
                'availability' => isset($row['availability']) ? sanitize_text_field(wp_unslash($row['availability'])) : '',
                'dimensions' => isset($row['dimensions']) ? sanitize_text_field(wp_unslash($row['dimensions'])) : '',
                'last_synced' => isset($row['last_synced']) ? absint($row['last_synced']) : 0,
                'active' => !empty($row['active']),
                'assignment_mode' => $mode,
                'page_id' => $page_id,
                'auto_topic_label' => isset($row['auto_topic_label']) ? sanitize_text_field(wp_unslash($row['auto_topic_label'])) : '',
                'auto_topic_score' => isset($row['auto_topic_score']) ? absint($row['auto_topic_score']) : 0,
                'auto_topic_reason' => isset($row['auto_topic_reason']) ? sanitize_text_field(wp_unslash($row['auto_topic_reason'])) : '',
                'match_descendants' => !empty($row['match_descendants']),
                'match_slugs' => $slugs,
                'match_keywords' => $keywords,
                'match_term_ids' => $term_ids,
                'priority' => $priority,
                'start_date' => $start_date,
                'end_date' => $end_date,
                'placements' => $placements,
                'label' => isset($row['label']) ? sanitize_text_field(wp_unslash($row['label'])) : 'Anzeige',
                'title' => $title,
                'description' => isset($row['description']) ? sanitize_textarea_field(wp_unslash($row['description'])) : '',
                'button_text' => isset($row['button_text']) ? sanitize_text_field(wp_unslash($row['button_text'])) : 'Mehr erfahren',
                'image_url' => $image_url,
                'url' => $url,
                'target' => isset($row['target']) && wp_unslash($row['target']) === '_self' ? '_self' : '_blank',
                'subid_param' => isset($row['subid_param']) ? sanitize_key(wp_unslash($row['subid_param'])) : '',
                'required_url_fragment' => isset($row['required_url_fragment']) ? sanitize_text_field(wp_unslash($row['required_url_fragment'])) : '',
                'allowed_domains' => array_values(array_filter(array_map(function($domain){ $domain=strtolower(trim((string)$domain)); $domain=preg_replace('#^https?://#','',$domain); $domain=explode('/', $domain)[0]; return preg_replace('/[^a-z0-9.\-]/','',$domain); }, $this->admin_list_to_array(isset($row['allowed_domains']) ? wp_unslash($row['allowed_domains']) : '', false)))),
                'health_check_enabled' => array_key_exists('health_check_enabled', $row) ? !empty($row['health_check_enabled']) : true,
                'source' => isset($row['source']) ? sanitize_key(wp_unslash($row['source'])) : 'manual',
                'external_id' => isset($row['external_id']) ? sanitize_text_field(wp_unslash($row['external_id'])) : '',
            );
            if ($campaign['programme_status'] !== 'unknown' && $campaign['programme_status_source'] !== '') {
                $campaign['programme_status_checked_at'] = time();
            }

            if ($campaign['assignment_mode'] === 'auto_topic') {
                $auto = $this->auto_assign_campaign_topic($campaign);
                $campaign['page_id'] = absint($auto['page_id'] ?? 0);
                $campaign['auto_topic_label'] = sanitize_text_field((string)($auto['label'] ?? ''));
                $campaign['auto_topic_score'] = absint($auto['score'] ?? 0);
                $campaign['auto_topic_reason'] = sanitize_text_field((string)($auto['reason'] ?? ''));
                $campaign['match_descendants'] = true;
            }

            if ($campaign['active'] && !$this->campaign_is_complete($campaign)) {
                $campaign['active'] = false;
                $blocked_count++;
            }
            $out[] = $campaign;
        }
        return $out;
    }

    public function handle_save_campaigns() {
        if (!current_user_can('manage_options')) {
            wp_die('Keine Berechtigung.');
        }
        check_admin_referer('ppar_save_campaigns', 'ppar_campaigns_nonce');
        $rows = isset($_POST['ppar_campaigns']) && is_array($_POST['ppar_campaigns']) ? $_POST['ppar_campaigns'] : array();
        $blocked = 0;
        $campaigns = $this->sanitize_campaign_rows($rows, $blocked);
        update_option(self::OPTION_CAMPAIGNS, $campaigns, false);
        update_option(self::OPTION_CAMPAIGNS_MIGRATED, '1', false);
        update_option(self::OPTION_ENABLED, !empty($_POST['ppar_enabled']) ? '1' : '0', false);
        update_option(self::OPTION_DISCLOSURE, isset($_POST['ppar_disclosure']) ? sanitize_textarea_field(wp_unslash($_POST['ppar_disclosure'])) : '', false);
        $this->article_plan_bump_campaign_revision('campaigns_saved');

        $args = array('page' => 'affiliate-portal-zentrale', 'ppar_campaigns_saved' => '1');
        if ($blocked > 0) {
            $args['ppar_campaigns_blocked'] = $blocked;
        }
        wp_safe_redirect(add_query_arg($args, admin_url('admin.php')));
        exit;
    }

    public function handle_save_central_settings() {
        if (!current_user_can('manage_options')) {
            wp_die('Keine Berechtigung.');
        }
        check_admin_referer('ppar_save_central_settings', 'ppar_settings_nonce');
        update_option(self::OPTION_ENABLED, !empty($_POST['ppar_enabled']) ? '1' : '0', false);
        update_option(self::OPTION_DISCLOSURE, isset($_POST['ppar_disclosure']) ? sanitize_textarea_field(wp_unslash($_POST['ppar_disclosure'])) : '', false);
        wp_safe_redirect(add_query_arg(array('page' => 'affiliate-portal-zentrale', 'ppar_settings_saved' => '1'), admin_url('admin.php')));
        exit;
    }

    public function handle_save_placeholder_settings() {
        if (!current_user_can('manage_options')) {
            wp_die('Keine Berechtigung.');
        }
        check_admin_referer('ppar_save_placeholder_settings', 'ppar_placeholder_nonce');
        $raw = isset($_POST['ppar_placeholder']) && is_array($_POST['ppar_placeholder']) ? wp_unslash($_POST['ppar_placeholder']) : array();
        $old_settings = $this->get_placeholder_settings();
        $settings = $this->sanitize_placeholder_settings($raw);

        // V2.2.17: Startbild A/B sind die einzigen gepflegten Bildquellen.
        // Historische Felder werden nur synchron gehalten, damit alter Fremdcode
        // ebenfalls das neue Bild sieht und nicht auf eine alte ID zurueckfaellt.
        $image_a_id = absint($settings['start_image_id'] ?? 0);
        $image_b_id = absint($settings['start_image_b_id'] ?? 0);
        $image_a_url = $this->placeholder_attachment_url($settings, 'start_image_id');
        $image_b_url = $this->placeholder_attachment_url($settings, 'start_image_b_id');
        foreach (array('hub_image_id', 'category_grid_image_id', 'category_image_id') as $key) { $settings[$key] = $image_a_id; }
        foreach (array('hub_image_b_id', 'category_grid_image_b_id') as $key) { $settings[$key] = $image_b_id; }
        foreach (array('hub_image_url', 'category_grid_image_url', 'category_image_url') as $key) { $settings[$key] = $image_a_url; }
        foreach (array('hub_image_b_url', 'category_grid_image_b_url') as $key) { $settings[$key] = $image_b_url; }
        $settings['revision'] = (string)time() . '-' . (function_exists('wp_rand') ? (string)wp_rand(1000, 9999) : (string)mt_rand(1000, 9999));
        update_option(self::OPTION_PLACEHOLDER_SETTINGS, $settings, false);
        if (function_exists('wp_cache_delete')) { wp_cache_delete(self::OPTION_PLACEHOLDER_SETTINGS, 'options'); }
        $this->purge_placeholder_frontend_caches();
        wp_safe_redirect(add_query_arg(array('page' => 'affiliate-portal-zentrale', 'ppar_placeholders_saved' => '1'), admin_url('admin.php')));
        exit;
    }

    public function handle_save_campaign() {
        if (!current_user_can('manage_options')) {
            wp_die('Keine Berechtigung.');
        }
        check_admin_referer('ppar_save_campaign', 'ppar_campaign_nonce');
        $post_id = isset($_POST['campaign_post_id']) ? absint($_POST['campaign_post_id']) : 0;
        $row = isset($_POST['ppar_campaign']) && is_array($_POST['ppar_campaign']) ? $_POST['ppar_campaign'] : array();
        $blocked = 0;
        $sanitized = $this->sanitize_campaign_rows(array($row), $blocked);
        if (empty($sanitized[0])) {
            wp_safe_redirect(add_query_arg(array('page' => 'affiliate-portal-campaign-edit', 'campaign_id' => $post_id, 'ppar_campaign_error' => 'empty'), admin_url('admin.php')));
            exit;
        }
        $campaign = $sanitized[0];
        if ($post_id > 0) {
            $existing = $this->campaign_from_post(get_post($post_id));
            if ($existing && !empty($existing['id'])) {
                $campaign['id'] = $existing['id'];
            }
        }
        $saved_id = $this->save_campaign_record($campaign, $post_id);
        if (!empty($campaign['active'])) {
            update_option(self::OPTION_ENABLED, '1', false);
        }
        if (!is_wp_error($saved_id) && $saved_id) {
            $this->article_plan_bump_campaign_revision('campaign_saved');
        }
        if (is_wp_error($saved_id) || !$saved_id) {
            wp_safe_redirect(add_query_arg(array('page' => 'affiliate-portal-campaign-edit', 'campaign_id' => $post_id, 'ppar_campaign_error' => 'save'), admin_url('admin.php')));
            exit;
        }
        $args = array('page' => 'affiliate-portal-creatives', 'ppar_campaign_saved' => '1');
        if ($blocked > 0) {
            $args['ppar_campaign_blocked'] = '1';
        }
        if (!empty($_POST['save_and_continue'])) {
            $args['page'] = 'affiliate-portal-campaign-edit';
            $args['campaign_id'] = (int) $saved_id;
        }
        wp_safe_redirect(add_query_arg($args, admin_url('admin.php')));
        exit;
    }

    public function handle_delete_campaign() {
        if (!current_user_can('manage_options')) {
            wp_die('Keine Berechtigung.');
        }
        $post_id = isset($_POST['campaign_post_id']) ? absint($_POST['campaign_post_id']) : 0;
        check_admin_referer('ppar_delete_campaign_' . $post_id, 'ppar_delete_nonce');
        if ($post_id > 0 && get_post_type($post_id) === self::CAMPAIGN_POST_TYPE) {
            wp_trash_post($post_id);
            $this->article_plan_bump_campaign_revision('campaign_deleted');
        }
        wp_safe_redirect(add_query_arg(array('page' => 'affiliate-portal-creatives', 'ppar_campaign_deleted' => '1'), admin_url('admin.php')));
        exit;
    }

    public function upsert_campaign_from_external($data) {
        if (!is_array($data)) {
            return new WP_Error('invalid_campaign', 'Kampagnendaten müssen als Array übergeben werden.');
        }
        $external_id = isset($data['external_id']) ? sanitize_text_field((string) $data['external_id']) : '';
        if ($external_id === '') {
            return new WP_Error('missing_external_id', 'Für automatische Importe ist eine externe ID erforderlich.');
        }
        $post_id = 0;
        foreach ($this->get_campaigns() as $existing) {
            if ((string) ($existing['external_id'] ?? '') === $external_id) {
                $post_id = (int) ($existing['post_id'] ?? 0);
                if (empty($data['id']) && !empty($existing['id'])) {
                    $data['id'] = $existing['id'];
                }
                break;
            }
        }
        if (empty($data['placements'])) {
            $data['placements'] = array('hub_grid_card');
        }
        $blocked = 0;
        $rows = $this->sanitize_campaign_rows(array($data), $blocked);
        if (empty($rows[0])) {
            return new WP_Error('empty_campaign', 'Die Kampagne enthält keine verwertbaren Daten.');
        }
        $saved_id = $this->save_campaign_record($rows[0], $post_id);
        if (is_wp_error($saved_id)) {
            return $saved_id;
        }
        return array('post_id' => (int) $saved_id, 'active' => !empty($rows[0]['active']), 'blocked' => $blocked > 0);
    }

    private function render_campaign_editor($campaign, $index, $is_new = false) {
        $campaign = wp_parse_args(is_array($campaign) ? $campaign : array(), $this->central_blank_campaign());
        $complete = $this->campaign_is_complete($campaign);
        $open = $is_new || !empty($_GET['ppar_open_campaign']) && sanitize_key((string) $_GET['ppar_open_campaign']) === sanitize_key((string) $campaign['id']);
        $title = $is_new ? 'Neue Kampagne anlegen' : (string) $campaign['name'];
        $status = !empty($campaign['active']) && $complete ? 'Aktiv' : ($complete ? 'Bereit, aber inaktiv' : 'Unvollständig');
        $status_class = !empty($campaign['active']) && $complete ? 'ppar-ok' : ($complete ? 'ppar-neutral' : 'ppar-warn');
        $prefix = 'ppar_campaigns[' . (int) $index . ']';
        ?>
        <details class="ppar-campaign" <?php echo $open ? 'open' : ''; ?>>
            <summary><strong><?php echo esc_html($title); ?></strong><span class="ppar-status <?php echo esc_attr($status_class); ?>"><?php echo esc_html($status); ?></span></summary>
            <div class="ppar-campaign-body">
                <input type="hidden" name="<?php echo esc_attr($prefix); ?>[id]" value="<?php echo esc_attr((string) $campaign['id']); ?>">
                <input type="hidden" name="<?php echo esc_attr($prefix); ?>[source]" value="<?php echo esc_attr((string) $campaign['source']); ?>">

                <h3>1. Angebot</h3>
                <div class="ppar-grid">
                    <label><span>Interner Name</span><input type="text" name="<?php echo esc_attr($prefix); ?>[name]" value="<?php echo esc_attr((string) $campaign['name']); ?>" placeholder="z. B. Regendecken Sommeraktion"></label>
                    <label><span>Kennzeichnung</span><input type="text" name="<?php echo esc_attr($prefix); ?>[label]" value="<?php echo esc_attr((string) $campaign['label']); ?>" placeholder="Anzeige"></label>
                    <label class="ppar-wide"><span>Titel der Werbekachel</span><input type="text" name="<?php echo esc_attr($prefix); ?>[title]" value="<?php echo esc_attr((string) $campaign['title']); ?>" placeholder="Passende Produkte entdecken"></label>
                    <label class="ppar-wide"><span>Kurztext (optional)</span><textarea name="<?php echo esc_attr($prefix); ?>[description]" rows="2"><?php echo esc_textarea((string) $campaign['description']); ?></textarea></label>
                    <label class="ppar-wide"><span>Affiliate-/Ziel-URL</span><input type="url" name="<?php echo esc_attr($prefix); ?>[url]" value="<?php echo esc_attr((string) $campaign['url']); ?>" placeholder="https://..."></label>
                    <label><span>Bild (optional)</span><input class="ppar-image-url" type="url" name="<?php echo esc_attr($prefix); ?>[image_url]" value="<?php echo esc_attr((string) $campaign['image_url']); ?>" placeholder="https://..."><button type="button" class="button ppar-select-image">Aus Mediathek wählen</button></label>
                    <label><span>Linktext</span><input type="text" name="<?php echo esc_attr($prefix); ?>[button_text]" value="<?php echo esc_attr((string) $campaign['button_text']); ?>"></label>
                </div>

                <h3>2. Automatische Zuordnung</h3>
                <div class="ppar-grid">
                    <label><span>Zuordnung</span><select name="<?php echo esc_attr($prefix); ?>[assignment_mode]">
                        <option value="page_tree" <?php selected($campaign['assignment_mode'], 'page_tree'); ?>>Bereich/Hub und alle Unterseiten</option>
                        <option value="keywords" <?php selected($campaign['assignment_mode'], 'keywords'); ?>>Automatisch nach Themenbegriffen</option>
                        <option value="fallback" <?php selected($campaign['assignment_mode'], 'fallback'); ?>>Allgemeiner Fallback</option>
                    </select></label>
                    <label><span>Bereich oder Hub</span><?php
                        wp_dropdown_pages(array(
                            'name' => $prefix . '[page_id]',
                            'id' => 'ppar-page-' . (int) $index,
                            'selected' => (int) $campaign['page_id'],
                            'show_option_none' => 'Bereich/Hub auswählen',
                            'option_none_value' => '0',
                            'sort_column' => 'menu_order,post_title',
                        ));
                    ?></label>
                    <label class="ppar-wide"><span>Themenbegriffe (optional; einer pro Zeile)</span><textarea name="<?php echo esc_attr($prefix); ?>[match_keywords]" rows="3" placeholder="regendecke&#10;pferdedecke"><?php echo esc_textarea($this->array_to_admin_list($campaign['match_keywords'])); ?></textarea></label>
                </div>
                <input type="hidden" name="<?php echo esc_attr($prefix); ?>[match_descendants]" value="1">
                <p class="description">Beim Modus „Bereich/Hub und alle Unterseiten“ wird die gewählte Seite einmal zugeordnet; alle darunterliegenden Seiten werden automatisch mit erfasst.</p>

                <h3>3. Veröffentlichung</h3>
                <div class="ppar-grid">
                    <label><span>Priorität</span><input type="number" min="0" max="1000" name="<?php echo esc_attr($prefix); ?>[priority]" value="<?php echo esc_attr((string) $campaign['priority']); ?>"><small>Höher gewinnt, wenn mehrere Kampagnen passen.</small></label>
                    <label><span>Linkziel</span><select name="<?php echo esc_attr($prefix); ?>[target]"><option value="_blank" <?php selected($campaign['target'], '_blank'); ?>>Neuer Tab</option><option value="_self" <?php selected($campaign['target'], '_self'); ?>>Gleiches Fenster</option></select></label>
                    <label><span>Startdatum (optional)</span><input type="date" name="<?php echo esc_attr($prefix); ?>[start_date]" value="<?php echo esc_attr((string) $campaign['start_date']); ?>"></label>
                    <label><span>Enddatum (optional)</span><input type="date" name="<?php echo esc_attr($prefix); ?>[end_date]" value="<?php echo esc_attr((string) $campaign['end_date']); ?>"></label>
                </div>
                <?php $placement_options = $this->central_placement_options(); ?>
                <fieldset class="ppar-placement"><legend>Ausgabeposition</legend>
                    <label><input type="checkbox" name="<?php echo esc_attr($prefix); ?>[placements][]" value="hub_grid_card" <?php checked(in_array('hub_grid_card', (array) $campaign['placements'], true)); ?>> <strong><?php echo esc_html($placement_options['hub_grid_card']); ?></strong></label>
                </fieldset>
                <details class="ppar-advanced"><summary>Weitere Ausgabepositionen</summary>
                    <div class="ppar-placement">
                    <?php foreach ($placement_options as $slot => $label) : if ($slot === 'hub_grid_card') { continue; } ?>
                        <label><input type="checkbox" name="<?php echo esc_attr($prefix); ?>[placements][]" value="<?php echo esc_attr($slot); ?>" <?php checked(in_array($slot, (array) $campaign['placements'], true)); ?>> <?php echo esc_html($label); ?></label>
                    <?php endforeach; ?>
                    </div>
                </details>

                <div class="ppar-activate">
                    <label><input type="checkbox" name="<?php echo esc_attr($prefix); ?>[active]" value="1" <?php checked(!empty($campaign['active'])); ?>> <strong>Kampagne aktivieren</strong></label>
                    <span>Aktivierung wird nur übernommen, wenn Link, Titel oder Bild, Zuordnung und Ausgabeposition vollständig sind.</span>
                </div>

                <details class="ppar-advanced"><summary>Erweiterte Import-/Kompatibilitätsfelder</summary>
                    <div class="ppar-grid">
                        <label class="ppar-wide"><span>Zusätzliche Seiten-Slugs</span><textarea name="<?php echo esc_attr($prefix); ?>[match_slugs]" rows="3"><?php echo esc_textarea($this->array_to_admin_list($campaign['match_slugs'])); ?></textarea></label>
                        <label><span>Externe ID</span><input type="text" name="<?php echo esc_attr($prefix); ?>[external_id]" value="<?php echo esc_attr((string) $campaign['external_id']); ?>"></label>
                        <label><span>SubID-Parameter</span><input type="text" name="<?php echo esc_attr($prefix); ?>[subid_param]" value="<?php echo esc_attr((string) $campaign['subid_param']); ?>"></label>
                    </div>
                </details>

                <?php if (!$is_new) : ?>
                    <label class="ppar-delete"><input type="checkbox" name="<?php echo esc_attr($prefix); ?>[delete]" value="1"> Kampagne beim Speichern löschen</label>
                <?php endif; ?>
            </div>
        </details>
        <?php
    }

    private function campaign_match_reason($group, $context) {
        $post_id = isset($context['post_id']) ? (int) $context['post_id'] : 0;
        $match_post_ids = isset($group['match_post_ids']) && is_array($group['match_post_ids']) ? array_map('intval', $group['match_post_ids']) : array();
        if ($post_id > 0 && in_array($post_id, $match_post_ids, true)) {
            return 'Die Seite ist direkt dem gewählten Bereich/Hub zugeordnet.';
        }
        $ancestors = isset($context['ancestor_ids']) && is_array($context['ancestor_ids']) ? array_map('intval', $context['ancestor_ids']) : array();
        if (!empty(array_intersect($match_post_ids, $ancestors))) {
            return 'Die Seite liegt unter dem zugeordneten Bereich/Hub und wird automatisch erfasst.';
        }
        foreach ((array) ($group['match_slugs'] ?? array()) as $slug) {
            if (in_array(sanitize_key((string) $slug), (array) ($context['slugs'] ?? array()), true)) {
                return 'Der Seiten- oder Bereichs-Slug passt.';
            }
        }
        foreach ((array) ($group['match_keywords'] ?? array()) as $keyword) {
            if ($keyword !== '' && strpos((string) ($context['haystack'] ?? ''), strtolower((string) $keyword)) !== false) {
                return 'Ein definierter Themenbegriff passt.';
            }
        }
        return (($group['match_mode'] ?? '') === 'fallback') ? 'Die Kampagne ist als allgemeiner Fallback eingestellt.' : 'Die Zuordnungsregel passt.';
    }

    private function render_central_test($post_id) {
        if ($post_id <= 0 || get_post_type($post_id) !== 'page') {
            return;
        }
        $context = $this->get_content_context($post_id);
        $selection = $this->select_campaign_for_slot($context, 'hub_grid_card');
        $campaign = $selection['campaign'] ?? null;
        $enabled = $this->is_enabled();
        $valid = $enabled && is_array($campaign) && $this->campaign_is_complete($campaign) && $this->rule_is_current($campaign);
        $page_url = get_permalink($post_id);
        echo '<div class="ppar-test-result ' . ($valid ? 'ppar-test-ok' : 'ppar-test-no') . '">';
        echo '<h3>' . esc_html(get_the_title($post_id)) . '</h3>';
        if (!$enabled) {
            echo '<p><strong>5 Kacheln:</strong> Die Affiliate-Automatik ist global deaktiviert.</p>';
        } elseif (!$campaign) {
            echo '<p><strong>5 Kacheln:</strong> Keine passende aktive Kampagne gefunden.</p>';
        } else {
            echo '<p><strong>5 + Banner:</strong> Kampagne „' . esc_html((string) ($campaign['name'] ?? $campaign['id'])) . '“ wird ausgewählt.</p>';
            echo '<p>' . esc_html((string) ($selection['reason'] ?? 'Passende Zuordnung.')) . '</p>';
            echo '<p><strong>Voraussetzung im Frontend:</strong> Die Hubseite besitzt genau fünf normale Kacheln.</p>';
        }
        if ($page_url) {
            echo '<p><a class="button" href="' . esc_url($page_url) . '" target="_blank" rel="noopener">Seite im Frontend öffnen</a></p>';
        }
        echo '</div>';
    }


    private function central_campaign_status($campaign) {
        $complete = $this->campaign_is_complete($campaign);
        if (!$complete) {
            return array('label' => 'Unvollständig', 'class' => 'ppar-warn');
        }
        if (empty($campaign['active'])) {
            return array('label' => 'Inaktiv', 'class' => 'ppar-neutral');
        }
        if (!$this->rule_is_current($campaign)) {
            $today = current_time('Y-m-d');
            $start = trim((string) ($campaign['start_date'] ?? ''));
            return ($start !== '' && $start > $today)
                ? array('label' => 'Geplant', 'class' => 'ppar-neutral')
                : array('label' => 'Abgelaufen', 'class' => 'ppar-warn');
        }
        return array('label' => 'Aktiv', 'class' => 'ppar-ok');
    }

    private function central_page_type($page_id) {
        $page_id = absint($page_id);
        if ($page_id <= 0) {
            return '';
        }
        if (class_exists('Pferde_Template_Kit') && method_exists('Pferde_Template_Kit', 'affiliate_page_type')) {
            return (string) Pferde_Template_Kit::affiliate_page_type($page_id);
        }
        $ancestors = get_post_ancestors($page_id);
        $children = get_pages(array('parent' => $page_id, 'post_status' => 'publish', 'number' => 1));
        $depth = count((array) $ancestors);
        if ($depth === 0 && !empty($children)) {
            return 'hub1';
        }
        if ($depth === 1 && !empty($children)) {
            return 'hub2';
        }
        return '';
    }

    private function central_hub_pages() {
        $front_id = (int) get_option('page_on_front', 0);
        $pages = get_pages(array('post_status' => 'publish', 'sort_column' => 'menu_order,post_title', 'sort_order' => 'ASC'));
        $out = array('hub1' => array(), 'hub2' => array());
        foreach ((array) $pages as $page) {
            if (!$page instanceof WP_Post || (int) $page->ID === $front_id) {
                continue;
            }
            $type = $this->central_page_type((int) $page->ID);
            if (!isset($out[$type])) {
                continue;
            }
            $out[$type][] = $page;
        }
        return $out;
    }

    private function render_hub_page_dropdown($name, $selected = 0, $none_label = 'Hubseite auswaehlen') {
        $groups = $this->central_hub_pages();
        echo '<select name="' . esc_attr($name) . '">';
        echo '<option value="0">' . esc_html($none_label) . '</option>';
        foreach (array('hub1' => 'Hub Ebene 1', 'hub2' => 'Hub Ebene 2') as $type => $label) {
            if (empty($groups[$type])) {
                continue;
            }
            echo '<optgroup label="' . esc_attr($label) . '">';
            foreach ($groups[$type] as $page) {
                echo '<option value="' . esc_attr((string) $page->ID) . '"' . selected((int) $selected, (int) $page->ID, false) . '>' . esc_html((string) $page->post_title) . '</option>';
            }
            echo '</optgroup>';
        }
        echo '</select>';
    }

    private function central_assignment_summary($campaign) {
        $mode = sanitize_key((string) ($campaign['assignment_mode'] ?? 'page_tree'));
        if ($mode === 'fallback') {
            return 'Allgemeiner Fallback';
        }
        if ($mode === 'keywords') {
            $keywords = array_values(array_filter((array) ($campaign['match_keywords'] ?? array())));
            return empty($keywords) ? 'Themenbegriffe fehlen' : 'Themen: ' . implode(', ', array_slice($keywords, 0, 3));
        }
        if ($mode === 'auto_topic') {
            $label = sanitize_text_field((string)($campaign['auto_topic_label'] ?? ''));
            return $label !== '' ? 'Automatisch: ' . $label . ' (Score ' . absint($campaign['auto_topic_score'] ?? 0) . ')' : 'Automatik: Prüfung nötig';
        }
        $page_id = (int) ($campaign['page_id'] ?? 0);
        $title = $page_id > 0 ? get_the_title($page_id) : '';
        if ($title === '') {
            return 'Bereich/Seite fehlt';
        }
        return $mode === 'exact_page' ? 'Nur: ' . $title : $title . ' + Unterseiten';
    }

    public function render_central_page() {
        if (!current_user_can('manage_options')) {
            wp_die('Keine Berechtigung.');
        }
        $campaigns = $this->get_campaigns();
        $enabled = $this->is_enabled();
        $active_count = 0;
        foreach ($campaigns as $campaign) {
            if (!empty($campaign['active']) && $this->campaign_is_complete($campaign) && $this->rule_is_current($campaign)) {
                $active_count++;
            }
        }
        $design_loaded = class_exists('Pferde_Template_Kit');
        $design_version = $design_loaded && defined('Pferde_Template_Kit::VERSION') ? constant('Pferde_Template_Kit::VERSION') : '';
        $design_contract = $design_loaded && method_exists('Pferde_Template_Kit', 'affiliate_contract_version') ? (string) Pferde_Template_Kit::affiliate_contract_version() : '';
        $compatible = $design_loaded && $design_contract === self::CONTRACT_VERSION;
        $test_page_id = isset($_GET['ppar_test_page_id']) ? absint($_GET['ppar_test_page_id']) : 0;
        ?>
        <div class="wrap ppar-central">
            <style>
                .ppar-central{max-width:1180px}.ppar-top{display:grid;grid-template-columns:2fr 1fr;gap:16px;margin:16px 0}.ppar-box{background:#fff;border:1px solid #c3c4c7;border-radius:8px;padding:18px}.ppar-box h2{margin-top:0}.ppar-actions{display:flex;gap:10px;align-items:center;flex-wrap:wrap}.ppar-status{display:inline-block;font-size:12px;border-radius:999px;padding:4px 9px;font-weight:600}.ppar-ok{background:#dff5e1;color:#006b1b}.ppar-warn{background:#fff1d2;color:#8a5100}.ppar-neutral{background:#e8f0f7;color:#135e96}.ppar-table td{vertical-align:middle}.ppar-test-result{padding:16px;border-radius:8px;margin-top:14px}.ppar-test-ok{background:#edfaef;border:1px solid #88c999}.ppar-test-no{background:#fff8e5;border:1px solid #dba617}@media(max-width:782px){.ppar-top{grid-template-columns:1fr}.ppar-table thead{display:none}.ppar-table tr,.ppar-table td{display:block}.ppar-table tr{padding:10px 0}}
            </style>
            <h1>Affiliate-Zentrale</h1>
            <p><strong>Ein zentraler Ablauf:</strong> Kampagne anlegen -> Hub zuordnen -> aktivieren -> automatisch ausspielen -> Klicks hier sehen.</p>
            <p><a class="button button-primary" href="<?php echo esc_url(admin_url('admin.php?page=affiliate-portal-networks')); ?>">Provider verbinden</a></p>

            <div class="ppar-top">
                <div class="ppar-box">
                    <h2>Systemstatus</h2>
                    <p><strong>Affiliate-Automatik:</strong> <?php echo $enabled ? '<span class="ppar-status ppar-ok">Aktiv</span>' : '<span class="ppar-status ppar-neutral">Inaktiv</span>'; ?></p>
                    <p><strong>Designplugin:</strong> <?php
                        if ($compatible) {
                            echo '<span class="ppar-status ppar-ok">Verbunden</span> Version ' . esc_html($design_version);
                        } elseif ($design_loaded) {
                            echo '<span class="ppar-status ppar-warn">Nicht kompatibel</span>';
                        } else {
                            echo '<span class="ppar-status ppar-warn">Nicht erkannt</span>';
                        }
                    ?></p>
                    <p><strong>Kampagnen:</strong> <?php echo esc_html((string) $active_count); ?> aktiv / <?php echo esc_html((string) count($campaigns)); ?> insgesamt</p><p><strong>Klickmessung:</strong> Aktiv, ohne Speicherung von IP-Adresse oder Browserdaten.</p>
                </div>
                <div class="ppar-box">
                    <h2>Hauptschalter</h2>
                    <form method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>">
                        <input type="hidden" name="action" value="ppar_save_central_settings">
                        <?php wp_nonce_field('ppar_save_central_settings', 'ppar_settings_nonce'); ?>
                        <p><label><input type="checkbox" name="ppar_enabled" value="1" <?php checked($enabled); ?>> <strong>Affiliate-Automatik aktiv</strong></label></p>
                        <details><summary>Affiliate-Hinweis für Beiträge</summary><textarea name="ppar_disclosure" rows="3" class="large-text"><?php echo esc_textarea((string) get_option(self::OPTION_DISCLOSURE, '')); ?></textarea></details>
                        <?php submit_button('Einstellung speichern', 'secondary', 'submit', false); ?>
                    </form>
                </div>
            </div>

            <?php $placeholder = $this->get_placeholder_settings(); ?>
            <div class="ppar-box" style="margin:20px 0;">
                <h2>Werbeplatz-Platzhalter</h2>
                <p><strong>Reihenfolge:</strong> Echte passende Kampagne zuerst. Nur wenn keine Kampagne passt, erscheint das hier hinterlegte Platzhalterbild.</p>
                <form method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>">
                    <input type="hidden" name="action" value="ppar_save_placeholder_settings">
                    <?php wp_nonce_field('ppar_save_placeholder_settings', 'ppar_placeholder_nonce'); ?>
                    <table class="form-table" role="presentation"><tbody>
                        <tr><th scope="row">Platzhalter verwenden</th><td><label><input type="checkbox" name="ppar_placeholder[enabled]" value="1" <?php checked(!empty($placeholder['enabled'])); ?>> Aktiv</label><p class="description">Ohne ausgewähltes Bild bleibt der jeweilige Platz unsichtbar.</p></td></tr>
                        <tr><th scope="row">Ausgabe</th><td><strong>Nur das Bild.</strong><p class="description">Platzhalter zeigen niemals Kennzeichnung, Überschrift, Kurztext oder Button. Beim Speichern wird die Bildversion erneuert und der Frontend-Cache geleert.</p></td></tr>
                        <tr><th scope="row">Ziel-URL</th><td><input type="url" class="large-text" name="ppar_placeholder[url]" value="<?php echo esc_attr((string) $placeholder['url']); ?>" placeholder="https://.../werben/"><p class="description">Optional. Ohne Ziel-URL bleibt das Bild sichtbar, ist aber nicht anklickbar.</p></td></tr>
                        <tr><th scope="row">Linkziel</th><td><select name="ppar_placeholder[target]"><option value="_self" <?php selected($placeholder['target'], '_self'); ?>>gleiches Fenster</option><option value="_blank" <?php selected($placeholder['target'], '_blank'); ?>>neuer Tab</option></select></td></tr>
                        <?php $this->render_placeholder_image_field('start_image_id', 'Zentrale Partner-Vorschau A', 'Dieses Bild gilt auf Startseite, Hub 1, Hub 2 und Ebene 3.', $placeholder); ?>
                        <?php $this->render_placeholder_image_field('start_image_b_id', 'Zentrale Partner-Vorschau B', 'Optionales zweites Bild für zwei Partnerplätze. Ohne B erscheint nur A.', $placeholder); ?>
                        <tr><th scope="row">Startseite</th><td><label><input type="checkbox" name="ppar_placeholder[start_enabled]" value="1" <?php checked(!empty($placeholder['start_enabled'])); ?>> kleinere Partnerflächen nach „Ausgewählte Themen“ aktiv</label></td></tr>
                        <tr><th scope="row">Hub Ebene 1</th><td><label><input type="checkbox" name="ppar_placeholder[hub1_enabled]" value="1" <?php checked(!empty($placeholder['hub1_enabled'])); ?>> Partner-Vorschauen im Kachelraster aktiv</label></td></tr>
                        <tr><th scope="row">Hub Ebene 2</th><td><label><input type="checkbox" name="ppar_placeholder[hub2_enabled]" value="1" <?php checked(!empty($placeholder['hub2_enabled'])); ?>> Partner-Vorschauen im Kachelraster aktiv</label></td></tr>
                        <tr><th scope="row">Ebene 3</th><td><label><input type="checkbox" name="ppar_placeholder[category_enabled]" value="1" <?php checked(!empty($placeholder['category_enabled'])); ?>> Partner-Vorschauen im Kachelraster aktiv</label></td></tr>
                    </tbody></table>
                    <?php submit_button('Werbeplatz-Platzhalter speichern', 'secondary'); ?>
                </form>
            </div>

            <div class="ppar-actions" style="margin:22px 0 12px;">
                <a class="button button-primary button-hero" href="<?php echo esc_url(admin_url('admin.php?page=affiliate-portal-campaign-edit')); ?>">Neue Kampagne</a>
                <span>Banner, Link, Zuordnung und Veröffentlichung werden ausschließlich hier gepflegt.</span>
            </div>

            <h2>Kampagnen</h2>
            <?php if (empty($campaigns)) : ?>
                <div class="ppar-box"><p>Noch keine Kampagne vorhanden.</p></div>
            <?php else : ?>
                <table class="widefat striped ppar-table">
                    <thead><tr><th>Kampagne</th><th>Status</th><th>Zuordnung</th><th>Klicks</th><th>Laufzeit</th><th></th></tr></thead>
                    <tbody>
                    <?php foreach ($campaigns as $campaign) : $status = $this->central_campaign_status($campaign); ?>
                        <tr>
                            <td><strong><?php echo esc_html((string) ($campaign['name'] ?? 'Kampagne')); ?></strong><br><span class="description"><?php echo esc_html((string) ($campaign['title'] ?? '')); ?></span></td>
                            <td><span class="ppar-status <?php echo esc_attr($status['class']); ?>"><?php echo esc_html($status['label']); ?></span></td>
                            <td><?php echo esc_html($this->central_assignment_summary($campaign)); ?></td>
                            <td><strong><?php echo esc_html((string) $this->campaign_click_total($campaign)); ?></strong> gesamt<br><span class="description"><?php echo esc_html((string) $this->campaign_click_last_days($campaign, 30)); ?> in 30 Tagen</span></td>
                            <td><?php
                                $start = trim((string) ($campaign['start_date'] ?? ''));
                                $end = trim((string) ($campaign['end_date'] ?? ''));
                                echo esc_html($start === '' && $end === '' ? 'Dauerhaft' : (($start ?: 'sofort') . ' bis ' . ($end ?: 'offen')));
                            ?></td>
                            <td><a class="button" href="<?php echo esc_url(admin_url('admin.php?page=affiliate-portal-campaign-edit&campaign_id=' . (int) ($campaign['post_id'] ?? 0))); ?>">Bearbeiten</a><?php
                                $preview_page_id = (int) ($campaign['page_id'] ?? 0);
                                if ($preview_page_id > 0 && $this->campaign_is_complete($campaign)) {
                                    $preview_url = add_query_arg('affiliate_preview_campaign', (int) ($campaign['post_id'] ?? 0), get_permalink($preview_page_id));
                                    echo ' <a class="button" target="_blank" rel="noopener" href="' . esc_url($preview_url) . '">Vorschau</a>';
                                }
                            ?></td>
                        </tr>
                    <?php endforeach; ?>
                    </tbody>
                </table>
            <?php endif; ?>

            <div class="ppar-box" style="margin-top:24px;">
                <h2>Ausgabe testen</h2>
                <p>Hubseite auswählen. Der Test verändert nichts und zeigt, ob 5 Kacheln oder 5 + Banner erwartet werden.</p>
                <form method="get" class="ppar-actions">
                    <input type="hidden" name="page" value="affiliate-portal-zentrale">
                    <?php $this->render_hub_page_dropdown('ppar_test_page_id', $test_page_id, 'Hubseite auswaehlen'); ?>
                    <button class="button">Testen</button>
                </form>
                <?php $this->render_central_test($test_page_id); ?>
            </div>

        </div>
        <?php
    }

    public function render_campaign_edit_page() {
        if (!current_user_can('manage_options')) {
            wp_die('Keine Berechtigung.');
        }
        $post_id = isset($_GET['campaign_id']) ? absint($_GET['campaign_id']) : 0;
        $campaign = $post_id > 0 ? $this->campaign_from_post(get_post($post_id)) : $this->central_blank_campaign();
        if (!$campaign) {
            $campaign = $this->central_blank_campaign();
            $post_id = 0;
        }
        $placements = $this->central_placement_options();
        ?>
        <div class="wrap ppar-edit">
            <style>
                .ppar-edit{max-width:980px}.ppar-card{background:#fff;border:1px solid #c3c4c7;border-radius:8px;padding:20px;margin:16px 0}.ppar-card h2{margin-top:0}.ppar-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}.ppar-grid label{display:flex;flex-direction:column;gap:5px}.ppar-grid input,.ppar-grid select,.ppar-grid textarea{width:100%;max-width:none}.ppar-wide{grid-column:1/-1}.ppar-footer{display:flex;gap:10px;align-items:center;flex-wrap:wrap;position:sticky;bottom:0;background:#f0f0f1;padding:12px 0;border-top:1px solid #c3c4c7}.ppar-danger{color:#b32d2e}@media(max-width:782px){.ppar-grid{grid-template-columns:1fr}.ppar-wide{grid-column:auto}}
            </style>
            <p><a href="<?php echo esc_url(admin_url('admin.php?page=affiliate-portal-creatives')); ?>">← Zur Affiliate-Zentrale</a></p>
            <h1><?php echo $post_id > 0 ? 'Kampagne bearbeiten' : 'Neue Kampagne'; ?></h1>
            <form method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>">
                <input type="hidden" name="action" value="ppar_save_campaign">
                <input type="hidden" name="campaign_post_id" value="<?php echo esc_attr((string) $post_id); ?>">
                <input type="hidden" name="ppar_campaign[id]" value="<?php echo esc_attr((string) ($campaign['id'] ?? '')); ?>">
                <input type="hidden" name="ppar_campaign[source]" value="<?php echo esc_attr((string) ($campaign['source'] ?? 'manual')); ?>">
                <?php wp_nonce_field('ppar_save_campaign', 'ppar_campaign_nonce'); ?>

                <div class="ppar-card">
                    <h2>1. Quelle und Werbemittelart</h2>
                    <div class="ppar-grid">
                        <label><span>Werbemittelart</span><select name="ppar_campaign[creative_type]"><option value="banner" <?php selected($campaign['creative_type'] ?? 'banner','banner'); ?>>Banner</option><option value="product" <?php selected($campaign['creative_type'] ?? 'banner','product'); ?>>Produkt</option></select></label>
                        <label><span>Netzwerk / Quelle</span><select name="ppar_campaign[network]"><?php foreach($this->provider_registry() as $provider_key=>$provider_def): ?><option value="<?php echo esc_attr($provider_key); ?>" <?php selected($campaign['network'] ?? 'manual',$provider_key); ?>><?php echo esc_html((string)$provider_def['label']); ?></option><?php endforeach; ?></select></label>
                        <label><span>Advertiser-/Programm-ID</span><input type="text" name="ppar_campaign[advertiser_id]" value="<?php echo esc_attr((string)($campaign['advertiser_id'] ?? '')); ?>"></label>
                        <label><span>Programmname</span><input type="text" name="ppar_campaign[programme_name]" value="<?php echo esc_attr((string)($campaign['programme_name'] ?? '')); ?>"></label>
                        <label><span>Programmstatus</span><select name="ppar_campaign[programme_status]"><option value="unknown" <?php selected($campaign['programme_status'] ?? 'unknown','unknown'); ?>>Unbekannt</option><option value="active" <?php selected($campaign['programme_status'] ?? 'unknown','active'); ?>>Aktiv</option><option value="paused" <?php selected($campaign['programme_status'] ?? 'unknown','paused'); ?>>Pausiert</option><option value="ended" <?php selected($campaign['programme_status'] ?? 'unknown','ended'); ?>>Beendet</option></select></label>
                        <label><span>Statusquelle</span><input type="text" name="ppar_campaign[programme_status_source]" value="<?php echo esc_attr((string)($campaign['programme_status_source'] ?? '')); ?>" placeholder="z. B. Awin API oder manuell geprüft"></label><?php if (!empty($campaign['programme_status_checked_at'])) : ?><p class="description">Status zuletzt bestätigt: <?php echo esc_html(wp_date('d.m.Y H:i', (int)$campaign['programme_status_checked_at'])); ?></p><?php endif; ?>
                        <label><span>Produktfreigabe</span><select name="ppar_campaign[quality_manual_status]"><option value="unknown" <?php selected($campaign['quality_manual_status'] ?? 'unknown','unknown'); ?>>Ungeprüft</option><option value="approved" <?php selected($campaign['quality_manual_status'] ?? 'unknown','approved'); ?>>Fachlich freigegeben</option><option value="rejected" <?php selected($campaign['quality_manual_status'] ?? 'unknown','rejected'); ?>>Abgelehnt</option></select><small>Nur für Werbemittelart „Produkt“. Öffentliche Produktblöcke verwenden ausschließlich freigegebene Produkte.</small></label>
                        <label class="ppar-wide"><span>Qualitätsnotiz</span><textarea name="ppar_campaign[quality_note]" rows="2"><?php echo esc_textarea((string)($campaign['quality_note'] ?? '')); ?></textarea></label>
                        <label><span>Externe Werbemittel-ID</span><input type="text" name="ppar_campaign[external_id]" value="<?php echo esc_attr((string)($campaign['external_id'] ?? '')); ?>"></label>
                    </div>
                </div>

                <div class="ppar-card">
                    <h2>2. Inhalt</h2>
                    <div class="ppar-grid">
                        <label><span>Interner Name</span><input type="text" name="ppar_campaign[name]" value="<?php echo esc_attr((string) ($campaign['name'] ?? '')); ?>" required placeholder="z. B. Regendecken Sommeraktion"></label>
                        <label><span>Partner / Netzwerk (optional)</span><input type="text" name="ppar_campaign[partner]" value="<?php echo esc_attr((string) ($campaign['partner'] ?? '')); ?>" placeholder="z. B. Amazon, Awin, Direktpartner"></label>
                        <label><span>Kennzeichnung</span><input type="text" name="ppar_campaign[label]" value="<?php echo esc_attr((string) ($campaign['label'] ?? 'Anzeige')); ?>"></label>
                        <label class="ppar-wide"><span>Titel der Werbekachel</span><input type="text" name="ppar_campaign[title]" value="<?php echo esc_attr((string) ($campaign['title'] ?? '')); ?>" placeholder="Passende Produkte entdecken"></label>
                        <label class="ppar-wide"><span>Kurztext (optional)</span><textarea name="ppar_campaign[description]" rows="2"><?php echo esc_textarea((string) ($campaign['description'] ?? '')); ?></textarea></label>
                        <label class="ppar-wide"><span>Affiliate-/Ziel-URL</span><input type="url" name="ppar_campaign[url]" value="<?php echo esc_attr((string) ($campaign['url'] ?? '')); ?>" placeholder="https://..."></label>
                        <label><span>Bild (optional)</span><input class="ppar-image-url" type="url" name="ppar_campaign[image_url]" value="<?php echo esc_attr((string) ($campaign['image_url'] ?? '')); ?>"><button type="button" class="button ppar-select-image">Aus Mediathek wählen</button></label>
                        <label><span>Linktext</span><input type="text" name="ppar_campaign[button_text]" value="<?php echo esc_attr((string) ($campaign['button_text'] ?? 'Mehr erfahren')); ?>"></label>
                        <label><span>Darstellung</span><select name="ppar_campaign[render_mode]"><option value="image_link" <?php selected($campaign['render_mode'] ?? 'image_link','image_link'); ?>>Bild / Text / Link</option><option value="html" <?php selected($campaign['render_mode'] ?? 'image_link','html'); ?>>Netzwerk-HTML</option></select></label>
                        <label><span>Preis (optional)</span><input type="text" name="ppar_campaign[price]" value="<?php echo esc_attr((string)($campaign['price'] ?? '')); ?>"></label>
                        <label><span>Währung</span><input type="text" maxlength="3" name="ppar_campaign[currency]" value="<?php echo esc_attr((string)($campaign['currency'] ?? 'EUR')); ?>"></label>
                        <label><span>Verfügbarkeit</span><input type="text" name="ppar_campaign[availability]" value="<?php echo esc_attr((string)($campaign['availability'] ?? '')); ?>"></label>
                        <label><span>Bannerformat</span><input type="text" name="ppar_campaign[dimensions]" value="<?php echo esc_attr((string)($campaign['dimensions'] ?? '')); ?>" placeholder="z. B. 970×250"></label>
                        <label class="ppar-wide"><span>Netzwerk-HTML (nur bei Darstellung „Netzwerk-HTML“)</span><textarea name="ppar_campaign[html]" rows="5"><?php echo esc_textarea((string)($campaign['html'] ?? '')); ?></textarea></label>
                    </div>
                </div>

                <div class="ppar-card">
                    <h2>3. Automatische Zuordnung</h2>
                    <div class="ppar-grid">
                        <label><span>Wo soll die Kampagne erscheinen?</span><select id="ppar-assignment-mode" name="ppar_campaign[assignment_mode]">
                            <option value="auto_topic" <?php selected($campaign['assignment_mode'], 'auto_topic'); ?>>Automatisch im passenden Hauptbereich (empfohlen)</option>
                            <option value="page_tree" <?php selected($campaign['assignment_mode'], 'page_tree'); ?>>Manuell: ausgewählter Hub und Unterseiten</option>
                            <option value="exact_page" <?php selected($campaign['assignment_mode'], 'exact_page'); ?>>Manuelle Ausnahme: nur eine Seite</option>
                            <option value="keywords" <?php selected($campaign['assignment_mode'], 'keywords'); ?>>Manuell definierte Themenbegriffe</option>
                            <option value="fallback" <?php selected($campaign['assignment_mode'], 'fallback'); ?>>Allgemeiner Fallback</option>
                        </select></label>
                        <label><span>Manueller Hub / Bereich</span><?php $this->render_hub_page_dropdown('ppar_campaign[page_id]', (int) ($campaign['page_id'] ?? 0), 'nur für manuelle Modi'); ?></label>
                        <label class="ppar-wide"><span>Zusätzliche Themenbegriffe</span><textarea name="ppar_campaign[match_keywords]" rows="3" placeholder="z. B. futter, mineralfutter, mash"><?php echo esc_textarea($this->array_to_admin_list((array) ($campaign['match_keywords'] ?? array()))); ?></textarea></label>
                        <?php if (sanitize_key((string)($campaign['assignment_mode'] ?? '')) === 'auto_topic') : ?><div class="ppar-wide" style="background:#f6f7f7;border-left:4px solid #C89214;padding:12px 14px"><strong>Automatisches Ergebnis:</strong> <?php echo esc_html((string)($campaign['auto_topic_label'] ?? '') ?: 'noch kein eindeutiger Bereich'); ?><?php if (!empty($campaign['auto_topic_score'])) : ?> · Score <?php echo absint($campaign['auto_topic_score']); ?><?php endif; ?><br><span class="description"><?php echo esc_html((string)($campaign['auto_topic_reason'] ?? 'Wird beim Speichern aus Partner, Titel, Beschreibung, URL und Themenbegriffen gegen den realen Portalbaum geprüft.')); ?></span></div><?php endif; ?>
                    </div>
                    <input type="hidden" name="ppar_campaign[match_descendants]" value="1">
                    <p class="description">Standard: Das Plugin ermittelt aus Werbemittel- und Partnerdaten genau einen passenden Hub-1-Bereich und erfasst dessen Unterseiten. Schwache oder mehrdeutige Treffer bleiben inaktiv. Manuelle Modi sind nur Ausnahmen.</p>
                </div>

                <div class="ppar-card">
                    <h2>4. Veröffentlichung</h2>
                    <p><label><input type="checkbox" name="ppar_campaign[placements][]" value="product_after_category_tiles" <?php checked(in_array('product_after_category_tiles', (array)($campaign['placements'] ?? array()), true)); ?>> <strong>Affiliate-Banner auf Produkt-/Kategorieseiten</strong></label></p>
                    <p><label><input type="checkbox" name="ppar_campaign[placements][]" value="category_product" <?php checked(in_array('category_product', (array)($campaign['placements'] ?? array()), true)); ?>> <strong>Produktvorschläge auf Produkt-/Kategorieseiten</strong></label></p>
                    <p><label><input type="checkbox" name="ppar_campaign[placements][]" value="post_inline_banner" <?php checked(in_array('post_inline_banner', (array)($campaign['placements'] ?? array()), true)); ?>> <strong>Banner in Einzelbeiträgen</strong> <span class="description">nur für Werbemittelart „Banner“</span></label></p>
                    <p><label><input type="checkbox" name="ppar_campaign[placements][]" value="post_bottom_products" <?php checked(in_array('post_bottom_products', (array)($campaign['placements'] ?? array()), true)); ?>> <strong>Produktvorschläge am Beitragsende</strong> <span class="description">nur für Werbemittelart „Produkt“</span></label></p>
                    <div class="ppar-grid">
                        <label><span>Priorität</span><input type="number" min="0" max="1000" name="ppar_campaign[priority]" value="<?php echo esc_attr((string) ($campaign['priority'] ?? 50)); ?>"><small>Nur bei gleich spezifischer Zuordnung entscheidet die höhere Zahl.</small></label>
                        <label><span>Linkziel</span><select name="ppar_campaign[target]"><option value="_blank" <?php selected($campaign['target'], '_blank'); ?>>Neuer Tab</option><option value="_self" <?php selected($campaign['target'], '_self'); ?>>Gleiches Fenster</option></select></label>
                        <label><span>Startdatum (optional)</span><input type="date" name="ppar_campaign[start_date]" value="<?php echo esc_attr((string) ($campaign['start_date'] ?? '')); ?>"></label>
                        <label><span>Enddatum (optional)</span><input type="date" name="ppar_campaign[end_date]" value="<?php echo esc_attr((string) ($campaign['end_date'] ?? '')); ?>"></label>
                    </div>
                    <p style="margin-top:18px;"><label><input type="checkbox" name="ppar_campaign[active]" value="1" <?php checked(!empty($campaign['active'])); ?>> <strong>Kampagne aktivieren</strong></label></p>
                    <p class="description">Unvollständige Kampagnen werden automatisch inaktiv gespeichert. Ohne gültige Kampagne bleibt das 5er-Raster bestehen.</p>

                    <details style="margin-top:16px;"><summary>Weitere Ausgabepositionen und Importfelder</summary>
                        <div style="padding-top:12px;">
                            <?php foreach ($placements as $slot => $label) : if (in_array($slot, array('hub_grid_card','product_after_category_tiles','category_product','post_inline_banner','post_bottom_products'), true)) { continue; } ?>
                                <p><label><input type="checkbox" name="ppar_campaign[placements][]" value="<?php echo esc_attr($slot); ?>" <?php checked(in_array($slot, (array) ($campaign['placements'] ?? array()), true)); ?>> <?php echo esc_html($label); ?></label></p>
                            <?php endforeach; ?>
                            <div class="ppar-grid">
                                <label class="ppar-wide"><span>Zusätzliche Seiten-Slugs</span><textarea name="ppar_campaign[match_slugs]" rows="2"><?php echo esc_textarea($this->array_to_admin_list((array) ($campaign['match_slugs'] ?? array()))); ?></textarea></label>
                                <label><span>SubID-Parameter</span><input type="text" name="ppar_campaign[subid_param]" value="<?php echo esc_attr((string) ($campaign['subid_param'] ?? '')); ?>"></label>
                                <label><span>Erforderliches Trackingmerkmal</span><input type="text" name="ppar_campaign[required_url_fragment]" value="<?php echo esc_attr((string) ($campaign['required_url_fragment'] ?? '')); ?>" placeholder="z. B. tag=DEIN-TAG"></label>
                                <label class="ppar-wide"><span>Erlaubte Ziel-Domains</span><textarea name="ppar_campaign[allowed_domains]" rows="2" placeholder="eine Domain pro Zeile"><?php echo esc_textarea($this->array_to_admin_list((array)($campaign['allowed_domains'] ?? array()))); ?></textarea></label>
                                <label class="ppar-wide"><input type="checkbox" name="ppar_campaign[health_check_enabled]" value="1" <?php checked(!empty($campaign['health_check_enabled'])); ?>> Dieses Werbemittel regelmäßig im Prüfzentrum kontrollieren</label>
                            </div>
                        </div>
                    </details>
                </div>

                <div class="ppar-footer">
                    <?php submit_button('Speichern', 'primary', 'submit', false); ?>
                    <button class="button" type="submit" name="save_and_continue" value="1">Speichern und weiter bearbeiten</button>
                    <a class="button" href="<?php echo esc_url(admin_url('admin.php?page=affiliate-portal-creatives')); ?>">Abbrechen</a>
                    <?php if ($post_id > 0 && (int) ($campaign['page_id'] ?? 0) > 0 && $this->campaign_is_complete($campaign)) :
                        $preview_url = add_query_arg('affiliate_preview_campaign', $post_id, get_permalink((int) $campaign['page_id'])); ?>
                        <a class="button" target="_blank" rel="noopener" href="<?php echo esc_url($preview_url); ?>">Banner auf Hubseite ansehen</a>
                    <?php endif; ?>
                </div>
            </form>

            <?php if ($post_id > 0) : ?>
                <form method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>" onsubmit="return confirm('Kampagne wirklich in den Papierkorb verschieben?');" style="margin-top:28px;">
                    <input type="hidden" name="action" value="ppar_delete_campaign"><input type="hidden" name="campaign_post_id" value="<?php echo esc_attr((string) $post_id); ?>">
                    <?php wp_nonce_field('ppar_delete_campaign_' . $post_id, 'ppar_delete_nonce'); ?>
                    <button class="button ppar-danger">Kampagne löschen</button>
                </form>
            <?php endif; ?>
        </div>
        <?php
    }

    public function render_control_center_page() {
        if (!current_user_can('manage_options')) {
            wp_die('Keine Berechtigung.');
        }

        $groups = $this->get_groups();
        $active_groups = array_filter($groups, function($g) { return !empty($g['active']); });
        $banner_counts = $this->get_control_center_banner_counts($groups);
        $warnings = $this->build_control_center_warnings($groups);

        $filter = isset($_GET['ppar_cc_filter']) ? sanitize_key((string) $_GET['ppar_cc_filter']) : 'all';
        $search = isset($_GET['ppar_cc_search']) ? sanitize_text_field(wp_unslash((string) $_GET['ppar_cc_search'])) : '';
        $rows_all = $this->build_control_center_rows();
        $rows = $this->filter_control_center_rows($rows_all, $filter, $search);
        $status_counts = $this->count_control_center_row_statuses($rows_all);
        ?>
        <div class="wrap">
            <h1>Affiliate Portal Kontrollzentrum</h1>
            <p><strong>Version:</strong> <?php echo esc_html(self::VERSION); ?>. Zentrale read-only Übersicht. Änderungen erfolgen ausschließlich in der Affiliate-Zentrale.</p>
            <p><a class="button button-primary" href="<?php echo esc_url(admin_url('admin.php?page=affiliate-portal-creatives')); ?>">Affiliate-Zentrale öffnen</a> <a class="button" href="<?php echo esc_url(admin_url('admin.php?page=affiliate-portal-router-check')); ?>">Trockenprüfung öffnen</a></p>

            <h2>Status</h2>
            <table class="widefat striped" style="max-width:980px;">
                <tbody>
                    <tr><th>Affiliate-Ausgabe</th><td><?php echo $this->is_enabled() ? 'Aktiv' : 'Inaktiv'; ?></td></tr>
                    <tr><th>Kategorie-/Archiv-Ausgabe</th><td><?php echo $this->is_category_archive_enabled() ? 'Aktiv' : 'Inaktiv'; ?></td></tr>
                    <tr><th>Template-/Hub-Ausgabe</th><td><?php echo $this->is_template_enabled() ? 'Aktiv' : 'Inaktiv'; ?></td></tr>
                    <tr><th>Aktive Gruppen</th><td><?php echo esc_html((string) count($active_groups)); ?> / <?php echo esc_html((string) count($groups)); ?></td></tr>
                    <tr><th>Aktive Banner absolut</th><td><?php echo esc_html((string) $banner_counts['active']); ?> / <?php echo esc_html((string) $banner_counts['total']); ?></td></tr>
                    <tr><th>Effektiv ausspielbare Banner</th><td><?php echo esc_html((string) $banner_counts['effective']); ?> / <?php echo esc_html((string) $banner_counts['total']); ?></td></tr>
                    <tr><th>Live-Stichprobe</th><td><?php echo esc_html((string) ($status_counts['ok'] ?? 0)); ?> OK / <?php echo esc_html((string) ($status_counts['warn'] ?? 0)); ?> WARN / <?php echo esc_html((string) ($status_counts['info'] ?? 0)); ?> INFO</td></tr>
                </tbody>
            </table>

            <h2>Kontrollhinweise</h2>
            <?php if (empty($warnings)) : ?>
                <div class="notice notice-success inline"><p><strong>PASS:</strong> Keine harten Konfigurationshinweise im Kontrollzentrum.</p></div>
            <?php else : ?>
                <table class="widefat striped" style="max-width:1100px;">
                    <thead><tr><th>Status</th><th>Bereich</th><th>Hinweis</th><th>Bearbeiten</th></tr></thead>
                    <tbody>
                        <?php foreach ($warnings as $warning) : ?>
                            <tr>
                                <td><strong><?php echo esc_html($warning['severity']); ?></strong></td>
                                <td><?php echo esc_html($warning['area']); ?></td>
                                <td><?php echo esc_html($warning['message']); ?></td>
                                <td><?php echo !empty($warning['edit_url']) ? '<a class="button" href="' . esc_url($warning['edit_url']) . '">Bearbeiten</a>' : '-'; ?></td>
                            </tr>
                        <?php endforeach; ?>
                    </tbody>
                </table>
            <?php endif; ?>

            <?php $suggestions = $this->build_control_center_suggestions($rows_all); ?>
            <h2>Automatisierungs-Vorschläge</h2>
            <p>Massentaugliche Hinweise aus der Live-Stichprobe. Es werden keine Gruppen automatisch angelegt.</p>
            <?php if (empty($suggestions)) : ?>
                <div class="notice notice-success inline"><p><strong>PASS:</strong> Keine priorisierten Vorschläge aus der aktuellen Stichprobe.</p></div>
            <?php else : ?>
                <table class="widefat striped" style="max-width:1100px;">
                    <thead><tr><th>Typ</th><th>Vorschlag</th><th>Grund</th></tr></thead>
                    <tbody>
                        <?php foreach ($suggestions as $suggestion) : ?>
                            <tr>
                                <td><?php echo esc_html($suggestion['type']); ?></td>
                                <td><code><?php echo esc_html($suggestion['suggested_group_id']); ?></code></td>
                                <td><?php echo esc_html($suggestion['reason']); ?></td>
                            </tr>
                        <?php endforeach; ?>
                    </tbody>
                </table>
            <?php endif; ?>

            <h2>Anzeigengruppen und Banner</h2>
            <table class="widefat striped">
                <thead><tr><th>Gruppe</th><th>Status</th><th>Matching</th><th>Banner</th><th>Slots</th><th>Bearbeiten</th></tr></thead>
                <tbody>
                    <?php foreach ($groups as $g_index => $group) : ?>
                        <?php $banners = isset($group['banners']) && is_array($group['banners']) ? $group['banners'] : array(); ?>
                        <tr>
                            <td><strong><?php echo esc_html((string) ($group['label'] ?? $group['id'] ?? '')); ?></strong><br><code><?php echo esc_html((string) ($group['id'] ?? '')); ?></code></td>
                            <td><?php echo !empty($group['active']) ? 'Aktiv' : 'Inaktiv'; ?></td>
                            <td>
                                <strong>Modus:</strong> <?php echo esc_html($this->match_mode_label($group['match_mode'] ?? 'auto')); ?><br>
                                <strong>Workflow:</strong> <?php echo esc_html($this->workflow_status_label($group['workflow_status'] ?? 'offen')); ?><br>
                                <strong>Slugs:</strong> <?php echo esc_html($this->control_join($group['match_slugs'] ?? array())); ?><br>
                                <strong>Keywords:</strong> <?php echo esc_html($this->control_join($group['match_keywords'] ?? array())); ?>
                                <?php if (!empty($group['workflow_note'])) : ?><br><em><?php echo esc_html((string) $group['workflow_note']); ?></em><?php endif; ?>
                            </td>
                            <td>
                                <?php foreach ($banners as $banner) : ?>
                                    <?php
                                        $banner_active = !empty($banner['active']);
                                        $has_output = !empty($banner['url']) || !empty($banner['html']);
                                        $effective = !empty($group['active']) && $banner_active && $has_output;
                                    ?>
                                    <?php echo $banner_active ? 'Aktiv' : 'Inaktiv'; ?> / <?php echo $effective ? 'effektiv ausspielbar' : 'nicht effektiv'; ?> - <code><?php echo esc_html((string) ($banner['id'] ?? '')); ?></code> <?php echo !$has_output ? '<strong style="color:#b32d2e;">ohne URL/HTML</strong>' : ''; ?><br>
                                <?php endforeach; ?>
                            </td>
                            <td>
                                <?php foreach ($banners as $banner) : ?>
                                    <code><?php echo esc_html($this->control_join($banner['slots'] ?? array())); ?></code><br>
                                <?php endforeach; ?>
                            </td>
                            <td><a class="button" href="<?php echo esc_url($this->build_group_edit_url($g_index)); ?>">Gruppe bearbeiten</a></td>
                        </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>

            <h2>Live-Stichprobe</h2>
            <p>Zeigt, was nach den aktuellen globalen Regeln voraussichtlich matched. Es werden keine Inhalte verändert.</p>
            <form method="get" style="margin:12px 0 16px 0;">
                <input type="hidden" name="page" value="affiliate-portal-kontrollzentrum">
                <label for="ppar_cc_filter"><strong>Filter:</strong></label>
                <select id="ppar_cc_filter" name="ppar_cc_filter">
                    <?php
                    $filters = array(
                        'all' => 'alle',
                        'matches' => 'nur Matches',
                        'no_match' => 'nur kein Match',
                        'warn' => 'nur WARN',
                        'posts' => 'nur Beiträge',
                        'categories' => 'nur Kategorien',
                        'pages' => 'nur Seiten/Hubs',
                    );
                    foreach ($filters as $key => $label) {
                        echo '<option value="' . esc_attr($key) . '" ' . selected($filter, $key, false) . '>' . esc_html($label) . '</option>';
                    }
                    ?>
                </select>
                <label for="ppar_cc_search" style="margin-left:12px;"><strong>Suche:</strong></label>
                <input id="ppar_cc_search" type="search" name="ppar_cc_search" value="<?php echo esc_attr($search); ?>" placeholder="Titel, Slug, Gruppe, Banner" style="min-width:280px;">
                <button class="button">Anwenden</button>
                <a class="button" href="<?php echo esc_url(admin_url('admin.php?page=affiliate-portal-kontrollzentrum')); ?>">Zurücksetzen</a>
            </form>
            <table class="widefat striped">
                <thead><tr><th>Typ</th><th>Objekt</th><th>Kontext/Slot</th><th>Erkannte Gruppe</th><th>Erkannter Banner</th><th>Status</th></tr></thead>
                <tbody>
                    <?php foreach ($rows as $row) : ?>
                        <tr>
                            <td><?php echo esc_html($row['type']); ?></td>
                            <td><?php echo !empty($row['edit_url']) ? '<a href="' . esc_url($row['edit_url']) . '">' . esc_html($row['title']) . '</a>' : esc_html($row['title']); ?><br><code><?php echo esc_html($row['slug']); ?></code></td>
                            <td><?php echo esc_html($row['context']); ?><br><code><?php echo esc_html($row['slot']); ?></code></td>
                            <td><?php echo esc_html($row['group']); ?></td>
                            <td><?php echo esc_html($row['banner']); ?></td>
                            <td><strong><?php echo esc_html($row['status']); ?></strong> <span style="opacity:.75;">(<?php echo esc_html($row['severity']); ?>)</span><br><?php echo esc_html($row['details']); ?></td>
                        </tr>
                    <?php endforeach; ?>
                    <?php if (empty($rows)) : ?>
                        <tr><td colspan="6">Keine Stichproben gefunden.</td></tr>
                    <?php endif; ?>
                </tbody>
            </table>

            <h2>Bedienregel</h2>
            <p>80 bis 90 Prozent sollen automatisch über Gruppen, Slugs, Keywords und Slots laufen. Manuelle Änderungen erfolgen nachträglich je Anzeigengruppe/Banner im Router. Einzelobjekt-Ausnahmen sind für eine spätere Version vorgesehen und dürfen nicht zu Massen-Handarbeit führen.</p>
        </div>
        <?php
    }

    private function get_control_center_banner_counts($groups) {
        $counts = array('total' => 0, 'active' => 0, 'effective' => 0);
        foreach ($groups as $group) {
            $group_active = !empty($group['active']);
            $banners = isset($group['banners']) && is_array($group['banners']) ? $group['banners'] : array();
            foreach ($banners as $banner) {
                $counts['total']++;
                $banner_active = !empty($banner['active']);
                $has_output = !empty($banner['url']) || !empty($banner['html']);
                if ($banner_active) {
                    $counts['active']++;
                }
                if ($group_active && $banner_active && $has_output) {
                    $counts['effective']++;
                }
            }
        }
        return $counts;
    }

    private function build_control_center_warnings($groups) {
        $warnings = array();
        foreach ($groups as $g_index => $group) {
            $group_label = (string) ($group['label'] ?? $group['id'] ?? ('Gruppe ' . ((int) $g_index + 1)));
            $group_active = !empty($group['active']);
            $banners = isset($group['banners']) && is_array($group['banners']) ? $group['banners'] : array();
            $workflow_status = isset($group['workflow_status']) ? sanitize_key((string) $group['workflow_status']) : 'offen';
            if ($workflow_status === 'fehler') {
                $warnings[] = array(
                    'severity' => 'WARN',
                    'area' => $group_label,
                    'message' => 'Gruppe ist im Workflow als Fehler markiert. Vor produktiver Nutzung prüfen.',
                    'edit_url' => $this->build_group_edit_url($g_index),
                );
            }
            if (!$group_active && !empty($banners)) {
                foreach ($banners as $banner) {
                    if (!empty($banner['active'])) {
                        $warnings[] = array(
                            'severity' => 'WARN',
                            'area' => $group_label,
                            'message' => 'Banner aktiv, aber Gruppe inaktiv; Banner wird nicht ausgespielt.',
                            'edit_url' => $this->build_group_edit_url($g_index),
                        );
                        break;
                    }
                }
            }
            foreach ($banners as $banner) {
                $banner_id = (string) ($banner['id'] ?? 'ohne_id');
                if (!empty($banner['active']) && empty($banner['url']) && empty($banner['html'])) {
                    $warnings[] = array(
                        'severity' => 'WARN',
                        'area' => $group_label,
                        'message' => 'Banner ' . $banner_id . ' ist aktiv, hat aber keine URL/HTML; Ausgabe bleibt leer.',
                        'edit_url' => $this->build_group_edit_url($g_index),
                    );
                }
                $slots = isset($banner['slots']) && is_array($banner['slots']) ? $banner['slots'] : array();
                if (!empty($banner['active']) && empty($slots)) {
                    $warnings[] = array(
                        'severity' => 'WARN',
                        'area' => $group_label,
                        'message' => 'Banner ' . $banner_id . ' ist aktiv, hat aber keinen Slot; Ausgabe ist unwirksam.',
                        'edit_url' => $this->build_group_edit_url($g_index),
                    );
                }
            }
        }
        return $warnings;
    }

    private function build_control_center_suggestions($rows) {
        $suggestions = array();
        $seen = array();
        foreach ($rows as $row) {
            if (($row['status'] ?? '') !== 'kein Match') {
                continue;
            }
            $type = (string) ($row['type'] ?? '');
            if (!in_array($type, array('Kategoriearchiv', 'Seite/Hub'), true)) {
                continue;
            }
            $slug = sanitize_key((string) ($row['slug'] ?? ''));
            if ($slug === '' || $slug === 'uncategorized') {
                continue;
            }
            $parts = explode('-', $slug);
            $base_parts = array();
            foreach ($parts as $part) {
                if (in_array($part, array('faq', 'beratung', 'vergleich', 'pflege', 'kosten', 'ratgeber', 'checklisten'), true)) {
                    continue;
                }
                $base_parts[] = $part;
            }
            $suggested = sanitize_key(implode('_', array_slice($base_parts, 0, 4)));
            if ($suggested === '' || isset($seen[$suggested])) {
                continue;
            }
            $seen[$suggested] = true;
            $suggestions[] = array(
                'type' => $type,
                'suggested_group_id' => $suggested,
                'reason' => 'Kein Match für ' . (string) ($row['title'] ?? $slug) . '. Prüfen, ob eine neue Anzeigengruppe sinnvoll ist.',
            );
            if (count($suggestions) >= 10) {
                break;
            }
        }
        return $suggestions;
    }

    private function filter_control_center_rows($rows, $filter, $search) {
        $filtered = array();
        foreach ($rows as $row) {
            if (!$this->row_matches_control_filter($row, $filter)) {
                continue;
            }
            if ($search !== '') {
                $haystack = strtolower(implode(' ', array(
                    $row['type'] ?? '',
                    $row['title'] ?? '',
                    $row['slug'] ?? '',
                    $row['context'] ?? '',
                    $row['slot'] ?? '',
                    $row['group'] ?? '',
                    $row['banner'] ?? '',
                    $row['status'] ?? '',
                    $row['details'] ?? '',
                )));
                if (strpos($haystack, strtolower($search)) === false) {
                    continue;
                }
            }
            $filtered[] = $row;
        }
        return $filtered;
    }

    private function row_matches_control_filter($row, $filter) {
        $status = (string) ($row['status'] ?? '');
        $severity = (string) ($row['severity'] ?? 'INFO');
        $type = (string) ($row['type'] ?? '');
        if ($filter === 'matches') {
            return in_array($status, array('wird ausgespielt', 'würde ausspielen', 'wird über Design-Slot ausgespielt'), true) || strpos($status, 'würde') === 0;
        }
        if ($filter === 'no_match') {
            return $status === 'kein Match';
        }
        if ($filter === 'warn') {
            return $severity === 'WARN';
        }
        if ($filter === 'posts') {
            return $type === 'Beitrag';
        }
        if ($filter === 'categories') {
            return $type === 'Kategoriearchiv';
        }
        if ($filter === 'pages') {
            return $type === 'Seite/Hub';
        }
        return true;
    }

    private function count_control_center_row_statuses($rows) {
        $counts = array('ok' => 0, 'warn' => 0, 'info' => 0);
        foreach ($rows as $row) {
            $severity = (string) ($row['severity'] ?? 'INFO');
            if ($severity === 'OK') {
                $counts['ok']++;
            } elseif ($severity === 'WARN') {
                $counts['warn']++;
            } else {
                $counts['info']++;
            }
        }
        return $counts;
    }

    private function build_group_edit_url($group_index) {
        $groups = $this->get_groups();
        $id = isset($groups[(int) $group_index]['id']) ? sanitize_key((string) $groups[(int) $group_index]['id']) : '';
        $url = admin_url('admin.php?page=affiliate-portal-creatives');
        return $id !== '' ? add_query_arg('ppar_open_campaign', $id, $url) : $url;
    }

    private function control_join($items) {
        if (!is_array($items) || empty($items)) {
            return '-';
        }
        $items = array_map('strval', $items);
        return implode(', ', $items);
    }

    private function build_control_center_rows() {
        $rows = array();
        $groups = $this->get_groups();

        $post_slots = $this->get_auto_slots();
        if (empty($post_slots)) {
            $post_slots = array('post_bottom_recommendation');
        }
        $posts = get_posts(array('post_type' => 'post', 'post_status' => 'publish', 'numberposts' => 20, 'orderby' => 'date', 'order' => 'DESC'));
        foreach ($posts as $post) {
            $context = $this->get_content_context($post->ID);
            $rows[] = $this->build_control_row('Beitrag', $post->post_title, $post->post_name, get_edit_post_link($post->ID, ''), $context, $post_slots[0], 'primary_product', $groups);
        }

        $category_slots = $this->get_category_slots();
        if (empty($category_slots)) {
            $category_slots = array('category_recommendation');
        }
        $terms = get_categories(array('hide_empty' => false, 'number' => 20, 'orderby' => 'count', 'order' => 'DESC'));
        foreach ($terms as $term) {
            $context = $this->get_category_archive_context($term);
            $rows[] = $this->build_control_row('Kategoriearchiv', $term->name, $term->slug, get_edit_term_link($term->term_id, 'category'), $context, $category_slots[0], 'primary_product', $groups);
        }

        $pages = get_posts(array('post_type' => 'page', 'post_status' => 'publish', 'numberposts' => 20, 'orderby' => 'menu_order title', 'order' => 'ASC'));
        $front_page_id = (int) get_option('page_on_front');
        foreach ($pages as $page) {
            $context_key = $this->get_template_context_for_page_id($page->ID, $front_page_id > 0 && (int) $page->ID === $front_page_id);
            $slot = in_array($context_key, array('hub_ebene_1', 'hub_ebene_2'), true) ? 'hub_grid_card' : 'product_after_category_tiles';
            $context = $this->get_content_context($page->ID);
            $has_design_shortcode = $this->content_has_design_template_shortcode((string) $page->post_content);
            $row = $this->build_control_row('Seite/Hub', $page->post_title, $page->post_name, get_edit_post_link($page->ID, ''), $context, $slot, 'primary_product', $groups);

            if ($row['group'] !== '-' && $row['banner'] !== '-' && $has_design_shortcode) {
                $slot_visible = $this->is_design_slot_visible_for_content((string) $page->post_content, $slot);
                if ($slot_visible) {
                    $row['status'] = 'wird über Design-Slot ausgespielt';
                    $row['severity'] = 'OK';
                    $row['details'] = 'Matching aktiv; Design-Shortcode vorhanden; Router ersetzt kein Hubdesign und füllt nur den Design-Slot. Template-/Hub-Ausgabe darf dafür inaktiv bleiben.';
                } else {
                    $row['status'] = 'Design-Slot inaktiv';
                    $row['severity'] = 'WARN';
                    $row['details'] = 'Matching aktiv, aber der passende Design-Slot ist im Design-Plugin deaktiviert. Hubdesign bleibt geschützt; Slot im Design-Plugin aktivieren oder bewusst ignorieren.';
                }
            }

            if ($context_key === '' && $row['group'] !== '-' && !$has_design_shortcode) {
                $row['status'] = 'Portalrolle fehlt';
                $row['severity'] = 'WARN';
                $row['details'] = 'Gruppe/Banner matched, aber keine Portalrolle erkannt. Portalrolle setzen oder bewusst ignorieren. ' . $row['details'];
            } elseif ($context_key === '') {
                $row['details'] .= ' Keine Portalrolle erkannt.';
            } else {
                $row['details'] .= ' Portalrolle: ' . $context_key . '.';
            }
            if ($has_design_shortcode) {
                $row['details'] .= ' Design-Shortcode geschützt; keine Router-Template-Ersetzung.';
            }
            $rows[] = $row;
        }

        return $rows;
    }

    private function build_control_row($type, $title, $slug, $edit_url, $context, $slot, $intent, $groups) {
        $base = array(
            'type' => $type,
            'title' => $title,
            'slug' => $slug,
            'edit_url' => $edit_url,
            'context' => $context['post_type'] ?? '',
            'slot' => $slot,
            'group' => '-',
            'banner' => '-',
            'status' => 'kein Match',
            'severity' => 'INFO',
            'details' => 'Keine aktive Gruppe passend zu Slug/Keyword.',
        );

        $group = $this->find_matching_group($groups, $context);
        if (!$group) {
            return $base;
        }

        $base['group'] = (string) ($group['id'] ?? '');
        $banner = $this->find_matching_banner($group, $context, $slot, $intent);
        if (!$banner) {
            $base['status'] = 'kein Banner';
            $base['severity'] = 'WARN';
            $base['details'] = 'Gruppe matched, aber kein aktiver Banner fuer Slot/Intention.';
            return $base;
        }

        $base['banner'] = (string) ($banner['id'] ?? '');
        $has_output = !empty($banner['url']) || !empty($banner['html']);
        if (!$has_output) {
            $base['status'] = 'leer blockiert';
            $base['severity'] = 'WARN';
            $base['details'] = 'Banner hat keine URL/HTML und muss leer bleiben.';
            return $base;
        }

        if (!$this->is_enabled()) {
            $base['status'] = 'Affiliate-Ausgabe inaktiv';
            $base['severity'] = 'WARN';
            $base['details'] = 'Matching aktiv, aber globaler Affiliate-Schalter ist inaktiv.';
            return $base;
        }

        $slot_state = $this->control_slot_state($type, $slot);
        if ($slot_state['active'] === false) {
            $base['status'] = $slot_state['status'];
            $base['severity'] = $slot_state['severity'];
            $base['details'] = 'Matching aktiv, aber Ausgabe aktuell nicht aktiv: ' . $slot_state['details'];
            return $base;
        }

        $base['status'] = 'wird ausgespielt';
        $base['severity'] = 'OK';
        $base['details'] = 'Matching aktiv; globaler Schalter und Slot sind aktiv.';
        return $base;
    }

    private function control_slot_state($type, $slot) {
        if ($type === 'Beitrag') {
            $auto_slots = $this->get_auto_slots();
            $accepted = $this->equivalent_slot_names($slot);
            return array(
                'active' => !empty(array_intersect($auto_slots, $accepted)),
                'status' => 'Beitragsslot inaktiv',
                'severity' => 'WARN',
                'details' => 'Automatische Beitragsslots enthalten ' . $slot . ' nicht.',
            );
        }
        if ($type === 'Kategoriearchiv') {
            if (!$this->is_category_archive_enabled()) {
                return array('active' => false, 'status' => 'Kategorie-Ausgabe inaktiv', 'severity' => 'WARN', 'details' => 'Kategorie-/Archiv-Ausgabe ist global inaktiv.');
            }
            $category_slots = $this->get_category_slots();
            $accepted = $this->equivalent_slot_names($slot);
            return array(
                'active' => !empty(array_intersect($category_slots, $accepted)),
                'status' => 'Kategorie-Slot inaktiv',
                'severity' => 'WARN',
                'details' => 'Automatische Kategorie-Slots enthalten ' . $slot . ' nicht.',
            );
        }
        if ($type === 'Seite/Hub') {
            if (!$this->is_template_enabled()) {
                return array('active' => false, 'status' => 'Hub-Ausgabe inaktiv', 'severity' => 'INFO', 'details' => 'Template-/Hub-Ausgabe ist global inaktiv; vorhandenes Design bleibt geschützt.');
            }
            return array('active' => true, 'status' => 'würde ausspielen', 'severity' => 'OK', 'details' => 'Hub-Ausgabe ist aktiv.');
        }
        return array('active' => true, 'status' => 'würde ausspielen', 'severity' => 'OK', 'details' => 'Kein spezieller Slot-Blocker erkannt.');
    }

    public function render_check_page() {
        if (!current_user_can('manage_options')) {
            wp_die('Keine Berechtigung.');
        }

        $checks = $this->run_diagnostic_checks();
        $fail = 0;
        $warn = 0;
        $pass = 0;
        foreach ($checks as $check) {
            if ($check['status'] === 'FAIL') {
                $fail++;
            } elseif ($check['status'] === 'WARN') {
                $warn++;
            } elseif ($check['status'] === 'PASS') {
                $pass++;
            }
        }
        ?>
        <div class="wrap">
            <h1>Interne Systemprüfung</h1>
            <p><strong>Version:</strong> <?php echo esc_html(self::VERSION); ?>. Diese Seite führt eine read-only Trockenprüfung aus. Es werden keine Beiträge, Seiten, Kategorien, Gruppen oder Banner angelegt oder verändert.</p>
            <p><strong>Zweck:</strong> Positiv-/Negativtest für Allgemeingültigkeit, Automatisierung, Slot-Vertrag, Affiliate-Ausgabe und Backend-Bedienbarkeit. <strong>Kein Nachweis einer realen WordPress-/HivePress-Frontend-End-to-End-Ausgabe.</strong></p>
            <p><strong>Ergebnis:</strong> <?php echo esc_html((string) $pass); ?> PASS, <?php echo esc_html((string) $warn); ?> WARN, <?php echo esc_html((string) $fail); ?> FAIL.</p>

            <?php if ($fail > 0) : ?>
                <div class="notice notice-error"><p><strong>BLOCKED:</strong> Mindestens ein harter Negativ-/Konfigurationstest ist fehlgeschlagen.</p></div>
            <?php elseif ($warn > 0) : ?>
                <div class="notice notice-warning"><p><strong>BEDINGT OK:</strong> Harte Tests bestanden, aber es gibt Warnungen für echte WordPress-Inhalte oder aktive Angebote.</p></div>
            <?php else : ?>
                <div class="notice notice-success"><p><strong>PASS:</strong> Trockenprüfung bestanden.</p></div>
            <?php endif; ?>

            <table class="widefat striped" style="max-width:1100px;">
                <thead>
                    <tr>
                        <th>Status</th>
                        <th>Bereich</th>
                        <th>Prüfung</th>
                        <th>Details</th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach ($checks as $check) : ?>
                        <tr>
                            <td><strong><?php echo esc_html($check['status']); ?></strong></td>
                            <td><?php echo esc_html($check['area']); ?></td>
                            <td><?php echo esc_html($check['label']); ?></td>
                            <td><?php echo esc_html($check['details']); ?></td>
                        </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>

        </div>
        <?php
    }

    private function diagnostic_version_consistency() {
        $main_source = @file_get_contents(__FILE__);
        $readme_path = dirname(__FILE__) . '/readme.txt';
        $readme_source = is_readable($readme_path) ? @file_get_contents($readme_path) : false;

        $header_version = '';
        if (is_string($main_source) && preg_match('/^[ \t\/*#@]*Version:\s*([^\r\n]+)/mi', $main_source, $match)) {
            $header_version = trim((string) $match[1]);
        }

        $stable_tag = '';
        if (is_string($readme_source) && preg_match('/^\s*Stable tag:\s*([^\r\n]+)/mi', $readme_source, $match)) {
            $stable_tag = trim((string) $match[1]);
        }

        $ok = $header_version === self::VERSION && $stable_tag === self::VERSION;
        return array(
            'ok' => $ok,
            'details' => 'Klasse ' . self::VERSION . ', Plugin-Header ' . ($header_version !== '' ? $header_version : 'FEHLT') . ', Readme ' . ($stable_tag !== '' ? $stable_tag : 'FEHLT') . '.',
        );
    }

    private function run_diagnostic_checks() {
        $checks = array();

        $version_check = $this->diagnostic_version_consistency();
        $this->add_check($checks, 'Basis', 'Versionskonsistenz', !empty($version_check['ok']) ? 'PASS' : 'FAIL', (string) $version_check['details']);
        $this->add_check($checks, 'V4-Architektur', 'Zentrales Ausgabeobjekt', method_exists($this, 'output_plan_creative') && method_exists($this, 'render_output_objects_page') && self::OUTPUT_SCHEMA_VERSION === '1.3' ? 'PASS' : 'FAIL', 'Partner, Creative, Portalziel und Ausgabe werden über das V4-Ausgabeobjekt verbunden.');
        $registry = method_exists($this, 'output_portal_registry') ? $this->output_portal_registry() : array();
        $local_portal_key = method_exists($this, 'output_local_portal_key') ? $this->output_local_portal_key() : '';
        $portal_ok = $local_portal_key !== '' && is_array($registry[$local_portal_key] ?? null) && !is_wp_error($this->output_validate_portal_profile($registry[$local_portal_key]));
        $this->add_check($checks, 'V4-Architektur', 'Lokales Portalprofil', $portal_ok ? 'PASS' : 'FAIL', $portal_ok ? 'Lokales Portal ist mit Fachprofil und Ausgabetypen registriert.' : 'Lokales Portalprofil fehlt oder ist ungültig.');
        $slot_matrix = $portal_ok ? $this->output_slot_matrix($registry[$local_portal_key]) : array();
        $required_v4_slots = array('start_after_topics','hub_grid_card','hub_after_cards','product_after_category_tiles','journal_banner','anzeigenmarkt_top_banner','category_product_1','category_product_2','category_product_3','journal_product_1','journal_product_2','journal_product_3');
        $missing_v4_slots = array_diff($required_v4_slots, array_keys(is_array($slot_matrix) ? $slot_matrix : array()));
        $this->add_check($checks, 'V4-Architektur', 'Design V1.50.387 Slotmatrix', empty($missing_v4_slots) ? 'PASS' : 'FAIL', empty($missing_v4_slots) ? 'Alle zwölf realen Designslots sind registriert.' : 'Fehlende V4-Designslots: ' . implode(', ', $missing_v4_slots));
        $this->add_check($checks, 'V4-Architektur', 'Portaladaptervertrag', self::PORTAL_ADAPTER_VERSION === '1.0' ? 'PASS' : 'FAIL', 'Weitere Portale benötigen Adaptervertrag 1.0 und bleiben bei fehlenden Pflichtdaten fail-closed.');
        $ebay_settings = method_exists($this, 'ebay_settings') ? $this->ebay_settings() : array();
        $ebay_core_ok = method_exists($this, 'run_ebay_sync') && method_exists($this, 'ebay_filter_stale_posts') && method_exists($this, 'ebay_expire_stale_items');
        $this->add_check($checks, 'eBay', 'Provideradapter und Eingangsweiche', $ebay_core_ok ? 'PASS' : 'FAIL', $ebay_core_ok ? 'INDIVIDUAL/BUSINESS-Adapter, Inhaltsisolation und Löschpfad vorhanden.' : 'eBay-Kern ist unvollständig.');
        $ebay_limits_ok = absint($ebay_settings['sync_interval_hours'] ?? 0) === 3 && absint($ebay_settings['stale_hours'] ?? 0) === 6;
        $this->add_check($checks, 'eBay', 'Drei-Stunden-Abgleich und Sechs-Stunden-Grenze', $ebay_limits_ok ? 'PASS' : 'FAIL', $ebay_limits_ok ? 'Sicherheitsgrenzen sind unveränderbar aktiv.' : 'eBay-Sicherheitsgrenzen weichen ab.');
        $ebay_errors = !empty($ebay_settings['enabled']) && method_exists($this, 'ebay_configuration_errors') ? $this->ebay_configuration_errors($ebay_settings) : array();
        $this->add_check($checks, 'eBay', 'Produktionsfreigabe', empty($ebay_settings['enabled']) || empty($ebay_errors) ? 'PASS' : 'FAIL', empty($ebay_settings['enabled']) ? 'eBay-Synchronisierung ist AUS; Aktivierung erst nach Verbindungstest.' : (empty($ebay_errors) ? 'Lokale Pflichtkonfiguration vollständig.' : implode(' ', $ebay_errors)));
        $automation_settings = $this->automation_settings();
        $automation_limits_ok = in_array((string) ($automation_settings['executor'] ?? ''), array('server_cron','wp_cron'), true)
            && absint($automation_settings['batch_size'] ?? 0) >= 100
            && absint($automation_settings['batch_size'] ?? 0) <= 1000
            && absint($automation_settings['time_budget'] ?? 0) >= 10
            && absint($automation_settings['time_budget'] ?? 0) <= 25
            && absint($automation_settings['request_timeout'] ?? 0) >= 15
            && absint($automation_settings['request_timeout'] ?? 0) <= 45;
        $this->add_check($checks, 'Automatisierung', 'Sichere Verarbeitungsgrenzen', $automation_limits_ok ? 'PASS' : 'FAIL', $automation_limits_ok ? 'Paket-, Zeit- und Downloadgrenzen gültig.' : 'Mindestens eine Sicherheitsgrenze liegt außerhalb des zulässigen Bereichs.');
        $this->add_check($checks, 'Automatisierung', 'Automatische Synchronisierung', empty($automation_settings['enabled']) ? 'PASS' : 'WARN', empty($automation_settings['enabled']) ? 'Automatisierung ist AUS.' : 'Automatisierung ist aktiv; nur nach bestätigtem Live-Test zulässig.');
        $awin_settings = $this->network_settings('awin');
        $manual_feed_url = trim((string) ($awin_settings['product_feed_url'] ?? ''));
        $manual_feed_partner = absint($awin_settings['product_feed_partner_id'] ?? 0);
        $manual_feed_ok = $manual_feed_url === '' || $manual_feed_partner > 0;
        $this->add_check($checks, 'Awin', 'Manueller Produktfeed eindeutig gebunden', $manual_feed_ok ? 'PASS' : 'FAIL', $manual_feed_url === '' ? 'Keine manuelle Produktfeed-URL hinterlegt.' : ($manual_feed_ok ? 'Produktfeed ist einer Advertiser-ID eindeutig zugeordnet.' : 'Produktfeed-URL vorhanden, aber Advertiser-ID fehlt; Produktimport bleibt gesperrt.'));
        $this->add_check($checks, 'Basis', 'Affiliate standardmäßig getrennt aktivierbar', is_bool($this->is_enabled()) ? 'PASS' : 'FAIL', 'Affiliate-Ausgabe läuft über eigenen Aktiv-Schalter.');
        $this->add_check($checks, 'Basis', 'Template standardmäßig getrennt aktivierbar', is_bool($this->is_template_enabled()) ? 'PASS' : 'FAIL', 'Template-Ausgabe läuft über eigenen Aktiv-Schalter.');

        $groups_json = (string) get_option(self::OPTION_GROUPS_JSON, self::default_groups_json());
        $groups = json_decode($groups_json, true);
        $groups_valid = is_array($groups) && json_last_error() === JSON_ERROR_NONE;
        $this->add_check($checks, 'Backend', 'Affiliate-Gruppen lesbar', $groups_valid ? 'PASS' : 'FAIL', $groups_valid ? 'Gruppen-JSON ist gültig.' : 'Gruppen-JSON ist ungültig. Speichern/Import blockieren.');

        $template_json = (string) get_option(self::OPTION_TEMPLATE_RULES_JSON, self::default_template_rules_json());
        $template_rules = json_decode($template_json, true);
        $template_valid = is_array($template_rules) && json_last_error() === JSON_ERROR_NONE;
        $template_rule_check = $template_valid ? $this->validate_template_rules($template_rules) : false;
        $this->add_check($checks, 'Backend', 'Template-Regeln lesbar', ($template_valid && $template_rule_check === true) ? 'PASS' : 'FAIL', ($template_rule_check === 'word_alle') ? 'Einzelwort „Alle“ wird korrekt blockiert.' : ($template_valid ? 'Template-Regeln gültig.' : 'Template-Regeln ungültig.'));

        $design_json = (string) get_option(self::OPTION_DESIGN_RULES_JSON, self::default_design_rules_json());
        $design_rules = json_decode($design_json, true);
        $design_valid = is_array($design_rules) && json_last_error() === JSON_ERROR_NONE;
        $this->add_check($checks, 'Backend', 'Design-Regeln lesbar', $design_valid ? 'PASS' : 'FAIL', $design_valid ? 'Design-Regeln gültig.' : 'Design-Regeln ungültig.');

        $required_contexts = array('startseite', 'haupt_hub_ebene_1', 'bereichs_hub_ebene_2', 'produktseite_ebene_3');
        $missing_contexts = array_diff($required_contexts, $this->allowed_template_contexts());
        $this->add_check($checks, 'Allgemeingültigkeit', 'Start/Hub1/Hub2/Produkt-Ebene vorhanden', empty($missing_contexts) ? 'PASS' : 'FAIL', empty($missing_contexts) ? 'Alle Pflicht-Kontexte vorhanden.' : 'Fehlende Kontexte: ' . implode(', ', $missing_contexts));

        $required_slots = array('post_after_intro', 'post_mid_content', 'post_bottom_recommendation');
        $missing_slots = array_diff($required_slots, $this->allowed_auto_slots());
        $this->add_check($checks, 'Slot-Vertrag', 'Beitrags-Slots vorhanden', empty($missing_slots) ? 'PASS' : 'FAIL', empty($missing_slots) ? 'Pflichtslots vorhanden.' : 'Fehlende Slots: ' . implode(', ', $missing_slots));

        $hub_aliases = $this->equivalent_slot_names('hub_after_cards');
        $this->add_check($checks, 'Slot-Vertrag', 'Hub-Slot-Alias funktioniert', in_array('template_after_selected', $hub_aliases, true) ? 'PASS' : 'FAIL', 'hub_after_cards muss mit template_after_selected kompatibel sein.');

        $product_tile_aliases = $this->equivalent_slot_names('product_after_category_tiles');
        $this->add_check($checks, 'Slot-Vertrag', 'Produktseiten-Slot nach Kategorie-Kacheln vorhanden', in_array('category_recommendation', $product_tile_aliases, true) ? 'PASS' : 'FAIL', 'product_after_category_tiles muss mit category_recommendation kompatibel sein, damit bestehende Banner weiter funktionieren.');

        $bottom_aliases = $this->equivalent_slot_names('post_bottom_recommendation');
        $this->add_check($checks, 'Slot-Vertrag', 'Neuer Beitragsslot mit Legacy kompatibel', in_array('bottom_recommendation', $bottom_aliases, true) ? 'PASS' : 'FAIL', 'post_bottom_recommendation muss bottom_recommendation-Banner akzeptieren.');

        $missing_category_slots = array_diff(array('category_recommendation'), $this->allowed_category_slots());
        $this->add_check($checks, 'Kategoriearchive', 'Kategorie-Slot vorhanden', empty($missing_category_slots) ? 'PASS' : 'FAIL', empty($missing_category_slots) ? 'category_recommendation vorhanden.' : 'Kategorie-Slot fehlt.');

        $missing_template_placements = array_diff(array('top_cta', 'after_selected', 'after_hint', 'bottom'), $this->allowed_template_affiliate_placements());
        $this->add_check($checks, 'Hub-/Startseiten', 'Template-Affiliate-Platzierungen vorhanden', empty($missing_template_placements) ? 'PASS' : 'FAIL', empty($missing_template_placements) ? 'Start-/Hub-/Produktseiten-Platzierungen vorhanden.' : 'Fehlende Platzierungen: ' . implode(', ', $missing_template_placements));

        $filter_source = (method_exists($this, 'auto_inject_template_affiliate_slots') && method_exists($this, 'content_has_design_template_shortcode'));
        $this->add_check($checks, 'Hub-/Startseiten', 'Designschutz vorhanden', $filter_source ? 'PASS' : 'FAIL', $filter_source ? 'Hub-/Startseiten-Schutz vorhanden: Design-Shortcodes werden nicht durch Router-Template ersetzt.' : 'Designschutz fehlt.');

        $role_helper_ok = method_exists($this, 'get_template_context_for_page_id') && method_exists($this, 'is_design_slot_visible_for_content');
        $this->add_check($checks, 'Kontrollzentrum', 'Admin-sichere Hub-/Portalrollen-Erkennung', $role_helper_ok ? 'PASS' : 'FAIL', $role_helper_ok ? 'Kontrollzentrum erkennt Portalrollen und Design-Slots ohne Frontend-Conditional-Abhaengigkeit.' : 'Admin-sichere Portalrollen-/Designslot-Erkennung fehlt.');
        $this->add_check($checks, 'Bedienbarkeit', 'Matching-Modus je Gruppe vorhanden', method_exists($this, 'allowed_match_modes') ? 'PASS' : 'FAIL', 'Anzeigengruppen müssen eng, breit, automatisch oder Fallback matchen können.');
        $this->add_check($checks, 'Workflow', 'Workflow-Status je Gruppe vorhanden', method_exists($this, 'allowed_workflow_statuses') ? 'PASS' : 'FAIL', 'Anzeigengruppen müssen als offen, geprüft, ignorieren oder Fehler markierbar sein.');
        $this->add_check($checks, 'Automatisierung', 'Kontrollzentrum-Vorschläge vorbereitet', method_exists($this, 'build_control_center_suggestions') ? 'PASS' : 'FAIL', 'Kontrollzentrum soll Themen ohne Match als Vorschläge bündeln.');

        $mock_context = array(
            'slugs' => array('testprodukt', 'testgruppe'),
            'names' => array('Testprodukt', 'Testgruppe'),
            'primary_slug' => 'testprodukt',
            'primary_name' => 'Testprodukt',
            'post_type' => 'post',
            'haystack' => 'testprodukt testgruppe kaufberatung vergleich kosten angebot'
        );
        $mock_groups = array(
            array(
                'id' => 'testgruppe',
                'label' => 'Testgruppe',
                'active' => true,
                'match_mode' => 'auto',
                'workflow_status' => 'geprueft',
                'match_slugs' => array('testprodukt'),
                'match_keywords' => array('kaufberatung'),
                'banners' => array(
                    array(
                        'id' => 'testbanner',
                        'label' => 'Anzeige',
                        'active' => true,
                        'mode' => 'image_link',
                        'slots' => array('post_mid_content', 'post_bottom_recommendation', 'hub_after_cards', 'category_recommendation'),
                        'intent' => array('primary_product'),
                        'priority' => 10,
                        'match_slugs' => array('testprodukt'),
                        'match_keywords' => array('angebot'),
                        'url' => 'https://example.com/test?subid={subid}',
                        'subid_param' => '',
                        'image_url' => '',
                        'title' => 'Testangebot',
                        'description' => 'Trockenlauf-Angebot',
                        'button_text' => 'Zum Testangebot'
                    )
                )
            )
        );

        $matched_group = $this->find_matching_group($mock_groups, $mock_context);
        $this->add_check($checks, 'Positivtest', 'Gruppe wird über Slug/Keyword gefunden', (!empty($matched_group) && $matched_group['id'] === 'testgruppe') ? 'PASS' : 'FAIL', 'Mock-Kontext muss aktive Testgruppe finden.');

        $matched_banner = $matched_group ? $this->find_matching_banner($matched_group, $mock_context, 'post_mid_content', 'primary_product') : null;
        $this->add_check($checks, 'Positivtest', 'Banner wird über Slot/Intent gefunden', (!empty($matched_banner) && $matched_banner['id'] === 'testbanner') ? 'PASS' : 'FAIL', 'Mock-Banner muss für post_mid_content/primary_product gefunden werden.');

        $bottom_banner = $matched_group ? $this->find_matching_banner($matched_group, $mock_context, 'post_bottom_recommendation', 'primary_product') : null;
        $this->add_check($checks, 'Positivtest', 'post_bottom_recommendation findet Banner', (!empty($bottom_banner) && $bottom_banner['id'] === 'testbanner') ? 'PASS' : 'FAIL', 'Neuer Beitragsslot muss ohne Legacy-Haken funktionieren.');

        $html = $matched_banner ? $this->render_banner($matched_banner, 999999, $mock_context, $matched_group, 'post_mid_content') : '';
        $rel_tokens = array();
        if (preg_match('/\brel="([^"]*)"/i', $html, $rel_match)) {
            $rel_tokens = preg_split('/\s+/', strtolower(trim((string) $rel_match[1])));
            $rel_tokens = is_array($rel_tokens) ? array_values(array_filter($rel_tokens, 'strlen')) : array();
        }
        $required_rel_tokens = array('sponsored', 'nofollow', 'noopener');
        $html_ok = strpos($html, 'href=') !== false
            && strpos($html, 'Zum Testangebot') !== false
            && empty(array_diff($required_rel_tokens, $rel_tokens));
        $this->add_check($checks, 'Positivtest', 'Affiliate-HTML ist klickbar und gekennzeichnet', $html_ok ? 'PASS' : 'FAIL', 'Ausgabe muss Link, Buttontext sowie mindestens sponsored, nofollow und noopener im rel-Attribut enthalten. Zusätzliche Sicherheitswerte sind zulässig.');

        $bad_context = $mock_context;
        $bad_context['slugs'] = array('falsches-thema');
        $bad_context['haystack'] = 'falsches thema ohne treffer';
        $bad_match = $this->find_matching_group($mock_groups, $bad_context);
        $this->add_check($checks, 'Negativtest', 'Falsches Thema erzeugt keinen Treffer', $bad_match === null ? 'PASS' : 'FAIL', 'Unpassende Slugs/Keywords dürfen kein Banner ausspielen.');

        $inactive_group = $mock_groups;
        $inactive_group[0]['banners'][0]['active'] = false;
        $inactive_banner = $this->find_matching_banner($inactive_group[0], $mock_context, 'post_mid_content', 'primary_product');
        $this->add_check($checks, 'Negativtest', 'Inaktiver Banner bleibt unsichtbar', $inactive_banner === null ? 'PASS' : 'FAIL', 'Inaktive Banner dürfen nicht ausgegeben werden.');

        $empty_url_banner = $mock_groups[0]['banners'][0];
        $empty_url_banner['url'] = '';
        $empty_html = $this->render_banner($empty_url_banner, 999999, $mock_context, $mock_groups[0], 'post_mid_content');
        $this->add_check($checks, 'Negativtest', 'Banner ohne URL erzeugt keine leere Box', $empty_html === '' ? 'PASS' : 'FAIL', 'Leerer URL-Banner muss vollständig leer bleiben.');

        $word_alle = $this->validate_template_rules(array('startseite' => array('button_text' => 'Alle')));
        $this->add_check($checks, 'Negativtest', 'Verbotenes Einzelwort „Alle“ wird blockiert', $word_alle === 'word_alle' ? 'PASS' : 'FAIL', 'Unklare Button-/Überschrift darf nicht gespeichert werden.');

        $top_pages = function_exists('get_pages') ? get_pages(array('parent' => 0, 'post_status' => 'publish')) : array();
        $top_count = is_array($top_pages) ? count($top_pages) : 0;
        $this->add_check($checks, 'Live-Strukturtest', 'Top-Level-Seiten lesbar', $top_count > 0 ? 'PASS' : 'WARN', $top_count > 0 ? 'Top-Level-Seiten gefunden: ' . $top_count . '.' : 'Keine veröffentlichten Top-Level-Seiten gefunden. Für echten Hub-Test Testseiten anlegen.');

        $terms = function_exists('get_terms') ? get_terms(array('taxonomy' => 'category', 'hide_empty' => false)) : array();
        $term_count = (!is_wp_error($terms) && is_array($terms)) ? count($terms) : 0;
        $this->add_check($checks, 'Live-Strukturtest', 'Kategorien lesbar', $term_count > 0 ? 'PASS' : 'WARN', $term_count > 0 ? 'Kategorien gefunden: ' . $term_count . '.' : 'Keine Kategorien gefunden. Für Produkt-/Kategorieebene Testkategorien anlegen.');

        $conflicts = $this->get_conflicting_template_plugins();
        $this->add_check($checks, 'Konfliktprüfung', 'Template-Konflikte', empty($conflicts) ? 'PASS' : 'WARN', empty($conflicts) ? 'Keine aktiven Konfliktplugins erkannt.' : 'Mögliche Konflikte: ' . implode(', ', $conflicts));
        $this->add_check($checks, 'Kontrollzentrum', 'Übersicht verfügbar', method_exists($this, 'render_control_center_page') ? 'PASS' : 'FAIL', 'Zentrale Übersicht für Gruppen, Banner, Slots und Live-Stichproben muss vorhanden sein.');
        $this->add_check($checks, 'Kontrollzentrum', 'Gruppen nachträglich bearbeitbar', method_exists($this, 'build_group_edit_url') ? 'PASS' : 'FAIL', 'Kontrollzentrum verlinkt in die Bearbeitung der jeweiligen Anzeigengruppe.');

        return $checks;
    }

    private function add_check(&$checks, $area, $label, $status, $details) {
        $status = strtoupper((string) $status);
        if (!in_array($status, array('PASS', 'WARN', 'FAIL', 'INFO'), true)) {
            $status = 'INFO';
        }
        $checks[] = array(
            'area' => (string) $area,
            'label' => (string) $label,
            'status' => $status,
            'details' => (string) $details,
        );
    }

    public function render_article_hybrid_page() {
        if (!current_user_can('manage_options')) {
            wp_die('Keine Berechtigung.');
        }
        $enabled = $this->is_enabled();
        $settings = $this->article_hybrid_settings();
        $preview = $this->article_preview_settings();
        $banner_choices = $this->article_preview_campaign_choices('banner');
        $product_choices = $this->article_preview_campaign_choices('product');
        $normal_banner_count = $this->article_normal_placement_count('banner', 'post_inline_banner');
        $normal_product_count = $this->article_normal_placement_count('product', 'post_bottom_products');
        $posts = get_posts(array(
            'post_type' => 'post',
            'post_status' => array('publish','draft','pending','private'),
            'numberposts' => 250,
            'orderby' => 'modified',
            'order' => 'DESC',
        ));
        ?>
        <div class="wrap">
            <h1>Affiliate-Ausgabe in Einzelbeiträgen</h1>
            <?php if (isset($_GET['ppar_article_saved'])) : ?>
                <div class="notice notice-success is-dismissible"><p>Einzelbeitrags-Einstellungen gespeichert.</p></div>
            <?php endif; ?>
            <?php if (isset($_GET['ppar_article_preview_saved'])) : ?>
                <div class="notice notice-success is-dismissible"><p>Administrator-Test gespeichert.</p></div>
            <?php endif; ?>
            <p>Der gespeicherte Beitragstext wird nicht verändert.</p>

            <div style="background:#fff;border:1px solid #c3c4c7;padding:18px;margin:16px 0;max-width:980px">
                <h2 style="margin-top:0">Harter Ausgabestatus</h2>
                <p><strong>Aktive Banner mit Freigabe „Banner in Einzelbeiträgen“:</strong> <?php echo absint($normal_banner_count); ?></p>
                <p><strong>Aktive Produkte mit Freigabe „Produktvorschläge am Beitragsende“:</strong> <?php echo absint($normal_product_count); ?></p>
                <p class="description">Das Speichern des Hybridmodells erzeugt und ordnet kein Werbemittel zu. Ein Banner benötigt zusätzlich die sichtbare Kampagnenfreigabe „Banner in Einzelbeiträgen“. Der Abschlussblock akzeptiert ausschließlich Werbemittelart „Produkt“.</p>
            </div>

            <form method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>" style="background:#fff;border:1px solid #c3c4c7;padding:18px;max-width:980px">
                <?php wp_nonce_field('ppar_save_article_hybrid', 'ppar_article_hybrid_nonce'); ?>
                <input type="hidden" name="action" value="ppar_save_article_hybrid">
                <h2>Normale automatische Ausgabe</h2>
                <table class="form-table" role="presentation">
                    <tr>
                        <th scope="row">Affiliate-Ausgabe für Beiträge aktivieren</th>
                        <td><label><input type="checkbox" name="ppar_enabled" value="1" <?php checked($enabled); ?>> Aktiv</label><p class="description">Ohne diesen Hauptschalter wird in Beiträgen nichts ausgegeben.</p></td>
                    </tr>
                    <tr>
                        <th scope="row">Hybridmodell für bestehende Beiträge aktivieren</th>
                        <td><label><input type="checkbox" name="ppar_article_hybrid[enabled]" value="1" <?php checked(!empty($settings['enabled'])); ?>> Aktiv</label><p class="description">Pro Beitrag ist höchstens ein Inline-Banner zulässig. Die Position wird vorab als Ausgabeplan gespeichert: nach abgeschlossenem Fließtext und direkt vor der nächsten geeigneten H2- oder H3-Zwischenüberschrift. Produkte erscheinen ausschließlich am Beitragsende.</p></td>
                    </tr>
                </table>
                <?php submit_button('Einstellungen speichern'); ?>
            </form>

            <form method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>" style="background:#fff;border:1px solid #c3c4c7;padding:18px;margin-top:18px;max-width:980px">
                <?php wp_nonce_field('ppar_save_article_preview', 'ppar_article_preview_nonce'); ?>
                <input type="hidden" name="action" value="ppar_save_article_preview">
                <h2>Administrator-Test mit vorhandenen Werbemitteln</h2>
                <p>Der Test ist ausschließlich für angemeldete Administratoren sichtbar. Er ändert weder die Kampagne noch die öffentliche Zuordnung und darf deshalb auch einen thematisch unpassenden Testpartner verwenden.</p>
                <table class="form-table" role="presentation">
                    <tr><th scope="row">Administrator-Test aktivieren</th><td><label><input type="checkbox" name="ppar_article_preview[enabled]" value="1" <?php checked(!empty($preview['enabled'])); ?>> Aktiv</label></td></tr>
                    <tr><th scope="row"><label for="ppar-preview-post">Testbeitrag</label></th><td><select id="ppar-preview-post" name="ppar_article_preview[post_id]" style="min-width:420px"><option value="0">– auswählen –</option><?php foreach ($posts as $post) : ?><option value="<?php echo absint($post->ID); ?>" <?php selected(absint($preview['post_id']), absint($post->ID)); ?>><?php echo esc_html(get_the_title($post) . ' · ID ' . $post->ID); ?></option><?php endforeach; ?></select></td></tr>
                    <?php for ($i=0;$i<1;$i++) : $selected=absint($preview['banner_campaign_ids'][$i] ?? 0); ?>
                    <tr><th scope="row"><label for="ppar-preview-banner-<?php echo $i+1; ?>">Testbanner <?php echo $i+1; ?></label></th><td><select id="ppar-preview-banner-<?php echo $i+1; ?>" name="ppar_article_preview[banner_campaign_ids][]" style="min-width:420px"><option value="0">– kein Banner –</option><?php foreach ($banner_choices as $id=>$label) : ?><option value="<?php echo absint($id); ?>" <?php selected($selected, absint($id)); ?>><?php echo esc_html($label . ' · ID ' . $id); ?></option><?php endforeach; ?></select></td></tr>
                    <?php endfor; ?>
                    <tr><th scope="row"><label for="ppar-preview-product-count">Anzahl Produktflächen im Test</label></th><td><select id="ppar-preview-product-count" name="ppar_article_preview[product_preview_count]"><option value="0" <?php selected((int)$preview['product_preview_count'],0); ?>>0</option><option value="1" <?php selected((int)$preview['product_preview_count'],1); ?>>1</option><option value="2" <?php selected((int)$preview['product_preview_count'],2); ?>>2</option><option value="3" <?php selected((int)$preview['product_preview_count'],3); ?>>3</option></select><p class="description">Nur im Administrator-Test. Öffentliche Beiträge zeigen weiterhin ausschließlich 1–3 echte Produkte; bei 0 bleibt der Bereich unsichtbar.</p></td></tr>
                    <?php for ($i=0;$i<3;$i++) : $selected=absint($preview['product_campaign_ids'][$i] ?? 0); ?>
                    <tr><th scope="row"><label for="ppar-preview-product-<?php echo $i+1; ?>">Testprodukt <?php echo $i+1; ?></label></th><td><select id="ppar-preview-product-<?php echo $i+1; ?>" name="ppar_article_preview[product_campaign_ids][]" style="min-width:420px"><option value="0">– kein Produkt –</option><?php foreach ($product_choices as $id=>$label) : ?><option value="<?php echo absint($id); ?>" <?php selected($selected, absint($id)); ?>><?php echo esc_html($label . ' · ID ' . $id); ?></option><?php endforeach; ?></select></td></tr>
                    <?php endfor; ?>
                </table>
                <p class="description">Verfügbare vollständige Banner: <?php echo count($banner_choices); ?> · vollständige Produkte: <?php echo count($product_choices); ?>. Wenn hier 0 Produkte stehen, kann der Produktblock noch nicht real dargestellt werden.</p>
                <?php submit_button('Administrator-Test speichern'); ?>
                <?php if (!empty($preview['enabled']) && absint($preview['post_id']) > 0) : ?><p><a class="button button-secondary" target="_blank" rel="noopener" href="<?php echo esc_url(get_permalink(absint($preview['post_id']))); ?>">Testbeitrag öffnen</a></p><?php endif; ?>
            </form>

            <div style="background:#fff;border:1px solid #c3c4c7;padding:18px;margin-top:18px;max-width:980px">
                <h2 style="margin-top:0">Persistente Ausgabepläne</h2>
                <p>Die öffentliche Ausgabe verwendet ausschließlich einen gespeicherten, aktuellen Plan. Ändert sich Beitrag oder Kampagnenbestand, wird ein alter Plan fail-closed nicht mehr ausgespielt.</p>
                <?php if (isset($_GET['ppar_plans_rebuilt'])) : ?><div class="notice notice-success inline"><p><?php echo absint($_GET['ppar_plans_rebuilt']); ?> Ausgabepläne neu berechnet.</p></div><?php endif; ?>
                <form method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>">
                    <?php wp_nonce_field('ppar_rebuild_article_plans', 'ppar_article_plans_nonce'); ?>
                    <input type="hidden" name="action" value="ppar_rebuild_article_plans">
                    <?php submit_button('Alle Ausgabepläne neu berechnen', 'secondary', 'submit', false); ?>
                </form>
                <table class="widefat striped" style="margin-top:16px"><thead><tr><th>Beitrag</th><th>Plan</th><th>Banner</th><th>Produkte</th><th>Aktion</th></tr></thead><tbody>
                <?php foreach (array_slice($posts, 0, 50) as $article_post) : $plan=$this->article_plan_get($article_post->ID); $current=$this->article_plan_is_current($article_post->ID,$plan); ?>
                    <tr>
                        <td><strong><?php echo esc_html(get_the_title($article_post)); ?></strong><br><small>ID <?php echo absint($article_post->ID); ?></small></td>
                        <td><?php echo $current ? esc_html((string)($plan['status'] ?? '')) : '<strong style="color:#b32d2e">veraltet/fehlt</strong>'; ?></td>
                        <td><?php echo esc_html((string)($plan['banner']['status'] ?? 'none')); ?><?php if (!empty($plan['banner']['reason'])) : ?><br><small><?php echo esc_html((string)$plan['banner']['reason']); ?></small><?php endif; ?></td>
                        <td><?php echo count((array)($plan['products']['campaign_post_ids'] ?? array())); ?><?php if (!empty($plan['products']['reason'])) : ?><br><small><?php echo esc_html((string)$plan['products']['reason']); ?></small><?php endif; ?></td>
                        <td><form method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>"><?php wp_nonce_field('ppar_rebuild_single_article_plan_' . $article_post->ID, 'ppar_single_plan_nonce'); ?><input type="hidden" name="action" value="ppar_rebuild_single_article_plan"><input type="hidden" name="post_id" value="<?php echo absint($article_post->ID); ?>"><button class="button">Neu berechnen</button></form></td>
                    </tr>
                <?php endforeach; ?>
                </tbody></table>
            </div>
        </div>
        <?php
    }

    public function handle_save_article_hybrid() {
        if (!current_user_can('manage_options')) {
            wp_die('Keine Berechtigung.');
        }
        check_admin_referer('ppar_save_article_hybrid', 'ppar_article_hybrid_nonce');
        $raw = isset($_POST['ppar_article_hybrid']) && is_array($_POST['ppar_article_hybrid']) ? wp_unslash($_POST['ppar_article_hybrid']) : array();
        $settings = array(
            'enabled' => !empty($raw['enabled']),
        );
        update_option(self::OPTION_ENABLED, isset($_POST['ppar_enabled']) ? '1' : '0', false);
        update_option(self::OPTION_ARTICLE_HYBRID, $settings, false);
        wp_safe_redirect(add_query_arg('ppar_article_saved', '1', admin_url('admin.php?page=affiliate-portal-article-hybrid')));
        exit;
    }


    public function handle_save_article_preview() {
        if (!current_user_can('manage_options')) {
            wp_die('Keine Berechtigung.');
        }
        check_admin_referer('ppar_save_article_preview', 'ppar_article_preview_nonce');
        $raw = isset($_POST['ppar_article_preview']) && is_array($_POST['ppar_article_preview']) ? wp_unslash($_POST['ppar_article_preview']) : array();
        $settings = array(
            'enabled' => !empty($raw['enabled']),
            'post_id' => absint($raw['post_id'] ?? 0),
            'banner_campaign_ids' => array_slice(array_values(array_filter(array_map('absint', (array)($raw['banner_campaign_ids'] ?? array())))), 0, 1),
            'product_campaign_ids' => array_slice(array_values(array_filter(array_map('absint', (array)($raw['product_campaign_ids'] ?? array())))), 0, 3),
            'product_preview_count' => max(0, min(3, absint($raw['product_preview_count'] ?? 3))),
        );
        update_option(self::OPTION_ARTICLE_PREVIEW, $settings, false);
        wp_safe_redirect(add_query_arg('ppar_article_preview_saved', '1', admin_url('admin.php?page=affiliate-portal-article-hybrid')));
        exit;
    }

    public function render_admin_page() {
        if (!current_user_can('manage_options')) {
            wp_die('Keine Berechtigung.');
        }

        $enabled = $this->is_enabled();
        $template_enabled = $this->is_template_enabled();
        $debug = get_option(self::OPTION_DEBUG, '0') === '1';
        $auto_slots = $this->get_auto_slots();
        $template_contexts = $this->get_template_contexts();
        $category_enabled = $this->is_category_archive_enabled();
        $category_slots = $this->get_category_slots();
        $groups_json = (string) get_option(self::OPTION_GROUPS_JSON, self::default_groups_json());
        $template_rules_json = (string) get_option(self::OPTION_TEMPLATE_RULES_JSON, self::default_template_rules_json());
        $design_rules_json = (string) get_option(self::OPTION_DESIGN_RULES_JSON, self::default_design_rules_json());
        $disclosure = (string) get_option(self::OPTION_DISCLOSURE, '');
        $article_hybrid = $this->article_hybrid_settings();
        $groups = $this->get_groups();
        $template_rules_for_form = json_decode($template_rules_json, true);
        if (!is_array($template_rules_for_form)) {
            $template_rules_for_form = array();
        }
        $active_groups = array_filter($groups, function($g) { return !empty($g['active']); });

        $slot_options = array(
            'post_after_intro' => 'Beitrag: nach Einleitung',
            'post_mid_content' => 'Beitrag: im Inhalt',
            'post_bottom_recommendation' => 'Beitrag: unten',
            'hub_top_cta' => 'Hub: CTA oben',
            'hub_after_cards' => 'Hub: nach Karten',
            'hub_grid_card' => 'Hub: sechste Kachel im 5/6-Raster',
            'hub_mid_banner' => 'Hub: mittlerer Banner',
            'category_recommendation' => 'Produkt/Kategorie: Empfehlung',
            'product_after_category_tiles' => 'Ebene 3: Rasterwerbung; auf Endkategorien bis zu zwei Anzeigen',
            'top_info' => 'Legacy: top_info',
            'mid_content' => 'Legacy: mid_content',
            'bottom_recommendation' => 'Legacy: bottom_recommendation',
        );
        $intent_options = array(
            'soft_hint' => 'weicher Hinweis',
            'primary_product' => 'primäre Produktempfehlung',
            'fallback' => 'Fallback',
        );
        $template_affiliate_slot_options = array(
            'top_cta' => 'Hub/Start: CTA oben',
            'after_selected' => 'Hub/Start: nach Karten',
            'after_hint' => 'Hub/Start: nach Hinweis',
            'bottom' => 'Hub/Start/Produkt: unten',
        );
        ?>
        <div class="wrap">
            <h1>Affiliate Portal Router <small style="font-size:13px;">allgemein / pferde-kompatibel</small></h1>
            <p><strong>Status:</strong> Version <?php echo esc_html(self::VERSION); ?>. Design definiert Slots. Affiliate füllt passende aktive Slots. Leere Slots bleiben unsichtbar.</p>
            <p><strong>Bedienprinzip:</strong> Formular ist Hauptbedienung. JSON bleibt nur als Experten-/Importmodus erhalten. Kein Rückbau: vorhandene Gruppen und Banner bleiben erhalten.</p>

            <form method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>">
                <?php wp_nonce_field('ppar_save_settings', 'ppar_nonce'); ?>
                <input type="hidden" name="action" value="ppar_save_settings">
                <input type="hidden" name="ppar_groups_form_submitted" value="1">

                <h2>1. Affiliate-Ausgabe für Beiträge</h2>
                <table class="form-table" role="presentation">
                    <tr>
                        <th scope="row">Affiliate-Ausgabe aktivieren</th>
                        <td>
                            <label><input type="checkbox" name="ppar_enabled" value="1" <?php checked($enabled); ?>> Aktiv</label>
                            <p class="description">Wenn deaktiviert, gibt das Plugin weder automatisch noch per Shortcode Banner aus.</p>
                        </td>
                    </tr>
                    <tr>
                        <th scope="row">Automatische Beitragsslots</th>
                        <td>
                            <label><input type="checkbox" name="ppar_auto_slots[]" value="post_after_intro" <?php checked(in_array('post_after_intro', $auto_slots, true)); ?>> post_after_intro nach Einleitung</label><br>
                            <label><input type="checkbox" name="ppar_auto_slots[]" value="post_mid_content" <?php checked(in_array('post_mid_content', $auto_slots, true)); ?>> post_mid_content im Artikel</label><br>
                            <label><input type="checkbox" name="ppar_auto_slots[]" value="post_bottom_recommendation" <?php checked(in_array('post_bottom_recommendation', $auto_slots, true)); ?>> post_bottom_recommendation am Ende</label><br>
                            <hr style="max-width:520px;margin-left:0;">
                            <label><input type="checkbox" name="ppar_auto_slots[]" value="top_info" <?php checked(in_array('top_info', $auto_slots, true)); ?>> Legacy-Alias top_info</label><br>
                            <label><input type="checkbox" name="ppar_auto_slots[]" value="mid_content" <?php checked(in_array('mid_content', $auto_slots, true)); ?>> Legacy-Alias mid_content</label><br>
                            <label><input type="checkbox" name="ppar_auto_slots[]" value="bottom_recommendation" <?php checked(in_array('bottom_recommendation', $auto_slots, true)); ?>> Legacy-Alias bottom_recommendation</label>
                            <p class="description">Empfehlung zum Start: erst nur post_bottom_recommendation testen. Legacy-Aliasse bleiben kompatibel.</p>
                        </td>
                    </tr>
                    <tr>
                        <th scope="row">Einzelbeitrag-Hybridtest</th>
                        <td>
                            <label><input type="checkbox" name="ppar_article_hybrid[enabled]" value="1" <?php checked(!empty($article_hybrid['enabled'])); ?>> Hybridmodell für bestehende Beiträge aktivieren</label>
                            <p class="description"><strong>Feste Schutzregel:</strong> Höchstens ein Banner nach abgeschlossenem Fließtext und direkt vor der nächsten geeigneten H2. Zusätzlich höchstens eine Produktanzeige mit 1–3 freigegebenen Produkten am Beitragsende. Die öffentliche Ausgabe verwendet ausschließlich einen zuvor gespeicherten, aktuellen Ausgabeplan. Ohne passende Befüllung keinerlei Ausgabe.</p>
                        </td>
                    </tr>
                    <tr>
                        <th scope="row">Affiliate-Hinweis</th>
                        <td>
                            <textarea name="ppar_disclosure" rows="3" class="large-text"><?php echo esc_textarea($disclosure); ?></textarea>
                            <p class="description">Wird pro Beitrag maximal einmal oberhalb des ersten ausgespielten Affiliate-Slots angezeigt.</p>
                        </td>
                    </tr>
                </table>

                <h2>2. Portal-Template-/Hub-Affiliate-Ausgabe</h2>
                <table class="form-table" role="presentation">
                    <tr>
                        <th scope="row">Template-Ausgabe aktivieren</th>
                        <td>
                            <label><input type="checkbox" name="ppar_template_enabled" value="1" <?php checked($template_enabled); ?>> Aktiv</label>
                            <p class="description">Wenn deaktiviert, werden Startseite und Hubseiten nicht automatisch mit Affiliate-Slots ergänzt. Vorhandene Design-Shortcodes bleiben unverändert.</p>
                        </td>
                    </tr>
                    <tr>
                        <th scope="row">Automatische Seitentypen</th>
                        <td>
                            <label><input type="checkbox" name="ppar_template_contexts[]" value="startseite" <?php checked(in_array('startseite', $template_contexts, true)); ?>> Startseite</label><br>
                            <label><input type="checkbox" name="ppar_template_contexts[]" value="haupt_hub_ebene_1" <?php checked(in_array('haupt_hub_ebene_1', $template_contexts, true)); ?>> Haupt-Hub Ebene 1</label><br>
                            <label><input type="checkbox" name="ppar_template_contexts[]" value="bereichs_hub_ebene_2" <?php checked(in_array('bereichs_hub_ebene_2', $template_contexts, true)); ?>> Bereichs-Hub Ebene 2</label><br>
                            <label><input type="checkbox" name="ppar_template_contexts[]" value="produktseite_ebene_3" <?php checked(in_array('produktseite_ebene_3', $template_contexts, true)); ?>> Produktseite Ebene 3</label>
                            <p class="description">V0.7: Der Router erzeugt hier kein eigenes Hub-Design mehr. Er darf nur sichere Affiliate-Slots ergänzen.</p>
                        </td>
                    </tr>
                    <tr>
                        <th scope="row">Automatische Template-Affiliate-Slots</th>
                        <td>
                            <p class="description">Gilt für Startseite, Haupt-Hub Ebene 1, Bereichs-Hub Ebene 2 und Produktseite Ebene 3. Seiten mit Design-Shortcode werden geschützt; dort füllt der Router nur die vom Design-Plugin aufgerufenen Slots.</p>
                            <?php foreach ($this->allowed_template_contexts() as $tpl_context) : ?>
                                <?php
                                $tpl_rule = isset($template_rules_for_form[$tpl_context]) && is_array($template_rules_for_form[$tpl_context]) ? $template_rules_for_form[$tpl_context] : array();
                                $tpl_label = isset($tpl_rule['label']) ? (string) $tpl_rule['label'] : $tpl_context;
                                $tpl_slots = !empty($tpl_rule['affiliate_slots']) && is_array($tpl_rule['affiliate_slots']) ? array_map('sanitize_key', $tpl_rule['affiliate_slots']) : array();
                                ?>
                                <fieldset style="margin:10px 0 12px;padding:10px;border:1px solid #dcdcde;max-width:760px;">
                                    <legend><strong><?php echo esc_html($tpl_label); ?></strong></legend>
                                    <?php foreach ($template_affiliate_slot_options as $tpl_slot_key => $tpl_slot_label) : ?>
                                        <label style="display:inline-block;min-width:220px;margin:2px 0;"><input type="checkbox" name="ppar_template_affiliate_slots[<?php echo esc_attr($tpl_context); ?>][]" value="<?php echo esc_attr($tpl_slot_key); ?>" <?php checked(in_array($tpl_slot_key, $tpl_slots, true)); ?>> <?php echo esc_html($tpl_slot_label); ?></label>
                                    <?php endforeach; ?>
                                </fieldset>
                            <?php endforeach; ?>
                        </td>
                    </tr>
                    <tr>
                        <th scope="row">Debug-Kommentare</th>
                        <td>
                            <label><input type="checkbox" name="ppar_debug" value="1" <?php checked($debug); ?>> Für Administratoren aktivieren</label>
                            <p class="description">Fügt unsichtbare HTML-Kommentare mit Matching-Status aus. Nur für eingeloggte Admins sichtbar.</p>
                        </td>
                    </tr>
                </table>

                <h2>3. Kategorie-/Archiv-Ausgabe</h2>
                <table class="form-table" role="presentation">
                    <tr>
                        <th scope="row">Kategorie-Ausgabe aktivieren</th>
                        <td>
                            <label><input type="checkbox" name="ppar_category_enabled" value="1" <?php checked($category_enabled); ?>> Aktiv</label>
                            <p class="description">Wenn aktiv, kann auf Kategoriearchiven am Ende der Beitragsliste ein passender Affiliate-Container erscheinen. Es werden keine Beiträge verändert.</p>
                        </td>
                    </tr>
                    <tr>
                        <th scope="row">Automatische Kategorie-Slots</th>
                        <td>
                            <label><input type="checkbox" name="ppar_category_slots[]" value="category_recommendation" <?php checked(in_array('category_recommendation', $category_slots, true)); ?>> category_recommendation Kategoriearchiv unten</label>
                        </td>
                    </tr>
                </table>

                <h2>4. Affiliate-Gruppen und Banner</h2>
                <p><strong>Hauptbedienung:</strong> Gruppen definieren Themen/Unterthemen. Banner werden passenden Slots und Suchintentionen zugeordnet. Das ist allgemeingültig und nicht pferdespezifisch.</p>
                <p class="description">Aktive Gruppen: <?php echo esc_html((string) count($active_groups)); ?> / Gesamtgruppen: <?php echo esc_html((string) count($groups)); ?>.</p>
                <?php
                $admin_groups = $groups;
                $admin_groups[] = array(
                    'id' => '', 'label' => '', 'active' => false, 'match_slugs' => array(), 'match_keywords' => array(), 'banners' => array()
                );
                foreach ($admin_groups as $g_index => $group) :
                    $is_new_group = empty($group['id']) && empty($group['label']);
                    $banners = isset($group['banners']) && is_array($group['banners']) ? $group['banners'] : array();
                    $banners[] = array('id' => '', 'label' => 'Anzeige', 'active' => false, 'mode' => 'image_link', 'slots' => array(), 'intent' => array(), 'priority' => 10, 'match_slugs' => array(), 'match_keywords' => array(), 'url' => '', 'subid_param' => '', 'image_url' => '', 'title' => '', 'description' => '', 'button_text' => 'Zum Angebot', 'html' => '');
                    ?>
                    <div id="ppar-group-<?php echo esc_attr((string) $g_index); ?>" style="background:#fff;border:1px solid #ccd0d4;border-radius:8px;padding:16px;margin:14px 0;">
                        <h3 style="margin-top:0;"><?php echo $is_new_group ? 'Neue Affiliate-Gruppe' : 'Affiliate-Gruppe: ' . esc_html((string) ($group['label'] ?? $group['id'])); ?></h3>
                        <table class="form-table" role="presentation">
                            <tr>
                                <th scope="row">Gruppe aktiv</th>
                                <td><label><input type="checkbox" name="ppar_groups_form[<?php echo esc_attr((string) $g_index); ?>][active]" value="1" <?php checked(!empty($group['active'])); ?>> Aktiv</label></td>
                            </tr>
                            <tr>
                                <th scope="row">Gruppen-ID</th>
                                <td><input type="text" class="regular-text" name="ppar_groups_form[<?php echo esc_attr((string) $g_index); ?>][id]" value="<?php echo esc_attr((string) ($group['id'] ?? '')); ?>" placeholder="z-b-produktgruppe"><p class="description">Technische ID, klein geschrieben, ohne Leerzeichen. Beispiel: gartenmoebel, akku_schrauber, pferdefutter.</p></td>
                            </tr>
                            <tr>
                                <th scope="row">Anzeigename</th>
                                <td><input type="text" class="regular-text" name="ppar_groups_form[<?php echo esc_attr((string) $g_index); ?>][label]" value="<?php echo esc_attr((string) ($group['label'] ?? '')); ?>"></td>
                            </tr>
                            <tr>
                                <th scope="row">Matching-Modus</th>
                                <td>
                                    <?php $group_match_mode = isset($group['match_mode']) ? sanitize_key((string) $group['match_mode']) : 'auto'; ?>
                                    <select name="ppar_groups_form[<?php echo esc_attr((string) $g_index); ?>][match_mode]">
                                        <option value="auto" <?php selected($group_match_mode, 'auto'); ?>>Automatisch: Slug + Keyword</option>
                                        <option value="exact_slug" <?php selected($group_match_mode, 'exact_slug'); ?>>Eng: nur exakter Slug</option>
                                        <option value="keyword" <?php selected($group_match_mode, 'keyword'); ?>>Breit: Keyword-Matching</option>
                                        <option value="fallback" <?php selected($group_match_mode, 'fallback'); ?>>Fallback: nur wenn nichts Spezifisches passt</option>
                                    </select>
                                    <p class="description">Für Tausende Beiträge: zuerst Gruppen breit automatisieren, Spezialgruppen eng stellen, Fallback nur als letzte Reserve verwenden.</p>
                                </td>
                            </tr>
                            <tr>
                                <th scope="row">Workflow-Status</th>
                                <td>
                                    <?php $group_workflow = isset($group['workflow_status']) ? sanitize_key((string) $group['workflow_status']) : 'offen'; ?>
                                    <select name="ppar_groups_form[<?php echo esc_attr((string) $g_index); ?>][workflow_status]">
                                        <option value="offen" <?php selected($group_workflow, 'offen'); ?>>offen</option>
                                        <option value="geprueft" <?php selected($group_workflow, 'geprueft'); ?>>geprüft</option>
                                        <option value="ignorieren" <?php selected($group_workflow, 'ignorieren'); ?>>ignorieren</option>
                                        <option value="fehler" <?php selected($group_workflow, 'fehler'); ?>>Fehler</option>
                                    </select>
                                    <label style="margin-left:16px;"><input type="checkbox" name="ppar_groups_form[<?php echo esc_attr((string) $g_index); ?>][duplicate_group]" value="1"> Gruppe beim Speichern duplizieren</label>
                                    <p class="description">Duplizieren erzeugt eine Kopie mit neuer ID und deaktiviertem Status. Das ist für ähnliche Produktgruppen gedacht.</p>
                                </td>
                            </tr>
                            <tr>
                                <th scope="row">Workflow-Notiz</th>
                                <td><textarea class="large-text" rows="2" name="ppar_groups_form[<?php echo esc_attr((string) $g_index); ?>][workflow_note]" placeholder="z. B. echte Partnerlinks fehlen noch, geprüft am Datum, nur eng matchen"><?php echo esc_textarea((string) ($group['workflow_note'] ?? '')); ?></textarea></td>
                            </tr>
                            <tr>
                                <th scope="row">Passende Slugs</th>
                                <td><textarea class="large-text code" rows="2" name="ppar_groups_form[<?php echo esc_attr((string) $g_index); ?>][match_slugs]"><?php echo esc_textarea($this->array_to_admin_list($group['match_slugs'] ?? array())); ?></textarea><p class="description">Kommagetrennt oder zeilenweise. Diese Slugs verbinden WordPress-Struktur mit Affiliate-Gruppe.</p></td>
                            </tr>
                            <tr>
                                <th scope="row">Passende Keywords</th>
                                <td><textarea class="large-text" rows="2" name="ppar_groups_form[<?php echo esc_attr((string) $g_index); ?>][match_keywords]"><?php echo esc_textarea($this->array_to_admin_list($group['match_keywords'] ?? array())); ?></textarea></td>
                            </tr>
                        </table>

                        <h4>Banner/Angebote dieser Gruppe</h4>
                        <?php foreach ($banners as $b_index => $banner) : ?>
                            <div style="border:1px solid #e2e4e7;border-radius:6px;padding:12px;margin:10px 0;background:#f8f9fa;">
                                <strong><?php echo empty($banner['id']) ? 'Neues Banner' : 'Banner: ' . esc_html((string) $banner['id']); ?></strong>
                                <table class="form-table" role="presentation">
                                    <tr>
                                        <th scope="row">Banner aktiv</th>
                                        <td><label><input type="checkbox" name="ppar_groups_form[<?php echo esc_attr((string) $g_index); ?>][banners][<?php echo esc_attr((string) $b_index); ?>][active]" value="1" <?php checked(!empty($banner['active'])); ?>> Aktiv</label></td>
                                    </tr>
                                    <tr>
                                        <th scope="row">Banner-ID / Label</th>
                                        <td>
                                            <input type="text" name="ppar_groups_form[<?php echo esc_attr((string) $g_index); ?>][banners][<?php echo esc_attr((string) $b_index); ?>][id]" value="<?php echo esc_attr((string) ($banner['id'] ?? '')); ?>" placeholder="angebot_1">
                                            <input type="text" name="ppar_groups_form[<?php echo esc_attr((string) $g_index); ?>][banners][<?php echo esc_attr((string) $b_index); ?>][label]" value="<?php echo esc_attr((string) ($banner['label'] ?? 'Anzeige')); ?>" placeholder="Anzeige">
                                        </td>
                                    </tr>
                                    <tr>
                                        <th scope="row">Ausgabeart</th>
                                        <td>
                                            <select name="ppar_groups_form[<?php echo esc_attr((string) $g_index); ?>][banners][<?php echo esc_attr((string) $b_index); ?>][mode]">
                                                <option value="image_link" <?php selected(($banner['mode'] ?? 'image_link'), 'image_link'); ?>>Bild/Text-Link</option>
                                                <option value="html" <?php selected(($banner['mode'] ?? 'image_link'), 'html'); ?>>HTML-Banner</option>
                                            </select>
                                            <label style="margin-left:16px;">Priorität <input type="number" style="width:80px;" name="ppar_groups_form[<?php echo esc_attr((string) $g_index); ?>][banners][<?php echo esc_attr((string) $b_index); ?>][priority]" value="<?php echo esc_attr((string) (int) ($banner['priority'] ?? 10)); ?>"></label>
                                        </td>
                                    </tr>
                                    <tr>
                                        <th scope="row">Slots</th>
                                        <td>
                                            <?php $banner_slots = isset($banner['slots']) && is_array($banner['slots']) ? array_map('sanitize_key', $banner['slots']) : array(); ?>
                                            <?php foreach ($slot_options as $slot_key => $slot_label) : ?>
                                                <label style="display:inline-block;min-width:210px;margin:2px 0;"><input type="checkbox" name="ppar_groups_form[<?php echo esc_attr((string) $g_index); ?>][banners][<?php echo esc_attr((string) $b_index); ?>][slots][]" value="<?php echo esc_attr($slot_key); ?>" <?php checked(in_array($slot_key, $banner_slots, true)); ?>> <?php echo esc_html($slot_label); ?></label>
                                            <?php endforeach; ?>
                                        </td>
                                    </tr>
                                    <tr>
                                        <th scope="row">Suchintention</th>
                                        <td>
                                            <?php $banner_intents = isset($banner['intent']) && is_array($banner['intent']) ? array_map('sanitize_key', $banner['intent']) : array(); ?>
                                            <?php foreach ($intent_options as $intent_key => $intent_label) : ?>
                                                <label style="display:inline-block;min-width:210px;margin:2px 0;"><input type="checkbox" name="ppar_groups_form[<?php echo esc_attr((string) $g_index); ?>][banners][<?php echo esc_attr((string) $b_index); ?>][intent][]" value="<?php echo esc_attr($intent_key); ?>" <?php checked(in_array($intent_key, $banner_intents, true)); ?>> <?php echo esc_html($intent_label); ?></label>
                                            <?php endforeach; ?>
                                        </td>
                                    </tr>
                                    <tr>
                                        <th scope="row">Banner-Matching</th>
                                        <td>
                                            <textarea class="large-text code" rows="2" name="ppar_groups_form[<?php echo esc_attr((string) $g_index); ?>][banners][<?php echo esc_attr((string) $b_index); ?>][match_slugs]" placeholder="optionale Slugs"><?php echo esc_textarea($this->array_to_admin_list($banner['match_slugs'] ?? array())); ?></textarea>
                                            <textarea class="large-text" rows="2" name="ppar_groups_form[<?php echo esc_attr((string) $g_index); ?>][banners][<?php echo esc_attr((string) $b_index); ?>][match_keywords]" placeholder="optionale Keywords"><?php echo esc_textarea($this->array_to_admin_list($banner['match_keywords'] ?? array())); ?></textarea>
                                        </td>
                                    </tr>
                                    <tr>
                                        <th scope="row">Link/Bild/Text</th>
                                        <td>
                                            <input type="url" class="large-text" name="ppar_groups_form[<?php echo esc_attr((string) $g_index); ?>][banners][<?php echo esc_attr((string) $b_index); ?>][url]" value="<?php echo esc_attr((string) ($banner['url'] ?? '')); ?>" placeholder="Affiliate-Link, Tokens erlaubt: {subid}, {post_id}, {category_slug}">
                                            <input type="text" class="regular-text" name="ppar_groups_form[<?php echo esc_attr((string) $g_index); ?>][banners][<?php echo esc_attr((string) $b_index); ?>][subid_param]" value="<?php echo esc_attr((string) ($banner['subid_param'] ?? '')); ?>" placeholder="SubID-Parameter optional">
                                            <input type="url" class="large-text" name="ppar_groups_form[<?php echo esc_attr((string) $g_index); ?>][banners][<?php echo esc_attr((string) $b_index); ?>][image_url]" value="<?php echo esc_attr((string) ($banner['image_url'] ?? '')); ?>" placeholder="Bild-URL optional">
                                            <input type="text" class="large-text" name="ppar_groups_form[<?php echo esc_attr((string) $g_index); ?>][banners][<?php echo esc_attr((string) $b_index); ?>][title]" value="<?php echo esc_attr((string) ($banner['title'] ?? '')); ?>" placeholder="Titel">
                                            <textarea class="large-text" rows="2" name="ppar_groups_form[<?php echo esc_attr((string) $g_index); ?>][banners][<?php echo esc_attr((string) $b_index); ?>][description]" placeholder="Beschreibung"><?php echo esc_textarea((string) ($banner['description'] ?? '')); ?></textarea>
                                            <input type="text" class="regular-text" name="ppar_groups_form[<?php echo esc_attr((string) $g_index); ?>][banners][<?php echo esc_attr((string) $b_index); ?>][button_text]" value="<?php echo esc_attr((string) ($banner['button_text'] ?? 'Zum Angebot')); ?>" placeholder="Buttontext">
                                        </td>
                                    </tr>
                                    <tr>
                                        <th scope="row">HTML-Banner</th>
                                        <td><textarea class="large-text code" rows="3" name="ppar_groups_form[<?php echo esc_attr((string) $g_index); ?>][banners][<?php echo esc_attr((string) $b_index); ?>][html]" placeholder="Nur für Ausgabeart HTML-Banner"><?php echo esc_textarea((string) ($banner['html'] ?? '')); ?></textarea></td>
                                    </tr>
                                </table>
                            </div>
                        <?php endforeach; ?>
                    </div>
                <?php endforeach; ?>

                <h2>5. Design-Grundregeln</h2>
                <p>Allgemeine, bildunabhängige Grundregeln. Diese bleiben JSON-Expertenmodus, weil sie selten geändert werden.</p>
                <textarea name="ppar_design_rules_json" rows="14" class="large-text code" spellcheck="false"><?php echo esc_textarea($design_rules_json); ?></textarea>

                <h2>6. Template-Regeln</h2>
                <p>Steuert Startseite, Haupt-Hubs, Bereichs-Hubs und Produktseiten. Der einzelne Begriff <code>Alle</code> bleibt verboten.</p>
                <textarea name="ppar_template_rules_json" rows="30" class="large-text code" spellcheck="false"><?php echo esc_textarea($template_rules_json); ?></textarea>

                <details style="margin:18px 0;">
                    <summary><strong>Expertenmodus: Affiliate-Gruppen als JSON anzeigen/importieren</strong></summary>
                    <p class="description">Nur verwenden, wenn bewusst JSON importiert werden soll. Das Formular oben bleibt Hauptbedienung.</p>
                    <textarea name="ppar_groups_json" rows="22" class="large-text code" spellcheck="false"><?php echo esc_textarea($groups_json); ?></textarea>
                    <h3>JSON-Beispiel Affiliate</h3>
                    <pre style="background:#fff;border:1px solid #ccd0d4;padding:12px;overflow:auto;max-height:260px;"><?php echo esc_html(self::example_minimal_json()); ?></pre>
                </details>

                <h2>7. Shortcodes</h2>
                <p><code>[affiliate_portal_slot type="post_mid_content" intent="primary_product"]</code></p>
                <p><code>[pp_affiliate_slot type="mid_content" intent="primary_product"]</code> (Legacy kompatibel)</p>
                <p><code>[pp_affiliate_slot type="bottom_recommendation" group="pferdefutter"]</code></p>
                <p><code>[pp_portal_overview]</code> oder <code>[pp_portal_overview context="haupt_hub_ebene_1" part="full"]</code></p>

                <?php submit_button('Einstellungen speichern'); ?>
            </form>
        </div>
        <?php
    }

    private function array_to_admin_list($value) {
        if (!is_array($value)) {
            return '';
        }
        $clean = array();
        foreach ($value as $item) {
            $item = trim((string) $item);
            if ($item !== '') {
                $clean[] = $item;
            }
        }
        return implode("\n", $clean);
    }

    private function admin_list_to_array($value, $keys_only = false) {
        $value = (string) $value;
        $parts = preg_split('/[\r\n,]+/', $value);
        $out = array();
        foreach ($parts as $part) {
            $part = trim((string) $part);
            if ($part === '') {
                continue;
            }
            $out[] = $keys_only ? sanitize_key($part) : sanitize_text_field($part);
        }
        return array_values(array_unique($out));
    }

    private function build_groups_from_admin_form($posted_groups) {
        if (!is_array($posted_groups)) {
            return array();
        }

        $allowed_slots = array('post_inline_banner', 'post_bottom_products', 'post_after_intro', 'post_mid_content', 'post_bottom_recommendation', 'hub_top_cta', 'hub_after_cards', 'hub_grid_card', 'hub_mid_banner', 'category_recommendation', 'product_after_category_tiles', 'anzeigenmarkt_top_banner', 'journal_banner', 'journal_product_1', 'journal_product_2', 'journal_product_3', 'top_info', 'mid_content', 'bottom_recommendation');
        $allowed_intents = array('soft_hint', 'primary_product', 'fallback');
        $out = array();
        $used_group_ids = array();

        foreach ($posted_groups as $group) {
            if (!is_array($group)) {
                continue;
            }
            $id = isset($group['id']) ? sanitize_key(wp_unslash($group['id'])) : '';
            $label = isset($group['label']) ? sanitize_text_field(wp_unslash($group['label'])) : '';
            if ($id === '' && $label !== '') {
                $id = sanitize_key($label);
            }
            if ($id === '' || isset($used_group_ids[$id])) {
                continue;
            }
            $used_group_ids[$id] = true;

            $banners_out = array();
            $used_banner_ids = array();
            $posted_banners = isset($group['banners']) && is_array($group['banners']) ? $group['banners'] : array();
            foreach ($posted_banners as $banner) {
                if (!is_array($banner)) {
                    continue;
                }
                $banner_id = isset($banner['id']) ? sanitize_key(wp_unslash($banner['id'])) : '';
                $banner_title = isset($banner['title']) ? sanitize_text_field(wp_unslash($banner['title'])) : '';
                if ($banner_id === '' && $banner_title !== '') {
                    $banner_id = sanitize_key($banner_title);
                }
                if ($banner_id === '' || isset($used_banner_ids[$banner_id])) {
                    continue;
                }
                $used_banner_ids[$banner_id] = true;

                $slots = isset($banner['slots']) && is_array($banner['slots']) ? array_map('sanitize_key', wp_unslash($banner['slots'])) : array();
                $slots = array_values(array_intersect($slots, $allowed_slots));
                if (empty($slots)) {
                    $slots = array('post_bottom_recommendation');
                }

                $intents = isset($banner['intent']) && is_array($banner['intent']) ? array_map('sanitize_key', wp_unslash($banner['intent'])) : array();
                $intents = array_values(array_intersect($intents, $allowed_intents));
                if (empty($intents)) {
                    $intents = array('primary_product');
                }

                $mode = isset($banner['mode']) ? sanitize_key(wp_unslash($banner['mode'])) : 'image_link';
                if (!in_array($mode, array('image_link', 'html'), true)) {
                    $mode = 'image_link';
                }

                $banners_out[] = array(
                    'id' => $banner_id,
                    'label' => isset($banner['label']) ? sanitize_text_field(wp_unslash($banner['label'])) : 'Anzeige',
                    'active' => !empty($banner['active']),
                    'mode' => $mode,
                    'slots' => $slots,
                    'intent' => $intents,
                    'priority' => isset($banner['priority']) ? (int) $banner['priority'] : 10,
                    'match_slugs' => $this->admin_list_to_array(isset($banner['match_slugs']) ? wp_unslash($banner['match_slugs']) : '', true),
                    'match_keywords' => $this->admin_list_to_array(isset($banner['match_keywords']) ? wp_unslash($banner['match_keywords']) : '', false),
                    'url' => isset($banner['url']) ? esc_url_raw(trim((string) wp_unslash($banner['url']))) : '',
                    'subid_param' => isset($banner['subid_param']) ? sanitize_key(wp_unslash($banner['subid_param'])) : '',
                    'image_url' => isset($banner['image_url']) ? esc_url_raw(trim((string) wp_unslash($banner['image_url']))) : '',
                    'title' => $banner_title,
                    'description' => isset($banner['description']) ? sanitize_textarea_field(wp_unslash($banner['description'])) : '',
                    'button_text' => isset($banner['button_text']) ? sanitize_text_field(wp_unslash($banner['button_text'])) : '',
                    'html' => isset($banner['html']) ? $this->filter_allowed_banner_html(wp_unslash($banner['html'])) : '',
                );
            }

            $match_mode = isset($group['match_mode']) ? sanitize_key(wp_unslash($group['match_mode'])) : 'auto';
            if (!in_array($match_mode, $this->allowed_match_modes(), true)) {
                $match_mode = 'auto';
            }
            $workflow_status = isset($group['workflow_status']) ? sanitize_key(wp_unslash($group['workflow_status'])) : 'offen';
            if (!in_array($workflow_status, $this->allowed_workflow_statuses(), true)) {
                $workflow_status = 'offen';
            }
            $group_out = array(
                'id' => $id,
                'label' => $label !== '' ? $label : $id,
                'active' => !empty($group['active']),
                'match_mode' => $match_mode,
                'workflow_status' => $workflow_status,
                'workflow_note' => isset($group['workflow_note']) ? sanitize_textarea_field(wp_unslash($group['workflow_note'])) : '',
                'match_slugs' => $this->admin_list_to_array(isset($group['match_slugs']) ? wp_unslash($group['match_slugs']) : '', true),
                'match_keywords' => $this->admin_list_to_array(isset($group['match_keywords']) ? wp_unslash($group['match_keywords']) : '', false),
                'banners' => $banners_out,
            );
            $out[] = $group_out;
            if (!empty($group['duplicate_group'])) {
                $copy = $group_out;
                $base_id = sanitize_key($id . '_kopie');
                $copy_id = $base_id;
                $i = 2;
                while (isset($used_group_ids[$copy_id])) {
                    $copy_id = $base_id . '_' . $i;
                    $i++;
                }
                $used_group_ids[$copy_id] = true;
                $copy['id'] = $copy_id;
                $copy['label'] = $copy['label'] . ' Kopie';
                $copy['active'] = false;
                $copy['workflow_status'] = 'offen';
                $copy['workflow_note'] = 'Duplizierte Gruppe - vor Aktivierung prüfen.';
                $out[] = $copy;
            }
        }

        return $out;
    }

    public function handle_save_settings() {
        if (!current_user_can('manage_options')) {
            wp_die('Keine Berechtigung.');
        }
        check_admin_referer('ppar_save_settings', 'ppar_nonce');

        $enabled = isset($_POST['ppar_enabled']) ? '1' : '0';
        $template_enabled = isset($_POST['ppar_template_enabled']) ? '1' : '0';
        $debug = isset($_POST['ppar_debug']) ? '1' : '0';
        $category_enabled = isset($_POST['ppar_category_enabled']) ? '1' : '0';
        $category_slots = isset($_POST['ppar_category_slots']) && is_array($_POST['ppar_category_slots']) ? array_map('sanitize_key', wp_unslash($_POST['ppar_category_slots'])) : array();
        $category_slots = array_values(array_intersect($category_slots, $this->allowed_category_slots()));
        $auto_slots = isset($_POST['ppar_auto_slots']) && is_array($_POST['ppar_auto_slots']) ? array_map('sanitize_key', wp_unslash($_POST['ppar_auto_slots'])) : array();
        $auto_slots = array_values(array_intersect($auto_slots, $this->allowed_auto_slots()));
        $template_contexts = isset($_POST['ppar_template_contexts']) && is_array($_POST['ppar_template_contexts']) ? array_map('sanitize_key', wp_unslash($_POST['ppar_template_contexts'])) : array();
        $template_contexts = array_values(array_intersect($template_contexts, $this->allowed_template_contexts()));
        $disclosure = isset($_POST['ppar_disclosure']) ? sanitize_textarea_field(wp_unslash($_POST['ppar_disclosure'])) : '';
        $article_hybrid_raw = isset($_POST['ppar_article_hybrid']) && is_array($_POST['ppar_article_hybrid']) ? wp_unslash($_POST['ppar_article_hybrid']) : array();
        $article_hybrid = array(
            'enabled' => !empty($article_hybrid_raw['enabled']),
        );

        $groups_from_form = isset($_POST['ppar_groups_form_submitted']) && isset($_POST['ppar_groups_form']);
        if ($groups_from_form) {
            $decoded = $this->build_groups_from_admin_form(wp_unslash($_POST['ppar_groups_form']));
        } else {
            $groups_json = isset($_POST['ppar_groups_json']) ? wp_unslash($_POST['ppar_groups_json']) : '[]';
            $decoded = json_decode($groups_json, true);
            if (!is_array($decoded)) {
                wp_safe_redirect(add_query_arg('ppar_error', 'json', wp_get_referer() ?: admin_url('admin.php?page=pferde-affiliate-router')));
                exit;
            }
        }

        $template_rules_json = isset($_POST['ppar_template_rules_json']) ? wp_unslash($_POST['ppar_template_rules_json']) : '{}';
        $design_rules_json = isset($_POST['ppar_design_rules_json']) ? wp_unslash($_POST['ppar_design_rules_json']) : '{}';

        $design_decoded = json_decode($design_rules_json, true);
        if (!is_array($design_decoded)) {
            wp_safe_redirect(add_query_arg('ppar_error', 'design_json', wp_get_referer() ?: admin_url('admin.php?page=pferde-affiliate-router')));
            exit;
        }

        $template_decoded = json_decode($template_rules_json, true);
        if (!is_array($template_decoded)) {
            wp_safe_redirect(add_query_arg('ppar_error', 'template_json', wp_get_referer() ?: admin_url('admin.php?page=pferde-affiliate-router')));
            exit;
        }
        $template_slots_from_form = isset($_POST['ppar_template_affiliate_slots']) && is_array($_POST['ppar_template_affiliate_slots']) ? wp_unslash($_POST['ppar_template_affiliate_slots']) : array();
        foreach ($this->allowed_template_contexts() as $tpl_context) {
            if (!isset($template_decoded[$tpl_context]) || !is_array($template_decoded[$tpl_context])) {
                $template_decoded[$tpl_context] = array('label' => $tpl_context, 'active' => true);
            }
            $raw_tpl_slots = isset($template_slots_from_form[$tpl_context]) && is_array($template_slots_from_form[$tpl_context]) ? array_map('sanitize_key', $template_slots_from_form[$tpl_context]) : array();
            $template_decoded[$tpl_context]['affiliate_slots'] = array_values(array_intersect($raw_tpl_slots, $this->allowed_template_affiliate_placements()));
        }

        $template_validation = $this->validate_template_rules($template_decoded);
        if ($template_validation === 'word_alle') {
            wp_safe_redirect(add_query_arg('ppar_error', 'template_word_alle', wp_get_referer() ?: admin_url('admin.php?page=pferde-affiliate-router')));
            exit;
        }
        if ($template_validation !== true) {
            wp_safe_redirect(add_query_arg('ppar_error', 'template_json', wp_get_referer() ?: admin_url('admin.php?page=pferde-affiliate-router')));
            exit;
        }

        $pretty_json = wp_json_encode($decoded, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
        $pretty_template_json = wp_json_encode($template_decoded, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
        $pretty_design_json = wp_json_encode($design_decoded, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);

        update_option(self::OPTION_ENABLED, $enabled, false);
        update_option(self::OPTION_TEMPLATE_ENABLED, $template_enabled, false);
        update_option(self::OPTION_CATEGORY_ENABLED, $category_enabled, false);
        update_option(self::OPTION_DEBUG, $debug, false);
        update_option(self::OPTION_AUTO_SLOTS, $auto_slots, false);
        update_option(self::OPTION_TEMPLATE_CONTEXTS, $template_contexts, false);
        update_option(self::OPTION_CATEGORY_SLOTS, $category_slots, false);
        update_option(self::OPTION_DISCLOSURE, $disclosure, false);
        update_option(self::OPTION_ARTICLE_HYBRID, $article_hybrid, false);
        update_option(self::OPTION_GROUPS_JSON, $pretty_json, false);
        update_option(self::OPTION_TEMPLATE_RULES_JSON, $pretty_template_json, false);
        update_option(self::OPTION_DESIGN_RULES_JSON, $pretty_design_json, false);

        wp_safe_redirect(add_query_arg('ppar_saved', '1', admin_url('admin.php?page=pferde-affiliate-router')));
        exit;
    }

    public static function default_groups_json() {
        return wp_json_encode(array(
            array(
                'id' => 'pferdefutter',
                'label' => 'Pferdefutter',
                'active' => false,
                'match_mode' => 'auto',
                'workflow_status' => 'offen',
                'workflow_note' => 'Beispielgruppe; vor produktiver Nutzung an Projektprofil anpassen.',
                'match_slugs' => array(
                    'pferdefutter',
                    'mineralfutter-pferde',
                    'mash-pferde',
                    'heucobs-pferde',
                    'kraftfutter-pferde',
                    'ergaenzungsfutter-pferde',
                    'seniorenfutter-pferde'
                ),
                'match_keywords' => array(
                    'pferdefutter',
                    'mineralfutter',
                    'mash',
                    'heucobs',
                    'kraftfutter',
                    'ergänzungsfutter',
                    'seniorenfutter'
                ),
                'banners' => array(
                    array(
                        'id' => 'pferdefutter_beispiel_inaktiv',
                        'label' => 'Anzeige',
                        'active' => false,
                        'mode' => 'image_link',
                        'slots' => array('bottom_recommendation', 'mid_content', 'post_bottom_recommendation', 'post_mid_content', 'hub_after_cards', 'category_recommendation'),
                        'intent' => array('primary_product', 'fallback'),
                        'priority' => 10,
                        'match_slugs' => array('pferdefutter'),
                        'match_keywords' => array('pferdefutter'),
                        'url' => 'https://example.com/?ref={subid}',
                        'subid_param' => '',
                        'image_url' => '',
                        'title' => 'Pferdefutter online ansehen',
                        'description' => 'Beispiel ist inaktiv. Hier später echten Awin-/ADCELL-/Shop-Link eintragen.',
                        'button_text' => 'Zum Shop'
                    )
                )
            )
        ), JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
    }

    public static function default_template_rules_json() {
        return wp_json_encode(array(
            'startseite' => array(
                'label' => 'Startseite',
                'active' => true,
                'source' => 'top_level_pages',
                'insert_position' => 'after_intro',
                'selected_limit' => 8,
                'show_selected' => true,
                'show_hint' => true,
                'show_full_overview' => true,
                'selected_heading' => 'Beliebte Themen im Pferdeportal',
                'hint_heading' => 'Weitere Themen im Pferdeportal entdecken',
                'hint_text' => 'Die angezeigten Bereiche sind nur ein Einstieg. In der vollständigen Übersicht finden Sie alle Themen rund um Haltung, Ernährung, Ausrüstung, Pflege, Gesundheit und Training.',
                'button_text' => 'Alle Themenbereiche anzeigen',
                'button_anchor' => 'alle-themenbereiche',
                'full_heading' => 'Alle Themenbereiche im Überblick',
                'affiliate_slots' => array()
            ),
            'haupt_hub_ebene_1' => array(
                'label' => 'Haupt-Hub Ebene 1',
                'active' => true,
                'source' => 'child_pages',
                'insert_position' => 'after_intro',
                'selected_limit' => 8,
                'show_selected' => true,
                'show_hint' => true,
                'show_full_overview' => true,
                'selected_heading' => 'Beliebte Einstiege zu {thema}',
                'hint_heading' => 'Weitere Themen zu {thema}',
                'hint_text' => 'Die angezeigten Themen sind nur eine Auswahl. In der vollständigen Übersicht finden Sie alle Bereiche rund um {thema}.',
                'button_text' => 'Alle {thema}-Themen anzeigen',
                'button_anchor' => 'alle-themen',
                'full_heading' => 'Vollständige {thema}-Übersicht',
                'affiliate_slots' => array()
            ),
            'bereichs_hub_ebene_2' => array(
                'label' => 'Bereichs-Hub Ebene 2',
                'active' => true,
                'source' => 'child_pages',
                'insert_position' => 'after_intro',
                'selected_limit' => 8,
                'show_selected' => true,
                'show_hint' => true,
                'show_full_overview' => true,
                'selected_heading' => 'Beliebte Einstiege rund um {thema}',
                'hint_heading' => 'Mehr rund um {thema}',
                'hint_text' => 'Neben den beliebten Einstiegen gibt es weitere Ratgeber, Vergleiche und Fragen zu {thema}.',
                'button_text' => 'Alle Themen rund um {thema} anzeigen',
                'button_anchor' => 'alle-themen-rund-um-dieses-thema',
                'full_heading' => 'Alle Themen rund um {thema}',
                'affiliate_slots' => array()
            ),
            'produktseite_ebene_3' => array(
                'label' => 'Produktseite Ebene 3',
                'active' => true,
                'source' => 'child_pages_then_categories',
                'insert_position' => 'after_intro',
                'selected_limit' => 5,
                'show_selected' => true,
                'show_hint' => true,
                'show_full_overview' => true,
                'selected_heading' => '{thema}: beliebte Ratgeber',
                'hint_heading' => 'Alle Beiträge zu {thema}',
                'hint_text' => 'Hier finden Sie weitere Ratgeber, Fragen, Vergleiche und praktische Hinweise rund um {thema}.',
                'button_text' => 'Alle {thema}-Artikel anzeigen',
                'button_anchor' => 'alle-artikel-zum-thema',
                'full_heading' => 'Alle Beiträge zu {thema}',
                'affiliate_slots' => array()
            )
        ), JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
    }

    public static function default_design_rules_json() {
        return wp_json_encode(array(
            'system_principle' => 'Einheitliches, bildunabhängiges Grunddesign. Redaktionelle Bilder sind optional und nie Voraussetzung.',
            'editorial_images_required' => false,
            'affiliate_images_allowed' => true,
            'one_base_design_for_all_posts' => true,
            'card_show_description' => false,
            'card_description_words' => 14,
            'list_show_description' => false,
            'list_description_words' => 16,
            'selected_items_max_default' => 8,
            'overview_style' => 'compact_list',
            'affiliate_design_rule' => 'Design definiert feste Flächen; Affiliate-Router füllt nur passende aktive Flächen.',
            'empty_affiliate_slot_policy' => 'hide',
            'old_template_plugins_policy' => 'Nur eine Design-Instanz darf Startseite und Hubs final steuern.'
        ), JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
    }

    public static function example_minimal_json() {
        return wp_json_encode(array(
            array(
                'id' => 'pferdefutter',
                'label' => 'Pferdefutter',
                'active' => true,
                'match_slugs' => array('pferdefutter', 'mineralfutter-pferde', 'mash-pferde'),
                'match_keywords' => array('pferdefutter', 'mineralfutter', 'mash'),
                'banners' => array(
                    array(
                        'id' => 'mineralfutter_banner',
                        'label' => 'Anzeige',
                        'active' => true,
                        'mode' => 'image_link',
                        'slots' => array('post_mid_content', 'post_bottom_recommendation'),
                        'intent' => array('primary_product'),
                        'priority' => 50,
                        'match_slugs' => array('mineralfutter-pferde'),
                        'match_keywords' => array('mineralfutter'),
                        'url' => 'https://partnerlink.example/?clickref={subid}',
                        'subid_param' => '',
                        'image_url' => 'https://example.com/banner.jpg',
                        'title' => 'Mineralfutter für Pferde',
                        'description' => 'Passende Produkte im Partnershop ansehen.',
                        'button_text' => 'Zum Angebot'
                    )
                )
            )
        ), JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
    }
}

if (!function_exists('affiliate_portal_upsert_campaign')) {
    function affiliate_portal_upsert_campaign($data) {
        return Pferdeportal_Affiliate_Router::instance()->upsert_campaign_from_external($data);
    }
}

register_activation_hook(__FILE__, array('Pferdeportal_Affiliate_Router', 'activate'));
register_deactivation_hook(__FILE__, array('Pferdeportal_Affiliate_Router', 'deactivate'));

// Workflow V2 behält bewusst den live bekannten stabilen Pluginpfad
// `affiliate-portal-router/pferdeportal-affiliate-router.php`. Der Bootstrap
// startet weiterhin erst im normalen WordPress-Lauf; Aktivierung und eBay-
// Hintergrundprozesse bleiben voneinander getrennt.
Pferdeportal_Affiliate_Router::instance();
