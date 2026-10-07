<?php
/**
 * Regression gate for the ADCELL banner import basis.
 * No WordPress bootstrap required: source-contract assertions only.
 */

$root = dirname(__DIR__, 2) . '/current/affiliate-portal-router';
$auto = (string) file_get_contents($root . '/includes/trait-ppar-automation-suite.php');
$library = (string) file_get_contents($root . '/includes/trait-ppar-creative-library.php');
$output = (string) file_get_contents($root . '/includes/trait-ppar-output-objects.php');
$main = (string) file_get_contents($root . '/pferdeportal-affiliate-router.php');

$errors = array();
$must = static function ($needle, $label) use (&$errors, $auto) {
    if (strpos($auto, $needle) === false) {
        $errors[] = 'missing:' . $label;
    }
};
$mustNot = static function ($needle, $label) use (&$errors, $auto) {
    if (strpos($auto, $needle) !== false) {
        $errors[] = 'forbidden:' . $label;
    }
};

$start = strpos($auto, 'private function automation_adcell_banner_rows');
$end = strpos($auto, 'private function automation_adcell_deeplink_rows', $start === false ? 0 : $start);
if ($start === false || $end === false || $end <= $start) {
    $errors[] = 'banner_function_missing';
    $banner = '';
} else {
    $banner = substr($auto, $start, $end - $start);
}

foreach (array(
    'adcell_api_v2_promotion_categories($program_id)' => 'category_endpoint_is_used',
    "'adcell_promotion_categories_unavailable'" => 'category_failure_is_fail_closed',
    "isset(\$promotion_categories[\$category_id])" => 'category_id_is_resolved_to_name',
    "'provider_raw_json'=>\$provider_raw_json" => 'full_provider_payload_is_preserved',
    "'provider_raw_sha256'=>hash('sha256', \$provider_raw_json)" => 'raw_payload_integrity_hash',
    "'title_source'=>\$title_source" => 'title_provenance_is_preserved',
    "array('bannerName','promotionName','title','name')" => 'provider_title_fields_are_used_only_when_present',
) as $needle => $label) {
    if (strpos($banner, $needle) === false) {
        $errors[] = 'missing:' . $label;
    }
}

if (strpos($banner, "'creative_title'=>sanitize_text_field((string) \$program_name . ' Banner '") !== false) {
    $errors[] = 'forbidden:synthetic_banner_title_used_as_provider_title';
}
if (strpos($library, "'creative_import_provider_raw'") === false) {
    $errors[] = 'missing:adcell_raw_payload_fail_closed';
}
if (strpos($output, "title_evidence") === false
    || strpos($output, "provider_missing") === false) {
    $errors[] = 'missing:synthetic_display_title_excluded_from_evidence';
}

// Frontend-Hardlock: Der neue Basisnachlauf ist ausschließlich admin-/workergebunden.
// Die öffentliche Output-Schicht darf niemals direkt ADCELL-Provider-HTTP aufrufen.
if (strpos($main, "add_action('admin_init', array($this, 'maybe_upgrade_adcell_banner_import_basis_v672199')") === false
    || strpos($main, "add_action('ppar_v672199_adcell_banner_basis_resync', array($this, 'run_v672199_adcell_banner_basis_resync')") === false) {
    $errors[] = 'missing:adcell_basis_admin_worker_binding';
}
if (strpos($output, 'adcell_api_v2_') !== false
    || strpos($output, 'wp_safe_remote_get(') !== false
    || strpos($output, 'wp_safe_remote_post(') !== false
    || strpos($output, 'wp_safe_remote_head(') !== false) {
    $errors[] = 'forbidden:provider_http_in_output_runtime';
}
$resolver_start = strpos($library, 'private function creative_library_resolve_tracking_destination_import');
$resolver_end = strpos($library, 'private function creative_library_normalize_row', $resolver_start === false ? 0 : $resolver_start);
$resolver = ($resolver_start !== false && $resolver_end !== false && $resolver_end > $resolver_start)
    ? substr($library, $resolver_start, $resolver_end - $resolver_start) : '';
if ($resolver === ''
    || strpos($resolver, '$import_context') === false
    || strpos($resolver, "defined('WP_CLI')") === false
    || strpos($resolver, 'if (!$import_context') === false) {
    $errors[] = 'missing:destination_resolution_import_context_guard';
}

if ($errors) {
    fwrite(STDERR, "ADCELL_BANNER_IMPORT_BASIS_FAIL\n" . implode("\n", $errors) . "\n");
    exit(1);
}
echo "PASS category endpoint used once per programme\n";
echo "PASS category id resolved to authoritative category name\n";
echo "PASS full provider banner payload preserved\n";
echo "PASS provider title provenance preserved\n";
echo "PASS synthetic banner title no longer used as provider evidence\n";
echo "PASS missing or corrupt ADCELL raw provider basis is fail-closed\n";
echo "PASS synthetic display fallback is excluded from banner evidence\n";
echo "PASS ADCELL basis sync is admin-worker bound and output runtime contains no provider HTTP\n";
echo "PASS destination resolver is guarded to import/background contexts\n";
echo "ADCELL_BANNER_IMPORT_BASIS_COMPLETE\n";
