<?php
/*
 * Plugin Name: Design Performance V2 Gate
 */
if(!defined('ABSPATH')) exit;

$GLOBALS['pftk_v2_meta_hooks']=0;
$GLOBALS['pftk_v2_setup_hits']=0;
$GLOBALS['pftk_v2_cache_hits']=0;

add_filter('get_post_metadata',function($value,$object_id,$meta_key,$single,$meta_type){
    $GLOBALS['pftk_v2_meta_hooks']++;
    return $value;
},PHP_INT_MAX,5);

add_filter('wp_setup_nav_menu_item',function($item){
    if(is_object($item)){
        $GLOBALS['pftk_v2_setup_hits']++;
        $item->pftk_v2_gate_marker='setup-'.$GLOBALS['pftk_v2_setup_hits'];
    }
    return $item;
},20,1);

add_filter('pre_wp_setup_nav_menu_item',function($pre,$item){
    if($pre!==null){$GLOBALS['pftk_v2_cache_hits']++;}
    return $pre;
},1000000,2);

function pftk_v2_item_rows($items){
    $rows=[];
    foreach((array)$items as $item){
        if(!is_object($item)) continue;
        $rows[]=array(
            'ID'=>(int)($item->ID??0),
            'title'=>(string)($item->title??''),
            'url'=>(string)($item->url??''),
            'parent'=>(int)($item->menu_item_parent??0),
            'type'=>(string)($item->type??''),
            'object'=>(string)($item->object??''),
            'object_id'=>(int)($item->object_id??0),
            'marker'=>(string)($item->pftk_v2_gate_marker??''),
        );
    }
    return $rows;
}

function pftk_v2_run($baseline=false,$direct_loops=8){
    if($baseline && class_exists('PA_Affiliate_Design_Performance')){
        PA_Affiliate_Design_Performance::cleanup();
    }
    $menu_id=(int)get_option('pftk_v2_gate_menu_id',0);
    if($menu_id<=0) return array('error'=>'menu_missing');

    $direct_hashes=[];
    for($i=0;$i<$direct_loops;$i++){
        $items=wp_get_nav_menu_items($menu_id);
        $direct_hashes[]=hash('sha256',serialize(pftk_v2_item_rows($items)));
    }

    $desktop_filter=function($items){
        if(!empty($items)&&is_object($items[0])){$items[0]=clone $items[0];$items[0]->title.='|DESKTOP';}
        return $items;
    };
    add_filter('wp_nav_menu_objects',$desktop_filter,999,2);
    $desktop=wp_nav_menu(array(
        'menu'=>$menu_id,'theme_location'=>'primary','container'=>'nav',
        'menu_class'=>'pftk-brand-menu-v15065','fallback_cb'=>false,'depth'=>3,'echo'=>false
    ));
    remove_filter('wp_nav_menu_objects',$desktop_filter,999);

    $mobile_filter=function($items){
        if(!empty($items)&&is_object($items[0])){$items[0]=clone $items[0];$items[0]->title.='|MOBILE';}
        return $items;
    };
    add_filter('wp_nav_menu_objects',$mobile_filter,999,2);
    $mobile=wp_nav_menu(array(
        'menu'=>$menu_id,'theme_location'=>'primary','container'=>'nav',
        'menu_class'=>'pftk-mobile-menu-v15074','fallback_cb'=>false,'depth'=>3,'echo'=>false
    ));
    remove_filter('wp_nav_menu_objects',$mobile_filter,999);

    $astra_header=wp_nav_menu(array(
        'menu'=>$menu_id,'theme_location'=>'primary','container'=>'nav',
        'menu_class'=>'astra-header-menu','fallback_cb'=>false,'depth'=>3,'echo'=>false
    ));
    $astra_mobile=wp_nav_menu(array(
        'menu'=>$menu_id,'theme_location'=>'primary','container'=>'nav',
        'menu_class'=>'astra-mobile-menu','fallback_cb'=>false,'depth'=>3,'echo'=>false
    ));

    return array(
        'baseline'=>$baseline,
        'menu_id'=>$menu_id,
        'direct_loops'=>$direct_loops,
        'direct_hashes'=>$direct_hashes,
        'desktop_hash'=>hash('sha256',(string)$desktop),
        'mobile_hash'=>hash('sha256',(string)$mobile),
        'astra_header_hash'=>hash('sha256',(string)$astra_header),
        'astra_mobile_hash'=>hash('sha256',(string)$astra_mobile),
        'meta_hooks'=>(int)$GLOBALS['pftk_v2_meta_hooks'],
        'setup_filter_hits'=>(int)$GLOBALS['pftk_v2_setup_hits'],
        'cache_hits'=>(int)$GLOBALS['pftk_v2_cache_hits'],
    );
}

add_action('template_redirect',function(){
    if(!isset($_GET['design_v2_gate'])) return;
    $baseline=!empty($_GET['baseline']);
    header('Content-Type: application/json');
    echo wp_json_encode(pftk_v2_run($baseline,8));
    exit;
},-1000);

add_action('admin_post_nopriv_design_v2_admin',function(){
    header('Content-Type: application/json');
    echo wp_json_encode(pftk_v2_run(false,3));
    exit;
});
