<?php
if (!defined('ABSPATH')) {
    exit;
}

/**
 * Provider Registry / Provider-Vertrag V2.0.
 *
 * Ziel:
 * - Zugänge und Verbindungsstatus aller Provider zentral verwalten.
 * - Provider-spezifische Betriebslogik in eigenen Fachseiten kapseln.
 * - Partner, Creatives, Ziele, Slots und Ausgaben weiterhin zentral steuern.
 * - Neue Provider registrieren sich über einen einzigen Registry-Filter und
 *   optional Adapter-Hooks, ohne den zentralen Steuervertrag umzubauen.
 */
trait PPAR_Provider_Registry_Trait {
    private function provider_registry_defaults() {
        return array(
            'awin' => array(
                'label' => 'Awin',
                'state' => 'active',
                'access_owner' => 'core',
                'specialist_menu' => true,
                'specialist_slug' => 'affiliate-portal-provider-awin',
                'capabilities' => array('credentials','connection_test','programmes','partners','offers','product_feeds','synchronization','automation','creatives','outputs','veto'),
            ),
            'adcell' => array(
                'label' => 'ADCELL',
                'state' => 'active',
                'access_owner' => 'core',
                'specialist_menu' => true,
                'specialist_slug' => 'affiliate-portal-provider-adcell',
                'capabilities' => array('credentials','connection_test','partners','product_feeds','synchronization','automation','creatives','outputs','veto'),
            ),
            'ebay' => array(
                'label' => 'eBay',
                'state' => 'active',
                'access_owner' => 'core',
                'specialist_menu' => true,
                'specialist_slug' => 'affiliate-portal-ebay',
                'capabilities' => array('credentials','connection_test','marketplace','account_deletion_notifications','partners','private_listings','business_products','synchronization','automation','creatives','outputs','veto'),
            ),
            'amazon' => array(
                'label' => 'Amazon',
                'state' => 'prepared',
                'access_owner' => 'adapter',
                'specialist_menu' => false,
                'specialist_slug' => 'affiliate-portal-provider-amazon',
                'capabilities' => array('creatives','outputs','veto'),
            ),
            'idealo' => array(
                'label' => 'idealo',
                'state' => 'prepared',
                'access_owner' => 'adapter',
                'specialist_menu' => false,
                'specialist_slug' => 'affiliate-portal-provider-idealo',
                'capabilities' => array('creatives','outputs','veto'),
            ),
            'direct' => array(
                'label' => 'Direktpartner',
                'state' => 'active',
                'access_owner' => 'none',
                'specialist_menu' => false,
                'specialist_slug' => '',
                'capabilities' => array('partners','creatives','outputs','veto'),
            ),
            'manual' => array(
                'label' => 'Manuell',
                'state' => 'active',
                'access_owner' => 'none',
                'specialist_menu' => false,
                'specialist_slug' => '',
                'capabilities' => array('creatives','outputs','veto'),
            ),
        );
    }

    public function provider_registry() {
        $raw = apply_filters('ppar_affiliate_provider_registry', $this->provider_registry_defaults(), self::PROVIDER_CONTRACT_VERSION);
        $raw = is_array($raw) ? $raw : array();
        $safe = array();
        foreach ($raw as $key => $provider) {
            $key = sanitize_key((string) $key);
            if ($key === '' || !is_array($provider)) { continue; }
            $caps = array_values(array_unique(array_filter(array_map('sanitize_key', (array) ($provider['capabilities'] ?? array())))));
            // Chef-Veto ist Bestandteil des Kernvertrags und darf von keinem Adapter entfernt werden.
            if (!in_array('veto', $caps, true)) { $caps[] = 'veto'; }
            $state = sanitize_key((string) ($provider['state'] ?? 'prepared'));
            if (!in_array($state, array('active','prepared','disabled'), true)) { $state = 'prepared'; }
            $access_owner = sanitize_key((string) ($provider['access_owner'] ?? 'adapter'));
            if (!in_array($access_owner, array('core','adapter','none'), true)) { $access_owner = 'adapter'; }
            $safe[$key] = array(
                'key' => $key,
                'label' => sanitize_text_field((string) ($provider['label'] ?? strtoupper($key))),
                'state' => $state,
                'access_owner' => $access_owner,
                'specialist_menu' => !empty($provider['specialist_menu']),
                'specialist_slug' => sanitize_key((string) ($provider['specialist_slug'] ?? '')),
                'capabilities' => $caps,
            );
        }
        return $safe;
    }

