<?php
if(!function_exists("wp_json_encode")){function wp_json_encode($x,$flags=0){return json_encode($x,$flags);}}
/** Reproducible isolated integration test with the real 187 IDs from exported 2026-11-09 run.
 * Uses actual selector state transition from staged plugin, mock storage/provider interactions.
 * No WordPress DB, API or live site touched. */
error_reporting(E_ALL);
define('ABSPATH', '/');
function absint($x) { return abs((int)$x); }
function sanitize_key($x) { return strtolower(preg_replace('/[^a-z0-9_-]/','',strtolower((string)$x))); }
function sanitize_text_field($x) { return trim((string)$x); }
function is_wp_error($x) { return $x instanceof WP_Error; }
class WP_Error { private $code;private $msg; public function __construct($c,$m){$this->code=$c;$this->msg=$m;} public function get_error_code(){return $this->code;} public function get_error_message(){return $this->msg;} }
$path='/mnt/data/Pferdeatelier_eBay_fehlende_Produktfamilien_3e9e9207-d82.csv';
$f=fopen($path,'r');if(!$f)throw new RuntimeException('Missing exported dataset');
$header=fgetcsv($f,0,';', '"', '');$ids=[];
while(($row=fgetcsv($f,0,';', '"', ''))!==false){$id=sanitize_key((string)($row[2]??''));if($id!=='')$ids[]=$id;}
fclose($f);
if(count($ids)!==138 || count(array_unique($ids))!==138){throw new RuntimeException('Not the 138 unique families export');}
require '/mnt/data/qa15_integrated/affiliate-portal-router/includes/trait-ppar-ebay.php';
class EBay138Test{
 use PPAR_Ebay_Trait;
 public array $targets=[],$counts=[],$qualified=[],$plans=[];public string $errorPlan='',$errorRead='',$preselected='';
 public int $apiCalls=0,$published=0,$reuseCalls=0;
 private function ebay_selection_business_target_concepts($state){return $this->targets;}
 private function ebay_business_selection_plan_concept($id,$settings){
  $this->plans[$id]=($this->plans[$id]??0)+1;
  if($id===$this->errorPlan) return new WP_Error('plan_failed','Family-specific selection failure');
  $eligible=($id===$this->preselected || !empty($this->qualified[$id]));
  return ['active'=>$eligible?['offer-'.$id=>['concept'=>$id,'rank'=>1,'concepts'=>[$id=>['rank'=>1]]]]:[],'reserve'=>[]];
 }
 private function ebay_business_reuse_stored_for_concept($id,$settings){
  $this->counts[$id]=($this->counts[$id]??0)+1;$this->reuseCalls++;
  if($id===$this->errorRead)return new WP_Error('stored_db_read_failed','One family cannot read its stored offers');
  if(array_key_exists($id,$this->qualified)){$this->qualified[$id]=true;return ['attached'=>1];}
  return ['attached'=>0];
 }
 private function ebay_business_merge_selection_entry($a,$b){return array_merge($a,['concept'=>$b['concept'],'rank'=>1,'concepts'=>array_merge((array)($a['concepts']??[]),(array)$b['concepts'])]);}
 private function ebay_business_selection_apply_global_cap($entries,$settings){return $entries;}
 private function ebay_business_selection_coverage($data){return ['required'=>298,'covered'=>count($data['active'])];}
 public function tick(&$state,$batch=4){return $this->ebay_selection_reuse_checkpoint_batch([],$state,$batch);}
}
function assert_ok($cond,$msg){if(!$cond){fwrite(STDERR,"FAIL: $msg\n");exit(1);}echo "PASS $msg\n";}
$c=new EBay138Test();$c->targets=$ids;$c->errorRead=$ids[10];$c->errorPlan=$ids[25];$c->preselected=$ids[30];
$c->qualified=[$ids[11]=>false,$ids[60]=>false,$ids[count($ids)-1]=>false];
$state=['status'=>'running','phase'=>'business_prune','reason'=>'canonical_gapfill','business_target_concepts'=>$ids,'business_active'=>['offer-existing'=>['concept'=>'already-covered','rank'=>1,'concepts'=>['already-covered'=>[]]]], 'business_prune_cursor'=>42,'stats'=>['business'=>['materialized'=>1]]];
$ticks=0;while(empty($state['business_reuse_done']) && $ticks++<100){$c->tick($state,4);}
assert_ok($ticks===35,'138 source families progress in exactly 35 bounded batches');
assert_ok(($state['business_reuse_cursor']??-1)===138,'All 138 families reached exactly once');
assert_ok(($state['business_reuse_errors']??0)===2,'Two individual faults isolated instead of blocking the run');
assert_ok(($state['business_soft_failed']['reuse:'.$ids[10]]['code']??'')==='stored_db_read_failed','Specific storage failure recorded');
assert_ok(($state['business_soft_failed']['reuse:'.$ids[25]]['code']??'')==='plan_failed','Specific selection failure recorded');
assert_ok(($state['business_reuse_changes']??0)===4,'Three new verified entries plus one already preselected family included');
assert_ok($state['phase']==='business_materialize','New results handed to the original materializer');
assert_ok($state['business_prune_cursor']===0,'Original publish/prune cursor restarts only after new verified results');
assert_ok(isset($state['business_active']['offer-existing']),'Old published selection not discarded');
assert_ok(isset($state['business_active']['offer-'.$ids[11]]) && isset($state['business_active']['offer-'.$ids[60]]) && isset($state['business_active']['offer-'.$ids[count($ids)-1]]),'All newly qualified families retained');
assert_ok(count($c->counts)===136 && max($c->counts)===1 && min($c->counts)===1,'No duplicate stored-source lookups, with plan-error and preselected excluded');
assert_ok($c->apiCalls===0 && $c->published===0,'No eBay API or secondary publisher invoked');
assert_ok(($state['stats']['business_previous_apply']['materialized']??0)===1,'Old published statistics retained');
echo "DATASET_RUN=".count($ids)." FAMILIES; BATCHES={$ticks}; LOCAL_CHECKS={$c->reuseCalls}\n";