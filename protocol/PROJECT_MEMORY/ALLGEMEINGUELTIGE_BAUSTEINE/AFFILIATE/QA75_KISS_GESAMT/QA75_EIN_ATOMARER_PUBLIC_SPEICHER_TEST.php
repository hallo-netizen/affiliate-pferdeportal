<?php
/** Same real unaltered PHP checkpoint saver, with an in-memory WordPress SQL-CAS adapter. */
error_reporting(E_ALL & ~E_DEPRECATED);
define('ABSPATH', __DIR__.'/');
function absint($v){return abs((int)$v);}
function sanitize_text_field($x){return trim(strip_tags((string)$x));}
function sanitize_key($x){return preg_replace('/[^a-z0-9_-]/','',strtolower((string)$x));}
function wp_json_encode($x,$flags=0){return json_encode($x,$flags);}
function maybe_serialize($x){return is_array($x) || is_object($x) ? serialize($x) : (string)$x;}
function get_option($k,$default=[]){return array_key_exists($k,$GLOBALS['options'])?$GLOBALS['options'][$k]:$default;}
function update_option($k,$v,$autoload=false){$GLOBALS['options'][$k]=$v;return true;}
function add_option($k,$v,$deprecated='',$autoload=false){if(array_key_exists($k,$GLOBALS['options']))return false;$GLOBALS['options'][$k]=$v;return true;}
function wp_cache_delete($k,$group=''){return true;}
class WPDataCAS {
 public $options='wp_options', $replace_during_write=null, $queries=0;
 public function prepare($sql,...$args){return ['sql'=>$sql,'args'=>$args];}
 public function query($prepared){
  $this->queries++;
  [$value,$key,$expected]=$prepared['args'];
  if(is_array($this->replace_during_write)){
   $GLOBALS['options'][$key]=$this->replace_during_write;
   $this->replace_during_write=null;
  }
  if(!array_key_exists($key,$GLOBALS['options'])||maybe_serialize($GLOBALS['options'][$key])!==$expected)return 0;
  $GLOBALS['options'][$key]=unserialize($value,['allowed_classes'=>false]);
  return 1;
 }
}
$GLOBALS['options']=[];$GLOBALS['wpdb']=new WPDataCAS();
require $argv[1];
class PublicCASProof {
 use PPAR_Ebay_Run_Trait;
 public $audit_count=0;
 private function ebay_audit_record_durable_change($after,$before=[],$kind='',$details=[]){$this->audit_count++;}
}
$r=new PublicCASProof();$method=new ReflectionMethod($r,'ebay_public_checkpoint_save');
$base=['schema'=>'1.0','status'=>'safe','checkpoint_id'=>'base-safe','source'=>'canonical_public_verify','run_uuid'=>'old-run','business_campaign_ids'=>[1,2],'private_listing_ids'=>[]];
$key='ppar_ebay_public_checkpoint_v1';$GLOBALS['options'][$key]=$base;
$new=$base;$new['checkpoint_id']='new-safe';$new['run_uuid']='new-run';$new['business_campaign_ids']=[4,3,3,2];
$stored=$method->invoke($r,$new,$base);
$success=is_array($stored)&&$stored['checkpoint_id']==='new-safe'&&$stored['business_campaign_ids']===[2,3,4]&&$r->audit_count===1;
$current=$GLOBALS['options'][$key];
$parallel=$base;$parallel['checkpoint_id']='parallel-safe';$parallel['run_uuid']='independent-run';$parallel['business_campaign_ids']=[8,9];
$GLOBALS['wpdb']->replace_during_write=$parallel;
$stale=$new;$stale['checkpoint_id']='stale-should-not-win';$stale['business_campaign_ids']=[12];
$race=$method->invoke($r,$stale,$current);
$race_blocked=$race===false && ($GLOBALS['options'][$key]['checkpoint_id']??'')==='parallel-safe'&&$r->audit_count===1;
$wrong_before=$method->invoke($r,$stale,$base);
$no_override=$wrong_before===false &&($GLOBALS['options'][$key]['checkpoint_id']??'')==='parallel-safe'&&$r->audit_count===1;
$out=['actual_original_saver_invoked'=>true,'normal_approved_commit'=>$success,'concurrent_updated_shelf_retained'=>$race_blocked,'stale_snapshot_rejected'=>$no_override,'final_checkpoint_id'=>$GLOBALS['options'][$key]['checkpoint_id'],'db_sql_update_count'=>$GLOBALS['wpdb']->queries,'audit_changes'=>$r->audit_count,'pass'=>$success&&$race_blocked&&$no_override];
echo json_encode($out,JSON_PRETTY_PRINT|JSON_UNESCAPED_UNICODE),"\n";
if(!$out['pass'])exit(1);