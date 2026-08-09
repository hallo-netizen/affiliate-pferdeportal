<?php
if (!defined('ABSPATH')) {
    exit;
}

/**
 * Providerunabhängiger Affiliate-Steuervertrag.
 *
 * Provideradapter beschaffen und normalisieren ausschließlich Daten. Die
 * Freigabehierarchie, Chefentscheidungen, Sicherheitsblocker, Ziel-/Slot-
 * Vorgaben, Notabschaltung und Protokollierung liegen zentral in diesem Kern.
 */
trait PPAR_Control_Contract_Trait {
    private function control_decisions_table() {
        global $wpdb;
        return $wpdb->base_prefix . 'ppar_control_decisions';
    }

    private function control_audit_table() {
        global $wpdb;
        return $wpdb->base_prefix . 'ppar_control_audit';
    }

    public function maybe_install_control_contract_schema() {
        $installed = (string) get_option(self::OPTION_CONTROL_SCHEMA_VERSION, '0');
        if ($installed === self::CONTROL_SCHEMA_VERSION) {
            return;
        }
        require_once ABSPATH . 'wp-admin/includes/upgrade.php';
        global $wpdb;
        $decisions = $this->control_decisions_table();
        $audit = $this->control_audit_table();
        $charset = $wpdb->get_charset_collate();
        dbDelta("CREATE TABLE {$decisions} (
            id bigint(20) unsigned NOT NULL AUTO_INCREMENT,
            decision_key char(64) NOT NULL,
            portal_key varchar(191) NOT NULL DEFAULT '',
            scope_type varchar(30) NOT NULL,
            scope_key text NOT NULL,
            status varchar(30) NOT NULL DEFAULT 'automatic',
            reason text NOT NULL,
            payload longtext NULL,
            user_id bigint(20) unsigned NOT NULL DEFAULT 0,
            created_at bigint(20) unsigned NOT NULL DEFAULT 0,
            updated_at bigint(20) unsigned NOT NULL DEFAULT 0,
            PRIMARY KEY  (id),
            UNIQUE KEY decision_key (decision_key),
            KEY portal_scope (portal_key(100), scope_type, status),
            KEY updated_at (updated_at)
        ) {$charset};");
        dbDelta("CREATE TABLE {$audit} (
            id bigint(20) unsigned NOT NULL AUTO_INCREMENT,
            event_type varchar(50) NOT NULL,
            portal_key varchar(191) NOT NULL DEFAULT '',
            scope_type varchar(30) NOT NULL,
            scope_key text NOT NULL,
            old_status varchar(30) NOT NULL DEFAULT '',
            new_status varchar(30) NOT NULL DEFAULT '',
            reason text NOT NULL,
            payload longtext NULL,
            user_id bigint(20) unsigned NOT NULL DEFAULT 0,
            created_at bigint(20) unsigned NOT NULL DEFAULT 0,
            PRIMARY KEY  (id),
            KEY created_at (created_at),
            KEY portal_scope (portal_key(100), scope_type, new_status)
        ) {$charset};");
        if (get_option(self::OPTION_CONTROL_SETTINGS, null) === null) {
            update_option(self::OPTION_CONTROL_SETTINGS, array(
                'emergency_stop'=>0,
                'emergency_reason'=>'',
                'updated_at'=>0,
                'updated_by'=>0,
            ), false);
        }
        $this->control_migrate_existing_decisions($installed);
        update_option(self::OPTION_CONTROL_SCHEMA_VERSION, self::CONTROL_SCHEMA_VERSION, false);
    }

    private function control_decision_key($portal_key, $scope_type, $scope_key) {
        return hash('sha256', sanitize_key((string) $portal_key) . '|' . sanitize_key((string) $scope_type) . '|' . (string) $scope_key);
    }

    private function control_allowed_scope_types() {
        return array('provider','partner','creative','target','slot','output');
    }

