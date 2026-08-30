<?php
if (!defined('ABSPATH')) {
    exit;
}

/**
 * eBay Marketplace Account Deletion/Closure Compliance.
 *
 * Provider-spezifischer Hard-Safety-Baustein. Der Chefvertrag kann diesen
 * rechtlichen/technischen Blocker niemals ueberstimmen.
 *
 * - oeffentlicher HTTPS-REST-Endpunkt fuer eBays GET-Challenge,
 * - X-EBAY-SIGNATURE-Pruefung fuer POST-Benachrichtigungen,
 * - temporaer gecachter Public-Key-Abruf ueber die eBay Notification API,
 * - irreversible Entfernung aller lokal zuordenbaren eBay-Nutzerdaten,
 * - idempotente, PII-freie Verarbeitungsbelege.
 */
trait PPAR_Ebay_Account_Deletion_Trait {
    public function register_ebay_account_deletion_routes() {
        if (!function_exists('register_rest_route')) {
            return;
        }
        register_rest_route(self::EBAY_DELETION_REST_NAMESPACE, self::EBAY_DELETION_REST_ROUTE, array(
            array(
                'methods' => 'GET',
                'callback' => array($this, 'handle_ebay_account_deletion_challenge'),
                'permission_callback' => '__return_true',
            ),
            array(
                'methods' => 'POST',
                'callback' => array($this, 'handle_ebay_account_deletion_notification'),
                'permission_callback' => '__return_true',
            ),
        ));
    }

    public function ebay_deletion_endpoint_url() {
        $path = trim(self::EBAY_DELETION_REST_NAMESPACE, '/') . '/' . trim(self::EBAY_DELETION_REST_ROUTE, '/');
        return function_exists('rest_url') ? (string) rest_url($path) : '';
    }

    private function ebay_deletion_endpoint_is_https() {
        $endpoint = $this->ebay_deletion_endpoint_url();
        return $endpoint !== '' && strtolower((string) parse_url($endpoint, PHP_URL_SCHEME)) === 'https';
    }

    public function ebay_deletion_verification_token() {
        if (defined('PPAR_EBAY_DELETION_VERIFICATION_TOKEN')) {
            $constant = trim((string) PPAR_EBAY_DELETION_VERIFICATION_TOKEN);
            if ($this->ebay_deletion_token_is_valid($constant)) {
                return $constant;
            }
        }
        $stored = trim((string) get_option(self::OPTION_EBAY_DELETION_TOKEN, ''));
        if ($this->ebay_deletion_token_is_valid($stored)) {
            return $stored;
        }
        if (function_exists('wp_generate_password')) {
            $stored = wp_generate_password(48, false, false);
        } else {
            try {
                $stored = bin2hex(random_bytes(24));
            } catch (Exception $e) {
                $stored = substr(hash('sha256', uniqid('ppar-ebay-deletion-', true)), 0, 48);
            }
        }
        if (!$this->ebay_deletion_token_is_valid($stored)) {
            $stored = substr(preg_replace('/[^A-Za-z0-9_-]/', '', (string) $stored), 0, 48);
        }
        update_option(self::OPTION_EBAY_DELETION_TOKEN, $stored, false);
        return $stored;
    }

    public function ebay_deletion_token_is_valid($token) {
        $token = (string) $token;
        $len = strlen($token);
        return $len >= 32 && $len <= 80 && (bool) preg_match('/^[A-Za-z0-9_-]+$/', $token);
    }

    private function ebay_deletion_state() {
        $state = get_option(self::OPTION_EBAY_DELETION_STATE, array());
        $state = is_array($state) ? $state : array();
        return array_merge(array(
            'challenge_answered_at' => 0,
            'last_notification_at' => 0,
            'last_notification_status' => '',
            'last_notification_hash' => '',
            'last_deleted_items' => 0,
            'last_deleted_creatives' => 0,
            'last_deleted_outputs' => 0,
            'last_error' => '',
        ), $state);
    }

