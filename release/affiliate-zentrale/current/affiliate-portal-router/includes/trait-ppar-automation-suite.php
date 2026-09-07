<?php
if (!defined('ABSPATH')) {
    exit;
}

/**
 * Providerunabhängiger Automatisierungskern.
 *
 * - eine Providerquelle je Auftrag, kleine wiederaufnehmbare Arbeitspakete,
 * - Awin: Programmdaten, Offers und Enhanced-/CSV-Produktfeed,
 * - ADCELL: exakt konfigurierte CSV-Export-URL, paketweise und fail-closed,
 * - statische Creatives nur über offiziell dokumentierte Provider-API oder maschinenlesbaren Feed,
 * - many-to-many Zielkanten gegen den eingebetteten realen Portalbaum,
 * - automatische Slotvorschläge aus Typ und Abmessungen,
 * - fail-closed Materialisierung in bestehende, zunächst inaktive Kampagnen,
 * - keine Änderung an Design, HivePress oder anderen Plugins.
 */
trait PPAR_Automation_Suite_Trait {
    private function automation_edges_table() {
        global $wpdb;
        return $wpdb->prefix . 'ppar_target_edges';
    }

    private function automation_runs_table() {
        global $wpdb;
        return $wpdb->prefix . 'ppar_automation_runs';
    }

    private function automation_jobs_table() {
        global $wpdb;
        return $wpdb->prefix . 'ppar_automation_jobs';
    }

    public function maybe_install_automation_schema() {
        $installed = (string) get_option(self::OPTION_AUTOMATION_SCHEMA_VERSION, '0');
        if ($installed === self::AUTOMATION_SCHEMA_VERSION) {
            return;
        }
        require_once ABSPATH . 'wp-admin/includes/upgrade.php';
        global $wpdb;
        $charset = $wpdb->get_charset_collate();
        $edges = $this->automation_edges_table();
        $runs = $this->automation_runs_table();
        $jobs = $this->automation_jobs_table();
        dbDelta("CREATE TABLE {$edges} (
            id bigint(20) unsigned NOT NULL AUTO_INCREMENT,
            provider varchar(60) NOT NULL,
            partner_external_id varchar(191) NOT NULL DEFAULT '',
            asset_identity_hash char(64) NOT NULL,
            target_type varchar(30) NOT NULL,
            target_slug varchar(191) NOT NULL,
            target_path text NOT NULL,
            score int(10) unsigned NOT NULL DEFAULT 0,
            edge_status varchar(30) NOT NULL DEFAULT 'review',
            source varchar(60) NOT NULL DEFAULT 'automatic',
            updated_at bigint(20) unsigned NOT NULL DEFAULT 0,
            PRIMARY KEY (id),
            UNIQUE KEY asset_target (asset_identity_hash, target_type, target_slug),
            KEY provider_partner (provider(20), partner_external_id(100)),
            KEY target_lookup (target_type, target_slug(120), edge_status)
        ) {$charset};");
        dbDelta("CREATE TABLE {$runs} (
            id bigint(20) unsigned NOT NULL AUTO_INCREMENT,
            run_uuid char(36) NOT NULL,
            provider varchar(60) NOT NULL,
            partner_external_id varchar(191) NOT NULL DEFAULT '',
            operation varchar(60) NOT NULL,
            status varchar(30) NOT NULL,
            started_at bigint(20) unsigned NOT NULL DEFAULT 0,
            finished_at bigint(20) unsigned NOT NULL DEFAULT 0,
            imported int(10) unsigned NOT NULL DEFAULT 0,
            updated int(10) unsigned NOT NULL DEFAULT 0,
            unchanged int(10) unsigned NOT NULL DEFAULT 0,
            blocked int(10) unsigned NOT NULL DEFAULT 0,
            failed int(10) unsigned NOT NULL DEFAULT 0,
            message text NOT NULL,
            details longtext NULL,
            PRIMARY KEY (id),
            UNIQUE KEY run_uuid (run_uuid),
            KEY provider_partner (provider(20), partner_external_id(100), started_at)
        ) {$charset};");
        dbDelta("CREATE TABLE {$jobs} (
            id bigint(20) unsigned NOT NULL AUTO_INCREMENT,
            job_uuid char(36) NOT NULL,
            run_uuid char(36) NOT NULL,
            provider varchar(60) NOT NULL,
            partner_external_id varchar(191) NOT NULL DEFAULT '',
            stage varchar(30) NOT NULL DEFAULT 'programme',
            status varchar(30) NOT NULL DEFAULT 'queued',
            cursor_value bigint(20) unsigned NOT NULL DEFAULT 0,
            offer_page int(10) unsigned NOT NULL DEFAULT 1,
            retry_count int(10) unsigned NOT NULL DEFAULT 0,
            not_before bigint(20) unsigned NOT NULL DEFAULT 0,
            lock_token char(36) NOT NULL DEFAULT '',
            lock_expires_at bigint(20) unsigned NOT NULL DEFAULT 0,
            heartbeat_at bigint(20) unsigned NOT NULL DEFAULT 0,
            counts longtext NULL,
            details longtext NULL,
            message text NOT NULL,
            created_at bigint(20) unsigned NOT NULL DEFAULT 0,
            updated_at bigint(20) unsigned NOT NULL DEFAULT 0,
            finished_at bigint(20) unsigned NOT NULL DEFAULT 0,
            PRIMARY KEY (id),
            UNIQUE KEY job_uuid (job_uuid),
            KEY queue_lookup (status, not_before, id),
            KEY partner_open (provider(20), partner_external_id(100), status)
        ) {$charset};");
        update_option(self::OPTION_AUTOMATION_SCHEMA_VERSION, self::AUTOMATION_SCHEMA_VERSION, false);
    }

    public static function automation_settings_defaults() {
        return array(
            'enabled' => false,
            'schedule' => 'daily',
            'executor' => 'server_cron',
            'batch_size' => 500,
            'time_budget' => 20,
            'request_timeout' => 45,
        );
    }

    private function automation_settings() {
        $saved = get_option(self::OPTION_AUTOMATION_SETTINGS, array());
        $saved = is_array($saved) ? $saved : array();
        $merged = wp_parse_args($saved, self::automation_settings_defaults());
        return array(
            'enabled' => !empty($merged['enabled']),
            'schedule' => in_array((string) $merged['schedule'], array('daily','twicedaily'), true) ? (string) $merged['schedule'] : 'daily',
            'executor' => in_array((string) $merged['executor'], array('server_cron','wp_cron'), true) ? (string) $merged['executor'] : 'server_cron',
            'batch_size' => max(100, min(1000, absint($merged['batch_size']))),
            'time_budget' => max(10, min(25, absint($merged['time_budget']))),
            'request_timeout' => max(15, min(45, absint($merged['request_timeout']))),
        );
    }

    public function maybe_apply_automation_safety_upgrade() {
        $target = '4.0.0';
        if ((string) get_option(self::OPTION_AUTOMATION_SAFETY_VERSION, '') === $target) {
            return;
        }
        $settings = $this->automation_settings();
        $settings['enabled'] = false;
        $settings['executor'] = 'server_cron';
        $settings['batch_size'] = min(500, absint($settings['batch_size']));
        $settings['time_budget'] = min(20, absint($settings['time_budget']));
        $settings['request_timeout'] = min(45, absint($settings['request_timeout']));
        update_option(self::OPTION_AUTOMATION_SETTINGS, $settings, false);
        update_option(self::OPTION_AUTOMATION_CYCLE, array('remaining'=>0,'total'=>0,'started_at'=>0), false);
        if (function_exists('wp_clear_scheduled_hook')) {
            wp_clear_scheduled_hook(self::AUTOMATION_CRON_HOOK);
            wp_clear_scheduled_hook(self::AUTOMATION_WORKER_HOOK);
        }
        update_option(self::OPTION_AUTOMATION_SAFETY_VERSION, $target, false);
    }

    public function automation_cron_schedules($schedules) {
        if (!isset($schedules['ppar_five_minutes'])) {
            $schedules['ppar_five_minutes'] = array('interval'=>300, 'display'=>'Alle fünf Minuten');
        }
        return $schedules;
    }

    public function ensure_automation_schedule() {
        $settings = $this->automation_settings();
        $dispatch = wp_get_schedule(self::AUTOMATION_CRON_HOOK);
        $worker = wp_get_schedule(self::AUTOMATION_WORKER_HOOK);
        $use_wp_cron = !empty($settings['enabled']) && $settings['executor'] === 'wp_cron';
        if (!$use_wp_cron) {
            if ($dispatch) {
                wp_clear_scheduled_hook(self::AUTOMATION_CRON_HOOK);
            }
            if ($worker) {
                wp_clear_scheduled_hook(self::AUTOMATION_WORKER_HOOK);
            }
            return;
        }
        if ($dispatch !== $settings['schedule']) {
            wp_clear_scheduled_hook(self::AUTOMATION_CRON_HOOK);
            wp_schedule_event(time() + 300, $settings['schedule'], self::AUTOMATION_CRON_HOOK);
        }
        if ($worker !== 'ppar_five_minutes') {
            wp_clear_scheduled_hook(self::AUTOMATION_WORKER_HOOK);
            wp_schedule_event(time() + 300, 'ppar_five_minutes', self::AUTOMATION_WORKER_HOOK);
        }
    }

    public function reschedule_automation_cron($force = false) {
        if ($force) {
            wp_clear_scheduled_hook(self::AUTOMATION_CRON_HOOK);
            wp_clear_scheduled_hook(self::AUTOMATION_WORKER_HOOK);
        }
        $this->ensure_automation_schedule();
    }

    public function handle_automation_save_settings() {
        if (!current_user_can('manage_options')) {
            wp_die('Keine Berechtigung.');
        }
        check_admin_referer('ppar_automation_save_settings', 'ppar_automation_settings_nonce');
        $raw = isset($_POST['ppar_automation']) && is_array($_POST['ppar_automation']) ? wp_unslash($_POST['ppar_automation']) : array();
        $settings = array(
            'enabled' => !empty($raw['enabled']),
            'schedule' => in_array((string) ($raw['schedule'] ?? ''), array('daily','twicedaily'), true) ? (string) $raw['schedule'] : 'daily',
            'executor' => in_array((string) ($raw['executor'] ?? ''), array('server_cron','wp_cron'), true) ? (string) $raw['executor'] : 'server_cron',
            'batch_size' => max(100, min(1000, absint($raw['batch_size'] ?? 500))),
            'time_budget' => max(10, min(25, absint($raw['time_budget'] ?? 20))),
            'request_timeout' => max(15, min(45, absint($raw['request_timeout'] ?? 45))),
        );
        update_option(self::OPTION_AUTOMATION_SETTINGS, $settings, false);
        $this->reschedule_automation_cron(true);
        wp_safe_redirect(add_query_arg(array('page'=>'affiliate-portal-automation','ppar_auto'=>'settings_saved','ppar_message'=>rawurlencode('Automatisierungseinstellungen gespeichert.')), admin_url('admin.php')));
        exit;
    }

    private function automation_scheduled_partner_batch($snapshots, $cursor, $limit = 1) {
        $valid = array_values(array_filter((array) $snapshots, function ($snapshot) {
            return is_array($snapshot)
                && sanitize_key((string) ($snapshot['provider'] ?? '')) === 'awin'
                && absint($snapshot['external_id'] ?? 0) > 0
                && $this->awin_programme_gate_is_allowed(absint($snapshot['external_id'] ?? 0));
        }));
        usort($valid, static function ($a, $b) {
            return absint($a['external_id'] ?? 0) <=> absint($b['external_id'] ?? 0);
        });
        if (!$valid) {
            return array('ids'=>array(), 'next_cursor'=>0, 'total'=>0);
        }
        $total = count($valid);
        $cursor = absint($cursor) % $total;
        $id = absint($valid[$cursor]['external_id'] ?? 0);
        return array('ids'=>$id > 0 ? array($id) : array(), 'next_cursor'=>($cursor + 1) % $total, 'total'=>$total);
    }

    private function automation_scheduled_sources() {
        $sources = array();
        $awin = $this->network_settings('awin');
        if (!empty($awin['enabled'])) {
            foreach ($this->partner_intake_snapshots() as $snapshot) {
                if (!is_array($snapshot)
                    || sanitize_key((string) ($snapshot['provider'] ?? '')) !== 'awin'
                    || absint($snapshot['external_id'] ?? 0) <= 0
                    || !$this->awin_programme_gate_is_allowed(absint($snapshot['external_id'] ?? 0))) {
                    continue;
                }
                $sources[] = array(
                    'key' => 'awin:' . absint($snapshot['external_id']),
                    'provider' => 'awin',
                    'partner_external_id' => (string) absint($snapshot['external_id']),
                );
            }
        }
        $adcell = $this->network_settings('adcell');
        if (!empty($adcell['enabled']) && trim((string) ($adcell['csv_feed_url'] ?? '')) !== '') {
            $validated = $this->network_sync_validate_feed_url('adcell', (string) $adcell['csv_feed_url']);
            if (!is_wp_error($validated)) {
                $sources[] = array(
                    'key' => 'adcell:csv-feed',
                    'provider' => 'adcell',
                    'partner_external_id' => 'csv-feed',
                );
            }
        }
        $sources = apply_filters('ppar_affiliate_automation_scheduled_sources', $sources, $this->provider_registry(), self::PROVIDER_CONTRACT_VERSION);
        $sources = array_values(array_filter((array) $sources, function ($source) {
            if (!is_array($source)) { return false; }
            $provider = sanitize_key((string) ($source['provider'] ?? ''));
            return $provider !== ''
                && $this->provider_exists($provider)
                && $this->provider_supports($provider, 'automation')
                && trim((string) ($source['partner_external_id'] ?? '')) !== '';
        }));
        usort($sources, static function ($a, $b) {
            return strcmp((string) ($a['key'] ?? ''), (string) ($b['key'] ?? ''));
        });
        return $sources;
    }

