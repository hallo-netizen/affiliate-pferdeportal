<?php
if (!defined('ABSPATH')) { exit; }

/**
 * KISS navigation layer: fewer visible WordPress submenu entries while every
 * existing page, control, diagnostic and specialist screen remains registered
 * and directly reachable. This class changes navigation only, never domain logic.
 */
final class PPAR_Affiliate_Admin_KISS {
    private static $booted = false;

    public static function bootstrap() {
        if (self::$booted) { return; }
        self::$booted = true;
        add_action('admin_menu', array(__CLASS__, 'register_visible_navigation'), 10050);
        add_action('admin_head', array(__CLASS__, 'hide_legacy_navigation_css'), 10050);
    }

    private static function parent_slug() { return 'affiliate-portal-zentrale'; }

    private static function hidden_legacy_slugs() {
        return array(
            'affiliate-portal-creative-library','affiliate-portal-outputs','affiliate-portal-control',
            'affiliate-portal-creatives','affiliate-portal-assignments','affiliate-portal-preview',
            'affiliate-portal-ebay-business','affiliate-portal-coverage','affiliate-portal-article-hybrid',
            'affiliate-portal-networks','affiliate-portal-provider-awin','affiliate-portal-provider-adcell',
            'affiliate-portal-ebay','affiliate-portal-provider-idealo','affiliate-portal-provider-digistore24',
            'affiliate-portal-partners','affiliate-portal-sync','affiliate-portal-automation',
            'affiliate-portal-stats','affiliate-portal-health','affiliate-portal-deals'
        );
    }

    public static function register_visible_navigation() {
        if (!function_exists('add_submenu_page')) { return; }
        $parent = self::parent_slug();
        add_submenu_page($parent,'Produkte & Deals','Produkte & Deals','manage_options','affiliate-portal-kiss-products',array(__CLASS__,'render_products'));
        add_submenu_page($parent,'Partner & Einnahmen','Partner & Einnahmen','manage_options','affiliate-portal-kiss-partners',array(__CLASS__,'render_partners'));
        add_submenu_page($parent,'Ausspielung','Ausspielung','manage_options','affiliate-portal-kiss-delivery',array(__CLASS__,'render_delivery'));
        add_submenu_page($parent,'Anbieter & APIs','Anbieter & APIs','manage_options','affiliate-portal-kiss-providers',array(__CLASS__,'render_providers'));
        add_submenu_page($parent,'Steuerung & System','Steuerung & System','manage_options','affiliate-portal-kiss-system',array(__CLASS__,'render_system'));
    }

    /**
     * Hide legacy submenu links visually only. Never remove their WordPress
     * registration: the KISS buttons intentionally keep linking to these pages.
     * This preserves the 6.64.1 live navigation rootfix.
     */
    public static function hide_legacy_navigation_css() {
        if (!current_user_can('manage_options')) { return; }
        $selectors = array();
        foreach (self::hidden_legacy_slugs() as $slug) {
            $selectors[] = '#toplevel_page_' . self::parent_slug() . ' .wp-submenu a[href="admin.php?page=' . $slug . '"]';
            $selectors[] = '#toplevel_page_' . self::parent_slug() . ' .wp-submenu a[href$="page=' . $slug . '"]';
        }
        if (!$selectors) { return; }
        echo '<style id="ppar-kiss-legacy-nav-hide">' . implode(',', $selectors) . '{display:none!important}</style>';
    }

    private static function button($label, $slug, $primary = false) {
        $class = $primary ? 'button button-primary' : 'button';
        return '<a class="'.esc_attr($class).'" href="'.esc_url(admin_url('admin.php?page='.$slug)).'">'.esc_html($label).'</a>';
    }

    private static function header($title, $lead) {
        if (!current_user_can('manage_options')) { wp_die('Keine Berechtigung.'); }
        echo '<div class="wrap" style="max-width:1240px"><h1>'.esc_html($title).'</h1><p>'.esc_html($lead).'</p>';
    }

    private static function footer() { echo '</div>'; }

    private static function source_cards($sources) {
        echo '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(270px,1fr));gap:14px;margin:18px 0">';
        foreach ((array)$sources as $source) {
            if (!is_array($source)) { continue; }
            $state = sanitize_key((string)($source['state'] ?? 'prepared'));
            $label = (string)($source['label'] ?? 'Quelle');
            echo '<section class="postbox" style="padding:16px;margin:0"><h2 style="margin-top:0">'.esc_html($label).'</h2>';
            echo '<p><strong>'.esc_html($state === 'active' ? 'Aktiv' : 'Vorbereitet').'</strong></p>';
            if (!empty($source['purpose'])) { echo '<p>'.esc_html((string)$source['purpose']).'</p>'; }
            if (!empty($source['route'])) { echo '<p class="description">Technischer Weg: '.esc_html((string)$source['route']).'</p>'; }
            if (!empty($source['activation'])) { echo '<p class="description">Aktivierung: '.esc_html((string)$source['activation']).'</p>'; }
            if (!empty($source['note'])) { echo '<p><strong>'.esc_html((string)$source['note']).'</strong></p>'; }
            echo '</section>';
        }
        echo '</div>';
    }

