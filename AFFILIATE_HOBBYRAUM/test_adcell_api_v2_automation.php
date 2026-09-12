<?php
/**
 * ADCELL API-v2 bound regression gate.
 * Static/source-level gate only; live API and WordPress/MariaDB E2E remain separate.
 */

$files = array(
    'registry' => __DIR__ . '/trait-ppar-provider-registry.php',
    'automation' => __DIR__ . '/trait-ppar-automation-suite.php',
    'sync' => __DIR__ . '/trait-ppar-network-sync.php',
);
$errors = array();
$src = array();
foreach ($files as $key => $file) {
    if (!is_file($file)) { $errors[] = 'missing:' . $key; continue; }
    $src[$key] = (string) file_get_contents($file);
}
$mustContain = static function ($key, $needle, $label) use (&$errors, &$src) {
    if (!isset($src[$key]) || strpos($src[$key], $needle) === false) { $errors[] = 'missing_contract:' . $label; }
};
$mustNotContain = static function ($key, $needle, $label) use (&$errors, &$src) {
    if (isset($src[$key]) && strpos($src[$key], $needle) !== false) { $errors[] = 'forbidden_contract:' . $label; }
};

$mustContain('sync', 'https://api.adcell.org/api/v2/', 'official_api_host');
$mustContain('sync', '/user/getToken', 'token_endpoint');
$mustContain('sync', "'userName'", 'token_username_parameter');
$mustContain('sync', "'password'", 'token_password_parameter');
$mustContain('sync', "'token'", 'request_token_parameter');
$mustContain('sync', 'adcell_api_v2_token', 'token_helper');
$mustContain('sync', 'adcell_api_v2_request', 'request_helper');
$mustContain('sync', 'adcell_api_v2_test_connection', 'connection_test_helper');
$mustNotContain('sync', "Authorization'=>'Basic", 'basic_auth_sync');
$mustNotContain('registry', '$this->test_adcell_connection()', 'legacy_basic_test_route');
$mustContain('registry', '$this->adcell_api_v2_test_connection()', 'official_test_route');
$mustContain('sync', '/affiliate/program/export', 'program_export');
$mustContain('sync', '/affiliate/promotion/getPromotionTypeCsv', 'promotion_csv');
$mustContain('sync', '/affiliate/promotion/getPromotionTypeBanner', 'promotion_banner');
$mustContain('sync', '/affiliate/promotion/getPromotionTypeDeeplink', 'promotion_deeplink');
$mustContain('sync', 'program_id_allowlist', 'program_id_allowlist_setting');
$mustContain('sync', 'affiliateStatus', 'accepted_status_gate');
$mustContain('sync', 'isActive', 'active_program_gate');
$mustContain('sync', 'adcell_api_v2_allowlisted_programmes', 'allowlisted_programmes_helper');
$mustContain('automation', 'automation_enqueue_adcell_program', 'per_program_queue');
$mustContain('automation', 'adcell_api_v2_promotion_items', 'api_promotion_source');
$mustContain('automation', 'automation_download_adcell_feed_url', 'api_csv_download');
$mustNotContain('automation', "partner_external_id'=>'csv-feed'", 'legacy_csv_feed_job');
$mustNotContain('automation', "partner_external_id' => 'csv-feed'", 'legacy_csv_feed_source');
$mustNotContain('automation', 'ADCELL-CSV-Lauf starten', 'legacy_csv_run_button');
$mustNotContain('automation', 'Exakte CSV-Export-URL fehlt.', 'legacy_csv_missing_message');
$mustNotContain('registry', 'ADCELL-CSV-Export-URL', 'legacy_csv_registry_field');
$mustContain('automation', 'render_adcell_automation_page', 'adcell_specific_page');
$mustContain('automation', '$requested_provider === \'adcell\'', 'adcell_early_route');
$mustContain('automation', 'return $this->automation_enqueue_adcell_program', 'adcell_program_dispatch');
$mustContain('automation', 'automation_adcell_banner_rows', 'banner_ingestion');
$mustContain('automation', 'automation_adcell_deeplink_rows', 'deeplink_ingestion');

if ($errors) {
    fwrite(STDERR, "ADCELL_API_V2_GATE_FAIL\n" . implode("\n", $errors) . "\n");
    exit(1);
}
echo "ADCELL_API_V2_GATE_PASS\n";
