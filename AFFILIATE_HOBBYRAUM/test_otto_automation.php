<?php
declare(strict_types=1);

function pass_or_fail(bool $ok, string $name): void {
    if (!$ok) {
        fwrite(STDERR, "FAIL: {$name}\n");
        exit(1);
    }
    echo "PASS: {$name}\n";
}

function source(string $name): string {
    $text = @file_get_contents(__DIR__ . '/' . $name);
    if ($text === false) {
        fwrite(STDERR, "FAIL: source missing: {$name}\n");
        exit(1);
    }
    return $text;
}

$automation = source('trait-ppar-automation-suite.php');
$output = source('trait-ppar-output-objects.php');
$articles = source('trait-ppar-article-plans.php');
$creative = source('trait-ppar-creative-library.php');
$ebay = source('trait-ppar-ebay.php');
$router = source('pferdeportal-affiliate-router.php');

pass_or_fail(
    str_contains($automation, 'creative_library_schedule_asset_verification(10)'),
    'automated imports enter asset verification'
);
pass_or_fail(
    str_contains($automation, "ppar_affiliate_awin_product_seller")
    && str_contains($automation, "'seller_name' => \$seller_name"),
    'Awin product seller is explicit and fail-closed'
);
pass_or_fail(
    str_contains($output, 'function output_is_otto_awin_product')
    && str_contains($output, 'function output_otto_awin_auto_allowed')
    && str_contains($output, 'output_otto_seller_name($row)'),
    'OTTO remains a logical Awin product source with seller gate'
);
pass_or_fail(
    str_contains($output, "'category_product'")
    && str_contains($output, "'post_bottom_products'")
    && str_contains($output, "'hub_product_1'")
    && str_contains($output, "'journal_product_1'"),
    'OTTO uses existing category hub journal and article product placements'
);
pass_or_fail(
    str_contains($output, "'_ppar_otto_awin_auto'")
    && str_contains($output, "'otto_awin_verified_product'"),
    'only centrally verified OTTO campaigns receive auto marker'
);
pass_or_fail(
    str_contains($articles, '$trusted_awin_auto')
    && str_contains($articles, 'auto_verified_otto_awin')
    && str_contains($articles, '_ppar_otto_awin_auto'),
    'article plans trust only centrally verified OTTO Awin products'
);
pass_or_fail(
    str_contains($creative, "creative_asset_verification_complete")
    && str_contains($creative, "product_payload_hash")
    && str_contains($creative, "source_payload_for_hash"),
    'verification wave rebuilds articles and product payload changes alter freshness'
);
pass_or_fail(
    str_contains($ebay, 'ebay_verified_otto_awin_campaign')
    && str_contains($ebay, '$verified_otto_awin_present')
    && str_contains($ebay, "&& !\$verified_otto_awin_present"),
    'legacy eBay cohort cannot silently suppress verified OTTO'
);
pass_or_fail(
    str_contains($router, 'otto_awin_product_campaign_seller_ready')
    && substr_count($router, 'Verkauf durch ') >= 1
    && str_contains($articles, 'Verkauf durch '),
    'seller is a public-output gate and rendered on product cards'
);
pass_or_fail(
    !str_contains($output, 'product_image_as_banner')
    && !str_contains($automation, 'product_image_as_banner'),
    'no product-image banner fallback introduced'
);

// Behavioral mini-contracts.
function is_otto(array $row): bool {
    if (($row['provider'] ?? '') !== 'awin' || ($row['source_kind'] ?? '') !== 'product') return false;
    $id = strtolower(trim((string)($row['partner_name'] ?? '')));
    return preg_match('/(?:^|[^a-z0-9])otto(?:[^a-z0-9]|$)/', $id) === 1;
}
function auto_allowed(array $row): bool {
    return is_otto($row)
        && ($row['classification'] ?? '') === 'ready'
        && ($row['image_verified'] ?? false) === true
        && ($row['programme_allowed'] ?? false) === true
        && ($row['tracking_ok'] ?? false) === true
        && trim((string)($row['seller_name'] ?? '')) !== '';
}
$good = [
    'provider'=>'awin','source_kind'=>'product','partner_name'=>'OTTO',
    'classification'=>'ready','image_verified'=>true,'programme_allowed'=>true,
    'tracking_ok'=>true,'seller_name'=>'Reitsport Händler GmbH'
];
pass_or_fail(auto_allowed($good), 'positive OTTO auto contract');
$bad = $good; $bad['seller_name'] = '';
pass_or_fail(!auto_allowed($bad), 'missing seller blocks OTTO');
$bad = $good; $bad['programme_allowed'] = false;
pass_or_fail(!auto_allowed($bad), 'unapproved Awin programme blocks OTTO');
$bad = $good; $bad['image_verified'] = false;
pass_or_fail(!auto_allowed($bad), 'unverified image blocks OTTO');
$bad = $good; $bad['partner_name'] = 'Loesdau';
pass_or_fail(!auto_allowed($bad), 'non-OTTO Awin is not auto-enabled by OTTO rule');

$fp = static function(array $row): string {
    ksort($row);
    return hash('sha256', json_encode($row, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES));
};
$a = $fp(['price'=>'49.99','availability'=>'active','seller_name'=>'A']);
$b = $fp(['price'=>'54.99','availability'=>'active','seller_name'=>'A']);
$c = $fp(['price'=>'49.99','availability'=>'active','seller_name'=>'B']);
pass_or_fail($a !== $b && $a !== $c, 'price and seller changes alter product freshness');

echo "ALL OTTO HOBBYROOM TESTS PASS\n";
