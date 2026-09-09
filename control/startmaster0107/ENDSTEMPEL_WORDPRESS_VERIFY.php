<?php
/**
 * Pferde Atelier ENDSTEMPEL verifier.
 * Read-only until verification is complete. The private signing key is never present here.
 */

function pferde_endstempel_fail(string $reason): void {
    throw new RuntimeException($reason);
}

function pferde_endstempel_sort_recursive($value) {
    if (!is_array($value)) return $value;
    $isList = array_keys($value) === range(0, count($value) - 1);
    if ($isList) {
        $out = [];
        foreach ($value as $v) $out[] = pferde_endstempel_sort_recursive($v);
        return $out;
    }
    ksort($value, SORT_STRING);
    foreach ($value as $k => $v) $value[$k] = pferde_endstempel_sort_recursive($v);
    return $value;
}

function pferde_endstempel_stable_hash(array $value): string {
    $sorted = pferde_endstempel_sort_recursive($value);
    $json = json_encode($sorted, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
    if ($json === false) pferde_endstempel_fail('CANONICAL_JSON_FAILED');
    return hash('sha256', $json);
}

function pferde_endstempel_load_json(string $path): array {
    $raw = @file_get_contents($path);
    if ($raw === false) pferde_endstempel_fail('FINAL_JSON_MISSING');
    $obj = json_decode($raw, true);
    if (!is_array($obj)) pferde_endstempel_fail('FINAL_JSON_INVALID');
    return $obj;
}

function pferde_endstempel_verify_before_write(string $finalPath, array $trustedKeys, callable $isBatchUsed): array {
    $pkg = pferde_endstempel_load_json($finalPath);
    if (($pkg['contract'] ?? '') !== 'PSERC_APPROVED_PRODUCTION_PACKAGE_V1') pferde_endstempel_fail('PACKAGE_CONTRACT_INVALID');
    if (($pkg['endstamp_contract'] ?? '') !== 'PFERDE_ATELIER_ENDSTEMPEL_RELEASE_V1') pferde_endstempel_fail('ENDSTEMPEL_CONTRACT_INVALID');
    if (($pkg['status'] ?? '') !== 'ENDSTEMPEL_PASS') pferde_endstempel_fail('ENDSTEMPEL_STATUS_INVALID');
    if (($pkg['publish_allowed'] ?? null) !== false || ($pkg['content_mutation_performed'] ?? null) !== false) pferde_endstempel_fail('MUTATION_OR_PUBLISH_FORBIDDEN');

    $payloadHash = $pkg['package_payload_sha256'] ?? '';
    $copy = $pkg;
    unset($copy['package_payload_sha256']);
    if (!is_string($payloadHash) || !hash_equals($payloadHash, pferde_endstempel_stable_hash($copy))) pferde_endstempel_fail('PACKAGE_PAYLOAD_HASH_MISMATCH');

    $manifest = $pkg['article_manifest'] ?? null;
    if (!is_array($manifest) || ($manifest['contract'] ?? '') !== 'PFERDE_ATELIER_ENDSTEMPEL_ARTICLE_MANIFEST_V1') pferde_endstempel_fail('MANIFEST_INVALID');
    if (($manifest['publish_allowed'] ?? null) !== false || ($manifest['content_mutation_performed'] ?? null) !== false) pferde_endstempel_fail('MANIFEST_MUTATION_OR_PUBLISH_FORBIDDEN');
    $mhash = pferde_endstempel_stable_hash($manifest);
    if (!hash_equals((string)($pkg['article_manifest_sha256'] ?? ''), $mhash)) pferde_endstempel_fail('MANIFEST_HASH_MISMATCH');
    if (!hash_equals((string)($pkg['batch_sha256'] ?? ''), (string)($manifest['batch_sha256'] ?? ''))) pferde_endstempel_fail('BATCH_MISMATCH');

    $keyId = (string)($pkg['signing_key_id'] ?? '');
    if (!isset($trustedKeys[$keyId]) || !is_array($trustedKeys[$keyId])) pferde_endstempel_fail('UNTRUSTED_SIGNING_KEY');
    $trusted = $trustedKeys[$keyId];
    $pubB64 = (string)($trusted['public_key_b64'] ?? '');
    $pub = base64_decode($pubB64, true);
    if ($pub === false || strlen($pub) !== SODIUM_CRYPTO_SIGN_PUBLICKEYBYTES) pferde_endstempel_fail('TRUSTED_PUBLIC_KEY_INVALID');
    $pubSha = hash('sha256', $pub);
    if (!hash_equals((string)($trusted['sha256'] ?? ''), $pubSha)) pferde_endstempel_fail('TRUSTED_PUBLIC_KEY_SHA_INVALID');
    if (!hash_equals((string)($pkg['signing_public_key_sha256'] ?? ''), $pubSha)) pferde_endstempel_fail('PACKAGE_PUBLIC_KEY_SHA_MISMATCH');
    $sig = base64_decode((string)($pkg['signature_b64'] ?? ''), true);
    if ($sig === false || strlen($sig) !== SODIUM_CRYPTO_SIGN_BYTES) pferde_endstempel_fail('SIGNATURE_INVALID_ENCODING');
    if (!sodium_crypto_sign_verify_detached($sig, $mhash, $pub)) pferde_endstempel_fail('SIGNATURE_INVALID');

    $batch = (string)($manifest['batch_sha256'] ?? '');
    if (!preg_match('/^[0-9a-f]{64}$/', $batch)) pferde_endstempel_fail('BATCH_INVALID');
    if ($isBatchUsed($batch)) pferde_endstempel_fail('BATCH_ALREADY_IMPORTED');

    $articles = $manifest['articles'] ?? null;
    $count = (int)($manifest['article_count'] ?? -1);
    if (!is_array($articles) || $count < 1 || count($articles) !== $count) pferde_endstempel_fail('ARTICLE_COUNT_INVALID');
    $dir = dirname($finalPath);
    $expected = [];
    foreach ($articles as $row) {
        if (!is_array($row)) pferde_endstempel_fail('ARTICLE_ROW_INVALID');
        $name = (string)($row['name'] ?? '');
        if (!preg_match('/^ARTICLE_[0-9a-f]{64}\.md$/', $name)) pferde_endstempel_fail('ARTICLE_NAME_INVALID');
        if (isset($expected[$name])) pferde_endstempel_fail('ARTICLE_DUPLICATE');
        $path = $dir . DIRECTORY_SEPARATOR . $name;
        if (!is_file($path)) pferde_endstempel_fail('ARTICLE_MISSING:' . $name);
        $bytes = filesize($path);
        $sha = hash_file('sha256', $path);
        if ($bytes !== (int)($row['byte_length'] ?? -1)) pferde_endstempel_fail('ARTICLE_LENGTH_MISMATCH:' . $name);
        if (!hash_equals((string)($row['sha256'] ?? ''), (string)$sha)) pferde_endstempel_fail('ARTICLE_HASH_MISMATCH:' . $name);
        $expected[$name] = true;
    }
    $actual = [];
    foreach (glob($dir . DIRECTORY_SEPARATOR . 'ARTICLE_*.md') ?: [] as $path) {
        if (is_file($path)) $actual[basename($path)] = true;
    }
    $expectedNames = array_keys($expected); sort($expectedNames, SORT_STRING);
    $actualNames = array_keys($actual); sort($actualNames, SORT_STRING);
    if ($expectedNames !== $actualNames) pferde_endstempel_fail('ARTICLE_SET_MISMATCH');

    return [
        'ok' => true,
        'status' => 'ENDSTEMPEL_WORDPRESS_PREIMPORT_PASS',
        'batch_sha256' => $batch,
        'article_count' => $count,
        'articles' => $articles,
        'verified_before_first_write' => true,
        'publish_allowed' => false,
    ];
}

function pferde_endstempel_atomic_import(
    string $finalPath,
    array $trustedKeys,
    callable $isBatchUsed,
    callable $begin,
    callable $writer,
    callable $markBatchUsed,
    callable $commit,
    callable $rollback
) {
    $verified = pferde_endstempel_verify_before_write($finalPath, $trustedKeys, $isBatchUsed);
    $begun = false;
    try {
        $begin();
        $begun = true;
        $result = $writer($verified);
        $markBatchUsed($verified['batch_sha256']);
        $commit();
        return $result;
    } catch (Throwable $e) {
        if ($begun) $rollback();
        throw $e;
    }
}
