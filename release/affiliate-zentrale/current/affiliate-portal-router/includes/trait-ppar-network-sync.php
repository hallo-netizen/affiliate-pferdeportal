<?php
if (!defined('ABSPATH')) {
    exit;
}

trait PPAR_Network_Sync_Trait {
    private function network_sync_table($kind) {
        global $wpdb;
        $map = array(
            'programmes' => 'ppar_sync_programmes',
            'products' => 'ppar_sync_products',
            'runs' => 'ppar_sync_runs',
        );
        return $wpdb->prefix . ($map[$kind] ?? 'ppar_sync_unknown');
    }

    public function maybe_install_network_sync_schema() {
        // AF-062: the legacy router still defines Basic-Auth ADCELL handlers for
        // backwards source compatibility. Replace only their registered admin
        // routes before any admin-post dispatch; Awin keeps the existing path.
        $this->adcell_api_v2_bind_legacy_admin_routes();
        $installed = (string) get_option(self::OPTION_SYNC_SCHEMA_VERSION, '0');
        if ($installed === self::SYNC_SCHEMA_VERSION) {
            return;
        }
        require_once ABSPATH . 'wp-admin/includes/upgrade.php';
        global $wpdb;
        $charset = $wpdb->get_charset_collate();
        $programmes = $this->network_sync_table('programmes');
        $products = $this->network_sync_table('products');
        $runs = $this->network_sync_table('runs');

        dbDelta("CREATE TABLE {$programmes} (
            id bigint(20) unsigned NOT NULL AUTO_INCREMENT,
            network varchar(20) NOT NULL,
            external_id varchar(191) NOT NULL,
            name text NOT NULL,
            relationship varchar(60) NOT NULL DEFAULT '',
            status varchar(40) NOT NULL DEFAULT 'unknown',
            status_source varchar(255) NOT NULL DEFAULT '',
            first_seen bigint(20) unsigned NOT NULL DEFAULT 0,
            last_seen bigint(20) unsigned NOT NULL DEFAULT 0,
            payload longtext NULL,
            PRIMARY KEY  (id),
            UNIQUE KEY network_external (network, external_id),
            KEY network_status (network, status)
        ) {$charset};");

        dbDelta("CREATE TABLE {$products} (
            id bigint(20) unsigned NOT NULL AUTO_INCREMENT,
            network varchar(20) NOT NULL,
            external_key varchar(191) NOT NULL,
            programme_external_id varchar(191) NOT NULL DEFAULT '',
            programme_name text NOT NULL,
            title text NOT NULL,
            image_url text NOT NULL,
            tracking_url text NOT NULL,
            destination_url text NOT NULL,
            price varchar(80) NOT NULL DEFAULT '',
            currency varchar(20) NOT NULL DEFAULT '',
            brand text NOT NULL,
            category text NOT NULL,
            quality_status varchar(20) NOT NULL DEFAULT 'fail',
            source_hash char(64) NOT NULL,
            source_headers longtext NULL,
            payload longtext NULL,
            first_seen bigint(20) unsigned NOT NULL DEFAULT 0,
            last_seen bigint(20) unsigned NOT NULL DEFAULT 0,
            PRIMARY KEY  (id),
            UNIQUE KEY network_external (network, external_key),
            KEY network_quality (network, quality_status),
            KEY programme_lookup (network, programme_external_id)
        ) {$charset};");

        dbDelta("CREATE TABLE {$runs} (
            id bigint(20) unsigned NOT NULL AUTO_INCREMENT,
            network varchar(20) NOT NULL,
            operation varchar(60) NOT NULL,
            status varchar(20) NOT NULL,
            started_at bigint(20) unsigned NOT NULL DEFAULT 0,
            finished_at bigint(20) unsigned NOT NULL DEFAULT 0,
            items_seen int(10) unsigned NOT NULL DEFAULT 0,
            items_imported int(10) unsigned NOT NULL DEFAULT 0,
            items_updated int(10) unsigned NOT NULL DEFAULT 0,
            items_skipped int(10) unsigned NOT NULL DEFAULT 0,
            items_failed int(10) unsigned NOT NULL DEFAULT 0,
            message text NOT NULL,
            details longtext NULL,
            PRIMARY KEY  (id),
            KEY network_time (network, started_at)
        ) {$charset};");

        update_option(self::OPTION_SYNC_SCHEMA_VERSION, self::SYNC_SCHEMA_VERSION, false);
    }

    private function adcell_api_v2_bind_legacy_admin_routes() {
        if (!function_exists('remove_action') || !function_exists('add_action')) { return; }
        remove_action('admin_post_ppar_test_network', array($this, 'handle_test_network'));
        remove_action('admin_post_ppar_save_network', array($this, 'handle_save_network'));
        add_action('admin_post_ppar_test_network', array($this, 'handle_test_network_api_v2_safe'));
        add_action('admin_post_ppar_save_network', array($this, 'handle_save_network_api_v2_safe'));
    }

    public function handle_test_network_api_v2_safe() {
        $network = sanitize_key((string) ($_POST['network'] ?? ''));
        if ($network !== 'adcell') {
            return $this->handle_test_network();
        }
        if (!current_user_can('manage_options')) { wp_die('Keine Berechtigung.'); }
        check_admin_referer('ppar_test_network_adcell', 'ppar_network_test_nonce');
        $result = $this->adcell_api_v2_test_connection();
        $this->network_sync_update_connection_status('adcell', $result);
        $settings = $this->network_settings('adcell');
        wp_safe_redirect(add_query_arg(array(
            'ppar_network_test'=>'adcell',
            'ppar_network_status'=>(string) ($settings['last_status'] ?? '') === 'connected' ? 'connected' : 'failed',
        ), admin_url('admin.php?page=affiliate-portal-networks')));
        exit;
    }

