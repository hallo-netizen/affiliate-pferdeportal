<?php
if (!defined('ABSPATH')) { exit; }

/**
 * Amazon Creators API adapter for Hobby Depot.
 *
 * No credentials are committed. Constants can be used for secrets; WordPress
 * options are only a compatibility/configuration surface.
 */
trait HDAR_Amazon_Creators_Trait {
    public function amazon_creators_register_hooks() {
        add_filter('ppar_affiliate_provider_access_snapshot', array($this, 'amazon_creators_provider_access_snapshot'), 10, 4);
        add_filter('ppar_affiliate_provider_access_save', array($this, 'amazon_creators_provider_access_save'), 10, 4);
        add_filter('ppar_affiliate_provider_access_test', array($this, 'amazon_creators_provider_access_test'), 10, 3);
        add_filter('ppar_affiliate_provider_sync_dispatch', array($this, 'amazon_creators_sync_dispatch'), 10, 4);
        add_action('ppar_affiliate_render_provider_access_card_amazon', array($this, 'amazon_creators_render_access_card'), 10, 3);
    }

    private function amazon_creators_defaults() {
        return array(
            'enabled' => false,
            'marketplace' => 'www.amazon.de',
            'credential_version' => '3.2',
            'partner_tag' => '',
            'client_id' => '',
            'client_secret' => '',
            'last_status' => 'not_configured',
            'last_checked' => 0,
            'last_message' => '',
            'sync_cursor' => 0,
            'last_sync_at' => 0,
            'last_sync_count' => 0,
        );
    }

    private function amazon_creators_settings() {
        $s = get_option('hdar_amazon_creators_v1', array());
        $s = is_array($s) ? array_merge($this->amazon_creators_defaults(), $s) : $this->amazon_creators_defaults();
        if (defined('HDAR_AMAZON_CREATORS_CLIENT_ID') && HDAR_AMAZON_CREATORS_CLIENT_ID) {
            $s['client_id'] = (string) HDAR_AMAZON_CREATORS_CLIENT_ID;
        }
        if (defined('HDAR_AMAZON_CREATORS_CLIENT_SECRET') && HDAR_AMAZON_CREATORS_CLIENT_SECRET) {
            $s['client_secret'] = (string) HDAR_AMAZON_CREATORS_CLIENT_SECRET;
        }
        if (defined('HDAR_AMAZON_PARTNER_TAG') && HDAR_AMAZON_PARTNER_TAG) {
            $s['partner_tag'] = (string) HDAR_AMAZON_PARTNER_TAG;
        }
        $s['marketplace'] = strtolower(trim((string)$s['marketplace']));
        if (!in_array($s['marketplace'], array('www.amazon.de','www.amazon.co.uk','www.amazon.fr','www.amazon.it','www.amazon.es','www.amazon.nl','www.amazon.be'), true)) {
            $s['marketplace'] = 'www.amazon.de';
        }
        $s['credential_version'] = trim((string)$s['credential_version']);
        return $s;
    }

    private function amazon_creators_credentials_present($settings = null) {
        $s = is_array($settings) ? $settings : $this->amazon_creators_settings();
        return trim((string)($s['partner_tag'] ?? '')) !== ''
            && trim((string)($s['client_id'] ?? '')) !== ''
            && trim((string)($s['client_secret'] ?? '')) !== '';
    }

    public function amazon_creators_provider_access_snapshot($snapshot, $provider, $definition, $contract_version) {
        if ($provider !== 'amazon') { return $snapshot; }
        $s = $this->amazon_creators_settings();
        $state = method_exists($this, 'provider_access_state') ? $this->provider_access_state('amazon') : array();
        $configured = $this->amazon_creators_credentials_present($s);
        $status = sanitize_key((string)($state['status'] ?? $s['last_status'] ?? ($configured ? 'credentials_saved' : 'not_configured')));
        if (!$configured) { $status = 'not_configured'; }
        return array_merge(is_array($snapshot) ? $snapshot : array(), array(
            'provider' => 'amazon',
            'label' => 'Amazon',
            'state' => 'adapter_ready',
            'configured' => $configured,
            'enabled' => !empty($s['enabled']),
            'status' => $status,
            'last_checked' => absint($state['last_checked'] ?? $s['last_checked'] ?? 0),
            'message' => sanitize_text_field((string)($state['message'] ?? $s['last_message'] ?? '')),
        ));
    }