    public function provider_definition($provider) {
        $provider = sanitize_key((string) $provider);
        $registry = $this->provider_registry();
        return isset($registry[$provider]) ? $registry[$provider] : null;
    }

    public function provider_exists($provider) {
        return is_array($this->provider_definition($provider));
    }

    public function provider_supports($provider, $capability) {
        $definition = $this->provider_definition($provider);
        return is_array($definition) && in_array(sanitize_key((string) $capability), (array) $definition['capabilities'], true);
    }

    public function provider_label($provider) {
        $definition = $this->provider_definition($provider);
        return is_array($definition) ? (string) $definition['label'] : strtoupper(sanitize_key((string) $provider));
    }

    private function provider_access_state_all() {
        $state = get_option(self::OPTION_PROVIDER_ACCESS_STATE, array());
        return is_array($state) ? $state : array();
    }

    private function provider_access_state($provider) {
        $provider = sanitize_key((string) $provider);
        $all = $this->provider_access_state_all();
        $stored = isset($all[$provider]) && is_array($all[$provider]) ? $all[$provider] : array();
        return array_merge(array(
            'status' => 'not_configured',
            'last_checked' => 0,
            'message' => '',
            'updated_at' => 0,
        ), $stored);
    }

    private function provider_set_access_state($provider, $status, $message) {
        $provider = sanitize_key((string) $provider);
        $status = sanitize_key((string) $status);
        if (!$this->provider_exists($provider)) { return false; }
        if (!in_array($status, array('not_configured','credentials_saved','connected','failed','prepared'), true)) { $status = 'failed'; }
        $all = $this->provider_access_state_all();
        $all[$provider] = array(
            'status' => $status,
            'last_checked' => time(),
            'message' => sanitize_text_field((string) $message),
            'updated_at' => time(),
        );
        update_option(self::OPTION_PROVIDER_ACCESS_STATE, $all, false);
        return true;
    }

    private function provider_access_snapshot($provider) {
        $provider = sanitize_key((string) $provider);
        $definition = $this->provider_definition($provider);
        if (!$definition) { return array(); }
        $snapshot = array(
            'provider' => $provider,
            'label' => (string) $definition['label'],
            'state' => (string) $definition['state'],
            'configured' => false,
            'enabled' => false,
            'status' => 'not_configured',
            'last_checked' => 0,
            'message' => '',
        );
        if ((string) ($definition['access_owner'] ?? '') === 'none') {
            $snapshot['configured'] = true;
            $snapshot['enabled'] = (string) ($definition['state'] ?? '') === 'active';
            $snapshot['status'] = $snapshot['enabled'] ? 'not_required' : 'prepared';
            $snapshot['message'] = $snapshot['enabled'] ? 'Kein externer API-Zugang erforderlich.' : 'Provider ist noch nicht produktiv aktiviert.';
            return apply_filters('ppar_affiliate_provider_access_snapshot', $snapshot, $provider, $definition, self::PROVIDER_CONTRACT_VERSION);
        }
        if ($provider === 'awin') {
            $settings = $this->network_settings('awin');
            $snapshot['configured'] = $this->network_credentials_present('awin', $settings);
            $snapshot['enabled'] = !empty($settings['enabled']);
            $snapshot['status'] = sanitize_key((string) ($settings['last_status'] ?? ($snapshot['configured'] ? 'credentials_saved' : 'not_configured')));
            $snapshot['last_checked'] = absint($settings['last_checked'] ?? 0);
            $snapshot['message'] = sanitize_text_field((string) ($settings['last_message'] ?? ''));
            return apply_filters('ppar_affiliate_provider_access_snapshot', $snapshot, $provider, $definition, self::PROVIDER_CONTRACT_VERSION);
        }
        if ($provider === 'adcell') {
            $settings = $this->network_settings('adcell');
            $snapshot['configured'] = $this->network_credentials_present('adcell', $settings);
            $snapshot['enabled'] = !empty($settings['enabled']);
            $snapshot['status'] = sanitize_key((string) ($settings['last_status'] ?? ($snapshot['configured'] ? 'credentials_saved' : 'not_configured')));
            $snapshot['last_checked'] = absint($settings['last_checked'] ?? 0);
            $snapshot['message'] = sanitize_text_field((string) ($settings['last_message'] ?? ''));
            return apply_filters('ppar_affiliate_provider_access_snapshot', $snapshot, $provider, $definition, self::PROVIDER_CONTRACT_VERSION);
        }
        if ($provider === 'ebay' && method_exists($this, 'ebay_settings')) {
            $settings = $this->ebay_settings();
            $snapshot['configured'] = trim((string) ($settings['client_id'] ?? '')) !== ''
                && trim((string) ($settings['client_secret'] ?? '')) !== ''
                && preg_match('/^\d{10}$/', (string) ($settings['epn_campaign_id'] ?? ''));
            $snapshot['enabled'] = !empty($settings['enabled']);
            $state = $this->provider_access_state('ebay');
            $snapshot['status'] = $snapshot['configured'] ? sanitize_key((string) ($state['status'] ?? 'credentials_saved')) : 'not_configured';
            if ($snapshot['configured'] && $snapshot['status'] === 'not_configured') { $snapshot['status'] = 'credentials_saved'; }
            $snapshot['last_checked'] = absint($state['last_checked'] ?? 0);
            $snapshot['message'] = sanitize_text_field((string) ($state['message'] ?? ''));
            return apply_filters('ppar_affiliate_provider_access_snapshot', $snapshot, $provider, $definition, self::PROVIDER_CONTRACT_VERSION);
        }
        $state = $this->provider_access_state($provider);
        $snapshot['status'] = (string) ($definition['state'] === 'prepared' ? 'prepared' : $state['status']);
        $snapshot['last_checked'] = absint($state['last_checked'] ?? 0);
        $snapshot['message'] = sanitize_text_field((string) ($state['message'] ?? ''));
        return apply_filters('ppar_affiliate_provider_access_snapshot', $snapshot, $provider, $definition, self::PROVIDER_CONTRACT_VERSION);
    }

