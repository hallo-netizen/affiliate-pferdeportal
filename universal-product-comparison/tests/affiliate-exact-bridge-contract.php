<?php
declare(strict_types=1);

function check(bool $ok, string $name): void {
    if (!$ok) {
        fwrite(STDERR, "FAIL: {$name}\n");
        exit(1);
    }
    echo "PASS: {$name}\n";
}

$root = dirname(__DIR__);
$plugin = file_get_contents($root . '/universal-product-comparison.php');
$bridge = file_get_contents($root . '/src/class-upc-affiliate-bridge.php');
$draft  = file_get_contents($root . '/src/class-upc-wordpress-draft.php');

check($plugin !== false && $bridge !== false && $draft !== false, 'bridge source files readable');

check(
    str_contains($plugin, 'class-upc-affiliate-bridge.php')
    && str_contains($plugin, "UPC_Affiliate_Bridge', 'register"),
    'UPC registers the Affiliate bridge'
);

check(
    str_contains($bridge, 'ppar_affiliate_exact_product_requirements')
    && str_contains($bridge, 'get_comparison_bundle')
    && str_contains($bridge, "\$item['knowledge']"),
    'bridge resolves bound comparison subjects through UPC repository'
);

check(
    str_contains($draft, "'_upc_comparison_id'")
    && str_contains($bridge, "get_post_meta( \$post_id, '_upc_comparison_id'")
    && str_contains($bridge, '/^UPC-([0-9]+)$/'),
    'new drafts use direct comparison id and old drafts have strict UID fallback'
);

check(
    str_contains($bridge, "array( 'GTIN', 'EAN', 'MPN' )")
    && str_contains($bridge, "'identifier_type'")
    && str_contains($bridge, "'identifier_value'")
    && str_contains($bridge, "'identifiers' => \$identifiers"),
    'Affiliate receives only GTIN EAN or real MPN exact identifiers'
);

check(
    !str_contains($bridge, "array( 'GTIN', 'EAN', 'MPN', 'MANUFACTURER_ARTICLE_NUMBER' )")
    && str_contains($bridge, 'MANUFACTURER_ARTICLE_NUMBER remains useful product knowledge')
    && str_contains($bridge, 'not an automatic commerce match key'),
    'manufacturer article number is explicitly excluded from automatic Affiliate exact match'
);

check(
    str_contains($bridge, 'Fail closed')
    && str_contains($bridge, 'if ( empty( $identifiers ) )')
    && !str_contains($bridge, 'fuzzy_match'),
    'subject without allowed exact identifier produces no Affiliate substitute'
);

check(
    !str_contains($bridge, 'global $wpdb')
    && !str_contains($bridge, 'upk_products')
    && !str_contains($bridge, 'upk_variants')
    && !str_contains($bridge, 'upk_identifiers')
    && !str_contains($bridge, 'ppar_sync_products'),
    'bridge has no direct Productwissen or Affiliate table coupling'
);

check(
    str_contains($bridge, '$requirements = is_array( $requirements ) ? $requirements : array();')
    && str_contains($bridge, '$requirements[] = array('),
    'bridge preserves existing Affiliate requirements and appends exact subjects'
);

echo "ALL PRODUCTWISSEN/AFFILIATE BRIDGE CONTRACT TESTS PASS\n";
