<?php
if (!defined('ABSPATH')) { exit; }

/**
 * Ergänzt den universellen manuellen Dateieingang ohne Providerlogik zu duplizieren.
 * - hält identitätsgebundene DS24-CSV-Inventur über spätere Marketplace-Cache-Updates stabil;
 * - erkennt eindeutige DS24-Werbemitteldateien vor dem generischen Importer und
 *   delegiert sie an die vorhandene Creative-Library;
 * - widersprüchliche Provider-Signaturen werden fail-closed abgewiesen.
 */
final class PPAR_Affiliate_Manual_Import_Guard {
    const ACTION = 'ppar_universal_manual_import';
    const NONCE_ACTION = 'ppar_universal_manual_import';
    const NONCE_FIELD = 'ppar_universal_import_nonce';
    const DS24_INVENTORY_OPTION = 'ppar_digistore24_manual_inventory_v1';
    const DS24_MARKETPLACE_OPTION = 'ppar_digistore24_marketplace_v1';
    const MAX_SAMPLE_BYTES = 1048576;
    private static $booted = false;

    public static function bootstrap() {
        if (self::$booted) { return; }
        self::$booted = true;
        add_action('admin_post_' . self::ACTION, array(__CLASS__, 'maybe_handle_digistore24_creative'), 5);
        add_filter('pre_update_option_' . self::DS24_MARKETPLACE_OPTION, array(__CLASS__, 'preserve_digistore24_manual_inventory'), 20, 3);
    }

    public static function preserve_digistore24_manual_inventory($value, $old_value, $option = '') {
        if (!is_array($value) || !is_array($old_value)) { return $value; }
        $inventory = get_option(self::DS24_INVENTORY_OPTION, array());
        if (!is_array($inventory) || empty($inventory['rows']) || !is_array($inventory['rows'])) { return $value; }

        $inventory_fp = strtolower(trim((string)($inventory['key_fingerprint'] ?? '')));
        $inventory_affiliate = trim((string)($inventory['affiliate_id'] ?? ''));
        $incoming_fp = strtolower(trim((string)($value['key_fingerprint'] ?? '')));
        $incoming_affiliate = trim((string)($value['affiliate_id'] ?? ''));
        if ($inventory_fp === '' || $inventory_affiliate === '' || $incoming_fp === '' || $incoming_affiliate === '') { return $value; }
        if (!hash_equals($inventory_fp, $incoming_fp) || !hash_equals($inventory_affiliate, $incoming_affiliate)) { return $value; }

        $allowed = array();
        foreach ($inventory['rows'] as $row) {
            if (!is_array($row)) { continue; }
            $entry_id = preg_replace('/[^0-9]/', '', (string)($row['entry_id'] ?? ''));
            if ($entry_id !== '') { $allowed[$entry_id] = true; }
        }
        if (!$allowed) { return $value; }

        $incoming = array();
        foreach ((array)($value['items'] ?? array()) as $item) {
            if (!is_array($item) || empty($item['id'])) { continue; }
            $incoming[(string)$item['id']] = $item;
        }
        foreach ((array)($old_value['items'] ?? array()) as $item) {
            if (!is_array($item) || empty($item['id'])) { continue; }
            $entry_id = (string)$item['id'];
            if ((string)($item['source_kind'] ?? '') !== 'digistore24_manual_csv') { continue; }
            if (!isset($allowed[$entry_id]) || isset($incoming[$entry_id])) { continue; }
            $incoming[$entry_id] = $item;
        }
        if ($incoming) {
            ksort($incoming, SORT_STRING);
            $value['items'] = array_values($incoming);
        }
        return $value;
    }

    public static function maybe_handle_digistore24_creative() {
        if (!current_user_can('manage_options')) { return; }
        if (empty($_FILES['affiliate_import_file']) || !is_array($_FILES['affiliate_import_file'])) { return; }
        $file = $_FILES['affiliate_import_file'];
        if ((int)($file['error'] ?? UPLOAD_ERR_NO_FILE) !== UPLOAD_ERR_OK || empty($file['tmp_name']) || !is_uploaded_file($file['tmp_name'])) { return; }
        $name = sanitize_file_name((string)($file['name'] ?? ''));
        if (!preg_match('/\.(?:csv|json|txt)$/i', $name)) { return; }
        $sample = (string)@file_get_contents((string)$file['tmp_name'], false, null, 0, self::MAX_SAMPLE_BYTES);
        if ($sample === '') { return; }
        $lower = strtolower($sample);
        $ds24 = (strpos($lower, 'checkout-ds24.com') !== false || strpos($lower, 'digistore24.com') !== false)
            && (strpos($lower, '<img') !== false || preg_match('/(?:banner_url|image_url|image_source|tracking_url|affiliate_url|click_url)/i', $sample));
        if (!$ds24) { return; }

        $other = strpos($lower, 'awin1.com') !== false || strpos($lower, 'zenaps.com') !== false
            || strpos($lower, 'adcell.de') !== false || strpos($lower, 't.adcell.com') !== false;
        if ($other) {
            self::redirect_failed('Datei enthält widersprüchliche Provider-Signaturen und wird nicht geraten.');
        }

        check_admin_referer(self::NONCE_ACTION, self::NONCE_FIELD);
        if (!class_exists('Pferdeportal_Affiliate_Router')) {
            self::redirect_failed('Affiliate-Router ist nicht geladen.');
        }
        $hash = hash_file('sha256', (string)$file['tmp_name']);
        $_FILES['creative_file'] = $file;
        $_POST['provider'] = 'digistore24';
        $_POST['partner_external_id'] = 'manual-' . substr((string)$hash, 0, 20);
        $_POST['partner_name'] = 'Digistore24 · Dateiimport ' . $name;
        $_POST['creative_codes'] = '';
        $_POST['ppar_creative_library_nonce'] = wp_create_nonce('ppar_creative_library_import');
        $_REQUEST['ppar_creative_library_nonce'] = $_POST['ppar_creative_library_nonce'];
        Pferdeportal_Affiliate_Router::instance()->handle_creative_library_import();
        exit;
    }

    private static function redirect_failed($message) {
        wp_safe_redirect(add_query_arg(array(
            'page' => 'affiliate-portal-kiss-providers',
            'ppar_universal_import' => 'failed',
            'ppar_universal_message' => rawurlencode(sanitize_text_field((string)$message)),
        ), admin_url('admin.php')));
        exit;
    }
}
