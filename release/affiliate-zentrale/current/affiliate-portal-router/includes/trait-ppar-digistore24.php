<?php
if (!defined('ABSPATH')) {
    exit;
}

/**
 * Digistore24 adapter.
 *
 * Contract:
 * - read-only API access only;
 * - banner-only provider, never product/listing output;
 * - no provider-specific cron; use the central automation cursor only;
 * - manual partnership confirmation before vendor-banner import;
 * - provider-local failures never starve other automation providers.
 */
trait PPAR_Digistore24_Trait {
    private function digistore24_register_hooks() {
        add_filter('ppar_affiliate_provider_registry', array($this, 'digistore24_provider_registry'), 10, 2);
        add_filter('ppar_affiliate_provider_access_snapshot', array($this, 'digistore24_provider_access_snapshot'), 10, 4);
        add_filter('ppar_affiliate_provider_access_save', array($this, 'digistore24_provider_access_save'), 10, 4);
        add_filter('ppar_affiliate_provider_access_test', array($this, 'digistore24_provider_access_test'), 10, 4);
        add_filter('ppar_affiliate_automation_scheduled_sources', array($this, 'digistore24_automation_scheduled_sources'), 10, 3);
        add_filter('ppar_affiliate_automation_dispatch', array($this, 'digistore24_automation_dispatch'), 10, 5);
        add_action('ppar_affiliate_render_provider_access_card_digistore24', array($this, 'digistore24_render_access_card'), 10, 3);
        add_action('ppar_affiliate_render_provider_specialist_digistore24', array($this, 'digistore24_render_specialist'), 10, 3);
        add_action('admin_post_ppar_digistore24_marketplace_refresh', array($this, 'digistore24_handle_marketplace_refresh'));
        add_action('admin_post_ppar_digistore24_partnership', array($this, 'digistore24_handle_partnership'));
        add_action('admin_post_ppar_digistore24_import_banners', array($this, 'digistore24_handle_import_banners'));
    }

    public function digistore24_provider_registry($registry, $contract_version = '') {
        $registry = is_array($registry) ? $registry : array();
        $registry['digistore24'] = array(
            'label' => 'Digistore24',
            'state' => 'active',
            'access_owner' => 'adapter',
            'specialist_menu' => true,
            'specialist_slug' => 'affiliate-portal-provider-digistore24',
            'capabilities' => array('credentials','connection_test','marketplace','partners','automation','creatives','outputs','veto'),
        );
        return $registry;
    }

    private function digistore24_settings_defaults() {
        return array(
            'enabled' => false,
            'enable_requested' => false,
            'api_key' => '',
            'tested_key_fingerprint' => '',
            'affiliate_id' => '',
            'last_status' => 'not_configured',
            'last_checked' => 0,
            'last_message' => '',
        );
    }

    private function digistore24_settings() {
        $stored = get_option('ppar_network_digistore24_v1', array());
        $stored = is_array($stored) ? $stored : array();
        return array_merge($this->digistore24_settings_defaults(), $stored);
    }

    private function digistore24_normalize_affiliate_id($value) {
        $raw = trim(sanitize_text_field((string) $value));
        if ($raw === '') {
            return '';
        }
        $safe = preg_replace('/[^0-9A-Za-z._-]/', '', $raw);
        // Affiliate identity is attribution-critical: never silently rewrite the
        // API-reported ID into a different URL segment. Non-canonical values are
        // rejected until a real read-only API test provides an exact safe ID.
        return is_string($safe) && $safe !== '' && hash_equals($raw, $safe) ? $safe : '';
    }

    private function digistore24_update_settings($settings) {
        $settings = array_merge($this->digistore24_settings_defaults(), is_array($settings) ? $settings : array());
        $settings['enabled'] = !empty($settings['enabled']);
        $settings['enable_requested'] = !empty($settings['enable_requested']);
        $settings['api_key'] = trim((string) ($settings['api_key'] ?? ''));
        $settings['tested_key_fingerprint'] = preg_replace('/[^a-f0-9]/', '', strtolower((string) ($settings['tested_key_fingerprint'] ?? '')));
        $settings['affiliate_id'] = $this->digistore24_normalize_affiliate_id($settings['affiliate_id'] ?? '');
        $settings['last_status'] = sanitize_key((string) ($settings['last_status'] ?? 'not_configured'));
        $settings['last_checked'] = absint($settings['last_checked'] ?? 0);
        $settings['last_message'] = sanitize_text_field((string) ($settings['last_message'] ?? ''));
        update_option('ppar_network_digistore24_v1', $settings, false);
        return $settings;
    }

    private function digistore24_api_key($settings = null) {
        if (defined('PPAR_DIGISTORE24_API_KEY') && trim((string) PPAR_DIGISTORE24_API_KEY) !== '') {
            return trim((string) PPAR_DIGISTORE24_API_KEY);
        }
        $settings = is_array($settings) ? $settings : $this->digistore24_settings();
        return trim((string) ($settings['api_key'] ?? ''));
    }

    private function digistore24_key_fingerprint($key) {
        $key = trim((string) $key);
        return $key === '' ? '' : hash('sha256', $key);
    }

    private function digistore24_fingerprint_matches($settings = null) {
        $settings = is_array($settings) ? $settings : $this->digistore24_settings();
        $key = $this->digistore24_api_key($settings);
        $tested = strtolower(trim((string) ($settings['tested_key_fingerprint'] ?? '')));
        return $key !== '' && strlen($tested) === 64 && hash_equals($tested, $this->digistore24_key_fingerprint($key));
    }

    private function digistore24_automation_ready($settings = null) {
        $settings = is_array($settings) ? $settings : $this->digistore24_settings();
        $affiliate_id = $this->digistore24_normalize_affiliate_id($settings['affiliate_id'] ?? '');
        return !empty($settings['enabled'])
            && $this->digistore24_fingerprint_matches($settings)
            && $affiliate_id !== '';
    }

    public function digistore24_provider_access_snapshot($snapshot, $provider, $definition = array(), $contract_version = '') {
        if (sanitize_key((string) $provider) !== 'digistore24') {
            return $snapshot;
        }
        $settings = $this->digistore24_settings();
        $key = $this->digistore24_api_key($settings);
        $snapshot = is_array($snapshot) ? $snapshot : array();
        $snapshot['provider'] = 'digistore24';
        $snapshot['label'] = 'Digistore24';
        $snapshot['configured'] = $key !== '';
        $snapshot['enabled'] = $this->digistore24_automation_ready($settings);
        $snapshot['status'] = sanitize_key((string) ($settings['last_status'] ?? ($key !== '' ? 'credentials_saved' : 'not_configured')));
        $snapshot['last_checked'] = absint($settings['last_checked'] ?? 0);
        $snapshot['message'] = sanitize_text_field((string) ($settings['last_message'] ?? ''));
        if ($key === '') {
            $snapshot['status'] = 'not_configured';
            $snapshot['enabled'] = false;
        } elseif (!$this->digistore24_fingerprint_matches($settings) && $snapshot['status'] === 'connected') {
            $snapshot['status'] = 'credentials_saved';
            $snapshot['enabled'] = false;
        }
        return $snapshot;
    }

