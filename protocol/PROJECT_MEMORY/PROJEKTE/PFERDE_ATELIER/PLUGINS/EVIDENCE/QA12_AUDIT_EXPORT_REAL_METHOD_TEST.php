<?php
error_reporting(E_ALL); define('ABSPATH','/tmp');
$GLOBALS['options']=array();$GLOBALS['authorized']=true;
function get_option($key,$default=null){return array_key_exists($key,$GLOBALS['options'])?$GLOBALS['options'][$key]:$default;}
function update_option($key,$v,$a=false){$GLOBALS['options'][$key]=$v;return true;}
function absint($v){return abs((int)$v);}function sanitize_key($v){return preg_replace('/[^a-z0-9_\-]/','',strtolower((string)$v));}
function sanitize_text_field($v){return strip_tags(trim((string)$v));}function wp_json_encode($v,$f=0){return json_encode($v,$f);}
function current_user_can($cap){return $GLOBALS['authorized'];}function check_admin_referer($a,$b){return true;}
function wp_die($x,$s=0){throw new Exception($x);}function wp_unslash($v){return $v;} function nocache_headers(){}
require __DIR__.'/build/affiliate-portal-router/includes/trait-ppar-ebay-run.php';
class T { use PPAR_Ebay_Run_Trait;const EBAY_RUNTIME_BUILD='q12';public function save($x){return $this->ebay_run_save($x);} }
$x=new T();
for($i=0;$i<103;$i++){$x->save(['schema'=>'1.0','run_uuid'=>'old-run-a','status'=>'running','phase'=>'public_verify','progress_seq'=>$i+1,'transport_tick_count'=>$i+1]);}
$x->save(['schema'=>'1.0','run_uuid'=>'new-run-b','status'=>'failed','phase'=>'failed','error_code'=>'ebay_bad','progress_seq'=>1]);
$GLOBALS['options']['ppar_ebay_run_history_v1']=[['run_uuid'=>'legacy-old','status'=>'completed','phase'=>'completed','error_code'=>'','finished_at'=>12345]];
$_POST=['run_uuid'=>'all','format'=>'csv'];$x->handle_ebay_audit_export();