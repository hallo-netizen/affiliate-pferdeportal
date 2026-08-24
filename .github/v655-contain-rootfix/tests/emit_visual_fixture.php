<?php
if (!defined('ABSPATH')) { exit(1); }
$base = rtrim((string)getenv('PPAR_VISUAL_BASE'), '/');
if ($base === '') { fwrite(STDERR, "PPAR_VISUAL_BASE missing\n"); exit(1); }
$router = Pferdeportal_Affiliate_Router::instance();
$method = new ReflectionMethod($router, 'render_banner');
$method->setAccessible(true);
$context = array('primary_slug'=>'reitstiefel','primary_name'=>'Reitstiefel');
$group = array('id'=>'visual');
$files = array('landscape.svg','portrait.svg','square.svg');
for ($i=1; $i<=3; $i++) {
    $banner = array(
        'url' => 'https://example.com/item-' . $i,
        'image_url' => $base . '/' . $files[$i-1],
        'title' => 'Visual ' . $i,
        'button_text' => 'Bei eBay ansehen',
        'description' => '',
        'price' => '',
        'currency' => 'EUR',
        'availability' => '',
        'creative_type' => 'product',
        'target' => '_blank',
        'subid_param' => '',
    );
    $slot = 'category_product_' . $i;
    $html = (string)$method->invoke($router, $banner, 123, $context, $group, $slot);
    echo '<div class="visual-slot pa266-product is-real" data-slot="' . esc_attr($slot) . '">' . $html . '</div>' . "\n";
}
