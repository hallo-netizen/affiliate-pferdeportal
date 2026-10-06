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

$category_calls = array_values(array_filter($http_calls, static function($line) {
    return strpos($line, '/affiliate/promotion/getPromotionCategories') !== false;
}));
if (count($category_calls) !== 1) {
    $fail('category_endpoint_call_count_' . count($category_calls));
}
$ok('category_endpoint_called_once_per_programme');

echo "ADCELL_BANNER_IMPORT_BASIS_E2E_COMPLETE\n";
