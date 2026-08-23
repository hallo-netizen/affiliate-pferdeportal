<?php
if (!defined('ABSPATH')) { exit(1); }
$checks = array();
$ok = function($cond, $name) use (&$checks) {
    $checks[] = array((bool)$cond, $name);
    echo ($cond ? 'PASS ' : 'FAIL ') . $name . "\n";
};
require_once ABSPATH . 'wp-admin/includes/plugin.php';
$plugin_file = WP_PLUGIN_DIR . '/affiliate-portal-router/pferdeportal-affiliate-router.php';
$data = get_plugin_data($plugin_file, false, false);
$ok((string)($data['Version'] ?? '') === '6.55.0', 'wordpress_plugin_header_655');
$ok(Pferdeportal_Affiliate_Router::VERSION === '6.55.0', 'class_version_655');
$ok(Pferdeportal_Affiliate_Router::EBAY_RUNTIME_BUILD === '6.55.0-kiss-public-heartbeat-github-scheduler-20260823', 'runtime_build_unchanged');

$router = Pferdeportal_Affiliate_Router::instance();
$method = new ReflectionMethod($router, 'render_banner');
$method->setAccessible(true);
$banner = array(
    'url' => 'https://example.com/item',
    'image_url' => 'https://example.com/image.jpg',
    'title' => 'Testprodukt',
    'button_text' => 'Bei eBay ansehen',
    'description' => '',
    'price' => '59,90',
    'currency' => 'EUR',
    'availability' => '',
    'creative_type' => 'product',
    'target' => '_blank',
    'subid_param' => '',
);
$context = array('primary_slug'=>'reitstiefel','primary_name'=>'Reitstiefel');
$group = array('id'=>'realgate');
$required = array(
    'data-ppar-category-product-image-frame="150"',
    'width:150px!important', 'height:150px!important',
    'min-width:150px!important', 'min-height:150px!important',
    'max-width:150px!important', 'max-height:150px!important',
    'object-fit:cover!important', 'object-position:center center!important',
);
foreach (array('category_product_1','category_product_2','category_product_3') as $slot) {
    $html = (string)$method->invoke($router, $banner, 123, $context, $group, $slot);
    $ok($html !== '', $slot . '_renders');
    $ok(substr_count($html, 'data-ppar-category-product-image-frame="150"') === 1, $slot . '_single_frame_marker');
    foreach ($required as $token) {
        $ok(strpos($html, $token) !== false, $slot . '_has_' . preg_replace('/[^a-z0-9]+/i','_',trim($token,'"')));
    }
}
foreach (array('product_after_category_tiles','post_bottom_products','journal_product_1') as $slot) {
    $html = (string)$method->invoke($router, $banner, 123, $context, $group, $slot);
    $ok(strpos($html, 'data-ppar-category-product-image-frame=') === false, $slot . '_not_modified');
}
$banner2 = $banner; $banner2['creative_type'] = 'banner';
$html = (string)$method->invoke($router, $banner2, 123, $context, $group, 'category_product_1');
$ok(strpos($html, 'data-ppar-category-product-image-frame=') === false, 'non_product_creative_not_modified');

$fail = array_values(array_filter($checks, function($row){ return !$row[0]; }));
echo 'REAL_INLINE_IMAGE_ASSERTIONS=' . count($checks) . ' FAIL=' . count($fail) . "\n";
if ($fail) { exit(1); }
echo "REAL_INLINE_IMAGE_ROOTFIX=PASS\n";