    public function amazon_creators_provider_access_save($handled, $provider, $raw, $contract_version) {
        if ($provider !== 'amazon') { return $handled; }
        $previous = $this->amazon_creators_settings();
        $raw = is_array($raw) ? $raw : array();
        $saved = $previous;
        $saved['enabled'] = !empty($raw['enabled']);
        $marketplace = strtolower(trim((string)($raw['marketplace'] ?? $previous['marketplace'] ?? 'www.amazon.de')));
        $allowed = array('www.amazon.de','www.amazon.co.uk','www.amazon.fr','www.amazon.it','www.amazon.es','www.amazon.nl','www.amazon.be');
        $saved['marketplace'] = in_array($marketplace, $allowed, true) ? $marketplace : 'www.amazon.de';
        $version = trim((string)($raw['credential_version'] ?? $previous['credential_version'] ?? '3.2'));
        $saved['credential_version'] = in_array($version, array('3.1','3.2','3.3'), true) ? $version : '3.2';
        if (!defined('HDAR_AMAZON_PARTNER_TAG')) {
            $saved['partner_tag'] = sanitize_text_field((string)($raw['partner_tag'] ?? $previous['partner_tag'] ?? ''));
        }
        if (!defined('HDAR_AMAZON_CREATORS_CLIENT_ID')) {
            $saved['client_id'] = sanitize_text_field((string)($raw['client_id'] ?? $previous['client_id'] ?? ''));
        }
        if (!defined('HDAR_AMAZON_CREATORS_CLIENT_SECRET')) {
            $secret = trim((string)($raw['client_secret'] ?? ''));
            if ($secret !== '') { $saved['client_secret'] = $secret; }
            if (!empty($raw['remove_client_secret'])) { $saved['client_secret'] = ''; }
        }
        $credentials_changed =
            (string)($saved['marketplace'] ?? '') !== (string)($previous['marketplace'] ?? '')
            || (string)($saved['credential_version'] ?? '') !== (string)($previous['credential_version'] ?? '')
            || (string)($saved['partner_tag'] ?? '') !== (string)($previous['partner_tag'] ?? '')
            || (string)($saved['client_id'] ?? '') !== (string)($previous['client_id'] ?? '')
            || (!defined('HDAR_AMAZON_CREATORS_CLIENT_SECRET') && trim((string)($raw['client_secret'] ?? '')) !== '')
            || !empty($raw['remove_client_secret']);
        if ($credentials_changed) {
            $saved['last_status'] = $this->amazon_creators_credentials_present($saved) ? 'credentials_saved' : 'not_configured';
            $saved['last_checked'] = 0;
            $saved['last_message'] = $this->amazon_creators_credentials_present($saved)
                ? 'Amazon-Creators-Zugang gespeichert; erneuter Verbindungstest erforderlich.'
                : 'Amazon-Creators-Zugang noch unvollständig.';
        }
        update_option('hdar_amazon_creators_v1', $saved, false);
        if (method_exists($this, 'provider_set_access_state')) {
            $this->provider_set_access_state('amazon',
                $this->amazon_creators_credentials_present($saved) ? (string)($saved['last_status'] ?? 'credentials_saved') : 'not_configured',
                (string)($saved['last_message'] ?? ''));
        }
        return $this->amazon_creators_settings();
    }