    private function control_allowed_statuses($scope_type) {
        $scope_type = sanitize_key((string) $scope_type);
        $all = array(
            'provider'=>array('automatic','approved','paused','veto'),
            'partner'=>array('automatic','approved','review','veto'),
            'creative'=>array('automatic','approved','review','veto'),
            'target'=>array('automatic','fixed','veto'), // fixed bleibt als V4.4-Kompatibilitätsstatus les-/speicherbar; neue feste Ziele liegen Creative-bezogen im Payload.
            'slot'=>array('automatic','fixed','veto'),   // dito; UI erzeugt keine neuen globalen fixed-Entscheidungen.

            'output'=>array('automatic','approved','paused','veto'),
        );
        return $all[$scope_type] ?? array();
    }

    private function control_clean_payload($payload) {
        $payload = is_array($payload) ? $payload : array();
        $safe = array();
        foreach (array('target_type','target_key','target_label','target_context','slot_id','provider','partner_external_id','output_id') as $field) {
            if (!array_key_exists($field, $payload)) {
                continue;
            }
            if (in_array($field, array('target_label','target_key','partner_external_id'), true)) {
                $safe[$field] = sanitize_text_field((string) $payload[$field]);
            } elseif ($field === 'output_id') {
                $safe[$field] = absint($payload[$field]);
            } else {
                $safe[$field] = sanitize_key((string) $payload[$field]);
            }
        }
        return $safe;
    }

    public function control_get_decision($portal_key, $scope_type, $scope_key) {
        global $wpdb;
        $portal_key = sanitize_key((string) $portal_key);
        $scope_type = sanitize_key((string) $scope_type);
        $scope_key = sanitize_text_field((string) $scope_key);
        if (!in_array($scope_type, $this->control_allowed_scope_types(), true) || $scope_key === '') {
            return array('exists'=>false,'status'=>'automatic','reason'=>'','payload'=>array(),'user_id'=>0,'created_at'=>0,'updated_at'=>0);
        }
        $key = $this->control_decision_key($portal_key, $scope_type, $scope_key);
        $row = $wpdb->get_row($wpdb->prepare("SELECT * FROM {$this->control_decisions_table()} WHERE decision_key=%s", $key), ARRAY_A);
        if (!is_array($row)) {
            return array('exists'=>false,'status'=>'automatic','reason'=>'','payload'=>array(),'user_id'=>0,'created_at'=>0,'updated_at'=>0);
        }
        $payload = json_decode((string) ($row['payload'] ?? ''), true);
        return array(
            'exists'=>true,
            'id'=>absint($row['id'] ?? 0),
            'status'=>sanitize_key((string) ($row['status'] ?? 'automatic')),
            'reason'=>sanitize_text_field((string) ($row['reason'] ?? '')),
            'payload'=>is_array($payload) ? $payload : array(),
            'user_id'=>absint($row['user_id'] ?? 0),
            'created_at'=>absint($row['created_at'] ?? 0),
            'updated_at'=>absint($row['updated_at'] ?? 0),
        );
    }

    public function control_set_decision($portal_key, $scope_type, $scope_key, $status, $reason, $payload = array(), $event_type = 'manual_decision') {
        global $wpdb;
        $portal_key = sanitize_key((string) $portal_key);
        $scope_type = sanitize_key((string) $scope_type);
        $scope_key = sanitize_text_field((string) $scope_key);
        $status = sanitize_key((string) $status);
        $reason = sanitize_text_field((string) $reason);
        if (!in_array($scope_type, $this->control_allowed_scope_types(), true)
            || !in_array($status, $this->control_allowed_statuses($scope_type), true)
            || $scope_key === ''
            || ($status !== 'automatic' && $reason === '')) {
            return new WP_Error('control_decision_invalid', 'Chefentscheidung ist unvollständig oder ungültig.');
        }
        $payload = $this->control_clean_payload($payload);
        $existing = $this->control_get_decision($portal_key, $scope_type, $scope_key);
        $now = time();
        $user_id = function_exists('get_current_user_id') ? absint(get_current_user_id()) : 0;
        $key = $this->control_decision_key($portal_key, $scope_type, $scope_key);
        $data = array(
            'decision_key'=>$key,
            'portal_key'=>$portal_key,
            'scope_type'=>$scope_type,
            'scope_key'=>$scope_key,
            'status'=>$status,
            'reason'=>$reason,
            'payload'=>wp_json_encode($payload, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES),
            'user_id'=>$user_id,
            'updated_at'=>$now,
        );
        if (!empty($existing['exists'])) {
            $wpdb->update($this->control_decisions_table(), $data, array('id'=>absint($existing['id'])));
            $id = absint($existing['id']);
        } else {
            $data['created_at'] = $now;
            $wpdb->insert($this->control_decisions_table(), $data);
            $id = absint($wpdb->insert_id);
        }
        if ($id <= 0) {
            return new WP_Error('control_decision_save_failed', 'Chefentscheidung konnte nicht gespeichert werden.');
        }
        $this->control_log_event($event_type, $portal_key, $scope_type, $scope_key, (string) ($existing['status'] ?? 'automatic'), $status, $reason, $payload, $user_id);
        return $id;
    }

