<?php
if (!defined('ABSPATH')) {
    exit;
}

/**
 * Providerunabhängige lokale Werbemittelbibliothek.
 *
 * V4.0.0:
 * - akzeptiert ausschließlich reale, vom Provider gelieferte Werbemittel,
 * - importiert CSV, JSON oder gesammelt eingefügte vollständige Banner-Codes,
 * - führt beim Import bewusst keinen Remoteabruf aus,
 * - prüft Bilddatei, echte Pixelmaße und Inhalts-Hash anschließend paketweise,
 * - behandelt Providermaße nur als unverifizierte Vergleichsdaten,
 * - übergibt bestätigte Creatives ausschließlich an das zentrale Ausgabeobjekt,
 * - veröffentlicht nichts automatisch.
 */
trait PPAR_Creative_Library_Trait {
    private function creative_library_table() {
        global $wpdb;
        return $wpdb->prefix . 'ppar_creative_library';
    }

    public function maybe_install_creative_library_schema() {
        $installed = (string) get_option(self::OPTION_CREATIVE_LIBRARY_SCHEMA_VERSION, '0');
        if ($installed === self::CREATIVE_LIBRARY_SCHEMA_VERSION) {
            return;
        }
        require_once ABSPATH . 'wp-admin/includes/upgrade.php';
        global $wpdb;
        $table = $this->creative_library_table();
        $charset = $wpdb->get_charset_collate();
        dbDelta("CREATE TABLE {$table} (
            id bigint(20) unsigned NOT NULL AUTO_INCREMENT,
            provider varchar(60) NOT NULL,
            partner_external_id varchar(191) NOT NULL DEFAULT '',
            partner_name text NOT NULL,
            external_id varchar(191) NOT NULL,
            identity_hash char(64) NOT NULL,
            creative_type varchar(30) NOT NULL DEFAULT 'banner',
            title text NOT NULL,
            description longtext NULL,
            tags text NOT NULL,
            image_url text NOT NULL,
            destination_url text NOT NULL,
            tracking_url text NOT NULL,
            width int(10) unsigned NOT NULL DEFAULT 0,
            height int(10) unsigned NOT NULL DEFAULT 0,
            source_status varchar(30) NOT NULL DEFAULT 'active',
            source_kind varchar(30) NOT NULL DEFAULT 'banner',
            availability_state varchar(30) NOT NULL DEFAULT 'active',
            missing_count int(10) unsigned NOT NULL DEFAULT 0,
            last_complete_run char(36) NOT NULL DEFAULT '',
            review_status varchar(30) NOT NULL DEFAULT 'review',
            selected tinyint(1) unsigned NOT NULL DEFAULT 0,
            content_scope varchar(30) NOT NULL DEFAULT 'unclassified',
            scope_source varchar(30) NOT NULL DEFAULT '',
            classified_at bigint(20) unsigned NOT NULL DEFAULT 0,
            topic_status varchar(30) NOT NULL DEFAULT 'no_match',
            topic_score int(10) unsigned NOT NULL DEFAULT 0,
            topic_targets longtext NULL,
            source_hash char(64) NOT NULL,
            payload longtext NULL,
            first_seen bigint(20) unsigned NOT NULL DEFAULT 0,
            last_seen bigint(20) unsigned NOT NULL DEFAULT 0,
            PRIMARY KEY  (id),
            UNIQUE KEY identity_hash (identity_hash),
            KEY provider_partner (provider(20), partner_external_id(100)),
            KEY provider_source (provider(20), partner_external_id(100), source_kind, availability_state),
            KEY review_selected (review_status, selected),
            KEY content_scope (content_scope, partner_external_id(100)),
            KEY topic_status (topic_status, topic_score)
        ) {$charset};");
        $this->creative_library_mark_assets_for_reverification($installed);
        update_option(self::OPTION_CREATIVE_LIBRARY_SCHEMA_VERSION, self::CREATIVE_LIBRARY_SCHEMA_VERSION, false);
        $this->creative_library_schedule_asset_verification(10);
    }

    /**
     * V3.0-Schemamigration: alte Maße stammen möglicherweise nur aus Provider-
     * Angaben. Sie werden deshalb niemals als verifiziert übernommen. Manuelle
     * Vetos bleiben erhalten; alle übrigen Bild-Creatives gehen in die kleine,
     * wiederaufnehmbare Prüfwarteschlange.
     */
    private function creative_library_mark_assets_for_reverification($previous_version) {
        if ((string) $previous_version === self::CREATIVE_LIBRARY_SCHEMA_VERSION) {
            return;
        }
        global $wpdb;
        $table = $this->creative_library_table();
        $rows = $wpdb->get_results("SELECT id, payload, review_status, content_scope FROM {$table} WHERE creative_type IN ('banner','product') AND image_url<>''", ARRAY_A);
        foreach ((array) $rows as $row) {
            $payload = json_decode((string) ($row['payload'] ?? ''), true);
            $payload = is_array($payload) ? $payload : array();
            if (!isset($payload['_declared_width'])) {
                $payload['_declared_width'] = 0;
            }
            if (!isset($payload['_declared_height'])) {
                $payload['_declared_height'] = 0;
            }
            $payload['_dimension_state'] = 'pending';
            $payload['_dimension_error'] = '';
            $payload['_image_sha256'] = '';
            $payload['_image_mime'] = '';
            $payload['_image_bytes'] = 0;
            $payload['_measured_at'] = 0;
            $veto = (string) ($row['review_status'] ?? '') === 'rejected' || (string) ($row['content_scope'] ?? '') === 'other';
            $wpdb->update($table, array(
                'width'=>0,
                'height'=>0,
                'topic_status'=>$veto ? 'blocked' : 'format_pending',
                'topic_score'=>0,
                'payload'=>wp_json_encode($payload, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES),
            ), array('id'=>absint($row['id'])));
        }
    }

    private function creative_library_schedule_asset_verification($delay = 10) {
        if (!function_exists('wp_next_scheduled') || !function_exists('wp_schedule_single_event')) {
            return false;
        }
        if (!wp_next_scheduled(self::ASSET_VERIFY_HOOK)) {
            return (bool) wp_schedule_single_event(time() + max(1, absint($delay)), self::ASSET_VERIFY_HOOK);
        }
        return true;
    }


    public function maybe_cleanup_false_partner_creatives() {
        if (!current_user_can('manage_options')) {
            return;
        }
        $target = '3.0.0';
        if ((string) get_option(self::OPTION_FALSE_CREATIVE_CLEANUP_VERSION, '') === $target) {
            return;
        }
        $this->maybe_install_creative_library_schema();
        global $wpdb;
        $table = $this->creative_library_table();
        $wpdb->query("DELETE FROM {$table} WHERE creative_type='native_partner' OR external_id LIKE 'native-%' OR payload LIKE '%\"native_partner\":1%'");
        delete_option('ppar_native_creative_seed_version');
        update_option(self::OPTION_FALSE_CREATIVE_CLEANUP_VERSION, $target, false);
    }

    private function creative_library_allowed_upload_extensions() {
        return array('csv', 'json', 'txt');
    }

    private function creative_library_normalize_key($value) {
        $value = remove_accents(strtolower(trim((string) $value)));
        $value = preg_replace('/[^a-z0-9]+/', '_', $value);
        return trim((string) $value, '_');
    }

    private function creative_library_aliases() {
        return array(
            'external_id' => array('id','creative_id','creativeid','link_id','linkid','banner_id','bannerid','external_id'),
            'creative_type' => array('creative_type','type','werbemittel_typ','asset_type'),
            'title' => array('creative_title','title','name','werbemittel_titel','banner_name'),
            'description' => array('creative_description','description','beschreibung'),
            'tags' => array('creative_tag','tag','tags','category','kategorie'),
            'image_url' => array('image_source','image_url','image','bildquelle','bild_url','banner_url'),
            'destination_url' => array('destination_url','destination','target_url','landing_page','ziel_url'),
            'tracking_url' => array('tracking_url','affiliate_url','click_url','deeplink','deep_link','trackinglink','url_tracking'),
            'width' => array('width','breite','creative_width','banner_width'),
            'height' => array('height','hoehe','höhe','creative_height','banner_height'),
            'dimensions' => array('dimensions','dimension','size','format','groesse','größe'),
            'status' => array('status','creative_status','active'),
            'alt_text' => array('alt_text','alt','alternative_text'),
            'html' => array('html','code','creative_code','banner_code'),
        );
    }

    private function creative_library_detect_mapping($headers) {
        $normalized = array();
        foreach ((array) $headers as $header) {
            $key = $this->creative_library_normalize_key($header);
            if ($key !== '') {
                $normalized[$key] = (string) $header;
            }
        }
        $mapping = array();
        foreach ($this->creative_library_aliases() as $target => $aliases) {
            foreach ($aliases as $alias) {
                $alias = $this->creative_library_normalize_key($alias);
                if (isset($normalized[$alias])) {
                    $mapping[$target] = $normalized[$alias];
                    break;
                }
            }
        }
        return $mapping;
    }

