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
 * - API affiliation proof for automation; manual confirmation only for manual import;
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
        add_action('shutdown', array($this, 'digistore24_final_publication_guard'), 999);
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
        return array('listMarketplaceEntries','getMarketplaceEntry','getUserInfo','getAffiliateCommission');
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
        if ($method === 'getAffiliateCommission') {
            $identity = $this->digistore24_current_tested_identity($settings);
            $affiliate_id = $this->digistore24_normalize_affiliate_id($params['affiliate_id'] ?? '');
            if ($affiliate_id === '' || (string) ($identity['affiliate_id'] ?? '') === '' || !hash_equals((string) $identity['affiliate_id'], $affiliate_id)) {
                return new WP_Error('digistore24_affiliate_identity_mismatch', 'Provisionsabfrage für eine fremde oder ungeprüfte Affiliate-ID wurde vor dem Netzwerkzugriff blockiert.');
            }
            $product_ids = is_array($params['product_ids'] ?? null) ? $params['product_ids'] : explode(',', (string) ($params['product_ids'] ?? ''));
            if (count($product_ids) < 1 || count($product_ids) > 50) {
                return new WP_Error('digistore24_product_ids_count_invalid', 'Provisionsabfrage erfordert 1 bis 50 explizite Produkt-IDs.');
            }
            $canonical = array();
            foreach ($product_ids as $product_id) {
                $product_id = trim((string) $product_id);
                if ($product_id === '' || !ctype_digit($product_id) || (string) absint($product_id) !== $product_id) {
                    return new WP_Error('digistore24_product_id_invalid', 'Provisionsabfrage enthält eine nicht kanonische numerische Produkt-ID.');
                }
                $canonical[$product_id] = $product_id;
            }
            if (!$canonical || count($canonical) !== count($product_ids)) {
                return new WP_Error('digistore24_product_ids_invalid', 'Provisionsabfrage enthält leere oder doppelte Produkt-IDs.');
            }
            $safe_params['affiliate_id'] = $affiliate_id;
            $safe_params['product_ids'] = implode(',', $canonical);
        } elseif ($method === 'getMarketplaceEntry') {
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

    private function digistore24_affiliation_store() {
        $stored = get_option('ppar_digistore24_affiliations_v1', array());
        return is_array($stored) ? $stored : array();
    }

    private function digistore24_store_affiliation_response($product_ids, $response, $identity) {
        $data = is_array($response['data'] ?? null) ? $response['data'] : array();
        if (!array_key_exists('commissions', $data) || !is_array($data['commissions'])) {
            return new WP_Error('digistore24_commissions_schema_invalid', 'Digistore24-Provisionsantwort enthält keine gültige data.commissions-Liste.');
        }
        $requested = array_fill_keys(array_map('strval', $product_ids), true);
        $rows = array();
        foreach ($data['commissions'] as $raw) {
            $raw = is_array($raw) ? $raw : array();
            $product_id = trim((string) ($raw['product_id'] ?? ''));
            if ($product_id === '' || !ctype_digit($product_id) || !isset($requested[$product_id]) || isset($rows[$product_id])) { continue; }
            $rows[$product_id] = array(
                'product_id'=>$product_id,
                'product_is_active'=>filter_var($raw['product_is_active'] ?? false, FILTER_VALIDATE_BOOLEAN),
                'approval_status'=>sanitize_key((string) ($raw['approval_status'] ?? '')),
                'commission_rate'=>isset($raw['commission_rate']) && is_numeric($raw['commission_rate']) ? (float) $raw['commission_rate'] : null,
                'checked_at'=>time(),
                'key_fingerprint'=>(string) ($identity['key_fingerprint'] ?? ''),
                'affiliate_id'=>(string) ($identity['affiliate_id'] ?? ''),
            );
        }
        $store = $this->digistore24_affiliation_store();
        foreach (array_keys($requested) as $product_id) {
            // A missing row is persisted as a negative proof, so an older
            // approval can never survive a successful refresh that omitted it.
            $store[$product_id] = $rows[$product_id] ?? array(
                'product_id'=>$product_id,'product_is_active'=>false,'approval_status'=>'missing','commission_rate'=>null,
                'checked_at'=>time(),'key_fingerprint'=>(string) ($identity['key_fingerprint'] ?? ''),'affiliate_id'=>(string) ($identity['affiliate_id'] ?? ''),
            );
        }
        update_option('ppar_digistore24_affiliations_v1', $store, false);
        return $rows;
    }

    private function digistore24_refresh_affiliations($product_ids) {
        $identity = $this->digistore24_current_tested_identity();
        if ((string) ($identity['affiliate_id'] ?? '') === '' || (string) ($identity['key_fingerprint'] ?? '') === '') {
            return new WP_Error('digistore24_identity_not_tested', 'Provisionsprüfung erfordert den aktuell getesteten Digistore24-Zugang.');
        }
        $response = $this->digistore24_api_call('getAffiliateCommission', array('affiliate_id'=>$identity['affiliate_id'],'product_ids'=>$product_ids));
        if (is_wp_error($response)) { return $response; }
        $after = $this->digistore24_current_tested_identity();
        $response_fp = (string) ($response['key_fingerprint'] ?? '');
        if ($response_fp === '' || !hash_equals((string) $identity['key_fingerprint'], $response_fp)
            || !hash_equals((string) ($after['key_fingerprint'] ?? ''), $response_fp)
            || !hash_equals((string) $identity['affiliate_id'], (string) ($after['affiliate_id'] ?? ''))) {
            return new WP_Error('digistore24_identity_changed_during_request', 'Digistore24-Zugang änderte sich während der Provisionsprüfung; Antwort wird verworfen.');
        }
        return $this->digistore24_store_affiliation_response($product_ids, $response, $identity);
    }

    private function digistore24_affiliation_gate($product_id, $refresh_stale = false) {
        $product_id = trim((string) $product_id);
        if ($product_id === '' || !ctype_digit($product_id)) { return new WP_Error('digistore24_affiliation_product_missing', 'Kanonische Produkt-ID für den Partnerschaftsnachweis fehlt.'); }
        $identity = $this->digistore24_current_tested_identity();
        $store = $this->digistore24_affiliation_store();
        $proof = is_array($store[$product_id] ?? null) ? $store[$product_id] : array();
        $fresh = absint($proof['checked_at'] ?? 0) >= time() - (2 * DAY_IN_SECONDS);
        if ($refresh_stale && (!$proof || !$fresh)) {
            $refreshed = $this->digistore24_refresh_affiliations(array($product_id));
            if (is_wp_error($refreshed)) { return $refreshed; }
            $store = $this->digistore24_affiliation_store(); $proof = is_array($store[$product_id] ?? null) ? $store[$product_id] : array();
            $fresh = absint($proof['checked_at'] ?? 0) >= time() - (2 * DAY_IN_SECONDS);
        }
        if (!$proof) { return new WP_Error('digistore24_affiliation_missing', 'Aktueller Digistore24-Partnerschaftsnachweis fehlt.'); }
        if (!$fresh) { return new WP_Error('digistore24_affiliation_stale', 'Digistore24-Partnerschaftsnachweis ist älter als zwei Tage.'); }
        if ((string) ($identity['key_fingerprint'] ?? '') === '' || !hash_equals((string) $identity['key_fingerprint'], (string) ($proof['key_fingerprint'] ?? ''))
            || (string) ($identity['affiliate_id'] ?? '') === '' || !hash_equals((string) $identity['affiliate_id'], (string) ($proof['affiliate_id'] ?? ''))) {
            return new WP_Error('digistore24_affiliation_identity_mismatch', 'Partnerschaftsnachweis gehört nicht zum aktuell getesteten Zugang.');
        }
        if ((string) ($proof['approval_status'] ?? '') !== 'approved') { return new WP_Error('digistore24_affiliation_not_approved', 'Digistore24-Partnerschaft ist nicht approved.'); }
        if (empty($proof['product_is_active'])) { return new WP_Error('digistore24_affiliation_product_inactive', 'Digistore24-Produkt ist nicht aktiv.'); }
        return $proof;
    }

    /**
     * Final fail-closed proof for the explicitly imported manual CSV path.
     *
     * The imported CSV inventory itself is the authority for this path. It is
     * bound to the exact tested credential fingerprint, affiliate ID, original
     * import SHA and the exact Werbemittel entry. Derived partnership/API caches
     * may be refreshed later and are therefore not a publication dependency.
     *
     * When a Digistore24 URL exposes a canonical product ID (redir/content), the
     * row must match that exact product. For official link URLs without an
     * extractable product ID, the bound Werbemittel entry itself is sufficient:
     * the creative was imported from that entry's verified vendor page and the
     * tracking URL is separately revalidated against the current affiliate ID.
     */
    private function digistore24_manual_csv_bound_identity($inventory = null) {
        $inventory = is_array($inventory) ? $inventory : get_option('ppar_digistore24_manual_inventory_v1', array());
        $inventory = is_array($inventory) ? $inventory : array();
        $sha = preg_replace('/[^a-f0-9]/', '', strtolower((string) ($inventory['sha256'] ?? '')));
        $inventory_fp = strtolower(trim((string) ($inventory['key_fingerprint'] ?? '')));
        $inventory_affiliate = $this->digistore24_normalize_affiliate_id($inventory['affiliate_id'] ?? '');
        $imported_at = absint($inventory['imported_at'] ?? 0);
        if (!preg_match('/^[a-f0-9]{64}$/', $sha)
            || !preg_match('/^[a-f0-9]{64}$/', $inventory_fp)
            || $inventory_affiliate === ''
            || $imported_at <= 0) {
            return new WP_Error('digistore24_manual_affiliation_inventory_invalid', 'Manueller Digistore24-CSV-Nachweis ist unvollständig oder ungültig.');
        }

        $settings = $this->digistore24_settings();
        $settings_fp = strtolower(trim((string) ($settings['tested_key_fingerprint'] ?? '')));
        $settings_affiliate = $this->digistore24_normalize_affiliate_id($settings['affiliate_id'] ?? '');
        if (!preg_match('/^[a-f0-9]{64}$/', $settings_fp)
            || $settings_affiliate === ''
            || !hash_equals($inventory_fp, $settings_fp)
            || !hash_equals($inventory_affiliate, $settings_affiliate)) {
            return new WP_Error('digistore24_manual_affiliation_inventory_mismatch', 'Manueller Digistore24-CSV-Nachweis gehört nicht zum aktuell gebundenen Zugang.');
        }

        // If a raw API key is currently configured, it must still reproduce the
        // exact tested fingerprint. If the key is intentionally not persisted,
        // the import-time tested fingerprint remains the durable identity proof.
        $key = $this->digistore24_api_key($settings);
        if ($key !== '' && !hash_equals($settings_fp, $this->digistore24_key_fingerprint($key))) {
            return new WP_Error('digistore24_manual_affiliation_current_key_mismatch', 'Aktueller Digistore24-Schlüssel passt nicht zum gebundenen CSV-Nachweis.');
        }

        return array(
            'key_fingerprint'=>$inventory_fp,
            'affiliate_id'=>$inventory_affiliate,
            'imported_at'=>$imported_at,
            'import_sha256'=>$sha,
        );
    }

    private function digistore24_manual_csv_partnership_gate($entry_id, $product_id = '') {
        $entry_id = preg_replace('/[^0-9]/', '', (string) $entry_id);
        $product_id = preg_replace('/[^0-9]/', '', (string) $product_id);
        $partnerships = get_option('ppar_digistore24_partnerships_v1', array());
        $record = is_array($partnerships[$entry_id] ?? null) ? $partnerships[$entry_id] : array();
        if (!$record
            || empty($record['confirmed'])
            || sanitize_key((string) ($record['source'] ?? '')) !== 'manual_csv'
            || sanitize_key((string) ($record['approval_status'] ?? '')) !== 'approved') {
            return new WP_Error('digistore24_manual_affiliation_partnership_missing', 'Genehmigter manueller Digistore24-CSV-Partnerschaftsnachweis fehlt für diese Werbemittelquelle.');
        }

        $record_fp = strtolower(trim((string) ($record['key_fingerprint'] ?? '')));
        $record_affiliate = $this->digistore24_normalize_affiliate_id($record['affiliate_id'] ?? '');
        $record_sha = preg_replace('/[^a-f0-9]/', '', strtolower((string) ($record['import_sha256'] ?? '')));
        $record_time = max(absint($record['imported_at'] ?? 0), absint($record['confirmed_at'] ?? 0));
        if (!preg_match('/^[a-f0-9]{64}$/', $record_fp)
            || $record_affiliate === ''
            || !preg_match('/^[a-f0-9]{64}$/', $record_sha)
            || $record_time <= 0) {
            return new WP_Error('digistore24_manual_affiliation_partnership_invalid', 'Manueller Digistore24-CSV-Partnerschaftsnachweis ist unvollständig oder ungültig.');
        }

        $approved_products = array();
        foreach ((array) ($record['product_ids'] ?? array()) as $pid) {
            $pid = preg_replace('/[^0-9]/', '', (string) $pid);
            if ($pid !== '') { $approved_products[$pid] = true; }
        }
        if (!$approved_products) {
            return new WP_Error('digistore24_manual_affiliation_partnership_products_missing', 'Manueller Digistore24-CSV-Partnerschaftsnachweis enthält keine gebundenen Produkte.');
        }
        if ($product_id !== '' && !isset($approved_products[$product_id])) {
            return new WP_Error('digistore24_manual_affiliation_partnership_product_mismatch', 'Tracking-Produkt ist nicht an den genehmigten manuellen Digistore24-CSV-Nachweis dieser Werbemittelquelle gebunden.');
        }

        $settings = $this->digistore24_settings();
        $settings_fp = strtolower(trim((string) ($settings['tested_key_fingerprint'] ?? '')));
        $settings_affiliate = $this->digistore24_normalize_affiliate_id($settings['affiliate_id'] ?? '');
        if ($settings_fp !== '' && (!preg_match('/^[a-f0-9]{64}$/', $settings_fp) || !hash_equals($record_fp, $settings_fp))) {
            return new WP_Error('digistore24_manual_affiliation_partnership_fingerprint_mismatch', 'Manueller Digistore24-CSV-Nachweis gehört nicht zum aktuell gebundenen Zugang.');
        }
        if ($settings_affiliate !== '' && !hash_equals($record_affiliate, $settings_affiliate)) {
            return new WP_Error('digistore24_manual_affiliation_partnership_affiliate_mismatch', 'Manueller Digistore24-CSV-Nachweis gehört nicht zur aktuell gebundenen Affiliate-ID.');
        }
        $key = $this->digistore24_api_key($settings);
        if ($key !== '' && !hash_equals($record_fp, $this->digistore24_key_fingerprint($key))) {
            return new WP_Error('digistore24_manual_affiliation_partnership_key_mismatch', 'Aktueller Digistore24-Schlüssel passt nicht zum manuellen CSV-Partnerschaftsnachweis.');
        }

        return array(
            'product_id'=>$product_id,
            'entry_id'=>$entry_id,
            'approved_product_ids'=>array_keys($approved_products),
            'product_is_active'=>true,
            'approval_status'=>'approved',
            'checked_at'=>$record_time,
            'key_fingerprint'=>$record_fp,
            'affiliate_id'=>$record_affiliate,
            'source'=>'manual_csv_partnership',
            'import_sha256'=>$record_sha,
        );
    }


    /** Legacy-safe proof from the original manual CSV marketplace snapshot. */
    private function digistore24_manual_csv_marketplace_gate($entry_id, $product_id = '') {
        $entry_id = preg_replace('/[^0-9]/', '', (string) $entry_id);
        $product_id = preg_replace('/[^0-9]/', '', (string) $product_id);
        if ($entry_id === '') { return new WP_Error('digistore24_manual_marketplace_entry_missing', 'Kanonische Digistore24-Werbemittel-ID fehlt.'); }
        $store = get_option('ppar_digistore24_marketplace_v1', array());
        $store = is_array($store) ? $store : array();
        $store_fp = strtolower(trim((string) ($store['key_fingerprint'] ?? '')));
        $store_affiliate = $this->digistore24_normalize_affiliate_id($store['affiliate_id'] ?? '');
        if (!preg_match('/^[a-f0-9]{64}$/', $store_fp) || $store_affiliate === '') {
            return new WP_Error('digistore24_manual_marketplace_identity_invalid', 'Gebundene Identität des manuellen Digistore24-CSV-Snapshots fehlt.');
        }
        $entry = array();
        foreach ((array) ($store['items'] ?? array()) as $item) {
            if (is_array($item) && preg_replace('/[^0-9]/', '', (string) ($item['id'] ?? '')) === $entry_id) { $entry = $item; break; }
        }
        if (!$entry || sanitize_key((string) ($entry['source_kind'] ?? '')) !== 'digistore24_manual_csv' || sanitize_key((string) ($entry['approval_status'] ?? '')) !== 'approved') {
            return new WP_Error('digistore24_manual_marketplace_entry_not_approved', 'Werbemittelquelle ist im gebundenen manuellen Digistore24-CSV-Snapshot nicht genehmigt.');
        }
        $sha = preg_replace('/[^a-f0-9]/', '', strtolower((string) ($entry['manual_import_sha256'] ?? '')));
        $imported_at = absint($entry['manual_imported_at'] ?? 0);
        if (!preg_match('/^[a-f0-9]{64}$/', $sha) || $imported_at <= 0) {
            return new WP_Error('digistore24_manual_marketplace_import_proof_invalid', 'Importbeweis der manuellen Digistore24-Werbemittelquelle ist unvollständig.');
        }
        $approved = array();
        foreach ((array) ($entry['all_product_ids'] ?? array()) as $pid) {
            $pid = preg_replace('/[^0-9]/', '', (string) $pid); if ($pid !== '') { $approved[$pid] = true; }
        }
        $main = preg_replace('/[^0-9]/', '', (string) ($entry['main_product_id'] ?? ''));
        if ($main !== '') { $approved[$main] = true; }
        if (!$approved) { return new WP_Error('digistore24_manual_marketplace_products_missing', 'Gebundene manuelle Digistore24-Werbemittelquelle enthält keine genehmigten Produkte.'); }
        if ($product_id !== '' && !isset($approved[$product_id])) {
            return new WP_Error('digistore24_manual_marketplace_product_mismatch', 'Tracking-Produkt gehört nicht zur gebundenen manuellen Digistore24-Werbemittelquelle.');
        }
        $settings = $this->digistore24_settings();
        $settings_fp = strtolower(trim((string) ($settings['tested_key_fingerprint'] ?? '')));
        $settings_affiliate = $this->digistore24_normalize_affiliate_id($settings['affiliate_id'] ?? '');
        if ($settings_fp !== '' && (!preg_match('/^[a-f0-9]{64}$/', $settings_fp) || !hash_equals($store_fp, $settings_fp))) {
            return new WP_Error('digistore24_manual_marketplace_fingerprint_mismatch', 'Gebundener manueller Digistore24-CSV-Snapshot gehört nicht zum aktuell gesetzten Zugang.');
        }
        if ($settings_affiliate !== '' && !hash_equals($store_affiliate, $settings_affiliate)) {
            return new WP_Error('digistore24_manual_marketplace_affiliate_mismatch', 'Gebundener manueller Digistore24-CSV-Snapshot gehört nicht zur aktuell gesetzten Affiliate-ID.');
        }
        $key = $this->digistore24_api_key($settings);
        if ($key !== '' && !hash_equals($store_fp, $this->digistore24_key_fingerprint($key))) {
            return new WP_Error('digistore24_manual_marketplace_key_mismatch', 'Aktueller Digistore24-Schlüssel passt nicht zum gebundenen manuellen CSV-Snapshot.');
        }
        return array(
            'product_id'=>$product_id,'entry_id'=>$entry_id,'approved_product_ids'=>array_keys($approved),
            'product_is_active'=>true,'approval_status'=>'approved','checked_at'=>$imported_at,
            'key_fingerprint'=>$store_fp,'affiliate_id'=>$store_affiliate,'source'=>'manual_csv_marketplace',
            'import_sha256'=>$sha,
        );
    }

    private function digistore24_manual_csv_source_bound($entry_id) {
        $entry_id = preg_replace('/[^0-9]/', '', (string) $entry_id);
        if ($entry_id === '') { return false; }
        $inventory = get_option('ppar_digistore24_manual_inventory_v1', array());
        foreach ((array) (is_array($inventory) ? ($inventory['rows'] ?? array()) : array()) as $row) {
            if (is_array($row) && preg_replace('/[^0-9]/', '', (string) ($row['entry_id'] ?? '')) === $entry_id) { return true; }
        }
        $partnerships = get_option('ppar_digistore24_partnerships_v1', array());
        $record = is_array($partnerships[$entry_id] ?? null) ? $partnerships[$entry_id] : array();
        if ($record && sanitize_key((string) ($record['source'] ?? '')) === 'manual_csv') { return true; }
        $store = get_option('ppar_digistore24_marketplace_v1', array());
        foreach ((array) (is_array($store) ? ($store['items'] ?? array()) : array()) as $item) {
            if (is_array($item)
                && preg_replace('/[^0-9]/', '', (string) ($item['id'] ?? '')) === $entry_id
                && sanitize_key((string) ($item['source_kind'] ?? '')) === 'digistore24_manual_csv') { return true; }
        }
        return false;
    }

    private function digistore24_manual_csv_affiliation_gate($entry_id, $product_id = '') {
        $entry_id = preg_replace('/[^0-9]/', '', (string) $entry_id);
        $product_id = preg_replace('/[^0-9]/', '', (string) $product_id);
        if ($entry_id === '') {
            return new WP_Error('digistore24_manual_affiliation_identity_missing', 'Kanonische Digistore24-Werbemittel-ID für den manuellen Partnerschaftsnachweis fehlt.');
        }

        $inventory = get_option('ppar_digistore24_manual_inventory_v1', array());
        $inventory = is_array($inventory) ? $inventory : array();
        $rows = is_array($inventory['rows'] ?? null) ? $inventory['rows'] : array();
        if ($rows) {
            // A present current inventory is authoritative. A revoked/missing
            // entry or product must never be resurrected from older snapshots.
            $identity = $this->digistore24_manual_csv_bound_identity($inventory);
            if (is_wp_error($identity)) { return $identity; }
            $approved_products = array();
            foreach ($rows as $row_product_id => $row) {
                if (!is_array($row)) { continue; }
                $row_pid = preg_replace('/[^0-9]/', '', (string) ($row['product_id'] ?? $row_product_id));
                $row_entry = preg_replace('/[^0-9]/', '', (string) ($row['entry_id'] ?? ''));
                if ($row_pid === '' || $row_entry !== $entry_id || sanitize_key((string) ($row['status'] ?? '')) !== 'approved') { continue; }
                $approved_products[$row_pid] = true;
            }
            if (!$approved_products) {
                return new WP_Error('digistore24_manual_affiliation_inventory_entry_missing', 'Werbemittelquelle ist in der aktuellen genehmigten Digistore24-CSV nicht mehr freigegeben.');
            }
            if ($product_id !== '' && !isset($approved_products[$product_id])) {
                return new WP_Error('digistore24_manual_affiliation_inventory_row_missing', 'Tracking-Produkt ist in der aktuellen genehmigten Digistore24-CSV nicht an diese Werbemittelquelle gebunden.');
            }
            return array(
                'product_id'=>$product_id,
                'entry_id'=>$entry_id,
                'approved_product_ids'=>array_keys($approved_products),
                'product_is_active'=>true,
                'approval_status'=>'approved',
                'checked_at'=>absint($identity['imported_at'] ?? 0),
                'key_fingerprint'=>(string) ($identity['key_fingerprint'] ?? ''),
                'affiliate_id'=>(string) ($identity['affiliate_id'] ?? ''),
                'source'=>'manual_csv_inventory',
                'import_sha256'=>(string) ($identity['import_sha256'] ?? ''),
            );
        }

        // Legacy-safe path: first use the exact per-entry proof persisted by
        // newer imports. Older live imports predate that option but already
        // contain a bound manual-CSV marketplace snapshot; use it only when the
        // per-entry proof is genuinely absent, never to resurrect an invalid one.
        $partnerships = get_option('ppar_digistore24_partnerships_v1', array());
        if (is_array($partnerships) && array_key_exists($entry_id, $partnerships)) {
            return $this->digistore24_manual_csv_partnership_gate($entry_id, $product_id);
        }
        return $this->digistore24_manual_csv_marketplace_gate($entry_id, $product_id);
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
        $previous_store = $this->digistore24_marketplace_store();
        $previous_urls = array();
        foreach ((array) ($previous_store['items'] ?? array()) as $previous_item) {
            if (is_array($previous_item) && $this->digistore24_is_https_url((string) ($previous_item['support_url'] ?? ''))) {
                $previous_urls[(string) ($previous_item['id'] ?? '')] = (string) $previous_item['support_url'];
            }
        }
        $items = array();
        $blocked = 0;
        foreach ($entries as $entry) {
            $normalized = $this->digistore24_normalize_marketplace_entry($entry);
            if (is_wp_error($normalized)) {
                $blocked++;
                continue;
            }
            if (isset($previous_urls[(string) $normalized['id']])) { $normalized['support_url'] = $previous_urls[(string) $normalized['id']]; }
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
        $previous = $this->digistore24_marketplace_item($requested_entry_id);
        if ($this->digistore24_is_https_url((string) ($previous['support_url'] ?? ''))) { $normalized['support_url'] = (string) $previous['support_url']; }
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
        $processed = 0; $imported = 0; $needs_url = 0; $blocked = 0;
        foreach (array_slice((array) ($result['items'] ?? array()), 0, 5) as $entry) {
            $product_id = (string) ($entry['main_product_id'] ?? '');
            if ($product_id === '') { $blocked++; continue; }
            $proof = $this->digistore24_affiliation_gate($product_id, true);
            if (is_wp_error($proof)) { $blocked++; continue; }
            $processed++;
            $support_url = (string) ($entry['support_url'] ?? '');
            if (!$this->digistore24_is_https_url($support_url)) { $needs_url++; continue; }
            $banner_result = $this->digistore24_import_vendor_banners((string) ($entry['id'] ?? ''), $support_url, true);
            if (is_wp_error($banner_result)) { $blocked++; continue; }
            $imported += absint($banner_result['imported'] ?? 0);
        }
        $result['automation_processed'] = $processed;
        $result['automation_imported'] = $imported;
        $result['requires_support_url'] = $needs_url;
        $result['automation_blocked'] = $blocked;
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
            $existing = is_array($items[$entry_id] ?? null) ? $items[$entry_id] : array();
            $items[$entry_id] = array_merge($existing, array(
                'confirmed'=>1,
                'confirmed_at'=>time(),
                'key_fingerprint'=>(string) $identity['key_fingerprint'],
                'affiliate_id'=>(string) $identity['affiliate_id'],
            ));
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

    private function digistore24_tracking_url_allowed($url, $bound_affiliate_id = '') {
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
        $bound_affiliate_id = $this->digistore24_normalize_affiliate_id($bound_affiliate_id);
        if ($bound_affiliate_id !== '') {
            // Manual-CSV publication may use the affiliate identity already bound
            // to that signed import proof. It must still match the current stored
            // affiliate identity exactly; no raw API key is required at render time.
            $settings = $this->digistore24_settings();
            $current_affiliate = $this->digistore24_normalize_affiliate_id($settings['affiliate_id'] ?? '');
            if ($current_affiliate === '' || !hash_equals($current_affiliate, $bound_affiliate_id)) {
                return false;
            }
            $affiliate_id = $bound_affiliate_id;
        } else {
            $settings = $this->digistore24_settings();
            $affiliate_id = $this->digistore24_normalize_affiliate_id($settings['affiliate_id'] ?? '');
            if ($affiliate_id === '' || !$this->digistore24_fingerprint_matches($settings)) {
                return false;
            }
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

    private function digistore24_tracking_product_id($url) {
        $url = esc_url_raw(html_entity_decode((string) $url, ENT_QUOTES, 'UTF-8'));
        if (!$this->digistore24_is_https_url($url)) {
            return '';
        }
        $path = trim((string) wp_parse_url($url, PHP_URL_PATH), '/');
        $segments = array_values(array_filter(array_map('rawurldecode', explode('/', $path)), 'strlen'));
        $first = strtolower((string) ($segments[0] ?? ''));
        if (!in_array($first, array('redir','content'), true)) {
            return '';
        }
        $product_id = (string) ($segments[1] ?? '');
        return $product_id !== '' && ctype_digit($product_id) ? $product_id : '';
    }

    private function digistore24_manual_entry_tracking_allowed($entry, $url) {
        $entry = is_array($entry) ? $entry : array();
        if ((string) ($entry['source_kind'] ?? '') !== 'digistore24_manual_csv') {
            return true;
        }
        $allowed = array();
        foreach ((array) ($entry['all_product_ids'] ?? array()) as $product_id) {
            $product_id = trim((string) $product_id);
            if ($product_id !== '' && ctype_digit($product_id)) {
                $allowed[$product_id] = true;
            }
        }
        $product_id = $this->digistore24_tracking_product_id($url);
        return $product_id !== '' && isset($allowed[$product_id]);
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

    private function digistore24_manual_promo_occurrences($html, $entry) {
        $html = html_entity_decode((string) $html, ENT_QUOTES, 'UTF-8');
        $entry = is_array($entry) ? $entry : array();
        if ((string) ($entry['source_kind'] ?? '') !== 'digistore24_manual_csv' || $html === '') {
            return array();
        }
        $allowed = array();
        foreach ((array) ($entry['all_product_ids'] ?? array()) as $product_id) {
            $product_id = trim((string) $product_id);
            if ($product_id !== '' && ctype_digit($product_id)) {
                $allowed[$product_id] = true;
            }
        }
        if (!$allowed) {
            return array();
        }
        $settings = $this->digistore24_settings();
        $affiliate_id = $this->digistore24_normalize_affiliate_id($settings['affiliate_id'] ?? '');
        if ($affiliate_id === '' || !$this->digistore24_fingerprint_matches($settings)) {
            return array();
        }
        $pattern = "#https?://(?:www\\.)?(?:checkout-ds24\\.com|digistore24\\.com)/redir/([0-9]+)/([^/\\s<>&\"\']+)(?:/[^\\s<>&\"\']+)?#i";
        if (!preg_match_all($pattern, $html, $matches, PREG_SET_ORDER | PREG_OFFSET_CAPTURE)) {
            return array();
        }
        $out = array();
        foreach ($matches as $match) {
            $product_id = (string) ($match[1][0] ?? '');
            $path_affiliate = rawurldecode((string) ($match[2][0] ?? ''));
            if ($product_id === '' || !isset($allowed[$product_id])) {
                continue;
            }
            if (strcasecmp($path_affiliate, 'AFFILIATE') !== 0 && !hash_equals($affiliate_id, $path_affiliate)) {
                continue;
            }
            $tracking_url = 'https://www.checkout-ds24.com/redir/' . rawurlencode($product_id) . '/' . rawurlencode($affiliate_id);
            if (!$this->digistore24_tracking_url_allowed($tracking_url)) {
                continue;
            }
            $out[] = array(
                'product_id' => $product_id,
                'offset' => absint($match[0][1] ?? 0),
                'tracking_url' => $tracking_url,
            );
        }
        return $out;
    }

    private function digistore24_manual_html_container_spans($html) {
        $html = (string) $html;
        $pattern = '#</?(div|section|article|li|tr|td)\\b[^>]*>#i';
        if (!preg_match_all($pattern, $html, $matches, PREG_SET_ORDER | PREG_OFFSET_CAPTURE)) {
            return array();
        }
        $stack = array();
        $spans = array();
        foreach ($matches as $match) {
            $token = (string) ($match[0][0] ?? '');
            $offset = absint($match[0][1] ?? 0);
            $tag = strtolower((string) ($match[1][0] ?? ''));
            if ($tag === '') { continue; }
            $closing = strpos($token, '</') === 0;
            if (!$closing) {
                $stack[] = array('tag'=>$tag,'start'=>$offset,'token'=>$token);
                continue;
            }
            for ($i = count($stack) - 1; $i >= 0; $i--) {
                if ((string) ($stack[$i]['tag'] ?? '') !== $tag) { continue; }
                $open = $stack[$i];
                $stack = array_slice($stack, 0, $i);
                $end = $offset + strlen($token);
                if ($end > (int) $open['start']) {
                    $open_token = (string) ($open['token'] ?? '');
                    $semantic = in_array($tag, array('section','article','li','tr'), true)
                        || (bool) preg_match('#\b(?:class|id)\s*=\s*(["\'])(?:(?!\1).)*(?:row|product|banner|partner|creative|werbemittel)(?:(?!\1).)*\1#i', $open_token);
                    $spans[] = array('tag'=>$tag,'start'=>(int)$open['start'],'end'=>$end,'length'=>$end-(int)$open['start'],'semantic'=>$semantic);
                }
                break;
            }
        }
        return $spans;
    }

    private function digistore24_manual_single_image_from_segment($segment, $support_url) {
        $segment = (string) $segment;
        if (!preg_match_all('#<img\\b([^>]*)>#is', $segment, $images, PREG_SET_ORDER)) {
            return array();
        }
        $valid = array();
        foreach ($images as $image) {
            $attrs = (string) ($image[1] ?? '');
            $src = '';
            foreach (array('src','data-src','data-lazy-src') as $attr) {
                if (preg_match("#\\b" . preg_quote($attr, "#") . "\\s*=\\s*([\"\'])(.*?)\\1#is", $attrs, $m)) {
                    $candidate = $this->digistore24_resolve_url($support_url, $m[2]);
                    if ($this->digistore24_is_https_url($candidate)) {
                        $src = $candidate;
                        break;
                    }
                }
            }
            if ($src === '') { continue; }
            $width = 0; $height = 0;
            if (preg_match("#\\bwidth\\s*=\\s*([\"\']?)([0-9]+)\\1#i", $attrs, $m)) { $width = absint($m[2]); }
            if (preg_match("#\\bheight\\s*=\\s*([\"\']?)([0-9]+)\\1#i", $attrs, $m)) { $height = absint($m[2]); }
            if (($width > 0 && $width < 80) || ($height > 0 && $height < 40)) { continue; }
            $alt = '';
            if (preg_match("#\\balt\\s*=\\s*([\"\'])(.*?)\\1#is", $attrs, $m)) {
                $alt = sanitize_text_field(wp_strip_all_tags(html_entity_decode((string) $m[2], ENT_QUOTES, 'UTF-8')));
            }
            $valid[$src] = array('image_url'=>$src,'alt_text'=>$alt);
        }
        return count($valid) === 1 ? array_values($valid)[0] : array();
    }

    private function digistore24_parse_manual_vendor_banner_blocks($html, $support_url, $entry) {
        $html = (string) $html;
        $occurrences = $this->digistore24_manual_promo_occurrences($html, $entry);
        if (!$occurrences) { return array(); }
        $spans = $this->digistore24_manual_html_container_spans($html);
        if (!$spans) { return array(); }
        $all_occurrences = $occurrences;
        $banners = array();
        foreach ($occurrences as $occurrence) {
            $offset = absint($occurrence['offset'] ?? 0);
            $product_id = (string) ($occurrence['product_id'] ?? '');
            $candidates = array_values(array_filter($spans, static function ($span) use ($offset) {
                return !empty($span['semantic'])
                    && (int)($span['start'] ?? 0) <= $offset
                    && (int)($span['end'] ?? 0) > $offset
                    && (int)($span['length'] ?? 0) <= 50000;
            }));
            usort($candidates, static function ($a, $b) { return ((int)$a['length']) <=> ((int)$b['length']); });
            foreach ($candidates as $span) {
                $start = (int) ($span['start'] ?? 0);
                $end = (int) ($span['end'] ?? 0);
                if ($end <= $start) { continue; }
                $ids = array();
                foreach ($all_occurrences as $other) {
                    $other_offset = absint($other['offset'] ?? 0);
                    if ($other_offset >= $start && $other_offset < $end) {
                        $ids[(string)($other['product_id'] ?? '')] = true;
                    }
                }
                unset($ids['']);
                if (count($ids) !== 1 || !isset($ids[$product_id])) { continue; }
                $segment = substr($html, $start, $end - $start);
                $image = $this->digistore24_manual_single_image_from_segment($segment, $support_url);
                if (!$image) { continue; }
                $tracking_url = (string) ($occurrence['tracking_url'] ?? '');
                if (!$this->digistore24_tracking_url_allowed($tracking_url)
                    || !$this->digistore24_manual_entry_tracking_allowed($entry, $tracking_url)) { continue; }
                $key = (string)$image['image_url'] . '|' . $tracking_url;
                $banners[$key] = array(
                    'tracking_url'=>$tracking_url,
                    'image_url'=>(string)$image['image_url'],
                    'alt_text'=>(string)($image['alt_text'] ?? ''),
                );
                break;
            }
        }
        return array_values($banners);
    }

    private function digistore24_parse_vendor_banners($html, $support_url, $entry) {
        $html = (string) $html;
        $entry = is_array($entry) ? $entry : array();
        $fallback = $this->digistore24_partner_link_fallback($entry);
        $banners = array();
        if ($html === '') {
            return $banners;
        }
        // Keep the image inside the same anchor. The older pattern could cross
        // a closing/opening <a> boundary and accidentally pair link A with image B.
        $pattern = '#<a\b[^>]*href\s*=\s*(["\'])(.*?)\1[^>]*>(?:(?!</?a\b).)*?<img\b([^>]*)>(?:(?!</a>).)*?</a>#is';
        $matches = array();
        preg_match_all($pattern, $html, $matches, PREG_SET_ORDER);
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
            if (!$this->digistore24_tracking_url_allowed($href)
                || !$this->digistore24_manual_entry_tracking_allowed($entry, $href)) {
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
        if (!$banners && (string) ($entry['source_kind'] ?? '') === 'digistore24_manual_csv') {
            $banners = $this->digistore24_parse_manual_vendor_banner_blocks($html, $support_url, $entry);
        }
        return $banners;
    }

    private function digistore24_store_support_url($entry_id, $support_url) {
        if (!$this->digistore24_is_https_url($support_url)) { return new WP_Error('digistore24_support_url_invalid', 'Vendor-Supportseite muss eine gültige HTTPS-URL sein.'); }
        $store = $this->digistore24_marketplace_store(); $found = false;
        if (empty($store['items']) || !is_array($store['items'])) {
            return new WP_Error('digistore24_marketplace_entry_required', 'Vendor-URL gehört zu keinem aktuellen Marketplace-Eintrag.');
        }
        foreach ($store['items'] as &$item) {
            if (is_array($item) && (string) ($item['id'] ?? '') === (string) $entry_id) { $item['support_url'] = esc_url_raw($support_url); $found = true; break; }
        }
        unset($item);
        if (!$found) { return new WP_Error('digistore24_marketplace_entry_required', 'Vendor-URL gehört zu keinem aktuellen Marketplace-Eintrag.'); }
        update_option('ppar_digistore24_marketplace_v1', $store, false); return true;
    }

    private function digistore24_import_vendor_banners($entry_id, $support_url, $automatic = false) {
        $entry_id = preg_replace('/[^0-9]/', '', (string) $entry_id);
        $cached_entry = $this->digistore24_marketplace_item($entry_id);
        $automatic_proof = $automatic ? $this->digistore24_affiliation_gate((string) ($cached_entry['main_product_id'] ?? ''), false) : false;
        if ($automatic && is_wp_error($automatic_proof)) { return $automatic_proof; }
        if (!$automatic && !$this->digistore24_partnership_confirmed($entry_id)) {
            return new WP_Error('digistore24_partnership_required', 'Vendor-Bannerimport bleibt bis zur manuellen Partnerschaftsbestätigung gesperrt.');
        }
        if (!$this->digistore24_is_https_url($support_url)) {
            return new WP_Error('digistore24_support_url_invalid', 'Vendor-Supportseite muss eine gültige HTTPS-URL sein.');
        }
        $stored_url = $this->digistore24_store_support_url($entry_id, $support_url);
        if (is_wp_error($stored_url)) { return $stored_url; }
        // A manual CSV import is already the bound source of truth for this
        // explicitly confirmed partnership. Do not make its banner import depend
        // on getMarketplaceEntry, which may be unavailable for publisher keys.
        $manual_csv = !$automatic && (string) ($cached_entry['source_kind'] ?? '') === 'digistore24_manual_csv';
        if ($manual_csv) {
            $entry = $cached_entry;
        } else {
            $entry = $this->digistore24_refresh_marketplace_entry($entry_id);
            if (is_wp_error($entry)) {
                return $entry;
            }
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
            if (method_exists($this, 'output_plan_creative')) { $this->output_plan_creative($normalized, true); }
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
            <p class="description">Nur read-only GET: listMarketplaceEntries, getMarketplaceEntry, getAffiliateCommission und getUserInfo. Aktivierung erfolgt erst nach erfolgreichem Test desselben Schlüssels.</p>
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
            <form method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>"><input type="hidden" name="action" value="ppar_digistore24_import_banners"><input type="hidden" name="entry_id" value="<?php echo esc_attr($entry_id); ?>"><?php wp_nonce_field('ppar_digistore24_import_banners_' . $entry_id,'ppar_digistore24_nonce'); ?><label>Vendor-Support-/Werbemittelseite (HTTPS)<br><input class="large-text" type="url" name="support_url" value="<?php echo esc_attr((string)($entry['support_url'] ?? '')); ?>" placeholder="https://..."></label><p><button class="button" type="submit" <?php disabled(!$confirmed); ?>>Vendor-Banner prüfen &amp; importieren</button></p><p class="description">Importiert nur Banner mit zulässigem Digistore24-Trackinglink. Keine automatische öffentliche Aktivierung.</p></form>
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

    public function digistore24_final_publication_guard() {
        if (!method_exists($this, 'output_objects_table') || !method_exists($this, 'output_finalize_digistore24_object')) { return; }
        global $wpdb;
        if (!is_object($wpdb)) { return; }
        $table = $this->output_objects_table();
        $objects = $wpdb->get_results("SELECT * FROM {$table} WHERE provider='digistore24' AND status='published' ORDER BY updated_at ASC LIMIT 20", ARRAY_A);
        foreach ((array) $objects as $object) {
            $result = $this->output_finalize_digistore24_object($object);
            if (is_wp_error($result)) {
                // The final provider gate always wins over an earlier generic
                // activator. Deactivation is idempotent and preserves conflicts.
                $this->output_deactivate_materialized_object($object, $result->get_error_message());
                $wpdb->update($table, array('status'=>'draft','decision_reason'=>$result->get_error_message(),'updated_at'=>time()), array('id'=>absint($object['id'] ?? 0)));
            }
        }
    }
}
