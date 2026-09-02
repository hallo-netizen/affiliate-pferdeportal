<?php
if (!defined('ABSPATH')) { exit; }

/**
 * Ein einziger manueller Dateieingang für bestehende Affiliate-Provider.
 *
 * Der Provider wird ausschließlich aus starken Dateisignaturen erkannt. Bei
 * unbekannten oder widersprüchlichen Signaturen wird fail-closed nichts importiert.
 * Provider-spezifische Fachlogik wird nicht dupliziert: vorhandene öffentliche
 * Import-Handler werden weiterverwendet. Die DS24-Partnerschafts-CSV ist die
 * einzige Inventur, die hier direkt materialisiert wird, weil die öffentliche
 * DS24-API diese Affiliate-seitige Bestandsliste nicht vollständig liefert.
 */
final class PPAR_Affiliate_Universal_Import {
    const ACTION = 'ppar_universal_manual_import';
    const NONCE_ACTION = 'ppar_universal_manual_import';
    const NONCE_FIELD = 'ppar_universal_import_nonce';
    const LAST_OPTION = 'ppar_universal_import_last_v1';
    const DS24_INVENTORY_OPTION = 'ppar_digistore24_manual_inventory_v1';
    const MAX_SAMPLE_BYTES = 1048576;
    const MAX_DS24_DECOMPRESSED_BYTES = 33554432;

    private static $booted = false;

    public static function bootstrap() {
        if (self::$booted) { return; }
        self::$booted = true;
        add_action('admin_post_' . self::ACTION, array(__CLASS__, 'handle_upload'));
    }

    public static function render_form() {
        if (!current_user_can('manage_options')) { return; }
        $notice = sanitize_key((string)($_GET['ppar_universal_import'] ?? ''));
        $message = rawurldecode((string)($_GET['ppar_universal_message'] ?? ''));
        $last = get_option(self::LAST_OPTION, array());
        $last = is_array($last) ? $last : array();
        ?>
        <section class="postbox" style="padding:16px;margin:18px 0;max-width:900px">
            <h2 style="margin-top:0">Datei importieren</h2>
            <p>Eine Datei hochladen. Die Affiliate-Zentrale erkennt den Anbieter aus Dateiname, Kopfzeile und belastbaren Provider-Signaturen. Unklare Dateien werden ohne Änderung abgewiesen.</p>
            <?php if ($notice === 'success') : ?><div class="notice notice-success inline"><p><?php echo esc_html($message); ?></p></div><?php endif; ?>
            <?php if ($notice === 'failed') : ?><div class="notice notice-error inline"><p><?php echo esc_html($message); ?></p></div><?php endif; ?>
            <form method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>" enctype="multipart/form-data">
                <input type="hidden" name="action" value="<?php echo esc_attr(self::ACTION); ?>">
                <?php wp_nonce_field(self::NONCE_ACTION, self::NONCE_FIELD); ?>
                <p><input type="file" name="affiliate_import_file" accept=".csv,.csv.gz,.json,.txt,.gz" required></p>
                <p><button class="button button-primary" type="submit">Datei prüfen &amp; importieren</button></p>
                <p class="description">Unterstützt werden vorhandene manuelle Importpfade sowie der Digistore24-Export „Partnerschaften mit Vendoren“. Der Upload veröffentlicht nichts ungeprüft.</p>
            </form>
            <?php if (!empty($last['provider']) && !empty($last['imported_at'])) : ?>
                <p class="description"><strong>Letzter Import:</strong> <?php echo esc_html((string)$last['provider']); ?> · <?php echo esc_html(wp_date('d.m.Y H:i', absint($last['imported_at']))); ?><?php if (!empty($last['message'])) : ?> · <?php echo esc_html((string)$last['message']); ?><?php endif; ?></p>
            <?php endif; ?>
        </section>
        <?php
    }

