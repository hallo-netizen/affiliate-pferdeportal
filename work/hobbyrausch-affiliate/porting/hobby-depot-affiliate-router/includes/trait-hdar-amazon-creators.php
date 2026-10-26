<?php
if (!defined('ABSPATH')) { exit; }

/**
 * Amazon Creators API adapter for Hobby Depot.
 *
 * No credentials are committed. Constants can be used for secrets; WordPress
 * options are only a compatibility/configuration surface.
 */
trait HDAR_Amazon_Creators_Trait {
    private function amazon_creators_defaults() {
        return array(
            'enabled' => false,
            'marketplace' => 'www.amazon.de',
            'credential_version' => '3.2',
            'partner_tag' => '',
            'client_id' => '',
            'client_secret' => '',
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
}
