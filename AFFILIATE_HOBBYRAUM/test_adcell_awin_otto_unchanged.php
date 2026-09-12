<?php
declare(strict_types=1);

function fail_gate(string $message): void {
    fwrite(STDERR, "FAIL: {$message}\n");
    exit(1);
}

function automation_source(): string {
    $local = __DIR__ . '/trait-ppar-automation-suite.php';
    if (is_file($local)) {
        $text = file_get_contents($local);
        if ($text !== false) { return $text; }
    }
    $repo = dirname(__DIR__) . '/release/affiliate-zentrale/current/affiliate-portal-router/includes/trait-ppar-automation-suite.php';
    $text = @file_get_contents($repo);
    if ($text === false) { fail_gate('automation source missing'); }
    return $text;
}

function named_function_hashes(string $source): array {
    $tokens = token_get_all($source);
    $out = [];
    $count = count($tokens);
    for ($i = 0; $i < $count; $i++) {
        if (!is_array($tokens[$i]) || $tokens[$i][0] !== T_FUNCTION) { continue; }
        $start = $i;
        $j = $i + 1;
        while ($j < $count) {
            $token = $tokens[$j];
            if (is_array($token) && in_array($token[0], [T_WHITESPACE, T_AMPERSAND_FOLLOWED_BY_VAR_OR_VARARG, T_AMPERSAND_NOT_FOLLOWED_BY_VAR_OR_VARARG], true)) { $j++; continue; }
            if ($token === '&') { $j++; continue; }
            break;
        }
        if ($j >= $count || !is_array($tokens[$j]) || $tokens[$j][0] !== T_STRING) { continue; }
        $name = $tokens[$j][1];
        while ($j < $count && $tokens[$j] !== '{') { $j++; }
        if ($j >= $count) { continue; }
        $depth = 0;
        $buffer = '';
        for ($k = $start; $k < $count; $k++) {
            $token = $tokens[$k];
            $part = is_array($token) ? $token[1] : $token;
            $buffer .= $part;
            if ($k >= $j) {
                if ($part === '{') { $depth++; }
                elseif ($part === '}') {
                    $depth--;
                    if ($depth === 0) {
                        $out[$name] = hash('sha256', $buffer);
                        $i = $k;
                        break;
                    }
                }
            }
        }
    }
    return $out;
}

$expected = [
    'automation_stop_legacy_unfiltered_otto_jobs' => 'b865a12b06c2476fe7ae7226c1b755870d37c864382de81f06ec9960cd0424c9',
    'automation_cleanup_legacy_unfiltered_otto_imports' => 'e36a5f4f3e61167589a901797ae6334889e79a605ff084d88b61aa9f43ee6bdd',
    'automation_refresh_awin_programme_list' => '19e20f583cab151328dfeaaf5ce1ee53124e7bbf278c54e6393b0c1ec5d57519',
    'automation_refresh_awin_feed_list' => '1ae544163278402a4fac05d5743b447acc0934b870fa28c063e437db013f6a2f',
    'automation_enqueue_awin_partner' => 'd6758c77f2f8a0fef06d416c4b62fef2846079a15cf04d14ec3f5251157e321e',
    'automation_validate_awin_feed_url' => 'ceb1124ed666cc8ca6812623561512c25e66c5183801af58069cf0b1399dd6ea',
    'automation_otto_filtered_feed_binding' => '9cf7e4e20dfeb21f2b4e2d60aa5e5008a644e23a68370df372c369b34d77968f',
    'automation_select_awin_feed' => '2f2f50525c70caf1ff6a0f444b98f7f4eddf3f3b18bb3209e71ee7df53e3fe4f',
    'automation_download_awin_feed' => '49e19176dc22fed100b237eff922483d4a1d44676d26a8ff207469169a8568f9',
    'automation_awin_offer_has_next' => '116e813d7098d22ff14488658a1b89f8af957e04192984552abf92dd0171a8a0',
    'automation_otto_product_relevance_gate' => '5d5be0aba6c4781f029c6bce785756b6fc9ee46285e022f285e5f2e3e4d17f79',
    'automation_process_awin_product_batch' => '3596c7d478cf0467a5283eb28cb7521ab701c7e2ef46aa2587fbb3b1bc0a0240',
    'automation_awin_static_creative_rows' => '4b62000e89e8e204ea87c94a91566896ba6b41308a4e0fa5340dc5f713d0ab82',
    'automation_import_awin_static_creatives' => '17866aae820d6bb72771553c0c2898985ad96c5846398ddff4c8d6670866143b',
    'automation_awin_tracking_url' => 'a004160ad1eef363b4f9ef881da32cb9c43587842c0696d2b7929db370a33c17',
    'automation_awin_flatten_product' => '95cf0fcc975e2f54177a2fd238639f64638372f89a39649c4d44a79f8bc1d320',
    'automation_awin_field' => 'dab16b14043de48fb12bdf02351b19a708f4383bf99337fa11b5e5e8ff0c9158',
    'automation_awin_start_button_attributes' => '773370d109df1346d529b6500c43766e6b4de3d8200c1fb5dd3686f89cafdf67',
];

$actual = named_function_hashes(automation_source());
foreach ($expected as $name => $hash) {
    if (!isset($actual[$name])) { fail_gate("missing function {$name}"); }
    if (!hash_equals($hash, $actual[$name])) { fail_gate("Awin/OTTO function changed: {$name}"); }
    echo "PASS: {$name} unchanged\n";
}
echo 'ALL 18 AWIN/OTTO FUNCTION HASHES PASS' . PHP_EOL;