    public static function handle_upload() {
        if (!current_user_can('manage_options')) { wp_die('Keine Berechtigung.'); }
        check_admin_referer(self::NONCE_ACTION, self::NONCE_FIELD);
        if (empty($_FILES['affiliate_import_file']) || !is_array($_FILES['affiliate_import_file'])) {
            self::redirect('failed', 'Keine Importdatei hochgeladen.');
        }
        $file = $_FILES['affiliate_import_file'];
        if ((int)($file['error'] ?? UPLOAD_ERR_NO_FILE) !== UPLOAD_ERR_OK || empty($file['tmp_name']) || !is_uploaded_file($file['tmp_name'])) {
            self::redirect('failed', 'Dateiupload fehlgeschlagen.');
        }
        $size = (int)($file['size'] ?? 0);
        $server_limit = function_exists('wp_max_upload_size') ? (int)wp_max_upload_size() : 0;
        if ($size <= 0 || ($server_limit > 0 && $size > $server_limit)) {
            self::redirect('failed', 'Die Datei ist leer oder größer als das Server-Uploadlimit.');
        }
        $name = sanitize_file_name((string)($file['name'] ?? 'import'));
        if (!preg_match('/\.(?:csv|json|txt|csv\.gz|gz)$/i', $name)) {
            self::redirect('failed', 'Zulässig sind CSV, CSV.GZ, JSON oder TXT.');
        }
        $sample = self::read_sample((string)$file['tmp_name'], $name);
        if (is_wp_error($sample)) { self::redirect('failed', $sample->get_error_message()); }
        $detected = self::detect_provider($name, $sample);
        if (is_wp_error($detected)) { self::redirect('failed', $detected->get_error_message()); }

        $kind = (string)($detected['kind'] ?? '');
        if ($kind === 'digistore24_partnerships') {
            $result = self::import_digistore24_partnerships((string)$file['tmp_name'], $name);
            if (is_wp_error($result)) { self::redirect('failed', $result->get_error_message()); }
            self::remember('Digistore24', (string)$result['message'], (string)($result['sha256'] ?? ''));
            self::redirect('success', (string)$result['message']);
        }
        if ($kind === 'idealo_feed') {
            self::delegate_idealo($file);
        }
        if (in_array($kind, array('awin_creatives','adcell_creatives','digistore24_creatives'), true)) {
            $provider = array(
                'awin_creatives'=>'awin',
                'adcell_creatives'=>'adcell',
                'digistore24_creatives'=>'digistore24',
            )[$kind];
            self::delegate_creative_library($file, $provider, $name);
        }
        if ($kind === 'ebay_detected') {
            self::redirect('failed', 'eBay-Datei erkannt. Der bestehende eBay-Produktpfad ist API-basiert; diese Datei wird nicht in einen falschen Importpfad umgeleitet.');
        }
        self::redirect('failed', 'Anbieter erkannt, aber für dieses Dateiformat existiert kein freigegebener manueller Importpfad.');
    }

    private static function read_sample($path, $name) {
        $path = (string)$path;
        if ($path === '' || !is_readable($path)) { return new WP_Error('universal_import_unreadable', 'Importdatei ist nicht lesbar.'); }
        $is_gzip = preg_match('/\.gz$/i', (string)$name) === 1;
        if ($is_gzip) {
            if (!function_exists('gzopen')) { return new WP_Error('universal_import_gzip_missing', 'GZIP-Unterstützung fehlt auf dem Server.'); }
            $h = @gzopen($path, 'rb');
            if (!$h) { return new WP_Error('universal_import_gzip_open', 'GZIP-Datei konnte nicht geöffnet werden.'); }
            $body = '';
            while (!gzeof($h) && strlen($body) < self::MAX_SAMPLE_BYTES) {
                $chunk = gzread($h, min(131072, self::MAX_SAMPLE_BYTES - strlen($body)));
                if ($chunk === false) { gzclose($h); return new WP_Error('universal_import_gzip_read', 'GZIP-Datei konnte nicht gelesen werden.'); }
                $body .= $chunk;
            }
            gzclose($h);
        } else {
            $body = (string)@file_get_contents($path, false, null, 0, self::MAX_SAMPLE_BYTES);
        }
        if ($body === '') { return new WP_Error('universal_import_empty', 'Datei enthält keine lesbaren Daten.'); }
        return self::normalize_text_encoding($body);
    }

