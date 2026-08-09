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
            if (count($rows) >= $row_limit) {
                break;
            }
            if (!array_filter($values, static function ($value) { return trim((string) $value) !== ''; })) {
                continue;
            }
            $row = array();
            foreach ($headers as $index => $header) {
                if ($header === '') {
                    continue;
                }
                $row[$header] = isset($values[$index]) ? trim((string) $values[$index]) : '';
            }
            if ($row) {
                $rows[] = $row;
            }
        }
        fclose($stream);
        if (!$rows) {
            return new WP_Error('empty_csv_rows', 'Die Exportdatei enthält keine auswertbaren Produktzeilen.');
        }
        return array('headers' => $headers, 'mapping' => $mapping, 'delimiter' => $delimiter, 'rows' => $rows);
    }

    private function network_sync_mapped_value($row, $mapping, $field) {
        if (empty($mapping[$field]['source'])) {
            return '';
        }
        $source = (string) $mapping[$field]['source'];
        return isset($row[$source]) ? trim((string) $row[$source]) : '';
    }

    private function network_sync_quality_status($title, $tracking_url, $destination_url, $image_url) {
        if ($title === '' || ($tracking_url === '' && $destination_url === '')) {
            return 'fail';
        }
        if ($image_url === '') {
            return 'warn';
        }
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
            if (!is_array($programme)) {
                $counts['skipped']++;
                continue;
            }
            $external_id = trim((string) ($programme['id'] ?? $programme['external_id'] ?? ''));
            $name = trim((string) ($programme['name'] ?? ''));
            if ($external_id === '' || $name === '') {
                $counts['failed']++;
                continue;
            }
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
            if ($quality === 'fail') {
                $counts['failed']++;
                continue;
            }
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
        $settings = $this->network_settings($network);
        $url = $network === 'awin' ? (string) ($settings['product_feed_url'] ?? '') : (string) ($settings['csv_feed_url'] ?? '');
        $validated = $this->network_sync_validate_feed_url($network, $url);
        if (is_wp_error($validated)) {
            return $validated;
        }
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
        if (is_wp_error($parsed)) {
            return $parsed;
        }
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
        }
        update_option($option, $settings, false);
    }

    public function handle_run_network_sync() {
        if (!current_user_can('manage_options')) {
            wp_die('Keine Berechtigung.');
        }
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

        if (in_array($network, array('awin','adcell'), true) && $operation === 'connection') {
            $result = $network === 'awin' ? $this->test_awin_connection() : $this->test_adcell_connection();
            $this->network_sync_update_connection_status($network, $result);
            $status = ($result['status'] ?? '') === 'connected' ? 'success' : 'failed';
            $message = (string) ($result['message'] ?? 'Verbindungsprüfung beendet.');
            if ($network === 'awin' && $status === 'success') {
                $programmes = get_option(self::OPTION_NETWORK_AWIN_PROGRAMMES, array());
                $counts = $this->network_sync_upsert_programmes('awin', is_array($programmes) ? $programmes : array(), 'Awin Publisher API');
            }
        } elseif (in_array($network, array('awin','adcell'), true) && $operation === 'products') {
            $result = $this->network_sync_download_and_stage_products($network);
            if (is_wp_error($result)) {
                $message = $result->get_error_message();
            } else {
                $status = 'success';
                $counts = $result['counts'];
                $details = array(
                    'source_headers' => $result['headers'],
                    'detected_mapping' => $result['mapping'],
                    'delimiter' => $result['delimiter'] === "	" ? 'TAB' : $result['delimiter'],
                    'public_activation' => false,
                );
                $message = 'Produktdaten wurden ausschließlich in die interne Prüfstufe eingelesen. Es wurde nichts veröffentlicht.';
            }
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
        if (!current_user_can('manage_options')) {
            return;
        }
        $this->maybe_install_network_sync_schema();
        $awin = $this->network_settings('awin');
        $adcell = $this->network_settings('adcell');
        $awin_counts = $this->network_sync_counts('awin');
        $adcell_counts = $this->network_sync_counts('adcell');
        $runs = $this->network_sync_recent_runs();
        ?>
        <div class="wrap ppar-sync-page">
            <h1>Provider-Synchronisierung</h1>
            <p>Provider verwenden ihren registrierten Datenpfad. Awin/ADCELL nutzen zusätzlich die zentrale API-/CSV-Prüfstufe; eBay seinen eigenen Providerlauf. <strong>Keine synchronisierte Zeile wird automatisch öffentlich freigegeben.</strong></p>
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
                    <h2>ADCELL</h2>
                    <p><strong>Verbindung:</strong> <?php echo wp_strip_all_tags($this->network_status_html($adcell)); ?><br>
                    <strong>Produkte in Prüfstufe:</strong> <?php echo absint($adcell_counts['products']); ?> (PASS <?php echo absint($adcell_counts['pass']); ?> / WARN <?php echo absint($adcell_counts['warn']); ?>)<br>
                    <strong>ADCELL-CSV-Export-URL:</strong> <?php echo !empty($adcell['csv_feed_url']) ? 'gespeichert' : 'fehlt'; ?></p>
                    <form method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>" style="display:inline-block;margin-right:8px">
                        <input type="hidden" name="action" value="ppar_run_network_sync"><input type="hidden" name="network" value="adcell"><input type="hidden" name="operation" value="connection"><?php wp_nonce_field('ppar_run_network_sync','ppar_sync_nonce'); ?>
                        <button class="button button-primary">API-Verbindung prüfen</button>
                    </form>
                    <form method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>" style="display:inline-block">
                        <input type="hidden" name="action" value="ppar_run_network_sync"><input type="hidden" name="network" value="adcell"><input type="hidden" name="operation" value="products"><?php wp_nonce_field('ppar_run_network_sync','ppar_sync_nonce'); ?>
                        <button class="button" <?php disabled(empty($adcell['csv_feed_url'])); ?>>Produktfeed einlesen</button>
                    </form>
                </section>
                <?php $ebay_snapshot=$this->provider_access_snapshot('ebay'); ?>
                <section class="postbox" style="padding:18px"><h2>eBay</h2><p><strong>Zugang:</strong> <?php echo $this->provider_status_badge($ebay_snapshot); ?><br><strong>Datenpfad:</strong> Browse API / provider-spezifischer Lauf<br><strong>Routen:</strong> BUSINESS → Creative-Bibliothek; INDIVIDUAL → isolierte HivePress-Struktur.</p><p><a class="button button-primary" href="<?php echo esc_url(admin_url('admin.php?page=affiliate-portal-ebay')); ?>">eBay-Fachseite öffnen</a> <a class="button" href="<?php echo esc_url(admin_url('admin.php?page=affiliate-portal-automation&provider=ebay')); ?>">Automatisierung</a></p></section>
                <?php foreach($this->provider_registry() as $provider_key=>$provider_def): if(in_array($provider_key,array('awin','adcell','ebay','manual','direct'),true) || !$this->provider_supports($provider_key,'synchronization')){continue;} $provider_snapshot=$this->provider_access_snapshot($provider_key); ?>
                <section class="postbox" style="padding:18px"><h2><?php echo esc_html((string)$provider_def['label']); ?></h2><p><?php echo $this->provider_status_badge($provider_snapshot); ?><br>Synchronisationslogik wird vom Provideradapter geliefert.</p><?php do_action('ppar_affiliate_render_provider_sync_' . $provider_key, $provider_key, $provider_def, self::PROVIDER_CONTRACT_VERSION); ?></section>
                <?php endforeach; ?>
            </div>
            <div class="notice notice-warning inline" style="margin:18px 0"><p><strong>Fail-closed:</strong> Es wird für keinen Provider ein nicht dokumentierter Creative-/Produktendpunkt geraten. Ein Provideradapter darf Daten nur über dokumentierte und real konfigurierte Quellen einlesen; öffentliche Ausgabe bleibt bis zur zentralen Sicherheits- und Chefsteuerung gesperrt.</p></div>
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

