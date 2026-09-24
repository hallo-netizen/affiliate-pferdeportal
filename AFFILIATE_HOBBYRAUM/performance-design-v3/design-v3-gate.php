<?php
/*
 * Plugin Name: Design Performance V3 Persistent Gate
 */
if(!defined('ABSPATH')) exit;

$GLOBALS['pftk_v3_meta_hooks']=0;
$GLOBALS['pftk_v3_setup_hits']=0;
$GLOBALS['pftk_v3_cache_hits']=0;

add_filter('get_post_metadata',function($value,$object_id,$meta_key,$single,$meta_type){
    $GLOBALS['pftk_v3_meta_hooks']++;
    return $value;
},PHP_INT_MAX,5);

add_filter('wp_setup_nav_menu_item',function($item){
    if(is_object($item)){$GLOBALS['pftk_v3_setup_hits']++;}
    return $item;
},20,1);

add_filter('pre_wp_setup_nav_menu_item',function($pre,$item){
    if($pre!==null){$GLOBALS['pftk_v3_cache_hits']++;}
    return $pre;
},1000000,2);

function pftk_v3_reset_counts(){
    $GLOBALS['pftk_v3_meta_hooks']=0;
    $GLOBALS['pftk_v3_setup_hits']=0;
    $GLOBALS['pftk_v3_cache_hits']=0;
}

function pftk_v3_render(){
    pftk_v3_reset_counts();
    $menu_id=(int)get_option('pftk_v3_gate_menu_id',0);
    if($menu_id<=0)return array('error'=>'menu_missing');

    $desktop_filter=function($items){
        if(!empty($items)&&is_object($items[0])){
            $items[0]=clone $items[0];
            $items[0]->title.='|DESKTOP';
        }
        return $items;
    };
    add_filter('wp_nav_menu_objects',$desktop_filter,999,2);
    $desktop=wp_nav_menu(array(
        'menu'=>$menu_id,'theme_location'=>'primary','container'=>'nav',
        'menu_class'=>'pftk-brand-menu-v15065','fallback_cb'=>false,'depth'=>3,'echo'=>false
    ));
    remove_filter('wp_nav_menu_objects',$desktop_filter,999);

    $mobile_filter=function($items){
        if(!empty($items)&&is_object($items[0])){
            $items[0]=clone $items[0];
            $items[0]->title.='|MOBILE';
        }
        return $items;
    };
    add_filter('wp_nav_menu_objects',$mobile_filter,999,2);
    $mobile=wp_nav_menu(array(
        'menu'=>$menu_id,'theme_location'=>'primary','container'=>'nav',
        'menu_class'=>'pftk-mobile-menu-v15074','fallback_cb'=>false,'depth'=>3,'echo'=>false
    ));
    remove_filter('wp_nav_menu_objects',$mobile_filter,999);

    $astra=wp_nav_menu(array(
        'menu'=>$menu_id,'theme_location'=>'primary','container'=>'nav',
        'menu_class'=>'astra-header-menu','fallback_cb'=>false,'depth'=>3,'echo'=>false
    ));

    $stats=class_exists('PA_Affiliate_Design_Performance')&&method_exists('PA_Affiliate_Design_Performance','debug_stats')
        ? PA_Affiliate_Design_Performance::debug_stats():array();

    return array(
        'menu_id'=>$menu_id,
        'desktop_hash'=>hash('sha256',(string)$desktop),
        'mobile_hash'=>hash('sha256',(string)$mobile),
        'astra_hash'=>hash('sha256',(string)$astra),
        'desktop_changed_title'=>strpos((string)$desktop,'Item 1 CHANGED')!==false,
        'mobile_changed_title'=>strpos((string)$mobile,'Item 1 CHANGED')!==false,
        'meta_hooks'=>(int)$GLOBALS['pftk_v3_meta_hooks'],
        'setup_filter_hits'=>(int)$GLOBALS['pftk_v3_setup_hits'],
        'cache_hits'=>(int)$GLOBALS['pftk_v3_cache_hits'],
        'helper_stats'=>$stats,
    );
}

add_action('template_redirect',function(){
    if(!isset($_GET['design_v3_gate']))return;
    header('Content-Type: application/json; charset=utf-8');
    echo wp_json_encode(pftk_v3_render());
    exit;
},-1000);

add_action('admin_post_nopriv_design_v3_admin',function(){
    header('Content-Type: application/json; charset=utf-8');
    echo wp_json_encode(pftk_v3_render());
    exit;
});