    private static function read_full_text($path, $name) {
        $is_gzip = preg_match('/\.gz$/i', (string)$name) === 1;
        if (!$is_gzip) {
            $size = @filesize($path);
            if ($size !== false && $size > self::MAX_DS24_DECOMPRESSED_BYTES) {
                return new WP_Error('universal_import_too_large', 'Digistore24-Partnerschaftsdatei überschreitet 32 MiB.');
            }
            $body = (string)@file_get_contents($path);
            return $body === '' ? new WP_Error('universal_import_empty', 'Datei ist leer.') : self::normalize_text_encoding($body);
        }
        if (!function_exists('gzopen')) { return new WP_Error('universal_import_gzip_missing', 'GZIP-Unterstützung fehlt auf dem Server.'); }
        $h = @gzopen($path, 'rb');
        if (!$h) { return new WP_Error('universal_import_gzip_open', 'GZIP-Datei konnte nicht geöffnet werden.'); }
        $body = '';
        while (!gzeof($h)) {
            $chunk = gzread($h, 262144);
            if ($chunk === false) { gzclose($h); return new WP_Error('universal_import_gzip_read', 'GZIP-Datei konnte nicht gelesen werden.'); }
            $body .= $chunk;
            if (strlen($body) > self::MAX_DS24_DECOMPRESSED_BYTES) {
                gzclose($h);
                return new WP_Error('universal_import_too_large', 'Entpackte Digistore24-Partnerschaftsdatei überschreitet 32 MiB.');
            }
        }
        gzclose($h);
        return $body === '' ? new WP_Error('universal_import_empty', 'Datei ist leer.') : self::normalize_text_encoding($body);
    }

    private static function normalize_text_encoding($body) {
        $body = preg_replace('/^\xEF\xBB\xBF/', '', (string)$body);
        if (function_exists('mb_check_encoding') && !mb_check_encoding($body, 'UTF-8') && function_exists('mb_convert_encoding')) {
            $body = mb_convert_encoding($body, 'UTF-8', 'Windows-1252,ISO-8859-1,UTF-8');
        }
        return $body;
    }

    private static function normalize_key($value) {
        $value = trim((string)$value);
        if (function_exists('remove_accents')) { $value = remove_accents($value); }
        else { $value = strtr($value, array('Ä'=>'A','Ö'=>'O','Ü'=>'U','ä'=>'a','ö'=>'o','ü'=>'u','ß'=>'ss')); }
        $value = strtolower($value);
        $value = preg_replace('/[^a-z0-9]+/', '_', $value);
        return trim((string)$value, '_');
    }

    private static function detect_delimiter($line) {
        $best = ','; $score = -1;
        foreach (array(';', ',', "\t", '|') as $candidate) {
            $count = substr_count((string)$line, $candidate);
            if ($count > $score) { $best = $candidate; $score = $count; }
        }
        return $best;
    }

    private static function csv_headers_from_sample($sample) {
        $first = preg_split('/\r\n|\r|\n/', (string)$sample, 2)[0] ?? '';
        $delimiter = self::detect_delimiter($first);
        $headers = str_getcsv($first, $delimiter, '"', '\\');
        return array_values(array_filter(array_map(array(__CLASS__, 'normalize_key'), (array)$headers), 'strlen'));
    }

    private static function has_any($headers, $aliases) {
        $set = array_fill_keys((array)$headers, true);
        foreach ((array)$aliases as $alias) { if (isset($set[self::normalize_key($alias)])) { return true; } }
        return false;
    }

