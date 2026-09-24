<?php
/*
 * Performance Block A runtime reuse gate.
 * Loaded as MU plugin in the isolated WordPress/MariaDB hardtest only.
 */
if (!defined('ABSPATH')) { exit; }

function ppar_perf_reflect($object, $method) {
    $m = new ReflectionMethod($object, $method);
    $m->setAccessible(true);
    return $m;
}

function ppar_perf_campaign_fixture() {
    $post_id = wp_insert_post(array(
        'post_type' => 'ap_campaign',
        'post_status' => 'publish',
        'post_title' => 'Performance Fixture',
        'post_name' => 'performance-fixture',
    ), true);
    if (is_wp_error($post_id) || !$post_id) {
        throw new RuntimeException('fixture post create failed');
    }
    update_post_meta($post_id, 'ppar_campaign_data', array(
        'id' => ' Performance Fixture ',
        'active' => true,
        'network' => ' MANUAL ',
        'creative_type' => ' PRODUCT ',
        'render_mode' => ' IMAGE_LINK ',
        'programme_status' => ' ACTIVE ',
        'assignment_mode' => ' PAGE_TREE ',
        'placements' => array(' CATEGORY_PRODUCT_1 ', ' category_product_2 '),
        'page_id' => 123,
        'match_slugs' => array(' PferdeSaettel '),
        'automation_target_keys' => array('category:pferdesaettel'),
        'title' => 'Testprodukt',
        'image_url' => 'https://example.test/product.jpg',
        'url' => 'https://example.test/product',
        'health_check_enabled' => false,
    ));
    return (int)$post_id;
}

function ppar_perf_front_gate() {
    $router = Pferdeportal_Affiliate_Router::instance();
    if ((string)Pferdeportal_Affiliate_Router::VERSION !== '6.72.153') {
        throw new RuntimeException('wrong candidate version');
    }

    $post_id = ppar_perf_campaign_fixture();
    $from_post = ppar_perf_reflect($router, 'campaign_from_post');
    $slot_allowed = ppar_perf_reflect($router, 'campaign_slot_allowed');
    $complete = ppar_perf_reflect($router, 'campaign_is_complete');
    $slot_rule = ppar_perf_reflect($router, 'runtime_contract_slot_rule');

    $campaign = $from_post->invoke($router, get_post($post_id));
    if (!is_array($campaign) || empty($campaign['_ppar_runtime_normalized'])) {
        throw new RuntimeException('campaign normalization marker missing');
    }

    $expected = array(
        '_ppar_norm_id' => 'performancefixture',
        '_ppar_norm_network' => 'manual',
        '_ppar_norm_creative_type' => 'product',
        '_ppar_norm_render_mode' => 'image_link',
        '_ppar_norm_programme_status' => 'active',
        '_ppar_norm_assignment_mode' => 'page_tree',
    );
    foreach ($expected as $key => $value) {
        if ((string)($campaign[$key] ?? '') !== $value) {
            throw new RuntimeException('normalized scalar mismatch ' . $key . '=' . (string)($campaign[$key] ?? ''));
        }
    }

    $legacy = $campaign;
    foreach (array_keys($expected) as $key) { unset($legacy[$key]); }
    unset($legacy['_ppar_runtime_normalized'], $legacy['_ppar_runtime_normalized_slot_type']);

    $new = $campaign;
    $new['_ppar_runtime_normalized_slot_type'] = 1;

    foreach (array('category_product_1','category_product_2','post_bottom_products') as $slot) {
        $old_allowed = (bool)$slot_allowed->invoke($router, $legacy, $slot);
        $new_allowed = (bool)$slot_allowed->invoke($router, $new, $slot);
        if ($old_allowed !== $new_allowed) {
            throw new RuntimeException('slot semantic drift ' . $slot);
        }
    }
    if ((bool)$complete->invoke($router, $legacy) !== (bool)$complete->invoke($router, $new)) {
        throw new RuntimeException('campaign completeness semantic drift');
    }

    $GLOBALS['ppar_perf_sanitize_count'] = 0;
    $counter = static function($sanitized, $raw) {
        $GLOBALS['ppar_perf_sanitize_count']++;
        return $sanitized;
    };
    add_filter('sanitize_key', $counter, PHP_INT_MAX, 2);

    $GLOBALS['ppar_perf_sanitize_count'] = 0;
    for ($i=0; $i<500; $i++) {
        $tmp = $campaign;
        unset($tmp['_ppar_runtime_normalized']);
        $tmp['_ppar_norm_id'] = sanitize_key((string)($tmp['id'] ?? ''));
        $tmp['_ppar_norm_network'] = sanitize_key((string)($tmp['network'] ?? 'manual'));
        $tmp['_ppar_norm_creative_type'] = sanitize_key((string)($tmp['creative_type'] ?? 'banner'));
        $tmp['_ppar_norm_render_mode'] = sanitize_key((string)($tmp['render_mode'] ?? 'image_link'));
        $tmp['_ppar_norm_programme_status'] = sanitize_key((string)($tmp['programme_status'] ?? 'unknown'));
        $tmp['_ppar_norm_assignment_mode'] = sanitize_key((string)($tmp['assignment_mode'] ?? 'page_tree'));
    }
    $old_loop_sanitize = (int)$GLOBALS['ppar_perf_sanitize_count'];

    $GLOBALS['ppar_perf_sanitize_count'] = 0;
    for ($i=0; $i<500; $i++) {
        $tmp = $campaign;
        $tmp['_ppar_runtime_normalized_slot_type'] = 1;
        if (empty($tmp['_ppar_runtime_normalized'])) {
            $tmp['_ppar_norm_id'] = sanitize_key((string)($tmp['id'] ?? ''));
            $tmp['_ppar_norm_network'] = sanitize_key((string)($tmp['network'] ?? 'manual'));
            $tmp['_ppar_norm_creative_type'] = sanitize_key((string)($tmp['creative_type'] ?? 'banner'));
            $tmp['_ppar_norm_render_mode'] = sanitize_key((string)($tmp['render_mode'] ?? 'image_link'));
            $tmp['_ppar_norm_programme_status'] = sanitize_key((string)($tmp['programme_status'] ?? 'unknown'));
            $tmp['_ppar_norm_assignment_mode'] = sanitize_key((string)($tmp['assignment_mode'] ?? 'page_tree'));
        }
    }
    $new_loop_sanitize = (int)$GLOBALS['ppar_perf_sanitize_count'];
    remove_filter('sanitize_key', $counter, PHP_INT_MAX);

    if ($old_loop_sanitize !== 3000 || $new_loop_sanitize !== 0) {
        throw new RuntimeException("normalization reduction unexpected old={$old_loop_sanitize} new={$new_loop_sanitize}");
    }

    $GLOBALS['ppar_perf_registry_filter_calls'] = 0;
    $registry_counter = static function($portals) {
        $GLOBALS['ppar_perf_registry_filter_calls']++;
        return $portals;
    };
    add_filter('ppar_affiliate_portal_registry', $registry_counter, PHP_INT_MAX, 1);

    $first = $slot_rule->invoke($router, 'post_inline_banner');
    $calls_after_first = (int)$GLOBALS['ppar_perf_registry_filter_calls'];
    $second = $slot_rule->invoke($router, 'post_inline_banner');
    $calls_after_second = (int)$GLOBALS['ppar_perf_registry_filter_calls'];
    if ($first !== $second || $calls_after_first <= 0 || $calls_after_second !== $calls_after_first) {
        throw new RuntimeException('frontend slot-rule request cache failed');
    }
    $slot_rule->invoke($router, 'journal_banner');
    $calls_after_other_slot = (int)$GLOBALS['ppar_perf_registry_filter_calls'];
    if ($calls_after_other_slot <= $calls_after_second) {
        throw new RuntimeException('slot-rule cache key not slot-specific');
    }
    remove_filter('ppar_affiliate_portal_registry', $registry_counter, PHP_INT_MAX);

    wp_delete_post($post_id, true);

    return array(
        'old_loop_sanitize' => $old_loop_sanitize,
        'new_loop_sanitize' => $new_loop_sanitize,
        'slot_rule_filter_calls_first' => $calls_after_first,
        'slot_rule_filter_calls_second' => $calls_after_second,
        'slot_rule_filter_calls_other_slot' => $calls_after_other_slot,
    );
}

