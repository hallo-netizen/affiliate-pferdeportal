<?php
error_reporting(E_ALL & ~E_DEPRECATED); define('ABSPATH','/tmp');
$GLOBALS['opts']=[];$GLOBALS['fail_key']='';$GLOBALS['fail_remaining']=0;
function get_option($k,$d=null){return array_key_exists($k,$GLOBALS['opts'])?$GLOBALS['opts'][$k]:$d;}
function update_option($k,$v,$autoload=false){if($k===$GLOBALS['fail_key']&&$GLOBALS['fail_remaining']!==0){if($GLOBALS['fail_remaining']>0)$GLOBALS['fail_remaining']--;return false;}$old=$GLOBALS['opts'][$k]??null;$GLOBALS['opts'][$k]=$v;return serialize($old)!==serialize($v);}
function absint($v){return abs((int)$v);} function sanitize_key($v){return preg_replace('/[^a-z0-9_\-]/','',strtolower((string)$v));}
function sanitize_text_field($v){return trim(strip_tags((string)$v));} function wp_json_encode($v,$f=0){return json_encode($v,$f);}
require __DIR__.'/affiliate-portal-router/includes/trait-ppar-ebay-run.php';
class AuditMatrix {use PPAR_Ebay_Run_Trait; const EBAY_RUNTIME_BUILD='test-qa15';public function save($a){return $this->ebay_run_save($a);} public function saved(){return $this->ebay_run_load();}public function key($a){return $this->ebay_audit_key($a);} }
function check($c,$label){if(!$c)throw new Exception('FAIL '.$label);echo 'PASS '.$label."\n";}
function fault($key,$n){$GLOBALS['fail_key']=$key;$GLOBALS['fail_remaining']=$n;}function clear_fault(){fault('',0);}
$w=new AuditMatrix();$r=['schema'=>'1.0','run_uuid'=>'fault-injection-run','status'=>'running','phase'=>'reconcile_local','progress_seq'=>1,'transport_tick_count'=>1];
check(is_array($w->save($r)),'initial complete run state stored');$key=$w->key($r['run_uuid']);check(get_option($key.'_meta')['count']===1,'initial audit metadata stored');
// Simulated WP update_option returns false when value unchanged. It must not be counted as failure.
check(is_array($w->save($w->saved())),'identical WP option update is still a verified success');
$r['progress_seq']=2; fault($key.'_c0',1);check(is_array($w->save($r)),'one transient audit CHUNK failure never aborts verified run');
check(get_option($key.'_meta')['count']===2,'one retry repairs transient audit CHUNK failure in same canonical save');check(empty(get_option('ppar_ebay_audit_write_error_v1',0)),'fully recovered one-off failure does not produce false warning');clear_fault();
$r['progress_seq']=3;fault($key.'_meta',1);check(is_array($w->save($r)),'transient METADATA write failure still keeps durable worker state');
check(get_option($key.'_meta')['count']===3,'orphan event detected and metadata repaired immediately');check(count(get_option($key.'_c0'))===3,'event numbering preserved without duplicates');clear_fault();
$r['progress_seq']=4;fault($key.'_meta',-1);check(is_array($w->save($r)),'PERSISTENT metadata outage never invalidates primary run state');
check(get_option($key.'_meta')['count']===3 && count(get_option($key.'_c0'))===4,'durable orphan kept without overwrite');check(get_option('ppar_ebay_audit_write_error_v1',0)>0,'unrecovered failure visibly flagged');
clear_fault();$r['progress_seq']=5;check(is_array($w->save($r)),'run works after recovery');check(get_option($key.'_meta')['count']===5,'orphan from earlier failed write repaired before appending new event');
check(count(get_option($key.'_c0'))===5,'all 5 events retained once');
for($i=6;$i<=101;$i++){$r['progress_seq']=$i;$w->save($r);}check(get_option($key.'_meta')['count']===101,'crossed immutable 100-event chunk boundary');
$r['progress_seq']=102;fault($key.'_meta',1);$w->save($r);clear_fault();check(get_option($key.'_meta')['count']===102 && count(get_option($key.'_c1'))===2,'second chunk boundary also repairs metadata on retry');
// source errors retained in the original immutable event log
$r['progress_seq']=103;$r['phase']='public_verify';$r['public_source_refresh']=['provider_errors'=>2,'provider_error_samples'=>[['post_id'=>55,'code'=>'ebay_refresh_http']]];$w->save($r);
$all=array_merge(get_option($key.'_c0'),get_option($key.'_c1'));$last=end($all);check($last['source_provider_errors']===2 && $last['source_error_examples'][0]['post_id']===55,'affected product and original error remain in audit');
$r['status']='failed';$r['phase']='failed';$r['error_code']='public_source_refresh_provider_failed';$r['progress_seq']=104;$w->save($r);
$new=['schema'=>'1.0','run_uuid'=>'next-run-after-error','status'=>'running','phase'=>'reconcile_local','progress_seq'=>1];$w->save($new);
check(get_option($key.'_meta')['count']>=104,'old failed run remains in journal after new run');check(get_option($w->key($new['run_uuid']).'_meta')['count']===1,'new run starts separate journal');
check(in_array('fault-injection-run',get_option('ppar_ebay_audit_run_index_v1'),true),'archive index retains old failure');
echo "QA15_AUDIT_STORAGE_MATRIX_PASSED\n";