    private static function looks_like_ds24_partnership_headers($headers) {
        return self::has_any($headers, array('vendor','vendorname','anbieter'))
            && self::has_any($headers, array('produkt-id','produkt id','produkt_id','product-id','product_id','productid'))
            && self::has_any($headers, array('produkt','produktname','product','product_name'))
            && self::has_any($headers, array('werbemittel-id','werbemittel id','werbemittel_id','marketplace_entry_id','entry_id'))
            && self::has_any($headers, array('status der partnerschaft','partnerschaftsstatus','status','approval_status'))
            && self::has_any($headers, array('provision','affiliate-provision','affiliate_provision','commission','commission_rate'));
    }

    private static function detect_provider($name, $sample) {
        $headers = self::csv_headers_from_sample($sample);
        if (self::looks_like_ds24_partnership_headers($headers)) {
            return array('provider'=>'digistore24','kind'=>'digistore24_partnerships','confidence'=>'exact_headers');
        }
        $lower = strtolower((string)$sample);
        $name_lower = strtolower((string)$name);
        $signals = array();
        if (preg_match('/^productdata_[0-9]+\.csv(?:\.gz)?$/i', basename($name_lower))) { $signals['idealo_feed'] = true; }
        if (strpos($lower, 'awin1.com') !== false || strpos($lower, 'zenaps.com') !== false) { $signals['awin_creatives'] = true; }
        if (strpos($lower, 'adcell.de') !== false || strpos($lower, 't.adcell.com') !== false) { $signals['adcell_creatives'] = true; }
        if ((strpos($lower, 'checkout-ds24.com') !== false || strpos($lower, 'digistore24.com') !== false) && (strpos($lower, '<img') !== false || self::has_any($headers, array('banner_url','image_url','tracking_url')))) { $signals['digistore24_creatives'] = true; }
        if (strpos($lower, 'ebay.') !== false && (strpos($lower, 'itemid') !== false || strpos($lower, 'item_id') !== false || strpos($lower, 'epn') !== false)) { $signals['ebay_detected'] = true; }
        if (count($signals) === 1) {
            $kind = key($signals);
            return array('provider'=>strtok($kind, '_'),'kind'=>$kind,'confidence'=>'strong_signature');
        }
        if (count($signals) > 1) {
            return new WP_Error('universal_import_ambiguous', 'Datei enthält widersprüchliche Provider-Signaturen und wird nicht geraten.');
        }
        return new WP_Error('universal_import_unknown', 'Anbieter konnte aus dieser Datei nicht sicher erkannt werden. Keine Daten wurden verändert.');
    }

    private static function alias_map() {
        return array(
            'vendor'=>array('vendor','vendorname','anbieter'),
            'product_id'=>array('produkt-id','produkt id','produkt_id','produktid','product-id','product_id','productid'),
            'product'=>array('produkt','produktname','product','product_name'),
            'entry_id'=>array('werbemittel-id','werbemittel id','werbemittel_id','werbemittelid','marketplace_entry_id','entry_id'),
            'status'=>array('status der partnerschaft','partnerschaftsstatus','status','approval_status'),
            'commission'=>array('provision','affiliate-provision','affiliate_provision','commission','commission_rate'),
            'support_url'=>array('werbemittelseite','werbemittel-seite','werbemittel_url','werbemittel-url','support_url','affiliate_support_url','affiliate-support-seite'),
            'promolink'=>array('promolink','promo-link','promo_link','affiliate_link','affiliate-link','tracking_link','tracking-link'),
        );
    }

    private static function resolve_columns($headers) {
        $normalized = array();
        foreach ((array)$headers as $index=>$header) { $normalized[self::normalize_key($header)] = $index; }
        $resolved = array();
        foreach (self::alias_map() as $target=>$aliases) {
            foreach ($aliases as $alias) {
                $key = self::normalize_key($alias);
                if (array_key_exists($key, $normalized)) { $resolved[$target] = $normalized[$key]; break; }
            }
        }
        return $resolved;
    }

