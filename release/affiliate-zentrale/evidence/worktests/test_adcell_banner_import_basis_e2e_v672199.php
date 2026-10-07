<?php
if (!class_exists('Pferdeportal_Affiliate_Router')) {
    fwrite(STDERR, "FAIL plugin_not_loaded\n");
    exit(2);
}

update_option('ppar_network_adcell_v1', array(
    'enabled'=>true,
    'username'=>'basis-user',
    'password'=>'basis-password',
), false);
update_option('ppar_adcell_program_id_allowlist_v1', array(123), false);

$http_calls = array();
add_filter('pre_http_request', function($pre, $args, $url) use (&$http_calls) {
    $method = strtoupper((string)($args['method'] ?? 'GET'));
    $http_calls[] = $method . ' ' . $url;

    $reply = static function($body, $code=200, $headers=array()) {
        return array(
            'headers'=>$headers,
            'body'=>$body,
            'response'=>array('code'=>$code,'message'=>'OK'),
            'cookies'=>array(),
            'filename'=>null,
        );
    };

    if (strpos($url, 'api.adcell.org/api/v2/user/getToken') !== false) {
        return $reply(wp_json_encode(array('data'=>array('token'=>'basis-token-123456789'))));
    }
    if (strpos($url, 'api.adcell.org/api/v2/affiliate/promotion/getPromotionTypeBanner') !== false) {
        return $reply(wp_json_encode(array(
            'status'=>200,
            'data'=>array(
                'items'=>array(
                    array(
                        'programId'=>123,
                        'promotionId'=>393923,
                        'promotionCategoryId'=>77,
                        'clickoutLink'=>'https://t.adcell.com/p/click-schabracken',
                        'bannerUrl'=>'https://t.adcell.com/p/banner-schabracken',
                        'width'=>728,
                        'height'=>90,
                        'information'=>'Individueller Schabracken Designer',
                        'customNested'=>array('theme'=>'schabracken','source'=>'provider'),
                    ),
                    array(
                        'programId'=>123,
                        'promotionId'=>393924,
                        'promotionCategoryId'=>77,
                        'bannerName'=>'Original Provider Bannername',
                        'clickoutLink'=>'https://t.adcell.com/p/click-schabracken-2',
                        'bannerUrl'=>'https://t.adcell.com/p/banner-schabracken-2',
                        'width'=>300,
                        'height'=>250,
                        'information'=>'Zweites Werbemittel',
                    ),
                ),
                'total'=>array('numberItems'=>2),
            ),
        )));
    }
    if (strpos($url, 'api.adcell.org/api/v2/affiliate/promotion/getPromotionCategories') !== false) {
        return $reply(wp_json_encode(array(
            'status'=>200,
            'data'=>array(
                'items'=>array(
                    array(
                        'programId'=>123,
                        'promotionCategoryId'=>77,
                        'promotionCategoryName'=>'Schabracken',
                    ),
                ),
                'total'=>array('numberItems'=>1),
            ),
        )));
    }
    if (strpos($url, 'https://t.adcell.com/p/') === 0) {
        return $reply('', 200);
    }
    return new WP_Error('unexpected_http', 'Unexpected HTTP in test: ' . $method . ' ' . $url);
}, 10, 3);

$o = Pferdeportal_Affiliate_Router::instance();

// Testisolation: derselbe WordPress/MariaDB-Harness darf die Gates in beliebiger
// Reihenfolge und wiederholt ausführen.
$install = new ReflectionMethod($o, 'maybe_install_creative_library_schema');
$install->setAccessible(true);
$install->invoke($o);
$table_method = new ReflectionMethod($o, 'creative_library_table');
$table_method->setAccessible(true);
$table = $table_method->invoke($o);
global $wpdb;
$wpdb->query($wpdb->prepare(
    "DELETE FROM {$table} WHERE provider='adcell' AND partner_external_id=%s",
    '123'
));

$m = new ReflectionMethod($o, 'automation_adcell_banner_rows');
$m->setAccessible(true);
$result = $m->invoke($o, 123, 'procavallo', 'basis-run');

$fail = static function($message) {
    fwrite(STDERR, "FAIL " . $message . "\n");
    exit(1);
};
$ok = static function($message) {
    echo "PASS " . $message . "\n";
};

if (is_wp_error($result)) {
    $fail('banner_rows_wp_error ' . $result->get_error_code() . ' ' . $result->get_error_message());
}
$rows = (array)($result['rows'] ?? array());
if (count($rows) !== 2) {
    $fail('row_count ' . count($rows));
}

$first = $rows[0];
if ((string)($first['promotion_category_name'] ?? '') !== 'Schabracken') {
    $fail('category_name_not_resolved');
}
$ok('category_id_resolved_to_Schabracken');

