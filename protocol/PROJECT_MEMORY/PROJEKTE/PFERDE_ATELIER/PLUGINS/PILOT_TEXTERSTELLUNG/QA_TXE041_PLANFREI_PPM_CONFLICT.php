<?php
// QA only: the plan-free candidate must refuse to load original PSTE while PPM is active.
define('ABSPATH','/qa/');
$GLOBALS['opts']=['active_plugins'=>['portal-production-machine/portal-production-machine.php'],'texterstellung_testsite_confirmation_v1'=>hash('sha256','https://qa.example.invalid/|1')];
$GLOBALS['actions']=[];
function home_url($p='/'){return 'https://qa.example.invalid/';} function get_current_blog_id(){return 1;}
function get_option($k,$default=false){return $GLOBALS['opts'][$k]??$default;}
function get_site_option($k,$default=false){return $default;}
function add_action($hook,$cb,$priority=10){$GLOBALS['actions'][$hook][]=$cb;}
function add_filter($hook,$cb,$priority=10,$argc=1){$GLOBALS['actions'][$hook][]=$cb;}
require dirname(__DIR__).'/working_planfrei/texterstellung/texterstellung.php';
$checks=[
  'ppm_is_marked_active'=>in_array('portal-production-machine/portal-production-machine.php',get_option('active_plugins'),true),
  'pste_not_loaded'=>!class_exists('PSTE_Plugin',false),
  'pserc_not_loaded'=>!class_exists('PSERC_System4_Import',false),
  'no_jobs_registered'=>!isset($GLOBALS['actions']['pste_research_tick']) && !isset($GLOBALS['actions']['admin_post_txe_export']),
  'conflict_notice_registered'=>isset($GLOBALS['actions']['admin_notices']),
];
echo json_encode(['pass'=>count(array_filter($checks)),'total'=>count($checks),'checks'=>$checks],JSON_PRETTY_PRINT),"\n";
exit(in_array(false,$checks,true)?1:0);