    private function creative_library_mapped_value($row, $mapping, $field) {
        if (!is_array($row) || empty($mapping[$field])) {
            return '';
        }
        $source = $mapping[$field];
        return isset($row[$source]) && is_scalar($row[$source]) ? trim((string) $row[$source]) : '';
    }

    private function creative_library_detect_delimiter($line) {
        $best = ',';
        $best_count = -1;
        foreach (array(',', ';', "\t", '|') as $candidate) {
            $count = substr_count((string) $line, $candidate);
            if ($count > $best_count) {
                $best = $candidate;
                $best_count = $count;
            }
        }
        return $best;
    }

    private function creative_library_parse_csv($body, $limit = 5000) {
        $body = preg_replace('/^\xEF\xBB\xBF/', '', (string) $body);
        if (trim($body) === '') {
            return new WP_Error('creative_import_empty', 'Die Datei ist leer.');
        }
        $parts = preg_split('/\r\n|\r|\n/', $body, 2);
        $delimiter = $this->creative_library_detect_delimiter(isset($parts[0]) ? $parts[0] : '');
        $stream = fopen('php://temp', 'r+');
        if (!$stream) {
            return new WP_Error('creative_import_stream', 'Die Datei konnte nicht verarbeitet werden.');
        }
        fwrite($stream, $body);
        rewind($stream);
        $headers = fgetcsv($stream, 0, $delimiter, '"', '\\');
        if (!is_array($headers) || count(array_filter($headers, 'strlen')) < 2) {
            fclose($stream);
            return new WP_Error('creative_import_headers', 'Keine brauchbare CSV-Kopfzeile erkannt.');
        }
        $headers = array_map('trim', $headers);
        $mapping = $this->creative_library_detect_mapping($headers);
        $rows = array();
        while (($values = fgetcsv($stream, 0, $delimiter, '"', '\\')) !== false) {
            if (count($rows) >= $limit) {
                break;
            }
            if (!array_filter($values, static function ($value) { return trim((string) $value) !== ''; })) {
                continue;
            }
            $row = array();
            foreach ($headers as $index => $header) {
                if ($header !== '') {
                    $row[$header] = isset($values[$index]) ? trim((string) $values[$index]) : '';
                }
            }
            if ($row) {
                $rows[] = $row;
            }
        }
        fclose($stream);
        if (!$rows) {
            return new WP_Error('creative_import_rows', 'Keine Werbemittelzeilen erkannt.');
        }
        return array('rows' => $rows, 'mapping' => $mapping, 'format' => 'csv');
    }

    private function creative_library_is_list($value) {
        if (!is_array($value)) {
            return false;
        }
        $expected = 0;
        foreach (array_keys($value) as $key) {
            if ($key !== $expected) {
                return false;
            }
            $expected++;
        }
        return true;
    }

    private function creative_library_parse_json($body, $limit = 5000) {
        $decoded = json_decode((string) $body, true);
        if (!is_array($decoded)) {
            return new WP_Error('creative_import_json', 'Keine gültige JSON-Datei erkannt.');
        }
        $rows = array();
        if ($this->creative_library_is_list($decoded)) {
            $rows = $decoded;
        } else {
            foreach (array('creatives','items','data','results','banners') as $key) {
                if (isset($decoded[$key]) && is_array($decoded[$key]) && $this->creative_library_is_list($decoded[$key])) {
                    $rows = $decoded[$key];
                    break;
                }
            }
            if (!$rows) {
                $rows = array($decoded);
            }
        }
        $rows = array_slice(array_values(array_filter($rows, 'is_array')), 0, $limit);
        if (!$rows) {
            return new WP_Error('creative_import_rows', 'Keine Werbemittelobjekte erkannt.');
        }
        $headers = array();
        foreach ($rows as $row) {
            foreach (array_keys($row) as $key) {
                if (is_scalar($key)) {
                    $headers[(string) $key] = (string) $key;
                }
            }
        }
        return array('rows' => $rows, 'mapping' => $this->creative_library_detect_mapping(array_values($headers)), 'format' => 'json');
    }

    private function creative_library_html_attr($html, $tag, $attribute) {
        $pattern = '/<' . preg_quote($tag, '/') . '\b[^>]*\b' . preg_quote($attribute, '/') . '\s*=\s*(["\'])(.*?)\1/is';
        if (preg_match($pattern, (string) $html, $match)) {
            return html_entity_decode(trim((string) $match[2]), ENT_QUOTES, 'UTF-8');
        }
        $pattern = '/<' . preg_quote($tag, '/') . '\b[^>]*\b' . preg_quote($attribute, '/') . '\s*=\s*([^\s>]+)/is';
        return preg_match($pattern, (string) $html, $match) ? html_entity_decode(trim((string) $match[1], " \t\n\r\0\x0B\"'"), ENT_QUOTES, 'UTF-8') : '';
    }

    private function creative_library_parse_html_codes($body, $limit = 5000) {
        $body = trim((string) $body);
        if ($body === '') {
            return new WP_Error('creative_import_empty', 'Kein Banner-Code eingefügt.');
        }
        preg_match_all('/<a\b[^>]*>.*?<\/a>/is', $body, $matches);
        $chunks = !empty($matches[0]) ? $matches[0] : preg_split('/\n\s*\n/', $body);
        $rows = array();
        foreach ((array) $chunks as $index => $chunk) {
            if (count($rows) >= $limit || stripos((string) $chunk, '<img') === false) {
                continue;
            }
            $image = $this->creative_library_html_attr($chunk, 'img', 'src');
            $href = $this->creative_library_html_attr($chunk, 'a', 'href');
            if ($image === '' || $href === '') {
                continue;
            }
            $rows[] = array(
                'creative_id' => $this->creative_library_html_attr($chunk, 'a', 'data-id'),
                'creative_title' => $this->creative_library_html_attr($chunk, 'img', 'title'),
                'creative_description' => '',
                'creative_tag' => '',
                'image_source' => $image,
                'destination_url' => '',
                'tracking_url' => $href,
                'width' => $this->creative_library_html_attr($chunk, 'img', 'width'),
                'height' => $this->creative_library_html_attr($chunk, 'img', 'height'),
                'alt_text' => $this->creative_library_html_attr($chunk, 'img', 'alt'),
                'html' => $chunk,
                '_row_index' => $index + 1,
            );
        }
        if (!$rows) {
            return new WP_Error('creative_import_html', 'Kein vollständiger Bildbanner-Code erkannt.');
        }
        return array('rows' => $rows, 'mapping' => $this->creative_library_detect_mapping(array_keys($rows[0])), 'format' => 'html');
    }

    /**
     * Liest reale Bildmaße und einen Inhalts-Hash. Die Remote-Datei ist immer
     * die maßgebliche Quelle. Providerangaben werden nur dokumentiert, niemals
     * stillschweigend als verifiziert behandelt.
     */
    private function creative_library_remote_image_evidence($image_url, $force = false) {
        $image_url = esc_url_raw((string) $image_url);
        if ($image_url === '' || !wp_http_validate_url($image_url) || strtolower((string) wp_parse_url($image_url, PHP_URL_SCHEME)) !== 'https') {
            return new WP_Error('creative_dimension_url', 'Die Bild-URL ist nicht eindeutig als HTTPS-Bildquelle prüfbar.');
        }
        $cache_key = 'ppar_img_' . substr(hash('sha256', $image_url), 0, 40);
        $cached = $force ? false : get_transient($cache_key);
        if (is_array($cached) && !empty($cached['width']) && !empty($cached['height']) && !empty($cached['sha256'])) {
            $cached['cache'] = 'hit';
            return $cached;
        }
        $response = wp_safe_remote_get($image_url, array(
            'timeout' => 12,
            'redirection' => 3,
            'headers' => array('Accept'=>'image/*'),
            'limit_response_size' => 2097152,
        ));
        if (is_wp_error($response)) {
            return $response;
        }
        $code = absint(wp_remote_retrieve_response_code($response));
        $body = (string) wp_remote_retrieve_body($response);
        if ($code < 200 || $code >= 300 || $body === '') {
            return new WP_Error('creative_dimension_response', 'Das Bannerbild konnte nicht vollständig geladen werden.');
        }
        $content_type = strtolower((string) wp_remote_retrieve_header($response, 'content-type'));
        $width = 0;
        $height = 0;
        $size = function_exists('getimagesizefromstring') ? @getimagesizefromstring($body) : false;
        if (is_array($size)) {
            $width = absint($size[0] ?? 0);
            $height = absint($size[1] ?? 0);
        } elseif ((strpos($content_type, 'image/svg') !== false || stripos(ltrim($body), '<svg') === 0) && preg_match('/<svg\b[^>]*>/i', $body, $svg_tag)) {
            $width = absint($this->creative_library_html_attr($svg_tag[0], 'svg', 'width'));
            $height = absint($this->creative_library_html_attr($svg_tag[0], 'svg', 'height'));
            if ((!$width || !$height) && preg_match('/\bviewBox\s*=\s*["\']\s*[-0-9.]+\s+[-0-9.]+\s+([0-9.]+)\s+([0-9.]+)\s*["\']/i', $svg_tag[0], $viewbox)) {
                $width = $width ?: absint(round((float) $viewbox[1]));
                $height = $height ?: absint(round((float) $viewbox[2]));
            }
        }
        if ($width <= 0 || $height <= 0 || $width > 10000 || $height > 10000) {
            return new WP_Error('creative_dimension_unknown', 'Die echten Bildmaße konnten nicht sicher bestimmt werden.');
        }
        $evidence = array(
            'width'=>$width,
            'height'=>$height,
            'sha256'=>hash('sha256', $body),
            'mime'=>$content_type,
            'bytes'=>strlen($body),
            'measured_at'=>time(),
            'cache'=>'miss',
        );
        set_transient($cache_key, $evidence, DAY_IN_SECONDS);
        return $evidence;
    }