    private static function parse_ds24_csv($body) {
        $body = self::normalize_text_encoding($body);
        $lines = preg_split('/\r\n|\r|\n/', $body, 2);
        $delimiter = self::detect_delimiter($lines[0] ?? '');
        $h = fopen('php://temp', 'r+');
        if (!$h) { return new WP_Error('ds24_csv_stream', 'CSV konnte nicht verarbeitet werden.'); }
        fwrite($h, $body); rewind($h);
        $headers = fgetcsv($h, 0, $delimiter, '"', '\\');
        if (!is_array($headers)) { fclose($h); return new WP_Error('ds24_csv_headers', 'CSV-Kopfzeile fehlt.'); }
        $columns = self::resolve_columns($headers);
        foreach (array('vendor','product_id','product','entry_id','status','commission') as $required) {
            if (!array_key_exists($required, $columns)) { fclose($h); return new WP_Error('ds24_csv_schema', 'Digistore24-CSV hat nicht die erwarteten Partnerschaftsspalten.'); }
        }
        $rows = array(); $blocked = 0; $seen = 0;
        while (($values = fgetcsv($h, 0, $delimiter, '"', '\\')) !== false) {
            if (++$seen > 5000) { fclose($h); return new WP_Error('ds24_csv_row_limit', 'Mehr als 5.000 Partnerschaftszeilen werden nicht in einem Lauf verarbeitet.'); }
            if (!array_filter($values, static function($v){ return trim((string)$v) !== ''; })) { continue; }
            $get = static function($field) use ($columns, $values) {
                return array_key_exists($field, $columns) ? trim((string)($values[$columns[$field]] ?? '')) : '';
            };
            $status_raw = $get('status');
            $status = self::normalize_key($status_raw);
            if (!in_array($status, array('genehmigt','approved'), true)) { $blocked++; continue; }
            $vendor = trim($get('vendor'));
            $product_id = preg_replace('/\s+/', '', $get('product_id'));
            $product = trim($get('product'));
            $entry_id = preg_replace('/\s+/', '', $get('entry_id'));
            if ($vendor === '' || $product === '' || !ctype_digit($product_id) || !ctype_digit($entry_id)) { $blocked++; continue; }
            $support_url = trim($get('support_url'));
            $promolink = trim($get('promolink'));
            if ($support_url !== '' && (!filter_var($support_url, FILTER_VALIDATE_URL) || stripos($support_url, 'https://') !== 0)) { $support_url = ''; }
            if ($promolink !== '' && (!filter_var($promolink, FILTER_VALIDATE_URL) || stripos($promolink, 'https://') !== 0)) { $promolink = ''; }
            $rows[$product_id] = array(
                'vendor'=>$vendor,
                'product_id'=>$product_id,
                'product'=>$product,
                'entry_id'=>$entry_id,
                'status'=>'approved',
                'status_label'=>$status_raw,
                'commission'=>trim($get('commission')),
                'support_url'=>$support_url,
                'promolink'=>$promolink,
            );
        }
        fclose($h);
        if (!$rows) { return new WP_Error('ds24_csv_no_approved', 'Keine genehmigte Digistore24-Partnerschaft erkannt.'); }
        return array('rows'=>$rows,'blocked'=>$blocked);
    }

    private static function ds24_identity() {
        $settings = get_option('ppar_network_digistore24_v1', array());
        $settings = is_array($settings) ? $settings : array();
        $key = defined('PPAR_DIGISTORE24_API_KEY') && trim((string)PPAR_DIGISTORE24_API_KEY) !== '' ? trim((string)PPAR_DIGISTORE24_API_KEY) : trim((string)($settings['api_key'] ?? ''));
        $fingerprint = strtolower(trim((string)($settings['tested_key_fingerprint'] ?? '')));
        $affiliate_id = trim((string)($settings['affiliate_id'] ?? ''));
        if ($key === '' || !preg_match('/^[a-f0-9]{64}$/', $fingerprint) || !hash_equals($fingerprint, hash('sha256', $key)) || !preg_match('/^[0-9A-Za-z._-]+$/', $affiliate_id)) {
            return new WP_Error('ds24_manual_identity_required', 'Digistore24-Datei erkannt. Vor dem Import muss derselbe Digistore24-Zugang unter Anbieter & APIs einmal erfolgreich read-only geprüft sein.');
        }
        return array('key_fingerprint'=>$fingerprint,'affiliate_id'=>$affiliate_id);
    }

