<?php
/** QA50 adversarial public-commit integration; actual plugin's public_verify,
 * safe-gap-contract and public checkpoint COMMIT methods; only WP stores and
 * already-verified provider coverage results are simulated. */
error_reporting(E_ALL & ~E_DEPRECATED);
define('ABSPATH', __DIR__.'/'); define('MINUTE_IN_SECONDS', 60); define('ARRAY_A','ARRAY_A');
function sanitize_key($x){return preg_replace('/[^a-z0-9_-]/','',strtolower((string)$x));}
function sanitize_text_field($x){return trim(strip_tags((string)$x));}
function absint($x){return abs((int)$x);}
function is_wp_error($x){return $x instanceof WP_Error;}
function wp_json_encode($x,$f=0){return json_encode($x,$f);}
class WP_Error extends Exception{function get_error_code(){return 'test_error';}function get_error_message(){return $this->getMessage();}}
function sanitize_title($x){return sanitize_key($x);}
class QA50WPDB {
 public $last_error='', $sources=[], $creatives=[], $outputs=[], $deny=false;
 public function prepare($sql,...$args){return ['sql'=>$sql,'args'=>$args];}
 public function get_results($q,$format=null){
   $sql=is_array($q)?$q['sql']:(string)$q;$args=is_array($q)?$q['args']:[];
   if($this->deny){$this->last_error='synthetic DB unavailable';return null;}
   $this->last_error='';
   if(str_contains($sql,'wp_outputs')){
     $list=array_values($this->outputs);
     if(count($args)>0){$list=array_values(array_filter($list,fn($r)=>in_array($r['creative_identity_hash'],$args,true)));}
     return $list;
   }
   if(str_contains($sql,'wp_items') && str_contains($sql,'WHERE id>')){
     $cursor=(int)($args[0]??0);$max=max(1,(int)end($args));
     $targets=(str_contains($sql,'rule_id IN'))?array_slice($args,1,-1):[];
     $rows=array_values(array_filter($this->sources,function($r)use($cursor,$targets){
       return (int)$r['id']>$cursor && (!$targets || in_array($r['rule_id'],$targets,true));
     }));
     usort($rows,fn($a,$b)=>(int)$a['id']<=>(int)$b['id']);
     return array_slice($rows,0,$max);
   }
   if(str_contains($sql,'wp_items'))return array_values(array_filter($this->sources,fn($r)=>in_array($r['creative_identity_hash'],$args,true)));
   if(str_contains($sql,'wp_creatives'))return array_values(array_filter($this->creatives,fn($r)=>in_array($r['identity_hash'],$args,true)));
   throw new Exception('UNEXPECTED SQL get_results '.substr($sql,0,220));
 }
 public function get_row($q,$format=null){
  $this->last_error='';
  $args=is_array($q)?($q['args']??[]):[];$v=(string)($args[0]??'');
  foreach($this->sources as $source){if($source['item_id']===$v || $source['creative_identity_hash']===$v || (string)$source['id']===$v)return $source;}
  return null;
 }
 public function get_var($q){$args=is_array($q)?($q['args']??[]):[];$id=(int)($args[0]??0);return isset($this->outputs[$id])?$id:null;}

}
$GLOBALS['wpdb']=new QA50WPDB();

require $argv[1];
/** QA50: Real canonical controller and ALL phase methods, no tick_* overridden.
 * WP SQL + eBay discovery, refresh and nested selection engine stubbed.
 * Source and creative proof is checked by the real PHP public-coverage gate. */
