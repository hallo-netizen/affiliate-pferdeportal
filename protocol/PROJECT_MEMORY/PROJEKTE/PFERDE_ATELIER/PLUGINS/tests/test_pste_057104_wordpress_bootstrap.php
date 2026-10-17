<?php
declare(strict_types=1);
error_reporting(E_ALL);
define('ABSPATH','/tmp/wp-test-root/');
$GLOBALS['hooks']=[];
$GLOBALS['activation']=[];
$GLOBALS['write_attempts']=[];
$ruleset='PSTE_PRACTICAL_EDITORIALIZATION_V14_PERSISTED_EXTENSION_REVALIDATION';
$protocol='PSTE_SAFE_MIGRATION_PROTOCOL_V7_0310_ARTICLE_INTENT_TITLE_GATE';
$marker=['contract'=>'PSTE_SAFE_MIGRATION_PROTOCOL_MARKER_V1','protocol'=>$protocol,'plugin_version'=>'0.57.103','job_uuid'=>'fixture','completed_at_utc'=>'2026-10-17T00:00:00Z','editorial_ruleset'=>$ruleset,'source_schema'=>'12'];
$marker['sha256']=hash('sha256',json_encode($marker,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES|JSON_PRESERVE_ZERO_FRACTION));
$GLOBALS['options']=[
  'pste_schema_version'=>12,
  'pste_editorial_metadata_rebuild_marker_v1'=>$ruleset,
  'pste_editorial_metadata_rebuild_report_v1'=>['contract'=>'PSTE_EDITORIAL_METADATA_REBUILD_AUDIT_V1','ruleset'=>$ruleset,'report'=>['contract'=>$ruleset]],
  'pste_safe_migration_protocol_v2'=>$marker,
  'pste_boot_status_v1'=>['status'=>'READY','stage'=>'COMPLETE']
];
function is_admin(){return true;}
function add_action($hook,$callback,$priority=10,$accepted_args=1){$GLOBALS['hooks'][$hook][]=$callback;return true;}
function add_filter($hook,$callback,$priority=10,$accepted_args=1){$GLOBALS['hooks'][$hook][]=$callback;return true;}
function plugin_basename($path){return basename($path);}
function register_activation_hook($file,$callback){$GLOBALS['activation'][]=$callback;return true;}
function get_option($name,$default=false){return $GLOBALS['options'][$name]??$default;}
function update_option(...$args){$GLOBALS['write_attempts'][]=['update_option',$args];throw new RuntimeException('WRITES_FORBIDDEN_DURING_BOOT');}
function add_option(...$args){$GLOBALS['write_attempts'][]=['add_option',$args];throw new RuntimeException('WRITES_FORBIDDEN_DURING_BOOT');}
function delete_option(...$args){$GLOBALS['write_attempts'][]=['delete_option',$args];throw new RuntimeException('WRITES_FORBIDDEN_DURING_BOOT');}
function wp_json_encode($data,$flags=0){return json_encode($data,$flags);}
$src=getenv('PSTE_SOURCE_DIR')?:'/mnt/data/seo_work/modified/Portal SEO Topic Engine';
require $src.'/portal-seo-topic-engine.php';
function must(bool $condition,string $message){if(!$condition)throw new RuntimeException($message);}
must(class_exists('PSTE_Normal_Metadata_Path'),'normal metadata path missing');
must(class_exists('PSTE_Semantic_Review_Sandbox'),'sandbox missing');
must(class_exists('PSTE_Normal_Reentry_Coordinator'),'reentry missing');
must(class_exists('PSTE_Research_Driver'),'DataForSEO research driver missing');
must(isset($GLOBALS['hooks'][PSTE_SANDBOX_INTERNAL_RECHECK_CRON_HOOK]),'cron hook missing');
must(isset($GLOBALS['hooks'][PSTE_RESEARCH_DRIVER_CRON_HOOK]),'research cron hook missing');
must(isset($GLOBALS['hooks']['admin_menu']),'admin menus not registered');
must(isset($GLOBALS['hooks']['admin_post_pste_sandbox_recheck_internal']),'manual sandbox review form not registered');
must(count($GLOBALS['activation'])===1,'activation not registered exactly once');
must(count($GLOBALS['write_attempts'])===0,'unexpected writes during plugin bootstrap');
echo json_encode(['status'=>'PASS','bootstrap'=>true,'admin_hooks'=>count($GLOBALS['hooks']),'research_hook'=>true,'sandbox_hook'=>true,'activation_hook'=>true,'writes'=>count($GLOBALS['write_attempts'])],JSON_PRETTY_PRINT)."\n";