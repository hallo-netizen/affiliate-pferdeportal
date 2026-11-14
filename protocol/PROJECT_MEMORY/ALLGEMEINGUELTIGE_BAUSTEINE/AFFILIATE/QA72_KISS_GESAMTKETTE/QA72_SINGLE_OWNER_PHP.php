<?php
error_reporting(E_ALL & ~E_DEPRECATED);
if ($argc !== 2) {fwrite(STDERR,"Need source trait path\n");exit(2);}
define('ABSPATH',__DIR__);define('ARRAY_A','ARRAY_A');define('HOUR_IN_SECONDS',3600);
function sanitize_key($x){return preg_replace('/[^a-z0-9_\-]/','',strtolower((string)$x));}
function sanitize_text_field($x){return trim((string)$x);}
function absint($x){return abs((int)$x);}
function wp_json_encode($x,$flags=0){return json_encode($x,$flags);}
function is_wp_error($x){return $x instanceof WP_Error;}
function get_option($k,$v=[]){return $GLOBALS['testopts'][$k]??$v;}
function update_option($k,$v,$autoload=false){$GLOBALS['testopts'][$k]=$v;return true;}
class WP_Error {private $code;private $msg;function __construct($c,$m){$this->code=$c;$this->msg=$m;}function get_error_code(){return $this->code;}function get_error_message(){return $this->msg;}}
require $argv[1];
class MockWPDB {
  public $row=[];public $last_error='';public $updates=[];
  function prepare($sql,...$args){return $sql;}
  function get_row($sql,$fmt){return $this->row;}
  function update($table,$data,$where,...$rest){$this->updates[]=$data;foreach($data as $k=>$v){$this->row[$k]=$v;}return 1;}
}
class Probe {use PPAR_Ebay_Trait;
 public const EBAY_CONTENT_POLICY_VERSION='policy-test';public const EBAY_BUSINESS_CLASSIFIER_VERSION='classifier-test';
 public $quality_calls=0,$classify_calls=0,$quality_by_id=[],$source_rows=[],$block_ids=[];
 public function ebay_normalize_settings($settings,$preserve_secret=true){return $settings;}
 function eligible($r){return $this->ebay_business_source_row_is_public_fresh($r);}
 function plan($c,$s){return $this->ebay_business_selection_plan_concept($c,$s);}
 function attach($r,$i,$c,$q,$s){return $this->ebay_business_add_verified_secondary($r,$i,$c,$q,$s);}
 function store($i,$r){return $this->ebay_upsert_item($i,$r,"business_affiliate",0,[]);}
 private function ebay_business_selection_concept_rows($id,$settings=null){return $this->source_rows;}
 private function ebay_business_verified_source_claims($row){$p=json_decode($row['source_payload']??'{}',true);$claims=[]; if(isset($p['portal_classification']))$claims[$row['rule_id']]=['classification'=>$p['portal_classification'],'quality'=>[]];foreach($p['business_verified_concepts']??[] as $id=>$v)$claims[$id]=$v;return $claims;}
 private function ebay_business_source_row_item($row,$settings){$item=(array)(json_decode($row['source_payload']??'{}',true)['raw']??[]);$item['item_id']=$row['item_id'];return $item;}
 private function ebay_rule_by_id($id,$settings){return ['id'=>$id];}
 private function ebay_business_quality_assess($item,$cls,$rule,$settings,$median=0.0){$this->quality_calls++;$this->quality_by_id[$item['item_id']]=($this->quality_by_id[$item['item_id']]??0)+1;if(in_array($item['item_id'],$this->block_ids,true))return new WP_Error('veto','blocked');$relevance=80;$offer=70;$price=$this->ebay_business_price_plausibility_score($item['price_value'],$median);$overall=max(0,min(100,(int)round($relevance*.7+$offer*.2+$price*.1)));return ['overall'=>$overall,'relevance'=>$relevance,'offer'=>$offer,'price'=>$price,'brand_bonus'=>0,'pinned'=>false,'brand_preferred'=>false,'seller_username'=>'S'.$item['item_id'],'seller_feedback_percentage'=>90,'seller_feedback_score'=>5];}
 private function ebay_business_item_with_quality($i,$q){$i['business_quality']=$q;return $i;}
 private function ebay_business_classify_portal_item_strict($item,$rule){$this->classify_calls++;return ['product_concept_id'=>$rule['id'],'business_match_contract'=>'concept_v3','score'=>90,'evidence_hash'=>str_repeat('b',64)];}
 private function ebay_accept_item($raw,$type,$settings){return $raw;}
 private function ebay_workflow_evidence_sections($item){return ['text'=>(string)($item['evidence']??'')];}
 private function ebay_topic_text($s){return strtolower(trim((string)$s));}
 private function ebay_items_table(){return 'ebay_items';}
}
$concept='sattel';$mkClass=fn($id)=>['product_concept_id'=>$id,'business_match_contract'=>'concept_v3','score'=>90,'evidence_hash'=>str_repeat('b',64)];
$probe=new Probe();foreach(['a'=>20,'b'=>100,'c'=>40,'x'=>500,'v'=>30] as $id=>$price){$p=['portal_classification'=>$mkClass($concept),'raw'=>['title'=>'product-'.$id,'price_value'=>$price,'seller_username'=>'S-'.$id,'item_id'=>$id]];$probe->source_rows[]=['id'=>ord($id),'item_id'=>$id,'rule_id'=>$concept,'source_state'=>'available','policy_state'=>'allowed','route_state'=>'ready','fresh_until'=>time()+9999,'item_end_at'=>time()+10000,'source_payload'=>json_encode($p)];}
$probe->block_ids=['v'];$out=$probe->plan($concept,['business_candidate_pool_per_concept'=>10,'business_reserve_per_concept'=>2]);
$selected=array_keys($out['active']);$reserves=array_keys($out['reserve']);
$other=new Probe();$other->source_rows=[['id'=>100,'item_id'=>'secondary','rule_id'=>'primary','source_state'=>'available','policy_state'=>'allowed','route_state'=>'ready','fresh_until'=>time()+9000,'item_end_at'=>time()+9900,'source_payload'=>json_encode(['portal_classification'=>$mkClass('primary'),'business_verified_concepts'=>['extra'=>['classification'=>$mkClass('extra'),'quality'=>[]]],'raw'=>['title'=>'extra product','price_value'=>99,'item_id'=>'secondary']])]];
$s=$other->plan('extra',['business_candidate_pool_per_concept'=>10,'business_reserve_per_concept'=>2]);
$wpdb=new MockWPDB();$GLOBALS['wpdb']=$wpdb;$stored=['id'=>1,'item_id'=>'secondary','rule_id'=>'primary','title'=>'extra product','seller_account_type'=>'BUSINESS','seller_username'=>'seller','source_state'=>'available','policy_state'=>'allowed','route_state'=>'ready','fresh_until'=>time()+9999,'source_payload'=>json_encode(['raw'=>['title'=>'extra product','evidence'=>'same source','item_id'=>'secondary'],'portal_classification'=>$mkClass('primary')]),'classifier_version'=>'classifier-test','policy_version'=>'policy-test'];$wpdb->row=$stored;
 $attachment=new Probe();$debug=['fresh'=>$attachment->eligible($stored),'seller'=>strtoupper(sanitize_key($stored['seller_account_type'])),'itemid'=>sanitize_text_field($stored['item_id']),'policy'=>sanitize_key($stored['policy_state']),'route'=>sanitize_key($stored['route_state'])];$good=$attachment->attach($stored,['title'=>'extra product','evidence'=>'same source','item_id'=>'secondary','seller_username'=>'seller'],$mkClass('extra'),[],[]);