    private function ebay_deletion_update_state($changes) {
        $state = array_merge($this->ebay_deletion_state(), is_array($changes) ? $changes : array());
        foreach (array('challenge_answered_at','last_notification_at','last_deleted_items','last_deleted_creatives','last_deleted_outputs') as $field) {
            $state[$field] = absint($state[$field] ?? 0);
        }
        $hash = strtolower(sanitize_text_field((string) ($state['last_notification_hash'] ?? '')));
        $state['last_notification_hash'] = preg_match('/^[a-f0-9]{64}$/', $hash) ? $hash : '';
        $state['last_notification_status'] = substr(sanitize_key((string) ($state['last_notification_status'] ?? '')), 0, 40);
        $state['last_error'] = substr(sanitize_text_field((string) ($state['last_error'] ?? '')), 0, 240);
        update_option(self::OPTION_EBAY_DELETION_STATE, $state, false);
        return $state;
    }

    public function ebay_deletion_compliance_snapshot() {
        $state = $this->ebay_deletion_state();
        $endpoint = $this->ebay_deletion_endpoint_url();
        $state['endpoint'] = $endpoint;
        $state['https'] = $this->ebay_deletion_endpoint_is_https();
        $state['token_valid'] = $this->ebay_deletion_token_is_valid($this->ebay_deletion_verification_token());
        $state['challenge_answered'] = !empty($state['challenge_answered_at']);
        $state['signed_notification_verified'] = (string) ($state['last_notification_status'] ?? '') === 'verified';
        $state['complete'] = $state['https'] && $state['token_valid'] && $state['challenge_answered'] && $state['signed_notification_verified'];
        return $state;
    }

    public function ebay_deletion_compliance_complete() {
        $state = $this->ebay_deletion_compliance_snapshot();
        return !empty($state['complete']);
    }

    public function ebay_deletion_challenge_answered() {
        $state = $this->ebay_deletion_compliance_snapshot();
        return !empty($state['challenge_answered']);
    }

    public function ebay_deletion_challenge_response($challenge_code, $verification_token = null, $endpoint = null) {
        $challenge_code = (string) $challenge_code;
        $verification_token = $verification_token === null ? $this->ebay_deletion_verification_token() : (string) $verification_token;
        $endpoint = $endpoint === null ? $this->ebay_deletion_endpoint_url() : (string) $endpoint;
        if ($challenge_code === '' || !$this->ebay_deletion_token_is_valid($verification_token) || $endpoint === '') {
            return new WP_Error('ebay_deletion_challenge_invalid', 'eBay-Challenge, Verification Token oder Endpoint ist ungültig.');
        }
        return hash('sha256', $challenge_code . $verification_token . $endpoint);
    }

    public function handle_ebay_account_deletion_challenge($request) {
        if (!$this->ebay_deletion_endpoint_is_https()) {
            return new WP_Error('ebay_deletion_https_required', 'Der eBay Notification Endpoint muss per HTTPS erreichbar sein.', array('status' => 503));
        }
        $challenge = '';
        if (is_object($request) && method_exists($request, 'get_param')) {
            $challenge = trim((string) $request->get_param('challenge_code'));
        }
        if ($challenge === '' || strlen($challenge) > 512) {
            return new WP_Error('ebay_deletion_challenge_missing', 'challenge_code fehlt oder ist ungültig.', array('status' => 400));
        }
        $response = $this->ebay_deletion_challenge_response($challenge);
        if (is_wp_error($response)) {
            return $response;
        }
        // Wir wissen lokal nur, dass die Challenge korrekt beantwortet wurde.
        // Ob eBay sie akzeptiert hat, beweist erst der anschliessende aktive Keyset-/OAuth-Test.
        $this->ebay_deletion_update_state(array(
            'challenge_answered_at' => time(),
            'last_error' => '',
        ));
        return new WP_REST_Response(array('challengeResponse' => $response), 200);
    }

