<?php
// Real plugin trait method, same deterministic row set against QA4/QA5.
error_reporting(E_ALL & ~E_DEPRECATED);
define('ABSPATH','/');define('ARRAY_A','ARRAY_A');
function absint($x){return abs((int)$x);} function sanitize_key($x){return strtolower(preg_replace('/[^a-z0-9_-]/','',strtolower((string)$x)));}
function sanitize_text_field($x){return trim((string)$x);}
$src=$argv[1];$test=$argv[2]??'gapfill';require $src;
class QA5DB {
 public $rows=[],$last_error='',$queries=0,$read_rows=0,$fail=false,$sqls=[];
 public function prepare($query,...$args){$i=0;return preg_replace_callback('/%[sd]/',function($m)use(&$i,$args){$v=$args[$i++];return $m[0]==='%d'?(string)((int)$v):"'".addslashes((string)$v)."'";},$query);}
 public function get_results($sql,$format){$this->queries++;$this->sqls[]=$sql;if($this->fail){$this->last_error='forced SQL failure';return null;}
  preg_match('/id>(\d+)/',$sql,$m);$cursor=(int)($m[1]??0);preg_match('/LIMIT (\d+)/',$sql,$l);$limit=(int)($l[1]??50);
  if(str_contains($sql,'1=0'))return [];
  $targets=null;if(preg_match('/rule_id IN \(([^)]+)\)/',$sql,$m)){$targets=array_map('stripslashes',array_map(fn($x)=>trim($x," '\""),explode(',',$m[1])));}
  $out=[];foreach($this->rows as $r){if($r['id']<=$cursor)continue;if($targets!==null && !in_array($r['rule_id'],$targets,true))continue;$out[]=$r;if(count($out)>=$limit)break;}
  $this->read_rows+=count($out);return $out;
 }
}
class QA5Plugin {use PPAR_Ebay_Trait; public $actions=[];
 private function ebay_items_table(){return 'wp_ebay_items';}
 private function ebay_business_persist_quality_on_source_row($row,$quality,$role,$rank){$this->actions[]=['quality',$row['id'],$role,$rank];return true;}
 private function ebay_business_pause_output_for_capacity($row,$reason,$message){$this->actions[]=['pause',$row['id'],$reason];return true;}
}
$wpdb=new QA5DB();$q=new QA5Plugin();$now=time();
for($i=1;$i<=2000;$i++){$concept=$i%100===0?'heunetze':($i%175===0?'sattel':'other');if($test==='gapfill_sparse_tail' && $i>1300){$concept='other';}$wpdb->rows[]=['id'=>$i,'item_id'=>'item'.$i,'rule_id'=>$concept,'source_state'=>'available','item_end_at'=>$now+9999,'output_state'=>($i%7===0?'creative_ready':'candidate'),'creative_identity_hash'=>($i%7===0?'hash':''),'seller_account_type'=>'BUSINESS'];}
$state=['phase'=>'business_prune','status'=>'running','selection_scope'=>'business','business_target_mode'=>(str_starts_with($test,'gapfill') || $test==='checkpoint_gapfill')?'gapfill':'full','business_target_concepts'=>$test==='gapfill_empty'?[]:($test==='gapfill_single'?['sattel']:['heunetze','sattel']),'business_prune_cursor'=>($test==='gapfill_resume'?1000:0),'business_active'=>['item100'=>['rank'=>1]],'business_reserve'=>['item200'=>['rank'=>2,'quality'=>['a'=>1]]],'stats'=>['business'=>['materialized'=>1]]];
if($test==='error'){$wpdb->fail=true;}
$checkpoint=in_array($test,['checkpoint','checkpoint_gapfill'],true);$steps=0;
$ref=new ReflectionMethod($q,'ebay_selection_prune_business_batch');
while(++$steps<100){$res=$ref->invokeArgs($q,[[],&$state,50,true,!$checkpoint]);if($test==='error' || ($checkpoint&&!empty($state['checkpoint_business_cleanup_done'])) || ($state['status']??'')==='complete' || ($state['status']??'')==='failed')break;}
if($steps>=100)throw new Exception('unbounded');
$output=['state'=>$state,'actions'=>$q->actions,'rows'=>count($wpdb->rows),'queries'=>$wpdb->queries,'read_rows'=>$wpdb->read_rows,'steps'=>$steps];
echo json_encode($output,JSON_UNESCAPED_UNICODE|JSON_INVALID_UTF8_SUBSTITUTE|JSON_PRETTY_PRINT);