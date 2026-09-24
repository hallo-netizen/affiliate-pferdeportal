<?php
/*
 * Plugin Name: Pferde Atelier – Affiliate Design Performance
 * Description: Requestweiter und sicher invalidierter persistenter Cache fuer das teure WordPress-Core-Setup identischer Menuepunkte. Design, Menuefilter und HTML bleiben unveraendert.
 * Version: 3.0.0
 * Author: Pferde Atelier
 */
if (!defined('ABSPATH')) { exit; }

final class PA_Affiliate_Design_Performance {
    private const DESKTOP_MENU_CLASS='pftk-brand-menu-v15065';
    private const MOBILE_MENU_CLASS='pftk-mobile-menu-v15074';
    private const GENERATION_OPTION='pa_adp_menu_generation_v3';
    private const CACHE_PREFIX='pa_adp_menu_core_v3_';

    private static array $core_setup_cache=[];
    private static array $persistent_loaded_ids=[];
    private static array $persistent_build=[];
    private static bool $persistent_loaded=false;
    private static bool $persistent_dirty=false;
    private static bool $filters_installed=false;
    private static bool $brand_active=false;
    private static bool $invalidated=false;
    private static string $phase='idle';
    private static string $theme_location='';
    private static int $active_menu_id=0;
    private static ?int $generation=null;
    private static array $stats=[
        'persistent_loads'=>0,'persistent_items'=>0,'persistent_stores'=>0,
        'request_hits'=>0,'core_captures'=>0,
    ];

