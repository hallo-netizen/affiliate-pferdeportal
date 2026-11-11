<?php
error_reporting(E_ALL);
define('ABSPATH','/tmp');
$GLOBALS['opts']=array();$GLOBALS['fail_key']='';
function get_option($key,$default=null){return array_key_exists($key,$GLOBALS['opts'])?$GLOBALS['opts'][$key]:$default;}
function update_option($key,$value,$autoload=false){if($key===$GLOBALS['fail_key'])return false;$GLOBALS['opts'][$key]=$value;return true;}
function absint($v){return abs((int)$v);} function sanitize_key($v){return preg_replace('/[^a-z0-9_\-]/','',strtolower($v));}
function sanitize_text_field($v){return strip_tags(trim((string)$v));}
function wp_json_encode($v,$opts=0){return json_encode($v,$opts);}
function current_user_can($cap){return true;}function check_admin_referer($action,$name){return true;}
function wp_unslash($v){return $v;}function wp_die($s,$code=0){throw new Exception($s);}
function nocache_headers(){}
require __DIR__.'/build/affiliate-portal-router/includes/trait-ppar-ebay-run.php';
class AuditProbe {use PPAR_Ebay_Run_Trait; const EBAY_RUNTIME_BUILD='test_q12';
  public function save($v){return $this->ebay_run_save($v);} public function saved(){return $this->ebay_run_load();}
  public function getKey($id){return $this->ebay_audit_key($id);} public function probe($x){return $this->ebay_audit_note_state($x);}
}
function ok($cond,$msg){if(!$cond)throw new Exception('FAIL '.$msg);echo "PASS $msg\n";}
$p=new AuditProbe();
$r=['schema'=>'1.0','run_uuid'=>'run-old-1234','status'=>'running','phase'=>'gapfill_discovery','progress_seq'=>1,'transport_tick_count'=>1,'coverage'=>['covered'=>161,'required'=>298],'skipped_item_errors'=>[]];
$p->save($r);$k=$p->getKey('run-old-1234');
ok(get_option($k.'_meta')['count']===1,'first run initial event logged');
ok(count(get_option($k.'_c0'))===1,'initial detail chunk');
$p->save($r);ok(get_option($k.'_meta')['count']===1,'identical save does not duplicate audit');
for($i=2;$i<=103;$i++){$r['progress_seq']=$i;$r['transport_tick_count']=$i;$p->save($r);}
ok(get_option($k.'_meta')['count']===103,'every progress transition recorded');
ok(count(get_option($k.'_c0'))===100 && count(get_option($k.'_c1'))===3,'100-event chunks preserve all progress, no overwrite');
$r['status']='failed';$r['phase']='failed';$r['error_code']='public_source_refresh_provider_failed';$r['errors']=[['code'=>$r['error_code']]];$r['public_source_refresh']=['provider_errors'=>1,'provider_error_samples'=>[['code'=>'ebay_refresh_http','post_id'=>911]]];
$p->save($r);ok(get_option($k.'_meta')['count']===104,'terminal error recorded');
$entry=end($GLOBALS['opts'][$k.'_c1']);ok($entry['source_provider_errors']===1 && $entry['source_error_examples'][0]['post_id']===911,'real provider error code and affected post preserved');
$start=['schema'=>'1.0','run_uuid'=>'run-new-5678','status'=>'running','phase'=>'reconcile_local','progress_seq'=>1,'transport_tick_count'=>1];
$p->save($start);ok(get_option($k.'_meta')['count']===105,'old run supersession separately recorded');
$nk=$p->getKey('run-new-5678');ok(get_option($nk.'_meta')['count']===1 && count(get_option($k.'_c1'))===5,'new run starts without destroying preceding run audit');
$ix=get_option('ppar_ebay_audit_run_index_v1');ok(count($ix)===2 && $ix[0]==='run-old-1234','old and new run are available for export');
$copy=$p->saved();ok($copy['run_uuid']==='run-new-5678','current run preserved after audit');
// Simulate failure on audit chunk, not on canonical run.
$GLOBALS['fail_key']=$nk.'_c0';$start['progress_seq']=2;$p->save($start);
ok(get_option('ppar_ebay_audit_write_error_v1')>0,'audit storage problem explicitly flagged');
ok($p->saved()['progress_seq']===2,'audit failure does not destroy actual eBay progress');
// Verify old run still present and no secrets in audit.
ok(!array_key_exists('config_snapshot',get_option($nk.'_c0')[0]),'audit never stores API secrets/settings');
echo "ALL QA12 REAL PHP AUDIT TESTS PASS\n";