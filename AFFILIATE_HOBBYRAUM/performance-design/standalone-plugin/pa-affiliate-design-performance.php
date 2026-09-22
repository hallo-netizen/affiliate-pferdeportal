<?php
/**
 * Plugin Name: Pferde Atelier – Affiliate Design Performance
 * Description: Reduziert den doppelten WordPress-Menü-Setup-Aufwand des gemeinsamen Affiliate-Headers, ohne Menüinhalt, Desktop-/Mobile-Filter oder Design zu verändern.
 * Version: 1.0.0
 * Author: Pferde Atelier
 */
if (!defined('ABSPATH')) { exit; }
final class PA_Affiliate_Design_Performance {
    private const DESKTOP_MENU_CLASS = 'pftk-brand-menu-v15065';
    private const MOBILE_MENU_CLASS  = 'pftk-mobile-menu-v15074';
    private static array $core_setup_cache = [];
    private static bool $active = false;
    private static string $phase = 'idle';
    private static string $theme_location = '';
    public static function boot(): void {
        add_filter('wp_nav_menu_args', [__CLASS__, 'on_menu_args'], -999999, 1);
        add_filter('wp_nav_menu', [__CLASS__, 'on_menu_html'], 999999, 2);
        add_action('shutdown', [__CLASS__, 'cleanup'], 999999);
    }
    public static function on_menu_args($args) {
        if (!is_array($args)) { return $args; }
        $menu_class = isset($args['menu_class']) ? (string) $args['menu_class'] : '';
        $location = isset($args['theme_location']) ? (string) $args['theme_location'] : '';
        if ($menu_class === self::DESKTOP_MENU_CLASS) {
            self::begin($location); self::$phase = 'desktop'; return $args;
        }
        if ($menu_class === self::MOBILE_MENU_CLASS && self::$active && self::same_location($location)) {
            self::$phase = 'mobile'; return $args;
        }
        if (self::$active) { self::$phase = 'other'; }
        return $args;
    }
    public static function pre_setup($pre, $menu_item) {
        if ($pre !== null || !self::$active || self::$phase !== 'mobile' || !is_object($menu_item)) { return $pre; }
        $id = absint($menu_item->ID ?? 0);
        if ($id <= 0 || !isset(self::$core_setup_cache[$id])) { return $pre; }
        return apply_filters('wp_setup_nav_menu_item', clone self::$core_setup_cache[$id]);
    }
    public static function capture_setup($menu_item) {
        if (!self::$active || self::$phase !== 'desktop' || !is_object($menu_item)) { return $menu_item; }
        $id = absint($menu_item->ID ?? 0);
        if ($id > 0 && !isset(self::$core_setup_cache[$id])) { self::$core_setup_cache[$id] = clone $menu_item; }
        return $menu_item;
    }
    public static function on_menu_html($html, $args) {
        if (!self::$active || !is_object($args)) { return $html; }
        $menu_class = isset($args->menu_class) ? (string) $args->menu_class : '';
        $location = isset($args->theme_location) ? (string) $args->theme_location : '';
        if ($menu_class === self::DESKTOP_MENU_CLASS && self::same_location($location)) {
            self::$phase = 'between'; return $html;
        }
        if ($menu_class === self::MOBILE_MENU_CLASS && self::same_location($location)) { self::cleanup(); }
        return $html;
    }
    private static function begin(string $location): void {
        self::cleanup();
        self::$core_setup_cache = [];
        self::$theme_location = $location;
        self::$active = true;
        self::$phase = 'desktop';
        add_filter('pre_wp_setup_nav_menu_item', [__CLASS__, 'pre_setup'], 999999, 2);
        add_filter('wp_setup_nav_menu_item', [__CLASS__, 'capture_setup'], -999999, 1);
    }
    private static function same_location(string $location): bool { return self::$theme_location === $location; }
    public static function cleanup(): void {
        if (self::$active) {
            remove_filter('pre_wp_setup_nav_menu_item', [__CLASS__, 'pre_setup'], 999999);
            remove_filter('wp_setup_nav_menu_item', [__CLASS__, 'capture_setup'], -999999);
        }
        self::$core_setup_cache = [];
        self::$active = false;
        self::$phase = 'idle';
        self::$theme_location = '';
    }
}
PA_Affiliate_Design_Performance::boot();