    private function automation_scheduled_source_batch($sources, $cursor) {
        $sources = array_values(array_filter((array) $sources, function ($source) {
            if (!is_array($source)) { return false; }
            $provider = sanitize_key((string) ($source['provider'] ?? ''));
            return $provider !== ''
                && $this->provider_exists($provider)
                && $this->provider_supports($provider, 'automation')
                && trim((string) ($source['partner_external_id'] ?? '')) !== '';
        }));
        if (!$sources) {
            return array('source'=>array(), 'next_cursor'=>0, 'total'=>0);
        }
        $total = count($sources);
        $cursor = absint($cursor) % $total;
        return array(
            'source'=>$sources[$cursor],
            'next_cursor'=>($cursor + 1) % $total,
            'total'=>$total,
        );
    }

    private function automation_has_open_jobs() {
        global $wpdb;
        $table = $this->automation_jobs_table();
        return (bool) $wpdb->get_var("SELECT id FROM {$table} WHERE status IN ('queued','running','retry') LIMIT 1");
    }

    private function automation_cycle_state() {
        $state = get_option(self::OPTION_AUTOMATION_CYCLE, array());
        $state = is_array($state) ? $state : array();
        return array(
            'remaining'=>max(0, absint($state['remaining'] ?? 0)),
            'total'=>max(0, absint($state['total'] ?? 0)),
            'started_at'=>max(0, absint($state['started_at'] ?? 0)),
        );
    }

    private function automation_dispatch_due() {
        $cycle = $this->automation_cycle_state();
        if ($cycle['remaining'] > 0) {
            return true;
        }
        $settings = $this->automation_settings();
        $last = absint(get_option(self::OPTION_AUTOMATION_LAST_DISPATCH, 0));
        $interval = $settings['schedule'] === 'twicedaily' ? 12 * HOUR_IN_SECONDS : DAY_IN_SECONDS;
        return $last <= 0 || (time() - $last) >= $interval;
    }

    private function automation_dispatch_source($source, $manual = false) {
        $source = is_array($source) ? $source : array();
        $provider = sanitize_key((string) ($source['provider'] ?? ''));
        $partner_id = sanitize_text_field((string) ($source['partner_external_id'] ?? ''));
        if ($provider === '' || !$this->provider_exists($provider) || !$this->provider_supports($provider, 'automation')) {
            return new WP_Error('automation_provider_invalid', 'Provider ist nicht als Automatisierungsquelle registriert.');
        }
        if ($provider === 'awin') {
            return $this->automation_enqueue_awin_partner(absint($partner_id));
        }
        if ($provider === 'adcell') {
            return $this->automation_enqueue_adcell_feed();
        }
        if ($provider === 'ebay' && method_exists($this, 'run_ebay_sync')) {
            $summary = $this->run_ebay_sync((bool) $manual);
            return is_wp_error($summary) ? $summary : array('immediate'=>true,'provider'=>'ebay','summary'=>$summary);
        }
        $result = apply_filters('ppar_affiliate_automation_dispatch', null, $provider, $source, (bool) $manual, self::PROVIDER_CONTRACT_VERSION);
        return $result === null ? new WP_Error('automation_provider_adapter_missing', 'Für diesen Provider ist kein Automatisierungsadapter registriert.') : $result;
    }

    public function run_scheduled_partner_sync($external_executor = false) {
        $settings = $this->automation_settings();
        $expected_executor = $external_executor ? 'server_cron' : 'wp_cron';
        if (empty($settings['enabled']) || $settings['executor'] !== $expected_executor || $this->automation_has_open_jobs()) {
            return;
        }
        $sources = $this->automation_scheduled_sources();
        if (!$sources) {
            update_option(self::OPTION_AUTOMATION_CURSOR, 0, false);
            update_option(self::OPTION_AUTOMATION_CYCLE, array('remaining'=>0,'total'=>0,'started_at'=>0), false);
            return;
        }
        $cycle = $this->automation_cycle_state();
        if ($cycle['remaining'] <= 0) {
            if (!$this->automation_dispatch_due()) {
                return;
            }
            $cycle = array('remaining'=>count($sources),'total'=>count($sources),'started_at'=>time());
            update_option(self::OPTION_AUTOMATION_LAST_DISPATCH, time(), false);
        }
        $batch = $this->automation_scheduled_source_batch(
            $sources,
            absint(get_option(self::OPTION_AUTOMATION_CURSOR, 0))
        );
        $source = is_array($batch['source'] ?? null) ? $batch['source'] : array();
        if (!$source) {
            update_option(self::OPTION_AUTOMATION_CYCLE, array('remaining'=>0,'total'=>0,'started_at'=>0), false);
            return;
        }
        $provider = sanitize_key((string) ($source['provider'] ?? ''));
        $result = $this->automation_dispatch_source($source, false);
        if (!is_wp_error($result)) {
            update_option(self::OPTION_AUTOMATION_CURSOR, absint($batch['next_cursor']), false);
            $cycle['remaining'] = max(0, absint($cycle['remaining']) - 1);
            update_option(self::OPTION_AUTOMATION_CYCLE, $cycle, false);
        }
    }

    private function automation_provider_registry() {
        $out = array();
        foreach ($this->provider_registry() as $key => $provider) {
            if (!$this->provider_supports($key, 'automation')) { continue; }
            $out[$key] = array(
                'label'=>(string) $provider['label'],
                'specialist_slug'=>(string) ($provider['specialist_slug'] ?? ''),
                'adapter_mode'=>in_array($key, array('awin','adcell'), true) ? 'central_queue' : ($key === 'ebay' ? 'provider_runtime' : 'adapter'),
            );
        }
        return apply_filters('ppar_affiliate_automation_provider_registry', $out, self::PROVIDER_CONTRACT_VERSION);
    }

    private function automation_uuid() {
        if (function_exists('wp_generate_uuid4')) {
            return wp_generate_uuid4();
        }
        return sprintf('%08x-%04x-%04x-%04x-%012x', mt_rand(), mt_rand(0, 0xffff), mt_rand(0, 0xffff), mt_rand(0, 0xffff), mt_rand());
    }

    private function automation_insert_run($run_uuid, $provider, $partner_external_id, $operation, $status, $started, $counts, $message, $details = array()) {
        global $wpdb;
        $wpdb->insert($this->automation_runs_table(), array(
            'run_uuid' => sanitize_text_field($run_uuid),
            'provider' => sanitize_key($provider),
            'partner_external_id' => sanitize_text_field($partner_external_id),
            'operation' => sanitize_key($operation),
            'status' => sanitize_key($status),
            'started_at' => absint($started),
            'finished_at' => time(),
            'imported' => absint($counts['imported'] ?? 0),
            'updated' => absint($counts['updated'] ?? 0),
            'unchanged' => absint($counts['unchanged'] ?? 0),
            'blocked' => absint($counts['blocked'] ?? 0),
            'failed' => absint($counts['failed'] ?? 0),
            'message' => sanitize_text_field($message),
            'details' => wp_json_encode($details, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES),
        ));
    }

    private function automation_empty_counts() {
        return array('imported'=>0,'updated'=>0,'unchanged'=>0,'blocked'=>0,'failed'=>0);
    }

    private function automation_decode_job_json($value, $fallback = array()) {
        $decoded = json_decode((string) $value, true);
        return is_array($decoded) ? $decoded : $fallback;
    }

    private function automation_enqueue_awin_partner($advertiser_id) {
        $advertiser_id = absint($advertiser_id);
        if ($advertiser_id <= 0) {
            return new WP_Error('awin_partner_invalid', 'Ungültige Awin-Advertiser-ID.');
        }
        $gate = $this->awin_programme_gate_validate($advertiser_id);
        if (is_wp_error($gate)) {
            return $gate;
        }
        global $wpdb;
        $table = $this->automation_jobs_table();
        $existing = $wpdb->get_var($wpdb->prepare(
            "SELECT id FROM {$table} WHERE provider='awin' AND partner_external_id=%s AND status IN ('queued','running','retry') LIMIT 1",
            (string) $advertiser_id
        ));
        if ($existing) {
            return new WP_Error('awin_job_exists', 'Für diesen Partner ist bereits ein Lauf vorgemerkt.');
        }
        $now = time();
        $job_uuid = $this->automation_uuid();
        $run_uuid = $this->automation_uuid();
        $ok = $wpdb->insert($table, array(
            'job_uuid'=>$job_uuid,
            'run_uuid'=>$run_uuid,
            'provider'=>'awin',
            'partner_external_id'=>(string) $advertiser_id,
            'stage'=>'programme',
            'status'=>'queued',
            'cursor_value'=>0,
            'offer_page'=>1,
            'retry_count'=>0,
            'not_before'=>$now,
            'lock_token'=>'',
            'lock_expires_at'=>0,
            'heartbeat_at'=>0,
            'counts'=>wp_json_encode($this->automation_empty_counts()),
            'details'=>wp_json_encode(array('feed'=>'pending','feed_complete'=>false,'offers_complete'=>false,'static_creatives'=>'unsupported_no_publisher_catalog_api')),
            'message'=>'Partnerlauf vorgemerkt.',
            'created_at'=>$now,
            'updated_at'=>$now,
            'finished_at'=>0,
        ));
        if (!$ok) {
            return new WP_Error('awin_job_insert_failed', 'Partnerlauf konnte nicht vorgemerkt werden.');
        }
        return array('job_id'=>absint($wpdb->insert_id), 'job_uuid'=>$job_uuid, 'run_uuid'=>$run_uuid);
    }

    private function automation_enqueue_adcell_feed() {
        $settings = $this->network_settings('adcell');
        $url = trim((string) ($settings['csv_feed_url'] ?? ''));
        $validated = $this->network_sync_validate_feed_url('adcell', $url);
        if (is_wp_error($validated)) {
            return new WP_Error('adcell_feed_not_configured', $validated->get_error_message());
        }
        global $wpdb;
        $table = $this->automation_jobs_table();
        $existing = $wpdb->get_var(
            "SELECT id FROM {$table} WHERE provider='adcell' AND partner_external_id='csv-feed' AND status IN ('queued','running','retry') LIMIT 1"
        );
        if ($existing) {
            return new WP_Error('adcell_job_exists', 'Für den ADCELL-Produktfeed ist bereits ein Lauf vorgemerkt.');
        }
        $now = time();
        $job_uuid = $this->automation_uuid();
        $run_uuid = $this->automation_uuid();
        $ok = $wpdb->insert($table, array(
            'job_uuid'=>$job_uuid,
            'run_uuid'=>$run_uuid,
            'provider'=>'adcell',
            'partner_external_id'=>'csv-feed',
            'stage'=>'feed',
            'status'=>'queued',
            'cursor_value'=>0,
            'offer_page'=>1,
            'retry_count'=>0,
            'not_before'=>$now,
            'lock_token'=>'',
            'lock_expires_at'=>0,
            'heartbeat_at'=>0,
            'counts'=>wp_json_encode($this->automation_empty_counts()),
            'details'=>wp_json_encode(array('feed'=>'pending','feed_complete'=>false,'partners'=>array())),
            'message'=>'ADCELL-Feedlauf vorgemerkt.',
            'created_at'=>$now,
            'updated_at'=>$now,
            'finished_at'=>0,
        ));
        if (!$ok) {
            return new WP_Error('adcell_job_insert_failed', 'ADCELL-Feedlauf konnte nicht vorgemerkt werden.');
        }
        return array('job_id'=>absint($wpdb->insert_id), 'job_uuid'=>$job_uuid, 'run_uuid'=>$run_uuid);
    }