    private static function group_ds24_rows($rows) {
        $groups = array();
        foreach ((array)$rows as $product_id=>$row) {
            $entry_id = (string)($row['entry_id'] ?? '');
            if ($entry_id === '' || !ctype_digit($entry_id)) { continue; }
            if (!isset($groups[$entry_id])) {
                $groups[$entry_id] = array(
                    'entry_id'=>$entry_id,
                    'vendor'=>(string)$row['vendor'],
                    'product_ids'=>array(),
                    'products'=>array(),
                    'commissions'=>array(),
                    'support_url'=>(string)($row['support_url'] ?? ''),
                    'promolink'=>(string)($row['promolink'] ?? ''),
                );
            }
            if ((string)$groups[$entry_id]['vendor'] !== (string)$row['vendor']) {
                return new WP_Error('ds24_csv_entry_vendor_conflict', 'Dieselbe Werbemittel-ID ist mehreren Vendoren zugeordnet. Import wird vollständig abgebrochen.');
            }
            $groups[$entry_id]['product_ids'][(string)$product_id] = (string)$product_id;
            $groups[$entry_id]['products'][(string)$product_id] = (string)$row['product'];
            $groups[$entry_id]['commissions'][(string)$product_id] = (string)$row['commission'];
            if ($groups[$entry_id]['support_url'] === '' && !empty($row['support_url'])) { $groups[$entry_id]['support_url'] = (string)$row['support_url']; }
            if ($groups[$entry_id]['promolink'] === '' && !empty($row['promolink'])) { $groups[$entry_id]['promolink'] = (string)$row['promolink']; }
        }
        return $groups;
    }

