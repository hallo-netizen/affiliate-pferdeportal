#!/usr/bin/env python3
from pathlib import Path
import sys
p=Path(sys.argv[1])
s=p.read_text(encoding='utf-8')

decl="final class Pferde_Template_Kit {\n"
helpers="""final class Pferde_Template_Kit {
    private static $brand_menu_setup_cache_v150556 = array();
    private static $brand_menu_setup_cache_active_v150556 = false;

    public static function brand_menu_setup_cache_pre_v150556($pre, $menu_item) {
        if ($pre !== null || !self::$brand_menu_setup_cache_active_v150556 || !is_object($menu_item)) { return $pre; }
        $id = absint($menu_item->ID ?? 0);
        if ($id <= 0 || !isset(self::$brand_menu_setup_cache_v150556[$id])) { return $pre; }
        // Replay the normal post-setup filter chain from a pristine core-setup
        // clone. Only the expensive core metadata/term decoration is skipped.
        return apply_filters('wp_setup_nav_menu_item', clone self::$brand_menu_setup_cache_v150556[$id]);
    }

    public static function brand_menu_setup_cache_capture_v150556($menu_item) {
        if (!self::$brand_menu_setup_cache_active_v150556 || !is_object($menu_item)) { return $menu_item; }
        $id = absint($menu_item->ID ?? 0);
        if ($id > 0 && !isset(self::$brand_menu_setup_cache_v150556[$id])) {
            self::$brand_menu_setup_cache_v150556[$id] = clone $menu_item;
        }
        return $menu_item;
    }

    private static function brand_menu_setup_cache_begin_v150556() {
        self::$brand_menu_setup_cache_v150556 = array();
        self::$brand_menu_setup_cache_active_v150556 = true;
        add_filter('pre_wp_setup_nav_menu_item', [__CLASS__, 'brand_menu_setup_cache_pre_v150556'], 999999, 2);
        add_filter('wp_setup_nav_menu_item', [__CLASS__, 'brand_menu_setup_cache_capture_v150556'], -999999, 1);
    }

    private static function brand_menu_setup_cache_end_v150556() {
        remove_filter('pre_wp_setup_nav_menu_item', [__CLASS__, 'brand_menu_setup_cache_pre_v150556'], 999999);
        remove_filter('wp_setup_nav_menu_item', [__CLASS__, 'brand_menu_setup_cache_capture_v150556'], -999999);
        self::$brand_menu_setup_cache_active_v150556 = false;
        self::$brand_menu_setup_cache_v150556 = array();
    }

"""
if s.count(decl)!=1: raise SystemExit('FAIL class declaration')
s=s.replace(decl,helpers,1)

start="""        if ($location !== '') {
            add_filter('wp_nav_menu_objects', [__CLASS__, 'brand_menu_remove_hivepress_account_v150114'], 10000, 2);
"""
start_new="""        if ($location !== '') {
            self::brand_menu_setup_cache_begin_v150556();
            add_filter('wp_nav_menu_objects', [__CLASS__, 'brand_menu_remove_hivepress_account_v150114'], 10000, 2);
"""
if s.count(start)!=1: raise SystemExit('FAIL header start anchor')
s=s.replace(start,start_new,1)

end="""            remove_filter('wp_nav_menu_objects', [__CLASS__, 'brand_menu_remove_hivepress_account_v150114'], 10000);
        } else {
"""
end_new="""            remove_filter('wp_nav_menu_objects', [__CLASS__, 'brand_menu_remove_hivepress_account_v150114'], 10000);
            self::brand_menu_setup_cache_end_v150556();
        } else {
"""
if s.count(end)!=1: raise SystemExit('FAIL header end anchor')
s=s.replace(end,end_new,1)

p.write_text(s,encoding='utf-8')
print('DESIGN_BRAND_MENU_SETUP_CACHE_PATCH_PASS')