    private function automation_claim_next_job() {
        global $wpdb;
        $table = $this->automation_jobs_table();
        $now = time();
        $job = $wpdb->get_row($wpdb->prepare(
            "SELECT * FROM {$table} WHERE ((status IN ('queued','retry') AND not_before<=%d AND (lock_expires_at=0 OR lock_expires_at<%d)) OR (status='running' AND lock_expires_at>0 AND lock_expires_at<%d)) ORDER BY id ASC LIMIT 1",
            $now, $now, $now
        ), ARRAY_A);
        if (!is_array($job) || empty($job['id'])) {
            return array();
        }
        $token = $this->automation_uuid();
        $updated = $wpdb->query($wpdb->prepare(
            "UPDATE {$table} SET status='running', lock_token=%s, lock_expires_at=%d, heartbeat_at=%d, updated_at=%d WHERE id=%d AND ((status IN ('queued','retry') AND (lock_expires_at=0 OR lock_expires_at<%d)) OR (status='running' AND lock_expires_at>0 AND lock_expires_at<%d))",
            $token, $now + 120, $now, $now, absint($job['id']), $now, $now
        ));
        if (!$updated) {
            return array();
        }
        $job = $wpdb->get_row($wpdb->prepare("SELECT * FROM {$table} WHERE id=%d AND lock_token=%s", absint($job['id']), $token), ARRAY_A);
        return is_array($job) ? $job : array();
    }

    private function automation_job_heartbeat($job_id, $lock_token) {
        global $wpdb;
        $table = $this->automation_jobs_table();
        $now = time();
        $wpdb->query($wpdb->prepare(
            "UPDATE {$table} SET heartbeat_at=%d, lock_expires_at=%d, updated_at=%d WHERE id=%d AND lock_token=%s",
            $now, $now + 120, $now, absint($job_id), sanitize_text_field($lock_token)
        ));
    }

    private function automation_release_job($job, $stage, $cursor, $offer_page, $counts, $details, $message, $delay = 0) {
        global $wpdb;
        $table = $this->automation_jobs_table();
        $now = time();
        $wpdb->update($table, array(
            'stage'=>sanitize_key($stage),
            'status'=>'queued',
            'cursor_value'=>max(0, (int) $cursor),
            'offer_page'=>max(1, absint($offer_page)),
            'not_before'=>$now + max(0, absint($delay)),
            'lock_token'=>'',
            'lock_expires_at'=>0,
            'heartbeat_at'=>$now,
            'counts'=>wp_json_encode($counts, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES),
            'details'=>wp_json_encode($details, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES),
            'message'=>sanitize_text_field($message),
            'updated_at'=>$now,
        ), array('id'=>absint($job['id'])));
    }

    private function automation_cleanup_job_file($details) {
        $file = isset($details['feed_file']) ? (string) $details['feed_file'] : '';
        if ($file !== '' && is_file($file)) {
            @unlink($file);
        }
    }

    private function automation_fail_job($job, $error, $counts, $details) {
        global $wpdb;
        $table = $this->automation_jobs_table();
        $retry = absint($job['retry_count'] ?? 0) + 1;
        $message = is_wp_error($error) ? $error->get_error_message() : sanitize_text_field((string) $error);
        $error_code = is_wp_error($error) ? sanitize_key((string) $error->get_error_code()) : '';
        $permanent_gate_error = in_array($error_code, array(
            'awin_partner_id_missing','awin_partner_portal_missing','awin_partner_not_approved',
            'awin_partner_other_portal','awin_partner_test_blocked','awin_partner_excluded',
            'awin_partner_portal_mismatch','awin_partner_not_joined_current'
        ), true);
        $now = time();
        if (!$permanent_gate_error && $retry <= 3) {
            $delays = array(1=>300, 2=>900, 3=>3600);
            $wpdb->update($table, array(
                'status'=>'retry',
                'retry_count'=>$retry,
                'not_before'=>$now + $delays[$retry],
                'lock_token'=>'',
                'lock_expires_at'=>0,
                'heartbeat_at'=>$now,
                'counts'=>wp_json_encode($counts),
                'details'=>wp_json_encode($details, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES),
                'message'=>sanitize_text_field('Wiederholung ' . $retry . '/3: ' . $message),
                'updated_at'=>$now,
            ), array('id'=>absint($job['id'])));
            return;
        }
        $counts['failed'] = absint($counts['failed'] ?? 0) + 1;
        $this->automation_cleanup_job_file($details);
        $wpdb->update($table, array(
            'status'=>'failed',
            'retry_count'=>$retry,
            'lock_token'=>'',
            'lock_expires_at'=>0,
            'heartbeat_at'=>$now,
            'counts'=>wp_json_encode($counts),
            'details'=>wp_json_encode($details, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES),
            'message'=>sanitize_text_field($message),
            'updated_at'=>$now,
            'finished_at'=>$now,
        ), array('id'=>absint($job['id'])));
        $this->automation_insert_run(
            (string) $job['run_uuid'],
            sanitize_key((string) ($job['provider'] ?? 'awin')),
            (string) $job['partner_external_id'],
            sanitize_key((string) ($job['provider'] ?? 'awin')) === 'adcell' ? 'queued_feed_sync' : 'queued_partner_sync',
            'failed',
            absint($job['created_at'] ?? $now),
            $counts,
            $message,
            $details
        );
    }

    private function automation_complete_job($job, $counts, $details, $status, $message) {
        global $wpdb;
        $table = $this->automation_jobs_table();
        $now = time();
        $this->automation_cleanup_job_file($details);
        unset($details['feed_file']);
        $wpdb->update($table, array(
            'stage'=>'complete',
            'status'=>'completed',
            'lock_token'=>'',
            'lock_expires_at'=>0,
            'heartbeat_at'=>$now,
            'counts'=>wp_json_encode($counts),
            'details'=>wp_json_encode($details, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES),
            'message'=>sanitize_text_field($message),
            'updated_at'=>$now,
            'finished_at'=>$now,
        ), array('id'=>absint($job['id'])));
        $this->automation_insert_run(
            (string) $job['run_uuid'],
            sanitize_key((string) ($job['provider'] ?? 'awin')),
            (string) $job['partner_external_id'],
            sanitize_key((string) ($job['provider'] ?? 'awin')) === 'adcell' ? 'queued_feed_sync' : 'queued_partner_sync',
            sanitize_key($status),
            absint($job['created_at'] ?? $now),
            $counts,
            $message,
            $details
        );
    }

    private function automation_validate_awin_feed_url($url) {
        $url = esc_url_raw((string) $url);
        if ($url === '' || !wp_http_validate_url($url)) {
            return new WP_Error('awin_feed_url_invalid', 'Feed enthält keine gültige Download-URL.');
        }
        $parts = wp_parse_url($url);
        $scheme = strtolower((string) ($parts['scheme'] ?? ''));
        $host = strtolower((string) ($parts['host'] ?? ''));
        if ($scheme !== 'https' || !in_array($host, array('productdata.awin.com','api.awin.com'), true)) {
            return new WP_Error('awin_feed_host_blocked', 'Feed-URL stammt nicht von einem freigegebenen Awin-Host.');
        }
        if ($host === 'api.awin.com') {
            $settings = $this->network_settings('awin');
            $publisher_id = preg_replace('/[^0-9]/', '', (string) ($settings['publisher_id'] ?? ''));
            $path = (string) ($parts['path'] ?? '');
            if ($publisher_id === '' || strpos($path, '/publishers/' . $publisher_id . '/') !== 0) {
                return new WP_Error('awin_feed_api_path_blocked', 'Awin-API-Feedpfad gehört nicht zum Publisherkonto.');
            }
        }
        return $url;
    }

    private function automation_select_awin_feed($snapshot) {
        $snapshot_id = absint($snapshot['external_id'] ?? 0);
        if ($snapshot_id <= 0) {
            return new WP_Error('awin_feed_partner_missing', 'Partner-Snapshot enthält keine gültige Advertiser-ID.');
        }
        $network = $this->network_settings('awin');
        $configured_url = trim((string) ($network['product_feed_url'] ?? ''));
        $configured_partner_id = absint($network['product_feed_partner_id'] ?? 0);
        if ($configured_url !== '' && $configured_partner_id === $snapshot_id) {
            $validated = $this->automation_validate_awin_feed_url($configured_url);
            if (is_wp_error($validated)) {
                return $validated;
            }
            return array(
                'url'=>$validated,
                'name'=>'Manuell gebundener Awin-Produktfeed',
            );
        }
        $url_keys = array('download_url','downloadurl','feed_url','feedurl','product_feed_url','productfeedurl','url','download_link','downloadlink','download_uri','downloaduri');
        $candidates = array();
        foreach ((array) ($snapshot['feeds'] ?? array()) as $row) {
            if (!is_array($row)) { continue; }
            $row_partner_id = 0;
            foreach (array('merchant_id','advertiser_id') as $id_key) {
                if (isset($row[$id_key]) && absint($row[$id_key]) > 0) {
                    $row_partner_id = absint($row[$id_key]);
                    break;
                }
            }
            if ($row_partner_id > 0 && $row_partner_id !== $snapshot_id) { continue; }
            $url = '';
            foreach ($url_keys as $key) {
                if (!empty($row[$key])) { $url = (string) $row[$key]; break; }
            }
            if ($url === '') { continue; }
            $validated = $this->automation_validate_awin_feed_url($url);
            if (is_wp_error($validated)) { continue; }
            $candidates[$validated] = array(
                'url'=>$validated,
                'name'=>sanitize_text_field((string) ($row['feed_name'] ?? $row['advertiser_name'] ?? $row['merchant_name'] ?? 'Awin-Produktfeed')),
            );
        }
        if (!$candidates) {
            return new WP_Error('awin_feed_exact_url_missing', 'Für diese Advertiser-ID ist kein eindeutig zugeordneter Awin-Produktfeed vorhanden.');
        }
        if (count($candidates) > 1) {
            return new WP_Error('awin_feed_ambiguous', 'Für diese Advertiser-ID sind mehrere Produktfeeds vorhanden. Ohne ausdrückliche Auswahl wird kein Produktfeed geraten.');
        }
        return reset($candidates);
    }

    private function automation_private_feed_dir() {
        $base = rtrim((string) sys_get_temp_dir(), '/\\');
        if ($base === '' || !is_dir($base) || !is_writable($base)) {
            return new WP_Error('automation_temp_dir_missing', 'Kein beschreibbares, nicht öffentliches Server-Tempverzeichnis verfügbar.');
        }
        $namespace = substr(hash('sha256', (string) ABSPATH), 0, 16);
        $dir = trailingslashit($base) . 'ppar-automation-private-' . $namespace;
        if (!is_dir($dir) && !wp_mkdir_p($dir)) {
            return new WP_Error('automation_feed_dir_failed', 'Privates Arbeitsverzeichnis konnte nicht angelegt werden.');
        }
        @chmod($dir, 0700);
        if (!is_file($dir . '/index.php')) {
            @file_put_contents($dir . '/index.php', "<?php\nexit;\n");
        }
        if (!is_file($dir . '/.htaccess')) {
            @file_put_contents($dir . '/.htaccess', "Require all denied\nDeny from all\n");
        }
        return $dir;
    }

    private function automation_decompress_if_needed($file) {
        $fh = @fopen($file, 'rb');
        $magic = $fh ? fread($fh, 2) : '';
        if ($fh) {
            fclose($fh);
        }
        if ($magic !== "\x1f\x8b") {
            return $file;
        }
        if (!function_exists('gzopen')) {
            return new WP_Error('automation_gzip_unsupported', 'GZIP-Feed kann auf diesem Server nicht entpackt werden.');
        }
        $out = $file . '.unpacked';
        $in = @gzopen($file, 'rb');
        $target = @fopen($out, 'wb');
        if (!$in || !$target) {
            if ($in) { gzclose($in); }
            if ($target) { fclose($target); }
            @unlink($out);
            return new WP_Error('automation_gzip_open_failed', 'GZIP-Feed konnte nicht entpackt werden.');
        }
        while (!gzeof($in)) {
            $chunk = gzread($in, 1048576);
            if ($chunk === false) {
                gzclose($in);
                fclose($target);
                @unlink($out);
                return new WP_Error('automation_gzip_read_failed', 'GZIP-Feed konnte nicht vollständig gelesen werden.');
            }
            fwrite($target, $chunk);
        }
        gzclose($in);
        fclose($target);
        @unlink($file);
        return $out;
    }

