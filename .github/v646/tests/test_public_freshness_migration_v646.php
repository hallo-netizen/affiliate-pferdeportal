<?php
error_reporting(E_ALL);
define('ABSPATH','/tmp/'); define('ARRAY_A','ARRAY_A');
$GLOBALS['opts']=array();
class WP_Error{private $c,$m;function __construct($c='',$m=''){$this->c=$c;$this->m=$m;}function get_error_code(){return $this->c;}function get_error_message(){return $this->m;}}
function is_wp_error($x){return $x instanceof WP_Error;} function absint($v){return abs((int)$v);} function sanitize_key($v){return preg_replace('/[^a-z0-9_\-]/','',strtolower((string)$v));} function sanitize_text_field($v){return trim(strip_tags((string)$v));}
function wp_json_encode($v,$o=0){return json_encode($v,$o);} function get_option($k,$d=array()){return array_key_exists($k,$GLOBALS['opts'])?$GLOBALS['opts'][$k]:$d;} function update_option($k,$v,$a=false){$GLOBALS['opts'][$k]=$v;return true;} function maybe_serialize($v){return serialize($v);} function maybe_unserialize($v){$x=@unserialize($v);return $x===false&&$v!=='b:0;'?$v:$x;} function wp_cache_delete(){return true;}
class DB{public $options='wp_options'; function prepare($q,...$a){return array('q'=>$q,'a'=>$a);} function query($p){$a=$p['a'];$after=$a[0];$key=$a[1];$before=$a[2];$cur=maybe_serialize(get_option($key,array()));if(!hash_equals((string)$before,(string)$cur))return 0;$GLOBALS['opts'][$key]=maybe_unserialize($after);return 1;}}
$GLOBALS['wpdb']=new DB();
$root=getenv('PPAR_TEST_PLUGIN_DIR'); if(!$root){fwrite(STDERR,"missing root\n");exit(2);} require $root.'/includes/trait-ppar-ebay-run.php';
class H{use PPAR_Ebay_Run_Trait; const OPTION_EBAY_RUN_STATE='run',OPTION_EBAY_SELECTION_STATE='selection',OPTION_EBAY_REFRESH_JOB='refresh',EBAY_PROGRESS_CONTRACT_VERSION='2.0',EBAY_RUNTIME_BUILD='6.46.0-test'; public function migrate(){if(method_exists($this,'maybe_migrate_ebay_public_freshness_v6460'))$this->maybe_migrate_ebay_public_freshness_v6460();} public function state(){return $this->ebay_run_load();}}
$required=array();for($i=1;$i<=311;$i++)$required[]='c'.$i;
$invalid=array();for($i=1;$i<=231;$i++)$invalid[$i]='source_stale';
$uuid='110e360b-ad6-v645-stale';$at=time()-5;
$run=array('schema'=>'1.0','build'=>'6.45.0-canonical-run-persistence-race-rootfix-20260820','run_uuid'=>$uuid,'status'=>'failed','phase'=>'failed','finished_at'=>$at,'owner'=>'','lease_expires_at'=>0,'worker_transport'=>'admin_ajax','no_progress_count'=>0,'error_code'=>'insufficient_safe_sources','error_message'=>'x','phase_state'=>array('selection'=>array('stats'=>array('business'=>array('materialized'=>231))),'refresh'=>array('status'=>'completed')),'coverage'=>array('required'=>311,'covered'=>0,'missing'=>$required,'invalid'=>$invalid),'gapfill'=>array('attempts'=>1,'missing'=>$required),'end_manifest'=>array('bad'=>1),'errors'=>array(array('code'=>'insufficient_safe_sources','at'=>$at,'details'=>array('phase'=>'coverage_verify','build'=>'6.45.0-canonical-run-persistence-race-rootfix-20260820'))),'recovery_history'=>array());
update_option('run',$run,false);update_option('selection',array('status'=>'complete'),false);update_option('refresh',array('status'=>'completed'),false);
$h=new H();$h->migrate();$a=$h->state();
$f=0;$n=0;function ck($v,$m){global$f,$n;$n++;echo($v?'PASS ':'FAIL ').$m."\n";if(!$v)$f++;}
ck(($a['run_uuid']??'')===$uuid,'recovery preserves exact V6.45 run UUID');
ck(($a['status']??'')==='running'&&($a['phase']??'')==='reconcile_local','all-stale V6.45 public failure re-enters canonical reconcile path');
ck(($a['resume_reason']??'')==='public_freshness_contract_recovery','recovery reason is explicit');
ck(($a['coverage']??null)===array()&&($a['gapfill']??null)===array('attempts'=>0,'missing'=>array()),'only derived coverage/gapfill tail is invalidated');
ck(get_option('selection',null)===array()&&get_option('refresh',null)===array(),'nested selection and completed refresh job are cleared only after CAS');
$once=$a;$h->migrate();ck($h->state()===$once,'recovery migration is idempotent');
$bad=$run;$bad['run_uuid']=$uuid.'-mixed';$bad['coverage']['invalid'][1]='campaign_not_public';update_option('run',$bad,false);update_option('selection',array('status'=>'complete'),false);update_option('refresh',array('status'=>'completed'),false);$h->migrate();$b=$h->state();
ck(($b['status']??'')==='failed'&&($b['error_code']??'')==='insufficient_safe_sources','mixed/unknown public failure is not auto-recovered');
ck(get_option('selection',null)!==array()&&get_option('refresh',null)!==array(),'negative case performs no nested-state mutation');
echo "ASSERTIONS=$n FAIL=$f\n";exit($f?1:0);
