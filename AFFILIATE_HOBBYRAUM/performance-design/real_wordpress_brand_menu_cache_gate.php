<?php
if (!defined('ABSPATH')) { exit; }

final class PFTK_Menu_Setup_Cache_Gate {
    private static $cache = array();
    private static $active = false;
    public static $meta_fires = 0;
    public static $term_fires = 0;

    public static function pre($pre, $menu_item) {
        if ($pre !== null || !self::$active || !is_object($menu_item)) return $pre;
        $id = absint($menu_item->ID ?? 0);
        if ($id <= 0 || !isset(self::$cache[$id])) return $pre;
        return apply_filters('wp_setup_nav_menu_item', clone self::$cache[$id]);
    }
    public static function capture($menu_item) {
        if (!self::$active || !is_object($menu_item)) return $menu_item;
        $id = absint($menu_item->ID ?? 0);
        if ($id > 0 && !isset(self::$cache[$id])) self::$cache[$id] = clone $menu_item;
        return $menu_item;
    }
    public static function begin() {
        self::$cache = array(); self::$active = true;
        add_filter('pre_wp_setup_nav_menu_item', [__CLASS__,'pre'], 999999, 2);
        add_filter('wp_setup_nav_menu_item', [__CLASS__,'capture'], -999999, 1);
    }
    public static function end() {
        remove_filter('pre_wp_setup_nav_menu_item', [__CLASS__,'pre'], 999999);
        remove_filter('wp_setup_nav_menu_item', [__CLASS__,'capture'], -999999);
        self::$active = false; self::$cache = array();
    }
    public static function count_meta($value) { self::$meta_fires++; return $value; }
    public static function count_term($term) { self::$term_fires++; return $term; }
    public static function divergent_objects($items, $args) {
        $class = (string)($args->menu_class ?? '');
        foreach ((array)$items as $item) {
            if (!is_object($item)) continue;
            $item->classes = array_values((array)($item->classes ?? array()));
            if ($class === 'pftk-brand-menu-v15065') $item->classes[]='desktop-proof';
            if ($class === 'pftk-mobile-menu-v15074') $item->classes[]='mobile-proof';
        }
        return $items;
    }
}

add_action('template_redirect', static function() {
    $mode = sanitize_key((string)($_GET['pftk_menu_cache_gate'] ?? ''));
    if (!in_array($mode, array('baseline','cached'), true)) return;
    header('Content-Type: application/json; charset=utf-8');

    $menu = wp_get_nav_menu_object('pftk-perf-gate');
    if (!$menu) {
        $menu_id = wp_create_nav_menu('pftk-perf-gate');
        for ($i=0; $i<120; $i++) {
            wp_update_nav_menu_item($menu_id, 0, array(
                'menu-item-title' => 'Gate Item '.$i,
                'menu-item-url' => home_url('/gate-'.$i.'/'),
                'menu-item-status' => 'publish',
                'menu-item-parent-id' => 0,
            ));
        }
        $menu = wp_get_nav_menu_object($menu_id);
    }
    $menu_id = absint($menu->term_id ?? 0);

    add_filter('wp_nav_menu_objects',[PFTK_Menu_Setup_Cache_Gate::class,'divergent_objects'],500,2);
    add_filter('get_post_metadata',[PFTK_Menu_Setup_Cache_Gate::class,'count_meta'],-999999,5);
    add_filter('get_term',[PFTK_Menu_Setup_Cache_Gate::class,'count_term'],-999999,2);
    PFTK_Menu_Setup_Cache_Gate::$meta_fires=0;
    PFTK_Menu_Setup_Cache_Gate::$term_fires=0;

    if ($mode==='cached') PFTK_Menu_Setup_Cache_Gate::begin();

    $desktop = wp_nav_menu(array(
        'menu'=>$menu_id,'container'=>'nav','container_class'=>'pftk-brand-nav-inner-v15065',
        'menu_class'=>'pftk-brand-menu-v15065','fallback_cb'=>false,'depth'=>3,'echo'=>false
    ));
    $after_desktop_meta=PFTK_Menu_Setup_Cache_Gate::$meta_fires;
    $after_desktop_term=PFTK_Menu_Setup_Cache_Gate::$term_fires;

    $mobile = wp_nav_menu(array(
        'menu'=>$menu_id,'container'=>'nav','container_id'=>'pftk-main-navigation-v15071',
        'container_class'=>'pftk-mobile-nav-v15074','menu_class'=>'pftk-mobile-menu-v15074',
        'fallback_cb'=>false,'depth'=>3,'echo'=>false
    ));

    if ($mode==='cached') PFTK_Menu_Setup_Cache_Gate::end();

    $result=array(
        'mode'=>$mode,
        'desktop_sha256'=>hash('sha256',(string)$desktop),
        'mobile_sha256'=>hash('sha256',(string)$mobile),
        'desktop_has_marker'=>strpos((string)$desktop,'desktop-proof')!==false,
        'mobile_has_marker'=>strpos((string)$mobile,'mobile-proof')!==false,
        'meta_after_desktop'=>$after_desktop_meta,
        'meta_total'=>PFTK_Menu_Setup_Cache_Gate::$meta_fires,
        'meta_second'=>PFTK_Menu_Setup_Cache_Gate::$meta_fires-$after_desktop_meta,
        'term_after_desktop'=>$after_desktop_term,
        'term_total'=>PFTK_Menu_Setup_Cache_Gate::$term_fires,
        'term_second'=>PFTK_Menu_Setup_Cache_Gate::$term_fires-$after_desktop_term,
    );
    echo wp_json_encode($result);
    exit;
},0);