    public function digistore24_provider_access_save($handled, $provider, $raw, $contract_version = '') {
        if (sanitize_key((string) $provider) !== 'digistore24') {
            return $handled;
        }
        $raw = is_array($raw) ? $raw : array();
        $previous = $this->digistore24_settings();
        $settings = $previous;
        $mode = sanitize_key((string) ($_POST['ppar_provider_action'] ?? 'save'));
        $requested_enabled = !empty($raw['enabled']);
        $constant_key = defined('PPAR_DIGISTORE24_API_KEY') && trim((string) PPAR_DIGISTORE24_API_KEY) !== '';
        $submitted_key = trim((string) ($raw['api_key'] ?? ''));
        $remove_key = !$constant_key && !empty($raw['remove_api_key']);

        if (!$constant_key) {
            if ($submitted_key !== '') {
                $settings['api_key'] = $submitted_key;
            }
            if ($remove_key) {
                $settings['api_key'] = '';
            }
        }

        $old_key = $this->digistore24_api_key($previous);
        $new_key = $this->digistore24_api_key($settings);
        $credentials_changed = !hash_equals($this->digistore24_key_fingerprint($old_key), $this->digistore24_key_fingerprint($new_key));

        $settings['enable_requested'] = $requested_enabled;
        if ($credentials_changed || $new_key === '') {
            $settings['enabled'] = false;
            $settings['tested_key_fingerprint'] = '';
            $settings['affiliate_id'] = '';
            $settings['last_status'] = $new_key === '' ? 'not_configured' : 'credentials_saved';
            $settings['last_message'] = $new_key === ''
                ? 'Digistore24-API-Schlüssel fehlt; Provider bleibt deaktiviert.'
                : 'Digistore24-API-Schlüssel geändert; erneuter read-only API-Test erforderlich.';
            $settings['last_checked'] = 0;
        } else {
            $fingerprint_ok = $this->digistore24_fingerprint_matches($settings);
            $affiliate_id_ok = $this->digistore24_normalize_affiliate_id($settings['affiliate_id'] ?? '') !== '';
            $settings['enabled'] = $requested_enabled && $fingerprint_ok && $affiliate_id_ok;
            if (!$requested_enabled) {
                $settings['last_message'] = 'Digistore24-Verbindung gespeichert; Nutzung ist bewusst deaktiviert.';
            } elseif (!$fingerprint_ok || !$affiliate_id_ok) {
                $settings['last_status'] = 'credentials_saved';
                $settings['last_message'] = 'Digistore24-Zugang gespeichert; Aktivierung bleibt bis zum erfolgreichen read-only API-Test mit verwertbarer Affiliate-ID gesperrt.';
            }
        }

        // In save_test mode the subsequent generic test callback may fulfill the
        // remembered enable request in the same request, but never before PASS.
        if ($mode === 'save_test' && $new_key !== '') {
            $settings['enabled'] = false;
        }
        return $this->digistore24_update_settings($settings);
    }

    public function digistore24_provider_access_test($handled, $provider, $contract_version = '') {
        if (sanitize_key((string) $provider) !== 'digistore24') {
            return $handled;
        }
        $settings = $this->digistore24_settings();
        $key = $this->digistore24_api_key($settings);
        if ($key === '') {
            $current_settings = $this->digistore24_settings();
            if ($this->digistore24_api_key($current_settings) !== '') {
                return new WP_Error('digistore24_credentials_changed_during_test', 'Digistore24-Zugang wurde während des API-Tests geändert; Ergebnis wird verworfen und der neue Zugang bleibt unangetastet.');
            }
            $settings = $current_settings;
            $settings['enabled'] = false;
            $settings['last_status'] = 'not_configured';
            $settings['last_checked'] = time();
            $settings['last_message'] = 'Digistore24-API-Schlüssel fehlt.';
            $this->digistore24_update_settings($settings);
            return new WP_Error('digistore24_api_key_missing', 'Digistore24-API-Schlüssel fehlt.');
        }
        $request_key_fingerprint = $this->digistore24_key_fingerprint($key);
        $response = $this->digistore24_api_call('getUserInfo');
        if (is_wp_error($response)) {
            $current_settings = $this->digistore24_settings();
            $current_key_fingerprint = $this->digistore24_key_fingerprint($this->digistore24_api_key($current_settings));
            if (!hash_equals($request_key_fingerprint, $current_key_fingerprint)) {
                return new WP_Error('digistore24_credentials_changed_during_test', 'Digistore24-Zugang wurde während des API-Tests geändert; Fehler des alten Zugangs wird verworfen und der neue Zugang bleibt unangetastet.');
            }
            $settings = $current_settings;
            $settings['enabled'] = false;
            $settings['last_status'] = 'failed';
            $settings['last_checked'] = time();
            $settings['last_message'] = 'Read-only API-Test fehlgeschlagen: ' . $response->get_error_message();
            $this->digistore24_update_settings($settings);
            return $response;
        }
        $response_key_fingerprint = strtolower(trim((string) ($response['key_fingerprint'] ?? '')));
        $current_settings = $this->digistore24_settings();
        $current_key_fingerprint = $this->digistore24_key_fingerprint($this->digistore24_api_key($current_settings));
        if ($response_key_fingerprint === ''
            || !hash_equals($request_key_fingerprint, $response_key_fingerprint)
            || !hash_equals($current_key_fingerprint, $response_key_fingerprint)) {
            // A concurrent credential change must win. Never overwrite a newer
            // key with the stale settings snapshot that started this API test.
            return new WP_Error('digistore24_credentials_changed_during_test', 'Digistore24-Zugang wurde während des API-Tests geändert; Ergebnis wird verworfen und der neue Zugang bleibt unangetastet.');
        }
        $settings = $current_settings;
        $data = is_array($response['data'] ?? null) ? $response['data'] : array();
        $affiliate_raw = trim(sanitize_text_field((string) ($data['user_name'] ?? '')));
        $affiliate_id = $this->digistore24_normalize_affiliate_id($affiliate_raw);
        if ($affiliate_raw === '') {
            $settings['enabled'] = false;
            $settings['tested_key_fingerprint'] = '';
            $settings['affiliate_id'] = '';
            $settings['last_status'] = 'failed';
            $settings['last_checked'] = time();
            $settings['last_message'] = 'Digistore24 antwortete, aber die Affiliate-ID (user_name) fehlt.';
            $this->digistore24_update_settings($settings);
            return new WP_Error('digistore24_user_name_missing', 'Digistore24-API-Test ohne verwertbare Affiliate-ID.');
        }
        if ($affiliate_id === '') {
            $settings['enabled'] = false;
            $settings['tested_key_fingerprint'] = '';
            $settings['affiliate_id'] = '';
            $settings['last_status'] = 'failed';
            $settings['last_checked'] = time();
            $settings['last_message'] = 'Digistore24 antwortete mit einer Affiliate-ID, die nicht unverändert als sicherer Tracking-Pfad verwendet werden kann.';
            $this->digistore24_update_settings($settings);
            return new WP_Error('digistore24_user_name_invalid', 'Digistore24-API-Test lieferte keine kanonische, provisionssicher verwendbare Affiliate-ID.');
        }
        $settings['tested_key_fingerprint'] = $this->digistore24_key_fingerprint($key);
        $settings['affiliate_id'] = $affiliate_id;
        $settings['last_status'] = 'connected';
        $settings['last_checked'] = time();
        $settings['enabled'] = !empty($settings['enable_requested']);
        $settings['last_message'] = $settings['enabled']
            ? 'Digistore24 read-only API erfolgreich geprüft; Verbindung ist aktiviert.'
            : 'Digistore24 read-only API erfolgreich geprüft; Verbindung bleibt bewusst deaktiviert.';
        $this->digistore24_update_settings($settings);
        return array('status'=>'connected','message'=>$settings['last_message'],'affiliate_id'=>$affiliate_id);
    }

