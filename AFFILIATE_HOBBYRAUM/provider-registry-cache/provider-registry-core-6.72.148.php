<?php
if (!defined('ABSPATH')) {
    exit;
}
trait PPAR_Provider_Registry_Trait {
    /**
     * V6.72.148: Provider definitions are immutable during a normal public
     * frontend request. Rebuilding and sanitizing the full registry for every
     * campaign gate caused millions of redundant sanitize_* calls on leaf pages.
     * Keep admin/AJAX/cron/REST/WP-CLI uncached so operational/adaptor tooling
     * retains its existing per-call filter behaviour.
     */
    private $provider_registry_request_cache = null;

    private function provider_registry_request_cache_allowed() {
        if ((function_exists('is_admin') && is_admin())
            || (defined('DOING_CRON') && DOING_CRON)
            || (defined('REST_REQUEST') && REST_REQUEST)
            || (defined('WP_CLI') && WP_CLI)
            || (function_exists('wp_doing_ajax') && wp_doing_ajax())) {
            return false;
        }
        return true;
    }

    private function provider_registry_defaults() {
        return array(
            'awin' => array(
                'label' => 'Awin',
                'state' => 'active',
                'access_owner' => 'core',
                'specialist_menu' => true,
                'specialist_slug' => 'affiliate-portal-provider-awin',
                'capabilities' => array('credentials','connection_test','programmes','partners','offers','product_feeds','synchronization','automation','creatives','outputs','veto'),
            ),
            'adcell' => array(
                'label' => 'ADCELL',
                'state' => 'active',
                'access_owner' => 'core',
                'specialist_menu' => true,
                'specialist_slug' => 'affiliate-portal-provider-adcell',
                'capabilities' => array('credentials','connection_test','programmes','partners','product_feeds','synchronization','automation','creatives','outputs','veto'),
            ),
            'ebay' => array(
                'label' => 'eBay',
                'state' => 'active',
                'access_owner' => 'core',
                'specialist_menu' => true,
                'specialist_slug' => 'affiliate-portal-ebay',
                'capabilities' => array('credentials','connection_test','marketplace','account_deletion_notifications','partners','private_listings','business_products','synchronization','automation','creatives','outputs','veto'),
            ),
            'amazon' => array(
                'label' => 'Amazon',
                'state' => 'prepared',
                'access_owner' => 'adapter',
                'specialist_menu' => false,
                'specialist_slug' => 'affiliate-portal-provider-amazon',
                'capabilities' => array('creatives','outputs','veto'),
            ),
            'idealo' => array(
                'label' => 'idealo',
                'state' => 'active',
                'access_owner' => 'adapter',
                'specialist_menu' => true,
                'specialist_slug' => 'affiliate-portal-provider-idealo',
                'capabilities' => array('credentials','connection_test','product_feeds','synchronization','creatives','outputs','veto'),
            ),
            'direct' => array(
                'label' => 'Direktpartner',
                'state' => 'active',
                'access_owner' => 'none',
                'specialist_menu' => false,
                'specialist_slug' => '',
                'capabilities' => array('partners','creatives','outputs','veto'),
            ),
            'manual' => array(
                'label' => 'Manuell',
                'state' => 'active',
                'access_owner' => 'none',
                'specialist_menu' => false,
                'specialist_slug' => '',
                'capabilities' => array('creatives','outputs','veto'),
            ),
        );
    }

    public function provider_registry() {
        $cache_allowed = $this->provider_registry_request_cache_allowed();
        if ($cache_allowed && is_array($this->provider_registry_request_cache)) {
            return $this->provider_registry_request_cache;
        }
        $raw = apply_filters('ppar_affiliate_provider_registry', $this->provider_registry_defaults(), self::PROVIDER_CONTRACT_VERSION);
        $raw = is_array($raw) ? $raw : array();
        $safe = array();
        foreach ($raw as $key => $provider) {
            $key = sanitize_key((string) $key);
            if ($key === '' || !is_array($provider)) { continue; }
            $caps = array_values(array_unique(array_filter(array_map('sanitize_key', (array) ($provider['capabilities'] ?? array())))));
            // Chef-Veto ist Bestandteil des Kernvertrags und darf von keinem Adapter entfernt werden.
            if (!in_array('veto', $caps, true)) { $caps[] = 'veto'; }
            $state = sanitize_key((string) ($provider['state'] ?? 'prepared'));
            if (!in_array($state, array('active','prepared','disabled'), true)) { $state = 'prepared'; }
            $access_owner = sanitize_key((string) ($provider['access_owner'] ?? 'adapter'));
            if (!in_array($access_owner, array('core','adapter','none'), true)) { $access_owner = 'adapter'; }
            $safe[$key] = array(
                'key' => $key,
                'label' => sanitize_text_field((string) ($provider['label'] ?? strtoupper($key))),
                'state' => $state,
                'access_owner' => $access_owner,
                'specialist_menu' => !empty($provider['specialist_menu']),
                'specialist_slug' => sanitize_key((string) ($provider['specialist_slug'] ?? '')),
                'capabilities' => $caps,
            );
        }
        if ($cache_allowed) {
            $this->provider_registry_request_cache = $safe;
        }
        return $safe;
    }

    public function provider_definition($provider) {
        $provider = sanitize_key((string) $provider);
        $registry = $this->provider_registry();
        return isset($registry[$provider]) ? $registry[$provider] : null;
    }

    public function provider_exists($provider) {
        return is_array($this->provider_definition($provider));
    }

    public function provider_supports($provider, $capability) {
        $definition = $this->provider_definition($provider);
        return is_array($definition) && in_array(sanitize_key((string) $capability), (array) $definition['capabilities'], true);
    }

    public function provider_label($provider) {
        $definition = $this->provider_definition($provider);
        return is_array($definition) ? (string) $definition['label'] : strtoupper(sanitize_key((string) $provider));
    }
}