    public function control_reset_decision($portal_key, $scope_type, $scope_key, $reason = 'Manuelle Entscheidung zurückgenommen; Automatik wieder aktiv.') {
        return $this->control_set_decision($portal_key, $scope_type, $scope_key, 'automatic', $reason, array(), 'manual_decision_reset');
    }

    private function control_log_event($event_type, $portal_key, $scope_type, $scope_key, $old_status, $new_status, $reason, $payload = array(), $user_id = null) {
        global $wpdb;
        if ($user_id === null) {
            $user_id = function_exists('get_current_user_id') ? absint(get_current_user_id()) : 0;
        }
        $wpdb->insert($this->control_audit_table(), array(
            'event_type'=>sanitize_key((string) $event_type),
            'portal_key'=>sanitize_key((string) $portal_key),
            'scope_type'=>sanitize_key((string) $scope_type),
            'scope_key'=>sanitize_text_field((string) $scope_key),
            'old_status'=>sanitize_key((string) $old_status),
            'new_status'=>sanitize_key((string) $new_status),
            'reason'=>sanitize_text_field((string) $reason),
            'payload'=>wp_json_encode($this->control_clean_payload($payload), JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES),
            'user_id'=>absint($user_id),
            'created_at'=>time(),
        ));
    }

    private function control_settings() {
        $settings = get_option(self::OPTION_CONTROL_SETTINGS, array());
        $settings = is_array($settings) ? $settings : array();
        return array(
            'emergency_stop'=>!empty($settings['emergency_stop']) ? 1 : 0,
            'emergency_reason'=>sanitize_text_field((string) ($settings['emergency_reason'] ?? '')),
            'updated_at'=>absint($settings['updated_at'] ?? 0),
            'updated_by'=>absint($settings['updated_by'] ?? 0),
        );
    }

    public function control_emergency_stop_active() {
        $settings = $this->control_settings();
        return !empty($settings['emergency_stop']);
    }

    public function handle_control_save_global() {
        if (!current_user_can('manage_options')) {
            wp_die('Keine Berechtigung.');
        }
        check_admin_referer('ppar_control_save_global', 'ppar_control_nonce');
        $old = $this->control_settings();
        $new_stop = !empty($_POST['emergency_stop']) ? 1 : 0;
        $reason = sanitize_text_field((string) wp_unslash($_POST['emergency_reason'] ?? ''));
        if ($new_stop && $reason === '') {
            wp_safe_redirect(add_query_arg(array('page'=>'affiliate-portal-control','ppar_control'=>'failed','ppar_message'=>rawurlencode('Für die Notabschaltung ist eine Begründung erforderlich.')), admin_url('admin.php')));
            exit;
        }
        if (!$new_stop && $reason === '') {
            $reason = 'Globale Notabschaltung aufgehoben.';
        }
        $settings = array(
            'emergency_stop'=>$new_stop,
            'emergency_reason'=>$reason,
            'updated_at'=>time(),
            'updated_by'=>function_exists('get_current_user_id') ? absint(get_current_user_id()) : 0,
        );
        update_option(self::OPTION_CONTROL_SETTINGS, $settings, false);
        $this->control_log_event('global_emergency_stop', '', 'output', 'global', !empty($old['emergency_stop']) ? 'paused' : 'automatic', $new_stop ? 'paused' : 'automatic', $reason, array());
        wp_safe_redirect(add_query_arg(array('page'=>'affiliate-portal-control','ppar_control'=>'success','ppar_message'=>rawurlencode($new_stop ? 'Globale Affiliate-Ausgabe sofort pausiert.' : 'Globale Notabschaltung aufgehoben; vorherige Einzelentscheidungen gelten wieder.')), admin_url('admin.php')));
        exit;
    }