    public function ebay_deletion_decode_signature_header($header) {
        $header = trim((string) $header);
        if ($header === '' || strlen($header) > 8192) {
            return new WP_Error('ebay_deletion_signature_missing', 'X-EBAY-SIGNATURE fehlt oder ist ungültig.');
        }
        $decoded = base64_decode($header, true);
        if ($decoded === false) {
            return new WP_Error('ebay_deletion_signature_header_base64', 'X-EBAY-SIGNATURE ist nicht gültig Base64-kodiert.');
        }
        $json = json_decode($decoded, true);
        if (!is_array($json)) {
            return new WP_Error('ebay_deletion_signature_header_json', 'X-EBAY-SIGNATURE enthält kein gültiges JSON.');
        }
        $kid = trim((string) ($json['kid'] ?? ''));
        $signature = trim((string) ($json['signature'] ?? ''));
        $algorithm = strtoupper(trim((string) ($json['alg'] ?? '')));
        $digest = strtoupper(trim((string) ($json['digest'] ?? '')));
        if ($kid === '' || strlen($kid) > 255 || $signature === '') {
            return new WP_Error('ebay_deletion_signature_header_fields', 'X-EBAY-SIGNATURE enthält keine vollständigen Signaturdaten.');
        }
        if ($algorithm !== '' && strpos($algorithm, 'ECDSA') === false) {
            return new WP_Error('ebay_deletion_signature_algorithm', 'Nicht unterstützter eBay-Signaturalgorithmus.');
        }
        if ($digest === '') { $digest = 'SHA1'; }
        if (!in_array($digest, array('SHA1','SHA256','SHA384','SHA512'), true)) {
            return new WP_Error('ebay_deletion_signature_digest', 'Nicht unterstützter eBay-Signatur-Digest.');
        }
        return array('kid' => $kid, 'signature' => $signature, 'algorithm' => $algorithm, 'digest' => $digest);
    }

    private function ebay_deletion_public_key_cache_key($environment, $kid) {
        return 'ppar_ebay_notify_key_' . substr(hash('sha256', sanitize_key((string) $environment) . '|' . (string) $kid), 0, 32);
    }

    public function ebay_deletion_public_key_pem($key) {
        $key = trim((string) $key);
        if ($key === '') {
            return new WP_Error('ebay_deletion_public_key_empty', 'eBay Public Key ist leer.');
        }

        // eBays offizielles Event-Notification-PHP-SDK erwartet den Public Key
        // typischerweise als einzeilige PEM-Zeichenkette und rekonstruiert daraus
        // vor openssl_verify() ein normiertes PEM mit 64-Zeichen-Zeilen. Ein
        // unverändertes einzeiliges "BEGIN PUBLIC KEY ... END PUBLIC KEY" wird
        // von OpenSSL/PHP nicht zuverlässig akzeptiert und führte live zum HTTP 500.
        $body = $key;
        if (preg_match('/-----BEGIN PUBLIC KEY-----(.*?)-----END PUBLIC KEY-----/s', $key, $match)) {
            $body = (string) $match[1];
        }
        $compact = preg_replace('/\s+/', '', (string) $body);
        if ($compact === '' || base64_decode($compact, true) === false) {
            return new WP_Error('ebay_deletion_public_key_invalid', 'eBay Public Key ist weder PEM noch gültiges Base64.');
        }
        return "-----BEGIN PUBLIC KEY-----\n" . implode("\n", str_split($compact, 64)) . "\n-----END PUBLIC KEY-----\n";
    }

    private function ebay_deletion_fetch_public_key($kid, $settings) {
        $environment = (string) ($settings['environment'] ?? 'production');
        $cache_key = $this->ebay_deletion_public_key_cache_key($environment, $kid);
        if (function_exists('get_transient')) {
            $cached = get_transient($cache_key);
            if (is_array($cached) && !empty($cached['key'])) {
                return $cached;
            }
        }
        $token = $this->ebay_access_token($settings, false);
        if (is_wp_error($token)) {
            return $token;
        }
        $url = $this->ebay_api_base($settings) . '/commerce/notification/v1/public_key/' . rawurlencode((string) $kid);
        $response = wp_remote_get($url, array(
            'timeout' => 15,
            'redirection' => 1,
            'headers' => array(
                'Authorization' => 'Bearer ' . $token,
                'Accept' => 'application/json',
            ),
        ));
        if (is_wp_error($response)) {
            return $response;
        }
        $code = absint(wp_remote_retrieve_response_code($response));
        $body = json_decode((string) wp_remote_retrieve_body($response), true);
        if ($code !== 200 || !is_array($body) || empty($body['key'])) {
            return new WP_Error('ebay_deletion_public_key_failed', 'eBay Public Key konnte nicht geladen werden (HTTP ' . $code . ').');
        }
        $payload = array(
            'key' => (string) $body['key'],
            'algorithm' => strtoupper(sanitize_text_field((string) ($body['algorithm'] ?? 'ECDSA'))),
            'digest' => strtoupper(sanitize_text_field((string) ($body['digest'] ?? ''))),
        );
        if (function_exists('set_transient')) {
            set_transient($cache_key, $payload, HOUR_IN_SECONDS);
        }
        return $payload;
    }