if ((string)($first['provider_topic_name'] ?? '') !== 'Schabracken'
    || (string)($first['provider_topic_source'] ?? '') !== 'provider_promotion_category') {
    $fail('provider_topic_not_bound');
}
$ok('resolved_category_becomes_provider_topic');

if ((string)($first['creative_title'] ?? 'x') !== ''
    || (string)($first['title_source'] ?? '') !== 'provider_missing') {
    $fail('missing_provider_title_was_invented');
}
$ok('no_synthetic_provider_title');

$raw = json_decode((string)($first['provider_raw_json'] ?? ''), true);
if (!is_array($raw)
    || (int)($raw['promotionId'] ?? 0) !== 393923
    || (string)($raw['information'] ?? '') !== 'Individueller Schabracken Designer'
    || (string)($raw['customNested']['theme'] ?? '') !== 'schabracken') {
    $fail('raw_provider_payload_not_preserved');
}
if (!hash_equals(hash('sha256', (string)$first['provider_raw_json']), (string)($first['provider_raw_sha256'] ?? ''))) {
    $fail('raw_provider_payload_hash_mismatch');
}
$ok('full_provider_payload_preserved_with_hash');

$second = $rows[1];
if ((string)($second['creative_title'] ?? '') !== 'Original Provider Bannername'
    || (string)($second['title_source'] ?? '') !== 'provider_bannername') {
    $fail('provider_banner_name_not_preserved');
}
$ok('real_provider_banner_name_preserved');

// Fail-closed: ein ADCELL-Banner darf ohne belastbaren Rohdatensatz oder mit
// manipuliertem SHA nicht einmal normalisiert/importiert werden.
$detect = new ReflectionMethod($o, 'creative_library_detect_mapping');
$detect->setAccessible(true);
$normalize = new ReflectionMethod($o, 'creative_library_normalize_row');
$normalize->setAccessible(true);
$tampered = $first;
$tampered['provider_raw_sha256'] = str_repeat('0', 64);
$mapping = $detect->invoke($o, array_keys($tampered));
$bad = $normalize->invoke($o, $tampered, $mapping, array(
    'provider'=>'adcell',
    'partner_external_id'=>'123',
    'partner_name'=>'procavallo',
    'source_kind'=>'banner',
    'run_uuid'=>'basis-run-tampered',
));
if (!is_wp_error($bad) || $bad->get_error_code() !== 'creative_import_provider_raw') {
    $fail('tampered_provider_raw_not_blocked');
}
$missing = $first;
unset($missing['provider_raw_json'], $missing['provider_raw_sha256']);
$mapping = $detect->invoke($o, array_keys($missing));
$bad = $normalize->invoke($o, $missing, $mapping, array(
    'provider'=>'adcell',
    'partner_external_id'=>'123',
    'partner_name'=>'procavallo',
    'source_kind'=>'banner',
    'run_uuid'=>'basis-run-missing',
));
if (!is_wp_error($bad) || $bad->get_error_code() !== 'creative_import_provider_raw') {
    $fail('missing_provider_raw_not_blocked');
}
$ok('missing_or_tampered_provider_raw_fails_closed');

$category_calls = array_values(array_filter($http_calls, static function($line) {
    return strpos($line, '/affiliate/promotion/getPromotionCategories') !== false;
}));
if (count($category_calls) !== 1) {
    $fail('category_endpoint_call_count_' . count($category_calls));
}
$ok('category_endpoint_called_once_per_programme');

// Jetzt derselbe Datensatz durch den echten Bibliotheks-Import bis in MariaDB.
$import = new ReflectionMethod($o, 'automation_import_rows');
$import->setAccessible(true);
$counts = $import->invoke($o, $rows, array(
    'provider'=>'adcell',
    'partner_external_id'=>'123',
    'partner_name'=>'procavallo',
    'source_kind'=>'banner',
    'run_uuid'=>'basis-run',
));
if ((int)($counts['imported'] ?? 0) !== 2) {
    $fail('library_import_count_' . wp_json_encode($counts));
}