    public static function boot():void{
        add_filter('wp_nav_menu_args',[__CLASS__,'on_menu_args'],-999999,1);
        add_filter('wp_nav_menu',[__CLASS__,'on_menu_html'],999999,2);
        add_action('shutdown',[__CLASS__,'cleanup'],999999);
        if(self::cache_allowed()){self::install_filters();}

        add_action('save_post',[__CLASS__,'invalidate_on_post'],10,3);
        add_action('deleted_post',[__CLASS__,'invalidate']);
        add_action('trashed_post',[__CLASS__,'invalidate']);
        add_action('untrashed_post',[__CLASS__,'invalidate']);
        add_action('created_term',[__CLASS__,'invalidate']);
        add_action('edited_term',[__CLASS__,'invalidate']);
        add_action('delete_term',[__CLASS__,'invalidate']);
        add_action('wp_update_nav_menu',[__CLASS__,'invalidate']);
        add_action('switch_theme',[__CLASS__,'invalidate']);
        add_action('activated_plugin',[__CLASS__,'invalidate']);
        add_action('deactivated_plugin',[__CLASS__,'invalidate']);
        add_action('upgrader_process_complete',[__CLASS__,'invalidate']);
        add_action('update_option_permalink_structure',[__CLASS__,'invalidate']);
        add_action('update_option_home',[__CLASS__,'invalidate']);
        add_action('update_option_siteurl',[__CLASS__,'invalidate']);
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

    private static function locale():string{
        if(function_exists('determine_locale')) return (string)determine_locale();
        return function_exists('get_locale')?(string)get_locale():'';
    }

    private static function generation():int{
        if(self::$generation!==null)return self::$generation;
        $g=(int)get_option(self::GENERATION_OPTION,1);
        if($g<1)$g=1;
        self::$generation=$g;
        return $g;
    }

    private static function cache_option_name(int $menu_id):string{
        return self::CACHE_PREFIX.$menu_id.'_'.substr(md5(self::locale()),0,12);
    }

    private static function resolve_menu_id(array $args):int{
        if(!empty($args['menu'])){
            $obj=wp_get_nav_menu_object($args['menu']);
            if($obj&&!is_wp_error($obj))return (int)$obj->term_id;
        }
        $location=isset($args['theme_location'])?(string)$args['theme_location']:'';
        if($location!==''){
            $locations=get_nav_menu_locations();
            if(isset($locations[$location]))return (int)$locations[$location];
        }
        return 0;
    }

    private static function load_persistent(int $menu_id):void{
        self::$persistent_loaded=false;
        self::$persistent_loaded_ids=[];
        self::$persistent_build=[];
        self::$persistent_dirty=false;
        if($menu_id<=0)return;
        $payload=get_option(self::cache_option_name($menu_id),null);
        if(!is_array($payload)
            ||(int)($payload['v']??0)!==1
            ||(int)($payload['generation']??0)!==self::generation()
            ||(int)($payload['menu_id']??0)!==$menu_id
            ||(string)($payload['locale']??'')!==self::locale()
            ||!isset($payload['items'])||!is_array($payload['items'])||!$payload['items']){
            self::$persistent_dirty=true;
            return;
        }
        foreach($payload['items'] as $id=>$item){
            $id=absint($id);
            if($id<=0||!is_object($item))continue;
            if(!isset(self::$core_setup_cache[$id]))self::$core_setup_cache[$id]=clone $item;
            self::$persistent_loaded_ids[$id]=true;
        }
        if(!self::$persistent_loaded_ids){
            self::$persistent_dirty=true;
            return;
        }
        self::$persistent_loaded=true;
        self::$stats['persistent_loads']++;
        self::$stats['persistent_items']=count(self::$persistent_loaded_ids);
    }

    private static function persist_current_menu():void{
        if(!self::$persistent_dirty||self::$active_menu_id<=0||!self::$persistent_build)return;
        $payload=[
            'v'=>1,
            'generation'=>self::generation(),
            'menu_id'=>self::$active_menu_id,
            'locale'=>self::locale(),
            'created'=>time(),
            'items'=>self::$persistent_build,
        ];
        update_option(self::cache_option_name(self::$active_menu_id),$payload,false);
        self::$stats['persistent_stores']++;
        self::$persistent_dirty=false;
        self::$persistent_loaded=true;
        self::$persistent_loaded_ids=array_fill_keys(array_map('intval',array_keys(self::$persistent_build)),true);
    }

    public static function on_menu_args($args){
        if(!is_array($args))return $args;
        $menu_class=isset($args['menu_class'])?(string)$args['menu_class']:'';
        $location=isset($args['theme_location'])?(string)$args['theme_location']:'';
        if($menu_class===self::DESKTOP_MENU_CLASS){
            self::$brand_active=true;
            self::$theme_location=$location;
            self::$phase='desktop';
            self::$active_menu_id=self::resolve_menu_id($args);
            self::load_persistent(self::$active_menu_id);
            return $args;
        }
        if($menu_class===self::MOBILE_MENU_CLASS&&self::$brand_active&&self::same_location($location)){
            self::$phase='mobile';
            return $args;
        }
        if(self::$brand_active)self::$phase='other';
        return $args;
    }

    public static function pre_setup($pre,$menu_item){
        if($pre!==null||!self::cache_allowed()||!is_object($menu_item))return $pre;
        $id=absint($menu_item->ID??0);
        if($id<=0||!isset(self::$core_setup_cache[$id]))return $pre;
        self::$stats['request_hits']++;
        if(self::$brand_active&&self::$phase==='desktop'&&!isset(self::$persistent_loaded_ids[$id])){
            self::$persistent_dirty=true;
        }
        return apply_filters('wp_setup_nav_menu_item',clone self::$core_setup_cache[$id]);
    }

    public static function capture_setup($menu_item){
        if(!self::cache_allowed()||!is_object($menu_item))return $menu_item;
        $id=absint($menu_item->ID??0);
        if($id<=0)return $menu_item;
        if(!isset(self::$core_setup_cache[$id])){
            self::$core_setup_cache[$id]=clone $menu_item;
            self::$stats['core_captures']++;
        }
        if(self::$brand_active&&self::$phase==='desktop'&&self::$active_menu_id>0){
            self::$persistent_build[$id]=clone $menu_item;
            if(!isset(self::$persistent_loaded_ids[$id]))self::$persistent_dirty=true;
        }
        return $menu_item;
    }

    public static function on_menu_html($html,$args){
        if(!self::$brand_active||!is_object($args))return $html;
        $menu_class=isset($args->menu_class)?(string)$args->menu_class:'';
        $location=isset($args->theme_location)?(string)$args->theme_location:'';
        if($menu_class===self::DESKTOP_MENU_CLASS&&self::same_location($location)){
            self::persist_current_menu();
            self::$phase='between';
            return $html;
        }
        if($menu_class===self::MOBILE_MENU_CLASS&&self::same_location($location)){
            self::$phase='after-mobile';
            self::$brand_active=false;
            self::$theme_location='';
            self::$active_menu_id=0;
        }
        return $html;
    }

    private static function same_location(string $location):bool{return self::$theme_location===$location;}

    public static function invalidate_on_post($post_id,$post,$update):void{
        if(function_exists('wp_is_post_revision')&&wp_is_post_revision($post_id))return;
        self::invalidate();
    }

    public static function invalidate(...$unused):void{
        if(self::$invalidated)return;
        self::$invalidated=true;
        $g=(int)get_option(self::GENERATION_OPTION,1);
        if($g<1)$g=1;
        self::$generation=$g+1;
        update_option(self::GENERATION_OPTION,self::$generation,false);
        self::$core_setup_cache=[];
        self::$persistent_loaded_ids=[];
        self::$persistent_build=[];
        self::$persistent_loaded=false;
        self::$persistent_dirty=false;
    }

    public static function debug_stats():array{
        return self::$stats+[
            'generation'=>self::generation(),
            'persistent_loaded'=>self::$persistent_loaded,
            'active_menu_id'=>self::$active_menu_id,
        ];
    }

    public static function cleanup():void{
        if(self::$filters_installed){
            remove_filter('pre_wp_setup_nav_menu_item',[__CLASS__,'pre_setup'],999999);
            remove_filter('wp_setup_nav_menu_item',[__CLASS__,'capture_setup'],-999999);
        }
        self::$filters_installed=false;
        self::$core_setup_cache=[];
        self::$persistent_loaded_ids=[];
        self::$persistent_build=[];
        self::$persistent_loaded=false;
        self::$persistent_dirty=false;
        self::$brand_active=false;
        self::$phase='idle';
        self::$theme_location='';
        self::$active_menu_id=0;
    }
}
PA_Affiliate_Design_Performance::boot();