    private function digistore24_api_allowed_methods() {
        return array('listMarketplaceEntries','getMarketplaceEntry','getUserInfo');
    }

    private function digistore24_api_call($method, $params = array()) {
        $method = trim((string) $method);
        if (!in_array($method, $this->digistore24_api_allowed_methods(), true)) {
            return new WP_Error('digistore24_api_method_blocked', 'Nicht freigegebener Digistore24-API-Pfad blockiert.');
        }
        $settings = $this->digistore24_settings();
        $key = $this->digistore24_api_key($settings);
        if ($key === '') {
            return new WP_Error('digistore24_api_key_missing', 'Digistore24-API-Schlüssel fehlt.');
        }
        $params = is_array($params) ? $params : array();
        $safe_params = array();
        if ($method === 'getMarketplaceEntry') {
            $entry_id = preg_replace('/[^0-9]/', '', (string) ($params['entryId'] ?? $params['entry_id'] ?? ''));
            if ($entry_id === '') {
                return new WP_Error('digistore24_entry_id_missing', 'Marketplace-Entry-ID fehlt.');
            }
            $safe_params['entryId'] = $entry_id;
        } elseif ($method === 'listMarketplaceEntries' && (isset($params['sortBy']) || isset($params['sort_by']))) {
            // Digistore24/OpenAPI uses the canonical query key `sort_by`.
            // Accept the old internal camelCase alias but never send it upstream.
            $sort = sanitize_key((string) ($params['sort_by'] ?? $params['sortBy'] ?? ''));
            if ($sort !== '') {
                $safe_params['sort_by'] = $sort;
            }
        }
        $url = 'https://www.digistore24.com/api/call/' . rawurlencode($method);
        if ($safe_params) {
            $url = add_query_arg($safe_params, $url);
        }
        $response = wp_safe_remote_get($url, array(
            'timeout' => 20,
            'redirection' => 0,
            'limit_response_size' => 4 * 1024 * 1024,
            'headers' => array(
                'Accept' => 'application/json',
                'X-DS-API-KEY' => $key,
            ),
        ));
        if (is_wp_error($response)) {
            return new WP_Error('digistore24_api_http', 'Digistore24-API nicht erreichbar: ' . $response->get_error_message());
        }
        $code = absint(wp_remote_retrieve_response_code($response));
        if ($code < 200 || $code >= 300) {
            return new WP_Error('digistore24_api_http_status', 'Digistore24-API antwortete mit HTTP ' . $code . '.');
        }
        $body = (string) wp_remote_retrieve_body($response);
        $decoded = json_decode($body, true);
        if (!is_array($decoded)) {
            return new WP_Error('digistore24_api_json', 'Digistore24-API lieferte keine gültige JSON-Antwort.');
        }
        $result = strtolower(trim((string) ($decoded['result'] ?? '')));
        if ($result !== 'success') {
            $message = sanitize_text_field((string) ($decoded['message'] ?? $decoded['error'] ?? 'API-Ergebnis ist nicht success.'));
            return new WP_Error('digistore24_api_result', 'Digistore24-API-Fehler: ' . $message);
        }
        $data = $decoded['data'] ?? array();
        if (!is_array($data)) {
            $data = array();
        }
        return array(
            'result'=>'success',
            'data'=>$data,
            'http_code'=>$code,
            // PII-free request identity. Callers use this only to reject stale
            // responses when credentials are rotated concurrently.
            'key_fingerprint'=>$this->digistore24_key_fingerprint($key),
        );
    }

    private function digistore24_normalize_marketplace_entry($entry) {
        $entry = is_array($entry) ? $entry : array();
        $id = trim((string) ($entry['id'] ?? ''));
        if ($id === '') {
            return new WP_Error('digistore24_entry_invalid', 'Marketplace-Eintrag ohne ID blockiert.');
        }
        if (!ctype_digit($id)) {
            return new WP_Error('digistore24_entry_id_invalid', 'Marketplace-Entry-ID ist nicht kanonisch numerisch und wird nicht stillschweigend verändert.');
        }
        $approval = strtolower(trim((string) ($entry['approval_status'] ?? '')));
        if ($approval !== '' && $approval !== 'approved') {
            return new WP_Error('digistore24_entry_not_approved', 'Marketplace-Eintrag ' . $id . ' ist nicht freigegeben (' . sanitize_key($approval) . ').');
        }
        $main_product_id = trim((string) ($entry['main_product_id'] ?? ''));
        if ($main_product_id !== '' && !ctype_digit($main_product_id)) {
            return new WP_Error('digistore24_main_product_id_invalid', 'Digistore24-Hauptprodukt-ID ist nicht kanonisch numerisch und wird nicht für Tracking/Fallback verwendet.');
        }
        return array(
            'id' => $id,
            'main_product_id' => $main_product_id,
            'approval_status' => $approval,
            'approval_status_msg' => sanitize_text_field((string) ($entry['approval_status_msg'] ?? '')),
            'headline' => sanitize_text_field((string) ($entry['headline'] ?? '')),
            'description' => sanitize_textarea_field(wp_strip_all_tags((string) ($entry['description'] ?? ''))),
            'product_category' => sanitize_text_field((string) ($entry['product_category'] ?? '')),
            'product_category_id' => absint($entry['product_category_id'] ?? 0),
            'affiliate_share' => isset($entry['affiliate_share']) && is_numeric($entry['affiliate_share']) ? (float) $entry['affiliate_share'] : null,
            'stats_stars' => isset($entry['stats_stars']) && is_numeric($entry['stats_stars']) ? (float) $entry['stats_stars'] : null,
            'stats_count_orders' => absint($entry['stats_count_orders'] ?? 0),
        );
    }