    public function amazon_creators_provider_access_test($handled, $provider, $contract_version) {
        if ($provider !== 'amazon') { return $handled; }
        $result = $this->amazon_creators_test_connection();
        $s = $this->amazon_creators_settings();
        $s['last_checked'] = time();
        if (is_wp_error($result)) {
            $s['last_status'] = 'failed';
            $s['last_message'] = sanitize_text_field($result->get_error_message());
            update_option('hdar_amazon_creators_v1', $s, false);
            if (method_exists($this, 'provider_set_access_state')) { $this->provider_set_access_state('amazon', 'failed', $s['last_message']); }
            return $result;
        }
        $s['last_status'] = 'connected';
        $s['last_message'] = 'Amazon Creators API erfolgreich authentifiziert.';
        update_option('hdar_amazon_creators_v1', $s, false);
        if (method_exists($this, 'provider_set_access_state')) { $this->provider_set_access_state('amazon', 'connected', $s['last_message']); }
        return array('status'=>'connected','message'=>$s['last_message']);
    }

    private function amazon_creators_token_endpoint($version) {
        $version = trim((string)$version);
        if ($version === '3.1') { return 'https://api.amazon.com/auth/o2/token'; }
        if ($version === '3.3') { return 'https://api.amazon.co.jp/auth/o2/token'; }
        return 'https://api.amazon.co.uk/auth/o2/token';
    }

    private function amazon_creators_access_token($settings = null) {
        $s = is_array($settings) ? $settings : $this->amazon_creators_settings();
        $id = trim((string)($s['client_id'] ?? ''));
        $secret = trim((string)($s['client_secret'] ?? ''));
        if ($id === '' || $secret === '') {
            return new WP_Error('amazon_creators_credentials_missing', 'Amazon Creators API: Zugangsdaten fehlen.');
        }

        $cache_key = 'hdar_amz_token_' . substr(hash('sha256', $id . '|' . (string)($s['credential_version'] ?? '3.2')), 0, 24);
        $cached = get_transient($cache_key);
        if (is_string($cached) && $cached !== '') { return $cached; }

        $response = wp_remote_post($this->amazon_creators_token_endpoint($s['credential_version'] ?? '3.2'), array(
            'timeout' => 20,
            'headers' => array('Content-Type' => 'application/json'),
            'body' => wp_json_encode(array(
                'grant_type' => 'client_credentials',
                'client_id' => $id,
                'client_secret' => $secret,
                'scope' => 'creatorsapi::default',
            )),
        ));
        if (is_wp_error($response)) { return $response; }
        $code = absint(wp_remote_retrieve_response_code($response));
        $body = json_decode((string)wp_remote_retrieve_body($response), true);
        if ($code < 200 || $code >= 300 || !is_array($body) || empty($body['access_token'])) {
            return new WP_Error('amazon_creators_oauth_failed', 'Amazon Creators API OAuth fehlgeschlagen (HTTP ' . $code . ').');
        }
        $token = (string)$body['access_token'];
        $ttl = max(60, absint($body['expires_in'] ?? 3600) - 120);
        set_transient($cache_key, $token, $ttl);
        return $token;
    }