add_action('template_redirect', static function() {
    if ((string)($_GET['ppar_perf_runtime_gate'] ?? '') !== '1') { return; }
    header('Content-Type: application/json; charset=utf-8');
    try {
        $result = ppar_perf_front_gate();
        echo wp_json_encode(array('status'=>'PASS','marker'=>'PPAR_RUNTIME_REUSE_FRONTEND_PASS','result'=>$result));
    } catch (Throwable $e) {
        status_header(500);
        echo wp_json_encode(array('status'=>'FAIL','message'=>$e->getMessage()));
    }
    exit;
}, -1000);

add_action('admin_post_nopriv_ppar_perf_runtime_admin', static function() {
    header('Content-Type: application/json; charset=utf-8');
    try {
        $router = Pferdeportal_Affiliate_Router::instance();
        $slot_rule = ppar_perf_reflect($router, 'runtime_contract_slot_rule');
        $GLOBALS['ppar_perf_registry_filter_calls'] = 0;
        $registry_counter = static function($portals) {
            $GLOBALS['ppar_perf_registry_filter_calls']++;
            return $portals;
        };
        add_filter('ppar_affiliate_portal_registry', $registry_counter, PHP_INT_MAX, 1);
        $slot_rule->invoke($router, 'post_inline_banner');
        $first = (int)$GLOBALS['ppar_perf_registry_filter_calls'];
        $slot_rule->invoke($router, 'post_inline_banner');
        $second = (int)$GLOBALS['ppar_perf_registry_filter_calls'];
        remove_filter('ppar_affiliate_portal_registry', $registry_counter, PHP_INT_MAX);
        if ($first <= 0 || $second <= $first) {
            throw new RuntimeException("admin must preserve uncached semantics first={$first} second={$second}");
        }
        echo wp_json_encode(array('status'=>'PASS','marker'=>'PPAR_RUNTIME_REUSE_ADMIN_UNCACHED_PASS','first'=>$first,'second'=>$second));
    } catch (Throwable $e) {
        status_header(500);
        echo wp_json_encode(array('status'=>'FAIL','message'=>$e->getMessage()));
    }
    exit;
});