    private function digistore24_current_tested_identity($settings = null) {
        $settings = is_array($settings) ? $settings : $this->digistore24_settings();
        if (!$this->digistore24_fingerprint_matches($settings)) {
            return array('key_fingerprint'=>'','affiliate_id'=>'');
        }
        $key = $this->digistore24_api_key($settings);
        $affiliate_id = $this->digistore24_normalize_affiliate_id($settings['affiliate_id'] ?? '');
        if ($key === '' || $affiliate_id === '') {
            return array('key_fingerprint'=>'','affiliate_id'=>'');
        }
        return array(
            'key_fingerprint' => $this->digistore24_key_fingerprint($key),
            'affiliate_id' => $affiliate_id,
        );
    }

    private function digistore24_marketplace_store() {
        $stored = get_option('ppar_digistore24_marketplace_v1', array());
        $stored = is_array($stored) ? $stored : array();
        $stored = array_merge(array(
            'items'=>array(),
            'last_checked'=>0,
            'last_status'=>'never',
            'last_message'=>'',
            'blocked'=>0,
            'key_fingerprint'=>'',
            'affiliate_id'=>'',
        ), $stored);

        // Credential-identity boundary: marketplace cache is account-derived.
        // Never expose an old account's cached entries under a different or
        // currently unverified API key. The stored cache remains recoverable if
        // the exact previously tested credential identity is restored.
        $identity = $this->digistore24_current_tested_identity();
        $stored_fp = strtolower(trim((string) ($stored['key_fingerprint'] ?? '')));
        $stored_affiliate = sanitize_text_field((string) ($stored['affiliate_id'] ?? ''));
        $identity_ok = $stored_fp !== ''
            && strlen($stored_fp) === 64
            && (string) ($identity['key_fingerprint'] ?? '') !== ''
            && hash_equals($stored_fp, (string) $identity['key_fingerprint'])
            && $stored_affiliate !== ''
            && hash_equals($stored_affiliate, (string) ($identity['affiliate_id'] ?? ''));
        if (!$identity_ok && !empty($stored['items'])) {
            $stored['items'] = array();
            $stored['last_status'] = 'credentials_changed';
            $stored['last_message'] = 'Gespeicherter Marketplace-Cache gehört nicht zum aktuell erfolgreich geprüften Digistore24-Zugang und bleibt ausgeblendet.';
        }
        return $stored;
    }

    private function digistore24_marketplace_item($entry_id) {
        $entry_id = preg_replace('/[^0-9]/', '', (string) $entry_id);
        $store = $this->digistore24_marketplace_store();
        foreach ((array) ($store['items'] ?? array()) as $item) {
            if (is_array($item) && (string) ($item['id'] ?? '') === $entry_id) {
                return $item;
            }
        }
        return array();
    }

    private function digistore24_refresh_marketplace() {
        if (!$this->digistore24_fingerprint_matches()) {
            return new WP_Error('digistore24_key_not_tested', 'Aktueller Digistore24-Schlüssel wurde noch nicht erfolgreich read-only geprüft.');
        }
        $identity_before = $this->digistore24_current_tested_identity();
        $response = $this->digistore24_api_call('listMarketplaceEntries');
        if (is_wp_error($response)) {
            return $response;
        }
        $identity_after = $this->digistore24_current_tested_identity();
        $response_fp = strtolower(trim((string) ($response['key_fingerprint'] ?? '')));
        if ($response_fp === ''
            || !hash_equals((string) ($identity_before['key_fingerprint'] ?? ''), $response_fp)
            || !hash_equals((string) ($identity_after['key_fingerprint'] ?? ''), $response_fp)) {
            return new WP_Error('digistore24_identity_changed_during_request', 'Digistore24-Zugang wurde während des Marketplace-Abrufs geändert; Antwort wird verworfen.');
        }
        $data = is_array($response['data'] ?? null) ? $response['data'] : array();
        // Live fail-closed schema gate. `listMarketplaceEntries` is documented to
        // return data.entries. V6.63.0 silently converted a missing/malformed or
        // empty entries payload into a misleading successful 0/0 marketplace
        // refresh. That makes a transport/API success indistinguishable from a
        // usable marketplace result and can hide a schema/permission problem.
        if (!array_key_exists('entries', $data)) {
            $keys = array_slice(array_values(array_filter(array_map('sanitize_key', array_keys($data)))), 0, 12);
            $suffix = $keys ? ' Vorhandene data-Schlüssel: ' . implode(', ', $keys) . '.' : ' data ist leer.';
            return new WP_Error('digistore24_marketplace_schema_missing_entries', 'Digistore24-Marktplatzantwort enthält kein data.entries-Feld.' . $suffix);
        }
        if (!is_array($data['entries'])) {
            return new WP_Error('digistore24_marketplace_schema_invalid_entries', 'Digistore24-Marktplatzantwort enthält data.entries nicht als Liste. Antwort wird nicht als erfolgreicher Abruf gewertet.');
        }
        $entries = $data['entries'];
        if (!$entries) {
            return new WP_Error('digistore24_marketplace_empty_unverified', 'Digistore24 lieferte data.entries als leere Liste. 0/0 wird fail-closed nicht als Marketplace-PASS gewertet; bestehender Cache und öffentliche Ausgabe bleiben unverändert.');
        }
        $items = array();
        $blocked = 0;
        foreach ($entries as $entry) {
            $normalized = $this->digistore24_normalize_marketplace_entry($entry);
            if (is_wp_error($normalized)) {
                $blocked++;
                continue;
            }
            $items[] = $normalized;
        }
        usort($items, static function ($a, $b) {
            return strnatcasecmp((string) ($a['headline'] ?? ''), (string) ($b['headline'] ?? ''));
        });
        $identity = $this->digistore24_current_tested_identity();
        if ((string) ($identity['key_fingerprint'] ?? '') === '' || (string) ($identity['affiliate_id'] ?? '') === '') {
            return new WP_Error('digistore24_identity_not_tested', 'Aktueller Digistore24-Zugang besitzt keine erfolgreich geprüfte Identität.');
        }
        $store = array(
            'items' => $items,
            'last_checked' => time(),
            'last_status' => 'success',
            'last_message' => count($items) . ' freigegebene/kompatible Marketplace-Einträge gespeichert; ' . $blocked . ' explizit nicht freigegebene Einträge blockiert.',
            'blocked' => $blocked,
            'key_fingerprint' => (string) $identity['key_fingerprint'],
            'affiliate_id' => (string) $identity['affiliate_id'],
        );
        update_option('ppar_digistore24_marketplace_v1', $store, false);
        return array('status'=>'success','count'=>count($items),'blocked'=>$blocked,'items'=>$items);
    }

