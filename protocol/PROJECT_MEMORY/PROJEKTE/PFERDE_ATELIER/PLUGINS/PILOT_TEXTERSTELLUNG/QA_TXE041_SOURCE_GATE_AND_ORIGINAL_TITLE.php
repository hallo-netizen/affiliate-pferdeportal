<?php
/* Standalone source-only acceptance probe: mocks of WP hooks, never a WP live test. */
define('ABSPATH','/fake-wp/');
$mode=$argv[1]??'unconfirmed';
$all=[];$options=[];
function home_url($s='/'){return 'https://test.example/'.$s;}
function get_current_blog_id(){return 1;}
function get_option($n,$fallback=false){global $options;return $options[$n]??$fallback;}
function get_site_option($n,$fallback=false){return $fallback;}
function update_option($n,$v,$aut=false){global $options;$options[$n]=$v;return true;}
function is_admin(){return true;}
function plugin_basename($p){return basename($p);}
function add_action($hook,$cb,$priority=10,$args=1){global $all;$all[$hook][]=[$cb,$priority];}
function add_filter($hook,$cb,$priority=10,$args=1){add_action($hook,$cb,$priority,$args);}
function register_activation_hook($path,$cb){add_action('activation',$cb);}
if($mode==='confirmed')$options['texterstellung_testsite_confirmation_v1']=hash('sha256',home_url('/').'|'.get_current_blog_id());
if($mode==='old-active')$options['active_plugins']=['portal-seo-topic-engine/portal-seo-topic-engine.php'];
require __DIR__.'/../working_full/texterstellung/texterstellung.php';
$hasPste=class_exists('PSTE_Plugin',false);
$hasTxe=class_exists('TXE_Workshop',false);
if($mode==='confirmed'){
 $hasOriginalTitle=
  is_callable(['PSTE_Mini_Workflow','exportKeywords']) &&
  is_callable(['PSTE_Mini_Workflow','importKeywords']);
 $loaded=$hasPste && $hasTxe && $hasOriginalTitle;
} elseif($mode==='old-active'){
 $loaded=!$hasPste && empty($all['plugins_loaded']);
} else {
 $loaded=!$hasPste && $hasTxe && empty($all['pste_research_step_driver']);
}
$src=file_get_contents(__DIR__.'/../working_full/texterstellung/texterstellung.php');
$unmodifiedOriginalForms=str_contains($src,"pste_mini_keyword_export") && str_contains($src,"pste_mini_keyword_import");
$noSyntheticRouted=str_contains($src,"ORIGINAL_PSTE_TITLE_ACTION_ONLY");
$pass=$loaded && $unmodifiedOriginalForms && $noSyntheticRouted;
echo json_encode(['mode'=>$mode,'pass'=>$pass,'txe_loaded'=>$hasTxe,'pste_loaded'=>$hasPste,'original_title_handlers'=>isset($hasOriginalTitle)?$hasOriginalTitle:false,'original_forms'=>$unmodifiedOriginalForms,'synthetic_route_blocked'=>$noSyntheticRouted],JSON_UNESCAPED_SLASHES),"\n";
exit($pass?0:1);