    /**
     * Ein Veto ist immer die letzte fachliche Instanz: Es darf jede automatische
     * oder manuelle Freigabe blockieren. Umgekehrt kann eine manuelle Freigabe
     * niemals einen technischen/rechtlichen Sicherheitsblocker erzwingen.
     */
    private function control_manual_block($portal_key, $scope_type, $scope_key) {
        $decision = $this->control_get_decision($portal_key, $scope_type, $scope_key);
        if (empty($decision['exists'])) { return true; }
        $status = sanitize_key((string) ($decision['status'] ?? 'automatic'));
        if ($status === 'veto') {
            return new WP_Error('control_' . sanitize_key((string) $scope_type) . '_veto', (string) ($decision['reason'] ?: 'Manuelles Chef-Veto ist aktiv.'));
        }
        if ($status === 'paused' && in_array(sanitize_key((string) $scope_type), array('provider','output'), true)) {
            return new WP_Error('control_' . sanitize_key((string) $scope_type) . '_paused', (string) ($decision['reason'] ?: 'Manuelle Pause ist aktiv.'));
        }
        return true;
    }

    public function control_provider_gate($provider, $portal_key) {
        $provider = sanitize_key((string) $provider);
        $portal_key = sanitize_key((string) $portal_key);
        if ($provider === '' || $portal_key === '') {
            return new WP_Error('control_provider_context_missing', 'Provider- oder Portalkontext fehlt.');
        }
        if (method_exists($this, 'provider_exists') && !$this->provider_exists($provider)) {
            return new WP_Error('control_provider_unknown', 'Provider ist nicht im zentralen Providerregister registriert.');
        }

        // Nicht übersteuerbare Provider-Basis: ein deaktivierter/vorbereiteter
        // Provider oder ein bewusst ausgeschalteter/unvollständiger Zugang darf
        // weder durch Automatik noch durch eine manuelle Freigabe publizieren.
        if (method_exists($this, 'provider_definition')) {
            $definition = $this->provider_definition($provider);
            $state = is_array($definition) ? sanitize_key((string) ($definition['state'] ?? 'prepared')) : 'prepared';
            if ($state !== 'active') {
                return new WP_Error('control_provider_not_operational', 'Provider ist nicht für den produktiven Betrieb freigegeben.');
            }
            if (method_exists($this, 'provider_supports') && $this->provider_supports($provider, 'credentials') && method_exists($this, 'provider_access_snapshot')) {
                $access = $this->provider_access_snapshot($provider);
                if (empty($access['configured'])) {
                    return new WP_Error('control_provider_credentials_missing', 'Provider-Zugang ist nicht vollständig konfiguriert.');
                }
                if (empty($access['enabled'])) {
                    return new WP_Error('control_provider_access_disabled', 'Provider-Zugang ist zentral deaktiviert.');
                }
            }
        }

        // Chef-Veto kommt nach den unverrückbaren Sicherheitsblockern und ist
        // danach die letzte menschliche Stop-Instanz über Automatik/Freigaben.
        return $this->control_manual_block($portal_key, 'provider', $provider);
    }

    public function control_target_gate($portal_key, $target_key) {
        $portal_key = sanitize_key((string) $portal_key);
        $target_key = sanitize_text_field((string) $target_key);
        if ($portal_key === '' || $target_key === '') { return true; }
        return $this->control_manual_block($portal_key, 'target', $target_key);
    }

    public function control_slot_gate($portal_key, $slot_id) {
        $portal_key = sanitize_key((string) $portal_key);
        $slot_id = sanitize_key((string) $slot_id);
        if ($portal_key === '' || $slot_id === '') { return true; }
        return $this->control_manual_block($portal_key, 'slot', $slot_id);
    }

