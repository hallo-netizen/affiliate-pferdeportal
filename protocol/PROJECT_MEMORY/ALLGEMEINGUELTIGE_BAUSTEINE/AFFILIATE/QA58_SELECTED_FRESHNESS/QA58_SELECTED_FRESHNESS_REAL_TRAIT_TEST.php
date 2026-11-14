<?php
// QA58: call the actual packed eBay BUSINESS materialiser and actual 343/344
// availability-only updater; fake only WP DB/OAuth/eBay network/output IO.
error_reporting(E_ALL & ~E_DEPRECATED);
define('ABSPATH',__DIR__.'/'); define('ARRAY_A','ARRAY_A'); define('HOUR_IN_SECONDS',3600);define('MINUTE_IN_SECONDS',60);
function sanitize_key($v){return preg_replace('/[^a-z0-9_-]/','',strtolower((string)$v));}
function sanitize_text_field($v){return trim(strip_tags((string)$v));}
function absint($v){return abs((int)$v);}
function is_wp_error($v){return $v instanceof WP_Error;}
class WP_Error extends Exception { private $codeId;function __construct($code,$message=''){parent::__construct($message?:$code);$this->codeId=$code;}function get_error_code(){return $this->codeId;}function get_error_message(){return $this->getMessage();} }
class Store58 {
 public $rows=[],$last_error='',$brokenRead=false,$brokenWrite=false,$writes=0;
 function prepare($sql,...$args){return ['sql'=>$sql,'args'=>$args];}
 function get_results($q,$format=null){ $this->last_error='';$args=$q['args'];$cursor=(int)$args[0];$limit=(int)end($args);$ids=array_slice($args,1,-1);$rows=array_values(array_filter($this->rows,fn($r)=>$r['id']>$cursor && in_array($r['item_id'],$ids,true)));usort($rows,fn($a,$b)=>$a['id']<=>$b['id']);return array_slice($rows,0,$limit);}
 function get_row($q,$format=null){$this->last_error=$this->brokenRead?'blocked-storage':'';if($this->brokenRead)return null;$id=(int)($q['args'][0]??0);return $this->rows[$id]??null;}
 function update($table,$data,$where,$fmt=null,$wfmt=null){if($this->brokenWrite){$this->last_error='blocked-storage';return false;}$id=(int)$where['id'];if(!isset($this->rows[$id]))return 0;foreach($where as $k=>$v){if((string)($this->rows[$id][$k]??'')!==(string)$v)return 0;}$this->rows[$id]=array_merge($this->rows[$id],$data);$this->writes++;return 1;}
}
$GLOBALS['wpdb']=new Store58();
require $argv[1];
class ActualMaterialize58 {
 use PPAR_Ebay_Trait;
 public $modes=[],$fetches=0,$published=[],$purged=[],$claims=[],$sourceConversions=0,$oauths=0;
 private function ebay_items_table(){return 'ebay_items';}
 private function ebay_db_formats($r){return [];}
 private function ebay_access_token($settings,$force=false,$respect_channel_pause=true){$this->oauths++;return 'token';}
 private function ebay_fetch_item_for_refresh($row,$settings,$token){$this->fetches++;$id=(int)$row['id'];$mode=$this->modes[$id]??'same';if($mode==='transient_once' && $this->fetches===1)return new WP_Error('ebay_refresh_transport');if($mode==='transient')return new WP_Error('ebay_refresh_transport');if($mode==='ended')return ['state'=>'ended'];return ['state'=>'active','raw'=>['mode'=>$mode,'id'=>$id]];}
 private function ebay_accept_item($raw,$seller,$settings){$r=$GLOBALS['wpdb']->rows[$raw['id']];if($raw['mode']==='changed')$r['title']='Totally different; not the same product';$r['price_value']='31.25';return $r;}
 private function ebay_topic_text($s){return strtolower(trim($s));}
 private function ebay_purge_item_content($row,$status,$reason){$this->purged[]=$row['item_id'];return true;}
 private function ebay_business_source_row_item($row,$settings){$this->sourceConversions++;return ['item_id'=>$row['item_id'],'portal_classification'=>['product_concept_id'=>$row['rule_id']]];}
 private function ebay_rule_by_id($id,$settings=[]){return ['id'=>$id];}
 private function ebay_business_verified_source_claims($row){return [$row['rule_id']=>['classification'=>['product_concept_id'=>$row['rule_id']],'quality'=>[]]];}
 private function ebay_business_quality_assess($item,$classification,$rule,$settings,$w){return ['score'=>90];}
 private function ebay_business_item_with_quality($item,$quality){return $item;}
 private function ebay_route_business($row,$item,$rule,$origin,$classification){$this->published[]=$row['item_id'];return ['status'=>'success'];}
 private function ebay_business_commit_selected_source_role($row,$quality,$role,$rank,$concepts){return ['status'=>'success'];}
 private function ebay_business_selection_coverage($plan){return ['required'=>2,'covered'=>count((array)($plan['active']??[])),'missing_concepts'=>[]];}
 public function apply(&$state){return $this->ebay_selection_apply_business_batch(['enabled'=>1],$state,50);}
}
function source58($id,$expired=true,$policy='allowed'){$now=time();return ['id'=>$id,'item_id'=>'item'.$id,'seller_account_type'=>'BUSINESS','seller_username'=>'seller','title'=>'Sattel '.$id,'image_url'=>'https://images.example.org/item'.$id.'.jpg','condition_text'=>'NEW','source_state'=>'available','policy_state'=>$policy,'route_state'=>'ready','output_state'=>'none','creative_identity_hash'=>'hash'.$id,'rule_id'=>'family'.$id,'source_checked_at'=>$now-26000,'fresh_until'=>$expired?$now-100:$now+4000,'item_end_at'=>0,'price_value'=>'20.00','currency'=>'EUR','source_payload'=>'{}'];}
function state58($ids){$active=[];foreach($ids as $id)$active['item'.$id]=['concept'=>'family'.$id,'quality'=>['score'=>90],'rank'=>1];return ['phase'=>'business_materialize','status'=>'running','business_cursor'=>0,'business_active'=>$active,'stats'=>['business'=>[]],'plan_stats'=>['business'=>[]]];}
function scenario58($tag,$rows,$modes=[],$storage=false){$GLOBALS['wpdb']=new Store58();foreach($rows as $r)$GLOBALS['wpdb']->rows[$r['id']]=$r;$GLOBALS['wpdb']->brokenRead=$storage;$o=new ActualMaterialize58();$o->modes=$modes;$state=state58(array_column($rows,'id'));$runs=[];for($i=0;$i<5;$i++){$o->apply($state);$runs[]=['cursor'=>$state['business_cursor'],'phase'=>$state['phase'],'materialized'=>$state['stats']['business']['materialized']??0,'soft_fail'=>$state['stats']['business']['recoverable_failed']??0];if($state['phase']!=='business_materialize')break;}return ['name'=>$tag,'runs'=>$runs,'fetches'=>$o->fetches,'published'=>$o->published,'purged'=>$o->purged,'errors'=>$state['stats']['business']['errors']??[],'retry'=>$state['business_freshness_retry']??[],'status'=>$state['status']];}
$tests=[];
$tests['stale_two_selected_one_network_per_tick']=scenario58('stale_two',[source58(1),source58(2)]);
$tests['fresh_no_network']=scenario58('fresh',[source58(1,false)]);
$tests['changed_identity_not_published']=scenario58('changed',[source58(1)], [1=>'changed']);
$tests['ended_not_published']=scenario58('ended',[source58(1)], [1=>'ended']);
$tests['transport_one_retry']=scenario58('transient_once',[source58(1)], [1=>'transient_once']);
$tests['transport_two_strikes_no_publish']=scenario58('transient',[source58(1)], [1=>'transient']);
$tests['storage_error_blocks_publication']=scenario58('storage',[source58(1)], [],true);
$tests['policy_block_is_not_refreshed']=scenario58('policy',[source58(1,true,'blocked')]);
// 153 rejected as stale in the real CSV: prove the same 153 logical winners
// are not silently discarded if their source can be revalidated one per tick.
$GLOBALS['wpdb']=new Store58();$bulk=new ActualMaterialize58();$bulkState=state58(range(1,153));
foreach(range(1,153) as $i){$GLOBALS['wpdb']->rows[$i]=source58($i);}
$bulkTicks=0;
while($bulkState['phase']==='business_materialize' && $bulkTicks<160){$bulk->apply($bulkState);$bulkTicks++;}
$tests['153_stale_resumed_bounded']=array('fetches'=>$bulk->fetches,'materialized'=>absint($bulkState['stats']['business']['materialized']??0),'published_count'=>count($bulk->published),'ticks'=>$bulkTicks,'phase'=>$bulkState['phase']);
$expect=[
 'stale_two_selected_one_network_per_tick'=>fn($r)=>$r['fetches']===2 && count($r['published'])===2 && $r['runs'][0]['cursor']===1 && $r['runs'][0]['phase']==='business_materialize' && $r['runs'][1]['phase']==='business_prune',
 'fresh_no_network'=>fn($r)=>$r['fetches']===0&&count($r['published'])===1,
 'changed_identity_not_published'=>fn($r)=>$r['fetches']===1&&count($r['published'])===0,
 'ended_not_published'=>fn($r)=>$r['fetches']===1&&count($r['published'])===0&&count($r['purged'])===1,
 'transport_one_retry'=>fn($r)=>$r['fetches']===2&&count($r['published'])===1&&$r['runs'][0]['cursor']===0,
 'transport_two_strikes_no_publish'=>fn($r)=>$r['fetches']===2&&count($r['published'])===0&&$r['runs'][1]['phase']==='business_prune',
 'storage_error_blocks_publication'=>fn($r)=>$r['fetches']===1&&count($r['published'])===0&&$r['status']==='failed',
 'policy_block_is_not_refreshed'=>fn($r)=>$r['fetches']===0&&count($r['published'])===0,
 '153_stale_resumed_bounded'=>fn($r)=>$r['fetches']===153&&$r['materialized']===153&&$r['published_count']===153&&$r['ticks']===153&&$r['phase']==='business_prune',
];
$pass=0;$total=count($tests);foreach($tests as $tag=>$r){$ok=$expect[$tag]($r);printf("%s %s %s\n",$ok?'PASS':'FAIL',$tag,json_encode($r,JSON_UNESCAPED_UNICODE));$pass+=(int)$ok;}printf("TOTAL %d/%d\n",$pass,$total);if($pass!==$total)exit(1);