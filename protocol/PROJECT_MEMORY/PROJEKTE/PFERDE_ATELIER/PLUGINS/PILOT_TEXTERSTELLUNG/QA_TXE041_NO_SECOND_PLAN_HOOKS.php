<?php
/* Technical-only QA: the original SEO worker retains its hooks; the obsolete
 * separate production-plan endpoints may not survive consolidated startup. */
define('ABSPATH','/qa/');
$GLOBALS['qa_actions']=[];
$GLOBALS['qa_opts']=['texterstellung_testsite_confirmation_v1'=>hash('sha256','https://qa.invalid/|1')];
function home_url($path='/'){return 'https://qa.invalid/';}
function get_current_blog_id(){return 1;}
function get_option($k,$def=false){return $GLOBALS['qa_opts'][$k]??$def;}
function get_site_option($k,$def=false){return $def;}
function is_admin(){return false;}
function add_action($hook,$cb,$priority=10,$arity=1){$GLOBALS['qa_actions'][$hook][]=$cb;return true;}
function add_filter($hook,$cb,$priority=10,$arity=1){return add_action($hook,$cb,$priority,$arity);}
function remove_action($hook,$cb,$priority=10){$before=$GLOBALS['qa_actions'][$hook]??[];$after=array_values(array_filter($before,static fn($x)=>$x!==$cb));$GLOBALS['qa_actions'][$hook]=$after;return count($after)!==count($before);}
function register_activation_hook(...$args){}
$obsolete=[
 ['admin_post_pste_mini_forward_to_plan','PSTE_Mini_Workflow','forwardToPlan'],
 ['admin_post_pste_mini_legacy_plan_rebind','PSTE_Mini_Workflow','legacyEmptyPlanRebind'],
 ['admin_post_pste_import_editorial_plan','PSTE_Admin','importEditorialPlan'],
 ['admin_post_pste_export_planning_topics','PSTE_Admin','exportPlanningTopics'],
 ['admin_post_pste_title_desk_export','PSTE_Admin','exportTitleDesk'],
 ['admin_post_pste_title_desk_import','PSTE_Admin','importTitleDesk'],
 ['pste_title_desk_reentry','PSTE_Admin','processTitleDeskReentry'],
 ['wp_ajax_pste_title_desk_reentry_continue','PSTE_Admin','continueTitleDeskReentry'],
 ['wp_ajax_nopriv_pste_title_desk_reentry_continue','PSTE_Admin','continueTitleDeskReentry'],
 ['wp_ajax_pste_production_auto_step','PSTE_Admin','productionAutoStepAjax'],
 ['wp_ajax_pste_production_auto_status','PSTE_Admin','productionAutoStatusAjax'],
 ['wp_ajax_pste_production_auto_cancel','PSTE_Admin','productionAutoCancelAjax'],
];
foreach($obsolete as [$hook,$cl,$fn])add_action($hook,[$cl,$fn]);
add_action('admin_post_pste_mini_keyword_export',['PSTE_Mini_Workflow','exportKeywords']);
require dirname(__DIR__).'/working_planfree_seo/texterstellung/texterstellung.php';
$tests=[];
foreach($obsolete as [$hook,$cl,$fn])$tests['disabled_'.$hook]=!in_array([$cl,$fn],$GLOBALS['qa_actions'][$hook]??[],true);
$tests['unchanged_mini_title_hook_retained']=in_array(['PSTE_Mini_Workflow','exportKeywords'],$GLOBALS['qa_actions']['admin_post_pste_mini_keyword_export']??[],true);
$tests['original_PSTE_research_registered']=isset($GLOBALS['qa_actions'][PSTE_RESEARCH_DRIVER_CRON_HOOK]);
$tests['original_PSTE_loaded']=class_exists('PSTE_Plugin',false);
$pass=count(array_filter($tests));echo json_encode(['pass'=>$pass,'total'=>count($tests),'tests'=>$tests],JSON_PRETTY_PRINT|JSON_UNESCAPED_SLASHES),"\n";exit($pass===count($tests)?0:1);
