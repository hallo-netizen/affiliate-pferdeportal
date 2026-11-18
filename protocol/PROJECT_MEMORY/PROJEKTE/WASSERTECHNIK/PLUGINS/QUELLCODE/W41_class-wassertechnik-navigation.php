<?php
if (!defined('ABSPATH')) { exit; }
/** W32: purely read-only navigation with the original 79 WordPress owner paths. */
final class Wassertechnik_W32_Navigation {
    private static bool $already_displayed=false;
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
        add_action('wp_head', [self::class, 'style']);
        add_action('wp_body_open', [self::class, 'auto_render'], 15);
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
    private static function product_links(array $plan, array $paths, string $area, bool $buy): array {
        $links=[];
        foreach ($plan['existing_w4_pages'] as $p) {
            if (($p['bereich']??'') !== $area || (($p['menu']??null) === true) !== $buy) continue;
            $targetPath=$paths[$p['owner_id']]??null;
            if (!$targetPath) continue;
            $wp=get_page_by_path((string)$targetPath, OBJECT, 'page');
            if (!$wp && $targetPath !== $p['wordpress_path'])
                $wp=get_page_by_path((string)$p['wordpress_path'], OBJECT, 'page');
            if (!$wp || $wp->post_status !== 'publish'
                || (string)get_post_meta((int)$wp->ID,'_wt_owner_id',true) !== $p['owner_id']) continue;
            $links[]='<li><a href="'.esc_url(get_permalink((int)$wp->ID)).'">'
                .esc_html((string)$p['product_name']).'</a></li>';
        }
        return $links;
    }
    public static function render(): string {
        $plan=self::plan();
        $paths=self::new_owner_paths();
        if (!$plan || !$paths) return '';
        $html='<nav class="wassertechnik-fachnavigation" aria-label="Wassertechnik-Fachnavigation"><ul class="wt-w41-tabs">';
        foreach ($plan['hauptbereiche'] as $a) {
            $links=self::product_links($plan,$paths,(string)$a['id'],true);
            $html.='<li class="wt-w41-tab"><details><summary>'.esc_html((string)$a['name'])
                .'</summary><ul class="wt-w41-links">';
            $html.=$links?implode('',$links):'<li class="wt-w41-pending">Noch keine veröffentlichten Produktseiten</li>';
            $html.='</ul></details></li>';
        }
        // The eight existing specialist products are a separate access, not an eighth buyer root.
        $special=[];
        foreach ($plan['hauptbereiche'] as $a)
            $special=array_merge($special,self::product_links($plan,$paths,(string)$a['id'],false));
        $html.='<li class="wt-w41-tab"><details><summary>Fachtechnik</summary><ul class="wt-w41-links">';
        $html.=$special?implode('',$special):'<li class="wt-w41-pending">Noch keine veröffentlichten Fachproduktseiten</li>';
        return $html.'</ul></details></li></ul></nav>';
    }
    public static function style(): void {
        if (function_exists('is_admin') && is_admin()) return;
        echo '<style id="wt-w41-nav-style">';
        echo '.wassertechnik-fachnavigation{width:100%;position:relative;z-index:20;font:inherit}.wassertechnik-fachnavigation .wt-w41-tabs{display:flex;flex-wrap:wrap;gap:.35rem;list-style:none;margin:0;padding:.6rem 0}.wassertechnik-fachnavigation .wt-w41-tab{position:relative;list-style:none;margin:0;padding:0}.wassertechnik-fachnavigation summary{list-style:none;cursor:pointer;padding:.65rem .8rem;border-radius:.4rem;border:1px solid currentColor;font-weight:600}.wassertechnik-fachnavigation summary::-webkit-details-marker{display:none}.wassertechnik-fachnavigation .wt-w41-links{position:absolute;left:0;top:100%;width:min(700px,90vw);max-width:90vw;max-height:65vh;overflow:auto;box-shadow:0 5px 18px #0002;background:Canvas;color:CanvasText;padding:1rem 1.3rem;list-style:none;columns:3;column-gap:1.5rem;z-index:30}.wassertechnik-fachnavigation .wt-w41-links li{break-inside:avoid;padding:.22rem 0}.wassertechnik-fachnavigation a{color:inherit;text-decoration:underline}.wassertechnik-fachnavigation .wt-w41-pending{opacity:.75;font-style:italic}@media(max-width:700px){.wassertechnik-fachnavigation .wt-w41-tabs{display:block}.wassertechnik-fachnavigation .wt-w41-tab{margin:.25rem 0}.wassertechnik-fachnavigation .wt-w41-links{position:static;width:auto;max-width:100%;max-height:none;box-shadow:none;columns:1}}';
        echo '</style>';
    }
    public static function auto_render(): void {
        if (self::$already_displayed || (function_exists('is_admin') && is_admin())) return;
        global $post;
        if (is_object($post) && function_exists('has_shortcode')
            && has_shortcode((string)($post->post_content??''),'wassertechnik_fachnavigation')) return;
        $html=self::render();
        if ($html!=='') { echo $html; self::$already_displayed=true; }
    }
}