    private function automation_download_awin_feed($feed, $job_uuid) {
        $dir = $this->automation_private_feed_dir();
        if (is_wp_error($dir)) {
            return $dir;
        }
        $url = $this->automation_validate_awin_feed_url((string) ($feed['url'] ?? ''));
        if (is_wp_error($url)) {
            return $url;
        }
        $file = trailingslashit($dir) . 'feed-' . preg_replace('/[^a-z0-9-]/i', '', (string) $job_uuid) . '.dat';
        $settings = $this->automation_settings();
        $headers = array('Accept'=>'application/x-ndjson,application/json,text/csv,text/plain,application/octet-stream');
        $parts = wp_parse_url($url);
        if (strtolower((string) ($parts['host'] ?? '')) === 'api.awin.com') {
            $network = $this->network_settings('awin');
            $token = $this->network_secret('awin', 'access_token', $network);
            if ($token === '') {
                return new WP_Error('awin_not_configured', 'Awin API-Token fehlt.');
            }
            $headers['Authorization'] = 'Bearer ' . $token;
        }
        $response = wp_remote_get($url, array(
            'timeout'=>absint($settings['request_timeout']),
            'redirection'=>0,
            'stream'=>true,
            'filename'=>$file,
            'headers'=>$headers,
        ));
        if (is_wp_error($response)) {
            @unlink($file);
            return $response;
        }
        $code = (int) wp_remote_retrieve_response_code($response);
        if ($code !== 200) {
            @unlink($file);
            return new WP_Error('awin_feed_http_' . $code, 'Awin Feed HTTP ' . $code . '.');
        }
        if (!is_readable($file) || filesize($file) <= 0) {
            @unlink($file);
            return new WP_Error('awin_feed_empty_file', 'Awin lieferte keine lesbare Feeddatei.');
        }
        $file = $this->automation_decompress_if_needed($file);
        if (is_wp_error($file)) {
            return $file;
        }
        $handle = @fopen($file, 'rb');
        if (!$handle) {
            @unlink($file);
            return new WP_Error('awin_feed_open_failed', 'Awin-Feeddatei konnte nicht geöffnet werden.');
        }
        $first = '';
        while (($line = fgets($handle)) !== false) {
            if (trim((string) $line) !== '') {
                $first = preg_replace('/^\xEF\xBB\xBF/', '', (string) $line);
                break;
            }
        }
        if ($first === '') {
            fclose($handle);
            @unlink($file);
            return new WP_Error('awin_feed_empty', 'Awin-Feed enthält keine Datenzeilen.');
        }
        $json = json_decode(trim($first), true);
        if (is_array($json)) {
            $format = 'jsonl';
            $headers_row = array();
            $delimiter = '';
            $cursor = 0;
        } else {
            $format = 'csv';
            $delimiter = $this->network_sync_detect_delimiter($first);
            $headers_row = str_getcsv(rtrim($first, "\r\n"), $delimiter, '"', '\\');
            $headers_row = array_map('trim', (array) $headers_row);
            if (count(array_filter($headers_row, 'strlen')) < 2) {
                fclose($handle);
                @unlink($file);
                return new WP_Error('awin_feed_format_unknown', 'Feedformat konnte nicht sicher erkannt werden.');
            }
            $cursor = ftell($handle);
        }
        fclose($handle);
        return array('file'=>$file,'format'=>$format,'headers'=>$headers_row,'delimiter'=>$delimiter,'cursor'=>$cursor,'feed_name'=>(string) ($feed['name'] ?? 'Awin-Produktfeed'));
    }

    private function automation_download_adcell_feed($job_uuid) {
        $settings = $this->network_settings('adcell');
        $url = $this->network_sync_validate_feed_url('adcell', (string) ($settings['csv_feed_url'] ?? ''));
        if (is_wp_error($url)) {
            return new WP_Error('adcell_feed_not_configured', $url->get_error_message());
        }
        $dir = $this->automation_private_feed_dir();
        if (is_wp_error($dir)) {
            return $dir;
        }
        $file = trailingslashit($dir) . 'feed-adcell-' . preg_replace('/[^a-z0-9-]/i', '', (string) $job_uuid) . '.dat';
        $automation = $this->automation_settings();
        $response = wp_safe_remote_get($url, array(
            'timeout'=>absint($automation['request_timeout']),
            'redirection'=>0,
            'stream'=>true,
            'filename'=>$file,
            'headers'=>array('Accept'=>'text/csv,text/plain,application/csv,application/octet-stream'),
            'limit_response_size'=>104857600,
        ));
        if (is_wp_error($response)) {
            @unlink($file);
            return $response;
        }
        $code = (int) wp_remote_retrieve_response_code($response);
        if ($code !== 200) {
            @unlink($file);
            return new WP_Error('adcell_feed_http_' . $code, 'ADCELL Feed HTTP ' . $code . '.');
        }
        if (!is_readable($file) || filesize($file) <= 0) {
            @unlink($file);
            return new WP_Error('adcell_feed_empty_file', 'ADCELL lieferte keine lesbare Feeddatei.');
        }
        $file = $this->automation_decompress_if_needed($file);
        if (is_wp_error($file)) {
            return $file;
        }
        $handle = @fopen($file, 'rb');
        if (!$handle) {
            @unlink($file);
            return new WP_Error('adcell_feed_open_failed', 'ADCELL-Feeddatei konnte nicht geöffnet werden.');
        }
        $first = '';
        while (($line = fgets($handle)) !== false) {
            if (trim((string) $line) !== '') {
                $first = preg_replace('/^\xEF\xBB\xBF/', '', (string) $line);
                break;
            }
        }
        if ($first === '') {
            fclose($handle);
            @unlink($file);
            return new WP_Error('adcell_feed_empty', 'ADCELL-Feed enthält keine Datenzeilen.');
        }
        $delimiter = $this->network_sync_detect_delimiter($first);
        $headers = str_getcsv(rtrim($first, "\r\n"), $delimiter, '"', '\\');
        $headers = array_map('trim', (array) $headers);
        if (count(array_filter($headers, 'strlen')) < 2) {
            fclose($handle);
            @unlink($file);
            return new WP_Error('adcell_feed_header_invalid', 'ADCELL-Feed enthält keine brauchbare Kopfzeile.');
        }
        $mapping = $this->network_sync_detect_mapping($headers);
        foreach (array('external_id','programme_external_id','title','image_url','tracking_url') as $required) {
            if (empty($mapping[$required]['source'])) {
                fclose($handle);
                @unlink($file);
                return new WP_Error('adcell_feed_mapping_incomplete', 'ADCELL-Feedspalte fehlt: ' . $required . '.');
            }
        }
        $cursor = ftell($handle);
        fclose($handle);
        return array(
            'file'=>$file,
            'format'=>'csv',
            'headers'=>$headers,
            'mapping'=>$mapping,
            'delimiter'=>$delimiter,
            'cursor'=>$cursor,
            'feed_name'=>'ADCELL-CSV-Export',
        );
    }

    private function automation_awin_offer_has_next($raw, $page, $page_size, $row_count) {
        $page = max(1, absint($page));
        $page_size = max(1, absint($page_size));
        foreach (array('pagination','pageInfo','page_info','meta') as $key) {
            if (!isset($raw[$key]) || !is_array($raw[$key])) {
                continue;
            }
            $meta = $raw[$key];
            $total_pages = absint($meta['totalPages'] ?? $meta['total_pages'] ?? $meta['pageCount'] ?? $meta['page_count'] ?? 0);
            if ($total_pages > 0) {
                return $page < $total_pages;
            }
            $total = absint($meta['total'] ?? $meta['totalCount'] ?? $meta['total_count'] ?? 0);
            if ($total > 0) {
                return ($page * $page_size) < $total;
            }
        }
        return absint($row_count) >= $page_size;
    }

    private function automation_process_awin_product_batch($job, $snapshot, $details) {
        $file = (string) ($details['feed_file'] ?? '');
        $format = sanitize_key((string) ($details['feed_format'] ?? ''));
        if ($file === '' || !is_readable($file) || !in_array($format, array('jsonl','csv'), true)) {
            return new WP_Error('awin_feed_state_invalid', 'Gespeicherter Feed-Arbeitsstand ist ungültig.');
        }
        $handle = @fopen($file, 'rb');
        if (!$handle || fseek($handle, max(0, (int) ($job['cursor_value'] ?? 0))) !== 0) {
            if ($handle) { fclose($handle); }
            return new WP_Error('awin_feed_seek_failed', 'Feed-Fortschritt konnte nicht wieder aufgenommen werden.');
        }
        $settings = $this->automation_settings();
        $limit = absint($settings['batch_size']);
        $deadline = microtime(true) + absint($settings['time_budget']);
        $programme = is_array($snapshot['programme'] ?? null) ? $snapshot['programme'] : array();
        $context = array(
            'provider'=>'awin',
            'partner_external_id'=>(string) absint($snapshot['external_id'] ?? 0),
            'partner_name'=>sanitize_text_field((string) ($programme['name'] ?? $snapshot['submitted_name'] ?? 'Awin-Partner')),
            'source_kind'=>'product',
            'run_uuid'=>(string) $job['run_uuid'],
        );
        $counts = $this->automation_empty_counts();
        $processed = 0;
        $headers = is_array($details['feed_headers'] ?? null) ? $details['feed_headers'] : array();
        $delimiter = (string) ($details['feed_delimiter'] ?? ',');
        while ($processed < $limit && microtime(true) < $deadline) {
            if ($format === 'jsonl') {
                $line = fgets($handle);
                if ($line === false) {
                    break;
                }
                $line = trim((string) $line);
                if ($line === '') {
                    continue;
                }
                $row = json_decode($line, true);
                if (!is_array($row)) {
                    fclose($handle);
                    return new WP_Error('jsonl_invalid', 'Ungültige JSONL-Zeile im Produktfeed.');
                }
                if (isset($row['error'])) {
                    fclose($handle);
                    return new WP_Error('jsonl_incomplete', sanitize_text_field((string) ($row['message'] ?? 'Awin meldete einen unvollständigen Feed.')));
                }
            } else {
                $values = fgetcsv($handle, 0, $delimiter, '"', '\\');
                if ($values === false) {
                    break;
                }
                if (!array_filter($values, static function ($value) { return trim((string) $value) !== ''; })) {
                    continue;
                }
                $row = array();
                foreach ($headers as $index => $header) {
                    $row[(string) $header] = (string) ($values[$index] ?? '');
                }
            }
            $normalized = $this->automation_product_row($row, $snapshot, (string) $job['run_uuid']);
            if (is_wp_error($normalized)) {
                $counts['blocked']++;
            } else {
                $counts = $this->automation_merge_counts($counts, $this->automation_import_rows(array($normalized), $context));
            }
            $processed++;
            if (($processed % 100) === 0) {
                $this->automation_job_heartbeat(absint($job['id']), (string) $job['lock_token']);
            }
        }
        $cursor = ftell($handle);
        $eof = feof($handle);
        fclose($handle);
        return array('counts'=>$counts,'processed'=>$processed,'cursor'=>$cursor,'complete'=>$eof);
    }

    private function automation_process_adcell_product_batch($job, $details) {
        $file = (string) ($details['feed_file'] ?? '');
        $headers = is_array($details['feed_headers'] ?? null) ? $details['feed_headers'] : array();
        $mapping = is_array($details['feed_mapping'] ?? null) ? $details['feed_mapping'] : array();
        $delimiter = (string) ($details['feed_delimiter'] ?? ',');
        if ($file === '' || !is_readable($file) || !$headers || !$mapping) {
            return new WP_Error('adcell_feed_state_invalid', 'Gespeicherter ADCELL-Feed-Arbeitsstand ist ungültig.');
        }
        $handle = @fopen($file, 'rb');
        if (!$handle || fseek($handle, max(0, (int) ($job['cursor_value'] ?? 0))) !== 0) {
            if ($handle) { fclose($handle); }
            return new WP_Error('adcell_feed_seek_failed', 'ADCELL-Feed-Fortschritt konnte nicht wieder aufgenommen werden.');
        }
        $settings = $this->automation_settings();
        $limit = absint($settings['batch_size']);
        $deadline = microtime(true) + absint($settings['time_budget']);
        $counts = $this->automation_empty_counts();
        $processed = 0;
        $partners = array();
        while ($processed < $limit && microtime(true) < $deadline) {
            $values = fgetcsv($handle, 0, $delimiter, '"', '\\');
            if ($values === false) {
                break;
            }
            if (!array_filter($values, static function ($value) { return trim((string) $value) !== ''; })) {
                continue;
            }
            $row = array();
            foreach ($headers as $index => $header) {
                $row[(string) $header] = (string) ($values[$index] ?? '');
            }
            $normalized = $this->automation_adcell_product_row($row, $mapping, (string) $job['run_uuid']);
            if (is_wp_error($normalized)) {
                $counts['blocked']++;
            } else {
                $partner_id = (string) $normalized['_partner_external_id'];
                $partner_name = (string) $normalized['_partner_name'];
                unset($normalized['_partner_external_id'], $normalized['_partner_name']);
                $context = array(
                    'provider'=>'adcell',
                    'partner_external_id'=>$partner_id,
                    'partner_name'=>$partner_name,
                    'source_kind'=>'product',
                    'run_uuid'=>(string) $job['run_uuid'],
                );
                $counts = $this->automation_merge_counts($counts, $this->automation_import_rows(array($normalized), $context));
                $partners[$partner_id] = $partner_name;
            }
            $processed++;
            if (($processed % 100) === 0) {
                $this->automation_job_heartbeat(absint($job['id']), (string) $job['lock_token']);
            }
        }
        $cursor = ftell($handle);
        $eof = feof($handle);
        fclose($handle);
        return array('counts'=>$counts,'processed'=>$processed,'cursor'=>$cursor,'complete'=>$eof,'partners'=>$partners);
    }

