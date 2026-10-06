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
    if (strpos($url, '/affiliate/program/export') !== false) {
        return $reply(wp_json_encode(array(
            'status'=>200,
            'data'=>array(
                'items'=>array(array(
                    'programId'=>123,
                    'programName'=>'procavallo',
                    'affiliateStatus'=>'accepted',
                    'isActive'=>1,
                    'promotionCounts'=>array('banner'=>1),
                )),
                'total'=>array('totalItems'=>1),
            ),
        )));
    }
    if (strpos($url, '/affiliate/promotion/getPromotionTypeBanner') !== false) {
        return $reply(wp_json_encode(array(
            'status'=>200,
            'data'=>array(
                'items'=>array(array(
                    'programId'=>123,
                    'promotionId'=>393923,
                    'promotionCategoryId'=>77,
                    'clickoutLink'=>'https://t.adcell.com/p/click-schabracken',
                    'bannerUrl'=>'https://t.adcell.com/p/banner-schabracken',
                    'width'=>728,
                    'height'=>90,
                    'information'=>'Individueller Schabracken Designer',
                    'customNested'=>array('theme'=>'schabracken','source'=>'provider'),
                )),
                'total'=>array('numberItems'=>1),
            ),
        )));
    }
    if (strpos($url, '/affiliate/promotion/getPromotionCategories') !== false) {
        return $reply(wp_json_encode(array(
            'status'=>200,
            'data'=>array(
                'items'=>array(array(
                    'programId'=>123,
                    'promotionCategoryId'=>77,
                    'promotionCategoryName'=>'Schabracken',
                )),
                'total'=>array('numberItems'=>1),
            ),
        )));
    }
    if (strpos($url, '/affiliate/promotion/getPromotionTypeCsv') !== false
        || strpos($url, '/affiliate/promotion/getPromotionTypeDeeplink') !== false) {
        return $reply(wp_json_encode(array(
            'status'=>200,
            'data'=>array('items'=>array(),'total'=>array('numberItems'=>0)),
        )));
    }
    if (strpos($url, 'https://t.adcell.com/p/') === 0) {
        return $reply('', 200);
    }
    return new WP_Error('unexpected_http', 'Unexpected HTTP in test: ' . $method . ' ' . $url);
}, 10, 3);

$o = Pferdeportal_Affiliate_Router::instance();

foreach (array('maybe_install_automation_schema','maybe_install_creative_library_schema','maybe_install_output_objects_schema') as $method_name) {
    if (!method_exists($o, $method_name)) {
        $fail('missing_schema_method_' . $method_name);
    }
    $m = new ReflectionMethod($o, $method_name);
    $m->setAccessible(true);
    $m->invoke($o);
}

// Simuliere einen realistischen 6.72.198-Altbestand: gleiche Banner-ID,
// aber nur die grobe Kategorie "Ausrüstung" und ohne erhaltene Provider-Rohdaten.
$old_row = array(
    'creative_id'=>'banner-393923',
    'creative_type'=>'banner',
    'creative_title'=>'procavallo Banner 393923 – Ausrüstung',
    'creative_description'=>'Werbemittelkategorie: Ausrüstung',
    'creative_tag'=>'ADCELL Banner | Ausrüstung',
    'promotion_category_id'=>77,
    'promotion_category_name'=>'Ausrüstung',
    'provider_topic_id'=>'77',
    'provider_topic_name'=>'Ausrüstung',
    'provider_topic_source'=>'provider_promotion_category',
    'image_source'=>'https://t.adcell.com/p/banner-schabracken',
    'destination_url'=>'https://t.adcell.com/p/click-schabracken',
    'tracking_url'=>'https://t.adcell.com/p/click-schabracken',
    '_destination_source'=>'tracking_checked',
    'width'=>728,
    'height'=>90,
    'status'=>'active',
    '_source_kind'=>'banner',
    '_run_uuid'=>'old-v672198-run',
);
$detect = new ReflectionMethod($o, 'creative_library_detect_mapping');
$detect->setAccessible(true);
$mapping = $detect->invoke($o, array_keys($old_row));
$normalize = new ReflectionMethod($o, 'creative_library_normalize_row');
$normalize->setAccessible(true);
$old = $normalize->invoke($o, $old_row, $mapping, array(
    'provider'=>'adcell',
    'partner_external_id'=>'123',
    'partner_name'=>'procavallo',
    'source_kind'=>'banner',
    'run_uuid'=>'old-v672198-run',
));
if (is_wp_error($old)) {
    $fail('old_normalize_' . $old->get_error_message());
}
$upsert = new ReflectionMethod($o, 'creative_library_upsert');
$upsert->setAccessible(true);
if ($upsert->invoke($o, $old) !== 'imported') {
    $fail('old_row_not_seeded');
}
$ok('old_672198_banner_seeded');

