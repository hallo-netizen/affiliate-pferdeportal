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

$provider_banner_fixture = array(
    'programId'=>123,
    'promotionId'=>393923,
    'promotionCategoryId'=>77,
    'clickoutLink'=>'https://t.adcell.com/p/click-schabracken',
    'bannerUrl'=>'https://t.adcell.com/p/banner-schabracken',
    'width'=>728,
    'height'=>90,
    'information'=>'Individueller Schabracken Designer',
    'customNested'=>array(
        'theme'=>'schabracken',
        'source'=>'provider',
        'flags'=>array(true, false, null),
        'limits'=>array('min'=>0, 'max'=>'12.50'),
    ),
    'futureUnknown'=>array(
        'deep'=>array(
            'list'=>array(
                array('x'=>1, 'enabled'=>true),
                array('x'=>2, 'enabled'=>false),
            ),
        ),
    ),
);
$http_calls = array();
add_filter('pre_http_request', function($pre, $args, $url) use (&$http_calls, $provider_banner_fixture) {
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
                    $provider_banner_fixture,
                    array(
                        'programId'=>123,
                        'promotionId'=>393924,
                        'promotionCategoryId'=>77,
                        'bannerName'=>'Original Provider Bannername',
                        'clickoutLink'=>'https://t.adcell.com/p/click-resolve-schabracken',
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
    if ($url === 'https://t.adcell.com/p/click-resolve-schabracken') {
        return $reply('', 302, array(
            'location'=>'https://shop.example.test/schabracken/',
        ));
    }
    if ($url === 'https://shop.example.test/schabracken/') {
        return $reply('', 200);
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

$raw_json = (string)($first['provider_raw_json'] ?? '');
$expected_raw_json = wp_json_encode($provider_banner_fixture, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
$raw = json_decode($raw_json, true);
if (!is_array($raw)
    || $raw !== $provider_banner_fixture
    || $raw_json !== $expected_raw_json) {
    $fail('raw_provider_payload_not_value_and_type_identical');
}
if (!hash_equals(hash('sha256', $raw_json), (string)($first['provider_raw_sha256'] ?? ''))) {
    $fail('raw_provider_payload_hash_mismatch');
}
$ok('full_provider_payload_value_and_type_identical_with_hash');

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

// Reales eindeutiges Portalziel bereitstellen, damit die Reihenfolge
// "Assetprüfung VOR Zielkarte" wirklich beobachtbar ist.
$schabracken_term = get_term_by('slug', 'schabracken', 'category');
if (!$schabracken_term || is_wp_error($schabracken_term)) {
    $made = wp_insert_term('Schabracken', 'category', array('slug'=>'schabracken'));
    if (is_wp_error($made)) {
        $fail('schabracken_target_fixture_' . $made->get_error_code());
    }
    $schabracken_id = (int)$made['term_id'];
} else {
    $schabracken_id = (int)$schabracken_term->term_id;
}
if ($schabracken_id <= 0) {
    $fail('schabracken_target_fixture_missing');
}
$ok('real_schabracken_target_fixture_ready');

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

$resolved_stored = $wpdb->get_row($wpdb->prepare(
    "SELECT * FROM {$table} WHERE provider='adcell' AND partner_external_id='123' AND external_id=%s",
    'banner-393924'
), ARRAY_A);
$resolved_payload = json_decode((string)($resolved_stored['payload'] ?? ''), true);
if (!is_array($resolved_stored)
    || !is_array($resolved_payload)
    || (string)($resolved_stored['tracking_url'] ?? '') !== 'https://t.adcell.com/p/click-resolve-schabracken'
    || (string)($resolved_stored['destination_url'] ?? '') !== 'https://shop.example.test/schabracken/'
    || sanitize_key((string)($resolved_payload['_destination_source'] ?? '')) !== 'resolved_redirect') {
    $fail('real_destination_redirect_and_provenance_not_persisted');
}
$resolved_targets_before = json_decode((string)($resolved_stored['topic_targets'] ?? ''), true);
if (is_array($resolved_targets_before) && count($resolved_targets_before) !== 0) {
    $fail('resolved_destination_created_target_before_asset_verification');
}
$ok('tracking_redirect_resolved_once_and_real_destination_provenance_persisted');

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
$targets_before_verify = json_decode((string)($stored['topic_targets'] ?? ''), true);
$targets_before_verify = is_array($targets_before_verify) ? $targets_before_verify : array();
if (count($targets_before_verify) !== 0
    || !in_array(sanitize_key((string)($stored_payload['_dimension_state'] ?? '')), array('', 'pending'), true)) {
    $fail('target_created_before_asset_verification');
}
$ok('no_target_before_real_asset_verification');

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
if (!is_array($stored_raw)
    || $stored_raw !== $provider_banner_fixture
    || (string)$stored_payload['_provider_raw_json'] !== $expected_raw_json) {
    $fail('stored_full_provider_object_changed_or_lost');
}
$ok('full_provider_payload_reaches_library_value_and_type_identical');

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

$targets_after_verify = json_decode((string)($stored_after['topic_targets'] ?? ''), true);
$targets_after_verify = is_array($targets_after_verify) ? array_values(array_filter($targets_after_verify, 'is_array')) : array();
$target_keys_after_verify = array_values(array_map(static function($target) {
    return (string)($target['target_key'] ?? '');
}, $targets_after_verify));
if (!in_array('category:' . $schabracken_id, $target_keys_after_verify, true)) {
    $fail('schabracken_target_missing_after_asset_verification');
}
$target_sources_after_verify = array_values(array_unique(array_filter(array_map(static function($target) {
    return sanitize_key((string)($target['source'] ?? ''));
}, $targets_after_verify))));
if (!in_array('banner_provider_topic_exact', $target_sources_after_verify, true)) {
    $fail('provider_topic_exact_source_missing_after_verification');
}
$ok('asset_verification_precedes_exact_schabracken_target_assignment');

// Ein technischer Fehler bleibt innerhalb des Laufs terminal. Ein SPAETERER
// echter Provider-Reimport desselben unveraenderten Banners muss den Assetcheck
// aber erneut oeffnen; sonst waere ein temporaerer Bildfehler dauerhaft.
$failed_payload = $payload_after;
$failed_payload['_dimension_state'] = 'failed';
$failed_payload['_dimension_error'] = 'temporary provider image failure';
$failed_payload['_image_sha256'] = '';
$failed_payload['_image_mime'] = '';
$failed_payload['_image_bytes'] = 0;
$failed_payload['_measured_at'] = time();
$wpdb->update($table, array(
    'width'=>0,
    'height'=>0,
    'topic_status'=>'format_blocked',
    'topic_score'=>0,
    'topic_targets'=>wp_json_encode(array(array(
        'portal_key'=>'stale',
        'state'=>'mapped',
        'target_key'=>'category:' . $schabracken_id,
        'source'=>'stale_should_be_removed',
    ))),
    'classified_at'=>time(),
    'payload'=>wp_json_encode($failed_payload, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES),
), array('id'=>(int)$stored_after['id']));

$retry_counts = $import->invoke($o, $rows, array(
    'provider'=>'adcell',
    'partner_external_id'=>'123',
    'partner_name'=>'procavallo',
    'source_kind'=>'banner',
    'run_uuid'=>'basis-run-later-reimport',
));
if ((int)($retry_counts['updated'] ?? 0) < 1) {
    $fail('failed_asset_same_source_reimport_not_marked_updated_' . wp_json_encode($retry_counts));
}
$retry_row = $wpdb->get_row($wpdb->prepare(
    "SELECT * FROM {$table} WHERE provider='adcell' AND partner_external_id='123' AND external_id=%s",
    'banner-393923'
), ARRAY_A);
$retry_payload = json_decode((string)($retry_row['payload'] ?? ''), true);
$retry_targets = json_decode((string)($retry_row['topic_targets'] ?? ''), true);
if (!is_array($retry_payload)
    || sanitize_key((string)($retry_payload['_dimension_state'] ?? '')) !== 'pending'
    || (string)($retry_payload['_dimension_error'] ?? '') !== ''
    || (int)($retry_row['width'] ?? 0) !== 0
    || (int)($retry_row['height'] ?? 0) !== 0
    || sanitize_key((string)($retry_row['topic_status'] ?? '')) !== 'format_pending'
    || (is_array($retry_targets) && count($retry_targets) !== 0)) {
    $fail('failed_asset_not_reopened_pending_fail_closed_on_fresh_reimport');
}
$ok('fresh_provider_reimport_reopens_failed_asset_without_restoring_targets');

$verified_retry = $verify->invoke($o, $retry_row, true, false);
if (is_wp_error($verified_retry)) {
    $fail('retry_asset_verification_' . $verified_retry->get_error_code());
}
$retry_after = $wpdb->get_row($wpdb->prepare(
    "SELECT * FROM {$table} WHERE provider='adcell' AND partner_external_id='123' AND external_id=%s",
    'banner-393923'
), ARRAY_A);
$retry_after_targets = json_decode((string)($retry_after['topic_targets'] ?? ''), true);
$retry_after_keys = is_array($retry_after_targets) ? array_values(array_map(static function($target) {
    return (string)($target['target_key'] ?? '');
}, array_filter($retry_after_targets, 'is_array'))) : array();
if (!in_array('category:' . $schabracken_id, $retry_after_keys, true)) {
    $fail('reopened_asset_not_remapped_after_successful_retry_verification');
}
$ok('reopened_asset_maps_again_only_after_successful_retry_verification');

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