class FullPipeline50 {
 use PPAR_Ebay_Run_Trait;
 const VERSION='6.72.341';
 const EBAY_RUNTIME_BUILD='6.63.8-self-driven-canonical-orchestrator-rootfix-20260829';
 const OPTION_EBAY_EXTERNAL_TICK_RATE_LOCK='qa50_rate_lock';
 public $run,$cp,$selection=[],$sync=[], $refresh=[], $maintenance=[], $tickLog=[], $lastError='', $newSearches=0,$selectionCalls=0,$writes=0,$scenario='normal',$injected=false;
 public function __construct($scenario='normal'){
  $this->scenario=$scenario;
  $this->cp=['status'=>'safe','checkpoint_id'=>'old-safe-578','business_campaign_ids'=>range(1001,1578),'private_listing_ids'=>[],'source'=>'old_safe'];
  foreach(range(1001,1580) as $id){
   $family=$this->familyForId($id);$hash=hash('sha256',(string)$id);$item='ebay-item-'.$id;
   $GLOBALS['wpdb']->outputs[$id]=['id'=>$id,'campaign_post_id'=>$id,'provider'=>'ebay','status'=>'published','output_type'=>'product_campaign','creative_identity_hash'=>$hash,'image_url'=>'https://images.example.org/horse.jpg'];
   $GLOBALS['wpdb']->sources[$hash]=['id'=>$id,'item_id'=>$item,'creative_identity_hash'=>$hash,'rule_id'=>$family,'source_state'=>'available','policy_state'=>'allowed','route_state'=>'ready','fresh_until'=>time()+86400,'item_end_at'=>0,'title'=>'Safe horse product','status'=>'ready','image_url'=>'https://images.example.org/horse.jpg'];
   $GLOBALS['wpdb']->creatives[$hash]=['id'=>$id,'identity_hash'=>$hash,'provider'=>'ebay','source_kind'=>'ebay_business_item','creative_type'=>'product','payload'=>json_encode(['ebay_verified_product_concept'=>$family,'ebay_item_id'=>$item])];
  }
  $this->run=['schema'=>'1.0','run_uuid'=>'qa50-original-full-phase','status'=>'running','phase'=>'reconcile_local','operation'=>'sync','remote_subphase'=>'discovery',
   'config_snapshot'=>['seller_routes'=>['business'=>true],'settings'=>[]],'progress_seq'=>0,'progress_contract_version'=>'qa50',
   'transport_tick_count'=>0,'errors'=>[],'started_at'=>time(),'last_progress_at'=>time(),'last_transport_tick_at'=>0,
   'phase_state'=>[],'checkpoint_candidate'=>['business_campaign_ids'=>[],'private_listing_ids'=>[]],
   'checkpoint_cleanup_selection'=>[],'gapfill'=>['attempts'=>0],
   'owner'=>'','lease_expires_at'=>0,'no_progress_count'=>0,'resume_at'=>0];
  if($scenario==='old_blocked'){
    $h=hash('sha256','1001');$GLOBALS['wpdb']->sources[$h]['status']='blocked_manual';
  }
  if($scenario==='new_blocked'){
    $h=hash('sha256','1579');$GLOBALS['wpdb']->sources[$h]['status']='blocked_manual';
  }
  $this->maintenance=['status'=>'completed','last_stats'=>['scanned'=>200]];
  $this->refresh=['status'=>'completed','summary'=>['checked'=>300]];
 }
 public function loop($max=35){
   $previous='';$ticks=0;
   for($i=0;$i<$max && $this->run['status']==='running';$i++){
     $phase=$this->run['phase'];
     if($this->scenario==='db_down' && $phase==='public_verify')$GLOBALS['wpdb']->deny=true;
     if($this->scenario==='churn' && !$this->injected && $phase==='coverage_verify' && ($this->run['gapfill']['attempts']??0)>0){
       $h=hash('sha256','1001');$GLOBALS['wpdb']->sources[$h]['source_state']='ended';$this->injected=true;
     }
     $r=$this->run_ebay_canonical_worker();
     $ticks++;
     $this->tickLog[]=['tick'=>$ticks,'before'=>$phase,'after'=>$this->run['phase'],'result'=>$r['tick_result']??'?',
         'candidate_count'=>count($this->run['checkpoint_candidate']['business_campaign_ids']??[]),
         'public_safe_count'=>count($this->cp['business_campaign_ids']??[]),
         'cursor'=>$this->run['progress_seq']??0,
         'covered'=>$this->run['coverage']['covered']??null,
         'error'=>$this->run['error_code']??null];
     if($r['tick_result']==='failed'){break;}
   }
   return $this->tickLog;
 }
 public function familyForId($id){
    if($id>=1579)return 'family'.str_pad(258+($id-1579),3,'0',STR_PAD_LEFT);
    if($id<=1096)$n=$id-1000;
    else $n=97+(($id-1097)%161);
    return 'family'.str_pad($n,3,'0',STR_PAD_LEFT);
 }
 public function ebay_business_required_product_concept_ids(){return array_map(fn($i)=>'family'.str_pad($i,3,'0',STR_PAD_LEFT),range(1,283));}
 private function ebay_run_load(){return $this->run;}
 private function ebay_run_save($r){$this->run=$r;return $r;}
 private function ebay_run_is_open($r){return ($r['status']??'')==='running';}
 private function ebay_run_acquire_lease(&$run){$token='qa50-lease';$run['owner']=$token;$run['lease_expires_at']=time()+300;$this->ebay_run_save($run);return $token;}
 private function ebay_run_release_lease($token){$this->run['owner']='';$this->run['lease_expires_at']=0;}
 private function ebay_run_stop_requested($r=null){return false;}
 private function ebay_run_finish_requested_stop($r,$token){return false;}
 private function ebay_run_progress_contract_version(){return 'qa50';}
 private function ebay_run_effective_settings($r){return $this->ebay_settings();}
 private function ebay_settings(){return ['enabled'=>true,'environment'=>'test','business_enabled'=>true,'private_enabled'=>false,'inventory_refresh_enabled'=>false];}
 private function ebay_deletion_compliance_complete(){return true;}
 private function ebay_items_table(){return 'wp_items';}
 private function output_objects_table(){return 'wp_outputs';}
 private function creative_library_table(){return 'wp_creatives';}
 private function ebay_public_content_policy_reason_from_source_row($r,$title){return '';}
 private function ebay_remote_image_url_validate($url){return str_starts_with($url,'https://')?$url:'';}
 private function ebay_business_verified_source_claims($r){$f=$r['rule_id'];return [$f=>['classification'=>['evidence_hash'=>'proof-'.$f,'score'=>99,'product_target_slugs'=>[$f]]]];}
 private function ebay_business_verified_creative_contracts($c){$d=json_decode($c['payload'],true);$f=$d['ebay_verified_product_concept'];return [$f=>['evidence_hash'=>'proof-'.$f,'score'=>99,'product_target_slugs'=>[$f]]];}
 private function automation_normalize_target_key($x){return sanitize_key(str_replace(':','-',(string)$x));}
 private function output_campaign_by_post_id($id){$f=$this->familyForId($id);return ['id'=>$id,'active'=>true,'network'=>'ebay','creative_type'=>'product','automation_target_keys'=>['page:'.$f]];}
 private function ebay_business_campaign_source_allows_delivery_base($c){
  if(empty($c['active']))return false;
  $row=$GLOBALS['wpdb']->sources[hash('sha256',(string)($c['id']??0))]??null;
  return is_array($row)
    && ($row['status']??'')!=='blocked_manual'
    && ($row['source_state']??'')==='available'
    && ($row['policy_state']??'')==='allowed'
    && (int)($row['fresh_until']??0)>time();
 }
 private function ebay_public_checkpoint_load(){return $this->cp;}
 private function ebay_public_checkpoint_is_safe($cp){return is_array($cp)&&($cp['status']??'')==='safe';}
 private function ebay_public_checkpoint_business_ids($cp=null){return (array)(($cp??$this->cp)['business_campaign_ids']??[]);}
 private function ebay_public_checkpoint_save($cp){
    if($this->scenario==='save_fail' && $this->writes>=1){return false;}
    $this->cp=$cp;$this->writes++;return $cp;
 }
 private function article_hybrid_enabled(){return false;}
 private function run_ebay_maintenance_v2($n,$a,$b,$c){return ['processed'=>100];}
 private function ebay_maintenance_state_load(){return $this->maintenance;}
 private function ebay_maintenance_state_is_current($s){return ($s['status']??'')==='completed';}
 private function ebay_refresh_job_load(){return $this->refresh;}
 private function ebay_refresh_job_is_open($r){return ($r['status']??'')==='running';}
 private function ebay_refresh_job_is_resumable_partial($r){return false;}
 private function ebay_refresh_job_is_bounded_manual_partial($r){return false;}
 private function ebay_run_selection_scope($r){return 'business';}
 private function ebay_selection_state_load(){return $this->selection;}
 private function ebay_selection_state_is_open($s){return ($s['status']??'')==='running';}
 private function ebay_selection_request($reason,$owner,$safe,$scope){
    $this->selectionCalls++;
    $targets=$reason==='canonical_gapfill'?(array)($this->run['gapfill']['missing']??[]):$this->ebay_business_required_product_concept_ids();
    $this->selection=['status'=>'running','reason'=>$reason,'selection_scope'=>$scope,'owner'=>$owner,'phase'=>'prepare','business_target_mode'=>$reason==='canonical_gapfill'?'gapfill':'full','business_target_concepts'=>$targets,
       'business_active'=>[],'business_reserve'=>[],'business_soft_failed'=>[],'stats'=>['business'=>[]]];
    return $this->selection;
 }
 private function ebay_selection_process_tick($settings,$state){
    if(($this->selection['phase']??'')==='prepare'){$this->selection['phase']='business_materialize';}
    else {
      $chosen=($this->selection['reason']??'')==='canonical_gapfill'
        ?($this->scenario==='no_new'?[]:[1579,1580]):range(1001,1096);
      foreach($chosen as $id){$f=$this->familyForId($id);$this->selection['business_active']['ebay-item-'.$id]=['concept'=>$f,'post_id'=>$id];}
      $this->selection['status']='complete';$this->selection['phase']='complete';
    }
    return $this->selection;
 }
 private function ebay_sync_job_load(){return $this->sync;}
 private function ebay_sync_job_is_open($j){return ($j['status']??'')==='running';}
 private function ebay_start_sync_job($manual,$scope,$mode){$this->newSearches++;$this->sync=['status'=>'running','scope'=>$scope];return $this->sync;}
 private function run_ebay_sync_worker($x){$this->sync=['status'=>'completed','scope'=>'business_recovery'];return $this->sync;}
private function ebay_selection_prune_business_batch($settings, &$state, $limit = 20, $commit_public = false, $terminal_transition = true) {
        global $wpdb;
        $staging = !$commit_public && method_exists($this,'ebay_run_checkpoint_staging_active') && $this->ebay_run_checkpoint_staging_active();
        if(!is_object($wpdb)||!method_exists($wpdb,'get_results')||!method_exists($wpdb,'prepare')){
            $state['phase']='failed';$state['status']='failed';$state['completed_at']=time();
            $state['failure_reason']='storage_unavailable_prune';
            return 0;
        }
        $limit=max(1,min(50,absint($limit)));
        $table=$this->ebay_items_table();$cursor=absint($state['business_prune_cursor']??0);
        // The gap-fill cleanup only ever acts on its targeted product families.
        // Filter at the database instead of reading every unrelated BUSINESS
        // source row. Keep the original ID cursor and full-prune path intact.
        $gapfill=sanitize_key((string)($state['business_target_mode']??''))==='gapfill';
        $target_ids=array();
        if($gapfill){
            $target_ids=array_values(array_unique(array_filter(array_map('sanitize_key',(array)($state['business_target_concepts']??array())))));
        }
        if($gapfill && $target_ids){
            $marks=implode(',',array_fill(0,count($target_ids),'%s'));
            $sql="SELECT * FROM {$table} WHERE id>%d AND seller_account_type='BUSINESS' AND rule_id IN ({$marks}) ORDER BY id ASC LIMIT %d";
            $rows=$wpdb->get_results($wpdb->prepare($sql,...array_merge(array($cursor),$target_ids,array($limit))),ARRAY_A);
        }else{
            $rows=$wpdb->get_results($wpdb->prepare(
                "SELECT * FROM {$table} WHERE id>%d AND seller_account_type='BUSINESS' ORDER BY id ASC LIMIT %d",
                $cursor,$limit
            ),ARRAY_A);
        }
        if (!is_array($rows) || (string)($wpdb->last_error ?? '') !== '') {
            $state['phase']='failed';$state['status']='failed';$state['failed_at']=time();
            $state['failure_reason']='ebay_business_selection_storage_read_failed';
            $state['stats']['business']['errors'][]=array('code'=>'ebay_business_selection_storage_read_failed');
            return 0;
        }
        $stats=is_array($state['stats']['business']??null)?$state['stats']['business']:array();
        foreach($rows as $row){
            $row_id=absint($row['id']??0);if($row_id<=0){continue;}
            $state['business_prune_cursor']=max(absint($state['business_prune_cursor']??0),$row_id);
            $item_id=(string)($row['item_id']??'');
            $end=absint($row['item_end_at']??0);
            if(sanitize_key((string)($row['source_state']??''))==='ended'||($end>0&&$end<=time())){continue;}
            if(isset($state['business_active'][$item_id])){continue;}
            // Soft-failed candidate state (review/repair_pending or verified LKG)
            // is authoritative and must not be rewritten back to ready/candidate.
            if(isset($state['business_soft_failed'][$item_id])){continue;}
            if(sanitize_key((string)($state['business_target_mode']??''))==='gapfill'){
                $targets=array_fill_keys(array_values(array_filter(array_map('sanitize_key',(array)($state['business_target_concepts']??array())))),true);
                $concept=sanitize_key((string)($row['rule_id']??''));
                if($concept==='' || !isset($targets[$concept])){continue;}
            }
            if(isset($state['business_reserve'][$item_id])){
                $selection_entry=$state['business_reserve'][$item_id]??array();
                $rank=is_array($selection_entry)?absint($selection_entry['rank']??1):absint($selection_entry?:1);
                $quality=is_array($selection_entry)&&is_array($selection_entry['quality']??null)?$selection_entry['quality']:array();
                if($staging){
                    $stats['pending_deactivation']=absint($stats['pending_deactivation']??0)+1;
                }else{
                    $this->ebay_business_persist_quality_on_source_row($row,$quality,'reserve',$rank);
                    $this->ebay_business_pause_output_for_capacity($row,'reserve','Reserveprodukt – rückt automatisch nach, wenn ein aktiver Treffer entfällt.');
                    $stats['deactivated']=absint($stats['deactivated']??0)+1;
                }
            }else{
                $current=sanitize_key((string)($row['output_state']??''));
                if($staging){
                    $stats['pending_deactivation']=absint($stats['pending_deactivation']??0)+1;
                }else{
                    if($current==='creative_ready'||$current==='active_selected'||$current==='review_last_good'||(string)($row['creative_identity_hash']??'')!==''){
                        $this->ebay_business_pause_output_for_capacity($row,'candidate','Qualifizierter Kandidat außerhalb der aktiven Top-Auswahl.');
                        $stats['deactivated']=absint($stats['deactivated']??0)+1;
                    }elseif($current!=='candidate'){
                        $this->ebay_business_persist_quality_on_source_row($row,array(),'candidate',0);
                    }
                }
                $stats['candidate']=absint($stats['candidate']??0)+1;
            }
        }
        $state['stats']['business']=$stats;
        if(count($rows)<$limit){
            if(!$terminal_transition){
                $state['checkpoint_business_cleanup_done']=1;
            }else{
                $scope=sanitize_key((string)($state['selection_scope']??''));
                if($scope==='business'){
                    $state['phase']='complete';$state['status']='complete';$state['completed_at']=time();
                }elseif($scope==='all'){
                    $state['phase']='private_prune';
                }else{
                    $state['phase']='failed';$state['status']='failed';$state['failed_at']=time();
                    $state['failure_reason']='invalid_selection_scope_business_prune';
                }
            }
        }
        return count($rows);
    }
 private function ebay_business_persist_quality_on_source_row($row,$q,$state,$rank){return true;}
 private function ebay_business_pause_output_for_capacity($row,$state,$reason){
    $id=(int)($row['id']??0);
    if(isset($GLOBALS['wpdb']->outputs[$id]))$GLOBALS['wpdb']->outputs[$id]['status']='paused';
    return true;
 }

}
function get_post_meta($id,$key,$single=false){return hash('sha256',(string)$id);}
$scenario=$argv[2]??'normal';$p=new FullPipeline50($scenario);$log=$p->loop(40);
echo json_encode(['summary'=>['scenario'=>$scenario,'status'=>$p->run['status'],'last_phase'=>$p->run['phase'],
 'progress_seq'=>$p->run['progress_seq'],'worker_tickets'=>$p->run['transport_tick_count'],
 'candidate_count'=>count($p->run['checkpoint_candidate']['business_campaign_ids']),'public_count'=>count($p->cp['business_campaign_ids']),
 'new_searches'=>$p->newSearches, 'lost_old_ids'=>count(array_diff(range(1001,1578),(array)($p->cp['business_campaign_ids']??[]))),
 'new_ids'=>array_values(array_intersect([1579,1580],(array)($p->cp['business_campaign_ids']??[]))),
 'families_covered_in_run'=>$p->run['coverage']['covered']??null,'selection_calls'=>$p->selectionCalls,'public_writes'=>$p->writes, 'published_outputs'=>count(array_filter($GLOBALS['wpdb']->outputs,fn($r)=>$r['status']==='published')),
 'cleanup_logic'=>'Unmodified original ebay_selection_prune_business_batch copied verbatim from trait-ppar-ebay.php',
 'error'=>$p->run['error_code']??null], 'trace'=>$log],JSON_PRETTY_PRINT|JSON_UNESCAPED_UNICODE)."\n";
exit($p->run['status']==='completed'?0:1);