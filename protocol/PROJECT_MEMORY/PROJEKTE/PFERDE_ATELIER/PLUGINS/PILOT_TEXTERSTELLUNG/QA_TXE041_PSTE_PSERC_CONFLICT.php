<?php
error_reporting(E_ALL);
define('ABSPATH','/qa/');
$which=$argv[1]??'none';$GLOBALS['hooks']=[];
function get_option($key,$default=false){global $which;if($key==='active_plugins')return match($which){'pste'=>['portal-seo-topic-engine/portal-seo-topic-engine.php'],'pserc'=>['portal-seo-editorial-plan-compiler/portal-seo-editorial-plan-compiler.php'],'both'=>['portal-seo-topic-engine/portal-seo-topic-engine.php','portal-seo-editorial-plan-compiler/portal-seo-editorial-plan-compiler.php'],default=>[]};return $default;}
function get_site_option($key,$default=false){return $default;}
function add_action($name,$callback,$priority=10,$args=1){$GLOBALS['hooks'][$name][]=$callback;}
function add_filter(...$args){}
function register_activation_hook(...$args){}
function is_admin(){return false;}
require dirname(__DIR__).'/txe041_gesamtweg/texterstellung/texterstellung.php';
$expected=$which!=='none';
$blocked=count($GLOBALS['hooks']['admin_notices']??[])===1 && count($GLOBALS['hooks']['plugins_loaded']??[])===0;
$ok=$expected ? $blocked : class_exists('TXE_Workshop',false) && count($GLOBALS['hooks']['plugins_loaded']??[])===1;
echo json_encode(['mode'=>$which,'pass'=>$ok,'blocked'=>$blocked,'new_plugin_loaded'=>class_exists('TXE_Workshop',false)]),"\n";
exit($ok?0:1);