    private static function import_digistore24_partnerships($path, $name) {
        $identity = self::ds24_identity();
        if (is_wp_error($identity)) { return $identity; }
        $body = self::read_full_text($path, $name);
        if (is_wp_error($body)) { return $body; }
        $parsed = self::parse_ds24_csv($body);
        if (is_wp_error($parsed)) { return $parsed; }
        $groups = self::group_ds24_rows($parsed['rows']);
        if (is_wp_error($groups)) { return $groups; }
        if (!$groups) { return new WP_Error('ds24_csv_no_sources', 'Keine verwertbare Digistore24-Werbemittelquelle erkannt.'); }

        $sha = hash('sha256', $body);
        $now = time();
        $existing_store = get_option('ppar_digistore24_marketplace_v1', array());
        $existing_store = is_array($existing_store) ? $existing_store : array();
        $existing_items = array();
        foreach ((array)($existing_store['items'] ?? array()) as $item) {
            if (!is_array($item) || empty($item['id'])) { continue; }
            $existing_items[(string)$item['id']] = $item;
        }
        $new_ids = array_fill_keys(array_keys($groups), true);
        $items = array();
        $removed_manual = 0;
        foreach ($existing_items as $entry_id=>$item) {
            if ((string)($item['source_kind'] ?? '') === 'digistore24_manual_csv' && !isset($new_ids[$entry_id])) { $removed_manual++; continue; }
            if ((string)($item['source_kind'] ?? '') !== 'digistore24_manual_csv' && !isset($new_ids[$entry_id])) { $items[$entry_id] = $item; }
        }
        foreach ($groups as $entry_id=>$group) {
            $old = $existing_items[$entry_id] ?? array();
            $product_ids = array_values($group['product_ids']); sort($product_ids, SORT_STRING);
            $products = $group['products']; ksort($products, SORT_STRING);
            $headline = count($product_ids) === 1 ? (string)reset($products) : (string)$group['vendor'] . ' · ' . count($product_ids) . ' Produkte';
            $description_parts = array();
            foreach ($products as $pid=>$title) { $description_parts[] = $pid . ' · ' . $title; }
            $support = (string)($group['support_url'] ?? '');
            if ($support === '' && !empty($old['support_url']) && filter_var($old['support_url'], FILTER_VALIDATE_URL) && stripos((string)$old['support_url'], 'https://') === 0) { $support = (string)$old['support_url']; }
            $promolink = (string)($group['promolink'] ?? '');
            if ($promolink === '' && !empty($old['promolink']) && filter_var($old['promolink'], FILTER_VALIDATE_URL) && stripos((string)$old['promolink'], 'https://') === 0) { $promolink = (string)$old['promolink']; }
            $items[$entry_id] = array(
                'id'=>(string)$entry_id,
                'main_product_id'=>(string)$product_ids[0],
                'all_product_ids'=>$product_ids,
                'approval_status'=>'approved',
                'approval_status_msg'=>'Genehmigt · manueller Digistore24-CSV-Import',
                'headline'=>$headline,
                'description'=>implode("\n", $description_parts),
                'product_category'=>'',
                'product_category_id'=>0,
                'affiliate_share'=>null,
                'stats_stars'=>null,
                'stats_count_orders'=>0,
                'vendor'=>(string)$group['vendor'],
                'commissions'=>$group['commissions'],
                'support_url'=>$support,
                'promolink'=>$promolink,
                'source_kind'=>'digistore24_manual_csv',
                'manual_import_sha256'=>$sha,
                'manual_imported_at'=>$now,
            );
        }
        ksort($items, SORT_STRING);

        $partnerships = get_option('ppar_digistore24_partnerships_v1', array());
        $partnerships = is_array($partnerships) ? $partnerships : array();
        foreach ($partnerships as $entry_id=>$record) {
            if (is_array($record) && (string)($record['source'] ?? '') === 'manual_csv' && !isset($new_ids[(string)$entry_id])) { unset($partnerships[$entry_id]); }
        }
        foreach ($groups as $entry_id=>$group) {
            $old = is_array($partnerships[$entry_id] ?? null) ? $partnerships[$entry_id] : array();
            $product_ids = array_values($group['product_ids']); sort($product_ids, SORT_STRING);
            $partnerships[$entry_id] = array(
                'confirmed'=>1,
                'confirmed_at'=>absint($old['confirmed_at'] ?? 0) ?: $now,
                'key_fingerprint'=>(string)$identity['key_fingerprint'],
                'affiliate_id'=>(string)$identity['affiliate_id'],
                'source'=>'manual_csv',
                'approval_status'=>'approved',
                'product_ids'=>$product_ids,
                'vendor'=>(string)$group['vendor'],
                'products'=>$group['products'],
                'commissions'=>$group['commissions'],
                'imported_at'=>$now,
                'import_sha256'=>$sha,
            );
        }

        $inventory = array(
            'rows'=>$parsed['rows'],
            'product_count'=>count($parsed['rows']),
            'source_count'=>count($groups),
            'vendors'=>array_values(array_unique(array_map(static function($row){ return (string)$row['vendor']; }, array_values($parsed['rows'])))),
            'blocked'=>absint($parsed['blocked'] ?? 0),
            'imported_at'=>$now,
            'sha256'=>$sha,
            'key_fingerprint'=>(string)$identity['key_fingerprint'],
            'affiliate_id'=>(string)$identity['affiliate_id'],
        );
        sort($inventory['vendors'], SORT_NATURAL | SORT_FLAG_CASE);
        $store = array_merge($existing_store, array(
            'items'=>array_values($items),
            'last_checked'=>$now,
            'last_status'=>'manual_import',
            'last_message'=>count($parsed['rows']) . ' genehmigte Produktpartnerschaften aus Digistore24-CSV übernommen; ' . count($groups) . ' Werbemittelquellen; ' . count($inventory['vendors']) . ' Vendoren.',
            'blocked'=>absint($parsed['blocked'] ?? 0),
            'key_fingerprint'=>(string)$identity['key_fingerprint'],
            'affiliate_id'=>(string)$identity['affiliate_id'],
        ));

        // Alle Strukturen sind vollständig validiert, bevor die erste persistente
        // Mutation erfolgt. Der alte LKG-/Output-Bestand wird hier nicht angefasst.
        update_option(self::DS24_INVENTORY_OPTION, $inventory, false);
        update_option('ppar_digistore24_marketplace_v1', $store, false);
        update_option('ppar_digistore24_partnerships_v1', $partnerships, false);

        $message = 'Digistore24 erkannt · ' . count($parsed['rows']) . ' genehmigte Produktpartnerschaften · ' . count($groups) . ' Werbemittelquellen · ' . count($inventory['vendors']) . ' Vendoren';
        if (!empty($parsed['blocked'])) { $message .= ' · ' . absint($parsed['blocked']) . ' nicht genehmigte/ungültige Zeilen blockiert'; }
        if ($removed_manual > 0) { $message .= ' · ' . $removed_manual . ' alte manuelle Quelle(n) aus der Inventur entfernt'; }
        $message .= '. Bestehende veröffentlichte LKG-Ausgaben wurden nicht verändert.';
        return array('status'=>'success','message'=>$message,'sha256'=>$sha,'product_count'=>count($parsed['rows']),'source_count'=>count($groups),'vendor_count'=>count($inventory['vendors']));
    }

