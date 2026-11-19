<?php
// Tests ORIGINAL independent availability tick against a paused research run;
// only WP database rows and provider responses are substituted.
error_reporting(E_ALL & ~E_DEPRECATED);
define('ABSPATH','/tmp');define('HOUR_IN_SECONDS',3600);define('MINUTE_IN_SECONDS',60);define('ARRAY_A','ARRAY_A');
$GLOBALS['opt']=[];$GLOBALS['transient']=[];
function get_option($k,$d=null){return $GLOBALS['opt'][$k]??$d;}function update_option($k,$v,$autoload=false){$GLOBALS['opt'][$k]=$v;return true;}
function get_transient($k){return $GLOBALS['transient'][$k]??false;}function set_transient($k,$v,$ttl){$GLOBALS['transient'][$k]=$v;return true;}function delete_transient($k){unset($GLOBALS['transient'][$k]);return true;}
function absint($v){return abs((int)$v);}function sanitize_key($v){return preg_replace('/[^a-z0-9_\-]/','',strtolower((string)$v));}function sanitize_text_field($v){return trim(strip_tags((string)$v));}function is_wp_error($x){return $x instanceof WP_Error;}
class WP_Error{}
class TestDB {
 public $last_error='';public $round=0;public $queries=[];
 public function prepare($sql,...$args){$this->queries[]=['sql'=>$sql,'args'=>$args];return $sql;}
 public function get_results($sql,$mode){$this->round++;return $this->round===1?[
   ['id'=>1,'campaign_id'=>901,'creative_identity_hash'=>str_repeat('a',64),'item_end_at'=>0],
   ['id'=>2,'campaign_id'=>902,'creative_identity_hash'=>str_repeat('b',64),'item_end_at'=>time()-10],
   ['id'=>3,'campaign_id'=>903,'creative_identity_hash'=>str_repeat('c',64),'item_end_at'=>0]
 ]:[];}
 public function get_col($sql){return [901];}
}
require __DIR__.'/affiliate-portal-router/includes/trait-ppar-ebay.php';
class AvailProbe {
 use PPAR_Ebay_Trait;
 const EBAY_REFRESH_CRON_HOOK='test_refresh_hook',EBAY_RUNTIME_BUILD='test';
 public $checked=[],$published=[],$api_calls=0;
 private function ebay_settings(){return ['enabled'=>true,'business_enabled'=>true,'environment'=>'staging'];}
 private function ebay_deletion_compliance_complete(){return true;}
 private function ebay_access_token($settings){return 'token';}
 public function ebay_items_table(){return 'sample_items';} public function output_objects_table(){return 'sample_outputs';}
 public function ebay_refresh_process_row(&$job,$row,$settings,$token){$id=$row['id'];$this->checked[]=$id;$job['summary']['checked']++;
   if($id===2){$job['summary']['ended']++;return;}
   if($id===3){$job['summary']['technical_errors']++;return;}
   $job['summary']['available']++;
 }
 public function ebay_public_checkpoint_add_verified_business_ids($ids,$reason){$this->published=array_merge($this->published,$ids);return count($ids);}
}
function ok($c,$s){if(!$c)throw new Exception('FAIL '.$s);echo 'PASS '.$s."\n";}
$run=['schema'=>'1.0','run_uuid'=>'the-same-paused-discovery-run','status'=>'paused','phase'=>'gapfill_discovery','progress_seq'=>881,'cursor'=>98,'checkpoint_candidate'=>['business_campaign_ids'=>[901]]];
$GLOBALS['opt']['ppar_ebay_run_state_v1']=$run; $GLOBALS['wpdb']=new TestDB();$p=new AvailProbe();
$result=$p->ebay_public_availability_tick();ok($result['status']==='complete' && $result['checked']===3,'original independent availability tick processes 3 records');
ok($p->checked===[1,2,3],'one ended and one provider failed offer do not stop third item');
ok($p->published===[901],'only confirmed available campaign appended to SAFE checkpoint');
ok($GLOBALS['opt']['ppar_ebay_run_state_v1']===$run,'paused discovery UUID/cursor/checkpoint untouched');
$state=$GLOBALS['opt']['ppar_ebay_public_availability_state_v1'];
ok($state['available']===1 && $state['ended']===1 && $state['errors']===1,'availability counts distinguish available / ended / error');
ok($state['running']===0 && $state['next_due_at']>=time()+7100,'next verification due about 2h independent of search');
$again=$p->ebay_public_availability_tick();ok($again['status']==='not_due','no immediate duplicate availability check');
echo 'QA15_INDEPENDENT_AVAILABILITY_TEST_PASSED\n';