$stored = $wpdb->get_row($wpdb->prepare(
    "SELECT * FROM {$table} WHERE provider='adcell' AND partner_external_id='123' AND external_id=%s",
    'banner-393923'
), ARRAY_A);
if (!is_array($stored)) {
    $fail('stored_banner_missing');
}
$stored_payload = json_decode((string)($stored['payload'] ?? ''), true);
if (!is_array($stored_payload)) {
    $fail('stored_payload_invalid');
}
if ((string)($stored_payload['promotion_category_name'] ?? '') !== 'Schabracken') {
    $fail('stored_category_name_missing');
}
if ((string)($stored_payload['provider_topic_name'] ?? '') !== 'Schabracken') {
    $fail('stored_provider_topic_missing');
}
if ((string)($stored_payload['title_source'] ?? '') !== 'provider_missing') {
    $fail('stored_title_provenance_missing');
}
if ((string)($stored['tracking_url'] ?? '') !== 'https://t.adcell.com/p/click-schabracken'
    || (string)($stored['destination_url'] ?? '') !== 'https://t.adcell.com/p/click-schabracken'
    || (string)($stored_payload['_destination_source'] ?? '') !== 'tracking_checked') {
    $fail('stored_destination_provenance_missing');
}
if ((string)($stored['image_url'] ?? '') !== 'https://t.adcell.com/p/banner-schabracken'
    || (int)($stored_payload['_declared_width'] ?? 0) !== 728
    || (int)($stored_payload['_declared_height'] ?? 0) !== 90) {
    $fail('stored_image_or_declared_dimensions_missing');
}
if ((string)($stored_payload['information'] ?? '') !== 'Individueller Schabracken Designer'
    || (int)($stored_payload['promotion_category_id'] ?? 0) !== 77) {
    $fail('stored_provider_fields_missing');
}
$ok('tracking_destination_provenance_image_and_provider_fields_preserved');

if ((string)($stored_payload['_provider_raw_json'] ?? '') !== (string)$first['provider_raw_json']) {
    $fail('stored_raw_json_changed');
}
if ((string)($stored_payload['_provider_raw_sha256'] ?? '') !== (string)$first['provider_raw_sha256']) {
    $fail('stored_raw_sha_changed');
}
if (!hash_equals(
    hash('sha256', (string)$stored_payload['_provider_raw_json']),
    (string)$stored_payload['_provider_raw_sha256']
)) {
    $fail('stored_raw_integrity_failed');
}
$stored_raw = json_decode((string)$stored_payload['_provider_raw_json'], true);
if ((string)($stored_raw['customNested']['theme'] ?? '') !== 'schabracken') {
    $fail('stored_nested_raw_lost');
}
$ok('full_provider_payload_reaches_library_unchanged');

// Technische Bildprüfung: reales Bildbytes-Fixture erzwingt gemessene 1x1 Pixel.
// Providerangaben 728x90 bleiben als deklarierte Werte erhalten und werden als
// Mismatch sichtbar, statt stillschweigend als verifiziert zu gelten.
add_filter('pre_http_request', function($pre, $args, $url) {
    if ($url === 'https://t.adcell.com/p/banner-schabracken') {
        $png = base64_decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAusB9Wl+0iAAAAAASUVORK5CYII=');
        return array(
            'headers'=>array('content-type'=>'image/png','content-length'=>strlen($png)),
            'body'=>$png,
            'response'=>array('code'=>200,'message'=>'OK'),
            'cookies'=>array(),
            'filename'=>null,
        );
    }
    return $pre;
}, 20, 3);
$verify = new ReflectionMethod($o, 'creative_library_verify_asset_row');
$verify->setAccessible(true);
$verified = $verify->invoke($o, $stored, true, false);
if (is_wp_error($verified)) {
    $fail('asset_verification_' . $verified->get_error_code());
}
$stored_after = $wpdb->get_row($wpdb->prepare(
    "SELECT * FROM {$table} WHERE provider='adcell' AND partner_external_id='123' AND external_id=%s",
    'banner-393923'
), ARRAY_A);
$payload_after = json_decode((string)($stored_after['payload'] ?? ''), true);
if ((int)($stored_after['width'] ?? 0) !== 1
    || (int)($stored_after['height'] ?? 0) !== 1
    || (string)($payload_after['_dimension_state'] ?? '') !== 'mismatch'
    || (string)($payload_after['_image_sha256'] ?? '') === '') {
    $fail('real_asset_measurement_not_persisted');
}
$ok('real_asset_bytes_dimensions_and_mismatch_persisted');

// Negativfall: Kategorienbasis nicht erreichbar -> kompletter Bannerimport
// fail-closed, kein Raten aus Titel oder Altmetadaten.
add_filter('pre_http_request', function($pre, $args, $url) {
    if (strpos($url, '/affiliate/promotion/getPromotionCategories') !== false) {
        return new WP_Error('category_fixture_down', 'category endpoint unavailable');
    }
    return $pre;
}, 30, 3);
$blocked_basis = $m->invoke($o, 123, 'procavallo', 'basis-run-category-down');
if (!is_wp_error($blocked_basis) || $blocked_basis->get_error_code() !== 'adcell_promotion_categories_unavailable') {
    $fail('category_basis_failure_not_fail_closed');
}
$ok('category_basis_failure_fails_closed');

echo "ADCELL_BANNER_IMPORT_BASIS_E2E_COMPLETE\n";