    private function ebay_deletion_openssl_algorithm($digest) {
        $digest = strtoupper((string) $digest);
        $map = array(
            'SHA1' => defined('OPENSSL_ALGO_SHA1') ? OPENSSL_ALGO_SHA1 : 1,
            'SHA256' => defined('OPENSSL_ALGO_SHA256') ? OPENSSL_ALGO_SHA256 : 7,
            'SHA384' => defined('OPENSSL_ALGO_SHA384') ? OPENSSL_ALGO_SHA384 : 8,
            'SHA512' => defined('OPENSSL_ALGO_SHA512') ? OPENSSL_ALGO_SHA512 : 9,
        );
        return $map[$digest] ?? null;
    }

    public function ebay_deletion_verify_signature_with_key($raw_body, $signature_header, $public_key_payload) {
        if (!function_exists('openssl_verify') || !function_exists('openssl_pkey_get_public')) {
            return new WP_Error('ebay_deletion_openssl_missing', 'OpenSSL-Signaturprüfung ist auf dem Server nicht verfügbar.');
        }
        $header = is_array($signature_header) ? $signature_header : $this->ebay_deletion_decode_signature_header($signature_header);
        if (is_wp_error($header)) { return $header; }
        $public_key_payload = is_array($public_key_payload) ? $public_key_payload : array('key' => (string) $public_key_payload);
        $pem = $this->ebay_deletion_public_key_pem((string) ($public_key_payload['key'] ?? ''));
        if (is_wp_error($pem)) { return $pem; }
        $digest = strtoupper((string) ($header['digest'] ?? ''));
        $api_digest = strtoupper((string) ($public_key_payload['digest'] ?? ''));
        $api_algorithm = strtoupper((string) ($public_key_payload['algorithm'] ?? ''));
        if ($api_algorithm !== '' && strpos($api_algorithm, 'ECDSA') === false) {
            return new WP_Error('ebay_deletion_public_key_algorithm', 'eBay Public Key meldet einen nicht unterstützten Signaturalgorithmus.');
        }
        if ($api_digest !== '' && $digest !== '' && $api_digest !== $digest) {
            return new WP_Error('ebay_deletion_digest_mismatch', 'Digest aus eBay-Signatur und Public-Key-Antwort stimmt nicht überein.');
        }
        $algorithm = $this->ebay_deletion_openssl_algorithm($digest !== '' ? $digest : ($api_digest !== '' ? $api_digest : 'SHA1'));
        if ($algorithm === null) {
            return new WP_Error('ebay_deletion_digest_unsupported', 'eBay-Signatur-Digest wird nicht unterstützt.');
        }
        $signature = base64_decode((string) ($header['signature'] ?? ''), true);
        if ($signature === false || $signature === '') {
            return new WP_Error('ebay_deletion_signature_value_invalid', 'eBay-Signaturwert ist ungültig.');
        }
        $public_key = openssl_pkey_get_public($pem);
        if ($public_key === false) {
            return new WP_Error('ebay_deletion_public_key_parse_failed', 'eBay Public Key konnte nicht für OpenSSL geladen werden.');
        }
        $verified = openssl_verify((string) $raw_body, $signature, $public_key, $algorithm);
        if ($verified !== 1) {
            return new WP_Error('ebay_deletion_signature_invalid', 'eBay-Benachrichtigung konnte nicht kryptografisch verifiziert werden.');
        }
        return true;
    }

    private function ebay_deletion_verify_signature($raw_body, $header, $settings) {
        $decoded = $this->ebay_deletion_decode_signature_header($header);
        if (is_wp_error($decoded)) { return $decoded; }
        $public_key = $this->ebay_deletion_fetch_public_key((string) $decoded['kid'], $settings);
        if (is_wp_error($public_key)) { return $public_key; }
        return $this->ebay_deletion_verify_signature_with_key($raw_body, $decoded, $public_key);
    }