    private static function delegate_idealo($file) {
        if (!class_exists('Pferdeportal_Affiliate_Router')) { self::redirect('failed', 'Affiliate-Router ist nicht geladen.'); }
        $_FILES['idealo_feed'] = $file;
        $_POST['ppar_idealo_nonce'] = wp_create_nonce('ppar_idealo_import_file');
        $_REQUEST['ppar_idealo_nonce'] = $_POST['ppar_idealo_nonce'];
        Pferdeportal_Affiliate_Router::instance()->handle_idealo_import_file();
        exit;
    }

    private static function delegate_creative_library($file, $provider, $name) {
        if (!class_exists('Pferdeportal_Affiliate_Router')) { self::redirect('failed', 'Affiliate-Router ist nicht geladen.'); }
        $provider = sanitize_key((string)$provider);
        $hash = is_readable((string)$file['tmp_name']) ? hash_file('sha256', (string)$file['tmp_name']) : '';
        $_FILES['creative_file'] = $file;
        $_POST['provider'] = $provider;
        $_POST['partner_external_id'] = 'manual-' . substr((string)$hash, 0, 20);
        $_POST['partner_name'] = ucfirst($provider) . ' · Dateiimport ' . sanitize_file_name((string)$name);
        $_POST['creative_codes'] = '';
        $_POST['ppar_creative_library_nonce'] = wp_create_nonce('ppar_creative_library_import');
        $_REQUEST['ppar_creative_library_nonce'] = $_POST['ppar_creative_library_nonce'];
        Pferdeportal_Affiliate_Router::instance()->handle_creative_library_import();
        exit;
    }

    private static function remember($provider, $message, $sha) {
        update_option(self::LAST_OPTION, array(
            'provider'=>sanitize_text_field((string)$provider),
            'message'=>sanitize_text_field((string)$message),
            'sha256'=>preg_replace('/[^a-f0-9]/', '', strtolower((string)$sha)),
            'imported_at'=>time(),
        ), false);
    }

    private static function redirect($status, $message) {
        $args = array(
            'page'=>'affiliate-portal-kiss-providers',
            'ppar_universal_import'=>sanitize_key((string)$status),
            'ppar_universal_message'=>rawurlencode(sanitize_text_field((string)$message)),
        );
        wp_safe_redirect(add_query_arg($args, admin_url('admin.php')));
        exit;
    }
}