    public function handle_save_network_api_v2_safe() {
        $network = sanitize_key((string) ($_POST['network'] ?? ''));
        if ($network !== 'adcell') {
            return $this->handle_save_network();
        }
        if (!current_user_can('manage_options')) { wp_die('Keine Berechtigung.'); }
        check_admin_referer('ppar_save_network_adcell', 'ppar_network_nonce');
        $posted = isset($_POST['ppar_network']['adcell']) && is_array($_POST['ppar_network']['adcell']) ? $_POST['ppar_network']['adcell'] : array();
        $saved = $this->persist_network_settings('adcell', $posted);
        $return_page = sanitize_key((string) ($_POST['return_page'] ?? 'affiliate-portal-networks'));
        if (!in_array($return_page, array('affiliate-portal-networks','affiliate-portal-provider-adcell'), true)) { $return_page = 'affiliate-portal-networks'; }
        $args = array('page'=>$return_page);
        if (is_wp_error($saved)) {
            $args['ppar_network_save_error'] = 'adcell';
        } else {
            $args['ppar_network_saved'] = 'adcell';
            if (sanitize_key((string) ($_POST['ppar_network_action'] ?? 'save')) === 'save_test') {
                $result = $this->adcell_api_v2_test_connection();
                $this->network_sync_update_connection_status('adcell', $result);
                $settings = $this->network_settings('adcell');
                $args['ppar_network_test'] = 'adcell';
                $args['ppar_network_status'] = (string) ($settings['last_status'] ?? '') === 'connected' ? 'connected' : 'failed';
            }
        }
        wp_safe_redirect(add_query_arg($args, admin_url('admin.php')));
        exit;
    }

    private function network_sync_validate_feed_url($network, $url) {
        $url = trim((string) $url);
        if ($url === '' || !wp_http_validate_url($url)) {
            return new WP_Error('invalid_feed_url', 'Es ist keine gültige HTTPS-Export-URL gespeichert.');
        }
        $parts = wp_parse_url($url);
        $scheme = strtolower((string) ($parts['scheme'] ?? ''));
        $host = strtolower((string) ($parts['host'] ?? ''));
        if ($scheme !== 'https' || $host === '') {
            return new WP_Error('invalid_feed_url', 'Die Export-URL muss eine gültige HTTPS-Adresse sein.');
        }
        if ($network === 'awin' && $host !== 'productdata.awin.com') {
            return new WP_Error('invalid_awin_host', 'Die Awin-Export-URL muss von productdata.awin.com stammen.');
        }
        if (in_array($host, array('localhost', '127.0.0.1', '::1'), true)) {
            return new WP_Error('blocked_feed_host', 'Lokale Adressen sind nicht zulässig.');
        }
        return $url;
    }

    /**
     * ADCELL API-v2 is token based. The API host and four business endpoints
     * below are bound to the official ADCELL v2 documentation; no account URL
     * from the legacy www.adcell.de settings is used for API requests.
     */
    private function adcell_api_v2_base_url() {
        return 'https://api.adcell.org/api/v2/';
    }

    private function adcell_api_v2_extract_token($body) {
        $body = trim((string) $body);
        if ($body === '') {
            return new WP_Error('adcell_token_empty', 'ADCELL lieferte keinen API-Token.');
        }
        $decoded = json_decode($body, true);
        $token = '';
        if (is_string($decoded)) {
            $token = trim($decoded);
        } elseif (is_array($decoded)) {
            if (isset($decoded['data']) && is_array($decoded['data']) && is_scalar($decoded['data']['token'] ?? null)) {
                $token = trim((string) $decoded['data']['token']);
            } elseif (isset($decoded['data']) && is_scalar($decoded['data'])) {
                $token = trim((string) $decoded['data']);
            } elseif (is_scalar($decoded['token'] ?? null)) {
                $token = trim((string) $decoded['token']);
            }
        } elseif ($decoded === null && $body[0] !== '<' && strpos($body, '{') === false && strpos($body, '[') === false) {
            $token = $body;
        }
        if ($token === '' || strlen($token) < 8 || strlen($token) > 1024 || preg_match('/[\x00-\x20]/', $token)) {
            return new WP_Error('adcell_token_invalid', 'ADCELL lieferte keinen auswertbaren API-Token.');
        }
        return $token;
    }

    private function adcell_api_v2_token() {
        $settings = $this->network_settings('adcell');
        $username = $this->network_secret('adcell', 'username', $settings);
        $password = $this->network_secret('adcell', 'password', $settings);
        if ($username === '' || $password === '') {
            return new WP_Error('adcell_credentials_missing', 'ADCELL API-Benutzername oder API-Passwort fehlt.');
        }
        $token_path = '/user/getToken';
        $url = add_query_arg(array(
            'userName' => $username,
            'password' => $password,
        ), $this->adcell_api_v2_base_url() . ltrim($token_path, '/'));
        $response = $this->api_response(wp_safe_remote_get($url, array(
            'timeout' => 20,
            'redirection' => 0,
            'headers' => array('Accept' => 'application/json'),
            'limit_response_size' => 131072,
        )));
        if (empty($response['ok'])) {
            return new WP_Error('adcell_token_request_failed', 'ADCELL-Token konnte nicht erzeugt werden: ' . sanitize_text_field((string) ($response['message'] ?? 'HTTP-Fehler')));
        }
        return $this->adcell_api_v2_extract_token((string) ($response['body'] ?? ''));
    }

    private function adcell_api_v2_request($path, $params = array(), $token = '') {
        $path = '/' . ltrim((string) $path, '/');
        $allowed_paths = array(
            '/affiliate/program/export',
            '/affiliate/promotion/getPromotionTypeCsv',
            '/affiliate/promotion/getPromotionTypeBanner',
            '/affiliate/promotion/getPromotionTypeDeeplink',
        );
        if (!in_array($path, $allowed_paths, true)) {
            return new WP_Error('adcell_api_path_blocked', 'Nicht gebundener ADCELL-API-v2-Pfad wurde blockiert.');
        }
        if ($token === '') {
            $token = $this->adcell_api_v2_token();
            if (is_wp_error($token)) { return $token; }
        }
        $allowed_params = array(
            'affiliateStatus','programId','programIds','programIds[]','promotionId','promotionCategoryId',
            'outputSubId','outputTarget','outputDomElementId','outputEncryption','outputPostView',
            'showJsCode','showHtmlCode','outputText','outputDeeplink','rows','page',
        );
        $query = array();
        foreach ((array) $params as $key => $value) {
            $key = (string) $key;
            if (!in_array($key, $allowed_params, true)) { continue; }
            if (is_array($value)) {
                $query[$key] = array_values(array_map('strval', $value));
            } elseif (is_scalar($value)) {
                $query[$key] = (string) $value;
            }
        }
        $query['token'] = (string) $token;
        $url = add_query_arg($query, $this->adcell_api_v2_base_url() . ltrim($path, '/'));
        $response = $this->api_response(wp_safe_remote_get($url, array(
            'timeout' => 25,
            'redirection' => 0,
            'headers' => array('Accept' => 'application/json'),
            'limit_response_size' => 4194304,
        )));
        if (empty($response['ok'])) {
            return new WP_Error('adcell_api_request_failed', 'ADCELL API v2 nicht erreichbar: ' . sanitize_text_field((string) ($response['message'] ?? 'HTTP-Fehler')));
        }
        $json = json_decode((string) ($response['body'] ?? ''), true);
        if (!is_array($json)) {
            return new WP_Error('adcell_api_json_invalid', 'ADCELL API v2 lieferte keine gültige JSON-Antwort.');
        }
        if (isset($json['status']) && (string) $json['status'] !== '200') {
            return new WP_Error('adcell_api_status_failed', 'ADCELL API v2 meldet: ' . sanitize_text_field((string) ($json['message'] ?? $json['status'])));
        }
        if (!isset($json['data']) || !is_array($json['data'])) {
            return new WP_Error('adcell_api_data_missing', 'ADCELL API v2 lieferte keinen auswertbaren Datenblock.');
        }
        return $json;
    }