    public function ebay_deletion_extract_notification($payload) {
        $payload = is_array($payload) ? $payload : array();
        $topic = strtoupper(sanitize_text_field((string) ($payload['metadata']['topic'] ?? '')));
        if ($topic !== 'MARKETPLACE_ACCOUNT_DELETION') {
            return new WP_Error('ebay_deletion_topic_invalid', 'Unerwartetes eBay-Notification-Topic.');
        }
        $notification_id = trim((string) ($payload['notification']['notificationId'] ?? ''));
        $data = is_array($payload['notification']['data'] ?? null) ? $payload['notification']['data'] : array();
        if ($notification_id === '' || strlen($notification_id) > 255) {
            return new WP_Error('ebay_deletion_notification_id_missing', 'eBay notificationId fehlt oder ist ungültig.');
        }
        $identifiers = array(
            'username' => substr(trim((string) ($data['username'] ?? '')), 0, 191),
            'userId' => substr(trim((string) ($data['userId'] ?? '')), 0, 255),
            'eiasToken' => substr(trim((string) ($data['eiasToken'] ?? '')), 0, 512),
        );
        if ($identifiers['username'] === '' && $identifiers['userId'] === '' && $identifiers['eiasToken'] === '') {
            return new WP_Error('ebay_deletion_identifiers_missing', 'eBay-Löschbenachrichtigung enthält keinen Benutzeridentifikator.');
        }
        return array(
            'notification_id' => $notification_id,
            'notification_hash' => hash('sha256', $notification_id),
            'identifiers' => $identifiers,
        );
    }

    private function ebay_deletion_receipts() {
        $receipts = get_option(self::OPTION_EBAY_DELETION_RECEIPTS, array());
        return is_array($receipts) ? array_values($receipts) : array();
    }

    public function ebay_deletion_receipt_seen($notification_hash) {
        $notification_hash = strtolower((string) $notification_hash);
        if (!preg_match('/^[a-f0-9]{64}$/', $notification_hash)) { return false; }
        foreach ($this->ebay_deletion_receipts() as $receipt) {
            if (is_array($receipt) && hash_equals((string) ($receipt['notification_hash'] ?? ''), $notification_hash)) {
                return true;
            }
        }
        return false;
    }

    private function ebay_deletion_store_receipt($notification_hash, $counts) {
        $notification_hash = strtolower((string) $notification_hash);
        if (!preg_match('/^[a-f0-9]{64}$/', $notification_hash)) { return false; }
        $receipts = $this->ebay_deletion_receipts();
        $receipts[] = array(
            'notification_hash' => $notification_hash,
            'processed_at' => time(),
            'deleted_items' => absint($counts['items'] ?? 0),
            'deleted_creatives' => absint($counts['creatives'] ?? 0),
            'deleted_outputs' => absint($counts['outputs'] ?? 0),
        );
        if (count($receipts) > 200) {
            $receipts = array_slice($receipts, -200);
        }
        update_option(self::OPTION_EBAY_DELETION_RECEIPTS, $receipts, false);
        return true;
    }

    private function ebay_deletion_value_matches($field, $value, $identifiers) {
        $value = trim((string) $value);
        if ($value === '') { return false; }
        $field = strtolower((string) $field);
        if (in_array($field, array('username','seller_username','partner_external_id','external_id'), true)) {
            if (!empty($identifiers['username']) && strcasecmp($value, (string) $identifiers['username']) === 0) { return true; }
            // eBay kann in einzelnen Datenflüssen anstelle des sichtbaren Usernamens
            // die unveränderliche userId liefern. Ausschließlich exakter Vergleich.
            if (!empty($identifiers['userId']) && hash_equals((string) $identifiers['userId'], $value)) { return true; }
            return false;
        }
        if (in_array($field, array('userid','user_id'), true) && !empty($identifiers['userId'])) {
            return hash_equals((string) $identifiers['userId'], $value);
        }
        if (in_array($field, array('eiastoken','eias_token'), true) && !empty($identifiers['eiasToken'])) {
            return hash_equals((string) $identifiers['eiasToken'], $value);
        }
        return false;
    }

    public function ebay_deletion_payload_matches_identifiers($payload, $identifiers) {
        if (!is_array($payload)) { return false; }
        foreach ($payload as $key => $value) {
            if (is_array($value)) {
                if ($this->ebay_deletion_payload_matches_identifiers($value, $identifiers)) { return true; }
                continue;
            }
            if ($this->ebay_deletion_value_matches((string) $key, $value, $identifiers)) { return true; }
        }
        return false;
    }

