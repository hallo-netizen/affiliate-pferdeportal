<?php
/**
 * ADCELL API-v2 bound regression gate.
 * Static/source-level gate only; live API and WordPress/MariaDB E2E remain separate.
 */

$files = array(
    'main' => __DIR__ . '/pferdeportal-affiliate-router.php',
    'registry' => __DIR__ . '/trait-ppar-provider-registry.php',
    'automation' => __DIR__ . '/trait-ppar-automation-suite.php',
    'sync' => __DIR__ . '/trait-ppar-network-sync.php',
);

$errors = array();
$src = array();
foreach ($files as $key => $file) {
    if (!is_file($file)) {
        $errors[] = 'missing:' . $key;
        continue;
    }
    $src[$key] = (string) file_get_contents($file);
}

$mustContain = static function ($key, $needle, $label) use (&$errors, &$src) {
    if (!isset($src[$key]) || strpos($src[$key], $needle) === false) {
        $errors[] = 'missing_contract:' . $label;
    }
};
$mustNotContain = static function ($key, $needle, $label) use (&$errors, &$src) {
    if (isset($src[$key]) && strpos($src[$key], $needle) !== false) {
        $errors[] = 'forbidden_contract:' . $label;
    }
};

// AF-060: exact official ADCELL API-v2 auth contract.
$mustContain('sync', 'https://api.adcell.org/api/v2/', 'official_api_host');
$mustContain('sync', '/user/getToken', 'token_endpoint');
$mustContain('sync', "'userName'", 'token_username_parameter');
$mustContain('sync', "'password'", 'token_password_parameter');
$mustContain('sync', "'token'", 'request_token_parameter');
$mustContain('sync', 'adcell_api_v2_token', 'token_helper');
$mustContain('sync', 'adcell_api_v2_request', 'request_helper');
$mustNotContain('main', 'https://www.adcell.de/api/v2/', 'legacy_www_api_base');

if (isset($src['main']) && preg_match('/private function test_adcell_connection\s*\([^)]*\)\s*\{(.*?)\n\s*\}/s', $src['main'], $m)) {
    if (stripos($m[1], 'Authorization') !== false && stripos($m[1], 'Basic') !== false) {
        $errors[] = 'forbidden_contract:adcell_basic_auth';
    }
} else {
    $errors[] = 'missing_contract:test_adcell_connection';
}

// Official read-only/program/promotion API-v2 paths.
$mustContain('sync', '/affiliate/program/export', 'program_export');
$mustContain('sync', '/affiliate/promotion/getPromotionTypeCsv', 'promotion_csv');
$mustContain('sync', '/affiliate/promotion/getPromotionTypeBanner', 'promotion_banner');
$mustContain('sync', '/affiliate/promotion/getPromotionTypeDeeplink', 'promotion_deeplink');

// accepted + active + explicit programId allowlist, fail closed.
$mustContain('sync', 'program_id_allowlist', 'program_id_allowlist_setting');
$mustContain('sync', 'affiliateStatus', 'accepted_status_gate');
$mustContain('sync', 'isActive', 'active_program_gate');
$mustContain('automation', 'automation_enqueue_adcell_program', 'per_program_queue');
$mustNotContain('automation', "'partner_external_id' => 'csv-feed'", 'legacy_csv_feed_source');
$mustNotContain('automation', "'partner_external_id'=>'csv-feed'", 'legacy_csv_feed_job');

// AF-059: manual ADCELL CSV URL is not the normal automation prerequisite anymore.
$mustNotContain('automation', 'ADCELL-CSV-Lauf starten', 'legacy_csv_run_button');
$mustNotContain('automation', 'Exakte CSV-Export-URL fehlt.', 'legacy_csv_missing_message');
$mustNotContain('registry', 'ADCELL-CSV-Export-URL', 'legacy_csv_registry_field');

// AF-058: ADCELL automation must route before Awin rendering/dispatch.
$mustContain('automation', 'render_adcell_automation_page', 'adcell_specific_page');
$mustContain('automation', "if ($requested_provider === 'adcell')", 'adcell_early_route');
$mustContain('automation', "return $this->automation_enqueue_adcell_program", 'adcell_program_dispatch');

if ($errors) {
    fwrite(STDERR, "ADCELL_API_V2_GATE_FAIL\n" . implode("\n", $errors) . "\n");
    exit(1);
}

echo "ADCELL_API_V2_GATE_PASS\n";