    public function control_output_gate($portal_key, $output_key) {
        $portal_key = sanitize_key((string) $portal_key);
        $output_key = sanitize_text_field((string) $output_key);
        if ($portal_key === '' || $output_key === '') { return true; }
        return $this->control_manual_block($portal_key, 'output', $output_key);
    }

    /**
     * Zentrale Providerweiche. Neue Provider registrieren ausschließlich einen
     * Filter/Adapter; die Steuerlogik bleibt im Kern.
     */
    public function control_partner_gate($row, $portal) {
        if (!is_array($row) || !is_array($portal)) {
            return new WP_Error('control_partner_context_missing', 'Partner- oder Portalkontext fehlt.');
        }
        $provider = sanitize_key((string) ($row['provider'] ?? ''));
        $partner_id = sanitize_text_field((string) ($row['partner_external_id'] ?? ''));
        $portal_key = sanitize_key((string) ($portal['key'] ?? ''));
        if ($provider === '' || $partner_id === '' || $portal_key === '') {
            return new WP_Error('control_partner_identity_missing', 'Provider, Partner-ID oder Portal-ID fehlt.');
        }
        $provider_gate = $this->control_provider_gate($provider, $portal_key);
        if (is_wp_error($provider_gate)) { return $provider_gate; }
        if ($provider === 'awin' && method_exists($this, 'awin_programme_gate_validate')) {
            $awin = $this->awin_programme_gate_validate(absint($partner_id), $portal_key);
            if (is_wp_error($awin)) {
                return $awin;
            }
        }
        $partner_key = $provider . ':' . $partner_id;
        $manual_block = $this->control_manual_block($portal_key, 'partner', $partner_key);
        if (is_wp_error($manual_block)) { return $manual_block; }
        $manual = $this->control_get_decision($portal_key, 'partner', $partner_key);
        if (!empty($manual['exists']) && (string) $manual['status'] === 'review') {
            return new WP_Error('control_partner_review', (string) ($manual['reason'] ?: 'Partner wartet auf eine Chefentscheidung.'));
        }
        $filtered = apply_filters('ppar_affiliate_partner_gate_result', true, $row, $portal, self::CONTROL_CONTRACT_VERSION);
        return is_wp_error($filtered) ? $filtered : ($filtered === true ? true : new WP_Error('control_partner_adapter_blocked', 'Provideradapter hat den Partner fail-closed blockiert.'));
    }

    /** Nicht übersteuerbare technische/rechtliche Sicherheitsblocker. */
    public function control_creative_safety_check($row, $portal, $stage = 'plan') {
        if ($this->control_emergency_stop_active() && in_array(sanitize_key((string) $stage), array('materialize','publish','runtime'), true)) {
            return new WP_Error('control_emergency_stop_active', 'Globale Affiliate-Notabschaltung ist aktiv.');
        }
        $partner = $this->control_partner_gate($row, $portal);
        if (is_wp_error($partner)) {
            return $partner;
        }
        if ((string) ($row['source_status'] ?? 'active') !== 'active' || (string) ($row['availability_state'] ?? 'active') !== 'active') {
            return new WP_Error('control_source_inactive', 'Creative-Quelle ist nicht aktiv.');
        }
        $tracking = trim((string) ($row['tracking_url'] ?? ''));
        $image = trim((string) ($row['image_url'] ?? ''));
        if ($tracking === '' || !preg_match('#^https?://#i', $tracking)) {
            return new WP_Error('control_tracking_invalid', 'Gültiger Affiliate-Trackinglink fehlt.');
        }
        if ($image === '' || !preg_match('#^https?://#i', $image)) {
            return new WP_Error('control_image_invalid', 'Gültige Creative-Bildquelle fehlt.');
        }
        if (absint($row['width'] ?? 0) <= 0 || absint($row['height'] ?? 0) <= 0) {
            return new WP_Error('control_dimensions_missing', 'Reale Bildmaße fehlen.');
        }
        $payload = json_decode((string) ($row['payload'] ?? ''), true);
        $payload = is_array($payload) ? $payload : array();
        if (!in_array((string) ($payload['_dimension_state'] ?? ''), array('verified','mismatch'), true)) {
            return new WP_Error('control_image_not_verified', 'Bilddatei ist noch nicht technisch verifiziert.');
        }
        $filtered = apply_filters('ppar_affiliate_non_overridable_safety_check', true, $row, $portal, sanitize_key((string) $stage), self::CONTROL_CONTRACT_VERSION);
        return is_wp_error($filtered) ? $filtered : ($filtered === true ? true : new WP_Error('control_provider_safety_blocked', 'Provider-Sicherheitsprüfung hat das Creative blockiert.'));
    }

