<?php
if (!defined('ABSPATH')) { exit; }

/**
 * Explicit provider/source plan for the bundled Affiliate-Zentrale update.
 *
 * Product sources and banner/partner networks are deliberately separated.
 * Prepared providers expose only their future contract; no undocumented API,
 * feed shape or credential requirement is invented.
 */
final class PPAR_Affiliate_Source_Plan {
    const CONTRACT_VERSION = '1.0';
    private static $booted = false;
    private static $auto_banner_candidates = array();

    public static function bootstrap() {
        if (self::$booted) { return; }
        self::$booted = true;
        add_filter('ppar_affiliate_provider_registry', array(__CLASS__, 'extend_provider_registry'), 40, 2);
        add_filter('ppar_partner_analytics_providers', array(__CLASS__, 'extend_partner_analytics'), 40, 2);
        add_filter('ppar_partner_analytics_campaign_provider_key', array(__CLASS__, 'map_campaign_provider'), 40, 3);

        // Existing output planning already proves target + slot + asset + tracking.
        // Capture only campaigns touched in this request and activate them at shutdown
        // after the output-object transaction has finished. This avoids reviving old
        // drafts and never bypasses the existing classifier/materializer.
        add_action('save_post_ap_campaign', array(__CLASS__, 'capture_banner_candidate'), 100, 3);
        add_action('shutdown', array(__CLASS__, 'activate_verified_banner_candidates'), 1000);
    }

    public static function product_sources() {
        return array(
            'ebay' => array(
                'label'=>'eBay','state'=>'active','route'=>'direkter eBay-Provider',
                'purpose'=>'Produktquelle & Deals','activation'=>'aktiv',
            ),
            'idealo' => array(
                'label'=>'idealo','state'=>'active','route'=>'idealo-Feed/API',
                'purpose'=>'Preisvergleich & Produktquelle','activation'=>'aktiv',
            ),
            'otto' => array(
                'label'=>'OTTO','state'=>'prepared','route'=>'Awin → fachlich OTTO',
                'purpose'=>'Produktquelle & Deals','activation'=>'nach echter Programmfreigabe / nutzbarem Feed',
            ),
            'kaufland' => array(
                'label'=>'Kaufland','state'=>'prepared','route'=>'Lead Alliance / Kaufland Private Network',
                'purpose'=>'Produktquelle & Deals','activation'=>'nach echter Publisherfreigabe und bestätigter Datenquelle',
                'note'=>'Nicht über ADCocktail verdrahten.',
            ),
            'kelkoo' => array(
                'label'=>'Kelkoo','state'=>'prepared','route'=>'Kelkoo Publisher-/Produktdatenzugang',
                'purpose'=>'Preis-/Dealquelle','activation'=>'nach echter Freigabe und bestätigter Schnittstelle',
            ),
            'amazon' => array(
                'label'=>'Amazon','state'=>'prepared','route'=>'Amazon Associates / zulässiger Produktdatenzugang',
                'purpose'=>'Produktquelle & Deals','activation'=>'bewusst letzter Rollout; erst nach echtem Zugang',
            ),
        );
    }

    public static function banner_networks() {
        return array(
            'awin' => array('label'=>'Awin','state'=>'active','purpose'=>'Banner-/Partnernetzwerk'),
            'adcell' => array('label'=>'ADCELL','state'=>'active','purpose'=>'Banner-/Partnernetzwerk'),
            'adcocktail' => array(
                'label'=>'ADCocktail','state'=>'prepared','purpose'=>'Banner-/Partnernetzwerk',
                'activation'=>'CSV/XML/API erst nach bestätigtem Publisher-Schnittstellenvertrag anbinden',
            ),
            'digistore24' => array(
                'label'=>'Digistore24','state'=>'active','purpose'=>'Banner-/Partnernetzwerk',
                'activation'=>'bestehende read-only Verbindung + bestätigte Partnerschaft + echte Vendor-Werbemittel; verifizierte Banner automatisch auf passenden Slot aktivieren',
            ),
            'direct' => array('label'=>'Direktpartner','state'=>'active','purpose'=>'Banner-/Partnernetzwerk'),
        );
    }