    public static function render_products() {
        self::header('Produkte & Deals','Gesamtabdeckung statt eBay-Alleinabdeckung. Produktquellen bleiben strikt von Banner-Netzwerken getrennt.');
        if (class_exists('PPAR_Affiliate_Source_Plan')) { self::source_cards(PPAR_Affiliate_Source_Plan::product_sources()); }
        echo '<p style="display:flex;gap:8px;flex-wrap:wrap">';
        echo self::button('Produktquellen & Deal-Radar','affiliate-portal-deals',true);
        echo self::button('Import & Auswahl','affiliate-portal-creative-library');
        echo self::button('eBay Produktzuordnung','affiliate-portal-ebay-business');
        echo self::button('Portalabdeckung','affiliate-portal-coverage');
        echo self::button('Vorschau','affiliate-portal-preview');
        echo '</p>';
        self::footer();
    }

    public static function render_partners() {
        if (class_exists('PPAR_Partner_Analytics_Admin')) {
            PPAR_Partner_Analytics_Admin::render_page();
            return;
        }
        self::header('Partner & Einnahmen','Banner-/Partnernetzwerke, Produktquellen und echte Einnahmendaten an einer Stelle. Fehlende Werte werden nicht geschätzt.');
        if (class_exists('PPAR_Affiliate_Source_Plan')) {
            self::source_cards(array_merge(
                (array) PPAR_Affiliate_Source_Plan::product_sources(),
                (array) PPAR_Affiliate_Source_Plan::banner_networks()
            ));
        }
        echo '<p style="display:flex;gap:8px;flex-wrap:wrap">';
        echo self::button('Partner & Einnahmen','affiliate-portal-stats',true);
        echo self::button('Partner','affiliate-portal-partners');
        echo self::button('Werbemittel','affiliate-portal-creatives');
        echo self::button('Digistore24','affiliate-portal-provider-digistore24');
        echo '</p>';
        self::footer();
    }

    public static function render_delivery() {
        self::header('Ausspielung','Alle bisherigen Ausgabefunktionen bleiben erhalten; nur die Navigation ist zusammengefasst.');
        echo '<p style="display:flex;gap:8px;flex-wrap:wrap">';
        echo self::button('Ausgaben & Freigabe','affiliate-portal-outputs',true);
        echo self::button('Zuordnungen','affiliate-portal-assignments');
        echo self::button('Einzelbeiträge','affiliate-portal-article-hybrid');
        echo self::button('Vorschau','affiliate-portal-preview');
        echo '</p>';
        self::footer();
    }

    public static function render_providers() {
        self::header('Anbieter & APIs','Zugänge und technische Provider bleiben getrennt von der fachlichen Produkt-/Banner-Ausspielung.');
        echo '<p style="display:flex;gap:8px;flex-wrap:wrap">';
        echo self::button('Netzwerke & API','affiliate-portal-networks',true);
        echo self::button('Synchronisierung','affiliate-portal-sync');
        echo self::button('Awin','affiliate-portal-provider-awin');
        echo self::button('ADCELL','affiliate-portal-provider-adcell');
        echo self::button('eBay','affiliate-portal-ebay');
        echo self::button('idealo','affiliate-portal-provider-idealo');
        echo self::button('Digistore24','affiliate-portal-provider-digistore24');
        echo '</p>';
        echo '<p class="description">OTTO, Kelkoo, Kaufland, Amazon und ADCocktail erscheinen als vorbereitet, bis ein realer, dokumentierter Zugang vorhanden ist. Es werden keine Schnittstellen geraten.</p>';
        self::footer();
    }

    public static function render_system() {
        self::header('Steuerung & System','Chef-Veto, Automatisierung und Prüfungen bleiben vollständig verfügbar.');
        echo '<p style="display:flex;gap:8px;flex-wrap:wrap">';
        echo self::button('Steuerung & Veto','affiliate-portal-control',true);
        echo self::button('Automatisierung','affiliate-portal-automation');
        echo self::button('Prüfzentrum','affiliate-portal-health');
        echo '</p>';
        self::footer();
    }
}