    private function ebay_deletion_delete_owned_post($post_id, $identity_hash = '', $item_id = '') {
        $post_id = absint($post_id);
        if ($post_id <= 0 || !function_exists('wp_delete_post')) { return 0; }
        $attachment_id = function_exists('get_post_thumbnail_id') ? absint(get_post_thumbnail_id($post_id)) : 0;
        if ($attachment_id > 0 && function_exists('wp_delete_attachment') && function_exists('get_post_meta')) {
            $owned_identity = (string) get_post_meta($attachment_id, '_ppar_creative_identity_hash', true);
            $owned_item = (string) get_post_meta($attachment_id, '_ppar_ebay_item_id', true);
            if (($identity_hash !== '' && hash_equals((string) $identity_hash, $owned_identity)) || ($item_id !== '' && hash_equals((string) $item_id, $owned_item))) {
                wp_delete_attachment($attachment_id, true);
            }
        }
        $deleted = wp_delete_post($post_id, true);
        return $deleted ? 1 : 0;
    }

    private function ebay_deletion_delete_control_scope($scope_type, $scope_key) {
        if (!method_exists($this, 'control_decisions_table') || !method_exists($this, 'control_audit_table')) { return; }
        global $wpdb;
        $scope_type = sanitize_key((string) $scope_type);
        $scope_key = (string) $scope_key;
        $wpdb->delete($this->control_decisions_table(), array('scope_type' => $scope_type, 'scope_key' => $scope_key));
        $wpdb->delete($this->control_audit_table(), array('scope_type' => $scope_type, 'scope_key' => $scope_key));
    }

    private function ebay_deletion_delete_by_identity($identity_hash, &$counts) {
        $identity_hash = strtolower(trim((string) $identity_hash));
        if (!preg_match('/^[a-f0-9]{64}$/', $identity_hash)) { return; }
        global $wpdb;
        if (method_exists($this, 'output_objects_table')) {
            $table = $this->output_objects_table();
            $objects = $wpdb->get_results($wpdb->prepare("SELECT * FROM {$table} WHERE creative_identity_hash=%s", $identity_hash), ARRAY_A);
            foreach ((array) $objects as $object) {
                if (method_exists($this, 'output_deactivate_materialized_object')) {
                    $this->output_deactivate_materialized_object($object, 'eBay Marketplace Account Deletion/Closure: Nutzerdaten werden irreversibel gelöscht.');
                }
                $counts['posts'] += $this->ebay_deletion_delete_owned_post(absint($object['campaign_post_id'] ?? 0), $identity_hash, '');
                $counts['posts'] += $this->ebay_deletion_delete_owned_post(absint($object['listing_post_id'] ?? 0), $identity_hash, '');
            }
            $deleted = $wpdb->delete($table, array('creative_identity_hash' => $identity_hash));
            $counts['outputs'] += is_numeric($deleted) ? absint($deleted) : 0;
        }
        if (method_exists($this, 'output_portal_decisions_table')) {
            $wpdb->delete($this->output_portal_decisions_table(), array('creative_identity_hash' => $identity_hash));
        }
        if (method_exists($this, 'automation_edges_table')) {
            $wpdb->delete($this->automation_edges_table(), array('asset_identity_hash' => $identity_hash));
        }
        $this->ebay_deletion_delete_control_scope('creative', $identity_hash);
        if (method_exists($this, 'creative_library_table')) {
            $deleted = $wpdb->delete($this->creative_library_table(), array('identity_hash' => $identity_hash));
            $counts['creatives'] += is_numeric($deleted) ? absint($deleted) : 0;
        }
    }