    private function provider_status_badge($snapshot) {
        $status = sanitize_key((string) ($snapshot['status'] ?? 'not_configured'));
        if ($status === 'connected') { return '<span class="ppar-network-status ppar-network-ok">Verbunden</span>'; }
        if ($status === 'credentials_saved' || $status === 'pending') { return '<span class="ppar-network-status ppar-network-saved">Zugangsdaten gespeichert</span>'; }
        if ($status === 'failed') { return '<span class="ppar-network-status ppar-network-failed">Prüfung fehlgeschlagen</span>'; }
        if ($status === 'prepared') { return '<span class="ppar-network-status ppar-network-neutral">Adapter vorbereitet</span>'; }
        if ($status === 'not_required') { return '<span class="ppar-network-status ppar-network-ok">Kein API-Zugang erforderlich</span>'; }
        return '<span class="ppar-network-status ppar-network-neutral">Nicht eingerichtet</span>';
    }

    /**
     * Sichtbarer Chefstatus eines Providers. Ein Veto ist kein Sonderpfad des
     * Providers, sondern ein zentraler Laufzeitblocker und deshalb für jeden
     * registrierten Provider identisch verfügbar.
     */
    private function provider_control_snapshot($provider) {
        $provider = sanitize_key((string) $provider);
        $snapshot = array('portal_key'=>'','status'=>'automatic','reason'=>'','exists'=>false);
        if ($provider === '' || !method_exists($this, 'control_get_decision') || !method_exists($this, 'output_local_portal_key')) {
            return $snapshot;
        }
        $portal_key = sanitize_key((string) $this->output_local_portal_key());
        if ($portal_key === '') { return $snapshot; }
        $decision = $this->control_get_decision($portal_key, 'provider', $provider);
        $snapshot['portal_key'] = $portal_key;
        if (!empty($decision['exists'])) {
            $snapshot['exists'] = true;
            $snapshot['status'] = sanitize_key((string) ($decision['status'] ?? 'automatic'));
            $snapshot['reason'] = sanitize_text_field((string) ($decision['reason'] ?? ''));
        }
        return $snapshot;
    }

    private function provider_control_badge($provider) {
        $control = $this->provider_control_snapshot($provider);
        $status = sanitize_key((string) ($control['status'] ?? 'automatic'));
        if ($status === 'veto') { return '<span class="ppar-network-status ppar-network-failed">Chef-Veto aktiv</span>'; }
        if ($status === 'paused') { return '<span class="ppar-network-status ppar-network-saved">Manuell pausiert</span>'; }
        if ($status === 'approved') { return '<span class="ppar-network-status ppar-network-ok">Manuell freigegeben</span>'; }
        return '<span class="ppar-network-status ppar-network-neutral">Chefsteuerung: Automatik</span>';
    }