    private function control_migrate_existing_decisions($previous_version) {
        if (version_compare((string) $previous_version, '1.0', '>=')) {
            return;
        }
        global $wpdb;
        $legacy_output_schema = (string) get_option(self::OPTION_OUTPUT_SCHEMA_VERSION, '');
        if ($legacy_output_schema !== '' && method_exists($this, 'output_portal_decisions_table')) {
            $legacy = $wpdb->get_results("SELECT * FROM {$this->output_portal_decisions_table()}", ARRAY_A);
            foreach ((array) $legacy as $row) {
                $portal_key = sanitize_key((string) ($row['portal_key'] ?? ''));
                $hash = strtolower(sanitize_text_field((string) ($row['creative_identity_hash'] ?? '')));
                $status = sanitize_key((string) ($row['manual_status'] ?? 'automatic'));
                if ($portal_key === '' || !preg_match('/^[a-f0-9]{64}$/', $hash) || !in_array($status, array('automatic','approved','review','veto'), true)) {
                    continue;
                }
                $legacy_reason = sanitize_text_field((string) ($row['reason'] ?? ''));
                if ($status !== 'automatic' && $legacy_reason === '') {
                    $legacy_reason = 'Bestehende Portalentscheidung aus V4.3.1 migriert.';
                }
                $this->control_set_decision($portal_key, 'creative', $hash, $status, $legacy_reason, array(), 'migration');
            }
        }
        if (method_exists($this, 'awin_programme_gate_records') && method_exists($this, 'output_local_portal_key')) {
            $portal_key = $this->output_local_portal_key();
            foreach ((array) $this->awin_programme_gate_records() as $id => $entry) {
                $status = sanitize_key((string) ($entry['status'] ?? 'pending'));
                $mapped = $status === 'allow_local' ? 'approved' : ($status === 'pending' ? 'review' : 'veto');
                $reason = 'Awin-Eingangsweiche migriert: ' . $status . '.';
                $this->control_set_decision($portal_key, 'partner', 'awin:' . absint($id), $mapped, $reason, array('provider'=>'awin','partner_external_id'=>(string) absint($id)), 'migration');
            }
        }
    }

    public function handle_control_save_decision() {
        if (!current_user_can('manage_options')) { wp_die('Keine Berechtigung.'); }
        check_admin_referer('ppar_control_save_decision', 'ppar_control_nonce');
        $portal_key = sanitize_key((string) ($_POST['portal_key'] ?? ''));
        $scope_type = sanitize_key((string) ($_POST['scope_type'] ?? ''));
        $scope_key = sanitize_text_field((string) wp_unslash($_POST['scope_key'] ?? ''));
        $status = sanitize_key((string) ($_POST['status'] ?? 'automatic'));
        $reason = sanitize_text_field((string) wp_unslash($_POST['reason'] ?? ''));
        if ($portal_key === '' && method_exists($this, 'output_local_portal_key')) { $portal_key = $this->output_local_portal_key(); }
        $result = $this->control_set_decision($portal_key, $scope_type, $scope_key, $status, $reason, array(), 'manual_control_center');
        $args = array('page'=>'affiliate-portal-control');
        if (is_wp_error($result)) {
            $args['ppar_control'] = 'failed';
            $args['ppar_message'] = rawurlencode($result->get_error_message());
        } else {
            $args['ppar_control'] = 'success';
            $args['ppar_message'] = rawurlencode($status === 'automatic' ? 'Chefentscheidung zurückgenommen; Automatik gilt wieder.' : 'Chefentscheidung gespeichert.');
        }
        wp_safe_redirect(add_query_arg($args, admin_url('admin.php')));
        exit;
    }