    private function ebay_deletion_purge_partner_tables($identifiers, &$identities, &$counts) {
        global $wpdb;
        $partner_ids = array_values(array_unique(array_filter(array(
            trim((string) ($identifiers['username'] ?? '')),
            trim((string) ($identifiers['userId'] ?? '')),
        ))));
        if (!$partner_ids) { return; }

        foreach ($partner_ids as $partner_id) {
            if (method_exists($this, 'creative_library_table')) {
                $rows = $wpdb->get_results($wpdb->prepare("SELECT identity_hash FROM {$this->creative_library_table()} WHERE provider=%s AND partner_external_id=%s", 'ebay', $partner_id), ARRAY_A);
                foreach ((array) $rows as $row) {
                    $identity = strtolower((string) ($row['identity_hash'] ?? ''));
                    if (preg_match('/^[a-f0-9]{64}$/', $identity)) { $identities[$identity] = $identity; }
                }
            }
            if (method_exists($this, 'output_objects_table')) {
                $rows = $wpdb->get_results($wpdb->prepare("SELECT * FROM {$this->output_objects_table()} WHERE provider=%s AND partner_external_id=%s", 'ebay', $partner_id), ARRAY_A);
                foreach ((array) $rows as $row) {
                    $identity = strtolower((string) ($row['creative_identity_hash'] ?? ''));
                    if (preg_match('/^[a-f0-9]{64}$/', $identity)) { $identities[$identity] = $identity; }
                }
            }
            foreach (array('automation_edges_table','automation_runs_table','automation_jobs_table') as $method) {
                if (method_exists($this, $method)) {
                    $wpdb->delete($this->{$method}(), array('provider' => 'ebay', 'partner_external_id' => $partner_id));
                }
            }
            $this->ebay_deletion_delete_control_scope('partner', 'ebay:' . $partner_id);
        }
    }

    private function ebay_deletion_scrub_partner_options($identifiers) {
        foreach (array(self::OPTION_PARTNER_INTAKE, self::OPTION_PARTNER_PROFILES) as $option) {
            $value = get_option($option, array());
            if (!is_array($value)) { continue; }
            $changed = false;
            $filtered = array();
            foreach ($value as $key => $row) {
                $remove = false;
                if (is_array($row)) {
                    $provider = sanitize_key((string) ($row['provider'] ?? $row['network'] ?? ''));
                    if ($provider === 'ebay') {
                        foreach (array('partner_external_id','external_id','seller_username','username','userId','eiasToken') as $field) {
                            if (array_key_exists($field, $row) && $this->ebay_deletion_value_matches($field, $row[$field], $identifiers)) {
                                $remove = true;
                                break;
                            }
                        }
                    }
                }
                if (!$remove && is_string($key) && !empty($identifiers['username']) && strcasecmp($key, 'ebay:' . $identifiers['username']) === 0) {
                    $remove = true;
                }
                if ($remove) { $changed = true; continue; }
                $filtered[$key] = $row;
            }
            if ($changed) { update_option($option, $filtered, false); }
        }
    }

    public function ebay_deletion_irreversible_delete($identifiers) {
        $identifiers = is_array($identifiers) ? $identifiers : array();
        $counts = array('items'=>0,'creatives'=>0,'outputs'=>0,'posts'=>0);
        $identities = array();
        $item_rows = array();
        global $wpdb;

        $table = $this->ebay_items_table();
        $candidate_rows = array();
        $username = trim((string) ($identifiers['username'] ?? ''));
        $user_id = trim((string) ($identifiers['userId'] ?? ''));
        foreach (array_values(array_unique(array_filter(array($username, $user_id)))) as $seller_identifier) {
            $rows = $wpdb->get_results($wpdb->prepare("SELECT * FROM {$table} WHERE seller_username=%s", $seller_identifier), ARRAY_A);
            foreach ((array) $rows as $row) { $candidate_rows[] = $row; }
        }
        // Alle vorhandenen Identifikatoren werden in eBay-Rohpayloads strukturiert
        // und ausschließlich exakt geprüft; keine unsichere Substring-Suche.
        if ($username !== '' || $user_id !== '' || !empty($identifiers['eiasToken'])) {
            $payload_rows = $wpdb->get_results("SELECT * FROM {$table} WHERE source_payload<>'' AND source_payload<>'{}'", ARRAY_A);
            foreach ((array) $payload_rows as $row) {
                $decoded = json_decode((string) ($row['source_payload'] ?? ''), true);
                if ($this->ebay_deletion_payload_matches_identifiers($decoded, $identifiers)) {
                    $candidate_rows[] = $row;
                }
            }
        }
        foreach ((array) $candidate_rows as $row) {
            $id = absint($row['id'] ?? 0);
            if ($id <= 0 || isset($item_rows[$id])) { continue; }
            $item_rows[$id] = $row;
            $identity = strtolower((string) ($row['creative_identity_hash'] ?? ''));
            if (preg_match('/^[a-f0-9]{64}$/', $identity)) { $identities[$identity] = $identity; }
        }

        $this->ebay_deletion_purge_partner_tables($identifiers, $identities, $counts);
        foreach ($identities as $identity) {
            $this->ebay_deletion_delete_by_identity($identity, $counts);
        }
        foreach ($item_rows as $row) {
            $counts['posts'] += $this->ebay_deletion_delete_owned_post(absint($row['listing_post_id'] ?? 0), (string) ($row['creative_identity_hash'] ?? ''), (string) ($row['item_id'] ?? ''));
            $deleted = $wpdb->delete($table, array('id' => absint($row['id'])));
            $counts['items'] += is_numeric($deleted) ? absint($deleted) : 0;
        }
        $this->ebay_deletion_scrub_partner_options($identifiers);
        return $counts;
    }

