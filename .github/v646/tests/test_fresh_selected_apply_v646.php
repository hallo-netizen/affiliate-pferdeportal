<?php
error_reporting(E_ALL);
define('ABSPATH','/tmp/'); define('ARRAY_A','ARRAY_A'); define('HOUR_IN_SECONDS',3600); define('DAY_IN_SECONDS',86400);
class WP_Error{private $c,$m;function __construct($c='',$m=''){$this->c=$c;$this->m=$m;}function get_error_code(){return $this->c;}function get_error_message(){return $this->m;}}
function is_wp_error($x){return $x instanceof WP_Error;} function absint($v){return abs((int)$v);} function sanitize_key($v){return preg_replace('/[^a-z0-9_\-]/','',strtolower((string)$v));}
function sanitize_text_field($v){return trim(strip_tags((string)$v));} function sanitize_title($v){return trim(preg_replace('/[^a-z0-9]+/','-',strtolower((string)$v)),'-');}
function wp_json_encode($v,$o=0){return json_encode($v,$o);} function esc_url_raw($v){return $v;} function wp_http_validate_url($v){return true;} function remove_accents($v){return $v;} function wp_strip_all_tags($v){return strip_tags((string)$v);} function apply_filters($a,$b){return $b;}
class DB{public $prefix='wp_',$rows=array(); function prepare($q,...$a){return array('q'=>$q,'a'=>$a);} function get_results($q,$m=null){return $this->rows;} function get_row($q,$m=null){return null;} function update(){return 1;} }
$GLOBALS['wpdb']=new DB();
$root=getenv('PPAR_TEST_PLUGIN_DIR'); if(!$root){fwrite(STDERR,"missing root\n");exit(2);} require $root.'/includes/trait-ppar-ebay.php';
class H{use PPAR_Ebay_Trait; const EBAY_CONTENT_POLICY_VERSION='6.1',EBAY_BUSINESS_CLASSIFIER_VERSION='6.1',OPTION_EBAY_SELECTION_STATE='selection';
 private function ebay_settings(){return array();}
 public function apply(&$state){return $this->ebay_selection_apply_business_batch(array(),$state,1);} }
$now=time();
$row=array('id'=>1,'item_id'=>'fresh-1','seller_account_type'=>'BUSINESS','source_state'=>'available','policy_state'=>'allowed','route_state'=>'ready','fresh_until'=>$now+3600,'item_end_at'=>0,'rule_id'=>'test-concept','creative_identity_hash'=>'');
$GLOBALS['wpdb']->rows=array($row);
$state=array('business_cursor'=>0,'business_active'=>array('fresh-1'=>array('concept'=>'test-concept','rank'=>1)),'business_soft_failed'=>array(),'stats'=>array('business'=>array('scanned'=>0,'materialized'=>0,'active'=>0,'errors'=>array())),'plan_stats'=>array());
$h=new H(); $h->apply($state);
$kept=isset($state['business_active']['fresh-1']);
$notstale=!isset($state['business_soft_failed']['fresh-1']);
$recoverable=(int)($state['stats']['business']['recoverable_failed']??0)===0;
$f=0;$n=0; foreach(array('fresh active winner is not rejected by freshness guard'=>$kept,'fresh winner gets no stale soft-failure marker'=>$notstale,'fresh winner does not increment stale recoverable accounting'=>$recoverable) as $m=>$ok){$n++;echo($ok?'PASS ':'FAIL ').$m."\n";if(!$ok)$f++;}
echo "ASSERTIONS=$n FAIL=$f\n"; exit($f?1:0);