    private function automation_process_adcell_job($job, $counts, $details) {
        $stage = sanitize_key((string) ($job['stage'] ?? 'feed'));
        if ($stage === 'feed') {
            $download = $this->automation_download_adcell_feed((string) $job['job_uuid']);
            if (is_wp_error($download)) {
                return $download;
            }
            $details['feed'] = sanitize_text_field((string) $download['feed_name']);
            $details['feed_file'] = (string) $download['file'];
            $details['feed_format'] = 'csv';
            $details['feed_headers'] = (array) $download['headers'];
            $details['feed_mapping'] = (array) $download['mapping'];
            $details['feed_delimiter'] = (string) $download['delimiter'];
            $details['products'] = 0;
            $details['partners'] = array();
            $this->automation_release_job($job, 'products', absint($download['cursor']), 1, $counts, $details, 'ADCELL-Feed gespeichert. Erstes Produktpaket folgt.');
            return true;
        }
        if ($stage === 'products') {
            $result = $this->automation_process_adcell_product_batch($job, $details);
            if (is_wp_error($result)) {
                return $result;
            }
            $counts = $this->automation_merge_counts($counts, $result['counts']);
            $details['products'] = absint($details['products'] ?? 0) + absint($result['processed']);
            $details['partners'] = array_merge(is_array($details['partners'] ?? null) ? $details['partners'] : array(), (array) $result['partners']);
            if (!empty($result['complete'])) {
                $details['feed_complete'] = true;
                $this->automation_release_job($job, 'reconcile', 0, 1, $counts, $details, 'ADCELL-Produktfeed vollständig verarbeitet. Abgleich folgt.');
            } else {
                $this->automation_release_job($job, 'products', absint($result['cursor']), 1, $counts, $details, absint($result['processed']) . ' ADCELL-Produkte verarbeitet; Fortsetzung vorgemerkt.');
            }
            return true;
        }
        if ($stage === 'reconcile') {
            $partner_ids = array_keys(is_array($details['partners'] ?? null) ? $details['partners'] : array());
            $cursor = max(0, (int) ($job['cursor_value'] ?? 0));
            $deadline = microtime(true) + absint($this->automation_settings()['time_budget']);
            $processed = 0;
            while (isset($partner_ids[$cursor]) && $processed < 20 && microtime(true) < $deadline) {
                $partner_id = sanitize_text_field((string) $partner_ids[$cursor]);
                $this->automation_reconcile_partner_assets('adcell', $partner_id, 'product', (string) $job['run_uuid']);
                $this->automation_rebuild_edges('adcell', $partner_id);
                $cursor++;
                $processed++;
            }
            if (isset($partner_ids[$cursor])) {
                $this->automation_release_job($job, 'reconcile', $cursor, 1, $counts, $details, $processed . ' ADCELL-Partner abgeglichen; Fortsetzung vorgemerkt.');
                return true;
            }
            $this->automation_complete_job($job, $counts, $details, 'success', 'ADCELL-Feed vollständig und paketweise abgeschlossen.');
            return true;
        }
        return new WP_Error('adcell_stage_invalid', 'Unbekannte ADCELL-Automatisierungsstufe.');
    }

    private function automation_process_claimed_job($job) {
        $counts = $this->automation_decode_job_json($job['counts'] ?? '', $this->automation_empty_counts());
        $details = $this->automation_decode_job_json($job['details'] ?? '', array());
        $provider = sanitize_key((string) ($job['provider'] ?? ''));
        if ($provider === 'adcell') {
            return $this->automation_process_adcell_job($job, $counts, $details);
        }
        $advertiser_id = absint($job['partner_external_id'] ?? 0);
        $stage = sanitize_key((string) ($job['stage'] ?? 'programme'));
        if ($advertiser_id <= 0 || $provider !== 'awin') {
            return new WP_Error('automation_job_invalid', 'Ungültiger Automatisierungsauftrag.');
        }
        $gate = $this->awin_programme_gate_validate($advertiser_id);
        if (is_wp_error($gate)) {
            return $gate;
        }
        if ($stage === 'programme') {
            $snapshot = $this->partner_intake_probe_partner('awin', $advertiser_id, '', false);
            if (is_wp_error($snapshot)) {
                return $snapshot;
            }
            $this->partner_intake_store_snapshot('awin', (string) $advertiser_id, $snapshot);
            $programme = is_array($snapshot['programme'] ?? null) ? $snapshot['programme'] : array();
            $details['partner_name'] = sanitize_text_field((string) ($programme['name'] ?? 'Awin-Partner'));
            $this->automation_release_job($job, 'offers', 0, 1, $counts, $details, 'Programmdaten geprüft. Angebote folgen.');
            return true;
        }
        $snapshots = $this->partner_intake_snapshots();
        $snapshot = isset($snapshots['awin:' . $advertiser_id]) && is_array($snapshots['awin:' . $advertiser_id]) ? $snapshots['awin:' . $advertiser_id] : array();
        if (!$snapshot) {
            return new WP_Error('automation_snapshot_missing', 'Partner-Snapshot fehlt.');
        }
        if ($stage === 'offers') {
            $page = max(1, absint($job['offer_page'] ?? 1));
            $raw = $this->partner_intake_awin_offers($advertiser_id, $page, 200);
            if (is_wp_error($raw)) {
                return $raw;
            }
            $raw_rows = $this->partner_intake_extract_offer_rows($raw);
            $offer_rows = array();
            foreach ($this->partner_intake_normalize_offers($raw, $advertiser_id) as $offer) {
                $row = $this->automation_offer_row($offer, $snapshot, (string) $job['run_uuid']);
                if (is_wp_error($row)) {
                    $counts['blocked']++;
                } elseif (is_array($row)) {
                    $offer_rows[] = $row;
                }
            }
            if ($offer_rows) {
                $context = array(
                    'provider'=>'awin',
                    'partner_external_id'=>(string) $advertiser_id,
                    'partner_name'=>(string) ($details['partner_name'] ?? 'Awin-Partner'),
                    'source_kind'=>'offer',
                    'run_uuid'=>(string) $job['run_uuid'],
                );
                $counts = $this->automation_merge_counts($counts, $this->automation_import_rows($offer_rows, $context));
            }
            $details['offers'] = absint($details['offers'] ?? 0) + count($offer_rows);
            if ($this->automation_awin_offer_has_next($raw, $page, 200, count($raw_rows))) {
                if ($page >= 50) {
                    return new WP_Error('awin_offer_page_limit', 'Sicherheitsgrenze von 50 Angebotsseiten erreicht.');
                }
                $this->automation_release_job($job, 'offers', 0, $page + 1, $counts, $details, 'Angebotsseite ' . $page . ' verarbeitet.');
                return true;
            }
            $details['offers_complete'] = true;
            $this->automation_reconcile_partner_assets('awin', (string) $advertiser_id, 'offer', (string) $job['run_uuid']);
            $this->automation_release_job($job, 'feed', 0, 1, $counts, $details, 'Angebote vollständig verarbeitet. Produktfeed folgt.');
            return true;
        }
        if ($stage === 'feed') {
            $feed = $this->automation_select_awin_feed($snapshot);
            if (is_wp_error($feed)) {
                if (in_array($feed->get_error_code(), array('awin_feed_exact_url_missing','awin_feed_ambiguous'), true)) {
                    $details['feed'] = $feed->get_error_code() === 'awin_feed_ambiguous' ? 'blocked_ambiguous' : 'not_available_exact_url';
                    $details['feed_complete'] = false;
                    $details['feed_note'] = $feed->get_error_message();
                    $this->automation_release_job($job, 'finalize', 0, 1, $counts, $details, 'Produktfeed sicher ausgelassen: ' . $feed->get_error_message());
                    return true;
                }
                return $feed;
            }
            $download = $this->automation_download_awin_feed($feed, (string) $job['job_uuid']);
            if (is_wp_error($download)) {
                return $download;
            }
            $details['feed'] = sanitize_text_field((string) $download['feed_name']);
            $details['feed_file'] = (string) $download['file'];
            $details['feed_format'] = sanitize_key((string) $download['format']);
            $details['feed_headers'] = (array) $download['headers'];
            $details['feed_delimiter'] = (string) $download['delimiter'];
            $details['products'] = 0;
            $this->automation_release_job($job, 'products', absint($download['cursor']), 1, $counts, $details, 'Feed gespeichert. Erstes Produktpaket folgt.');
            return true;
        }
        if ($stage === 'products') {
            $result = $this->automation_process_awin_product_batch($job, $snapshot, $details);
            if (is_wp_error($result)) {
                return $result;
            }
            $counts = $this->automation_merge_counts($counts, $result['counts']);
            $details['products'] = absint($details['products'] ?? 0) + absint($result['processed']);
            if (!empty($result['complete'])) {
                $details['feed_complete'] = true;
                $this->automation_reconcile_partner_assets('awin', (string) $advertiser_id, 'product', (string) $job['run_uuid']);
                $this->automation_release_job($job, 'finalize', absint($result['cursor']), 1, $counts, $details, 'Produktfeed vollständig verarbeitet. Abschlussprüfung folgt.');
            } else {
                $this->automation_release_job($job, 'products', absint($result['cursor']), 1, $counts, $details, absint($result['processed']) . ' Produkte verarbeitet; Fortsetzung vorgemerkt.');
            }
            return true;
        }
        if ($stage === 'finalize') {
            $details['target_edges'] = $this->automation_rebuild_edges('awin', (string) $advertiser_id);
            $partial = empty($details['feed_complete']);
            $status = $partial ? 'partial' : 'success';
            $message = $partial
                ? 'Partnerlauf abgeschlossen; Angebote vollständig, Produktfeed nicht eindeutig verfügbar.'
                : 'Partnerlauf vollständig und paketweise abgeschlossen.';
            $this->automation_complete_job($job, $counts, $details, $status, $message);
            return true;
        }
        return new WP_Error('automation_stage_invalid', 'Unbekannte Automatisierungsstufe.');
    }

    public function run_automation_worker($manual_or_external = false) {
        if (!$manual_or_external) {
            $settings = $this->automation_settings();
            if (empty($settings['enabled']) || $settings['executor'] !== 'wp_cron') {
                return false;
            }
        }
        $job = $this->automation_claim_next_job();
        if (!$job && !$manual_or_external) {
            $this->run_scheduled_partner_sync(false);
            $job = $this->automation_claim_next_job();
        }
        if (!$job) {
            return false;
        }
        $counts = $this->automation_decode_job_json($job['counts'] ?? '', $this->automation_empty_counts());
        $details = $this->automation_decode_job_json($job['details'] ?? '', array());
        try {
            $result = $this->automation_process_claimed_job($job);
            if (is_wp_error($result)) {
                $this->automation_fail_job($job, $result, $counts, $details);
                return $result;
            }
            if (!$manual_or_external && !$this->automation_has_open_jobs()) {
                $this->run_scheduled_partner_sync(false);
            }
            return true;
        } catch (Throwable $error) {
            $wrapped = new WP_Error('automation_runtime_error', $error->getMessage());
            $this->automation_fail_job($job, $wrapped, $counts, $details);
            return $wrapped;
        }
    }

    public function handle_automation_process_next() {
        if (!current_user_can('manage_options')) {
            wp_die('Keine Berechtigung.');
        }
        check_admin_referer('ppar_automation_process_next', 'ppar_automation_process_nonce');
        $result = $this->run_automation_worker(true);
        $message = is_wp_error($result) ? $result->get_error_message() : ($result ? 'Ein Arbeitspaket wurde verarbeitet.' : 'Kein fälliges Arbeitspaket vorhanden.');
        $status = is_wp_error($result) ? 'failed' : 'progress';
        wp_safe_redirect(add_query_arg(array('page'=>'affiliate-portal-automation','ppar_auto'=>$status,'ppar_message'=>rawurlencode($message)), admin_url('admin.php')));
        exit;
    }

    public function register_automation_cli() {
        $router = $this;
        WP_CLI::add_command('ppar automation-tick', static function () use ($router) {
            $router->maybe_install_automation_schema();
            $settings = $router->automation_settings();
            if (empty($settings['enabled'])) {
                WP_CLI::warning('Affiliate-Automatisierung ist deaktiviert.');
                return;
            }
            if (!$router->automation_has_open_jobs()) {
                $router->run_scheduled_partner_sync(true);
            }
            $result = $router->run_automation_worker(true);
            if (is_wp_error($result)) {
                WP_CLI::error($result->get_error_message(), false);
            } elseif ($result) {
                WP_CLI::success('Ein Arbeitspaket wurde verarbeitet.');
            } else {
                WP_CLI::log('Kein fälliges Arbeitspaket.');
            }
        });
    }

    private function automation_awin_tracking_url($advertiser_id, $destination_url, $clickref = '') {
        $settings = $this->network_settings('awin');
        $publisher_id = preg_replace('/[^0-9]/', '', (string) ($settings['publisher_id'] ?? ''));
        $advertiser_id = absint($advertiser_id);
        $destination_url = esc_url_raw((string) $destination_url);
        if ($publisher_id === '' || $advertiser_id <= 0 || $destination_url === '') {
            return '';
        }
        $args = array(
            'awinmid' => $advertiser_id,
            'awinaffid' => $publisher_id,
            'ued' => $destination_url,
        );
        if ($clickref !== '') {
            $args['clickref'] = substr(sanitize_key($clickref), 0, 64);
        }
        return add_query_arg($args, 'https://www.awin1.com/cread.php');
    }