    public function handle_ebay_account_deletion_notification($request) {
        $raw_body = is_object($request) && method_exists($request, 'get_body') ? (string) $request->get_body() : '';
        if ($raw_body === '' || strlen($raw_body) > 1048576) {
            return new WP_Error('ebay_deletion_payload_invalid', 'eBay-Benachrichtigung ist leer oder zu groß.', array('status' => 400));
        }
        $payload = json_decode($raw_body, true);
        if (!is_array($payload)) {
            return new WP_Error('ebay_deletion_json_invalid', 'eBay-Benachrichtigung enthält kein gültiges JSON.', array('status' => 400));
        }
        $extracted = $this->ebay_deletion_extract_notification($payload);
        if (is_wp_error($extracted)) {
            return new WP_Error($extracted->get_error_code(), $extracted->get_error_message(), array('status' => 400));
        }
        $notification_hash = (string) $extracted['notification_hash'];
        $header = is_object($request) && method_exists($request, 'get_header') ? (string) $request->get_header('x-ebay-signature') : '';
        $settings = $this->ebay_settings();
        // Auch idempotente Wiederholungen werden zuerst kryptografisch geprüft.
        // Eine bekannte notificationId darf niemals als Ersatz für eine gültige
        // eBay-Signatur dienen.
        $verified = $this->ebay_deletion_verify_signature($raw_body, $header, $settings);
        if (is_wp_error($verified)) {
            $status = in_array($verified->get_error_code(), array('ebay_deletion_signature_invalid','ebay_deletion_signature_missing','ebay_deletion_signature_header_base64','ebay_deletion_signature_header_json','ebay_deletion_signature_header_fields','ebay_deletion_signature_algorithm','ebay_deletion_signature_digest','ebay_deletion_digest_mismatch','ebay_deletion_signature_value_invalid'), true) ? 412 : 500;
            $this->ebay_deletion_update_state(array('last_notification_at'=>time(),'last_notification_status'=>'rejected','last_error'=>$verified->get_error_message()));
            return new WP_Error($verified->get_error_code(), $verified->get_error_message(), array('status' => $status));
        }
        if ($this->ebay_deletion_receipt_seen($notification_hash)) {
            return new WP_REST_Response(null, 204);
        }
        $counts = $this->ebay_deletion_irreversible_delete((array) $extracted['identifiers']);
        $this->ebay_deletion_store_receipt($notification_hash, $counts);
        $this->ebay_deletion_update_state(array(
            'last_notification_at' => time(),
            'last_notification_status' => 'verified',
            'last_notification_hash' => $notification_hash,
            'last_deleted_items' => absint($counts['items'] ?? 0),
            'last_deleted_creatives' => absint($counts['creatives'] ?? 0),
            'last_deleted_outputs' => absint($counts['outputs'] ?? 0),
            'last_error' => '',
        ));
        return new WP_REST_Response(null, 204);
    }

    public function maybe_enforce_ebay_deletion_compliance() {
        if (!method_exists($this, 'ebay_settings')) { return; }
        $settings = $this->ebay_settings();
        if ((string) ($settings['environment'] ?? 'production') !== 'production' || empty($settings['enabled'])) { return; }
        if ($this->ebay_deletion_compliance_complete()) { return; }
        $settings['enabled'] = false;
        update_option(self::OPTION_NETWORK_EBAY, $this->ebay_normalize_settings($settings, true), false);
        if (method_exists($this, 'provider_set_access_state')) {
            $this->provider_set_access_state('ebay', 'credentials_saved', 'eBay Production wurde bis zur vollständigen Marketplace-Account-Deletion-Compliance hart deaktiviert.');
        }
        if (function_exists('wp_clear_scheduled_hook')) {
            wp_clear_scheduled_hook(self::EBAY_CRON_HOOK);
        }
    }
}