    private function creative_library_remote_image_dimensions($image_url) {
        $evidence = $this->creative_library_remote_image_evidence($image_url);
        if (is_wp_error($evidence)) {
            return $evidence;
        }
        return array(absint($evidence['width']), absint($evidence['height']));
    }

    private function creative_library_verify_asset_row($row, $force = false, $replan = true) {
        if (!is_array($row) || empty($row['id'])) {
            return new WP_Error('creative_asset_missing', 'Werbemittel wurde nicht gefunden.');
        }
        $image_url = esc_url_raw((string) ($row['image_url'] ?? ''));
        if ($image_url === '') {
            return new WP_Error('creative_asset_image_missing', 'Bildquelle fehlt.');
        }
        $evidence = $this->creative_library_remote_image_evidence($image_url, (bool) $force);
        $payload = json_decode((string) ($row['payload'] ?? ''), true);
        $payload = is_array($payload) ? $payload : array();
        global $wpdb;
        $table = $this->creative_library_table();
        if (is_wp_error($evidence)) {
            $payload['_dimension_state'] = 'failed';
            $payload['_dimension_error'] = $evidence->get_error_message();
            $payload['_measured_at'] = time();
            $wpdb->update($table, array(
                'width'=>0,
                'height'=>0,
                'topic_status'=>'format_blocked',
                'topic_score'=>0,
                'payload'=>wp_json_encode($payload, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES),
            ), array('id'=>absint($row['id'])));
            return $evidence;
        }
        $width = absint($evidence['width'] ?? 0);
        $height = absint($evidence['height'] ?? 0);
        $declared_width = absint($payload['_declared_width'] ?? 0);
        $declared_height = absint($payload['_declared_height'] ?? 0);
        $state = ($declared_width > 0 && $declared_height > 0 && ($declared_width !== $width || $declared_height !== $height)) ? 'mismatch' : 'verified';
        $payload['_dimension_state'] = $state;
        $payload['_dimension_error'] = '';
        $payload['_image_sha256'] = sanitize_text_field((string) ($evidence['sha256'] ?? ''));
        $payload['_image_mime'] = sanitize_text_field((string) ($evidence['mime'] ?? ''));
        $payload['_image_bytes'] = absint($evidence['bytes'] ?? 0);
        $payload['_measured_at'] = absint($evidence['measured_at'] ?? time());
        // Der Bildprüfer bestätigt ausschließlich das Asset. Portal- und Zielstatus
        // bleiben im zentralen Ausgabeobjekt-Modell und werden nicht global zurückgeschrieben.
        $topic_status = 'auto_verified';
        $topic_score = 0;
        $topic_targets = '[]';
        $wpdb->update($table, array(
            'width'=>$width,
            'height'=>$height,
            'topic_status'=>$topic_status,
            'topic_score'=>$topic_score,
            'topic_targets'=>$topic_targets,
            'payload'=>wp_json_encode($payload, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES),
        ), array('id'=>absint($row['id'])));
        $updated = array_merge($row, array(
            'width'=>$width,
            'height'=>$height,
            'topic_status'=>$topic_status,
            'topic_score'=>$topic_score,
            'topic_targets'=>$topic_targets,
            'payload'=>wp_json_encode($payload, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES),
        ));
        if ($replan && method_exists($this, 'output_plan_creative')) {
            $this->output_plan_creative($updated, true);
        }
        return $updated;
    }

    /**
     * Kleine, wiederaufnehmbare Prüfeinheit: höchstens fünf Bilder pro Lauf,
     * keine blockierende Wartefunktion und kein Partner-Monsterlauf. Der nächste Lauf wird nur geplant,
     * wenn noch tatsächlich ungeprüfte Assets vorhanden sind.
     */
    public function run_creative_asset_verification_batch() {
        $this->maybe_install_creative_library_schema();
        global $wpdb;
        $table = $this->creative_library_table();
        $rows = $wpdb->get_results("SELECT * FROM {$table} WHERE creative_type IN ('banner','product') AND image_url<>'' AND source_status='active' AND availability_state='active' AND (width=0 OR height=0 OR payload LIKE '%\"_dimension_state\":\"pending\"%') ORDER BY id ASC LIMIT 5", ARRAY_A);
        foreach ((array) $rows as $row) {
            $this->creative_library_verify_asset_row($row, false, true);
        }
        $remaining = absint($wpdb->get_var("SELECT COUNT(*) FROM {$table} WHERE creative_type IN ('banner','product') AND image_url<>'' AND source_status='active' AND availability_state='active' AND (width=0 OR height=0 OR payload LIKE '%\"_dimension_state\":\"pending\"%')"));
        if ($remaining > 0) {
            $this->creative_library_schedule_asset_verification(20);
        }
        return array('processed'=>count((array) $rows), 'remaining'=>$remaining);
    }

    private function creative_library_declared_dimensions($width, $height, $dimensions, $html = '') {
        $width = absint($width);
        $height = absint($height);
        if ((!$width || !$height) && preg_match('/(\d{2,5})\s*[x×]\s*(\d{2,5})/i', (string) $dimensions, $match)) {
            $width = $width ?: absint($match[1]);
            $height = $height ?: absint($match[2]);
        }
        if ((!$width || !$height) && $html !== '') {
            $width = $width ?: absint($this->creative_library_html_attr($html, 'img', 'width'));
            $height = $height ?: absint($this->creative_library_html_attr($html, 'img', 'height'));
        }
        if ($width > 10000 || $height > 10000) {
            return array(0, 0);
        }
        return array($width, $height);
    }

    private function creative_library_parse_dimensions($width, $height, $dimensions, $html = '', $image_url = '') {
        // Import bleibt skalierbar: deklarierte Maße werden nur dokumentiert.
        // Verifizierte Maße kommen ausschließlich aus der separaten Assetprüfung.
        return array(0, 0);
    }

    private function creative_library_normalize_type($value) {
        $value = $this->creative_library_normalize_key($value);
        if (in_array($value, array('5','text','text_link','textlink'), true)) {
            return 'text';
        }
        if (in_array($value, array('html','html5','html_5','iframe','widget'), true)) {
            return 'html';
        }
        if (in_array($value, array('product','produkt','item','product_link'), true)) {
            return 'product';
        }
        return 'banner';
    }

    private function creative_library_normalize_status($value) {
        $value = strtolower(trim((string) $value));
        return in_array($value, array('0','inactive','hidden','paused','disabled'), true) ? 'inactive' : 'active';
    }

    private function creative_library_destination_from_tracking($tracking_url) {
        $tracking_url = esc_url_raw((string) $tracking_url);
        if ($tracking_url === '') {
            return '';
        }
        $query = (string) wp_parse_url($tracking_url, PHP_URL_QUERY);
        if ($query === '') {
            return '';
        }
        parse_str($query, $params);
        foreach (array('ued','url','destination','destination_url','desturl','redirect','redirect_url','target') as $key) {
            if (!isset($params[$key]) || !is_scalar($params[$key])) {
                continue;
            }
            $candidate = (string) $params[$key];
            for ($i = 0; $i < 3; $i++) {
                $decoded = rawurldecode(html_entity_decode($candidate, ENT_QUOTES, 'UTF-8'));
                if ($decoded === $candidate) {
                    break;
                }
                $candidate = $decoded;
            }
            $candidate = esc_url_raw($candidate);
            if ($candidate !== '' && wp_http_validate_url($candidate) && in_array(strtolower((string) wp_parse_url($candidate, PHP_URL_SCHEME)), array('http','https'), true)) {
                return $candidate;
            }
        }
        return '';
    }

