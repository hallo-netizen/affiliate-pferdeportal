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
        add_action('update_option_' . self::INVENTORY_OPTION, array(__CLASS__, 'on_inventory_update'), 20, 3);
        add_action('admin_notices', array(__CLASS__, 'render_notice'));
    }

    public static function on_inventory_update($old_value, $value, $option = '') {
        if (self::$running || !is_array($value) || empty($value['rows']) || !is_array($value['rows'])) { return; }
        if (!class_exists('Pferdeportal_Affiliate_Router')) { return; }

        $groups = self::group_sources($value['rows']);
        if (!$groups) { return; }

        self::$running = true;
        $status = array(
            'inventory_sha256' => preg_replace('/[^a-f0-9]/', '', strtolower((string)($value['sha256'] ?? ''))),
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