$good_writes=count($wpdb->updates);$bad=$attachment->attach($stored,['title'=>'extra product','evidence'=>'changed text','item_id'=>'secondary','seller_username'=>'seller'],$mkClass('extra'),[],[]);
$saveDB=new MockWPDB();$GLOBALS['wpdb']=$saveDB;
$existing=$stored;
$existing['source_hash']=str_repeat('a',64);
$existing['output_state']='creative_ready';
$existing['source_payload']=json_encode(['raw'=>['title'=>'extra product','evidence'=>'same source','item_id'=>'secondary'],'portal_classification'=>$mkClass('primary'),'business_verified_concepts'=>['extra'=>['classification'=>$mkClass('extra'),'quality'=>['overall'=>80]]],'business_selection'=>['selected_concepts'=>['primary','extra']]]);
$saveDB->row=$existing;
$raw=['item_id'=>'secondary','legacy_item_id'=>'','seller_account_type'=>'BUSINESS','seller_username'=>'seller','title'=>'extra product','short_description'=>'same source','condition_text'=>'good','price_value'=>'100','currency'=>'EUR','shipping_value'=>'0','location_text'=>'','affiliate_url'=>'https://example.invalid/affiliate','item_web_url'=>'https://example.invalid/item','image_url'=>'https://example.invalid/image','item_end_at'=>time()+9999,'source_hash'=>str_repeat('a',64),'raw'=>['evidence'=>'same source'],'portal_classification'=>$mkClass('primary'),'business_quality'=>['overall'=>80],'business_selection'=>[]];
$saveProbe=new Probe();$saveResult=$saveProbe->store($raw,['id'=>'primary']);
$sameUpsClassify=$saveProbe->classify_calls;$sameUpsQuality=$saveProbe->quality_calls;
$extrasSame=json_decode($saveDB->row['source_payload'],true)['business_verified_concepts']??[];
$raw['source_hash']=str_repeat('c',64);
$saveProbe->store($raw,['id'=>'primary']);
$changedUpsClassify=$saveProbe->classify_calls-$sameUpsClassify;
$report=['upsert_same_classify_calls'=>$sameUpsClassify,'upsert_same_quality_calls'=>$sameUpsQuality,'upsert_unchanged_extra_preserved'=>isset($extrasSame['extra']),'upsert_changed_classify_calls'=>$changedUpsClassify,'debug'=>$debug,'quality_calls'=>$probe->quality_calls,'quality_by_id'=>$probe->quality_by_id,'primary_plan_active'=>$selected,'primary_plan_reserve'=>$reserves,'primary_plan_pool'=>$out['pool'],'secondary_planning_classify_calls'=>$other->classify_calls,'secondary_plan_active'=>array_keys($s['active']),'secondary_attach_classify_calls'=>$attachment->classify_calls,'secondary_same_source_success'=>!is_wp_error($good),'same_source_error'=>is_wp_error($good)?$good->get_error_code():null,'secondary_different_source_rejected'=>is_wp_error($bad),'secondary_different_source_code'=>is_wp_error($bad)?$bad->get_error_code():null,'writes_after_good'=>$good_writes,'total_writes'=>count($wpdb->updates)];echo json_encode($report,JSON_UNESCAPED_UNICODE|JSON_PRETTY_PRINT)."\n";