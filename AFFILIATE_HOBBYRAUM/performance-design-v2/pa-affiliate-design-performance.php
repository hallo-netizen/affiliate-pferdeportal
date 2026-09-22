<?php
/*
 * Plugin Name: Pferde Atelier – Affiliate Design Performance
 * Description: Requestweiter Cache fuer das teure WordPress-Core-Setup identischer Menuepunkte. Design, Menuefilter und HTML bleiben unveraendert.
 * Version: 2.0.0
 * Author: Pferde Atelier
 */
if (!defined('ABSPATH')) { exit; }
final class PA_Affiliate_Design_Performance {
    private const DESKTOP_MENU_CLASS='pftk-brand-menu-v15065';
    private const MOBILE_MENU_CLASS='pftk-mobile-menu-v15074';
    private static array $core_setup_cache=[];
    private static bool $filters_installed=false;
    private static bool $brand_active=false;
    private static string $phase='idle';
    private static string $theme_location='';
    public static function boot():void{
        add_filter('wp_nav_menu_args',[__CLASS__,'on_menu_args'],-999999,1);
        add_filter('wp_nav_menu',[__CLASS__,'on_menu_html'],999999,2);
        add_action('shutdown',[__CLASS__,'cleanup'],999999);
        if(self::cache_allowed()){self::install_filters();}
    }
    private static function cache_allowed():bool{
        if((function_exists('is_admin')&&is_admin())||(defined('DOING_CRON')&&DOING_CRON)||(defined('REST_REQUEST')&&REST_REQUEST)||(defined('WP_CLI')&&WP_CLI)||(function_exists('wp_doing_ajax')&&wp_doing_ajax())) return false;
        return true;
    }
    private static function install_filters():void{
        if(self::$filters_installed)return;
        add_filter('pre_wp_setup_nav_menu_item',[__CLASS__,'pre_setup'],999999,2);
        add_filter('wp_setup_nav_menu_item',[__CLASS__,'capture_setup'],-999999,1);
        self::$filters_installed=true;
    }
    public static function on_menu_args($args){
        if(!is_array($args))return $args;
        $menu_class=isset($args['menu_class'])?(string)$args['menu_class']:'';
        $location=isset($args['theme_location'])?(string)$args['theme_location']:'';
        if($menu_class===self::DESKTOP_MENU_CLASS){self::$brand_active=true;self::$theme_location=$location;self::$phase='desktop';return $args;}
        if($menu_class===self::MOBILE_MENU_CLASS&&self::$brand_active&&self::same_location($location)){self::$phase='mobile';return $args;}
        if(self::$brand_active)self::$phase='other';
        return $args;
    }
    public static function pre_setup($pre,$menu_item){
        if($pre!==null||!self::cache_allowed()||!is_object($menu_item))return $pre;
        $id=absint($menu_item->ID??0);
        if($id<=0||!isset(self::$core_setup_cache[$id]))return $pre;
        return apply_filters('wp_setup_nav_menu_item',clone self::$core_setup_cache[$id]);
    }
    public static function capture_setup($menu_item){
        if(!self::cache_allowed()||!is_object($menu_item))return $menu_item;
        $id=absint($menu_item->ID??0);
        if($id>0&&!isset(self::$core_setup_cache[$id]))self::$core_setup_cache[$id]=clone $menu_item;
        return $menu_item;
    }
    public static function on_menu_html($html,$args){
        if(!self::$brand_active||!is_object($args))return $html;
        $menu_class=isset($args->menu_class)?(string)$args->menu_class:'';
        $location=isset($args->theme_location)?(string)$args->theme_location:'';
        if($menu_class===self::DESKTOP_MENU_CLASS&&self::same_location($location)){self::$phase='between';return $html;}
        if($menu_class===self::MOBILE_MENU_CLASS&&self::same_location($location)){self::$phase='after-mobile';self::$brand_active=false;self::$theme_location='';}
        return $html;
    }
    private static function same_location(string $location):bool{return self::$theme_location===$location;}
    public static function cleanup():void{
        if(self::$filters_installed){remove_filter('pre_wp_setup_nav_menu_item',[__CLASS__,'pre_setup'],999999);remove_filter('wp_setup_nav_menu_item',[__CLASS__,'capture_setup'],-999999);}
        self::$filters_installed=false;self::$core_setup_cache=[];self::$brand_active=false;self::$phase='idle';self::$theme_location='';
    }
}
PA_Affiliate_Design_Performance::boot();