    private function provider_control_url($provider) {
        return add_query_arg(array(
            'page' => 'affiliate-portal-control',
            'scope_type' => 'provider',
            'scope_key' => sanitize_key((string) $provider),
        ), admin_url('admin.php'));
    }

    /**
     * Zugänge der Kernprovider werden zentral gespeichert; Fachseiten verwalten
     * ausschließlich Betriebslogik. Weitere Provider übernehmen denselben
     * Vertrag über Registry- und Adapter-Hooks, ohne den Steuerkern umzubauen.
     */
    public function handle_provider_access_save() {
        if (!current_user_can('manage_options')) { wp_die('Keine Berechtigung.'); }
        $provider = sanitize_key((string) ($_POST['provider'] ?? ''));
        if (!$this->provider_exists($provider)) { wp_die('Unbekannter Provider.'); }
        check_admin_referer('ppar_provider_access_' . $provider, 'ppar_provider_nonce');
        $mode = sanitize_key((string) ($_POST['ppar_provider_action'] ?? 'save'));
        $raw = isset($_POST['ppar_provider'][$provider]) && is_array($_POST['ppar_provider'][$provider]) ? wp_unslash($_POST['ppar_provider'][$provider]) : array();
        $result = null;

        if (in_array($provider, array('awin','adcell'), true)) {
            $result = $this->persist_network_settings($provider, $raw);
            if (!is_wp_error($result)) {
                $settings = $this->network_settings($provider);
                $configured = $this->network_credentials_present($provider, $settings);
                $this->provider_set_access_state($provider, $configured ? 'credentials_saved' : 'not_configured', $configured ? $this->provider_label($provider) . '-Zugangsdaten gespeichert; Verbindung noch nicht geprüft.' : $this->provider_label($provider) . '-Zugang noch unvollständig.');
            }
        } elseif ($provider === 'ebay' && method_exists($this, 'ebay_settings')) {
            $previous = $this->ebay_settings();
            $input = $previous;
            $requested_enabled = !empty($raw['enabled']);
            $input['environment'] = in_array((string) ($raw['environment'] ?? ''), array('production','sandbox'), true) ? (string) $raw['environment'] : (string) ($previous['environment'] ?? 'production');
            $input['client_id'] = sanitize_text_field((string) ($raw['client_id'] ?? $previous['client_id'] ?? ''));
            $secret = trim((string) ($raw['client_secret'] ?? ''));
            if ($secret !== '') { $input['client_secret'] = $secret; }
            if (!empty($raw['remove_client_secret'])) { $input['client_secret'] = ''; }
            $input['epn_campaign_id'] = preg_replace('/\D+/', '', (string) ($raw['epn_campaign_id'] ?? $previous['epn_campaign_id'] ?? ''));
            $input['affiliate_reference_prefix'] = sanitize_key((string) ($raw['affiliate_reference_prefix'] ?? $previous['affiliate_reference_prefix'] ?? 'pferde-atelier'));
            $credentials_changed = (string) ($input['environment'] ?? '') !== (string) ($previous['environment'] ?? '')
                || (string) ($input['client_id'] ?? '') !== (string) ($previous['client_id'] ?? '')
                || (string) ($input['epn_campaign_id'] ?? '') !== (string) ($previous['epn_campaign_id'] ?? '')
                || $secret !== '' || !empty($raw['remove_client_secret']);
            $access_state_before = $this->provider_access_state('ebay');
            $credential_ready_for_use = trim((string) ($input['client_id'] ?? '')) !== ''
                && trim((string) ($input['client_secret'] ?? '')) !== ''
                && preg_match('/^\d{10}$/', (string) ($input['epn_campaign_id'] ?? ''));
            $compliance_ready = (string) ($input['environment'] ?? 'production') === 'sandbox'
                || (method_exists($this, 'ebay_deletion_compliance_complete') && $this->ebay_deletion_compliance_complete());
            // Production bleibt bei jeder Credential-Aenderung und bis zur vollstaendigen
            // Account-Deletion-Compliance hart deaktiviert. Auch ein erfolgreicher OAuth-Test
            // darf die Nutzung ohne vollstaendige Affiliate-Konfiguration (inkl. 10-stelliger
            // EPN-Campaign-ID) nicht aktivieren. Danach ist ein bewusster Speicherschritt noetig.
            $input['enabled'] = $requested_enabled && $credential_ready_for_use && !$credentials_changed && $compliance_ready
                && (string) ($access_state_before['status'] ?? '') === 'connected';
            $settings = $this->ebay_normalize_settings($input, true);
            update_option(self::OPTION_NETWORK_EBAY, $settings, false);
            if (function_exists('delete_transient')) { delete_transient($this->ebay_token_cache_key($settings)); }
            $this->reschedule_ebay_cron(true);
            $saved = $this->ebay_settings();
            $expected_secret = trim((string) ($settings['client_secret'] ?? ''));
            $roundtrip_ok = (string) ($saved['environment'] ?? '') === (string) ($settings['environment'] ?? '')
                && (string) ($saved['client_id'] ?? '') === (string) ($settings['client_id'] ?? '')
                && (string) ($saved['epn_campaign_id'] ?? '') === (string) ($settings['epn_campaign_id'] ?? '')
                && ($expected_secret === '' || trim((string) ($saved['client_secret'] ?? '')) !== '');
            if (!$roundtrip_ok) {
                $result = new WP_Error('provider_access_roundtrip_failed', 'eBay-Zugangsdaten konnten nicht vollständig zurückgelesen werden.');
            } else {
                $configured = trim((string) ($saved['client_id'] ?? '')) !== '' && trim((string) ($saved['client_secret'] ?? '')) !== '' && preg_match('/^\d{10}$/', (string) ($saved['epn_campaign_id'] ?? ''));
                $production_compliance_missing = $configured
                    && (string) ($saved['environment'] ?? 'production') === 'production'
                    && method_exists($this, 'ebay_deletion_compliance_complete')
                    && !$this->ebay_deletion_compliance_complete();

                // Ein reiner Speichervorgang mit unveränderten Zugangsdaten darf einen
                // bereits real erfolgreich geprüften OAuth-Status niemals vernichten.
                // Genau dieser Statusverlust blockierte in V5.2.0 anschließend das Feld
                // „Verbindung verwenden“, obwohl Challenge, signierte Notification und
                // OAuth bereits erfolgreich waren. Nur echte Credential-/Compliance-
                // Änderungen erzwingen eine erneute Prüfung.
                if (!$configured) {
                    $this->provider_set_access_state('ebay', 'not_configured', 'eBay-Zugang noch unvollständig.');
                } elseif ($production_compliance_missing) {
                    $this->provider_set_access_state('ebay', 'credentials_saved', 'eBay-Zugangsdaten gespeichert; Production bleibt bis zur Account-Deletion-Compliance deaktiviert.');
                } elseif ($credentials_changed) {
                    $this->provider_set_access_state('ebay', 'credentials_saved', 'eBay-Zugangsdaten geändert; erneuter OAuth-Test erforderlich.');
                } elseif ((string) ($access_state_before['status'] ?? '') === 'connected') {
                    // Absichtlich keine Statusmutation: last_checked und die reale
                    // OAuth-Erfolgsmeldung bleiben als Evidenz des letzten Tests erhalten.
                } else {
                    $message = $requested_enabled && empty($saved['enabled'])
                        ? 'eBay-Zugangsdaten gespeichert; Verbindung bleibt bis zum erfolgreichen OAuth-Test bewusst deaktiviert.'
                        : 'eBay-Zugangsdaten gespeichert; Verbindung noch nicht geprüft.';
                    $this->provider_set_access_state('ebay', 'credentials_saved', $message);
                }
                $result = $saved;
            }
        } else {
            $handled = apply_filters('ppar_affiliate_provider_access_save', null, $provider, $raw, self::PROVIDER_CONTRACT_VERSION);
            $result = $handled === null ? new WP_Error('provider_access_handler_missing', 'Für diesen Provider ist noch kein Zugangsdaten-Adapter registriert.') : $handled;
        }

        if (!is_wp_error($result) && $mode === 'save_test') {
            $result = $this->provider_test_access($provider);
        }
        $args = array('page'=>'affiliate-portal-networks');
        if (is_wp_error($result)) {
            $args['ppar_provider_error'] = rawurlencode($result->get_error_message());
            $args['ppar_provider'] = $provider;
        } else {
            $args['ppar_provider_saved'] = $provider;
            if ($mode === 'save_test') { $args['ppar_provider_tested'] = $provider; }
        }
        wp_safe_redirect(add_query_arg($args, admin_url('admin.php')));
        exit;
    }