    private function digistore24_refresh_marketplace_entry($entry_id) {
        $requested_entry_id = preg_replace('/[^0-9]/', '', (string) $entry_id);
        if ($requested_entry_id === '') {
            return new WP_Error('digistore24_entry_id_missing', 'Marketplace-Entry-ID fehlt.');
        }
        if (!$this->digistore24_fingerprint_matches()) {
            return new WP_Error('digistore24_key_not_tested', 'Aktueller Digistore24-Schlüssel wurde noch nicht erfolgreich read-only geprüft.');
        }
        $identity_before = $this->digistore24_current_tested_identity();
        $response = $this->digistore24_api_call('getMarketplaceEntry', array('entryId'=>$requested_entry_id));
        if (is_wp_error($response)) {
            return $response;
        }
        $identity_after = $this->digistore24_current_tested_identity();
        $response_fp = strtolower(trim((string) ($response['key_fingerprint'] ?? '')));
        if ($response_fp === ''
            || !hash_equals((string) ($identity_before['key_fingerprint'] ?? ''), $response_fp)
            || !hash_equals((string) ($identity_after['key_fingerprint'] ?? ''), $response_fp)) {
            return new WP_Error('digistore24_identity_changed_during_request', 'Digistore24-Zugang wurde während des Marketplace-Detailabrufs geändert; Antwort wird verworfen.');
        }
        $data = is_array($response['data'] ?? null) ? $response['data'] : array();
        // Some API clients/spec variants expose the entry in data.entry; prefer it
        // when present, otherwise the detail data itself is the entry.
        $entry = isset($data['entry']) && is_array($data['entry']) ? array_merge($data, $data['entry']) : $data;
        $normalized = $this->digistore24_normalize_marketplace_entry($entry);
        if (is_wp_error($normalized)) {
            return $normalized;
        }
        if ((string) ($normalized['id'] ?? '') !== $requested_entry_id) {
            return new WP_Error('digistore24_entry_id_mismatch', 'Digistore24-Detailantwort gehört nicht zur angeforderten Marketplace-Entry-ID und wird verworfen.');
        }
        $store = $this->digistore24_marketplace_store();
        $items = array();
        $replaced = false;
        foreach ((array) ($store['items'] ?? array()) as $item) {
            if (is_array($item) && (string) ($item['id'] ?? '') === (string) $normalized['id']) {
                $items[] = $normalized;
                $replaced = true;
            } elseif (is_array($item)) {
                $items[] = $item;
            }
        }
        if (!$replaced) {
            $items[] = $normalized;
        }
        $identity = $this->digistore24_current_tested_identity();
        if ((string) ($identity['key_fingerprint'] ?? '') === '' || (string) ($identity['affiliate_id'] ?? '') === '') {
            return new WP_Error('digistore24_identity_not_tested', 'Aktueller Digistore24-Zugang besitzt keine erfolgreich geprüfte Identität.');
        }
        $store['items'] = $items;
        $store['last_checked'] = time();
        $store['key_fingerprint'] = (string) $identity['key_fingerprint'];
        $store['affiliate_id'] = (string) $identity['affiliate_id'];
        update_option('ppar_digistore24_marketplace_v1', $store, false);
        return $normalized;
    }

    public function digistore24_automation_scheduled_sources($sources, $registry = array(), $contract_version = '') {
        $sources = is_array($sources) ? $sources : array();
        if (!$this->digistore24_automation_ready()) {
            return $sources;
        }
        $sources[] = array(
            'key' => 'digistore24:marketplace',
            'provider' => 'digistore24',
            'partner_external_id' => 'marketplace',
        );
        return $sources;
    }

    public function digistore24_automation_dispatch($handled, $provider, $source, $manual = false, $contract_version = '') {
        if (sanitize_key((string) $provider) !== 'digistore24') {
            return $handled;
        }
        if (!$this->digistore24_automation_ready()) {
            return array(
                'immediate'=>true,
                'provider'=>'digistore24',
                'summary'=>array('status'=>'partial','message'=>'Digistore24 ist nicht aktiviert oder der aktuelle Schlüssel wurde nicht erfolgreich geprüft.'),
            );
        }
        $result = $this->digistore24_refresh_marketplace();
        if (is_wp_error($result)) {
            // Deliberately not WP_Error: central automation advances its cursor so
            // a single provider cannot starve Awin/ADCELL or other adapters.
            return array(
                'immediate'=>true,
                'provider'=>'digistore24',
                'summary'=>array('status'=>'partial','message'=>$result->get_error_message()),
            );
        }
        return array('immediate'=>true,'provider'=>'digistore24','summary'=>$result);
    }

    private function digistore24_partnerships() {
        $stored = get_option('ppar_digistore24_partnerships_v1', array());
        return is_array($stored) ? $stored : array();
    }

    private function digistore24_partnership_confirmed($entry_id) {
        $entry_id = preg_replace('/[^0-9]/', '', (string) $entry_id);
        $items = $this->digistore24_partnerships();
        $record = $entry_id !== '' && isset($items[$entry_id]) && is_array($items[$entry_id]) ? $items[$entry_id] : array();
        if (empty($record['confirmed'])) {
            return false;
        }
        $identity = $this->digistore24_current_tested_identity();
        $saved_fp = strtolower(trim((string) ($record['key_fingerprint'] ?? '')));
        $saved_affiliate = sanitize_text_field((string) ($record['affiliate_id'] ?? ''));
        $identity_ok = $saved_fp !== ''
            && strlen($saved_fp) === 64
            && (string) ($identity['key_fingerprint'] ?? '') !== ''
            && hash_equals($saved_fp, (string) $identity['key_fingerprint'])
            && $saved_affiliate !== ''
            && hash_equals($saved_affiliate, (string) ($identity['affiliate_id'] ?? ''));
        if (!$identity_ok) {
            return false;
        }
        // Partnership is meaningful only for an entry still present in the
        // current identity-bound marketplace cache. A removed/revoked/unknown
        // entry must not retain import authority from an old confirmation.
        return !empty($this->digistore24_marketplace_item($entry_id));
    }