    private function automation_awin_flatten_product($row) {
        if (!is_array($row)) {
            return array();
        }
        $flat = $row;
        $walk = static function ($value) use (&$walk, &$flat) {
            if (!is_array($value)) {
                return;
            }
            foreach ($value as $key => $child) {
                if (is_string($key) && !is_array($child) && !array_key_exists($key, $flat)) {
                    $flat[$key] = $child;
                } elseif (is_array($child) && array_keys($child) !== range(0, count($child) - 1)) {
                    $walk($child);
                }
            }
        };
        foreach ($row as $value) {
            if (is_array($value) && array_keys($value) !== range(0, count($value) - 1)) {
                $walk($value);
            }
        }
        return $flat;
    }

    private function automation_awin_field($row, $aliases, $default = '') {
        $normalized = array();
        foreach ((array) $row as $key => $value) {
            if (!is_scalar($value)) {
                continue;
            }
            $normalized[$this->network_sync_normalize_header((string) $key)] = (string) $value;
        }
        foreach ((array) $aliases as $alias) {
            $key = $this->network_sync_normalize_header((string) $alias);
            if (isset($normalized[$key]) && trim($normalized[$key]) !== '') {
                return trim($normalized[$key]);
            }
        }
        return $default;
    }

    private function automation_normalize_date($value) {
        $value = trim((string) $value);
        if ($value === '') {
            return '';
        }
        $time = strtotime($value);
        return $time ? gmdate('Y-m-d', $time) : '';
    }

    private function automation_normalize_price_currency($price, $currency = 'EUR') {
        $price = trim(sanitize_text_field((string) $price));
        $currency = strtoupper(trim(sanitize_text_field((string) $currency)));
        $symbol_map = array('€' => 'EUR', '$' => 'USD', '£' => 'GBP');
        foreach ($symbol_map as $symbol => $code) {
            if (strpos($price, $symbol) !== false) {
                $currency = $code;
                $price = str_replace($symbol, '', $price);
                break;
            }
        }
        if (preg_match('/(?:^|\s)(EUR|USD|GBP|CHF|PLN|SEK|NOK|DKK)(?:$|\s)/i', $price, $match)) {
            $currency = strtoupper($match[1]);
            $price = preg_replace('/(?:^|\s)' . preg_quote($match[1], '/') . '(?:$|\s)/i', ' ', $price);
        }
        $price = trim(preg_replace('/\s+/', ' ', (string) $price));
        if ($currency === '') {
            $currency = 'EUR';
        }
        return array(
            'price' => $price,
            'currency' => substr($currency, 0, 10),
        );
    }

    private function automation_product_row($row, $snapshot, $run_uuid) {
        $advertiser_id = absint($snapshot['external_id'] ?? 0);
        $programme = is_array($snapshot['programme'] ?? null) ? $snapshot['programme'] : array();
        $meta_advertiser = absint($row['meta']['advertiser_id'] ?? 0);
        $row = $this->automation_awin_flatten_product($row);
        $row_advertiser = absint($this->automation_awin_field($row, array('advertiser_id','merchant_id'), '0'));
        if (($meta_advertiser > 0 && $meta_advertiser !== $advertiser_id) || ($row_advertiser > 0 && $row_advertiser !== $advertiser_id)) {
            return new WP_Error('product_partner_mismatch', 'Produktzeile gehört zu einer anderen Awin-Advertiser-ID.');
        }
        $title = sanitize_text_field($this->automation_awin_field($row, array('title','product_name','productname','product_title','name')));
        $destination = esc_url_raw($this->automation_awin_field($row, array('link','mobile_link','merchant_deep_link','destination_url','product_url','url')));
        $tracking = esc_url_raw($this->automation_awin_field($row, array('aw_deep_link','tracking_url','affiliate_url','click_url','deep_link','deeplink','trackinglink')));
        $image = esc_url_raw($this->automation_awin_field($row, array('image_link','merchant_image_url','product_image_url','image_url','large_image','image')));
        $external = sanitize_text_field($this->automation_awin_field($row, array('id','aw_product_id','product_id','merchant_product_id','sku','ean','gtin')));
        if ($title === '' || $image === '' || $external === '' || ($destination === '' && $tracking === '')) {
            return new WP_Error('product_incomplete', 'Produkt ohne ID, Titel, Ziel oder Bild blockiert.');
        }
        if ($destination === '') {
            $destination = $tracking;
        }
        if ($tracking === '') {
            $tracking = $this->automation_awin_tracking_url($advertiser_id, $destination, 'product-' . $external);
        }
        if ($tracking === '') {
            return new WP_Error('product_tracking_missing', 'Produkt ohne belastbaren Trackinglink blockiert.');
        }
        $category = sanitize_text_field($this->automation_awin_field($row, array('product_type','merchant_category','category_name','product_category','category')));
        $google = sanitize_text_field($this->automation_awin_field($row, array('google_product_category')));
        $brand = sanitize_text_field($this->automation_awin_field($row, array('brand','brand_name')));
        $description = sanitize_textarea_field($this->automation_awin_field($row, array('description','product_description','short_description')));
        $availability = sanitize_text_field($this->automation_awin_field($row, array('availability','stock_status','in_stock'), 'active'));
        $availability_key = sanitize_key($availability);
        $inactive = in_array($availability_key, array('out_of_stock','out_ouf_stock','discontinued','unavailable','inactive','false','0'), true);
        $price_currency = $this->automation_normalize_price_currency(
            $this->automation_awin_field($row, array('sale_price','search_price','current_price','price')),
            $this->automation_awin_field($row, array('currency'), 'EUR')
        );
        return array(
            'creative_id' => $external,
            'creative_type' => 'product',
            'creative_title' => $title,
            'creative_description' => $description,
            'creative_tag' => trim(implode(' | ', array_filter(array($category, $google, $brand)))),
            'image_source' => $image,
            'destination_url' => $destination,
            'tracking_url' => $tracking,
            'status' => $inactive ? 'inactive' : 'active',
            'price' => $price_currency['price'],
            'currency' => $price_currency['currency'],
            'availability' => $availability,
            'brand' => $brand,
            'product_type' => $category,
            'google_product_category' => $google,
            'gtin' => sanitize_text_field($this->automation_awin_field($row, array('gtin','ean'))),
            'mpn' => sanitize_text_field($this->automation_awin_field($row, array('mpn','sku'))),
            '_source_kind' => 'product',
            '_run_uuid' => $run_uuid,
            '_partner_name' => sanitize_text_field((string) ($programme['name'] ?? $snapshot['submitted_name'] ?? 'Awin-Partner')),
        );
    }

    private function automation_adcell_product_row($row, $mapping, $run_uuid) {
        $external = sanitize_text_field($this->network_sync_mapped_value($row, $mapping, 'external_id'));
        $partner_id = preg_replace('/[^0-9A-Za-z._-]/', '', (string) $this->network_sync_mapped_value($row, $mapping, 'programme_external_id'));
        $partner_name = sanitize_text_field($this->network_sync_mapped_value($row, $mapping, 'programme_name'));
        $title = sanitize_text_field($this->network_sync_mapped_value($row, $mapping, 'title'));
        $image = esc_url_raw($this->network_sync_mapped_value($row, $mapping, 'image_url'));
        $tracking = esc_url_raw($this->network_sync_mapped_value($row, $mapping, 'tracking_url'));
        $destination = esc_url_raw($this->network_sync_mapped_value($row, $mapping, 'destination_url'));
        if ($external === '' || $partner_id === '' || $title === '' || $image === '' || $tracking === '') {
            return new WP_Error('adcell_product_incomplete', 'ADCELL-Produkt ohne Partner-ID, Produkt-ID, Titel, Bild oder Trackinglink blockiert.');
        }
        if ($partner_name === '') {
            $partner_name = 'ADCELL-Partner ' . $partner_id;
        }
        if ($destination === '') {
            $destination = $tracking;
        }
        $price_currency = $this->automation_normalize_price_currency(
            $this->network_sync_mapped_value($row, $mapping, 'price'),
            $this->network_sync_mapped_value($row, $mapping, 'currency') ?: 'EUR'
        );
        $category = sanitize_text_field($this->network_sync_mapped_value($row, $mapping, 'category'));
        $brand = sanitize_text_field($this->network_sync_mapped_value($row, $mapping, 'brand'));
        $availability = sanitize_text_field($this->automation_awin_field($row, array('availability','stock_status','in_stock'), 'active'));
        $availability_key = sanitize_key($availability);
        $inactive = in_array($availability_key, array('out_of_stock','out_ouf_stock','discontinued','unavailable','inactive','false','0'), true);
        return array(
            'creative_id'=>$external,
            'creative_type'=>'product',
            'creative_title'=>$title,
            'creative_description'=>sanitize_textarea_field($this->automation_awin_field($row, array('description','product_description','short_description'))),
            'creative_tag'=>trim(implode(' | ', array_filter(array($category, $brand)))),
            'image_source'=>$image,
            'destination_url'=>$destination,
            'tracking_url'=>$tracking,
            'status'=>$inactive ? 'inactive' : 'active',
            'price'=>$price_currency['price'],
            'currency'=>$price_currency['currency'],
            'availability'=>$availability,
            'brand'=>$brand,
            'product_type'=>$category,
            'google_product_category'=>'',
            'gtin'=>sanitize_text_field($this->automation_awin_field($row, array('gtin','ean'))),
            'mpn'=>sanitize_text_field($this->automation_awin_field($row, array('mpn','sku'))),
            '_source_kind'=>'product',
            '_run_uuid'=>$run_uuid,
            '_partner_external_id'=>$partner_id,
            '_partner_name'=>$partner_name,
        );
    }

    private function automation_offer_row($offer, $snapshot, $run_uuid) {
        $programme = is_array($snapshot['programme'] ?? null) ? $snapshot['programme'] : array();
        $external_id = absint($offer['external_id'] ?? 0);
        $title = sanitize_text_field((string) ($offer['title'] ?? ''));
        $tracking = esc_url_raw((string) ($offer['tracking_url'] ?? ''));
        $destination = esc_url_raw((string) ($offer['destination_url'] ?? ''));
        if ($tracking === '' && $destination !== '') {
            $tracking = $this->automation_awin_tracking_url(absint($snapshot['external_id'] ?? 0), $destination, 'offer-' . $external_id);
        }
        if ($external_id <= 0 || $title === '' || $tracking === '') {
            return new WP_Error('offer_incomplete', 'Angebot ohne ID, Titel oder Trackinglink blockiert.');
        }
        $start_date = $this->automation_normalize_date($offer['start_date'] ?? '');
        $end_date = $this->automation_normalize_date($offer['end_date'] ?? '');
        $today = gmdate('Y-m-d');
        $active = !($start_date !== '' && $start_date > $today) && !($end_date !== '' && $end_date < $today);
        $description = sanitize_textarea_field((string) ($offer['description'] ?? ''));
        $terms = sanitize_textarea_field((string) ($offer['terms'] ?? ''));
        if ($terms !== '') {
            $description = trim($description . "\n" . $terms);
        }
        return array(
            'creative_id' => 'offer-' . $external_id,
            'creative_type' => 'text',
            'creative_title' => $title,
            'creative_description' => $description,
            'creative_tag' => sanitize_text_field((string) ($offer['type'] ?? 'promotion')),
            'destination_url' => $destination !== '' ? $destination : $tracking,
            'tracking_url' => $tracking,
            'status' => $active ? 'active' : 'inactive',
            'start_date' => $start_date,
            'end_date' => $end_date,
            'voucher_code' => sanitize_text_field((string) ($offer['voucher_code'] ?? '')),
            'voucher_exclusive' => !empty($offer['voucher_exclusive']) ? '1' : '0',
            'voucher_attributable' => !empty($offer['voucher_attributable']) ? '1' : '0',
            '_source_kind' => 'offer',
            '_run_uuid' => $run_uuid,
            '_partner_name' => sanitize_text_field((string) ($programme['name'] ?? $snapshot['submitted_name'] ?? 'Awin-Partner')),
        );
    }

    private function automation_import_rows($rows, $context) {
        $mapping = $this->creative_library_detect_mapping(array_keys((array) reset($rows)));
        $counts = array('imported'=>0,'updated'=>0,'unchanged'=>0,'blocked'=>0,'failed'=>0);
        foreach ($rows as $row) {
            if (!is_array($row)) {
                $counts['failed']++;
                continue;
            }
            $normalized = $this->creative_library_normalize_row($row, $mapping, $context);
            if (is_wp_error($normalized)) {
                $counts['blocked']++;
                continue;
            }
            $result = $this->creative_library_upsert($normalized);
            if (isset($counts[$result])) {
                $counts[$result]++;
            } else {
                $counts['failed']++;
            }
        }
        return $counts;
    }

    private function automation_merge_counts($a, $b) {
        foreach (array('imported','updated','unchanged','blocked','failed') as $key) {
            $a[$key] = absint($a[$key] ?? 0) + absint($b[$key] ?? 0);
        }
        return $a;
    }