    private function provider_test_access($provider) {
        $provider = sanitize_key((string) $provider);
        if ($provider === 'awin') {
            $result = $this->test_awin_connection();
            $settings = $this->network_settings('awin');
            $settings['last_status'] = (string)($result['status'] ?? 'failed');
            $settings['last_checked'] = time();
            $settings['last_message'] = sanitize_text_field((string)($result['message'] ?? ''));
            $settings['programme_count'] = absint($result['programme_count'] ?? $settings['programme_count'] ?? 0);
            $settings['feed_status'] = sanitize_key((string)($result['feed_status'] ?? $settings['feed_status'] ?? 'not_configured'));
            $settings['feed_count'] = absint($result['feed_count'] ?? $settings['feed_count'] ?? 0);
            update_option(self::OPTION_NETWORK_AWIN, $settings, false);
            $status = (string)($result['status'] ?? '') === 'connected' ? 'connected' : ((string)($result['status'] ?? '') === 'failed' ? 'failed' : 'credentials_saved');
            $this->provider_set_access_state('awin', $status, (string)($result['message'] ?? 'Awin-Verbindungstest abgeschlossen.'));
            return (string)($result['status'] ?? '') === 'failed' ? new WP_Error('awin_connection_failed', (string)($result['message'] ?? 'Awin-Verbindungstest fehlgeschlagen.')) : $result;
        }
        if ($provider === 'adcell') {
            $result = $this->test_adcell_connection();
            $settings = $this->network_settings('adcell');
            $settings['last_status'] = (string)($result['status'] ?? 'failed');
            $settings['last_checked'] = time();
            $settings['last_message'] = sanitize_text_field((string)($result['message'] ?? ''));
            update_option(self::OPTION_NETWORK_ADCELL, $settings, false);
            $status = (string)($result['status'] ?? '') === 'connected' ? 'connected' : ((string)($result['status'] ?? '') === 'failed' ? 'failed' : 'credentials_saved');
            $this->provider_set_access_state('adcell', $status, (string)($result['message'] ?? 'ADCELL-Verbindungstest abgeschlossen.'));
            return (string)($result['status'] ?? '') === 'failed' ? new WP_Error('adcell_connection_failed', (string)($result['message'] ?? 'ADCELL-Verbindungstest fehlgeschlagen.')) : $result;
        }
        if ($provider === 'ebay' && method_exists($this, 'ebay_settings') && method_exists($this, 'ebay_access_token')) {
            $settings = $this->ebay_settings();
            if (trim((string) ($settings['client_id'] ?? '')) === '' || trim((string) ($settings['client_secret'] ?? '')) === '') {
                $this->provider_set_access_state('ebay', 'not_configured', 'Client-ID oder Client-Secret fehlt.');
                return new WP_Error('ebay_credentials_missing', 'Client-ID oder Client-Secret fehlt.');
            }
            if ((string) ($settings['environment'] ?? 'production') === 'production'
                && (!method_exists($this, 'ebay_deletion_challenge_answered') || !$this->ebay_deletion_challenge_answered())) {
                $message = 'eBay Production bleibt gesperrt, bis eBay den Marketplace-Account-Deletion-Endpoint per Challenge aufgerufen hat.';
                $this->provider_set_access_state('ebay', 'credentials_saved', $message);
                return new WP_Error('ebay_deletion_challenge_pending', $message);
            }
            $token = $this->ebay_access_token($settings, true);
            if (is_wp_error($token)) {
                $this->provider_set_access_state('ebay', 'failed', $token->get_error_message());
                return $token;
            }
            $this->provider_set_access_state('ebay', 'connected', 'eBay OAuth-Zugang erfolgreich authentifiziert.');
            return array('status'=>'connected');
        }
        $handled = apply_filters('ppar_affiliate_provider_access_test', null, $provider, self::PROVIDER_CONTRACT_VERSION);
        return $handled === null ? new WP_Error('provider_access_test_missing', 'Für diesen Provider ist noch kein Verbindungstest registriert.') : $handled;
    }