    private function digistore24_set_partnership($entry_id, $confirmed) {
        $entry_id = preg_replace('/[^0-9]/', '', (string) $entry_id);
        if ($entry_id === '') {
            return new WP_Error('digistore24_entry_id_missing', 'Marketplace-Entry-ID fehlt.');
        }
        $items = $this->digistore24_partnerships();
        if ($confirmed) {
            $identity = $this->digistore24_current_tested_identity();
            if ((string) ($identity['key_fingerprint'] ?? '') === '' || (string) ($identity['affiliate_id'] ?? '') === '') {
                return new WP_Error('digistore24_partnership_identity_required', 'Partnerschaftsbestätigung erfordert den aktuell erfolgreich geprüften Digistore24-Zugang.');
            }
            if (empty($this->digistore24_marketplace_item($entry_id))) {
                return new WP_Error('digistore24_marketplace_entry_required', 'Partnerschaft kann nur für einen aktuell im geprüften Digistore24-Marktplatz vorhandenen Eintrag bestätigt werden.');
            }
            $items[$entry_id] = array(
                'confirmed'=>1,
                'confirmed_at'=>time(),
                'key_fingerprint'=>(string) $identity['key_fingerprint'],
                'affiliate_id'=>(string) $identity['affiliate_id'],
            );
        } else {
            unset($items[$entry_id]);
        }
        update_option('ppar_digistore24_partnerships_v1', $items, false);
        return true;
    }

    private function digistore24_is_https_url($url) {
        $url = esc_url_raw((string) $url);
        return $url !== '' && wp_http_validate_url($url) && strtolower((string) wp_parse_url($url, PHP_URL_SCHEME)) === 'https';
    }

    private function digistore24_tracking_url_allowed($url) {
        $url = esc_url_raw(html_entity_decode((string) $url, ENT_QUOTES, 'UTF-8'));
        if (!$this->digistore24_is_https_url($url)) {
            return false;
        }
        $host = strtolower((string) wp_parse_url($url, PHP_URL_HOST));
        if (!in_array($host, array('checkout-ds24.com','www.checkout-ds24.com'), true)) {
            return false;
        }
        $port = wp_parse_url($url, PHP_URL_PORT);
        if ($port !== null && absint($port) !== 443) {
            return false;
        }
        // Promo/content attribution is path-bound. A simultaneous `aff` query
        // parameter creates an ambiguous second affiliate identity and is
        // therefore rejected. Documented cid/sid/ds24tr query tracking remains
        // untouched.
        $query = (string) wp_parse_url($url, PHP_URL_QUERY);
        if ($query !== '') {
            $query_args = array();
            parse_str(html_entity_decode($query, ENT_QUOTES, 'UTF-8'), $query_args);
            foreach (array_keys($query_args) as $query_key) {
                if (strtolower((string) $query_key) === 'aff') {
                    return false;
                }
            }
        }
        $path = trim((string) wp_parse_url($url, PHP_URL_PATH), '/');
        $segments = array_values(array_filter(array_map('rawurldecode', explode('/', $path)), 'strlen'));
        $first = strtolower((string) ($segments[0] ?? ''));
        if (!in_array($first, array('redir','content','link'), true)) {
            return false;
        }
        // Commission-integrity gate: an explicit vendor link is only accepted
        // when it actually carries the Affiliate-ID proven by the current tested
        // API key. Placeholders are handled separately via [PARTNER_LINK].
        $settings = $this->digistore24_settings();
        $affiliate_id = $this->digistore24_normalize_affiliate_id($settings['affiliate_id'] ?? '');
        if ($affiliate_id === '' || !$this->digistore24_fingerprint_matches($settings)) {
            return false;
        }
        // Official Digistore24 path positions are deterministic for promo
        // and content links. Never accept our Affiliate-ID merely because it
        // appears later in a URL whose actual attribution slot belongs to a
        // different affiliate.
        if ($first === 'redir') {
            $product_id = (string) ($segments[1] ?? '');
            $path_affiliate = (string) ($segments[2] ?? '');
            // Official promo shape: /redir/PRODUCT-ID/AFFILIATE[/CAMPAIGNKEY].
            // Query parameters such as cid/sid stay allowed, but unknown extra
            // path levels are rejected rather than interpreted optimistically.
            return count($segments) >= 3 && count($segments) <= 4
                && $product_id !== '' && ctype_digit($product_id)
                && $path_affiliate !== '' && hash_equals($affiliate_id, $path_affiliate);
        }
        if ($first === 'content') {
            $product_id = (string) ($segments[1] ?? '');
            $content_id = (string) ($segments[2] ?? '');
            $path_affiliate = (string) ($segments[3] ?? '');
            // Official content shape:
            // /content/PRODUCT-ID/CONTENTLINK-ID/AFFILIATE[/CAMPAIGNKEY].
            return count($segments) >= 4 && count($segments) <= 5
                && $product_id !== '' && ctype_digit($product_id)
                && $content_id !== '' && ctype_digit($content_id)
                && $path_affiliate !== '' && hash_equals($affiliate_id, $path_affiliate);
        }
        // `/link/` remains on the existing conservative allow-list pending the
        // real vendor payload gate; unlike redir/content its exact documented
        // positional schema is not assumed here.
        foreach (array_slice($segments, 1) as $segment) {
            if (hash_equals($affiliate_id, (string) $segment)) {
                return true;
            }
        }
        return false;
    }

    private function digistore24_partner_link_fallback($entry) {
        $entry = is_array($entry) ? $entry : array();
        $product_id = preg_replace('/[^0-9]/', '', (string) ($entry['main_product_id'] ?? ''));
        $settings = $this->digistore24_settings();
        $affiliate_id = $this->digistore24_normalize_affiliate_id($settings['affiliate_id'] ?? '');
        if ($product_id === '' || $affiliate_id === '' || !$this->digistore24_fingerprint_matches($settings)) {
            return '';
        }
        return 'https://www.checkout-ds24.com/redir/' . rawurlencode($product_id) . '/' . rawurlencode($affiliate_id);
    }

    private function digistore24_resolve_url($base_url, $candidate) {
        $candidate = trim(html_entity_decode((string) $candidate, ENT_QUOTES, 'UTF-8'));
        if ($candidate === '') {
            return '';
        }
        if (preg_match('#^https?://#i', $candidate)) {
            return esc_url_raw($candidate);
        }
        if (strpos($candidate, '//') === 0) {
            return esc_url_raw('https:' . $candidate);
        }
        $base = wp_parse_url($base_url);
        if (!is_array($base) || empty($base['host'])) {
            return '';
        }
        $scheme = strtolower((string) ($base['scheme'] ?? 'https'));
        $origin = $scheme . '://' . (string) $base['host'];
        if (!empty($base['port'])) {
            $origin .= ':' . absint($base['port']);
        }
        if (strpos($candidate, '/') === 0) {
            return esc_url_raw($origin . $candidate);
        }
        $path = (string) ($base['path'] ?? '/');
        $dir = preg_replace('#/[^/]*$#', '/', $path);
        return esc_url_raw($origin . $dir . $candidate);
    }