    public static function extend_provider_registry($registry, $contract_version = '') {
        $registry = is_array($registry) ? $registry : array();

        // Amazon already exists in the core registry. Extend only its prepared
        // capability contract; the real adapter remains absent until real access exists.
        $amazon = isset($registry['amazon']) && is_array($registry['amazon']) ? $registry['amazon'] : array();
        $registry['amazon'] = array_merge(array(
            'label'=>'Amazon','state'=>'prepared','access_owner'=>'adapter',
            'specialist_menu'=>false,'specialist_slug'=>'affiliate-portal-provider-amazon',
        ), $amazon, array(
            'state'=>'prepared','access_owner'=>'adapter','specialist_menu'=>false,
            'capabilities'=>array('credentials','connection_test','product_feeds','synchronization','outputs','veto'),
        ));

        $registry['otto'] = array(
            'label'=>'OTTO','state'=>'prepared','access_owner'=>'none',
            'specialist_menu'=>false,'specialist_slug'=>'',
            'capabilities'=>array('product_feeds','synchronization','outputs','veto'),
        );
        $registry['kelkoo'] = array(
            'label'=>'Kelkoo','state'=>'prepared','access_owner'=>'adapter',
            'specialist_menu'=>false,'specialist_slug'=>'affiliate-portal-provider-kelkoo',
            'capabilities'=>array('credentials','connection_test','product_feeds','synchronization','outputs','veto'),
        );
        $registry['kaufland'] = array(
            'label'=>'Kaufland','state'=>'prepared','access_owner'=>'adapter',
            'specialist_menu'=>false,'specialist_slug'=>'affiliate-portal-provider-kaufland',
            'capabilities'=>array('credentials','connection_test','product_feeds','synchronization','outputs','veto'),
        );
        $registry['adcocktail'] = array(
            'label'=>'ADCocktail','state'=>'prepared','access_owner'=>'adapter',
            'specialist_menu'=>false,'specialist_slug'=>'affiliate-portal-provider-adcocktail',
            'capabilities'=>array('credentials','connection_test','programmes','partners','automation','creatives','outputs','veto'),
        );
        return $registry;
    }

    public static function extend_partner_analytics($providers, $contract_version = '') {
        $providers = is_array($providers) ? $providers : array();
        $providers['kaufland'] = array(
            'label'=>'Kaufland','type'=>'Produktquelle','state'=>'prepared','source_network'=>'leadalliance',
        );
        $providers['adcocktail'] = array(
            'label'=>'ADCocktail','type'=>'Banner-/Partnernetzwerk','state'=>'prepared','source_network'=>'adcocktail',
        );
        return $providers;
    }

    public static function map_campaign_provider($key, $campaign, $contract_version = '') {
        $campaign = is_array($campaign) ? $campaign : array();
        $network = sanitize_key((string)($campaign['network'] ?? ''));
        $identity = strtolower(implode(' ', array_filter(array_map('strval', array(
            $campaign['name'] ?? '', $campaign['title'] ?? '', $campaign['partner_name'] ?? '',
            $campaign['merchant_name'] ?? '', $campaign['advertiser_name'] ?? '', $campaign['programme_name'] ?? '',
        )))));
        if ($network === 'leadalliance' && strpos($identity, 'kaufland') !== false) { return 'kaufland'; }
        if ($network === 'adcocktail') { return 'adcocktail'; }
        return $key;
    }

    public static function capture_banner_candidate($post_id, $post = null, $update = false) {
        $post_id = absint($post_id);
        if ($post_id <= 0) { return; }
        if (is_object($post) && isset($post->post_type) && (string)$post->post_type !== 'ap_campaign') { return; }
        self::$auto_banner_candidates[$post_id] = time();
    }

    private static function emergency_stop_active() {
        $settings = get_option('ppar_control_settings_v1', array());
        return is_array($settings) && !empty($settings['emergency_stop']);
    }

    private static function active_banner_provider($provider) {
        $provider = sanitize_key((string)$provider);
        $networks = self::banner_networks();
        return isset($networks[$provider])
            && sanitize_key((string)($networks[$provider]['state'] ?? 'prepared')) === 'active';
    }