    private function adcell_program_id_allowlist() {
        $raw = get_option('ppar_adcell_program_id_allowlist_v1', array());
        if (is_string($raw)) {
            $raw = preg_split('/[^0-9]+/', $raw, -1, PREG_SPLIT_NO_EMPTY);
        }
        $ids = array();
        foreach ((array) $raw as $id) {
            $id = absint($id);
            if ($id > 0) { $ids[$id] = $id; }
        }
        ksort($ids, SORT_NUMERIC);
        return array_values($ids);
    }

    private function adcell_save_program_id_allowlist($raw) {
        if (is_string($raw)) {
            $raw = preg_split('/[^0-9]+/', $raw, -1, PREG_SPLIT_NO_EMPTY);
        }
        $ids = array();
        foreach ((array) $raw as $id) {
            $id = absint($id);
            if ($id > 0) { $ids[$id] = $id; }
        }
        ksort($ids, SORT_NUMERIC);
        $ids = array_values($ids);
        update_option('ppar_adcell_program_id_allowlist_v1', $ids, false);
        return $ids;
    }

    private function adcell_api_v2_programme_catalog() {
        $rows = get_option('ppar_adcell_programme_catalog_v1', array());
        return is_array($rows) ? $rows : array();
    }

    private function adcell_api_v2_programme_items($token = '') {
        if ($token === '') {
            $token = $this->adcell_api_v2_token();
            if (is_wp_error($token)) { return $token; }
        }
        $items = array();
        $rows = 1000;
        for ($page = 1; $page <= 20; $page++) {
            $result = $this->adcell_api_v2_request('/affiliate/program/export', array(
                'affiliateStatus' => 'accepted',
                'rows' => $rows,
                'page' => $page,
            ), $token);
            if (is_wp_error($result)) { return $result; }
            $data = (array) ($result['data'] ?? array());
            $page_items = isset($data['items']) && is_array($data['items']) ? array_values($data['items']) : array();
            foreach ($page_items as $row) {
                if (is_array($row)) { $items[] = $row; }
            }
            $total = absint($data['total']['totalItems'] ?? $data['total']['numberItems'] ?? 0);
            if (!$page_items || count($page_items) < $rows || ($total > 0 && count($items) >= $total)) { break; }
        }
        return $items;
    }

    private function adcell_api_v2_refresh_programme_catalog($token = '') {
        $rows = $this->adcell_api_v2_programme_items($token);
        if (is_wp_error($rows)) { return $rows; }
        $safe = array();
        foreach ($rows as $programme) {
            if (!is_array($programme)) { continue; }
            $id = absint($programme['programId'] ?? 0);
            $name = sanitize_text_field((string) ($programme['programName'] ?? ''));
            $affiliate_status = strtolower(trim((string) ($programme['affiliateStatus'] ?? '')));
            $active = (string) ($programme['isActive'] ?? '') === '1';
            if ($id <= 0 || $name === '' || $affiliate_status !== 'accepted' || !$active) { continue; }
            $safe[$id] = array(
                'id' => $id,
                'name' => $name,
                'relationship' => 'accepted',
                'status' => 'active',
                'affiliateStatus' => 'accepted',
                'isActive' => 1,
                'promotionCounts' => is_array($programme['promotionCounts'] ?? null) ? $programme['promotionCounts'] : array(),
            );
        }
        ksort($safe, SORT_NUMERIC);
        $safe = array_values($safe);
        update_option('ppar_adcell_programme_catalog_v1', $safe, false);
        return $safe;
    }

    private function adcell_api_v2_allowlisted_programmes($refresh = true) {
        $allowlist = $this->adcell_program_id_allowlist();
        if (!$allowlist) {
            return new WP_Error('adcell_program_allowlist_empty', 'ADCELL programId-Allowlist ist leer; alle Programme bleiben fail-closed gesperrt.');
        }
        $catalog = $refresh ? $this->adcell_api_v2_refresh_programme_catalog() : $this->adcell_api_v2_programme_catalog();
        if (is_wp_error($catalog)) { return $catalog; }
        $allowed = array_fill_keys($allowlist, true);
        $out = array();
        foreach ((array) $catalog as $programme) {
            if (!is_array($programme)) { continue; }
            $id = absint($programme['id'] ?? $programme['programId'] ?? 0);
            $accepted = strtolower(trim((string) ($programme['affiliateStatus'] ?? $programme['relationship'] ?? ''))) === 'accepted';
            $active = (string) ($programme['isActive'] ?? ($programme['status'] ?? '')) === '1'
                || sanitize_key((string) ($programme['status'] ?? '')) === 'active';
            if ($id <= 0 || !isset($allowed[$id]) || !$accepted || !$active) { continue; }
            $programme['id'] = $id;
            $programme['name'] = sanitize_text_field((string) ($programme['name'] ?? $programme['programName'] ?? ('ADCELL ' . $id)));
            $out[$id] = $programme;
        }
        if (!$out) {
            return new WP_Error('adcell_allowlist_no_active_programme', 'Kein freigegebenes ADCELL-Programm ist aktuell zugleich accepted und aktiv.');
        }
        return $out;
    }