    private function digistore24_parse_vendor_banners($html, $support_url, $entry) {
        $html = (string) $html;
        $entry = is_array($entry) ? $entry : array();
        $fallback = $this->digistore24_partner_link_fallback($entry);
        $banners = array();
        if ($html === '') {
            return $banners;
        }
        $pattern = '#<a\b[^>]*href\s*=\s*(["\'])(.*?)\1[^>]*>\s*(?:<[^>]+>\s*)*<img\b([^>]*)>.*?</a>#is';
        if (!preg_match_all($pattern, $html, $matches, PREG_SET_ORDER)) {
            return $banners;
        }
        foreach ($matches as $match) {
            $href = trim((string) ($match[2] ?? ''));
            $img_attrs = (string) ($match[3] ?? '');
            if (stripos($href, '[PARTNER_LINK]') !== false) {
                if ($fallback === '') {
                    continue;
                }
                $href = str_ireplace('[PARTNER_LINK]', $fallback, $href);
            }
            $href = $this->digistore24_resolve_url($support_url, $href);
            if (!$this->digistore24_tracking_url_allowed($href)) {
                continue;
            }
            $src = '';
            $alt = '';
            if (preg_match('#\bsrc\s*=\s*(["\'])(.*?)\1#is', $img_attrs, $m)) {
                $src = $this->digistore24_resolve_url($support_url, $m[2]);
            }
            if (preg_match('#\balt\s*=\s*(["\'])(.*?)\1#is', $img_attrs, $m)) {
                $alt = sanitize_text_field(wp_strip_all_tags(html_entity_decode((string) $m[2], ENT_QUOTES, 'UTF-8')));
            }
            if (!$this->digistore24_is_https_url($src)) {
                continue;
            }
            $banners[] = array('tracking_url'=>$href,'image_url'=>$src,'alt_text'=>$alt);
        }
        return $banners;
    }

    private function digistore24_import_vendor_banners($entry_id, $support_url) {
        $entry_id = preg_replace('/[^0-9]/', '', (string) $entry_id);
        if (!$this->digistore24_partnership_confirmed($entry_id)) {
            return new WP_Error('digistore24_partnership_required', 'Vendor-Bannerimport bleibt bis zur manuellen Partnerschaftsbestätigung gesperrt.');
        }
        if (!$this->digistore24_is_https_url($support_url)) {
            return new WP_Error('digistore24_support_url_invalid', 'Vendor-Supportseite muss eine gültige HTTPS-URL sein.');
        }
        $entry = $this->digistore24_refresh_marketplace_entry($entry_id);
        if (is_wp_error($entry)) {
            return $entry;
        }
        $response = wp_safe_remote_get(esc_url_raw($support_url), array(
            'timeout'=>20,
            // No implicit redirects: every fetched support page must itself be
            // the explicitly validated HTTPS URL. A real vendor redirect can be
            // supplied as its final HTTPS destination during the live gate.
            'redirection'=>0,
            'limit_response_size'=>2 * 1024 * 1024,
            'headers'=>array('Accept'=>'text/html,application/xhtml+xml'),
        ));
        if (is_wp_error($response)) {
            return new WP_Error('digistore24_support_fetch_failed', 'Vendor-Supportseite konnte nicht sicher geladen werden: ' . $response->get_error_message());
        }
        $code = absint(wp_remote_retrieve_response_code($response));
        if ($code < 200 || $code >= 300) {
            return new WP_Error('digistore24_support_http_status', 'Vendor-Supportseite antwortete mit HTTP ' . $code . '.');
        }
        $banners = $this->digistore24_parse_vendor_banners((string) wp_remote_retrieve_body($response), $support_url, $entry);
        if (!$banners) {
            return new WP_Error('digistore24_no_valid_banners', 'Keine zulässigen Digistore24-Vendor-Banner mit gültigem Trackinglink gefunden.');
        }
        $imported = 0;
        $blocked = 0;
        foreach ($banners as $index => $banner) {
            $row = array(
                'external_id' => 'ds24-' . $entry_id . '-' . substr(hash('sha256', (string) $banner['image_url'] . '|' . (string) $banner['tracking_url']), 0, 24),
                'creative_type' => 'banner',
                'title' => (string) ($banner['alt_text'] ?? '') !== '' ? (string) $banner['alt_text'] : (string) ($entry['headline'] ?? 'Digistore24 Banner'),
                'description' => (string) ($entry['description'] ?? ''),
                'tags' => (string) ($entry['product_category'] ?? ''),
                'image_url' => (string) $banner['image_url'],
                'destination_url' => (string) $banner['tracking_url'],
                'tracking_url' => (string) $banner['tracking_url'],
                'status' => 'active',
                'alt_text' => (string) ($banner['alt_text'] ?? ''),
            );
            $mapping = $this->creative_library_detect_mapping(array_keys($row));
            $normalized = $this->creative_library_normalize_row($row, $mapping, array(
                'provider'=>'digistore24',
                'partner_external_id'=>'entry-' . $entry_id,
                'partner_name'=>'Digistore24 · ' . ((string) ($entry['headline'] ?? '') !== '' ? (string) $entry['headline'] : 'Marketplace ' . $entry_id),
                'source_kind'=>'digistore24_vendor_banner',
                'run_uuid'=>'',
            ));
            if (is_wp_error($normalized)) {
                $blocked++;
                continue;
            }
            if (sanitize_key((string) ($normalized['creative_type'] ?? '')) !== 'banner') {
                $blocked++;
                continue;
            }
            $status = $this->creative_library_upsert($normalized);
            if ($status === 'blocked') {
                $blocked++;
                continue;
            }
            $imported++;
        }
        if ($imported > 0) {
            $this->creative_library_schedule_asset_verification(10);
        }
        return array('status'=>'success','imported'=>$imported,'blocked'=>$blocked,'found'=>count($banners));
    }