    public function provider_register_admin_menus($parent_slug) {
        foreach ($this->provider_registry() as $key => $provider) {
            if (empty($provider['specialist_menu']) || empty($provider['specialist_slug'])) { continue; }
            add_submenu_page(
                $parent_slug,
                (string) $provider['label'],
                (string) $provider['label'],
                'manage_options',
                (string) $provider['specialist_slug'],
                $key === 'ebay' ? array($this, 'render_ebay_page') : array($this, 'render_provider_specialist_page')
            );
        }
    }

    public function render_provider_specialist_page() {
        if (!current_user_can('manage_options')) { wp_die('Keine Berechtigung.'); }
        $page = sanitize_key((string) ($_GET['page'] ?? ''));
        $provider = '';
        foreach ($this->provider_registry() as $key => $definition) {
            if ((string) ($definition['specialist_slug'] ?? '') === $page) { $provider = $key; break; }
        }
        if ($provider === '') { wp_die('Unbekannte Provider-Fachseite.'); }
        $definition = $this->provider_definition($provider);
        $snapshot = $this->provider_access_snapshot($provider);
        ?>
        <div class="wrap" style="max-width:1180px">
            <h1><?php echo esc_html((string) $definition['label']); ?></h1>
            <p><strong>Provider-Fachseite.</strong> Zugangsdaten bleiben zentral unter <a href="<?php echo esc_url(admin_url('admin.php?page=affiliate-portal-networks')); ?>">Netzwerke &amp; API</a>. Hier liegt ausschließlich provider-spezifische Betriebslogik.</p>
            <p><?php echo $this->provider_status_badge($snapshot); ?> <?php echo $this->provider_control_badge($provider); ?> <a class="button button-small" href="<?php echo esc_url($this->provider_control_url($provider)); ?>">Chefsteuerung &amp; Veto</a></p>
            <?php if ($provider === 'awin') : $awin_settings=$this->network_settings('awin'); $awin_programmes=get_option(self::OPTION_NETWORK_AWIN_PROGRAMMES,array()); $awin_programmes=is_array($awin_programmes)?$awin_programmes:array(); ?>
                <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:16px">
                    <section class="postbox" style="padding:18px"><h2>Programme &amp; Partner</h2><p>Advertiser aufnehmen, Geschäftsbereich bestätigen und Portal-Freigabe steuern.</p><a class="button" href="<?php echo esc_url(admin_url('admin.php?page=affiliate-portal-partner-intake&provider=awin')); ?>">Awin-Partner öffnen</a></section>
                    <section class="postbox" style="padding:18px"><h2>Automatisierung</h2><p>Programmdaten, Offers und Produktfeeds in sicheren Arbeitspaketen verarbeiten.</p><a class="button" href="<?php echo esc_url(admin_url('admin.php?page=affiliate-portal-automation&provider=awin')); ?>">Awin-Automatisierung öffnen</a></section>
                    <section class="postbox" style="padding:18px"><h2>Synchronisierung</h2><p>Read-only Netzwerk- und Produktdatenläufe prüfen.</p><a class="button" href="<?php echo esc_url(admin_url('admin.php?page=affiliate-portal-sync')); ?>">Synchronisierung öffnen</a></section>
                </div>
                <section class="postbox" style="padding:18px;margin-top:18px;max-width:900px"><h2>Produktfeed-Betriebsprofil</h2><p>Diese Zuordnung ist Providerlogik und gehört deshalb nicht zu den zentralen Zugangsdaten.</p>
                    <form method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>"><input type="hidden" name="action" value="ppar_save_network"><input type="hidden" name="network" value="awin"><input type="hidden" name="ppar_network_action" value="save"><input type="hidden" name="return_page" value="affiliate-portal-provider-awin"><?php wp_nonce_field('ppar_save_network_awin','ppar_network_nonce'); ?>
                    <p><label>Awin-Produktfeed-Export-URL (optional)<br><input class="large-text" type="url" name="ppar_network[awin][product_feed_url]" value="<?php echo esc_attr((string)($awin_settings['product_feed_url']??'')); ?>"></label></p>
                    <p><label>Advertiser-ID dieses Produktfeeds<br><input type="number" min="1" step="1" name="ppar_network[awin][product_feed_partner_id]" value="<?php echo esc_attr((string)($awin_settings['product_feed_partner_id']??'')); ?>"></label></p>
                    <p class="description">Eine manuelle Export-URL gilt ausschließlich für diese Advertiser-ID. Ohne eindeutige Bindung bleibt der Produktimport fail-closed.</p><?php submit_button('Awin-Betriebsprofil speichern','secondary'); ?></form>
                </section>
                <?php if (method_exists($this,'render_awin_programme_gate_section')) { $this->render_awin_programme_gate_section($awin_programmes); } ?>
            <?php elseif ($provider === 'adcell') : $adcell_settings=$this->network_settings('adcell'); ?>
                <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:16px">
                    <section class="postbox" style="padding:18px"><h2>Produktdaten</h2><p>ADCELL-CSV-Export und technische Synchronisierung.</p><a class="button" href="<?php echo esc_url(admin_url('admin.php?page=affiliate-portal-sync')); ?>">Synchronisierung öffnen</a></section>
                    <section class="postbox" style="padding:18px"><h2>Automatisierung</h2><p>ADCELL-Daten in den zentralen Creative- und Ausgabeprozess überführen.</p><a class="button" href="<?php echo esc_url(admin_url('admin.php?page=affiliate-portal-automation&provider=adcell')); ?>">ADCELL-Automatisierung öffnen</a></section>
                </div>
                <section class="postbox" style="padding:18px;margin-top:18px;max-width:900px"><h2>Produktfeed-Betriebsprofil</h2><form method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>"><input type="hidden" name="action" value="ppar_save_network"><input type="hidden" name="network" value="adcell"><input type="hidden" name="ppar_network_action" value="save"><input type="hidden" name="return_page" value="affiliate-portal-provider-adcell"><?php wp_nonce_field('ppar_save_network_adcell','ppar_network_nonce'); ?><p><label>ADCELL-CSV-Export-URL (optional)<br><input class="large-text" type="url" name="ppar_network[adcell][csv_feed_url]" value="<?php echo esc_attr((string)($adcell_settings['csv_feed_url']??'')); ?>"></label></p><p class="description">Produktdatenquelle; sie ist bewusst von der zentralen API-Zugangsprüfung getrennt.</p><?php submit_button('ADCELL-Betriebsprofil speichern','secondary'); ?></form></section>
            <?php endif; ?>
            <?php do_action('ppar_affiliate_render_provider_specialist_' . $provider, $provider, $definition, self::PROVIDER_CONTRACT_VERSION); ?>
        </div>
        <?php
    }