    private function adcell_api_v2_programme($program_id) {
        $program_id = absint($program_id);
        if ($program_id <= 0 || !in_array($program_id, $this->adcell_program_id_allowlist(), true)) {
            return new WP_Error('adcell_program_not_allowlisted', 'ADCELL-Programm ist nicht in der expliziten programId-Allowlist freigegeben.');
        }
        $programmes = $this->adcell_api_v2_allowlisted_programmes(true);
        if (is_wp_error($programmes)) { return $programmes; }
        return isset($programmes[$program_id]) ? $programmes[$program_id] : new WP_Error('adcell_program_not_active_accepted', 'ADCELL-Programm ist aktuell nicht accepted und aktiv.');
    }

    private function adcell_api_v2_promotion_items($program_id, $type, $extra = array()) {
        $program_id = absint($program_id);
        $type = sanitize_key((string) $type);
        $paths = array(
            'csv' => '/affiliate/promotion/getPromotionTypeCsv',
            'banner' => '/affiliate/promotion/getPromotionTypeBanner',
            'deeplink' => '/affiliate/promotion/getPromotionTypeDeeplink',
        );
        if ($program_id <= 0 || !isset($paths[$type])) {
            return new WP_Error('adcell_promotion_request_invalid', 'Ungültiger ADCELL-Werbemittelabruf.');
        }
        if (!in_array($program_id, $this->adcell_program_id_allowlist(), true)) {
            return new WP_Error('adcell_program_not_allowlisted', 'ADCELL-Werbemittel für nicht freigegebenes Programm blockiert.');
        }
        $token = $this->adcell_api_v2_token();
        if (is_wp_error($token)) { return $token; }
        $items = array();
        $rows = 1000;
        for ($page = 1; $page <= 20; $page++) {
            $params = array_merge((array) $extra, array(
                'programIds[]' => $program_id,
                'rows' => $rows,
                'page' => $page,
                'showJsCode' => 0,
                'showHtmlCode' => 0,
            ));
            $result = $this->adcell_api_v2_request($paths[$type], $params, $token);
            if (is_wp_error($result)) { return $result; }
            $data = (array) ($result['data'] ?? array());
            $page_items = isset($data['items']) && is_array($data['items']) ? array_values($data['items']) : array();
            foreach ($page_items as $item) {
                if (!is_array($item) || absint($item['programId'] ?? 0) !== $program_id) { continue; }
                if (isset($item['affiliateStatus']) && strtolower(trim((string) $item['affiliateStatus'])) !== 'accepted') { continue; }
                $items[] = $item;
            }
            $total = absint($data['total']['numberItems'] ?? $data['total']['totalItems'] ?? 0);
            if (!$page_items || count($page_items) < $rows || ($total > 0 && count($items) >= $total)) { break; }
        }
        return $items;
    }

    private function adcell_api_v2_validate_csv_url($url) {
        $url = esc_url_raw((string) $url);
        if ($url === '' || !wp_http_validate_url($url)) {
            return new WP_Error('adcell_csv_url_invalid', 'ADCELL-CSV-Werbemittel enthält keine gültige Download-URL.');
        }
        $parts = wp_parse_url($url);
        if (strtolower((string) ($parts['scheme'] ?? '')) !== 'https'
            || strtolower((string) ($parts['host'] ?? '')) !== 'www.adcell.de'
            || strpos((string) ($parts['path'] ?? ''), '/promotion/csv') !== 0) {
            return new WP_Error('adcell_csv_host_blocked', 'ADCELL-CSV-URL stammt nicht vom dokumentierten Promotion-Downloadpfad.');
        }
        return $url;
    }

    private function adcell_api_v2_validate_tracking_asset_url($url) {
        $url = esc_url_raw((string) $url);
        if ($url === '' || !wp_http_validate_url($url)) { return ''; }
        $parts = wp_parse_url($url);
        if (strtolower((string) ($parts['scheme'] ?? '')) !== 'https'
            || strtolower((string) ($parts['host'] ?? '')) !== 't.adcell.com'
            || strpos((string) ($parts['path'] ?? ''), '/p/') !== 0) {
            return '';
        }
        return $url;
    }

    private function adcell_api_v2_test_connection() {
        $token = $this->adcell_api_v2_token();
        if (is_wp_error($token)) {
            return array('status'=>'failed','message'=>$token->get_error_message(),'programme_count'=>0);
        }
        $catalog = $this->adcell_api_v2_refresh_programme_catalog($token);
        if (is_wp_error($catalog)) {
            return array('status'=>'failed','message'=>$catalog->get_error_message(),'programme_count'=>0);
        }
        return array(
            'status'=>'connected',
            'message'=>'ADCELL API v2 per Token authentifiziert; accepted+aktive Programme read-only synchronisiert.',
            'programme_count'=>count($catalog),
        );
    }

    private function network_sync_normalize_header($header) {
        $header = remove_accents(strtolower(trim((string) $header)));
        $header = preg_replace('/[^a-z0-9]+/', '_', $header);
        return trim((string) $header, '_');
    }

    private function network_sync_header_aliases() {
        return array(
            'external_id' => array('aw_product_id','product_id','produkt_id','artikelnummer','merchant_product_id','sku','ean','gtin','id'),
            'programme_external_id' => array('merchant_id','advertiser_id','programme_id','program_id','partnerprogramm_id','shop_id'),
            'programme_name' => array('merchant_name','advertiser_name','programme_name','program_name','partnerprogramm','shop_name'),
            'title' => array('product_name','productname','product_title','title','name','produktname','artikelname'),
            'image_url' => array('merchant_image_url','product_image_url','image_url','image','bild_url','bild'),
            'tracking_url' => array('aw_deep_link','tracking_url','affiliate_url','click_url','deep_link','deeplink','trackinglink'),
            'destination_url' => array('merchant_deep_link','destination_url','product_url','shop_url','url','ziel_url'),
            'price' => array('search_price','current_price','price','produktpreis','preis'),
            'currency' => array('currency','waehrung','wahrung'),
            'brand' => array('brand_name','brand','marke'),
            'category' => array('merchant_category','category_name','product_category','category','produktkategorie','kategorie'),
        );
    }

    private function network_sync_detect_mapping($headers) {
        $normalized = array();
        foreach ($headers as $index => $header) {
            $normalized[$this->network_sync_normalize_header($header)] = array('index' => (int) $index, 'source' => (string) $header);
        }
        $mapping = array();
        foreach ($this->network_sync_header_aliases() as $target => $aliases) {
            foreach ($aliases as $alias) {
                if (isset($normalized[$alias])) {
                    $mapping[$target] = $normalized[$alias];
                    break;
                }
            }
        }
        return $mapping;
    }