    public function digistore24_render_access_card($provider = '', $definition = array(), $contract_version = '') {
        $settings = $this->digistore24_settings();
        $has_constant = defined('PPAR_DIGISTORE24_API_KEY') && trim((string) PPAR_DIGISTORE24_API_KEY) !== '';
        ?>
        <form method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>">
            <input type="hidden" name="action" value="ppar_provider_access_save">
            <input type="hidden" name="provider" value="digistore24">
            <?php wp_nonce_field('ppar_provider_access_digistore24','ppar_provider_nonce'); ?>
            <p><label><input type="checkbox" name="ppar_provider[digistore24][enabled]" value="1" <?php checked(!empty($settings['enabled']) && $this->digistore24_fingerprint_matches($settings)); ?>> Verbindung verwenden</label></p>
            <p><label>Read-only API-Schlüssel <span class="ppar-saved"><?php echo esc_html($has_constant ? 'über wp-config.php' : (trim((string)($settings['api_key'] ?? '')) !== '' ? 'gespeichert' : 'nicht gespeichert')); ?></span><br><input type="password" autocomplete="new-password" name="ppar_provider[digistore24][api_key]" value="" placeholder="<?php echo esc_attr($has_constant ? 'über wp-config.php gesetzt' : 'leer lassen zum Beibehalten'); ?>"></label></p>
            <?php if (!$has_constant) : ?><details><summary>Zugangsdaten entfernen</summary><p><label><input type="checkbox" name="ppar_provider[digistore24][remove_api_key]" value="1"> API-Schlüssel entfernen</label></p></details><?php endif; ?>
            <p class="description">Nur read-only GET: listMarketplaceEntries, getMarketplaceEntry und getUserInfo. Aktivierung erfolgt erst nach erfolgreichem Test desselben Schlüssels.</p>
            <div class="ppar-v240-actions"><button class="button button-primary" name="ppar_provider_action" value="save">Speichern</button><button class="button" name="ppar_provider_action" value="save_test">Speichern &amp; API prüfen</button></div>
        </form>
        <?php
    }

    public function digistore24_render_specialist($provider = '', $definition = array(), $contract_version = '') {
        $settings = $this->digistore24_settings();
        $store = $this->digistore24_marketplace_store();
        $partnerships = $this->digistore24_partnerships();
        $items = (array) ($store['items'] ?? array());
        ?>
        <section class="postbox" style="padding:18px;margin-top:18px">
            <h2>Marketplace · read-only</h2>
            <p>Digistore24 ist hier ausschließlich Banner-Provider. Marktplatzabruf und Vorsortierung aktivieren nichts öffentlich.</p>
            <form method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>"><input type="hidden" name="action" value="ppar_digistore24_marketplace_refresh"><?php wp_nonce_field('ppar_digistore24_marketplace_refresh','ppar_digistore24_nonce'); ?><button class="button" type="submit" <?php disabled(!$this->digistore24_fingerprint_matches($settings)); ?>>Marketplace read-only abrufen</button></form>
            <p><strong>Letzter Abruf:</strong> <?php echo !empty($store['last_checked']) ? esc_html(wp_date('d.m.Y H:i',(int)$store['last_checked'])) : 'nie'; ?> · <?php echo esc_html((string)($store['last_message'] ?? '')); ?></p>
        </section>
        <?php foreach ($items as $entry) : if (!is_array($entry)) { continue; } $entry_id=(string)($entry['id']??''); $confirmed=$this->digistore24_partnership_confirmed($entry_id); ?>
        <section class="postbox" style="padding:18px;margin-top:14px">
            <h3><?php echo esc_html((string)($entry['headline'] ?? ('Marketplace ' . $entry_id))); ?></h3>
            <p><?php echo esc_html((string)($entry['product_category'] ?? '')); ?><?php if ((string)($entry['description'] ?? '') !== '') : ?><br><?php echo esc_html((string)$entry['description']); ?><?php endif; ?></p>
            <form method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>" style="margin-bottom:12px"><input type="hidden" name="action" value="ppar_digistore24_partnership"><input type="hidden" name="entry_id" value="<?php echo esc_attr($entry_id); ?>"><?php wp_nonce_field('ppar_digistore24_partnership_' . $entry_id,'ppar_digistore24_nonce'); ?><label><input type="checkbox" name="confirmed" value="1" <?php checked($confirmed); ?>> Partnerschaft/Freigabe manuell bestätigt</label> <button class="button button-small" type="submit">Bestätigung speichern</button></form>
            <form method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>"><input type="hidden" name="action" value="ppar_digistore24_import_banners"><input type="hidden" name="entry_id" value="<?php echo esc_attr($entry_id); ?>"><?php wp_nonce_field('ppar_digistore24_import_banners_' . $entry_id,'ppar_digistore24_nonce'); ?><label>Vendor-Support-/Werbemittelseite (HTTPS)<br><input class="large-text" type="url" name="support_url" value="" placeholder="https://..."></label><p><button class="button" type="submit" <?php disabled(!$confirmed); ?>>Vendor-Banner prüfen &amp; importieren</button></p><p class="description">Importiert nur Banner mit zulässigem Digistore24-Trackinglink. Keine automatische öffentliche Aktivierung.</p></form>
        </section>
        <?php endforeach;
    }

    private function digistore24_redirect_specialist($message = '', $error = false) {
        $args = array('page'=>'affiliate-portal-provider-digistore24');
        if ($message !== '') {
            $args[$error ? 'ppar_provider_error' : 'ppar_provider_saved'] = $error ? rawurlencode(sanitize_text_field($message)) : 'digistore24';
        }
        wp_safe_redirect(add_query_arg($args, admin_url('admin.php')));
        exit;
    }

    public function digistore24_handle_marketplace_refresh() {
        if (!current_user_can('manage_options')) { wp_die('Keine Berechtigung.'); }
        check_admin_referer('ppar_digistore24_marketplace_refresh','ppar_digistore24_nonce');
        $result = $this->digistore24_refresh_marketplace();
        $this->digistore24_redirect_specialist(is_wp_error($result) ? $result->get_error_message() : 'Marketplace read-only aktualisiert.', is_wp_error($result));
    }

    public function digistore24_handle_partnership() {
        if (!current_user_can('manage_options')) { wp_die('Keine Berechtigung.'); }
        $entry_id = preg_replace('/[^0-9]/', '', (string) ($_POST['entry_id'] ?? ''));
        check_admin_referer('ppar_digistore24_partnership_' . $entry_id,'ppar_digistore24_nonce');
        $result = $this->digistore24_set_partnership($entry_id, !empty($_POST['confirmed']));
        $this->digistore24_redirect_specialist(is_wp_error($result) ? $result->get_error_message() : 'Partnerschaftsstatus gespeichert.', is_wp_error($result));
    }

    public function digistore24_handle_import_banners() {
        if (!current_user_can('manage_options')) { wp_die('Keine Berechtigung.'); }
        $entry_id = preg_replace('/[^0-9]/', '', (string) ($_POST['entry_id'] ?? ''));
        check_admin_referer('ppar_digistore24_import_banners_' . $entry_id,'ppar_digistore24_nonce');
        $support_url = esc_url_raw((string) ($_POST['support_url'] ?? ''));
        $result = $this->digistore24_import_vendor_banners($entry_id, $support_url);
        $message = is_wp_error($result) ? $result->get_error_message() : absint($result['imported'] ?? 0) . ' Vendor-Banner importiert; ' . absint($result['blocked'] ?? 0) . ' blockiert.';
        $this->digistore24_redirect_specialist($message, is_wp_error($result));
    }
}
