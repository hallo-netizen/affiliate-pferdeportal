<?php
// Runs the ACTUAL QA86 PHP handlers and source-selection SQL with synthetic WP/eBay data.
// No network calls, no live data modifications, no new source or selection decision.
define('ABSPATH', __DIR__.'/'); define('HOUR_IN_SECONDS',3600); define('MINUTE_IN_SECONDS',60); define('ARRAY_A','ARRAY_A');
function sanitize_key($s){return preg_replace('/[^a-z0-9_-]/','',strtolower((string)$s));}
function sanitize_text_field($s){return trim(strip_tags((string)$s));}
function absint($v){return abs((int)$v);}
function is_wp_error($v){return $v instanceof WP_Error;}
class WP_Error extends Exception {public function __construct(private string $wpcode,$msg=''){parent::__construct($msg);}public function get_error_code(){return $this->wpcode;}}
$GLOBALS['opts']=[];
function get_option($key,$default=false){return $GLOBALS['opts'][$key]??$default;}
function update_option($key,$value,$autoload=false){$GLOBALS['opts'][$key]=$value;return true;}
function add_option($key,$value,$deprecated='',$autoload=false){if(array_key_exists($key,$GLOBALS['opts']))return false;$GLOBALS['opts'][$key]=$value;return true;}
function delete_option($key){unset($GLOBALS['opts'][$key]);return true;}
function rest_ensure_response($v){return $v;}
function get_post_meta($id,$key,$single=true){global $wpdb;foreach($wpdb->rows as $row){if($row['campaign_id']==$id){return ['_ppar_ebay_business_auto'=>1,'_ppar_creative_identity_hash'=>$row['creative_identity_hash'],'_ppar_ebay_business_match_contract'=>'concept_v3'][$key]??'';}}return '';}
class FakeDb {
 public $rows=[];public $last_error='';public $sql_calls=0,$source_reads=0,$any_outside_safe=0;
 public function prepare($sql,...$args){ if(count($args)===1 && is_array($args[0]))$args=$args[0]; foreach($args as $v){if(str_contains($sql,'%d'))$sql=preg_replace('/%d/',strval(intval($v)),$sql,1);else $sql=preg_replace('/%s/',"'".addslashes((string)$v)."'",$sql,1);}if(str_contains($sql,'%d')||str_contains($sql,'%s'))throw new Exception('Missing arg');return $sql; }
 public function get_row($sql,$format='ARRAY_A'){if(!preg_match("/creative_identity_hash='([a-f0-9]{64})'/",$sql,$match))throw new Exception('Bad hash lookup');foreach($this->rows as $row)if($row['creative_identity_hash']===$match[1])return $row;return null;}
 public function get_results($sql,$format='ARRAY_A'){
   $this->sql_calls++; if(!preg_match('/e\.id>(\d+)/',$sql,$m))throw new Exception('No cursor in SQL'); $cursor=intval($m[1]);
   if(preg_match('/o\.campaign_post_id IN \(([^)]+)\)/',$sql,$m)){
     $allowed=array_fill_keys(array_map('intval',explode(',',$m[1])),true);
   } else {$allowed=null;}
   $out=[];
   foreach($this->rows as $id=>$row){
     if($id<=$cursor || $row['output_status']!=='published' || $row['source_state']!=='available')continue;
     if($allowed!==null && !isset($allowed[$row['campaign_id']]))continue;
     if($row['source_checked_at']>time()-900)continue;
     if($row['fresh_until']>time()+7200)continue;
     $out[]=$row;if(count($out)>=20)break;
   }
   return $out;
 }
}
require $argv[1];require $argv[2];
class Runner {
  use PPAR_Ebay_Run_Trait;use PPAR_Ebay_Trait;
  const VERSION='test';const OPTION_EBAY_EXTERNAL_TICK_RATE_LOCK='rate';const OPTION_EBAY_RUN_STATE='run';const OPTION_EBAY_PUBLIC_CHECKPOINT='public_safe';
  public $remote_ids=[],$search_calls=0;
  private function ebay_items_table(){return 'fake_items';}private function output_objects_table(){return 'fake_output';}
  private function ebay_settings(){return ['enabled'=>true,'business_enabled'=>true,'inventory_refresh_enabled'=>true,'environment'=>'production','last_sync'=>['finished_at'=>time()],'last_refresh'=>['finished_at'=>time()]];}
  private function ebay_deletion_compliance_complete(){return true;}
  private function ebay_request_local_read_cache_allowed(){return false;}
  private function ebay_public_content_policy_reason_from_source_row($row,$title){return '';}
  public function delivery_allowed($campaign_id){return $this->ebay_business_campaign_source_allows_delivery(['network'=>'ebay','creative_type'=>'product','post_id'=>$campaign_id,'title'=>'Verified test']);}
  private function ebay_access_token($settings){return 'fake_token';}
  private function ebay_public_availability_state_save($key,$state){update_option($key,$state);return true;}
  private function ebay_public_availability_refresh_one(&$job,$row,$settings,$token){
      global $wpdb; $id=intval($row['id']);$wpdb->source_reads++;
      $this->remote_ids[]=$id;
      $wpdb->rows[$id]['fresh_until']=time()+6*HOUR_IN_SECONDS;
      $wpdb->rows[$id]['source_checked_at']=time();
      $job['summary']['available']=($job['summary']['available']??0)+1;
  }
  private function ebay_run_resume_failed_family_cap($run){return $run;}
  public function run_ebay_canonical_worker(){$this->search_calls++;return ['tick_result'=>'advanced'];}
  public function tick(){return $this->handle_ebay_external_tick([]);}
}
function main(){
 global $wpdb; $wpdb=new FakeDb();$now=time();
 // 9,792 historical sources, 496 previously published; only final 309 are SAFE.
 // Real snapshot counts are reused, but item identities and provider replies are SYNTHETIC.
 for($id=1;$id<=9792;$id++){
   $wpdb->rows[$id]=['id'=>$id,'campaign_id'=>100000+$id,'output_status'=>($id>9296?'published':'review'),
    'seller_account_type'=>'BUSINESS','source_state'=>'available','policy_state'=>'allowed','status'=>'active',
    'source_checked_at'=>$now-8*HOUR_IN_SECONDS,'fresh_until'=>$now-100,'item_end_at'=>0,
    'route_state'=>'ready','item_id'=>'item-'.$id,'creative_identity_hash'=>hash('sha256','item'.$id)];
 }
 $safe_ids=[];for($id=9484;$id<=9792;$id++)$safe_ids[]=100000+$id;
 $mode=$GLOBALS['argv'][3]??'full';if($mode==='empty')$safe_ids=[];
 $GLOBALS['opts']=[
 'public_safe'=>['schema'=>'1.0','status'=>'safe','checkpoint_id'=>'original-stored-public-shelf','business_campaign_ids'=>$safe_ids],
 'run'=>['schema'=>'1.0','run_uuid'=>'existing-real-run-not-reset','status'=>'completed','phase'=>'completed','operation'=>'sync','progress_seq'=>999,'finished_at'=>$now],
 'ppar_ebay_public_availability_state_v1'=>['running'=>1,'cursor'=>12568,'checked'=>448,'errors'=>24,'next_due_at'=>0],
 'untouched_global_publication'=>['pub'=>309,'old'=>'retained']
 ];
 $originalRun=$GLOBALS['opts']['run'];$originalSafe=$GLOBALS['opts']['public_safe'];$a=new Runner();$events=[];
 $beforeAllowed=$a->delivery_allowed($safe_ids[0]??109792);
 for($i=1;$i<=40;$i++){
   unset($GLOBALS['opts']['rate']);
   // Advance mock clock only by setting existing saved due timestamp; time() still real.
   if($i>1){$v=get_option('ppar_ebay_public_availability_state_v1',[]);$v['next_due_at']=0;update_option('ppar_ebay_public_availability_state_v1',$v);}
   $result=$a->tick();
   if($result instanceof WP_Error)throw new Exception('WP_Error '.$result->get_error_code());
   $state=get_option('ppar_ebay_public_availability_state_v1',[]);
   $events[]=['heartbeat'=>$i,'transport_status'=>$result['status'],'reason'=>$result['reason']??'',
   'source_checks'=>count($a->remote_ids),'cursor'=>$state['cursor']??null,'running'=>$state['running']??null];
   if(empty($state['running']))break;
 }
 $unique=array_unique($a->remote_ids);$safe_source_ids=array_fill_keys(range(9484,9792),true);
 $afterAllowed=$a->delivery_allowed(109792);
 // A stale output record outside the SAFE checkpoint never becomes public, even when its source is fresh.
 $wpdb->rows[9297]['fresh_until']=time()+3600;
 $outsideAllowed=$a->delivery_allowed(109297);
 $outOfSafe=count(array_filter($a->remote_ids,fn($id)=>!isset($safe_source_ids[$id])));
 $checks=count($a->remote_ids);$state=get_option('ppar_ebay_public_availability_state_v1',[]);
 $checksPassed=$checks===(($mode==='empty')?0:309) && count($unique)===(($mode==='empty')?0:309)
   && $outOfSafe===0 && $a->search_calls===0 && $wpdb->source_reads===$checks
   && $GLOBALS['opts']['run']===$originalRun && $GLOBALS['opts']['public_safe']===$originalSafe
   && empty($state['running']) && ($state['cursor']??-1)===0
   && ($state['checked']??0)===(($mode==='empty')?448:757)
   && ($state['safe_checkpoint_id']??'')==='original-stored-public-shelf'
   && !$beforeAllowed && !$outsideAllowed && ($mode==='empty'?!$afterAllowed:$afterAllowed);
 echo json_encode(['status'=>$checksPassed?'PASS':'FAIL','model'=>'real PHP + modeled 9792 source rows / 496 older published / 309 SAFE',
 'basic_gate_before_refresh'=>$beforeAllowed,'basic_gate_after_refresh'=>$afterAllowed,'old_outside_safe_gate'=>$outsideAllowed,
 'check_count'=>$checks,'source_checks_unique'=>count($unique),'out_of_safe'=>$outOfSafe,
 'heartbeat_count'=>count($events),'last_3_events'=>array_slice($events,-3),'canonical_search_new_calls'=>$a->search_calls,
 'same_original_run'=>$GLOBALS['opts']['run']===$originalRun,'same_public_safe'=>$GLOBALS['opts']['public_safe']===$originalSafe,
 'old_checked'=>448,'new_checked'=>$state['checked']??null,'final_availability_state'=>$state],JSON_UNESCAPED_UNICODE|JSON_PRETTY_PRINT)."\n";
 exit($checksPassed?0:1);
}
main();