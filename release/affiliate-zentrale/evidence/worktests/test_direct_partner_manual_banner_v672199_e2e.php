<?php
if (!class_exists('Pferdeportal_Affiliate_Router')) {
    fwrite(STDERR, "FAIL plugin_not_loaded\n");
    exit(2);
}
if (Pferdeportal_Affiliate_Router::VERSION !== '6.72.199') {
    fwrite(STDERR, "FAIL wrong_version " . Pferdeportal_Affiliate_Router::VERSION . "\n");
    exit(2);
}
$fail = static function($message) {
    fwrite(STDERR, "FAIL " . $message . "\n");
    exit(1);
};
$ok = static function($message) {
    echo "PASS " . $message . "\n";
};
$o = Pferdeportal_Affiliate_Router::instance();

$snapshots_m = new ReflectionMethod($o, 'creative_library_snapshots_for_select');
$snapshots_m->setAccessible(true);
$snapshots = $snapshots_m->invoke($o);
if (($snapshots['direct:tarifcheck']['name'] ?? '') !== 'Tarifcheck') {
    $fail('tarifcheck_preset_missing');
}
if (($snapshots['direct:check24']['name'] ?? '') !== 'CHECK24') {
    $fail('check24_preset_missing');
}
$ok('tarifcheck_and_check24_direct_partner_presets');

$manual_m = new ReflectionMethod($o, 'creative_library_manual_banner_row');
$manual_m->setAccessible(true);
$manual = $manual_m->invoke($o, array(
    'manual_banner_external_id'=>'check24-test-01',
    'manual_banner_title'=>'CHECK24 Testbanner',
    'manual_banner_image_url'=>'https://cdn.example.test/check24-banner.png',
    'manual_banner_tracking_url'=>'https://tracking.example.test/check24',
    'manual_banner_destination_url'=>'https://www.check24.de/',
    'manual_banner_description'=>'Manuell hinterlegter Testbanner',
    'manual_banner_tags'=>'CHECK24',
    'manual_banner_width'=>728,
    'manual_banner_height'=>90,
));
if (is_wp_error($manual)) {
    $fail('manual_row_' . $manual->get_error_code());
}
if (($manual['creative_id'] ?? '') !== 'check24-test-01'
    || ($manual['tracking_url'] ?? '') !== 'https://tracking.example.test/check24'
    || ($manual['destination_url'] ?? '') !== 'https://www.check24.de/') {
    $fail('manual_row_fields');
}
$ok('manual_banner_row_built');

$invalid = $manual_m->invoke($o, array(
    'manual_banner_image_url'=>'https://cdn.example.test/check24-banner.png',
    'manual_banner_tracking_url'=>'',
));
if (!is_wp_error($invalid) || $invalid->get_error_code() !== 'manual_banner_tracking') {
    $fail('manual_missing_tracking_not_blocked');
}
$ok('manual_banner_missing_tracking_fails_closed');

$install = new ReflectionMethod($o, 'maybe_install_creative_library_schema');
$install->setAccessible(true);
$install->invoke($o);
$detect = new ReflectionMethod($o, 'creative_library_detect_mapping');
$detect->setAccessible(true);
$mapping = $detect->invoke($o, array_keys($manual));
$normalize = new ReflectionMethod($o, 'creative_library_normalize_row');
$normalize->setAccessible(true);
$creative = $normalize->invoke($o, $manual, $mapping, array(
    'provider'=>'direct',
    'partner_external_id'=>'check24',
    'partner_name'=>'CHECK24',
    'source_kind'=>'manual_banner',
    'run_uuid'=>'manual-check24-test',
));
if (is_wp_error($creative)) {
    $fail('manual_normalize_' . $creative->get_error_code());
}
$upsert = new ReflectionMethod($o, 'creative_library_upsert');
$upsert->setAccessible(true);
$result = $upsert->invoke($o, $creative);
if (!in_array($result, array('imported','updated','unchanged'), true)) {
    $fail('manual_upsert_' . $result);
}
$table_m = new ReflectionMethod($o, 'creative_library_table');
$table_m->setAccessible(true);
$table = $table_m->invoke($o);
global $wpdb;
$stored = $wpdb->get_row($wpdb->prepare(
    "SELECT * FROM {$table} WHERE provider='direct' AND partner_external_id='check24' AND external_id=%s",
    'check24-test-01'
), ARRAY_A);
if (!is_array($stored)
    || ($stored['partner_name'] ?? '') !== 'CHECK24'
    || ($stored['creative_type'] ?? '') !== 'banner') {
    $fail('manual_check24_not_stored');
}
$ok('manual_check24_banner_stored_in_creative_library');

$source = (string) file_get_contents(dirname(__DIR__, 2) . '/current/affiliate-portal-router/includes/trait-ppar-creative-library.php');
foreach (array('value="direct:tarifcheck"', 'value="direct:check24"', 'Banner händisch einfügen', 'name="manual_banner_image_url"', 'name="manual_banner_tracking_url"') as $needle) {
    if (strpos($source, $needle) === false) {
        $fail('ui_missing_' . md5($needle));
    }
}
$ok('backend_ui_contains_tarifcheck_check24_and_manual_banner_form');
echo "DIRECT_PARTNER_MANUAL_BANNER_V672199_E2E_COMPLETE\n";