delete_option('ppar_v672199_adcell_banner_basis_state');
delete_option('ppar_v672199_adcell_banner_basis_result');
foreach (array('state','cursor','result','reset_done') as $suffix) {
    delete_option('ppar_v672199_banner_reconcile_' . $suffix);
}

$upgrade = new ReflectionMethod($o, 'run_v672199_adcell_banner_basis_resync');
$upgrade->setAccessible(true);
$upgrade->invoke($o);
if ((string)get_option('ppar_v672199_adcell_banner_basis_state','') !== 'waiting_jobs') {
    $fail('fresh_resync_not_queued_' . (string)get_option('ppar_v672199_adcell_banner_basis_state',''));
}
$ok('fresh_672199_resync_queued');

for ($i=0; $i<12; $i++) {
    $worker_result = $o->run_automation_worker(true, 'adcell');
    if (is_wp_error($worker_result)) {
        $fail('worker_' . $worker_result->get_error_code() . '_' . $worker_result->get_error_message());
    }
    $has_open = new ReflectionMethod($o, 'automation_has_open_jobs');
    $has_open->setAccessible(true);
    if (!$has_open->invoke($o, 'adcell')) {
        break;
    }
}
$has_open = new ReflectionMethod($o, 'automation_has_open_jobs');
$has_open->setAccessible(true);
if ($has_open->invoke($o, 'adcell')) {
    $fail('adcell_jobs_not_finished');
}
$ok('fresh_672199_adcell_job_completed');

$upgrade->invoke($o);
if ((string)get_option('ppar_v672199_adcell_banner_basis_state','') !== 'done') {
    // Ein grosser Reconcile kann mehrere Batches brauchen; im Fixture ist es
    // nur ein Banner. Ein zweiter direkter Aufruf deckt trotzdem den
    // Fortsetzungsvertrag ab.
    $upgrade->invoke($o);
}
if ((string)get_option('ppar_v672199_adcell_banner_basis_state','') !== 'done') {
    $fail('basis_upgrade_not_done_' . (string)get_option('ppar_v672199_adcell_banner_basis_state',''));
}
$ok('basis_upgrade_completed_after_fresh_import');

$table_method = new ReflectionMethod($o, 'creative_library_table');
$table_method->setAccessible(true);
$table = $table_method->invoke($o);
global $wpdb;
$stored = $wpdb->get_row($wpdb->prepare(
    "SELECT * FROM {$table} WHERE provider='adcell' AND partner_external_id='123' AND external_id=%s",
    'banner-393923'
), ARRAY_A);
if (!is_array($stored)) {
    $fail('updated_banner_missing');
}
$payload = json_decode((string)($stored['payload'] ?? ''), true);
if (!is_array($payload)) {
    $fail('updated_payload_invalid');
}
if ((string)($payload['promotion_category_name'] ?? '') !== 'Schabracken'
    || (string)($payload['provider_topic_name'] ?? '') !== 'Schabracken') {
    $fail('old_broad_category_not_replaced');
}
$raw_json = (string)($payload['_provider_raw_json'] ?? '');
$raw_sha = (string)($payload['_provider_raw_sha256'] ?? '');
if ($raw_json === '' || !hash_equals(hash('sha256', $raw_json), $raw_sha)) {
    $fail('provider_raw_not_persisted_after_upgrade');
}
$raw = json_decode($raw_json, true);
if ((string)($raw['customNested']['theme'] ?? '') !== 'schabracken') {
    $fail('provider_nested_raw_missing_after_upgrade');
}
$ok('old_banner_replaced_with_complete_current_provider_evidence');

$category_calls = array_values(array_filter($http_calls, static function($line) {
    return strpos($line, '/affiliate/promotion/getPromotionCategories') !== false;
}));
if (count($category_calls) !== 1) {
    $fail('category_endpoint_not_once_' . count($category_calls));
}
$ok('category_endpoint_once_for_fresh_programme_run');

echo "ADCELL_BANNER_BASIS_UPGRADE_V672199_E2E_COMPLETE\n";
