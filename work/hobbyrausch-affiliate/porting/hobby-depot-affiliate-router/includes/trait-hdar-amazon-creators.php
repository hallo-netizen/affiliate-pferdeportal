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

    private function amazon_creators_hobby_depot_concepts() {
        if (!function_exists('hd_category_registry_ready') || !hd_category_registry_ready()
            || !function_exists('hd_category_registry_snapshot')) {
            return new WP_Error('amazon_hobby_depot_registry_missing', 'Hobby-Depot-Kategorie-Registry ist nicht bereit.');
        }
        $snapshot = hd_category_registry_snapshot();
        if (!is_array($snapshot) || empty($snapshot['nodes']) || !is_array($snapshot['nodes'])) {
            return new WP_Error('amazon_hobby_depot_registry_invalid', 'Hobby-Depot-Kategorie-Snapshot ist leer oder ungültig.');
        }
        $mapping = is_array($snapshot['mapping'] ?? null) ? $snapshot['mapping'] : array();
        $nodes = array();
        $children = array();
        foreach ($snapshot['nodes'] as $node) {
            if (!is_array($node)) { continue; }
            $node_id = trim((string)($node['node_id'] ?? ''));
            if ($node_id === '' || sanitize_key((string)($node['status'] ?? 'active')) !== 'active') { continue; }
            $nodes[$node_id] = $node;
            $parent_id = trim((string)($node['parent_id'] ?? ''));
            if ($parent_id !== '') { $children[$parent_id][] = $node_id; }
        }
        $concepts = array();
        foreach ($nodes as $node_id => $node) {
            if (!preg_match('/^core:entity:[^:]+$/', $node_id)) { continue; }
            $title = trim((string)($node['display_name'] ?? $node['name'] ?? ''));
            $slug = sanitize_title((string)($node['slug'] ?? ''));
            if ($title === '' || $slug === '') { continue; }
            $parent = $nodes[(string)($node['parent_id'] ?? '')] ?? array();
            $grand = is_array($parent) ? ($nodes[(string)($parent['parent_id'] ?? '')] ?? array()) : array();
            $map = is_array($mapping[$node_id] ?? null) ? $mapping[$node_id] : array();
            $targets = array(array(
                'slug'=>$slug,
                'title'=>$title,
                'object_id'=>absint($map['object_id'] ?? 0),
                'object_type'=>sanitize_key((string)($map['object_type'] ?? $node['object_type'] ?? 'page')),
                'target_key'=>'page:' . $slug,
            ));
            foreach ((array)($children[$node_id] ?? array()) as $child_id) {
                $child = $nodes[$child_id] ?? null;
                if (!is_array($child)) { continue; }
                $child_slug = sanitize_title((string)($child['slug'] ?? ''));
                $child_title = trim((string)($child['display_name'] ?? $child['name'] ?? ''));
                if ($child_slug === '' || $child_title === '') { continue; }
                $child_map = is_array($mapping[$child_id] ?? null) ? $mapping[$child_id] : array();
                $targets[] = array(
                    'slug'=>$child_slug,
                    'title'=>$child_title,
                    'object_id'=>absint($child_map['object_id'] ?? 0),
                    'object_type'=>sanitize_key((string)($child_map['object_type'] ?? $child['object_type'] ?? 'category')),
                    'target_key'=>'category:' . $child_slug,
                );
            }
            $hub_slug = sanitize_title((string)($parent['slug'] ?? ''));
            $main_slug = sanitize_title((string)($grand['slug'] ?? ''));
            $target_keys = array('page:' . $slug);
            if ($hub_slug !== '') { $target_keys[] = 'page:' . $hub_slug; }
            if ($main_slug !== '') { $target_keys[] = 'page:' . $main_slug; }
            foreach ($targets as $target) {
                $key = sanitize_text_field((string)($target['target_key'] ?? ''));
                if ($key !== '') { $target_keys[] = $key; }
            }
            $concepts[] = array(
                'id'=>'hd-' . substr(hash('sha256', $node_id), 0, 20),
                'node_id'=>$node_id,
                'title'=>$title,
                'slug'=>$slug,
                'hub'=>trim((string)($parent['display_name'] ?? $parent['name'] ?? '')),
                'main_hub'=>trim((string)($grand['display_name'] ?? $grand['name'] ?? '')),
                'target_keys'=>array_values(array_unique(array_filter($target_keys))),
                'targets'=>$targets,
            );
        }
        usort($concepts, static function($a, $b) {
            return strcmp((string)($a['node_id'] ?? ''), (string)($b['node_id'] ?? ''));
        });
        return $concepts ?: new WP_Error('amazon_hobby_depot_concepts_empty', 'Hobby-Depot-Kategorie-Registry enthält keine aktiven Hobbyziele.');
    }

    private function amazon_creators_campaigns_should_be_active() {
        $s = $this->amazon_creators_settings();
        if (empty($s['enabled']) || !$this->amazon_creators_credentials_present($s)) { return false; }
        if (method_exists($this, 'provider_access_state')) {
            $state = $this->provider_access_state('amazon');
            if (sanitize_key((string)($state['status'] ?? '')) !== 'connected') { return false; }
        }
        if (method_exists($this, 'provider_channel_pause_gate') && is_wp_error($this->provider_channel_pause_gate('amazon'))) { return false; }
        return true;
    }

    private function amazon_creators_campaign_key($concept_id, $asin) {
        return sanitize_key('amazon-' . substr(hash('sha256', sanitize_key((string)$concept_id) . '|' . strtoupper(trim((string)$asin))), 0, 28));
    }

    private function amazon_creators_save_product_campaign($concept, $item) {
        if (!is_array($concept) || !is_array($item) || !method_exists($this, 'central_blank_campaign')
            || !method_exists($this, 'save_campaign_record') || !function_exists('get_posts')) {
            return new WP_Error('amazon_campaign_runtime_missing', 'Amazon-Kampagnenruntime fehlt.');
        }
        $concept_id = sanitize_key((string)($concept['id'] ?? ''));
        $asin = strtoupper(trim((string)($item['external_id'] ?? '')));
        $title = sanitize_text_field((string)($item['title'] ?? ''));
        $url = esc_url_raw((string)($item['url'] ?? ''));
        $image = esc_url_raw((string)($item['image_url'] ?? ''));
        if ($concept_id === '' || $asin === '' || $title === '' || $url === '' || $image === '') {
            return new WP_Error('amazon_campaign_item_incomplete', 'Amazon-Produkt ist für eine sichtbare Produktkarte unvollständig.');
        }
        $external_key = $concept_id . ':' . $asin;
        $ids = get_posts(array(
            'post_type'=>self::CAMPAIGN_POST_TYPE,
            'post_status'=>array('publish','draft','private'),
            'meta_key'=>'_hdar_amazon_external_key',
            'meta_value'=>$external_key,
            'posts_per_page'=>1,
            'fields'=>'ids',
        ));
        $post_id = $ids ? absint($ids[0]) : 0;
        $campaign = $this->central_blank_campaign();
        $campaign['id'] = $this->amazon_creators_campaign_key($concept_id, $asin);
        $campaign['name'] = 'Amazon – ' . $title;
        $campaign['partner'] = 'Amazon';
        $campaign['creative_type'] = 'product';
        $campaign['network'] = 'amazon';
        $campaign['programme_name'] = 'Amazon Associates / Creators API';
        $campaign['programme_status'] = 'active';
        $campaign['programme_status_source'] = 'amazon_creators_api';
        $campaign['programme_status_checked_at'] = time();
        $campaign['quality_manual_status'] = 'auto_verified';
        $campaign['quality_note'] = 'Hobby-Depot-Registry + Amazon Creators SearchItems + ASIN.';
        $campaign['render_mode'] = 'image_link';
        $campaign['active'] = $this->amazon_creators_campaigns_should_be_active();
        $campaign['assignment_mode'] = 'page_tree';
        $campaign['match_descendants'] = false;
        $campaign['automation_target_keys'] = array_values(array_unique(array_filter(array_map('sanitize_text_field', (array)($concept['target_keys'] ?? array())))));
        $campaign['placements'] = array(
            'hub_product_1','hub_product_2','hub_product_3',
            'category_product_1','category_product_2','category_product_3',
            'journal_product_1','journal_product_2','journal_product_3',
            'post_bottom_products'
        );
        $campaign['priority'] = 92;
        $campaign['label'] = 'Amazon · Affiliate';
        $campaign['title'] = $title;
        $campaign['description'] = '';
        $campaign['button_text'] = 'Bei Amazon ansehen';
        $campaign['image_url'] = $image;
        $campaign['url'] = $url;
        $campaign['target'] = '_blank';
        $campaign['price'] = sanitize_text_field((string)($item['price'] ?? ''));
        $campaign['currency'] = sanitize_text_field((string)($item['currency'] ?? ''));
        $campaign['availability'] = 'available';
        $campaign['health_check_enabled'] = false;
        $campaign['source'] = 'amazon_creators_searchitems_v1';
        $campaign['last_synced'] = time();
        $campaign['external_id'] = $asin;
        $campaign['product_asins'] = array($asin);
        $campaign['product_gtins'] = array();
        $campaign['product_identity_source'] = 'asin';
        $campaign['product_provider'] = 'amazon';

        $saved = $this->save_campaign_record($campaign, $post_id);
        if (is_wp_error($saved) || !$saved) {
            return is_wp_error($saved) ? $saved : new WP_Error('amazon_campaign_save_failed', 'Amazon-Produktkampagne konnte nicht gespeichert werden.');
        }
        $post_id = absint($saved);
        update_post_meta($post_id, '_hdar_amazon_auto', 1);
        update_post_meta($post_id, '_hdar_amazon_external_key', $external_key);
        update_post_meta($post_id, '_hdar_amazon_concept_id', $concept_id);
        delete_post_meta($post_id, '_ppar_product_asin');
        add_post_meta($post_id, '_ppar_product_asin', $asin, false);
        return $post_id;
    }

    private function amazon_creators_retire_missing_for_concept($concept_id, $selected_external_keys) {
        if (!function_exists('get_posts') || !method_exists($this, 'campaign_from_post') || !method_exists($this, 'save_campaign_record')) { return 0; }
        $concept_id = sanitize_key((string)$concept_id);
        $selected_external_keys = array_fill_keys(array_map('strval', (array)$selected_external_keys), true);
        $ids = get_posts(array(
            'post_type'=>self::CAMPAIGN_POST_TYPE,
            'post_status'=>array('publish','draft','private'),
            'meta_key'=>'_hdar_amazon_concept_id',
            'meta_value'=>$concept_id,
            'posts_per_page'=>-1,
            'fields'=>'ids',
        ));
        $retired = 0;
        foreach ((array)$ids as $id) {
            $id = absint($id);
            $external_key = (string)get_post_meta($id, '_hdar_amazon_external_key', true);
            if (isset($selected_external_keys[$external_key])) { continue; }
            $campaign = $this->campaign_from_post(get_post($id));
            if (!is_array($campaign) || empty($campaign['active'])) { continue; }
            $campaign['active'] = false;
            if ($this->save_campaign_record($campaign, $id)) { $retired++; }
        }
        return $retired;
    }

    private function amazon_creators_sync_hobby_depot_products($batch_size = 8) {
        $s = $this->amazon_creators_settings();
        if (empty($s['enabled'])) { return new WP_Error('amazon_creators_disabled', 'Amazon Creators API ist für Hobby Depot nicht aktiviert.'); }
        if (!$this->amazon_creators_credentials_present($s)) { return new WP_Error('amazon_creators_credentials_missing', 'Amazon Creators API: Zugangsdaten fehlen.'); }
        $state = method_exists($this, 'provider_access_state') ? $this->provider_access_state('amazon') : array();
        if (sanitize_key((string)($state['status'] ?? $s['last_status'] ?? '')) !== 'connected') {
            return new WP_Error('amazon_creators_connection_unverified', 'Amazon Creators API muss vor der Produktsynchronisierung erfolgreich geprüft werden.');
        }

        $concepts = $this->amazon_creators_hobby_depot_concepts();
        if (is_wp_error($concepts)) { return $concepts; }
        $count = count($concepts);
        $batch_size = max(1, min(20, absint($batch_size)));
        $cursor = absint($s['sync_cursor'] ?? 0);
        if ($cursor >= $count) { $cursor = 0; }
        $processed = 0; $searched = 0; $saved_count = 0; $retired = 0; $skipped = 0; $errors = array();

        while ($processed < $batch_size && $processed < $count) {
            $index = ($cursor + $processed) % $count;
            $concept = $concepts[$index];
            $query = trim(sanitize_text_field((string)($concept['title'] ?? '')));
            if ($query === '') { $processed++; $skipped++; continue; }
            $items = $this->amazon_creators_search($query, 10);
            $searched++;
            if (is_wp_error($items)) {
                $errors[] = sanitize_text_field($query . ': ' . $items->get_error_message());
                $processed++;
                continue;
            }
            $selected = array();
            foreach ((array)$items as $item) {
                if (!is_array($item)) { continue; }
                $asin = strtoupper(trim((string)($item['external_id'] ?? '')));
                if ($asin === '') { continue; }
                $saved = $this->amazon_creators_save_product_campaign($concept, $item);
                if (is_wp_error($saved)) { $skipped++; continue; }
                $selected[] = sanitize_key((string)($concept['id'] ?? '')) . ':' . $asin;
                $saved_count++;
            }
            $retired += $this->amazon_creators_retire_missing_for_concept((string)($concept['id'] ?? ''), $selected);
            $processed++;
        }

        $next = ($cursor + $processed) % max(1, $count);
        $s = $this->amazon_creators_settings();
        $s['sync_cursor'] = $next;
        $s['last_sync_at'] = time();
        $s['last_sync_count'] = $saved_count;
        $s['last_message'] = sprintf('Amazon Creators: %d Hobbykonzepte geprüft, %d Produktkampagnen gespeichert, %d alte Kampagnen deaktiviert.', $processed, $saved_count, $retired);
        update_option('hdar_amazon_creators_v1', $s, false);
        if ($saved_count > 0 && method_exists($this, 'article_plan_bump_campaign_revision')) {
            $this->article_plan_bump_campaign_revision('amazon_creators_materialized');
        }
        return array(
            'status'=>'success',
            'message'=>$s['last_message'],
            'counts'=>array('concepts'=>$processed,'searches'=>$searched,'campaigns'=>$saved_count,'retired'=>$retired,'skipped'=>$skipped,'errors'=>count($errors)),
            'details'=>array('cursor_before'=>$cursor,'cursor_after'=>$next,'total_concepts'=>$count,'errors'=>array_slice($errors,0,10),'public_activation'=>$this->amazon_creators_campaigns_should_be_active()),
        );
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
