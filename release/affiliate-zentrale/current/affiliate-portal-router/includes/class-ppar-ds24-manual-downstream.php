<?php
if (!defined('ABSPATH')) { exit; }

/**
 * Bridges an already validated manual Digistore24 partnership inventory into the
 * existing banner/output pipeline. It does not discover partnerships and does
 * not duplicate the provider's banner/parser/output logic.
 */
final class PPAR_DS24_Manual_Downstream {
    const INVENTORY_OPTION = 'ppar_digistore24_manual_inventory_v1';
    const STATUS_OPTION = 'ppar_digistore24_manual_downstream_v1';
    private static $booted = false;
    private static $running = false;

    public static function bootstrap() {
        if (self::$booted) { return; }
        self::$booted = true;
        // The CSV importer writes marketplace + partnerships first and affiliations last.
        // Start only after the final affiliation write, never on the earlier inventory write.
        add_action('update_option_ppar_digistore24_affiliations_v1', array(__CLASS__, 'on_affiliations_update'), 20, 3);
        add_action('add_option_ppar_digistore24_affiliations_v1', array(__CLASS__, 'on_affiliations_add'), 20, 2);
        add_action('admin_notices', array(__CLASS__, 'render_notice'));
    }

    public static function on_affiliations_add($option, $value) {
        self::run_after_affiliations($value);
    }

    public static function on_affiliations_update($old_value, $value, $option = '') {
        self::run_after_affiliations($value);
    }

    private static function run_after_affiliations($affiliations) {
        if (self::$running || !is_array($affiliations)) { return; }
        if (!class_exists('Pferdeportal_Affiliate_Router')) { return; }
        $inventory = get_option(self::INVENTORY_OPTION, array());
        if (!is_array($inventory) || empty($inventory['rows']) || !is_array($inventory['rows'])) { return; }
        if (!self::affiliations_match_inventory($affiliations, $inventory)) { return; }

        $groups = self::group_sources($inventory['rows']);
        if (!$groups) { return; }
        $groups = self::merge_cached_support_urls($groups);

        self::$running = true;
        $status = array(
            'inventory_sha256' => preg_replace('/[^a-f0-9]/', '', strtolower((string)($inventory['sha256'] ?? ''))),
            'started_at' => time(),
            'finished_at' => 0,
            'sources_total' => count($groups),
            'sources_processed' => 0,
            'sources_imported' => 0,
            'sources_needing_support_url' => 0,
            'sources_failed' => 0,
            'creatives_found' => 0,
            'creatives_imported' => 0,
            'creatives_blocked' => 0,
            'errors' => array(),
            'status' => 'running',
        );

        try {
            $router = Pferdeportal_Affiliate_Router::instance();
            $method = new ReflectionMethod($router, 'digistore24_import_vendor_banners');
            $method->setAccessible(true);

            foreach ($groups as $entry_id => $group) {
                $support_url = (string)($group['support_url'] ?? '');
                if (!self::is_https_url($support_url)) {
                    $status['sources_needing_support_url']++;
                    continue;
                }

                $status['sources_processed']++;
                try {
                    // false = use the manual-partnership gate already populated by
                    // the CSV import; do not invoke automatic partnership discovery.
                    $result = $method->invoke($router, (string)$entry_id, $support_url, false);
                    if (is_wp_error($result)) {
                        $status['sources_failed']++;
                        $status['errors'][(string)$entry_id] = sanitize_text_field($result->get_error_message());
                        continue;
                    }
                    $status['sources_imported']++;
                    $status['creatives_found'] += absint($result['found'] ?? 0);
                    $status['creatives_imported'] += absint($result['imported'] ?? 0);
                    $status['creatives_blocked'] += absint($result['blocked'] ?? 0);
                } catch (Throwable $e) {
                    $status['sources_failed']++;
                    $status['errors'][(string)$entry_id] = sanitize_text_field($e->getMessage());
                }
            }

            self::restore_manual_marketplace_facts($inventory);
            $status['status'] = $status['sources_failed'] > 0
                ? 'partial'
                : ($status['sources_needing_support_url'] > 0 ? 'partial' : 'complete');
        } catch (Throwable $e) {
            $status['status'] = 'failed';
            $status['errors']['bridge'] = sanitize_text_field($e->getMessage());
        }

        $status['finished_at'] = time();
        update_option(self::STATUS_OPTION, $status, false);
        self::$running = false;
    }

