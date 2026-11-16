<?php
if (!defined('ABSPATH')) { exit; }
/** W32: purely read-only navigation with the original 79 WordPress owner paths. */
final class Wassertechnik_W32_Navigation {
    private const ASSET = 'ASSETS/W32_wassertechnik-navigation.json';
    public static function plan(): array {
        $file = dirname(__DIR__) . '/' . self::ASSET;
        if (!is_readable($file)) return [];
        $j = json_decode((string)file_get_contents($file), true);
        if (!is_array($j) || ($j['version'] ?? '') !== 'W32_2026-11-16_v1'
            || ($j['wp_owner_count'] ?? null) !== 79
            || ($j['wp_buy_menu_count'] ?? null) !== 71
            || ($j['wp_industry_count'] ?? null) !== 8
            || count($j['hauptbereiche'] ?? []) !== 7
            || count($j['existing_w4_pages'] ?? []) !== 79) return [];
        return $j;
    }
    public static function boot(): void {
        add_shortcode('wassertechnik_fachnavigation', [self::class, 'render']);
        add_action('admin_menu', [self::class, 'admin_menu'], 40);
    }
    public static function admin_menu(): void {
        add_submenu_page('wassertechnik-kategorie', 'Fachnavigation – Vorschau',
            'Fachnavigation – Vorschau', 'manage_options', 'wassertechnik-w32-navigation', [self::class, 'admin_screen']);
    }
    public static function admin_screen(): void {
        if (!current_user_can('manage_options')) wp_die('Administratorrechte erforderlich.');
        $j = self::plan();
        echo '<div class="wrap"><h1>Wassertechnik: Navigation (nur schreibfreie Vorschau)</h1>';
        if (!$j) { echo '<p>GESPERRT: W32-Fachplan nicht lesbar.</p></div>'; return; }
        echo '<p>79 bestehende Produktowner: 71 kaufnahe, 8 Fachtechnik. 81 neue Produkte sind nicht SEO- oder WordPress-freigegeben. Keine URL-Änderung.</p>';
        foreach ($j['hauptbereiche'] as $a) {
            echo '<p><strong>'.esc_html((string)$a['name']).'</strong>: '
                .(int)$a['existing_menu'].' bestehende kaufnahe Produktseiten; '
                .(int)$a['new_not_approved'].' neue, nicht freigegebene Produktarten.</p>';
        }
        echo self::render() . '</div>';
    }
    private static function new_owner_paths(): array {
        $file = dirname(__DIR__) . '/ASSETS/W35_wordpress_importplan_219.json';
        if (!is_readable($file)) return [];
        $j = json_decode((string)file_get_contents($file), true);
        if (!is_array($j) || ($j['schema'] ?? '') !== 'wassertechnik-w35-one-time-wp-import-v1'
            || count($j['wp_targets'] ?? []) !== 219) return [];
        $paths=[];
        foreach($j['wp_targets'] as $r) if (($r['kind'] ?? '') === 'page')
            $paths[$r['owner_id']]=$r['path'];
        return count($paths)===114?$paths:[];
    }
    public static function render(): string {
        $j = self::plan();
        if (!$j) return '';
        $paths = self::new_owner_paths();
        if (!$paths) return ''; // Fail closed if current single import-target master is missing.
        $html = '';
        foreach ($j['hauptbereiche'] as $a) {
            $list = [];
            foreach ($j['existing_w4_pages'] as $p) {
                if (($p['bereich'] ?? '') !== $a['id'] || ($p['menu'] ?? null) !== true) continue;
                $targetPath = $paths[$p['owner_id']] ?? null;
                if (!$targetPath) continue;
                // Read exact same WP owner at its final path OR its original legacy path.
                // This is a lookup, not a second page/SEO decision.
                $wp = get_page_by_path((string)$targetPath, OBJECT, 'page');
                if (!$wp && $targetPath !== $p['wordpress_path'])
                    $wp = get_page_by_path((string)$p['wordpress_path'], OBJECT, 'page');
                if (!$wp || $wp->post_status !== 'publish'
                    || (string)get_post_meta((int)$wp->ID, '_wt_owner_id', true) !== $p['owner_id']) continue;
                $list[] = '<li><a href="'.esc_url(get_permalink((int)$wp->ID)).'">'
                    .esc_html((string)$p['product_name']).'</a></li>';
            }
            if (!$list) continue;
            $html .= '<section class="wt-fachbereich"><h3>'.esc_html((string)$a['name'])
                .'</h3><ul>'.implode('', $list).'</ul></section>';
        }
        return '<nav class="wassertechnik-fachnavigation" aria-label="Wassertechnik-Fachnavigation">'.$html.'</nav>';
    }
}