    private function network_sync_detect_delimiter($line) {
        $candidates = array(",", ";", "\t", "|");
        $best = ',';
        $best_count = -1;
        foreach ($candidates as $candidate) {
            $count = substr_count((string) $line, $candidate);
            if ($count > $best_count) {
                $best = $candidate;
                $best_count = $count;
            }
        }
        return $best;
    }

    private function network_sync_parse_csv($body, $row_limit = 5000) {
        $body = preg_replace('/^\xEF\xBB\xBF/', '', (string) $body);
        if (trim($body) === '') {
            return new WP_Error('empty_csv', 'Die Exportdatei enthält keine auswertbaren Daten.');
        }
        $physical_lines = preg_split('/\r\n|\r|\n/', $body, 2);
        $first_line = isset($physical_lines[0]) ? (string) $physical_lines[0] : '';
        $delimiter = $this->network_sync_detect_delimiter($first_line);
        $stream = fopen('php://temp', 'r+');
        if (!$stream) {
            return new WP_Error('csv_stream_failed', 'Die Exportdatei konnte nicht lokal verarbeitet werden.');
        }
        fwrite($stream, $body);
        rewind($stream);
        $headers = fgetcsv($stream, 0, $delimiter, '"', '\\');
        if (!is_array($headers)) {
            fclose($stream);
            return new WP_Error('invalid_csv_header', 'Die Exportdatei enthält keine brauchbare Kopfzeile.');
        }
        $headers = array_map(static function ($value) { return trim((string) $value); }, $headers);
        if (count(array_filter($headers, 'strlen')) < 2) {
            fclose($stream);
            return new WP_Error('invalid_csv_header', 'Die Exportdatei enthält keine brauchbare Kopfzeile.');
        }
        $mapping = $this->network_sync_detect_mapping($headers);
        $rows = array();
        while (($values = fgetcsv($stream, 0, $delimiter, '"', '\\')) !== false) {
            if (count($rows) >= $row_limit) { break; }
            if (!array_filter($values, static function ($value) { return trim((string) $value) !== ''; })) { continue; }
            $row = array();
            foreach ($headers as $index => $header) {
                if ($header === '') { continue; }
                $row[$header] = isset($values[$index]) ? trim((string) $values[$index]) : '';
            }
            if ($row) { $rows[] = $row; }
        }
        fclose($stream);
        if (!$rows) {
            return new WP_Error('empty_csv_rows', 'Die Exportdatei enthält keine auswertbaren Produktzeilen.');
        }
        return array('headers' => $headers, 'mapping' => $mapping, 'delimiter' => $delimiter, 'rows' => $rows);
    }

    private function network_sync_mapped_value($row, $mapping, $field) {
        if (empty($mapping[$field]['source'])) { return ''; }
        $source = (string) $mapping[$field]['source'];
        return isset($row[$source]) ? trim((string) $row[$source]) : '';
    }

    private function network_sync_quality_status($title, $tracking_url, $destination_url, $image_url) {
        if ($title === '' || ($tracking_url === '' && $destination_url === '')) { return 'fail'; }
        if ($image_url === '') { return 'warn'; }
        return 'pass';
    }

    private function network_sync_insert_run($network, $operation, $status, $started, $counts, $message, $details = array()) {
        global $wpdb;
        $wpdb->insert($this->network_sync_table('runs'), array(
            'network' => sanitize_key($network),
            'operation' => sanitize_key($operation),
            'status' => sanitize_key($status),
            'started_at' => absint($started),
            'finished_at' => time(),
            'items_seen' => absint($counts['seen'] ?? 0),
            'items_imported' => absint($counts['imported'] ?? 0),
            'items_updated' => absint($counts['updated'] ?? 0),
            'items_skipped' => absint($counts['skipped'] ?? 0),
            'items_failed' => absint($counts['failed'] ?? 0),
            'message' => sanitize_text_field($message),
            'details' => wp_json_encode($details, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES),
        ), array('%s','%s','%s','%d','%d','%d','%d','%d','%d','%d','%s','%s'));
    }

    private function network_sync_upsert_programmes($network, $programmes, $source) {
        global $wpdb;
        $table = $this->network_sync_table('programmes');
        $now = time();
        $counts = array('seen' => 0, 'imported' => 0, 'updated' => 0, 'skipped' => 0, 'failed' => 0);
        foreach ($programmes as $programme) {
            if (!is_array($programme)) { $counts['skipped']++; continue; }
            $external_id = trim((string) ($programme['id'] ?? $programme['external_id'] ?? ''));
            $name = trim((string) ($programme['name'] ?? ''));
            if ($external_id === '' || $name === '') { $counts['failed']++; continue; }
            $counts['seen']++;
            $existing = (int) $wpdb->get_var($wpdb->prepare("SELECT id FROM {$table} WHERE network=%s AND external_id=%s", $network, $external_id));
            $data = array(
                'network' => $network,
                'external_id' => $external_id,
                'name' => sanitize_text_field($name),
                'relationship' => sanitize_key((string) ($programme['relationship'] ?? 'joined')),
                'status' => 'active',
                'status_source' => sanitize_text_field($source),
                'first_seen' => $existing ? (int) $wpdb->get_var($wpdb->prepare("SELECT first_seen FROM {$table} WHERE id=%d", $existing)) : $now,
                'last_seen' => $now,
                'payload' => wp_json_encode($programme, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES),
            );
            if ($existing) {
                $wpdb->update($table, $data, array('id' => $existing));
                $counts['updated']++;
            } else {
                $wpdb->insert($table, $data);
                $counts['imported']++;
            }
        }
        return $counts;
    }