    private static function affiliations_match_inventory($affiliations, $inventory) {
        $sha = preg_replace('/[^a-f0-9]/', '', strtolower((string)($inventory['sha256'] ?? '')));
        if ($sha === '') { return false; }
        $expected = array();
        foreach ((array)$inventory['rows'] as $row) {
            if (!is_array($row)) { continue; }
            $product_id = preg_replace('/[^0-9]/', '', (string)($row['product_id'] ?? ''));
            if ($product_id !== '') { $expected[$product_id] = true; }
        }
        if (!$expected) { return false; }
        foreach ($expected as $product_id => $_) {
            $proof = is_array($affiliations[$product_id] ?? null) ? $affiliations[$product_id] : array();
            if ((string)($proof['source'] ?? '') !== 'manual_csv') { return false; }
            if (!hash_equals($sha, preg_replace('/[^a-f0-9]/', '', strtolower((string)($proof['import_sha256'] ?? ''))))) { return false; }
            if ((string)($proof['approval_status'] ?? '') !== 'approved' || empty($proof['product_is_active'])) { return false; }
        }
        return true;
    }

    private static function merge_cached_support_urls($groups) {
        $store = get_option('ppar_digistore24_marketplace_v1', array());
        $store = is_array($store) ? $store : array();
        foreach ((array)($store['items'] ?? array()) as $item) {
            if (!is_array($item)) { continue; }
            $entry_id = preg_replace('/[^0-9]/', '', (string)($item['id'] ?? ''));
            if ($entry_id === '' || !isset($groups[$entry_id]) || self::is_https_url($groups[$entry_id]['support_url'] ?? '')) { continue; }
            $support_url = trim((string)($item['support_url'] ?? ''));
            if (self::is_https_url($support_url)) { $groups[$entry_id]['support_url'] = esc_url_raw($support_url); }
        }
        return $groups;
    }

    private static function restore_manual_marketplace_facts($inventory) {
        $store = get_option('ppar_digistore24_marketplace_v1', array());
        if (!is_array($store)) { return; }
        $rows_by_entry = array();
        foreach ((array)($inventory['rows'] ?? array()) as $row) {
            if (!is_array($row)) { continue; }
            $entry_id = preg_replace('/[^0-9]/', '', (string)($row['entry_id'] ?? ''));
            $product_id = preg_replace('/[^0-9]/', '', (string)($row['product_id'] ?? ''));
            if ($entry_id === '' || $product_id === '') { continue; }
            if (!isset($rows_by_entry[$entry_id])) {
                $rows_by_entry[$entry_id] = array('product_ids'=>array(),'vendor'=>(string)($row['vendor'] ?? ''),'commissions'=>array(),'support_url'=>'','promolink'=>'');
            }
            $rows_by_entry[$entry_id]['product_ids'][$product_id] = $product_id;
            $rows_by_entry[$entry_id]['commissions'][$product_id] = (string)($row['commission'] ?? '');
            if ($rows_by_entry[$entry_id]['support_url'] === '' && self::is_https_url($row['support_url'] ?? '')) { $rows_by_entry[$entry_id]['support_url'] = esc_url_raw((string)$row['support_url']); }
            if ($rows_by_entry[$entry_id]['promolink'] === '' && self::is_https_url($row['promolink'] ?? '')) { $rows_by_entry[$entry_id]['promolink'] = esc_url_raw((string)$row['promolink']); }
        }
        if (empty($store['items']) || !is_array($store['items'])) { return; }
        $changed = false;
        foreach ($store['items'] as &$item) {
            if (!is_array($item)) { continue; }
            $entry_id = preg_replace('/[^0-9]/', '', (string)($item['id'] ?? ''));
            if ($entry_id === '' || !isset($rows_by_entry[$entry_id])) { continue; }
            $facts = $rows_by_entry[$entry_id];
            $product_ids = array_values($facts['product_ids']); sort($product_ids, SORT_STRING);
            $item['source_kind'] = 'digistore24_manual_csv';
            $item['manual_import_sha256'] = preg_replace('/[^a-f0-9]/', '', strtolower((string)($inventory['sha256'] ?? '')));
            $item['manual_imported_at'] = absint($inventory['imported_at'] ?? 0);
            $item['all_product_ids'] = $product_ids;
            if ((string)($item['main_product_id'] ?? '') === '' && $product_ids) { $item['main_product_id'] = (string)$product_ids[0]; }
            $item['vendor'] = (string)$facts['vendor'];
            $item['commissions'] = $facts['commissions'];
            $item['approval_status'] = 'approved';
            $item['approval_status_msg'] = 'Genehmigt · manueller Digistore24-CSV-Import';
            if (self::is_https_url($facts['support_url'])) { $item['support_url'] = $facts['support_url']; }
            if (self::is_https_url($facts['promolink'])) { $item['promolink'] = $facts['promolink']; }
            $changed = true;
        }
        unset($item);
        if ($changed) { update_option('ppar_digistore24_marketplace_v1', $store, false); }
    }