    private function automation_rebuild_edges($provider, $partner_external_id) {
        global $wpdb;
        $library = $this->creative_library_table();
        $edges = $this->automation_edges_table();
        $provider = sanitize_key($provider);
        $partner_external_id = sanitize_text_field($partner_external_id);
        $wpdb->query($wpdb->prepare(
            "DELETE FROM {$edges} WHERE provider=%s AND partner_external_id=%s AND source='automatic'",
            $provider, $partner_external_id
        ));
        $rows = $wpdb->get_results($wpdb->prepare(
            "SELECT identity_hash, topic_status, topic_targets FROM {$library} WHERE provider=%s AND partner_external_id=%s AND source_status='active' AND availability_state='active' AND topic_status IN ('auto_verified','auto_review','ambiguous')",
            $provider, $partner_external_id
        ), ARRAY_A);
        $now = time();
        $count = 0;
        foreach ($rows as $row) {
            $targets = json_decode((string) ($row['topic_targets'] ?? ''), true);
            if (!is_array($targets)) {
                continue;
            }
            foreach ($targets as $target) {
                if (!is_array($target)) {
                    continue;
                }
                $type = sanitize_key((string) ($target['type'] ?? ''));
                $slug = sanitize_key((string) ($target['slug'] ?? ''));
                if (!in_array($type, array('page','category','journal','market'), true) || $slug === '') {
                    continue;
                }
                $data = array(
                    'provider' => sanitize_key($provider),
                    'partner_external_id' => sanitize_text_field($partner_external_id),
                    'asset_identity_hash' => sanitize_text_field((string) $row['identity_hash']),
                    'target_type' => $type,
                    'target_slug' => $slug,
                    'target_path' => sanitize_text_field((string) ($target['path'] ?? $slug)),
                    'score' => absint($target['score'] ?? 0),
                    'edge_status' => sanitize_key((string) ($row['topic_status'] ?? 'review')),
                    'source' => 'automatic',
                    'updated_at' => $now,
                );
                $existing = $wpdb->get_var($wpdb->prepare("SELECT id FROM {$edges} WHERE asset_identity_hash=%s AND target_type=%s AND target_slug=%s", $data['asset_identity_hash'], $type, $slug));
                if ($existing) {
                    $wpdb->update($edges, $data, array('id'=>absint($existing)));
                } else {
                    $wpdb->insert($edges, $data);
                }
                $count++;
            }
        }
        return $count;
    }

    private function automation_reconcile_partner_assets($provider, $partner_external_id, $source_kind, $run_uuid) {
        global $wpdb;
        $table = $this->creative_library_table();
        $rows = $wpdb->get_results($wpdb->prepare(
            "SELECT id, missing_count FROM {$table} WHERE provider=%s AND partner_external_id=%s AND source_kind=%s AND last_complete_run<>%s",
            sanitize_key($provider), sanitize_text_field($partner_external_id), sanitize_key($source_kind), sanitize_text_field($run_uuid)
        ), ARRAY_A);
        foreach ($rows as $row) {
            $missing = absint($row['missing_count'] ?? 0) + 1;
            $wpdb->update($table, array(
                'missing_count'=>$missing,
                'availability_state'=>$missing >= 2 ? 'inactive_missing' : 'quarantine_missing',
                'selected'=>0,
            ), array('id'=>absint($row['id'])));
        }
    }

    public function handle_automation_full_sync() {
        if (!current_user_can('manage_options')) {
            wp_die('Keine Berechtigung.');
        }
        check_admin_referer('ppar_automation_full_sync', 'ppar_automation_nonce');
        $provider = sanitize_key((string) ($_POST['provider'] ?? ''));
        $partner_id = preg_replace('/[^0-9A-Za-z._-]/', '', (string) ($_POST['partner_external_id'] ?? ''));
        if ($provider === '') {
            $result = new WP_Error('automation_provider_missing', 'Provider fehlt.');
        } else {
            if ($provider === 'adcell' && $partner_id === '') { $partner_id = 'csv-feed'; }
            if ($provider === 'ebay' && $partner_id === '') { $partner_id = 'provider'; }
            $result = $this->automation_dispatch_source(array(
                'key'=>$provider . ':' . $partner_id,
                'provider'=>$provider,
                'partner_external_id'=>$partner_id,
            ), true);
        }
        $immediate = is_array($result) && !empty($result['immediate']);
        if (!is_wp_error($result) && !$immediate) {
            $this->run_automation_worker(true);
        }
        $status = is_wp_error($result) ? 'failed' : ($immediate ? 'completed' : 'progress');
        $message = is_wp_error($result)
            ? $result->get_error_message()
            : ($immediate ? $this->provider_label($provider) . '-Lauf wurde unmittelbar verarbeitet.' : 'Lauf gestartet; das erste kleine Arbeitspaket wurde verarbeitet.');
        wp_safe_redirect(add_query_arg(array('page'=>'affiliate-portal-automation','ppar_auto'=>$status,'ppar_message'=>rawurlencode($message),'provider'=>$provider,'partner_external_id'=>$partner_id), admin_url('admin.php')));
        exit;
    }

    /**
     * Entfernt ausschließlich die nicht mehr unterstützten Browser-Bridge-Token.
     * Der Awin-Bannerkatalog wird nicht über Browserautomatisierung oder Scraping bezogen.
     */
    public function maybe_cleanup_removed_import_tokens() {
        if (get_option(self::OPTION_BRIDGE_TOKENS, null) !== null) {
            delete_option(self::OPTION_BRIDGE_TOKENS);
        }
        if (function_exists('delete_user_meta')) {
            delete_user_meta(get_current_user_id(), 'ppar_last_bridge_token');
        }
    }

    /**
     * V4: Slot- und Formatentscheidungen liegen ausschließlich im zentralen
     * Ausgabeobjekt-Modell. Die alte globale Bibliothekslogik wurde entfernt,
     * damit kein zweiter, widersprüchlicher Materialisierungspfad existiert.
     */

    public function automation_normalize_target_key($key) {
        $key = strtolower(trim((string) $key));
        if (!preg_match('/^(page|category|journal|market):([a-z0-9_-]+)$/', $key, $match)) {
            return '';
        }
        return $match[1] . ':' . sanitize_key($match[2]);
    }

    private function automation_campaign_exact_target_rank($campaign, $context) {
        $wanted = array_values(array_filter(array_map(array($this, 'automation_normalize_target_key'), (array) ($campaign['automation_target_keys'] ?? array()))));
        if (!$wanted) {
            return null;
        }
        $primary = sanitize_key((string) ($context['primary_slug'] ?? ''));
        $post_type = sanitize_key((string) ($context['post_type'] ?? ''));
        $available = array();
        $slot_type = sanitize_key((string) ($context['slot_type'] ?? ''));
        if ($post_type === 'page' && $slot_type === 'anzeigenmarkt_top_banner') {
            $available[] = 'market:anzeigenmarkt';
        }
        if ($primary !== '') {
            if ($post_type === 'page') {
                $available[] = 'page:' . $primary;
                $available[] = 'journal:' . $primary;
            } elseif ($post_type === 'category_archive') {
                $available[] = 'category:' . $primary;
                $available[] = 'journal:' . $primary;
            } elseif ($post_type === 'hp_listing_category_archive') {
                $available[] = 'market:' . $primary;
            }
        }
        foreach ((array) ($context['direct_term_slugs'] ?? array()) as $slug) {
            $slug = sanitize_key((string) $slug);
            if ($slug === '') {
                continue;
            }
            if ($post_type === 'post') {
                $available[] = 'category:' . $slug;
                $available[] = 'journal:' . $slug;
            } elseif ($post_type === 'hp_listing') {
                $available[] = 'market:' . $slug;
            }
        }
        $matches = array_values(array_intersect(array_unique($wanted), array_unique($available)));
        if (!$matches) {
            return null;
        }
        return array('specificity'=>520, 'matches'=>count($matches), 'reason'=>'Exakte automatisierte Zielkante: ' . implode(', ', $matches) . '.');
    }

    public function handle_automation_materialize() {
        if (!current_user_can('manage_options')) {
            wp_die('Keine Berechtigung.');
        }
        check_admin_referer('ppar_automation_materialize', 'ppar_materialize_nonce');
        global $wpdb;
        $table = $this->creative_library_table();
        $rows = $wpdb->get_results("SELECT * FROM {$table} WHERE selected=1 AND source_status='active' AND availability_state='active' ORDER BY id ASC LIMIT 100", ARRAY_A);
        $ok = 0;
        $blocked = 0;
        foreach ((array) $rows as $row) {
            if (!method_exists($this, 'output_plan_creative')) {
                $blocked++;
                continue;
            }
            $result = $this->output_plan_creative($row, true);
            $ok += absint($result['drafts'] ?? 0);
            $blocked += absint($result['blocked'] ?? 0);
        }
        wp_safe_redirect(add_query_arg(array('page'=>'affiliate-portal-automation','ppar_auto'=>'materialized','created'=>$ok,'blocked'=>$blocked), admin_url('admin.php')));
        exit;
    }

    public function automation_extend_topic_with_hivepress($topic, $creative) {
        if (!is_array($topic) || (string) ($topic['status'] ?? '') === 'blocked') {
            return $topic;
        }
        if (!function_exists('taxonomy_exists') || !taxonomy_exists('hp_listing_category') || !function_exists('get_terms')) {
            return $topic;
        }
        $terms = get_terms(array('taxonomy'=>'hp_listing_category','hide_empty'=>false));
        if (is_wp_error($terms) || !is_array($terms)) {
            return $topic;
        }
        $source = $this->creative_library_text(implode(' ', array(
            (string) ($creative['title'] ?? ''),
            (string) ($creative['tags'] ?? ''),
            (string) ($creative['description'] ?? ''),
            (string) ($creative['destination_url'] ?? ''),
        )));
        $source_tokens = $this->creative_library_tokens($source);
        if (!$source_tokens) {
            return $topic;
        }
        $candidates = array();
        foreach ($terms as $term) {
            if (!is_object($term) || empty($term->slug) || empty($term->name)) {
                continue;
            }
            $name = $this->creative_library_text((string) $term->name);
            $target_tokens = $this->creative_library_tokens((string) $term->name . ' ' . (string) $term->slug . ' ' . (string) ($term->description ?? ''));
            $hits = array_values(array_intersect($source_tokens, $target_tokens));
            $phrase = $name !== '' && strpos(' ' . $source . ' ', ' ' . $name . ' ') !== false;
            $score = ($phrase ? 75 : 0) + min(24, count($hits) * 8) + (count($hits) >= 2 ? 8 : 0);
            if ($score < 70) {
                continue;
            }
            $candidates[] = array(
                'type'=>'market',
                'slug'=>sanitize_key((string) $term->slug),
                'path'=>'Anzeigenmarkt > ' . sanitize_text_field((string) $term->name),
                'score'=>min(100, $score),
                'reason'=>$hits ? 'Passender HivePress-Kontext: ' . implode(', ', array_slice($hits, 0, 4)) : 'Exakte HivePress-Phrase.',
                'relation'=>'hivepress_context',
            );
        }
        usort($candidates, static function ($a, $b) { return (int) $a['score'] > (int) $b['score'] ? -1 : 1; });
        if (!$candidates) {
            return $topic;
        }
        $targets = is_array($topic['targets'] ?? null) ? $topic['targets'] : array();
        $seen = array();
        foreach ($targets as $target) {
            if (is_array($target)) {
                $seen[(string) ($target['type'] ?? '') . ':' . (string) ($target['slug'] ?? '')] = true;
            }
        }
        foreach (array_slice($candidates, 0, 3) as $candidate) {
            $key = 'market:' . $candidate['slug'];
            if (!isset($seen[$key])) {
                $targets[] = $candidate;
                $seen[$key] = true;
            }
        }
        $topic['targets'] = $targets;
        if ((string) ($topic['status'] ?? '') === 'no_match') {
            $topic['status'] = 'auto_review';
            $topic['score'] = absint($candidates[0]['score'] ?? 70);
            $topic['reason'] = 'Nur HivePress-Ziel gefunden; Sichtprüfung erforderlich.';
        }
        return $topic;
    }

    private function automation_recent_runs() {
        global $wpdb;
        $table = $this->automation_runs_table();
        return $wpdb->get_results("SELECT * FROM {$table} ORDER BY id DESC LIMIT 15", ARRAY_A);
    }

    private function automation_recent_jobs() {
        global $wpdb;
        $table = $this->automation_jobs_table();
        return $wpdb->get_results("SELECT * FROM {$table} ORDER BY id DESC LIMIT 15", ARRAY_A);
    }

    /**
     * V4.3.1 – WordPress behandelt bereits ein leeres HTML-Attribut `disabled`
     * als deaktiviert. Deshalb darf das Attribut im positiven Fall überhaupt
     * nicht an submit_button() übergeben werden.
     */
    private function automation_awin_start_button_attributes($selected_snapshot) {
        return is_array($selected_snapshot) && absint($selected_snapshot['external_id'] ?? 0) > 0
            ? array()
            : array('disabled' => 'disabled');
    }

