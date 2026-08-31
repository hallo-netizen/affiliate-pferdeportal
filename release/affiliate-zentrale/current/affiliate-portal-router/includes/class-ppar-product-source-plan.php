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

    public static function bootstrap() {
        if (self::$booted) { return; }
        self::$booted = true;
        add_filter('ppar_affiliate_provider_registry', array(__CLASS__, 'extend_provider_registry'), 40, 2);
        add_filter('ppar_partner_analytics_providers', array(__CLASS__, 'extend_partner_analytics'), 40, 2);
        add_filter('ppar_partner_analytics_campaign_provider_key', array(__CLASS__, 'map_campaign_provider'), 40, 3);
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
                'activation'=>'read-only Marketplace + bestätigte Partnerschaft + echte Vendor-Werbemittel',
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
}