    private function creative_library_normalize_row($row, $mapping, $context) {
        $provider = sanitize_key((string) ($context['provider'] ?? ''));
        $partner_external_id = preg_replace('/[^0-9A-Za-z._-]/', '', (string) ($context['partner_external_id'] ?? ''));
        $partner_name = sanitize_text_field((string) ($context['partner_name'] ?? ''));
        if ($provider === '' || $partner_name === '') {
            return new WP_Error('creative_import_partner', 'Provider und Partnername sind erforderlich.');
        }
        $title = sanitize_text_field($this->creative_library_mapped_value($row, $mapping, 'title'));
        $description = sanitize_textarea_field($this->creative_library_mapped_value($row, $mapping, 'description'));
        $tags = sanitize_text_field($this->creative_library_mapped_value($row, $mapping, 'tags'));
        $alt = sanitize_text_field($this->creative_library_mapped_value($row, $mapping, 'alt_text'));
        if ($title === '') {
            $title = $alt !== '' ? $alt : $partner_name . ' Banner';
        }
        $image_url = esc_url_raw($this->creative_library_mapped_value($row, $mapping, 'image_url'));
        $destination_url = esc_url_raw($this->creative_library_mapped_value($row, $mapping, 'destination_url'));
        $tracking_url = esc_url_raw($this->creative_library_mapped_value($row, $mapping, 'tracking_url'));
        $html = (string) $this->creative_library_mapped_value($row, $mapping, 'html');
        if ($image_url === '' && $html !== '') {
            $image_url = esc_url_raw($this->creative_library_html_attr($html, 'img', 'src'));
        }
        if ($tracking_url === '' && $html !== '') {
            $tracking_url = esc_url_raw($this->creative_library_html_attr($html, 'a', 'href'));
        }
        if ($destination_url === '') {
            $destination_url = $this->creative_library_destination_from_tracking($tracking_url);
        }
        if ($destination_url === '') {
            $destination_url = $tracking_url;
        }
        $type = $this->creative_library_normalize_type($this->creative_library_mapped_value($row, $mapping, 'creative_type'));
        if (in_array($type, array('banner','product'), true) && $image_url === '') {
            return new WP_Error('creative_import_image', 'Bildbanner ohne Bild-URL blockiert.');
        }
        if ($tracking_url === '' || !wp_http_validate_url($tracking_url)) {
            return new WP_Error('creative_import_tracking', 'Werbemittel ohne gültigen Trackinglink blockiert.');
        }
        if ($image_url !== '' && !wp_http_validate_url($image_url)) {
            return new WP_Error('creative_import_image', 'Ungültige Bild-URL blockiert.');
        }
        list($declared_width, $declared_height) = $this->creative_library_declared_dimensions(
            $this->creative_library_mapped_value($row, $mapping, 'width'),
            $this->creative_library_mapped_value($row, $mapping, 'height'),
            $this->creative_library_mapped_value($row, $mapping, 'dimensions'),
            $html
        );
        $width = 0;
        $height = 0;
        $dimension_state = 'pending';
        $external_id = sanitize_text_field($this->creative_library_mapped_value($row, $mapping, 'external_id'));
        if ($external_id === '') {
            $external_id = substr(hash('sha256', $provider . '|' . $partner_external_id . '|' . $title . '|' . $image_url . '|' . $tracking_url), 0, 40);
        }
        $external_id = substr(preg_replace('/[^0-9A-Za-z._-]/', '-', $external_id), 0, 191);
        $source_status = $this->creative_library_normalize_status($this->creative_library_mapped_value($row, $mapping, 'status'));
        // Import ist absichtlich portalneutral. Branche, Portalziel und Ausgabeform
        // werden ausschließlich im zentralen Output-Modell je Portal entschieden.
        $payload = array(
            '_declared_width'=>$declared_width,
            '_declared_height'=>$declared_height,
            '_dimension_state'=>$dimension_state,
            '_dimension_error'=>'',
            '_image_sha256'=>'',
            '_image_mime'=>'',
            '_image_bytes'=>0,
            '_measured_at'=>0,
            '_preverify_topic_status'=>'portal_pending',
            '_preverify_topic_score'=>0,
            '_preverify_topic_targets'=>array(),
        );
        foreach ((array) $row as $key => $value) {
            if (strpos((string) $key, '_') === 0) {
                continue;
            }
            if (is_scalar($value)) {
                $payload[sanitize_text_field((string) $key)] = sanitize_text_field((string) $value);
            }
        }
        $normalized = array(
            'provider' => $provider,
            'partner_external_id' => $partner_external_id,
            'partner_name' => $partner_name,
            'external_id' => $external_id,
            'identity_hash' => hash('sha256', $provider . '|' . $partner_external_id . '|' . $external_id),
            'creative_type' => $type,
            'title' => $title,
            'description' => $description,
            'tags' => $tags,
            'image_url' => $image_url,
            'destination_url' => $destination_url,
            'tracking_url' => $tracking_url,
            'width' => $width,
            'height' => $height,
            'source_status' => $source_status,
            'source_kind' => sanitize_key((string) ($context['source_kind'] ?? ($row['_source_kind'] ?? $type))),
            'availability_state' => 'active',
            'missing_count' => 0,
            'last_complete_run' => substr(sanitize_text_field((string) ($context['run_uuid'] ?? ($row['_run_uuid'] ?? ''))), 0, 36),
            'review_status' => 'review',
            'selected' => 0,
            'content_scope' => 'unclassified',
            'scope_source' => '',
            'classified_at' => 0,
            'topic_status' => 'format_pending',
            'topic_score' => 0,
            'topic_targets' => '[]',
            'payload' => wp_json_encode($payload, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES),
        );
        $source_fingerprint = array(
            'provider'=>$provider,
            'partner_external_id'=>$partner_external_id,
            'external_id'=>$external_id,
            'creative_type'=>$type,
            'title'=>$title,
            'description'=>$description,
            'tags'=>$tags,
            'image_url'=>$image_url,
            'destination_url'=>$destination_url,
            'tracking_url'=>$tracking_url,
            'declared_width'=>$declared_width,
            'declared_height'=>$declared_height,
            'source_status'=>$source_status,
            'source_kind'=>$normalized['source_kind'],
        );
        $normalized['source_hash'] = hash('sha256', wp_json_encode($source_fingerprint, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES));
        return $normalized;
    }









