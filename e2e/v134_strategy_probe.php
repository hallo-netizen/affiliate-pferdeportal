<?php
if (!defined('ABSPATH')) exit(2);
$o=Pferdeportal_Affiliate_Router::instance();
$s=get_option('ppar_network_idealo_v1',array());$s=is_array($s)?$s:array();
echo 'IDEALO_MODE='.sanitize_key((string)($s['output_mode']??''))."\n";
echo 'IDEALO_STRATEGY='.sanitize_key((string)($s['link_strategy']??''))."\n";
$m=new ReflectionMethod($o,'multiprovider_reorder_candidates');$m->setAccessible(true);
function c($id,$n){return array('campaign'=>array('id'=>$id,'network'=>$n,'product_gtins'=>array()));}
$r=$m->invoke($o,array(c('e1','ebay'),c('e2','ebay'),c('i1','idealo'),c('a1','amazon_future')),'automatic');
$p=array_map(function($x){return sanitize_key((string)($x['campaign']['network']??''));},$r);
echo 'GENERIC_ORDER='.wp_json_encode($p)."\n";
if(array_slice($p,0,3)!==array('ebay','idealo','amazon_future')){fwrite(STDERR,"FAIL_GENERIC\n");exit(10);}
echo "HISTORICAL_STRATEGY_PROBE_PASS\n";