    public function amazon_creators_search($keywords, $item_count = 10) {
        $s = $this->amazon_creators_settings();
        if (empty($s['enabled'])) {
            return new WP_Error('amazon_creators_disabled', 'Amazon Creators API ist für Hobby Depot nicht aktiviert.');
        }
        $keywords = trim(sanitize_text_field((string)$keywords));
        if ($keywords === '') {
            return new WP_Error('amazon_creators_query_missing', 'Amazon-Suchbegriff fehlt.');
        }
        $partner_tag = trim((string)($s['partner_tag'] ?? ''));
        if ($partner_tag === '') {
            return new WP_Error('amazon_creators_partner_tag_missing', 'Amazon Partner-Tag fehlt.');
        }

        $token = $this->amazon_creators_access_token($s);
        if (is_wp_error($token)) { return $token; }

        $payload = array(
            'partnerTag' => $partner_tag,
            'marketplace' => $s['marketplace'],
            'keywords' => $keywords,
            'searchIndex' => 'All',
            'itemCount' => min(10, max(1, absint($item_count))),
            'resources' => array(
                'images.primary.medium',
                'itemInfo.title',
                'itemInfo.externalIds',
                'itemInfo.features',
                'offersV2.listings.price',
            ),
        );
        $response = wp_remote_post('https://creatorsapi.amazon/catalog/v1/searchItems', array(
            'timeout' => 25,
            'headers' => array(
                'Authorization' => 'Bearer ' . $token,
                'Content-Type' => 'application/json',
                'x-marketplace' => $s['marketplace'],
            ),
            'body' => wp_json_encode($payload),
        ));
        if (is_wp_error($response)) { return $response; }
        $code = absint(wp_remote_retrieve_response_code($response));
        $body = json_decode((string)wp_remote_retrieve_body($response), true);
        if ($code < 200 || $code >= 300 || !is_array($body)) {
            return new WP_Error('amazon_creators_search_failed', 'Amazon Creators API Suche fehlgeschlagen (HTTP ' . $code . ').');
        }

        $items = array();
        foreach ((array)($body['searchResult']['items'] ?? array()) as $item) {
            if (!is_array($item)) { continue; }
            $asin = sanitize_text_field((string)($item['asin'] ?? ''));
            $url = esc_url_raw((string)($item['detailPageURL'] ?? ''));
            $title = sanitize_text_field((string)($item['itemInfo']['title']['displayValue'] ?? ''));
            if ($asin === '' || $url === '' || $title === '') { continue; }

            $image = esc_url_raw((string)($item['images']['primary']['medium']['url'] ?? ''));
            $price = '';
            $currency = '';
            $listing = $item['offersV2']['listings'][0] ?? array();
            if (is_array($listing)) {
                $price = (string)($listing['price']['amount'] ?? $listing['price']['displayAmount'] ?? '');
                $currency = sanitize_text_field((string)($listing['price']['currency'] ?? ''));
            }
            $items[] = array(
                'provider' => 'amazon',
                'external_id' => $asin,
                'title' => $title,
                'url' => $url,
                'image_url' => $image,
                'price' => sanitize_text_field($price),
                'currency' => $currency,
                'raw' => $item,
            );
        }
        return $items;
    }

    public function amazon_creators_test_connection() {
        $s = $this->amazon_creators_settings();
        if (trim((string)($s['partner_tag'] ?? '')) === '') {
            return new WP_Error('amazon_creators_partner_tag_missing', 'Amazon Partner-Tag fehlt.');
        }
        $token = $this->amazon_creators_access_token($s);
        if (is_wp_error($token)) { return $token; }
        return array('status' => 'connected', 'marketplace' => $s['marketplace'], 'partner_tag_present' => true);
    }

    public function amazon_creators_sync_dispatch($handled, $network, $operation, $contract_version) {
        if ($network !== 'amazon') { return $handled; }
        if ($operation === 'connection') {
            $test = $this->amazon_creators_provider_access_test(null, 'amazon', $contract_version);
            if (is_wp_error($test)) { return $test; }
            return array('status'=>'success','message'=>'Amazon-Creators-Verbindung geprüft.','counts'=>array(),'details'=>array('public_activation'=>false));
        }
        if ($operation !== 'products') {
            return new WP_Error('amazon_creators_sync_operation_unknown', 'Unbekannte Amazon-Synchronisationsaktion.');
        }
        if (!method_exists($this, 'amazon_creators_sync_hobby_depot_products')) {
            return new WP_Error('amazon_creators_sync_missing', 'Amazon-Produktsynchronisierung ist nicht verfügbar.');
        }
        return $this->amazon_creators_sync_hobby_depot_products();
    }