    private function network_sync_upsert_products($network, $parsed) {
        global $wpdb;
        $table = $this->network_sync_table('products');
        $mapping = $parsed['mapping'];
        $headers = $parsed['headers'];
        $now = time();
        $counts = array('seen' => 0, 'imported' => 0, 'updated' => 0, 'skipped' => 0, 'failed' => 0, 'pass' => 0, 'warn' => 0);
        foreach ($parsed['rows'] as $row) {
            $counts['seen']++;
            $title = sanitize_text_field($this->network_sync_mapped_value($row, $mapping, 'title'));
            $tracking_url = esc_url_raw($this->network_sync_mapped_value($row, $mapping, 'tracking_url'));
            $destination_url = esc_url_raw($this->network_sync_mapped_value($row, $mapping, 'destination_url'));
            $image_url = esc_url_raw($this->network_sync_mapped_value($row, $mapping, 'image_url'));
            $external_id = sanitize_text_field($this->network_sync_mapped_value($row, $mapping, 'external_id'));
            $quality = $this->network_sync_quality_status($title, $tracking_url, $destination_url, $image_url);
            if ($quality === 'fail') { $counts['failed']++; continue; }
            $external_key = $external_id !== '' ? $external_id : hash('sha256', $title . '|' . $tracking_url . '|' . $destination_url);
            $external_key = substr($external_key, 0, 191);
            $source_hash = hash('sha256', wp_json_encode($row, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES));
            $existing = $wpdb->get_row($wpdb->prepare("SELECT id, source_hash, first_seen FROM {$table} WHERE network=%s AND external_key=%s", $network, $external_key), ARRAY_A);
            $data = array(
                'network' => $network,
                'external_key' => $external_key,
                'programme_external_id' => sanitize_text_field($this->network_sync_mapped_value($row, $mapping, 'programme_external_id')),
                'programme_name' => sanitize_text_field($this->network_sync_mapped_value($row, $mapping, 'programme_name')),
                'title' => $title,
                'image_url' => $image_url,
                'tracking_url' => $tracking_url,
                'destination_url' => $destination_url,
                'price' => sanitize_text_field($this->network_sync_mapped_value($row, $mapping, 'price')),
                'currency' => sanitize_text_field($this->network_sync_mapped_value($row, $mapping, 'currency')),
                'brand' => sanitize_text_field($this->network_sync_mapped_value($row, $mapping, 'brand')),
                'category' => sanitize_text_field($this->network_sync_mapped_value($row, $mapping, 'category')),
                'quality_status' => $quality,
                'source_hash' => $source_hash,
                'source_headers' => wp_json_encode($headers, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES),
                'payload' => wp_json_encode($row, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES),
                'first_seen' => $existing ? absint($existing['first_seen']) : $now,
                'last_seen' => $now,
            );
            if ($existing) {
                if (hash_equals((string) $existing['source_hash'], $source_hash)) {
                    $wpdb->update($table, array('last_seen' => $now), array('id' => absint($existing['id'])));
                    $counts['skipped']++;
                } else {
                    $wpdb->update($table, $data, array('id' => absint($existing['id'])));
                    $counts['updated']++;
                }
            } else {
                $wpdb->insert($table, $data);
                $counts['imported']++;
            }
            $counts[$quality]++;
        }
        return $counts;
    }

    private function network_sync_download_and_stage_products($network) {
        if ($network === 'adcell') {
            return new WP_Error('adcell_api_v2_automation_required', 'ADCELL-Produktdaten werden im Normalbetrieb ausschließlich aus API-v2-CSV-Werbemitteln der freigegebenen Programme bezogen.');
        }
        $settings = $this->network_settings($network);
        $url = (string) ($settings['product_feed_url'] ?? '');
        $validated = $this->network_sync_validate_feed_url($network, $url);
        if (is_wp_error($validated)) { return $validated; }
        $response = wp_safe_remote_get($validated, array(
            'timeout' => 60,
            'redirection' => 3,
            'headers' => array('Accept' => 'text/csv,text/plain,application/csv,application/octet-stream'),
            'limit_response_size' => 10485760,
        ));
        $parsed_response = $this->api_response($response);
        if (!$parsed_response['ok']) {
            return new WP_Error('feed_download_failed', 'Produktfeed nicht erreichbar: ' . $parsed_response['message']);
        }
        $parsed = $this->network_sync_parse_csv($parsed_response['body'], 5000);
        if (is_wp_error($parsed)) { return $parsed; }
        $counts = $this->network_sync_upsert_products($network, $parsed);
        return array('counts' => $counts, 'headers' => $parsed['headers'], 'mapping' => $parsed['mapping'], 'delimiter' => $parsed['delimiter']);
    }

    private function network_sync_update_connection_status($network, $result) {
        $option = $network === 'awin' ? self::OPTION_NETWORK_AWIN : self::OPTION_NETWORK_ADCELL;
        $settings = $this->network_settings($network);
        $settings['last_status'] = (string) ($result['status'] ?? 'failed');
        $settings['last_checked'] = time();
        $settings['last_message'] = sanitize_text_field((string) ($result['message'] ?? ''));
        if ($network === 'awin') {
            $settings['programme_count'] = absint($result['programme_count'] ?? $settings['programme_count'] ?? 0);
            $settings['feed_status'] = sanitize_key((string) ($result['feed_status'] ?? $settings['feed_status'] ?? 'not_configured'));
            $settings['feed_count'] = absint($result['feed_count'] ?? $settings['feed_count'] ?? 0);
        } else {
            $settings['programme_count'] = absint($result['programme_count'] ?? $settings['programme_count'] ?? 0);
        }
        update_option($option, $settings, false);
    }