    public function render_control_page() {
        if (!current_user_can('manage_options')) {
            wp_die('Keine Berechtigung.');
        }
        $this->maybe_install_control_contract_schema();
        $settings = $this->control_settings();
        global $wpdb;
        $audit = $wpdb->get_results("SELECT * FROM {$this->control_audit_table()} ORDER BY id DESC LIMIT 100", ARRAY_A);
        $notice = sanitize_key((string) ($_GET['ppar_control'] ?? ''));
        $message = rawurldecode((string) ($_GET['ppar_message'] ?? ''));
        $prefill_scope_type = sanitize_key((string) ($_GET['scope_type'] ?? 'provider'));
        if (!in_array($prefill_scope_type, $this->control_allowed_scope_types(), true)) { $prefill_scope_type = 'provider'; }
        $prefill_scope_key = sanitize_text_field((string) wp_unslash($_GET['scope_key'] ?? ''));
        ?>
        <div class="wrap">
            <h1>Steuerung &amp; Veto</h1>
            <p><strong>Providerunabhängiger Steuervertrag <?php echo esc_html(self::CONTROL_CONTRACT_VERSION); ?></strong>: Technische/rechtliche Sicherheitsblocker bleiben fail-closed. Chef-Veto kann jede Ausgabe jederzeit stoppen und ist die letzte fachliche Instanz. Ohne Chefentscheidung arbeitet die Automatik.</p>
            <?php if ($notice === 'success') : ?><div class="notice notice-success inline"><p><?php echo esc_html($message); ?></p></div><?php endif; ?>
            <?php if ($notice === 'failed') : ?><div class="notice notice-error inline"><p><?php echo esc_html($message); ?></p></div><?php endif; ?>
            <form method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>" style="background:#fff;border:1px solid #c3c4c7;padding:20px;max-width:900px">
                <input type="hidden" name="action" value="ppar_control_save_global">
                <?php wp_nonce_field('ppar_control_save_global', 'ppar_control_nonce'); ?>
                <h2>Globale Notabschaltung</h2>
                <p><label><input type="checkbox" name="emergency_stop" value="1" <?php checked(!empty($settings['emergency_stop'])); ?>> <strong>Alle öffentlichen Affiliate-Ausgaben sofort pausieren</strong></label></p>
                <p><label><strong>Begründung</strong><br><input type="text" class="regular-text" style="width:min(760px,100%)" name="emergency_reason" value="<?php echo esc_attr((string) $settings['emergency_reason']); ?>"></label></p>
                <?php submit_button('Globale Steuerung speichern'); ?>
            </form>
            <h2 style="margin-top:28px">Chefentscheidung setzen</h2>
            <form method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>" style="background:#fff;border:1px solid #c3c4c7;padding:20px;max-width:900px">
                <input type="hidden" name="action" value="ppar_control_save_decision">
                <?php wp_nonce_field('ppar_control_save_decision', 'ppar_control_nonce'); ?>
                <table class="form-table" role="presentation"><tbody>
                    <tr><th>Portal</th><td><input class="regular-text" name="portal_key" value="<?php echo esc_attr(method_exists($this,'output_local_portal_key') ? $this->output_local_portal_key() : ''); ?>"><p class="description">Leer nur bei nicht-portalgebundenen Sonderfällen; normalerweise lokales Portal.</p></td></tr>
                    <tr><th>Ebene</th><td><select name="scope_type"><option value="provider" <?php selected($prefill_scope_type,'provider'); ?>>Provider/Netzwerk</option><option value="partner" <?php selected($prefill_scope_type,'partner'); ?>>Partner/Advertiser</option><option value="creative" <?php selected($prefill_scope_type,'creative'); ?>>Creative/Werbemittel</option><option value="target" <?php selected($prefill_scope_type,'target'); ?>>Portalziel</option><option value="slot" <?php selected($prefill_scope_type,'slot'); ?>>Designslot</option><option value="output" <?php selected($prefill_scope_type,'output'); ?>>Ausgabeobjekt</option></select></td></tr>
                    <tr><th>Objektschlüssel</th><td><input class="regular-text" name="scope_key" value="<?php echo esc_attr($prefill_scope_key); ?>" required><p class="description">Provider z. B. <code>ebay</code>; Partner z. B. <code>awin:118619</code>; Creative = Identity-Hash; Ziel/Slot = exakter Schlüssel; Ausgabe = Objekt-ID oder z. B. <code>ebay-listing:123</code>. Feste Ziel-/Slot-Zuordnungen je Creative werden unter „Import &amp; Auswahl“ gesetzt.</p></td></tr>
                    <tr><th>Entscheidung</th><td><select name="status"><option value="veto">Veto / sperren</option><option value="paused">Pausieren (Provider/Ausgabe)</option><option value="approved">Freigeben</option><option value="review">Zur Prüfung (Partner/Creative)</option><option value="automatic">Zur Automatik zurückkehren</option></select><p class="description">Nicht passende Kombinationen werden fail-closed abgelehnt.</p></td></tr>
                    <tr><th>Begründung</th><td><input class="regular-text" style="width:min(760px,100%)" name="reason"><p class="description">Für jede manuelle Entscheidung außer Rückkehr zur Automatik verpflichtend.</p></td></tr>
                </tbody></table>
                <?php submit_button('Chefentscheidung speichern'); ?>
            </form>
            <?php $active_decisions=$wpdb->get_results("SELECT * FROM {$this->control_decisions_table()} WHERE status<>'automatic' ORDER BY updated_at DESC LIMIT 100", ARRAY_A); ?>
            <h2 style="margin-top:28px">Aktive Chefentscheidungen</h2>
            <table class="widefat striped"><thead><tr><th>Portal</th><th>Ebene</th><th>Objekt</th><th>Status</th><th>Begründung</th><th>Geändert</th></tr></thead><tbody>
            <?php if (!$active_decisions) : ?><tr><td colspan="6">Keine aktiven manuellen Entscheidungen.</td></tr><?php endif; ?>
            <?php foreach ((array) $active_decisions as $row) : ?><tr><td><?php echo esc_html((string)$row['portal_key']); ?></td><td><?php echo esc_html((string)$row['scope_type']); ?></td><td><?php echo esc_html((string)$row['scope_key']); ?></td><td><strong><?php echo esc_html((string)$row['status']); ?></strong></td><td><?php echo esc_html((string)$row['reason']); ?></td><td><?php echo esc_html(wp_date('d.m.Y H:i:s', absint($row['updated_at']))); ?></td></tr><?php endforeach; ?>
            </tbody></table>
            <h2 style="margin-top:28px">Entscheidungshistorie</h2>
            <table class="widefat striped"><thead><tr><th>Zeit</th><th>Benutzer</th><th>Ebene</th><th>Objekt</th><th>Änderung</th><th>Begründung</th></tr></thead><tbody>
            <?php if (!$audit) : ?><tr><td colspan="6">Noch keine protokollierten Chefentscheidungen.</td></tr><?php endif; ?>
            <?php foreach ((array) $audit as $row) : $audit_user=function_exists('get_userdata')?get_userdata(absint($row['user_id']??0)):null; ?>
                <tr><td><?php echo esc_html(wp_date('d.m.Y H:i:s', absint($row['created_at'] ?? 0))); ?></td><td><?php echo esc_html($audit_user ? (string) $audit_user->display_name . ' (#' . absint($row['user_id'] ?? 0) . ')' : '#' . absint($row['user_id'] ?? 0)); ?></td><td><?php echo esc_html((string) $row['scope_type']); ?></td><td><?php echo esc_html((string) $row['scope_key']); ?></td><td><?php echo esc_html((string) $row['old_status'] . ' → ' . (string) $row['new_status']); ?></td><td><?php echo esc_html((string) $row['reason']); ?></td></tr>
            <?php endforeach; ?>
            </tbody></table>
        </div>
        <?php
    }
}