    public function amazon_creators_render_access_card($provider, $definition, $contract_version) {
        if ($provider !== 'amazon' || !current_user_can('manage_options')) { return; }
        $s = $this->amazon_creators_settings();
        $client_const = defined('HDAR_AMAZON_CREATORS_CLIENT_ID') && HDAR_AMAZON_CREATORS_CLIENT_ID;
        $secret_const = defined('HDAR_AMAZON_CREATORS_CLIENT_SECRET') && HDAR_AMAZON_CREATORS_CLIENT_SECRET;
        $tag_const = defined('HDAR_AMAZON_PARTNER_TAG') && HDAR_AMAZON_PARTNER_TAG;
        ?>
        <form method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>">
            <input type="hidden" name="action" value="ppar_provider_access_save">
            <input type="hidden" name="provider" value="amazon">
            <?php wp_nonce_field('ppar_provider_access_amazon','ppar_provider_nonce'); ?>
            <p><label><input type="checkbox" name="ppar_provider[amazon][enabled]" value="1" <?php checked(!empty($s['enabled'])); ?>> Amazon Creators API für Hobby Depot aktivieren</label></p>
            <p><label>Marketplace<br><select name="ppar_provider[amazon][marketplace]">
                <?php foreach (array('www.amazon.de','www.amazon.co.uk','www.amazon.fr','www.amazon.it','www.amazon.es','www.amazon.nl','www.amazon.be') as $marketplace) : ?>
                    <option value="<?php echo esc_attr($marketplace); ?>" <?php selected((string)$s['marketplace'],$marketplace); ?>><?php echo esc_html($marketplace); ?></option>
                <?php endforeach; ?>
            </select></label></p>
            <p><label>Credential-Version<br><select name="ppar_provider[amazon][credential_version]">
                <?php foreach (array('3.1','3.2','3.3') as $version) : ?><option value="<?php echo esc_attr($version); ?>" <?php selected((string)$s['credential_version'],$version); ?>><?php echo esc_html($version); ?></option><?php endforeach; ?>
            </select></label></p>
            <p><label>Partner-Tag <span class="ppar-saved"><?php echo esc_html($tag_const ? 'über wp-config.php' : ((string)($s['partner_tag'] ?? '') !== '' ? 'gespeichert' : 'nicht gespeichert')); ?></span><br>
                <input type="text" autocomplete="off" name="ppar_provider[amazon][partner_tag]" value="<?php echo esc_attr($tag_const ? '' : (string)($s['partner_tag'] ?? '')); ?>" placeholder="<?php echo esc_attr($tag_const ? 'über wp-config.php gesetzt' : ''); ?>">
            </label></p>
            <p><label>Credential-ID <span class="ppar-saved"><?php echo esc_html($client_const ? 'über wp-config.php' : ((string)($s['client_id'] ?? '') !== '' ? 'gespeichert' : 'nicht gespeichert')); ?></span><br>
                <input type="text" autocomplete="off" name="ppar_provider[amazon][client_id]" value="<?php echo esc_attr($client_const ? '' : (string)($s['client_id'] ?? '')); ?>" placeholder="<?php echo esc_attr($client_const ? 'über wp-config.php gesetzt' : ''); ?>">
            </label></p>
            <p><label>Credential-Secret <span class="ppar-saved"><?php echo esc_html($secret_const ? 'über wp-config.php' : ((string)($s['client_secret'] ?? '') !== '' ? 'gespeichert' : 'nicht gespeichert')); ?></span><br>
                <input type="password" autocomplete="new-password" name="ppar_provider[amazon][client_secret]" value="" placeholder="<?php echo esc_attr($secret_const ? 'über wp-config.php gesetzt' : 'leer lassen zum Beibehalten'); ?>">
            </label></p>
            <?php if (!$secret_const) : ?><details><summary>Zugangsdaten entfernen</summary><p><label><input type="checkbox" name="ppar_provider[amazon][remove_client_secret]" value="1"> Credential-Secret entfernen</label></p></details><?php endif; ?>
            <p class="description">Secrets werden nicht im Plugin oder in Projektdateien hinterlegt. wp-config.php-Konstanten haben Vorrang.</p>
            <p><button class="button button-primary" name="ppar_provider_action" value="save">Speichern</button> <button class="button" name="ppar_provider_action" value="save_test">Speichern &amp; Verbindung prüfen</button></p>
        </form>
        <?php
    }
}
