<?php
/** Actual complete original PHP selection trait under isolated WordPress stubs.
 * No real database or product identity is supplied here: behavioral proof ONLY.
 * Usage: php QA69_SELECTION_NO_PREPUBLIC_PRUNE.php /path/to/trait-ppar-ebay.php
 */
error_reporting(E_ALL & ~E_DEPRECATED);
define('ABSPATH',__DIR__.'/');define('ARRAY_A','ARRAY_A');
function sanitize_key($x){return preg_replace('/[^a-z0-9_-]/','',strtolower((string)$x));}
function sanitize_text_field($x){return trim(strip_tags((string)$x));}
function absint($x){return abs((int)$x);}
function is_wp_error($x){return $x instanceof WP_Error;}
function get_option($key,$default=array()){return $GLOBALS['QAOPTIONS'][$key]??$default;}
function update_option($key,$value,$auto=false){$GLOBALS['QAOPTIONS'][$key]=$value;return true;}
class WP_Error extends Exception {function get_error_code(){return 'mock_failed';}function get_error_message(){return $this->getMessage();}}
class QA69DB {
 public $queries=0,$last_error='';
 public function prepare($sql,...$args){return ['sql'=>$sql,'args'=>$args];}
 public function get_results($query,$format=null){$this->queries++;return [];} // Empty data, never claim 283 products.
}
$GLOBALS['wpdb']=new QA69DB();$GLOBALS['QAOPTIONS']=[];
require $argv[1];
class QA69Runner {
 use PPAR_Ebay_Trait;
 public $canonical=true,$run=[],$tableCalls=0;
 public function __construct($canonical){$this->canonical=$canonical;
  $this->run=['schema'=>'1.0','status'=>'running','phase'=>'business_materialize','run_uuid'=>'97507628-4f4d-4527-bd77-fa573bce7067',
    'phase_state'=>[],'checkpoint_candidate'=>['business_campaign_ids'=>[],'private_listing_ids'=>[]]];
 }
 public function ebay_settings(){return ['business_enabled'=>true,'private_enabled'=>false];}
 public function ebay_normalize_settings($settings,$strict=true){return $settings;}
 public function ebay_run_load(){return $this->run;}
 public function ebay_run_checkpoint_staging_active(){return $this->canonical && ($this->run['status']??'')==='running' && is_array($this->run['checkpoint_candidate']??null);}
 public function ebay_run_phase_state_save($key,$value){$this->run['phase_state'][$key]=$value;return true;}
 public function ebay_items_table(){return 'wp_items';}
 public function ebay_db_formats($data){return array_fill(0,count($data),'%s');}
 public function invoke($state){$m=new ReflectionMethod($this,'ebay_selection_process_tick');$m->setAccessible(true);return $m->invoke($this,$this->ebay_settings(),$state);}
}
function caseRun($name,$canonical,$phase,$reason='canonical_run',$reuse=0){
 $GLOBALS['wpdb']->queries=0;$run=new QA69Runner($canonical);
 $state=['version'=>'2.0','owner'=>'run:97507628-4f4d-4527-bd77-fa573bce7067',
  'status'=>'running','phase'=>$phase,'reason'=>$reason,'selection_scope'=>'business',
  'business_target_mode'=>$reason==='canonical_gapfill'?'gapfill':'full',
  'business_target_concepts'=>[],'business_reuse_done'=>$reuse,'business_active'=>[],
  'business_reserve'=>[],'business_soft_failed'=>[],'stats'=>['business'=>['scanned'=>0,'materialized'=>0,'errors'=>[]]],
  'business_cursor'=>0,'business_prune_cursor'=>0];
 $out=$run->invoke($state);
 return ['name'=>$name,'canonical'=>$canonical,'begin'=>$phase,'reason'=>$reason,
 'end'=>$out['phase']??null,'status'=>$out['status']??null,
 'db_queries'=>$GLOBALS['wpdb']->queries,
 'canonical_cleanup_deferred_to_public_checkpoint'=>!empty($out['canonical_cleanup_deferred_to_public_checkpoint']),
 'run_uuid'=>$run->run['run_uuid'],'run_state'=>$run->run['status']];
}
$result=[];
$result[]=caseRun('full_old_prune_phase_recovery',true,'business_prune');
$result[]=caseRun('full_materialization_finishes_without_prune',true,'business_materialize');
$result[]=caseRun('gapfill_after_reuse_finishes_without_prune',true,'business_prune','canonical_gapfill',1);
$result[]=caseRun('standalone_keeps_existing_prune',false,'business_prune');
$result[]=caseRun('standalone_materialization_still_enters_prune',false,'business_materialize');
foreach($result as $x)echo json_encode($x,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)."\n";