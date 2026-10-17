<?php
declare(strict_types=1);
error_reporting(E_ALL);
define('ABSPATH','/tmp/');define('DAY_IN_SECONDS',86400);define('PSTE_VERSION','0.57.103');
define('PSTE_OPTION_SITE_BASELINE','pste_baseline');define('PSTE_OPTION_SANDBOX_MAINTENANCE_HEALTH','pste_health');
define('PSTE_OPTION_SEMANTIC_SANDBOX_LOCK','pste_lock');define('PSTE_OPTION_SEMANTIC_SANDBOX','pste_legacy_full');
define('PSTE_SANDBOX_INTERNAL_RECHECK_CRON_HOOK','pste_daily_recheck');
$GLOBALS['options']=['pste_baseline'=>['contract'=>'PSTE_SITE_BASELINE_V1','structure_sha256'=>str_repeat('a',64),'protected_category_map_sha256'=>str_repeat('b',64)]];
$GLOBALS['option_reads']=[];$GLOBALS['single_events']=[];$GLOBALS['fail_cursor_write']=false;
function check($ok,string $msg):void {if(!$ok)throw new RuntimeException($msg);}
function get_option($k,$d=false){$GLOBALS['option_reads'][$k]=($GLOBALS['option_reads'][$k]??0)+1;return $GLOBALS['options'][$k]??$d;}
function update_option($k,$v,$autoload=null){if($k==='pste_health'&&$GLOBALS['fail_cursor_write'])return false;$GLOBALS['options'][$k]=$v;return true;}
function add_option($k,$v,$dummy='',$autoload=false){if(isset($GLOBALS['options'][$k]))return false;$GLOBALS['options'][$k]=$v;return true;}
function delete_option($k){unset($GLOBALS['options'][$k]);return true;}
function wp_json_encode($v,$opts=0){return json_encode($v,$opts);}
function wp_cache_delete($k,$g=''){return true;}
function maybe_unserialize($s){return unserialize($s);}
function wp_next_scheduled($name){return time()+86400;}
function wp_schedule_single_event($at,$hook){$GLOBALS['single_events'][]=[$at,$hook];return true;}
class DB {public string $options='wp_options',$last_error='';function prepare($s,...$args){return $s;}function get_var($sql){return serialize($GLOBALS['options']['pste_lock']??null);}function get_row($sql,$mode){return ['payload_json'=>json_encode(['primary_longtail_query'=>'Wie funktioniert Pferdepflege?','query_record'=>['source'=>'SAMPLE']]),'pool_key'=>'sample'];}}
$GLOBALS['wpdb']=new DB;define('ARRAY_A','ARRAY_A');
class PSTE_DB_Write_Guard {public static function query($sql,$reason){delete_option('pste_lock');return 1;}}
class PSTE_Plugin {public static function assertReady():void{}}
class PSTE_Editorializer {public const RULESET='ACTIVE_TITLE_RULESET';}
class PSTE_Article_Type_Registry {public static function build($b){return ['registry_sha256'=>'registry_ok'];}}
class PSTE_Snapshot {public static int $inventories=0;public static function inventory(){self::$inventories++;return ['inventory_ok'=>true];}}
class PSTE_Repository {public static function table($k){return 'wp_topic_pool';}}
class PSTE_Sandbox_Internal_Planner {public static int $calls=0;public static function plan($r,$registry,$baseline,$external,$payload,$inventory){self::$calls++;if(($r['pool_key']??'')==='fail_11')throw new RuntimeException('SIMULATED_FAMILY_UNRESOLVED');return ['status'=>'PROPOSAL_READY_FOR_REVIEW','target_category'=>'stallsicherheit'];}}
class PSTE_Sandbox_Record_Store {
 public static array $rows=[], $readCounts=[],$writes=[];public static bool $failNextWrite=false;
 public static function isComplete(){return true;}
 public static array $header=['job'=>null];public static function legacyHeader(){return self::$header;}
 public static function recordIds(){$ids=array_keys(self::$rows);sort($ids,SORT_STRING);return $ids;}
 public static function getRecord($id){self::$readCounts[$id]=(self::$readCounts[$id]??0)+1;return self::$rows[$id];}
 public static function putRecordsBatch($items){if(self::$failNextWrite){self::$failNextWrite=false;throw new RuntimeException('SIMULATED_WRITE_FAILURE');}check(count($items)<=25,'unbounded write');foreach($items as $id=>$row)self::$rows[$id]=$row;self::$writes[]=count($items);}
}
for($i=0;$i<65;$i++){
 $id=str_pad((string)$i,64,'0',STR_PAD_LEFT);
 $eligible=$i%3!==0;
 PSTE_Sandbox_Record_Store::$rows[$id]=['sandbox_id'=>$id,'status'=>$eligible?'STRUCTURE_GAP':'RETAINED_NOT_RELEVANT',
 'pool_key'=>$i===11?'fail_11':'sample_'.$i,'current_relevance_proof'=>['status'=>$eligible?'RELEVANT_FOR_PORTAL':'NOT_RELEVANT_FOR_PORTAL'],'history'=>[]];
}
require (getenv('PSTE_SOURCE_DIR')?:'/mnt/data/seo_work/modified/Portal SEO Topic Engine').'/includes/class-pste-semantic-review-sandbox.php';
$r1=PSTE_Semantic_Review_Sandbox::refreshInternalStructureBacklog(false);
check($r1['status']==='IN_PROGRESS'&&$r1['cursor']===25&&$r1['total']===65,'first batch cursor');
check(count(PSTE_Sandbox_Record_Store::$readCounts)===25,'first batch read more than 25');
check(!isset($GLOBALS['option_reads']['pste_legacy_full']),'legacy 58MiB Sandbox was loaded');
check(count($GLOBALS['single_events'])===1,'automatic continuation not scheduled');
// Freshly retained keywords appearing during a run may change sort positions.
// Offset-only continuation would skip them. The bound set must restart safely.
$idNew='0000000000000000000000000000000000000000000000000000000000000000';
$idNew=substr($idNew,0,-1).'A'; // distinct before other sorted IDs
PSTE_Sandbox_Record_Store::$rows[$idNew]=['sandbox_id'=>$idNew,'status'=>'STRUCTURE_GAP','pool_key'=>'new_source','current_relevance_proof'=>['status'=>'RELEVANT_FOR_PORTAL'],'history'=>[]];
$rChanged=PSTE_Semantic_Review_Sandbox::refreshInternalStructureBacklog(false);
check($rChanged['cursor']===25&&$rChanged['total']===66,'new keyword did not reset bound cursor');
check((PSTE_Sandbox_Record_Store::$rows[$idNew]['status']??'')==='PROPOSAL_READY_FOR_REVIEW','new keyword skipped on added record');
unset(PSTE_Sandbox_Record_Store::$rows[$idNew]);
// Removing the inserted test record also resets the set-bound cursor.
$rRestart=PSTE_Semantic_Review_Sandbox::refreshInternalStructureBacklog(false);
check($rRestart['cursor']===25&&$rRestart['total']===65,'restored record set not replayed');
$r2=PSTE_Semantic_Review_Sandbox::refreshInternalStructureBacklog(false);
check($r2['status']==='IN_PROGRESS'&&$r2['cursor']===50,'second batch did not resume');
$r3=PSTE_Semantic_Review_Sandbox::refreshInternalStructureBacklog(false);
check($r3['status']==='PARTIAL_FAILURE'&&$r3['cursor']===65&&$r3['complete']===true,'partial failure not retained at completion');
check($r3['total_failed']===1,'failed keyword not counted');
check((PSTE_Sandbox_Record_Store::$rows[str_pad('11',64,'0',STR_PAD_LEFT)]['status']??'')==='STRUCTURE_GAP','failed keyword was wrongly dropped');
$r4=PSTE_Semantic_Review_Sandbox::refreshInternalStructureBacklog(false);
check($r4['status']==='NOT_DUE'&&$r4['checked']===0,'unchanged successful scan repeated');
check(!isset($GLOBALS['option_reads']['pste_legacy_full']),'legacy registry read');
$GLOBALS['options']['pste_baseline']['protected_category_map_sha256']=str_repeat('c',64);
$r5=PSTE_Semantic_Review_Sandbox::refreshInternalStructureBacklog(false);
check($r5['status']==='IN_PROGRESS'&&$r5['cursor']===25,'category change did not reset scan');
$r6=PSTE_Semantic_Review_Sandbox::refreshInternalStructureBacklog(true);
check($r6['status']==='IN_PROGRESS'&&$r6['cursor']===50,'manual retry discarded ongoing work');
$GLOBALS['fail_cursor_write']=true;
$old=$GLOBALS['options']['pste_health']['structure_recheck_v1']['cursor'];
try{PSTE_Semantic_Review_Sandbox::refreshInternalStructureBacklog(false);throw new RuntimeException('silently ignored failed progress write');}
catch(RuntimeException $e){check($e->getMessage()==='PSTE_SANDBOX_RECHECK_CURSOR_NOT_SAVED','incorrect save error');}
check($GLOBALS['options']['pste_health']['structure_recheck_v1']['cursor']===$old,'cursor advanced despite failed persistence');
$GLOBALS['fail_cursor_write']=false;
$r7=PSTE_Semantic_Review_Sandbox::refreshInternalStructureBacklog(false);
check($r7['complete']===true&&$r7['cursor']===65,'resume after write failure');
check(!isset($GLOBALS['option_reads']['pste_legacy_full']),'forbidden full legacy load');
check(count(PSTE_Sandbox_Record_Store::$rows)===65,'records lost');
// The existing active-job guard must also work on the record-local path.
PSTE_Sandbox_Record_Store::$header['job']=['status'=>'RUNNING'];
try{PSTE_Semantic_Review_Sandbox::refreshInternalStructureBacklog(true);throw new RuntimeException('active job not blocked');}
catch(RuntimeException $e){check($e->getMessage()==='PSTE_SANDBOX_REVIEW_BLOCKED_WHILE_JOB_ACTIVE','active job bypassed');}
PSTE_Sandbox_Record_Store::$header['job']=null;
// Tampering with the stored resume cursor must never skip a slice.
$GLOBALS['options']['pste_health']['structure_recheck_v1']['cursor']=999;
try{PSTE_Semantic_Review_Sandbox::refreshInternalStructureBacklog(false);throw new RuntimeException('tampered cursor went unnoticed');}
catch(RuntimeException $e){check($e->getMessage()==='PSTE_SANDBOX_RECHECK_PROGRESS_HASH_INVALID','tampered progress accepted or wrong error');}
// A routine weekly check must be possible with unchanged categories/rules, without provider calls.
$progress=$GLOBALS['options']['pste_health']['structure_recheck_v1'];$progress['cursor']=65;$progress['last_completed_at_utc']=gmdate('c',time()-8*DAY_IN_SECONDS);
$method=new ReflectionMethod('PSTE_Semantic_Review_Sandbox','internalStructureRecheckProgressHash');
$progress['checkpoint_sha256']=$method->invoke(null,$progress);$GLOBALS['options']['pste_health']['structure_recheck_v1']=$progress;
$r8=PSTE_Semantic_Review_Sandbox::refreshInternalStructureBacklog(false);
check($r8['status']==='IN_PROGRESS'&&$r8['cursor']===25,'weekly safety net did not restart');
echo json_encode(['status'=>'PASS','bounded_batch'=>25,'records_retained'=>65,'first_run_status'=>$r1['status'],'partial_status'=>$r3['status'],'category_change'=>'RECHECK_RESTARTED','manual_continuation'=>'PASS','failed_write_cursor_rollback'=>'PASS','tampered_cursor_rejected'=>'PASS','weekly_retry'=>'PASS','active_job_isolation'=>'PASS','new_keyword_rescan'=>'PASS','legacy_full_reads'=>0,'scheduled_continuations'=>count($GLOBALS['single_events']),'per_record_write_max'=>max(PSTE_Sandbox_Record_Store::$writes)],JSON_PRETTY_PRINT)."\n";