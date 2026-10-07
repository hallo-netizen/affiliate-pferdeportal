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
    || ($manual['destination_url'] ?? '') !== 'https://www.check24.de/'
    || ($manual['title_source'] ?? '') !== 'manual_user') {
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

$untitled = $manual_m->invoke($o, array(
    'manual_banner_external_id'=>'check24-test-no-title',
    'manual_banner_image_url'=>'https://cdn.example.test/check24-banner-no-title.png',
    'manual_banner_tracking_url'=>'https://tracking.example.test/check24-no-title',
));
if (is_wp_error($untitled) || ($untitled['title_source'] ?? '') !== 'manual_missing') {
    $fail('manual_missing_title_provenance');
}
$ok('manual_missing_title_marked_non_evidence');

$install = new ReflectionMethod($o, 'maybe_install_creative_library_schema');
$install->setAccessible(true);
$install->invoke($o);
$table_m = new ReflectionMethod($o, 'creative_library_table');
$table_m->setAccessible(true);
$table = $table_m->invoke($o);
global $wpdb;
$wpdb->query($wpdb->prepare(
    "DELETE FROM {$table} WHERE provider='direct' AND partner_external_id=%s",
    'check24'
));
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

$admins = get_users(array('role'=>'administrator','number'=>1));
if (!$admins) {
    $uid = wp_create_user('banner-gate-admin', 'ci-banner-gate-pass!', 'banner-gate@example.test');
    if (is_wp_error($uid)) { $fail('admin_fixture_create'); }
    $user = new WP_User($uid);
    $user->set_role('administrator');
    $admins = array($user);
}
wp_set_current_user(absint($admins[0]->ID));
$_GET = array('page'=>'affiliate-portal-creative-library');
ob_start();
$o->render_creative_library_page();
$html = ob_get_clean();
foreach (array(
    'value="direct:tarifcheck"',
    '>Tarifcheck</option>',
    'value="direct:check24"',
    '>CHECK24</option>',
    'Banner händisch einfügen',
    'name="manual_banner_image_url"',
    'name="manual_banner_tracking_url"',
    'name="manual_banner_destination_url"'
) as $needle) {
    if (strpos($html, $needle) === false) {
        $fail('rendered_ui_missing_' . md5($needle));
    }
}
$ok('rendered_backend_ui_contains_tarifcheck_check24_and_manual_banner_form');
echo "DIRECT_PARTNER_MANUAL_BANNER_V672199_E2E_COMPLETE\n";
