<?php
/* Disposable WordPress CI only: one isolated Hobby Depot registry and design contract. */
if (!defined('ABSPATH') || !defined('HD009_DISPOSABLE_WORDPRESS_TEST')) { exit; }
function hd_category_registry_ready(){ return true; }
function hd_category_registry_revision(){ return 'hd009-e2e-fixture-20261030'; }
function hd_category_registry_snapshot(){
    static $snapshot=null;
    if($snapshot!==null){return $snapshot;}
    $nodes=[];
    for($w=1;$w<=8;$w++){
        $nodes[]=['node_id'=>'core:world:w'.$w,'pillar'=>'core','status'=>'active',
            'object_type'=>'page','parent_id'=>'','slug'=>'welt-'.$w,'display_name'=>'Welt '.$w];
        for($h=1;$h<=40;$h++){
            $slug='hobby-'.$w.'-'.$h;$id='core:hobby:w'.$w.'-h'.$h;
            $nodes[]=['node_id'=>$id,'pillar'=>'core','status'=>'active','object_type'=>'page',
                'parent_id'=>'core:world:w'.$w,'slug'=>$slug,'display_name'=>'Hobby '.$w.'-'.$h];
            $nodes[]=['node_id'=>'core:category:w'.$w.'-h'.$h,'pillar'=>'core','status'=>'active',
                'object_type'=>'category','parent_id'=>$id,'slug'=>$slug.'-kategorie',
                'display_name'=>'Hobby '.$w.'-'.$h.' Kategorie'];
        }
    }
    return $snapshot=['revision'=>'hd009-e2e-fixture-20261030','nodes'=>$nodes];
}
final class HD009_CI_Design_Fixture {
    public const AFFILIATE_CONTRACT='1.0';
    public static function design_profile(){return 'hobby_depot';}
    public static function design_profile_contract_version(){return '1.0';}
    public static function affiliate_contract_version(){return '1.0';}
    public static function affiliate_page_type($post_id){return 'hobby';}
}
add_filter('pre_http_request', static function($preempt,$request,$url){
    $host=strtolower((string)parse_url((string)$url, PHP_URL_HOST));
    if(in_array($host,['api.ebay.com','api.sandbox.ebay.com','auth.ebay.com'],true)){
        return new WP_Error('hd009_ci_external_ebay_blocked','No external eBay API calls in disposable test');
    }
    return $preempt;
},1,3);