    private static function same_url($a, $b) {
        $a = esc_url_raw((string)$a);
        $b = esc_url_raw((string)$b);
        return $a !== '' && $b !== '' && hash_equals($a, $b);
    }

    public static function activate_verified_banner_candidates() {
        if (!self::$auto_banner_candidates || self::emergency_stop_active()) { return; }
        if (!function_exists('get_post_meta') || !function_exists('update_post_meta')) { return; }
        global $wpdb;
        if (!is_object($wpdb) || !method_exists($wpdb, 'prepare') || !method_exists($wpdb, 'get_row') || !method_exists($wpdb, 'update')) { return; }

        $table = $wpdb->base_prefix . 'ppar_output_objects';
        foreach (array_slice(array_keys(self::$auto_banner_candidates), 0, 50) as $post_id) {
            $post_id = absint($post_id);
            $captured_at = absint(self::$auto_banner_candidates[$post_id] ?? 0);
            if ($post_id <= 0 || $captured_at <= 0) { continue; }

            $campaign = get_post_meta($post_id, 'ppar_campaign_data', true);
            if (!is_array($campaign) || !empty($campaign['active'])) { continue; }
            if (sanitize_key((string)($campaign['source'] ?? '')) !== 'output_object_v4') { continue; }
            if (sanitize_key((string)($campaign['render_mode'] ?? '')) !== 'image_link') { continue; }

            $provider = sanitize_key((string)($campaign['network'] ?? ''));
            if (!self::active_banner_provider($provider)) { continue; }

            $object = $wpdb->get_row($wpdb->prepare(
                "SELECT * FROM {$table} WHERE campaign_post_id=%d AND output_type='portal_banner' ORDER BY updated_at DESC, id DESC LIMIT 1",
                $post_id
            ), ARRAY_A);
            if (!is_array($object)) { continue; }
            if (sanitize_key((string)($object['provider'] ?? '')) !== $provider) { continue; }
            if (sanitize_key((string)($object['status'] ?? '')) !== 'draft') { continue; }
            if (absint($object['updated_at'] ?? 0) + 2 < $captured_at) { continue; }
            if (trim((string)($object['target_key'] ?? '')) === '' || sanitize_key((string)($object['slot_id'] ?? '')) === '') { continue; }
            if (absint($object['image_width'] ?? 0) <= 0 || absint($object['image_height'] ?? 0) <= 0) { continue; }
            $image_hash = strtolower(trim((string)($object['image_hash'] ?? '')));
            if (!preg_match('/^[a-f0-9]{64}$/', $image_hash)) { continue; }
            if (!self::same_url($object['tracking_url'] ?? '', $campaign['url'] ?? '')) { continue; }
            if (!self::same_url($object['image_url'] ?? '', $campaign['image_url'] ?? '')) { continue; }

            $targets = array_values(array_filter(array_map('strval', (array)($campaign['automation_target_keys'] ?? array()))));
            $placements = array_values(array_filter(array_map('sanitize_key', (array)($campaign['placements'] ?? array()))));
            if (!in_array((string)$object['target_key'], $targets, true)) { continue; }
            if (!in_array(sanitize_key((string)$object['slot_id']), $placements, true)) { continue; }

            // Digistore24 is additionally constrained to the validated DS24 tracking host.
            if ($provider === 'digistore24') {
                $host = strtolower((string)wp_parse_url((string)($campaign['url'] ?? ''), PHP_URL_HOST));
                if (!in_array($host, array('checkout-ds24.com','www.checkout-ds24.com'), true)) { continue; }
            }

            $campaign['active'] = true;
            if (update_post_meta($post_id, 'ppar_campaign_data', $campaign) === false) {
                $roundtrip = get_post_meta($post_id, 'ppar_campaign_data', true);
                if (!is_array($roundtrip) || empty($roundtrip['active'])) { continue; }
            }

            $wpdb->update($table, array(
                'status'=>'published',
                'decision_source'=>'automatic_banner_network',
                'decision_reason'=>'Verifiziertes Banner automatisch auf dem bereits klassifizierten Ziel und Slot aktiviert.',
                'last_verified'=>time(),
                'updated_at'=>time(),
            ), array('id'=>absint($object['id'] ?? 0)));
        }
        self::$auto_banner_candidates = array();
    }
}