    public function render_automation_page() {
        if (!current_user_can('manage_options')) {
            wp_die('Keine Berechtigung.');
        }
        $snapshots = $this->partner_intake_snapshots();
        $allowed_snapshots = array_values(array_filter($snapshots, function ($snapshot) {
            return is_array($snapshot)
                && sanitize_key((string) ($snapshot['provider'] ?? '')) === 'awin'
                && $this->awin_programme_gate_is_allowed(absint($snapshot['external_id'] ?? 0));
        }));
        $partner_id = sanitize_text_field((string) ($_GET['partner_external_id'] ?? ''));
        if ($partner_id === '' && $allowed_snapshots) {
            $first = reset($allowed_snapshots);
            if (is_array($first)) {
                $partner_id = sanitize_text_field((string) ($first['external_id'] ?? ''));
            }
        }
        $notice = sanitize_key((string) ($_GET['ppar_auto'] ?? ''));
        $message = rawurldecode((string) ($_GET['ppar_message'] ?? ''));
        $counts = $this->creative_library_count_rows();
        $automation_settings = $this->automation_settings();
        $jobs = $this->automation_recent_jobs();
        $runs = $this->automation_recent_runs();
        $adcell_settings = $this->network_settings('adcell');
        $adcell_feed_ready = !is_wp_error($this->network_sync_validate_feed_url('adcell', (string) ($adcell_settings['csv_feed_url'] ?? '')));
        $selected_snapshot = array();
        foreach ($allowed_snapshots as $snapshot) {
            if (is_array($snapshot) && sanitize_key((string) ($snapshot['provider'] ?? '')) === 'awin' && (string) ($snapshot['external_id'] ?? '') === (string) $partner_id) {
                $selected_snapshot = $snapshot;
                break;
            }
        }
        $awin_feed_check = $selected_snapshot ? $this->automation_select_awin_feed($selected_snapshot) : new WP_Error('awin_feed_partner_missing', 'Partner auswählen.');
        $awin_feed_ready = !is_wp_error($awin_feed_check);
        $awin_feed_message = $awin_feed_ready ? 'Produktfeed eindeutig: ' . sanitize_text_field((string) ($awin_feed_check['name'] ?? 'Awin-Produktfeed')) : $awin_feed_check->get_error_message();
        ?>
        <div class="wrap" style="max-width:1400px"><h1>Affiliate-Automatisierung</h1>
        <p>Sichere Paketverarbeitung: ein Partner, <?php echo absint($automation_settings['batch_size']); ?> Produkte je Paket, keine Sofortveröffentlichung.</p>
        <?php if ($notice && $message) : ?><div class="notice <?php echo $notice === 'failed' ? 'notice-error' : 'notice-success'; ?> inline"><p><?php echo esc_html($message); ?></p></div><?php endif; ?>
        <?php if ($notice === 'materialized') : ?><div class="notice notice-success inline"><p><?php echo absint($_GET['created'] ?? 0); ?> inaktive Kampagnen vorbereitet; <?php echo absint($_GET['blocked'] ?? 0); ?> blockiert.</p></div><?php endif; ?>
        <div style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px;margin:18px 0">
          <div style="background:#fff;border:1px solid #c3c4c7;padding:18px"><strong style="font-size:24px"><?php echo absint($counts['all']); ?></strong><br>Bibliotheksobjekte</div>
          <div style="background:#fff;border:1px solid #c3c4c7;padding:18px"><strong style="font-size:24px"><?php echo absint($counts['auto_verified']); ?></strong><br>automatisch sicher</div>
          <div style="background:#fff;border:1px solid #c3c4c7;padding:18px"><strong style="font-size:24px"><?php echo absint($counts['selected']); ?></strong><br>ausgewählt</div>
        </div>
        <section style="background:#fff;border:1px solid #c3c4c7;padding:20px;margin-bottom:18px"><h2>Provider-Orchestrierung</h2><p>Zentrale Automatisierung erkennt alle Provider mit der Fähigkeit <code>automation</code>. Awin/ADCELL verwenden die interne Paketwarteschlange; eBay verwendet seinen eigenen sicheren Providerlauf. Weitere Provider können ihren Adapter registrieren, ohne diesen Kern umzubauen.</p><table class="widefat striped"><thead><tr><th>Provider</th><th>Zugang</th><th>Automatisierung</th><th>Fachseite</th></tr></thead><tbody><?php foreach($this->automation_provider_registry() as $auto_provider=>$auto_def): $snap=$this->provider_access_snapshot($auto_provider); ?><tr><td><strong><?php echo esc_html((string)$auto_def['label']); ?></strong></td><td><?php echo $this->provider_status_badge($snap); ?></td><td><?php echo esc_html((string)$auto_def['adapter_mode']); ?></td><td><?php if(!empty($auto_def['specialist_slug'])): ?><a class="button button-small" href="<?php echo esc_url(admin_url('admin.php?page='.(string)$auto_def['specialist_slug'])); ?>">Öffnen</a><?php else: ?><span class="description">Adaptergesteuert</span><?php endif; ?></td></tr><?php endforeach; ?></tbody></table><?php do_action('ppar_affiliate_render_automation_providers', $this->provider_registry(), self::PROVIDER_CONTRACT_VERSION); ?></section>
        <section style="background:#fff;border:1px solid #c3c4c7;padding:20px;margin-bottom:18px"><h2>1. Datenlauf starten</h2>
        <form method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>"><input type="hidden" name="action" value="ppar_automation_full_sync"><?php wp_nonce_field('ppar_automation_full_sync','ppar_automation_nonce'); ?>
        <p><label>Partner<br><select name="partner_external_id" required style="min-width:360px" onchange="window.location.href='<?php echo esc_js(admin_url('admin.php?page=affiliate-portal-automation&partner_external_id=')); ?>'+encodeURIComponent(this.value)" <?php disabled(!$allowed_snapshots); ?>><option value="">Partner auswählen</option><?php foreach ($allowed_snapshots as $snap) : $id=sanitize_text_field((string)($snap['external_id']??'')); $prog=is_array($snap['programme']??null)?$snap['programme']:array(); $name=sanitize_text_field((string)($prog['name']??$snap['submitted_name']??$id)); ?><option value="<?php echo esc_attr($id); ?>" <?php selected($partner_id,$id); ?>><?php echo esc_html('AWIN · '.$name.' · '.$id); ?></option><?php endforeach; ?></select><input type="hidden" name="provider" value="awin"></label></p>
        <p class="description"><strong>Eingangsweiche:</strong> Nur unter „Awin“ für dieses Portal aktive Partner erscheinen hier.</p>
        <p class="description"><strong>Produktfeed:</strong> <?php echo esc_html($awin_feed_message); ?> Angebote werden auch ohne Produktfeed verarbeitet.</p>
        <?php submit_button('Awin-Lauf starten','primary','submit',true,$this->automation_awin_start_button_attributes($selected_snapshot)); ?></form>
        <form method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>" style="margin-top:8px"><input type="hidden" name="action" value="ppar_automation_full_sync"><input type="hidden" name="provider" value="adcell"><?php wp_nonce_field('ppar_automation_full_sync','ppar_automation_nonce'); ?><button class="button" <?php disabled(!$adcell_feed_ready); ?>>ADCELL-CSV-Lauf starten</button><?php if(!$adcell_feed_ready): ?> <span class="description">Exakte CSV-Export-URL fehlt.</span><?php endif; ?></form>
        <?php $ebay_snapshot=$this->provider_access_snapshot('ebay'); $ebay_settings=method_exists($this,'ebay_settings')?$this->ebay_settings():array(); $ebay_ready=!empty($ebay_snapshot['configured'])&&!empty($ebay_settings['contract_confirmed'])&&!empty($ebay_settings['privacy_confirmed']); ?>
        <form method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>" style="margin-top:8px"><input type="hidden" name="action" value="ppar_automation_full_sync"><input type="hidden" name="provider" value="ebay"><input type="hidden" name="partner_external_id" value="provider"><?php wp_nonce_field('ppar_automation_full_sync','ppar_automation_nonce'); ?><button class="button" <?php disabled(!$ebay_ready); ?>>eBay-Lauf starten</button><?php if(!$ebay_ready): ?> <span class="description">Zugang oder eBay-Vertrags-/Datenschutzbestätigung noch unvollständig.</span><?php endif; ?></form>
        <form method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>" style="margin-top:8px"><input type="hidden" name="action" value="ppar_automation_process_next"><?php wp_nonce_field('ppar_automation_process_next','ppar_automation_process_nonce'); ?><?php submit_button('Nächstes Arbeitspaket verarbeiten','secondary', 'submit', false); ?></form></section>
        <section style="background:#fff;border:1px solid #c3c4c7;padding:20px;margin-bottom:18px"><h2>2. Auswahl vorbereiten</h2><p>Es entstehen ausschließlich inaktive Kampagnen zur Vorschau.</p>
        <form method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>"><input type="hidden" name="action" value="ppar_automation_materialize"><?php wp_nonce_field('ppar_automation_materialize','ppar_materialize_nonce'); ?><?php submit_button('Ausgewählte Creatives portalübergreifend als Entwürfe planen','primary'); ?></form></section>
        <section style="background:#fff;border:1px solid #c3c4c7;padding:20px;margin-bottom:18px"><h2>Automatische Aktualisierung</h2>
        <form method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>"><input type="hidden" name="action" value="ppar_automation_save_settings"><?php wp_nonce_field('ppar_automation_save_settings','ppar_automation_settings_nonce'); ?>
        <p><label><input type="checkbox" name="ppar_automation[enabled]" value="1" <?php checked(!empty($automation_settings['enabled'])); ?>> automatische Synchronisierung aktiv</label></p>
        <p><label>Ausführung <select name="ppar_automation[executor]"><option value="server_cron" <?php selected($automation_settings['executor'],'server_cron'); ?>>Server-Cron / WP-CLI</option><option value="wp_cron" <?php selected($automation_settings['executor'],'wp_cron'); ?>>WP-Cron-Fallback</option></select></label> <label style="margin-left:18px">Rhythmus <select name="ppar_automation[schedule]"><option value="daily" <?php selected($automation_settings['schedule'],'daily'); ?>>täglich</option><option value="twicedaily" <?php selected($automation_settings['schedule'],'twicedaily'); ?>>alle 12 Stunden</option></select></label></p>
        <p><label>Produkte je Paket <input type="number" min="100" max="1000" step="100" name="ppar_automation[batch_size]" value="<?php echo absint($automation_settings['batch_size']); ?>"></label> <label style="margin-left:18px">Zeitbudget <input type="number" min="10" max="25" name="ppar_automation[time_budget]" value="<?php echo absint($automation_settings['time_budget']); ?>"> s</label> <label style="margin-left:18px">Download-Timeout <input type="number" min="15" max="45" name="ppar_automation[request_timeout]" value="<?php echo absint($automation_settings['request_timeout']); ?>"> s</label></p>
        <p><code>wp ppar automation-tick</code></p>
        <?php submit_button('Automatisierung speichern','secondary'); ?></form></section>
        <p><a class="button" href="<?php echo esc_url(admin_url('admin.php?page=affiliate-portal-creative-library')); ?>">Werbemittel auswählen</a> <a class="button" href="<?php echo esc_url(admin_url('admin.php?page=affiliate-portal-preview')); ?>">Vorschau öffnen</a></p>
        <h2>Arbeitswarteschlange</h2><table class="widefat striped"><thead><tr><th>Zeit</th><th>Partner</th><th>Stufe</th><th>Status</th><th>Meldung</th></tr></thead><tbody><?php if(!$jobs): ?><tr><td colspan="5">Keine Aufträge.</td></tr><?php else: foreach($jobs as $job): ?><tr><td><?php echo esc_html(wp_date('d.m.Y H:i',absint($job['updated_at']))); ?></td><td><?php echo esc_html($this->provider_label((string)$job['provider']).' · '.(string)$job['partner_external_id']); ?></td><td><?php echo esc_html((string)$job['stage']); ?></td><td><?php echo esc_html((string)$job['status']); ?></td><td><?php echo esc_html((string)$job['message']); ?></td></tr><?php endforeach; endif; ?></tbody></table>
        <h2>Abgeschlossene Läufe</h2><table class="widefat striped"><thead><tr><th>Zeit</th><th>Partner</th><th>Status</th><th>Importiert</th><th>Aktualisiert</th><th>Blockiert</th><th>Meldung</th></tr></thead><tbody><?php if(!$runs): ?><tr><td colspan="7">Noch kein Lauf.</td></tr><?php else: foreach($runs as $run): ?><tr><td><?php echo esc_html(wp_date('d.m.Y H:i',absint($run['started_at']))); ?></td><td><?php echo esc_html($this->provider_label((string)$run['provider']).' · '.(string)$run['partner_external_id']); ?></td><td><?php echo esc_html((string)$run['status']); ?></td><td><?php echo absint($run['imported']); ?></td><td><?php echo absint($run['updated']); ?></td><td><?php echo absint($run['blocked']); ?></td><td><?php echo esc_html((string)$run['message']); ?></td></tr><?php endforeach; endif; ?></tbody></table>
        </div><?php
    }

}
