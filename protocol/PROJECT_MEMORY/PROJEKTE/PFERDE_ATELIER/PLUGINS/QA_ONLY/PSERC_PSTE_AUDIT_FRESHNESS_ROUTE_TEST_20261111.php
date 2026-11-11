<?php
declare(strict_types=1);
error_reporting(E_ALL);
define('ABSPATH','/qa/');
define('PSERC_DIR',__DIR__.'/../packaged_qa/portal-seo-editorial-plan-compiler/');
define('PSERC_VERSION','0.28.64');
define('PSERC_BUILD','0.28.64-kiss-signed-pste-audit-pretype-owner-only-qa');
$GLOBALS['options']=[
'pste_context_refresh_job_v1'=>['status'=>'COMPLETE','generation'=>12,'final_structure_sha256'=>str_repeat('f',64),'final_plan_sha256'=>str_repeat('1',64),'context_index_manifest_sha256'=>str_repeat('2',64)],
'pste_site_baseline_v1'=>['editorial_plan_sha256'=>str_repeat('1',64),'leaf_categories'=>[['term_id'=>10]]],
'pste_schema_version'=>'12',
];
function get_option($key,$default=null){return $GLOBALS['options'][$key]??$default;}
function wp_json_encode($v,$flags=0){return json_encode($v,$flags);}
function wp_strip_all_tags($str){return strip_tags($str);}
function current_user_can($cap){return true;}
function esc_html($value){return htmlspecialchars((string)$value,ENT_QUOTES);}
function esc_url($value){return (string)$value;}
function wp_create_nonce($x){return 'nonce';}
function admin_url($sub){return '/wp-admin/'.$sub;}
function wp_nonce_field($x){echo '<input name="nonce">';}
function submit_button($title,$type='',$name='submit',$wrap=true){echo '<button>'.$title.'</button>';}
function wp_die($message){throw new RuntimeException('WP_DIE:'.strip_tags((string)$message));}
class PSTE_Breadth_Research_Queue {static $state='valid';static function existingOnlyAuditCurrent():bool{ if(self::$state==='throws')throw new RuntimeException('CORRUPT_AUDIT');return self::$state==='valid';}}
class PSTE_Snapshot {static function editorialPlan(){return ['sha256'=>str_repeat('1',64)];}}
class PSERC_SEO_Source_Binding {static function validate(){return ['ok'=>true,'capability_sha256'=>str_repeat('a',64)];}}
class PSERC_Article_Type_Extension_Registry {static function verified(){return ['ok'=>true,'manifest_sha256'=>str_repeat('b',64)];}}
class PSERC_Production_Reader {static function snapshot(){return ['ok'=>true,'version'=>'6.7.9','baseline_sha256'=>str_repeat('c',64),'normal_draft_release_sha256'=>str_repeat('d',64),'normal_draft_release_self_hash'=>str_repeat('e',64),'registered_article_types'=>['Beratung'],'planning_registered_article_types'=>['Beratung'],'supported_article_types'=>['Beratung']];}}
class PSERC_Plan_Snapshot_Store {
  static array $active=[];
  static function getActive(){return self::$active;}
  static function verifyHeader($h){return true;}
  static function getJob(){return [];}
  static function getReadyPage($gen,$cursor,$limit){return ['items'=>[['binding'=>['article_type'=>'Beratung','title'=>'echter Testartikel','target_keyword'=>'Test','category'=>'test','plan_slot'=>str_repeat('f',64)]]],'complete'=>true];}
  static function materializeReadyBatch($h){throw new RuntimeException('REACHED_MATERIALIZE_AFTER_AUDIT_GATE');}
  static function readyCount($gen){throw new RuntimeException('REACHED_READY_COUNT_AFTER_AUDIT_GATE');}
}
class PSERC_System4_Import {static function renderPanel(){echo '<section>IMPORT_PANEL</section>';}}
class FakeWPDB { public $prefix='wp_',$last_error='';function get_var($query){return 333;}}
$GLOBALS['wpdb']=new FakeWPDB();
require_once PSERC_DIR.'includes/class-pserc-stable-json.php';
require_once __DIR__.'/class-pserc-plan-dependency-fingerprint.php';
require_once __DIR__.'/class-pserc-plan-compile-job.php';
require_once __DIR__.'/class-pserc-admin.php';
$dep=PSERC_Plan_Dependency_Fingerprint::current();
PSERC_Plan_Snapshot_Store::$active=['dependency'=>$dep,'generation'=>'safe-qa','ready_batch_descriptor'=>['item_count'=>3],'counts'=>['READY_FOR_METADATA_HANDOFF'=>3]];
$checks=0;$cases=[];
function test(bool $ok,string $reason){global $checks,$cases;if(!$ok){fwrite(STDERR,'FAILED: '.$reason."\n");exit(2);}++$checks;$cases[$reason]=($cases[$reason]??0)+1;}
for($repeat=0;$repeat<60;$repeat++){
 foreach(['valid','missing','throws'] as $case){
    PSTE_Breadth_Research_Queue::$state=$case;
    $allowed=$case==='valid';
    test(PSERC_Plan_Dependency_Fingerprint::existingPsteAuditCurrent()===$allowed,'shared-audit-gate-'.$case);
    $start=PSERC_Plan_Compile_Job::start();
    test(($allowed?($start['status']==='COMPLETE'):($start['status']==='BLOCKED'&&$start['error_code']==='PSERC_PLAN_PSTE_AUDIT_NOT_CURRENT')),'compiler-start-'.$case);
    ob_start();PSERC_Admin::page();$html=ob_get_clean();
    test((str_contains($html,'Produktionsübergabe herunterladen'))===$allowed,'admin-download-visibility-'.$case);
    test((str_contains($html,'Letzter geprüfter Snapshot'))===!$allowed,'stale-warning-'.$case);
    try {
      $rm=new ReflectionMethod(PSERC_Admin::class,'exportSingleHandoff');$rm->invoke(null);
      test(false,'export-unexpected-return-'.$case);
    }catch(Throwable $e){
      $expected=$allowed?'REACHED_MATERIALIZE_AFTER_AUDIT_GATE':'WP_DIE:Die gespeicherte Themenprüfung';
      test(str_contains($e->getMessage(),$expected),'export-post-check-'.$case);
    }
    try {
       $rm=new ReflectionMethod(PSERC_Plan_Compile_Job::class,'tickActivate');
       $rm->invoke(null,['generation'=>'safe-qa','dependency'=>$dep]);
       test(false,'activate-unexpected-return-'.$case);
    }catch(Throwable $e){
       $expected=$allowed?'REACHED_READY_COUNT_AFTER_AUDIT_GATE':'PSERC_PLAN_PSTE_AUDIT_NOT_CURRENT_BEFORE_ACTIVATE';
       test(str_contains($e->getMessage(),$expected),'compiler-activate-'.$case);
    }
 }
}
// A queued job may start while the audit is valid and lose its proof before ACTIVATE.
for($repeat=0;$repeat<50;$repeat++){
 PSTE_Breadth_Research_Queue::$state='valid';
 $s=PSERC_Plan_Compile_Job::start();
 test($s['status']==='COMPLETE','race-start-valid');
 PSTE_Breadth_Research_Queue::$state='missing';
 try{
   (new ReflectionMethod(PSERC_Plan_Compile_Job::class,'tickActivate'))->invoke(null,['generation'=>'safe-qa','dependency'=>$dep]);
   test(false,'race-activated-invalid');
 }catch(Throwable $e){test(str_contains($e->getMessage(),'PSERC_PLAN_PSTE_AUDIT_NOT_CURRENT_BEFORE_ACTIVATE'),'race-activate-revoked');}
 try{
   (new ReflectionMethod(PSERC_Admin::class,'exportSingleHandoff'))->invoke(null);
   test(false,'race-export-unexpected');
 }catch(Throwable $e){test(str_contains($e->getMessage(),'WP_DIE:Die gespeicherte Themenprüfung'),'race-export-revoked');}
 PSTE_Breadth_Research_Queue::$state='valid';
 test(PSERC_Plan_Dependency_Fingerprint::existingPsteAuditCurrent(),'race-recovered-audit-current');
}
print(json_encode(['status'=>'PASS','tests'=>$checks,'cycles'=>60,'race_cycles'=>50,'states'=>['valid','missing','throws'],'routes'=>['shared-audit-gate','compiler-start','admin-download-visibility','stale-warning','export-post-check','compiler-activate'],'wordpress_real_database'=>false,'simulated_options'=>true],JSON_PRETTY_PRINT|JSON_UNESCAPED_SLASHES)."\n");