    private static function group_sources($rows) {
        $groups = array();
        foreach ((array)$rows as $row) {
            if (!is_array($row)) { continue; }
            $entry_id = preg_replace('/[^0-9]/', '', (string)($row['entry_id'] ?? ''));
            if ($entry_id === '') { continue; }
            if (!isset($groups[$entry_id])) {
                $groups[$entry_id] = array('support_url' => '');
            }
            $support_url = trim((string)($row['support_url'] ?? ''));
            if ($groups[$entry_id]['support_url'] === '' && self::is_https_url($support_url)) {
                $groups[$entry_id]['support_url'] = esc_url_raw($support_url);
            }
        }
        ksort($groups, SORT_STRING);
        return $groups;
    }

    private static function is_https_url($url) {
        $url = trim((string)$url);
        if ($url === '' || !filter_var($url, FILTER_VALIDATE_URL)) { return false; }
        return strtolower((string)parse_url($url, PHP_URL_SCHEME)) === 'https';
    }

    public static function render_notice() {
        if (!current_user_can('manage_options')) { return; }
        if (empty($_GET['page']) || sanitize_key((string)$_GET['page']) !== 'affiliate-portal-kiss-providers') { return; }
        $status = get_option(self::STATUS_OPTION, array());
        if (!is_array($status) || empty($status['finished_at'])) { return; }

        $class = (string)($status['status'] ?? '') === 'complete' ? 'notice-success' : 'notice-warning';
        $message = 'Digistore24-Weiterverarbeitung: '
            . absint($status['sources_imported'] ?? 0) . '/' . absint($status['sources_total'] ?? 0) . ' Werbemittelquellen verarbeitet; '
            . absint($status['creatives_imported'] ?? 0) . ' echte Banner importiert.';
        if (!empty($status['sources_needing_support_url'])) {
            $message .= ' ' . absint($status['sources_needing_support_url']) . ' Quelle(n) enthalten keine nutzbare Werbemittelseite und bleiben einzeln offen.';
        }
        if (!empty($status['sources_failed'])) {
            $message .= ' ' . absint($status['sources_failed']) . ' Quelle(n) sind einzeln fehlgeschlagen; andere Quellen wurden weiterverarbeitet.';
        }
        echo '<div class="notice ' . esc_attr($class) . ' is-dismissible"><p>' . esc_html($message) . '</p></div>';
    }
}