    public function handle_run_network_sync() {
        if (!current_user_can('manage_options')) { wp_die('Keine Berechtigung.'); }
        check_admin_referer('ppar_run_network_sync', 'ppar_sync_nonce');
        $network = sanitize_key((string) ($_POST['network'] ?? ''));
        $operation = sanitize_key((string) ($_POST['operation'] ?? ''));
        if (!$this->provider_exists($network) || !$this->provider_supports($network, 'synchronization')) {
            wp_die('Provider ist nicht als Synchronisationsquelle registriert.');
        }
        $started = time();
        $status = 'failed';
        $message = 'Unbekannte Synchronisationsaktion.';
        $counts = array();
        $details = array();

        if ($network === 'adcell' && $operation === 'allowlist') {
            $ids = $this->adcell_save_program_id_allowlist($_POST['program_ids'] ?? '');
            $status = 'success';
            $message = $ids ? 'ADCELL programId-Allowlist gespeichert: ' . implode(', ', $ids) . '.' : 'ADCELL programId-Allowlist geleert; Automatisierung bleibt vollständig gesperrt.';
            $details = array('program_ids'=>$ids,'fail_closed'=>true);
        } elseif (in_array($network, array('awin','adcell'), true) && $operation === 'connection') {
            $result = $network === 'awin' ? $this->test_awin_connection() : $this->adcell_api_v2_test_connection();
            $this->network_sync_update_connection_status($network, $result);
            $status = ($result['status'] ?? '') === 'connected' ? 'success' : 'failed';
            $message = (string) ($result['message'] ?? 'Verbindungsprüfung beendet.');
            if ($status === 'success') {
                if ($network === 'awin') {
                    $programmes = get_option(self::OPTION_NETWORK_AWIN_PROGRAMMES, array());
                    $counts = $this->network_sync_upsert_programmes('awin', is_array($programmes) ? $programmes : array(), 'Awin Publisher API');
                } else {
                    $programmes = $this->adcell_api_v2_programme_catalog();
                    $counts = $this->network_sync_upsert_programmes('adcell', $programmes, 'ADCELL API v2 /affiliate/program/export');
                }
            }
        } elseif ($network === 'awin' && $operation === 'products') {
            $result = $this->network_sync_download_and_stage_products('awin');
            if (is_wp_error($result)) {
                $message = $result->get_error_message();
            } else {
                $status = 'success';
                $counts = $result['counts'];
                $details = array(
                    'source_headers' => $result['headers'],
                    'detected_mapping' => $result['mapping'],
                    'delimiter' => $result['delimiter'] === "\t" ? 'TAB' : $result['delimiter'],
                    'public_activation' => false,
                );
                $message = 'Produktdaten wurden ausschließlich in die interne Prüfstufe eingelesen. Es wurde nichts veröffentlicht.';
            }
        } elseif ($network === 'adcell' && $operation === 'products') {
            $message = 'Manueller ADCELL-Feedimport ist nicht der Normalbetrieb. Produktdaten laufen ausschließlich über API v2 und die freigegebenen programIds.';
        } else {
            $adapter = apply_filters('ppar_affiliate_provider_sync_dispatch', null, $network, $operation, self::PROVIDER_CONTRACT_VERSION);
            if (is_wp_error($adapter)) {
                $message = $adapter->get_error_message();
            } elseif (is_array($adapter)) {
                $status = sanitize_key((string)($adapter['status'] ?? 'failed')) === 'success' ? 'success' : 'failed';
                $message = sanitize_text_field((string)($adapter['message'] ?? 'Provider-Synchronisationsadapter abgeschlossen.'));
                $counts = is_array($adapter['counts'] ?? null) ? $adapter['counts'] : array();
                $details = is_array($adapter['details'] ?? null) ? $adapter['details'] : array();
            } else {
                $message = 'Für diesen Provider ist kein Synchronisationsadapter für diese Aktion registriert.';
            }
        }

        $this->network_sync_insert_run($network, $operation, $status, $started, $counts, $message, $details);
        wp_safe_redirect(add_query_arg(array(
            'page' => 'affiliate-portal-sync',
            'ppar_sync_network' => $network,
            'ppar_sync_status' => $status,
        ), admin_url('admin.php')));
        exit;
    }

    private function network_sync_counts($network) {
        global $wpdb;
        $programmes = $this->network_sync_table('programmes');
        $products = $this->network_sync_table('products');
        return array(
            'programmes' => (int) $wpdb->get_var($wpdb->prepare("SELECT COUNT(*) FROM {$programmes} WHERE network=%s AND status='active'", $network)),
            'products' => (int) $wpdb->get_var($wpdb->prepare("SELECT COUNT(*) FROM {$products} WHERE network=%s", $network)),
            'pass' => (int) $wpdb->get_var($wpdb->prepare("SELECT COUNT(*) FROM {$products} WHERE network=%s AND quality_status='pass'", $network)),
            'warn' => (int) $wpdb->get_var($wpdb->prepare("SELECT COUNT(*) FROM {$products} WHERE network=%s AND quality_status='warn'", $network)),
        );
    }

    private function network_sync_recent_runs() {
        global $wpdb;
        $runs = $this->network_sync_table('runs');
        return $wpdb->get_results("SELECT * FROM {$runs} ORDER BY id DESC LIMIT 20", ARRAY_A);
    }