    private function creative_library_upsert($creative) {
        if (!is_array($creative) || (string) ($creative['creative_type'] ?? '') === 'native_partner' || strpos((string) ($creative['external_id'] ?? ''), 'native-') === 0) {
            return 'blocked';
        }
        global $wpdb;
        $table = $this->creative_library_table();
        $now = time();
        $existing = $wpdb->get_row($wpdb->prepare(
            "SELECT id, source_hash, first_seen, review_status, selected, content_scope, scope_source, classified_at, payload FROM {$table} WHERE identity_hash=%s",
            $creative['identity_hash']
        ), ARRAY_A);
        $data = $creative;
        $data['first_seen'] = $existing ? absint($existing['first_seen']) : $now;
        $data['last_seen'] = $now;
        if ($existing) {
            $data['review_status'] = (string) $existing['review_status'];
            $data['selected'] = absint($existing['selected']);
            $data['content_scope'] = sanitize_key((string) ($existing['content_scope'] ?? 'unclassified'));
            $data['scope_source'] = sanitize_key((string) ($existing['scope_source'] ?? ''));
            $data['classified_at'] = absint($existing['classified_at'] ?? 0);
            if (hash_equals((string) $existing['source_hash'], (string) $creative['source_hash'])) {
                // Source bytes can be unchanged while a newer policy/classifier
                // contract produces different derived metadata. Keeping the old
                // payload here stranded existing eBay BUSINESS creatives on an
                // obsolete concept contract forever: Maintenance reclassified the
                // source row, but Output planning read the stale creative payload.
                // Refresh only derived/runtime fields; manual review/selection and
                // editorial classification remain preserved above.
                $same_source_update = array(
                    'last_seen'=>$now,
                    'source_status'=>$creative['source_status'],
                    'source_kind'=>$creative['source_kind'],
                    'availability_state'=>'active',
                    'missing_count'=>0,
                    'last_complete_run'=>$creative['last_complete_run'],
                );
                if (array_key_exists('payload', $creative)) {
                    $existing_payload = json_decode((string)($existing['payload'] ?? ''), true);
                    $incoming_payload = json_decode((string)$creative['payload'], true);
                    $existing_payload = is_array($existing_payload) ? $existing_payload : array();
                    $incoming_payload = is_array($incoming_payload) ? $incoming_payload : array();
                    // The source hash includes the image URL. Therefore an equal
                    // source hash means an already verified asset still refers to
                    // the same bytes/source. Refresh classifier/policy-derived
                    // fields, but never downgrade verified image evidence back to
                    // the new creative's initial pending/0x0 state.
                    foreach (array(
                        '_declared_width','_declared_height','_dimension_state','_dimension_error',
                        '_image_sha256','_image_mime','_image_bytes','_measured_at',
                        '_preverify_topic_status','_preverify_topic_score','_preverify_topic_targets'
                    ) as $runtime_key) {
                        if (array_key_exists($runtime_key, $existing_payload)) {
                            $incoming_payload[$runtime_key] = $existing_payload[$runtime_key];
                        }
                    }
                    $same_source_update['payload'] = wp_json_encode($incoming_payload, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
                }
                if (array_key_exists('tags', $creative)) {
                    $same_source_update['tags'] = $creative['tags'];
                }
                $wpdb->update($table, $same_source_update, array('id'=>absint($existing['id'])));
                return 'unchanged';
            }
            $wpdb->update($table, $data, array('id'=>absint($existing['id'])));
            return 'updated';
        }
        $wpdb->insert($table, $data);
        return $wpdb->insert_id ? 'imported' : 'failed';
    }

    private function creative_library_import_body($body, $extension, $paste_mode = false) {
        if ($paste_mode) {
            return $this->creative_library_parse_html_codes($body, 5000);
        }
        if ($extension === 'json') {
            return $this->creative_library_parse_json($body, 5000);
        }
        if ($extension === 'txt') {
            return $this->creative_library_parse_html_codes($body, 5000);
        }
        return $this->creative_library_parse_csv($body, 5000);
    }

    private function creative_library_partner_context($source) {
        $provider = sanitize_key((string) ($source['provider'] ?? 'awin'));
        $partner_external_id = preg_replace('/[^0-9A-Za-z._-]/', '', (string) ($source['partner_external_id'] ?? ''));
        $partner_name = sanitize_text_field((string) ($source['partner_name'] ?? ''));
        if ($provider === '' || strlen($provider) > 60 || !method_exists($this, 'provider_exists') || !$this->provider_exists($provider)) {
            return new WP_Error('creative_import_provider', 'Provider ist nicht im zentralen Providerregister registriert.');
        }
        if ($partner_name === '') {
            return new WP_Error('creative_import_partner', 'Partnername fehlt.');
        }
        return array('provider'=>$provider,'partner_external_id'=>$partner_external_id,'partner_name'=>$partner_name);
    }

    public function handle_creative_library_import() {
        if (!current_user_can('manage_options')) {
            wp_die('Keine Berechtigung.');
        }
        check_admin_referer('ppar_creative_library_import', 'ppar_creative_library_nonce');
        $context = $this->creative_library_partner_context($_POST);
        if (is_wp_error($context)) {
            $this->creative_library_redirect('failed', $context->get_error_message());
        }
        $paste = trim((string) wp_unslash($_POST['creative_codes'] ?? ''));
        $body = '';
        $extension = '';
        $paste_mode = false;
        if ($paste !== '') {
            $body = $paste;
            $extension = 'txt';
            $paste_mode = true;
        } elseif (!empty($_FILES['creative_file']['tmp_name'])) {
            $file = $_FILES['creative_file'];
            if (!empty($file['error']) || !is_uploaded_file($file['tmp_name'])) {
                $this->creative_library_redirect('failed', 'Dateiupload fehlgeschlagen.');
            }
            if ((int) $file['size'] <= 0 || (int) $file['size'] > 20971520) {
                $this->creative_library_redirect('failed', 'Die Datei muss zwischen 1 Byte und 20 MiB groß sein.');
            }
            $extension = strtolower(pathinfo((string) $file['name'], PATHINFO_EXTENSION));
            if (!in_array($extension, $this->creative_library_allowed_upload_extensions(), true)) {
                $this->creative_library_redirect('failed', 'Nur CSV, JSON oder TXT sind zulässig.');
            }
            $body = (string) file_get_contents($file['tmp_name']);
        } else {
            $this->creative_library_redirect('failed', 'Bitte eine Sammeldatei hochladen oder Banner-Codes einfügen.');
        }
        $parsed = $this->creative_library_import_body($body, $extension, $paste_mode);
        if (is_wp_error($parsed)) {
            $this->creative_library_redirect('failed', $parsed->get_error_message());
        }
        $counts = array('seen'=>0,'imported'=>0,'updated'=>0,'unchanged'=>0,'blocked'=>0,'failed'=>0);
        foreach ((array) $parsed['rows'] as $row) {
            $counts['seen']++;
            $creative = $this->creative_library_normalize_row($row, $parsed['mapping'], $context);
            if (is_wp_error($creative)) {
                $counts['blocked']++;
                continue;
            }
            $result = $this->creative_library_upsert($creative);
            if (isset($counts[$result])) {
                $counts[$result]++;
            } else {
                $counts['failed']++;
            }
        }
        if ($counts['imported'] > 0 || $counts['updated'] > 0) {
            $this->creative_library_schedule_asset_verification(10);
        }
        $message = sprintf('%d erkannt · %d neu · %d aktualisiert · %d unverändert · %d blockiert. Bildprüfung läuft paketweise im Hintergrund.', $counts['seen'], $counts['imported'], $counts['updated'], $counts['unchanged'], $counts['blocked']);
        $this->creative_library_redirect('success', $message, $context);
    }

    private function creative_library_redirect($status, $message, $context = array()) {
        $args = array(
            'page' => 'affiliate-portal-creative-library',
            'ppar_library' => sanitize_key((string) $status),
            'ppar_message' => rawurlencode(sanitize_text_field((string) $message)),
        );
        if (!empty($context['provider'])) {
            $args['provider'] = sanitize_key($context['provider']);
        }
        if (!empty($context['partner_external_id'])) {
            $args['partner_external_id'] = rawurlencode((string) $context['partner_external_id']);
        }
        wp_safe_redirect(add_query_arg($args, admin_url('admin.php')));
        exit;
    }

    private function creative_library_row_by_id($id) {
        global $wpdb;
        $table = $this->creative_library_table();
        return $wpdb->get_row($wpdb->prepare("SELECT * FROM {$table} WHERE id=%d", absint($id)), ARRAY_A);
    }

    private function creative_library_existing_campaign_ids($identity_hash) {
        if (!function_exists('get_posts') || !defined('ABSPATH')) {
            return array();
        }
        return array_values(array_filter(array_map('absint', (array) get_posts(array(
            'post_type'=>self::CAMPAIGN_POST_TYPE,
            'post_status'=>array('publish','draft','pending','private'),
            'meta_key'=>'ppar_library_identity_hash',
            'meta_value'=>sanitize_text_field((string) $identity_hash),
            'posts_per_page'=>20,
            'fields'=>'ids',
        )))));
    }

    private function creative_library_deactivate_existing_campaigns($identity_hash) {
        $count = 0;
        foreach ($this->creative_library_existing_campaign_ids($identity_hash) as $post_id) {
            if (!method_exists($this, 'campaign_from_post') || !method_exists($this, 'save_campaign_record') || !function_exists('get_post')) {
                continue;
            }
            $post = get_post($post_id);
            $campaign = $this->campaign_from_post($post);
            if (!is_array($campaign)) {
                continue;
            }
            $campaign['active'] = false;
            if ($this->save_campaign_record($campaign, $post_id)) {
                $count++;
            }
        }
        return $count;
    }


    public function creative_library_reapply_partner_profile($provider, $partner_external_id) {
        global $wpdb;
        $table = $this->creative_library_table();
        $rows = $wpdb->get_results($wpdb->prepare(
            "SELECT * FROM {$table} WHERE provider=%s AND partner_external_id=%s AND source_status='active' AND availability_state='active'",
            sanitize_key((string) $provider),
            preg_replace('/[^0-9A-Za-z._-]/', '', (string) $partner_external_id)
        ), ARRAY_A);
        $counts = array('updated'=>0,'blocked'=>0,'unchanged'=>0);
        foreach ((array) $rows as $row) {
            $payload = json_decode((string) ($row['payload'] ?? ''), true);
            $payload = is_array($payload) ? $payload : array();
            if (!in_array((string) ($payload['_dimension_state'] ?? ''), array('verified','mismatch'), true)) {
                $verified = $this->creative_library_verify_asset_row($row, false, true);
                if (is_wp_error($verified)) {
                    $counts['blocked']++;
                } else {
                    $counts['updated']++;
                }
                continue;
            }
            if (method_exists($this, 'output_plan_creative')) {
                $plan = $this->output_plan_creative($row, true);
                if (absint($plan['drafts'] ?? 0) > 0 || absint($plan['created'] ?? 0) > 0) {
                    $counts['updated']++;
                } else {
                    $counts['unchanged']++;
                }
            }
        }
        return $counts;
    }

    public function handle_creative_library_selection() {
        if (!current_user_can('manage_options')) {
            wp_die('Keine Berechtigung.');
        }
        check_admin_referer('ppar_creative_library_selection', 'ppar_creative_library_selection_nonce');
        $ids = array_values(array_filter(array_map('absint', (array) ($_POST['creative_ids'] ?? array()))));
        $mode = sanitize_key((string) ($_POST['selection_mode'] ?? 'selected'));
        $portal_key = sanitize_key((string) ($_POST['portal_key'] ?? ''));
        $allowed = array('selected','unselected','plan_all','prepare_all','portal_approve','portal_approve_fixed','portal_review','portal_veto','portal_automatic');
        if (!in_array($mode, $allowed, true)) {
            $mode = 'selected';
        }
        if (in_array($mode, array('portal_approve','portal_approve_fixed','portal_review','portal_veto','portal_automatic'), true)) {
            $portal = method_exists($this, 'output_portal_by_key') ? $this->output_portal_by_key($portal_key, true) : new WP_Error('portal_model_missing', 'Portalmodell fehlt.');
            if (is_wp_error($portal)) {
                $this->creative_library_redirect('failed', $portal->get_error_message());
            }
        }
        global $wpdb;
        $table = $this->creative_library_table();
        $updated = 0;
        $planned = 0;
        $drafts = 0;
        $blocked = 0;
        $errors = array();
        $context = array();
        foreach (array_slice($ids, 0, 1000) as $id) {
            $row = $this->creative_library_row_by_id($id);
            if (!is_array($row)) {
                $blocked++;
                continue;
            }
            if (!$context) {
                $context = array('provider'=>$row['provider'] ?? '', 'partner_external_id'=>$row['partner_external_id'] ?? '');
            }
            if ($mode === 'selected' || $mode === 'unselected') {
                $wpdb->update($table, array('selected'=>$mode === 'selected' ? 1 : 0), array('id'=>$id));
                $updated++;
                continue;
            }
            if (strpos($mode, 'portal_') === 0) {
                $decision = array(
                    'portal_approve'=>'approved',
                    'portal_approve_fixed'=>'approved',
                    'portal_review'=>'review',
                    'portal_veto'=>'veto',
                    'portal_automatic'=>'automatic',
                )[$mode];
                $decision_reason = sanitize_text_field((string) wp_unslash($_POST['decision_reason'] ?? ''));
                if ($decision_reason === '') {
                    $blocked++;
                    $errors['manual_reason_required'] = 'Für jede Chefentscheidung ist eine Begründung erforderlich.';
                    continue;
                }
                $decision_payload = array();
                if ($mode === 'portal_approve_fixed') {
                    $fixed_target_key = sanitize_text_field((string) wp_unslash($_POST['fixed_target_key'] ?? ''));
                    $fixed_slot_id = sanitize_key((string) wp_unslash($_POST['fixed_slot_id'] ?? ''));
                    if ($fixed_target_key === '') {
                        $blocked++;
                        $errors['fixed_target_required'] = 'Für eine feste Chefzuordnung muss ein Portalziel gewählt werden.';
                        continue;
                    }
                    $targets = method_exists($this, 'output_portal_targets') ? $this->output_portal_targets($portal) : new WP_Error('portal_targets_missing', 'Portalziele sind nicht verfügbar.');
                    if (is_wp_error($targets)) {
                        $blocked++;
                        $errors[$targets->get_error_code()] = $targets->get_error_message();
                        continue;
                    }
                    $fixed_target = null;
                    foreach ((array) $targets as $target) {
                        if (is_array($target) && (string) ($target['key'] ?? '') === $fixed_target_key) {
                            $fixed_target = $target;
                            break;
                        }
                    }
                    if (!is_array($fixed_target)) {
                        $blocked++;
                        $errors['fixed_target_invalid'] = 'Gewähltes Portalziel existiert nicht mehr.';
                        continue;
                    }
                    $decision_payload = array(
                        'target_type'=>(string) ($fixed_target['type'] ?? ''),
                        'target_key'=>(string) ($fixed_target['key'] ?? ''),
                        'target_label'=>(string) ($fixed_target['label'] ?? ''),
                        'target_context'=>(string) ($fixed_target['context'] ?? ''),
                        'slot_id'=>$fixed_slot_id,
                    );
                }
                if ($decision === 'veto') {
                    $this->output_block_creative((string) ($row['identity_hash'] ?? ''), $decision_reason, $portal_key);
                } else {
                    $saved = $this->output_set_portal_decision($portal_key, (string) ($row['identity_hash'] ?? ''), $decision, $decision_reason, $decision_payload);
                    if (is_wp_error($saved)) {
                        $blocked++;
                        $errors[$saved->get_error_code()] = $saved->get_error_message();
                        continue;
                    }
                }
                if (in_array($decision, array('approved','automatic'), true) && method_exists($this, 'output_plan_creative')) {
                    $result = $this->output_plan_creative($row, true);
                    if (is_wp_error($result)) {
                        $blocked++;
                        $errors[$result->get_error_code()] = $result->get_error_message();
                    } else {
                        $planned += absint($result['created'] ?? 0);
                        $drafts += absint($result['drafts'] ?? 0);
                        $blocked += absint($result['blocked'] ?? 0);
                        foreach ((array) ($result['errors'] ?? array()) as $code => $error_message) {
                            $errors[sanitize_key((string) $code)] = sanitize_text_field((string) $error_message);
                        }
                    }
                }
                $updated++;
                continue;
            }
            if (!method_exists($this, 'output_plan_creative')) {
                $blocked++;
                $errors['output_model_missing'] = 'Zentrales Ausgabeobjekt-Modell fehlt.';
                continue;
            }
            $result = $this->output_plan_creative($row, $mode === 'prepare_all');
            if (is_wp_error($result)) {
                $blocked++;
                $errors[$result->get_error_code()] = $result->get_error_message();
                continue;
            }
            $planned += absint($result['created'] ?? 0);
            $drafts += absint($result['drafts'] ?? 0);
            $blocked += absint($result['blocked'] ?? 0);
            foreach ((array) ($result['errors'] ?? array()) as $code => $message) {
                $errors[sanitize_key((string) $code)] = sanitize_text_field((string) $message);
            }
            $updated++;
        }
        $message = sprintf('%d Werbemittel verarbeitet · %d Ausgabeobjekte geplant · %d Entwürfe vorbereitet · %d blockiert.', $updated, $planned, $drafts, $blocked);
        if ($errors) {
            $message .= ' ' . implode(' ', array_values($errors));
        }
        $this->creative_library_redirect($blocked > 0 && $updated === 0 ? 'failed' : 'success', $message, $context);
    }
    private function creative_library_snapshots_for_select() {
        $snapshots = $this->partner_intake_snapshots();
        $out = array();
        foreach ($snapshots as $key => $snapshot) {
            if (!is_array($snapshot)) {
                continue;
            }
            $programme = is_array($snapshot['programme'] ?? null) ? $snapshot['programme'] : array();
            $provider = sanitize_key((string) ($snapshot['provider'] ?? ''));
            $external_id = preg_replace('/[^0-9A-Za-z._-]/', '', (string) ($snapshot['external_id'] ?? ''));
            $name = sanitize_text_field((string) ($programme['name'] ?? $snapshot['entered_name'] ?? ''));
            if ($provider !== '' && $name !== '') {
                $out[$provider . ':' . $external_id] = array('provider'=>$provider,'external_id'=>$external_id,'name'=>$name);
            }
        }
        return $out;
    }

    private function creative_library_query_rows($filters, $limit = 500) {
        global $wpdb;
        $table = $this->creative_library_table();
        $where = array("creative_type<>'native_partner'", "external_id NOT LIKE 'native-%'", "availability_state<>'inactive_missing'");
        $args = array();
        if (!empty($filters['provider'])) {
            $where[] = 'provider=%s';
            $args[] = $filters['provider'];
        }
        if (!empty($filters['partner_external_id'])) {
            $where[] = 'partner_external_id=%s';
            $args[] = $filters['partner_external_id'];
        }
        if (!empty($filters['topic_status'])) {
            $where[] = 'topic_status=%s';
            $args[] = $filters['topic_status'];
        }
        if (!empty($filters['selected'])) {
            $where[] = 'selected=1';
        }
        $sql = "SELECT * FROM {$table} WHERE " . implode(' AND ', $where) . ' ORDER BY partner_name ASC, width DESC, height DESC, id DESC LIMIT ' . absint($limit);
        return $args ? $wpdb->get_results($wpdb->prepare($sql, $args), ARRAY_A) : $wpdb->get_results($sql, ARRAY_A);
    }

    private function creative_library_count_rows() {
        global $wpdb;
        $table = $this->creative_library_table();
        $rows = $wpdb->get_results("SELECT review_status, selected, topic_status, COUNT(*) amount FROM {$table} WHERE creative_type<>'native_partner' AND external_id NOT LIKE 'native-%' AND availability_state<>'inactive_missing' GROUP BY review_status, selected, topic_status", ARRAY_A);
        $counts = array('all'=>0,'selected'=>0,'approved'=>0,'review'=>0,'blocked'=>0,'auto_verified'=>0,'auto_review'=>0,'ambiguous'=>0,'no_match'=>0,'format_blocked'=>0);
        foreach ((array) $rows as $row) {
            $amount = absint($row['amount'] ?? 0);
            $counts['all'] += $amount;
            if (!empty($row['selected'])) { $counts['selected'] += $amount; }
            $review = sanitize_key((string) ($row['review_status'] ?? ''));
            $topic = sanitize_key((string) ($row['topic_status'] ?? ''));
            if (isset($counts[$review])) { $counts[$review] += $amount; }
            if (isset($counts[$topic])) { $counts[$topic] += $amount; }
        }
        return $counts;
    }

    private function creative_library_target_summary($row) {
        if (!method_exists($this, 'output_portal_status_summary')) {
            return 'Noch keine portalbezogene Planung';
        }
        return $this->output_portal_status_summary((string) ($row['identity_hash'] ?? ''));
    }
    public function render_creative_library_page() {
        if (!current_user_can('manage_options')) {
            wp_die('Keine Berechtigung.');
        }
        $snapshots = $this->creative_library_snapshots_for_select();
        $provider = sanitize_key((string) ($_GET['provider'] ?? ''));
        $partner_external_id = preg_replace('/[^0-9A-Za-z._-]/', '', rawurldecode((string) ($_GET['partner_external_id'] ?? '')));
        $topic_status = sanitize_key((string) ($_GET['topic_status'] ?? ''));
        $selected = !empty($_GET['selected']);
        $rows = $this->creative_library_query_rows(compact('provider','partner_external_id','topic_status','selected'));
        $counts = $this->creative_library_count_rows();
        $notice = sanitize_key((string) ($_GET['ppar_library'] ?? ''));
        $message = rawurldecode((string) ($_GET['ppar_message'] ?? ''));
        $provider_registry = method_exists($this,'provider_registry') ? $this->provider_registry() : array();
        $default = array('provider'=>'manual','external_id'=>'','name'=>'');
        if ($provider !== '' && $partner_external_id !== '' && isset($snapshots[$provider . ':' . $partner_external_id])) {
            $default = $snapshots[$provider . ':' . $partner_external_id];
        } elseif ($snapshots) {
            $default = reset($snapshots);
        }
        $portals = method_exists($this, 'output_portal_registry') ? $this->output_portal_registry() : array();
        $fixed_targets = array();
        $fixed_slots = array();
        foreach ((array) $portals as $portal_key_option => $portal_option) {
            $targets_option = method_exists($this, 'output_portal_targets') ? $this->output_portal_targets($portal_option) : array();
            if (!is_wp_error($targets_option)) {
                foreach ((array) $targets_option as $target_option) {
                    if (!is_array($target_option) || empty($target_option['key']) || empty($target_option['label'])) { continue; }
                    $fixed_targets[] = array(
                        'portal_key'=>sanitize_key((string) $portal_key_option),
                        'key'=>(string) $target_option['key'],
                        'label'=>(string) $target_option['label'],
                        'type'=>(string) ($target_option['type'] ?? ''),
                    );
                }
            }
            $matrix_option = method_exists($this, 'output_slot_matrix') ? $this->output_slot_matrix($portal_option) : array();
            foreach ((array) $matrix_option as $slot_key_option => $slot_rule_option) {
                $fixed_slots[] = array(
                    'portal_key'=>sanitize_key((string) $portal_key_option),
                    'key'=>sanitize_key((string) $slot_key_option),
                    'label'=>sanitize_text_field((string) $slot_key_option . ' · ' . (string) ($slot_rule_option['creative_type'] ?? '')),
                );
            }
        }
        ?>
        <div class="wrap ppar-library-wrap">
            <style>
                .ppar-library-kpis{display:flex;flex-wrap:wrap;gap:10px}.ppar-library-kpi,.ppar-library-panel{background:#fff;border:1px solid #c3c4c7;padding:12px}.ppar-library-kpi{min-width:130px}.ppar-library-kpi span{display:block;color:#646970}.ppar-library-kpi strong{font-size:22px}.ppar-library-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:14px;align-items:start}.ppar-library-card{box-sizing:border-box;min-width:0;padding:12px;border:1px solid #c3c4c7;background:#fff}.ppar-library-card>img{display:block;width:100%;height:112px;margin:10px 0;object-fit:contain;background:#f6f7f7}.ppar-library-card h3{margin:8px 0;font-size:14px;line-height:1.3}.ppar-library-meta,.ppar-library-topic{font-size:12px;line-height:1.45}.ppar-library-decision{margin-top:8px;padding:8px;background:#f6f7f7;border-left:3px solid #2271b1}.ppar-chief-fields{display:grid;grid-template-columns:minmax(260px,1fr) minmax(260px,1fr);gap:12px;max-width:1000px;margin:10px 0}.ppar-chief-fields label{display:block}.ppar-chief-fields select,.ppar-chief-fields input{width:100%}@media(max-width:780px){.ppar-chief-fields{grid-template-columns:1fr}}
            </style>
            <h1>Import &amp; Auswahl</h1>
            <p>Werbemittel werden einmal importiert und danach automatisch je aktiviertem Portal gegen dessen Fachprofil, Zielbaum und Ausgabeplätze geprüft. Ein manuelles Veto gilt nur für das gewählte Portal.</p>
            <?php if ($notice === 'success') : ?><div class="notice notice-success inline"><p><?php echo esc_html($message); ?></p></div><?php endif; ?>
            <?php if ($notice === 'failed') : ?><div class="notice notice-error inline"><p><?php echo esc_html($message); ?></p></div><?php endif; ?>
            <div class="ppar-library-kpis">
                <div class="ppar-library-kpi"><span>Gesamt</span><strong><?php echo absint($counts['all']); ?></strong></div>
                <div class="ppar-library-kpi"><span>Ausgewählt</span><strong><?php echo absint($counts['selected']); ?></strong></div>
                <div class="ppar-library-kpi"><span>Bild geprüft</span><strong><?php echo absint($counts['auto_verified']); ?></strong></div>
                <div class="ppar-library-kpi"><span>Prüfung offen</span><strong><?php echo absint($counts['auto_review'] + $counts['ambiguous']); ?></strong></div>
                <div class="ppar-library-kpi"><span>Blockiert</span><strong><?php echo absint($counts['no_match'] + $counts['blocked'] + $counts['format_blocked']); ?></strong></div>
            </div>
            <details class="ppar-library-panel" style="margin-top:16px">
                <summary><strong>Sammelimport echter Provider-Werbemittel</strong></summary>
                <p class="description">CSV, JSON, TXT mit vollständigen Bannercodes oder direkt eingefügte vollständige Codes werden gesammelt verarbeitet. Der Import nimmt noch keine Portalzuordnung vor.</p>
                <form method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>" enctype="multipart/form-data">
                    <input type="hidden" name="action" value="ppar_creative_library_import">
                    <?php wp_nonce_field('ppar_creative_library_import', 'ppar_creative_library_nonce'); ?>
                    <div class="ppar-library-import"><div>
                        <p><label><strong>Aufgenommener Partner</strong><br><select id="ppar-library-snapshot"><option value="">Manuell eingeben</option><?php foreach ($snapshots as $key => $snapshot) : ?><option value="<?php echo esc_attr($key); ?>" data-provider="<?php echo esc_attr($snapshot['provider']); ?>" data-external="<?php echo esc_attr($snapshot['external_id']); ?>" data-name="<?php echo esc_attr($snapshot['name']); ?>"><?php echo esc_html($this->provider_label((string)$snapshot['provider']) . ' · ' . $snapshot['name'] . ($snapshot['external_id'] !== '' ? ' · ' . $snapshot['external_id'] : '')); ?></option><?php endforeach; ?></select></label></p>
                        <p><label><strong>Provider</strong><br><select id="ppar-library-provider" name="provider" required><?php foreach($provider_registry as $provider_key=>$provider_def): ?><option value="<?php echo esc_attr($provider_key); ?>" <?php selected((string)$default['provider'],$provider_key); ?>><?php echo esc_html((string)$provider_def['label']); ?></option><?php endforeach; ?></select></label></p>
                        <p><label><strong>Partner-ID</strong><br><input id="ppar-library-external" type="text" name="partner_external_id" maxlength="191" value="<?php echo esc_attr($default['external_id']); ?>"></label></p>
                        <p><label><strong>Partnername</strong><br><input id="ppar-library-name" type="text" name="partner_name" required maxlength="180" value="<?php echo esc_attr($default['name']); ?>"></label></p>
                    </div><div>
                        <p><label><strong>Sammeldatei</strong><br><input type="file" name="creative_file" accept=".csv,.json,.txt"></label><br><span class="description">CSV, JSON oder TXT; maximal 20 MiB und 5.000 Werbemittel.</span></p>
                        <p><label><strong>Oder mehrere Banner-Codes gesammelt einfügen</strong><br><textarea name="creative_codes" rows="8" placeholder="Mehrere vollständige &lt;a&gt;&lt;img&gt;-Codes auf einmal"></textarea></label></p>
                        <p><button class="button button-primary">Gesammelt importieren</button></p>
                    </div></div>
                </form>
                <script>document.addEventListener('DOMContentLoaded',function(){var s=document.getElementById('ppar-library-snapshot');if(!s)return;s.addEventListener('change',function(){var o=s.options[s.selectedIndex];if(!o||!o.value)return;document.getElementById('ppar-library-provider').value=o.dataset.provider||'';document.getElementById('ppar-library-external').value=o.dataset.external||'';document.getElementById('ppar-library-name').value=o.dataset.name||'';});});</script>
            </details>
            <form method="get" style="margin-top:18px"><input type="hidden" name="page" value="affiliate-portal-creative-library">
                <select name="provider"><option value="">Alle Provider</option><?php foreach($provider_registry as $provider_key=>$provider_def): ?><option value="<?php echo esc_attr($provider_key); ?>" <?php selected($provider,$provider_key); ?>><?php echo esc_html((string)$provider_def['label']); ?></option><?php endforeach; ?></select>
                <input type="text" name="partner_external_id" value="<?php echo esc_attr($partner_external_id); ?>" placeholder="Partner-ID">
                <select name="topic_status"><option value="">Alle technischen Zustände</option><option value="format_pending" <?php selected($topic_status,'format_pending'); ?>>Bildprüfung offen</option><option value="auto_verified" <?php selected($topic_status,'auto_verified'); ?>>Bild geprüft</option><option value="format_blocked" <?php selected($topic_status,'format_blocked'); ?>>Bild/Format blockiert</option></select>
                <label><input type="checkbox" name="selected" value="1" <?php checked($selected); ?>> nur ausgewählte</label>
                <?php submit_button('Filtern','secondary','',false); ?>
            </form>
            <form method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>">
                <input type="hidden" name="action" value="ppar_creative_library_selection">
                <?php wp_nonce_field('ppar_creative_library_selection', 'ppar_creative_library_selection_nonce'); ?>
                <p><label><strong>Portal für manuelle Entscheidung</strong> <select id="ppar-chief-portal" name="portal_key"><?php foreach ($portals as $key => $portal) : ?><option value="<?php echo esc_attr($key); ?>"><?php echo esc_html((string) ($portal['label'] ?? $key) . (empty($portal['enabled']) ? ' · deaktiviert' : '')); ?></option><?php endforeach; ?></select></label></p>
                <p><select id="ppar-chief-mode" name="selection_mode">
                    <option value="prepare_all">Alle aktivierten Portale automatisch prüfen und nur sichere Entwürfe vorbereiten</option>
                    <option value="plan_all">Alle aktivierten Portale automatisch prüfen, noch keine Entwürfe erzeugen</option>
                    <option value="portal_approve">Chefentscheidung: fachlich freigeben, Ziel und Slot automatisch</option>
                    <option value="portal_approve_fixed">Chefentscheidung: fachlich freigeben, Ziel und optional Slot fest vorgeben</option>
                    <option value="portal_review">Chefentscheidung: zur Prüfung zurückstellen</option>
                    <option value="portal_veto">Chefentscheidung: Creative für dieses Portal sperren (Veto)</option>
                    <option value="portal_automatic">Chefentscheidung zurücknehmen; Automatik wiederherstellen</option>
                    <option value="selected">Nur auswählen</option>
                    <option value="unselected">Markierung entfernen</option>
                </select></p>
                <div class="ppar-chief-fields">
                    <label><strong>Begründung der Chefentscheidung</strong><input type="text" name="decision_reason" placeholder="z. B. Zielgruppe Pferdehalter besitzt häufig weitere Hoftiere"></label>
                    <label class="ppar-fixed-field"><strong>Festes Portalziel</strong><select id="ppar-fixed-target" name="fixed_target_key"><option value="">Portalziel auswählen</option><?php foreach ($fixed_targets as $target_option) : ?><option data-portal="<?php echo esc_attr($target_option['portal_key']); ?>" value="<?php echo esc_attr($target_option['key']); ?>"><?php echo esc_html($target_option['label'] . ' · ' . $target_option['type']); ?></option><?php endforeach; ?></select></label>
                    <label class="ppar-fixed-field"><strong>Fester Designslot (optional)</strong><select id="ppar-fixed-slot" name="fixed_slot_id"><option value="">Slot automatisch bestimmen</option><?php foreach ($fixed_slots as $slot_option) : ?><option data-portal="<?php echo esc_attr($slot_option['portal_key']); ?>" value="<?php echo esc_attr($slot_option['key']); ?>"><?php echo esc_html($slot_option['label']); ?></option><?php endforeach; ?></select></label>
                </div>
                <p><button class="button">Auf angehakte Werbemittel anwenden</button></p>
                <script>(function(){var mode=document.getElementById('ppar-chief-mode'),portal=document.getElementById('ppar-chief-portal'),fixed=document.querySelectorAll('.ppar-fixed-field');function refresh(){var isFixed=mode&&mode.value==='portal_approve_fixed';fixed.forEach(function(el){el.style.display=isFixed?'block':'none';});[document.getElementById('ppar-fixed-target'),document.getElementById('ppar-fixed-slot')].forEach(function(sel){if(!sel)return;Array.prototype.forEach.call(sel.options,function(opt,index){if(index===0)return;opt.disabled=portal&&opt.getAttribute('data-portal')!==portal.value;});if(sel.selectedOptions.length&&sel.selectedOptions[0].disabled)sel.value='';});}if(mode)mode.addEventListener('change',refresh);if(portal)portal.addEventListener('change',refresh);refresh();})();</script>
                <div class="ppar-library-grid">
                    <?php if (!$rows) : ?><div class="ppar-library-panel"><p>Noch keine echten Provider-Werbemittel importiert.</p></div><?php endif; ?>
                    <?php foreach ($rows as $row) : $payload=json_decode((string)($row['payload']??''),true); $payload=is_array($payload)?$payload:array(); ?>
                        <article class="ppar-library-card">
                            <label><input type="checkbox" name="creative_ids[]" value="<?php echo absint($row['id']); ?>" <?php checked(!empty($row['selected'])); ?>> auswählen</label>
                            <?php if (!empty($row['image_url'])) : ?><img loading="lazy" src="<?php echo esc_url($row['image_url']); ?>" alt=""><?php endif; ?>
                            <h3><?php echo esc_html((string) $row['title']); ?></h3>
                            <p class="ppar-library-meta"><?php echo esc_html($this->provider_label((string)$row['provider']) . ' · ' . (string) $row['partner_name']); ?><br><?php echo $row['width'] && $row['height'] ? absint($row['width']) . ' × ' . absint($row['height']) . ' px' : 'Reale Bildmaße noch nicht verifiziert'; ?> · <?php echo esc_html((string) ($payload['_dimension_state'] ?? 'pending')); ?></p>
                            <div class="ppar-library-topic"><strong>Portalstatus</strong><br><?php echo esc_html($this->creative_library_target_summary($row)); ?></div>
                            <?php if ($portals) : foreach ($portals as $decision_portal_key => $decision_portal) : $chief_decision=$this->output_portal_decision((string)$decision_portal_key,(string)($row['identity_hash']??'')); $chief_payload=is_array($chief_decision['payload']??null)?$chief_decision['payload']:array(); ?>
                            <div class="ppar-library-decision" data-portal-key="<?php echo esc_attr((string)$decision_portal_key); ?>"><strong>Chefentscheidung · <?php echo esc_html((string)($decision_portal['label']??$decision_portal_key)); ?></strong><br><?php echo esc_html((string) ($chief_decision['manual_status'] ?? 'automatic')); ?><?php if (!empty($chief_decision['reason'])) : ?><br><?php echo esc_html((string) $chief_decision['reason']); ?><?php endif; ?><?php if(!empty($chief_payload['target_label'])): ?><br>Ziel: <?php echo esc_html((string)$chief_payload['target_label']); ?><?php endif; ?><?php if(!empty($chief_payload['slot_id'])): ?><br>Slot: <?php echo esc_html((string)$chief_payload['slot_id']); ?><?php endif; ?></div>
                            <?php endforeach; else : ?><div class="ppar-library-decision"><strong>Chefentscheidung</strong><br>Kein Portal registriert.</div><?php endif; ?>
                            <p class="ppar-library-meta">Quelle: <?php echo esc_html((string) $row['source_status']); ?> · Sichtprüfung: <?php echo esc_html((string) $row['review_status']); ?></p>
                        </article>
                    <?php endforeach; ?>
                </div>
            </form>
        </div>
        <?php
    }
}