    /**
     * Skalierbare Partnerübersicht. Feste WordPress-Menüpunkte pro Advertiser
     * sind ausdrücklich verboten; einzelne Partner bleiben Datensätze.
     */
    public function render_partner_directory_page() {
        if (!current_user_can('manage_options')) { wp_die('Keine Berechtigung.'); }
        $registry = $this->provider_registry();
        ?>
        <div class="wrap" style="max-width:1180px">
            <h1>Partner</h1>
            <p>Partner/Advertiser sind Datensätze innerhalb ihres Providers – keine festen WordPress-Menüpunkte. Chef-Veto und manuelle Freigaben gelten providerübergreifend.</p>
            <table class="widefat striped"><thead><tr><th>Provider</th><th>Status</th><th>Partnerverwaltung</th><th>Steuerung</th></tr></thead><tbody>
            <?php foreach ($registry as $key => $provider) : if (!in_array('partners', (array) $provider['capabilities'], true)) { continue; } $snapshot=$this->provider_access_snapshot($key); ?>
                <tr><td><strong><?php echo esc_html((string) $provider['label']); ?></strong></td><td><?php echo $this->provider_status_badge($snapshot); ?><br><?php echo $this->provider_control_badge($key); ?></td><td>
                    <?php if ($key === 'awin') : ?><a class="button" href="<?php echo esc_url(admin_url('admin.php?page=affiliate-portal-partner-intake&provider=awin')); ?>">Awin-Partner verwalten</a>
                    <?php elseif ($key === 'ebay') : ?><a class="button" href="<?php echo esc_url(admin_url('admin.php?page=affiliate-portal-ebay')); ?>">eBay-Verkäuferlogik öffnen</a>
                    <?php elseif (!empty($provider['specialist_menu']) && !empty($provider['specialist_slug'])) : ?><a class="button" href="<?php echo esc_url(admin_url('admin.php?page='.(string)$provider['specialist_slug'])); ?>">Provider-Fachseite öffnen</a>
                    <?php else : ?><?php do_action('ppar_affiliate_render_partner_directory_action_' . $key, $key, $provider, self::PROVIDER_CONTRACT_VERSION); ?><span class="description">Provideradapter/Import</span><?php endif; ?>
                </td><td><a class="button" href="<?php echo esc_url($this->provider_control_url($key)); ?>">Chefsteuerung &amp; Veto</a></td></tr>
            <?php endforeach; ?>
            </tbody></table>
        </div>
        <?php
    }
}