    public function render_network_sync_page() {
        if (!current_user_can('manage_options')) { return; }
        $this->maybe_install_network_sync_schema();
        $awin = $this->network_settings('awin');
        $adcell = $this->network_settings('adcell');
        $awin_counts = $this->network_sync_counts('awin');
        $adcell_counts = $this->network_sync_counts('adcell');
        $adcell_catalog = $this->adcell_api_v2_programme_catalog();
        $adcell_allowlist = $this->adcell_program_id_allowlist();
        $runs = $this->network_sync_recent_runs();
        ?>
        <div class="wrap ppar-sync-page">
            <h1>Provider-Synchronisierung</h1>
            <p>Provider verwenden ihren registrierten Datenpfad. Awin nutzt zusätzlich die zentrale Feed-Prüfstufe; ADCELL den dokumentierten API-v2-Tokenweg. <strong>Keine synchronisierte Zeile wird automatisch öffentlich freigegeben.</strong></p>
            <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:18px;max-width:1200px">
                <section class="postbox" style="padding:18px">
                    <h2>Awin</h2>
                    <p><strong>Verbindung:</strong> <?php echo wp_strip_all_tags($this->network_status_html($awin)); ?><br>
                    <strong>Aktive Programme in Prüfstufe:</strong> <?php echo absint($awin_counts['programmes']); ?><br>
                    <strong>Produkte in Prüfstufe:</strong> <?php echo absint($awin_counts['products']); ?> (PASS <?php echo absint($awin_counts['pass']); ?> / WARN <?php echo absint($awin_counts['warn']); ?>)<br>
                    <strong>Awin-Produktfeed-Export-URL:</strong> <?php echo !empty($awin['product_feed_url']) ? 'gespeichert' : 'fehlt'; ?></p>
                    <form method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>" style="display:inline-block;margin-right:8px">
                        <input type="hidden" name="action" value="ppar_run_network_sync"><input type="hidden" name="network" value="awin"><input type="hidden" name="operation" value="connection"><?php wp_nonce_field('ppar_run_network_sync','ppar_sync_nonce'); ?>
                        <button class="button button-primary">Programme und Feedliste synchronisieren</button>
                    </form>
                    <form method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>" style="display:inline-block">
                        <input type="hidden" name="action" value="ppar_run_network_sync"><input type="hidden" name="network" value="awin"><input type="hidden" name="operation" value="products"><?php wp_nonce_field('ppar_run_network_sync','ppar_sync_nonce'); ?>
                        <button class="button" <?php disabled(empty($awin['product_feed_url'])); ?>>Produktfeed einlesen</button>
                    </form>
                </section>
                <section class="postbox" style="padding:18px">
                    <h2>ADCELL API v2</h2>
                    <p><strong>Verbindung:</strong> <?php echo wp_strip_all_tags($this->network_status_html($adcell)); ?><br>
                    <strong>Zuletzt accepted + aktiv:</strong> <?php echo absint(count($adcell_catalog)); ?><br>
                    <strong>Explizit freigegebene programIds:</strong> <?php echo $adcell_allowlist ? esc_html(implode(', ', $adcell_allowlist)) : 'keine – vollständig gesperrt'; ?><br>
                    <strong>Normalbetrieb:</strong> API v2 → CSV/Banner/Deeplink; keine manuelle CSV-URL.</p>
                    <form method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>" style="display:inline-block;margin-right:8px">
                        <input type="hidden" name="action" value="ppar_run_network_sync"><input type="hidden" name="network" value="adcell"><input type="hidden" name="operation" value="connection"><?php wp_nonce_field('ppar_run_network_sync','ppar_sync_nonce'); ?>
                        <button class="button button-primary">Token + Programme prüfen</button>
                    </form>
                    <p class="description">Die Prüfung erzeugt einen kurzlebigen ADCELL-Token und liest <code>/affiliate/program/export</code> read-only.</p>
                    <form method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>" style="margin-top:14px">
                        <input type="hidden" name="action" value="ppar_run_network_sync"><input type="hidden" name="network" value="adcell"><input type="hidden" name="operation" value="allowlist"><?php wp_nonce_field('ppar_run_network_sync','ppar_sync_nonce'); ?>
                        <label><strong>programId-Allowlist</strong><br><input type="text" class="regular-text" name="program_ids" value="<?php echo esc_attr(implode(', ', $adcell_allowlist)); ?>" placeholder="z. B. 123, 456"></label>
                        <p class="description">Nur diese IDs dürfen laufen – und auch nur solange ADCELL sie aktuell als <code>accepted</code> und <code>isActive=1</code> meldet. Leer = alles gesperrt.</p>
                        <button class="button">Allowlist speichern</button>
                    </form>
                    <?php if ($adcell_catalog) : ?><details style="margin-top:12px"><summary>Zuletzt bestätigte accepted+aktive Programme</summary><ul><?php foreach ($adcell_catalog as $programme) : ?><li><code><?php echo absint($programme['id'] ?? 0); ?></code> · <?php echo esc_html((string) ($programme['name'] ?? '')); ?></li><?php endforeach; ?></ul></details><?php endif; ?>
                    <p><a class="button" href="<?php echo esc_url(admin_url('admin.php?page=affiliate-portal-automation&provider=adcell')); ?>">ADCELL-Automatisierung öffnen</a></p>
                </section>
                <?php $ebay_snapshot=$this->provider_access_snapshot('ebay'); ?>
                <section class="postbox" style="padding:18px"><h2>eBay</h2><p><strong>Zugang:</strong> <?php echo $this->provider_status_badge($ebay_snapshot); ?><br><strong>Datenpfad:</strong> Browse API / provider-spezifischer Lauf<br><strong>Routen:</strong> BUSINESS → Creative-Bibliothek; INDIVIDUAL → isolierte HivePress-Struktur.</p><p><a class="button button-primary" href="<?php echo esc_url(admin_url('admin.php?page=affiliate-portal-ebay')); ?>">eBay-Fachseite öffnen</a> <a class="button" href="<?php echo esc_url(admin_url('admin.php?page=affiliate-portal-automation&provider=ebay')); ?>">Automatisierung</a></p></section>
                <?php foreach($this->provider_registry() as $provider_key=>$provider_def): if(in_array($provider_key,array('awin','adcell','ebay','manual','direct'),true) || !$this->provider_supports($provider_key,'synchronization')){continue;} $provider_snapshot=$this->provider_access_snapshot($provider_key); ?>
                <section class="postbox" style="padding:18px"><h2><?php echo esc_html((string)$provider_def['label']); ?></h2><p><?php echo $this->provider_status_badge($provider_snapshot); ?><br>Synchronisationslogik wird vom Provideradapter geliefert.</p><?php do_action('ppar_affiliate_render_provider_sync_' . $provider_key, $provider_key, $provider_def, self::PROVIDER_CONTRACT_VERSION); ?></section>
                <?php endforeach; ?>
            </div>
            <div class="notice notice-warning inline" style="margin:18px 0"><p><strong>Fail-closed:</strong> Es wird für keinen Provider ein nicht dokumentierter Creative-/Produktendpunkt geraten. Öffentliche Ausgabe bleibt bis zur zentralen Sicherheits- und Chefsteuerung gesperrt.</p></div>
            <h2>Letzte Synchronisationsläufe</h2>
            <table class="widefat striped" style="max-width:1200px"><thead><tr><th>Zeit</th><th>Provider</th><th>Aktion</th><th>Status</th><th>Gesehen</th><th>Neu</th><th>Aktualisiert</th><th>Übersprungen</th><th>Fehler</th><th>Meldung</th></tr></thead><tbody>
            <?php if (!$runs) : ?><tr><td colspan="10">Noch kein Synchronisationslauf.</td></tr><?php else : foreach ($runs as $run) : ?>
                <tr><td><?php echo esc_html(wp_date('d.m.Y H:i', absint($run['finished_at']))); ?></td><td><?php echo esc_html($this->provider_label((string)$run['network'])); ?></td><td><?php echo esc_html($run['operation']); ?></td><td><?php echo esc_html($run['status']); ?></td><td><?php echo absint($run['items_seen']); ?></td><td><?php echo absint($run['items_imported']); ?></td><td><?php echo absint($run['items_updated']); ?></td><td><?php echo absint($run['items_skipped']); ?></td><td><?php echo absint($run['items_failed']); ?></td><td><?php echo esc_html($run['message']); ?></td></tr>
            <?php endforeach; endif; ?>
            </tbody></table>
            <p style="max-width:1100px"><strong>Prüfstatus:</strong> PASS/WARN in dieser Staging-Tabelle ist nur technische Datenqualität. Fachliche Freigabe, Zielwahl, Slotwahl und öffentliche Ausgabe folgen danach dem zentralen Steuervertrag.</p>
        </div>
        <?php
    }
}
