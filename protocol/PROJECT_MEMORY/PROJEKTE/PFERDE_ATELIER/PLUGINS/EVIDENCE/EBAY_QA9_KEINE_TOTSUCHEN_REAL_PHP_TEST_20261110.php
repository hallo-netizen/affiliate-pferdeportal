<?php
error_reporting(E_ALL);
define('ABSPATH','/');
function wp_strip_all_tags($x){return strip_tags((string)$x);}
function remove_accents($x){return strtr((string)$x,['ä'=>'a','ö'=>'o','ü'=>'u','Ä'=>'A','Ö'=>'O','Ü'=>'U','ß'=>'ss']);}
function sanitize_key($x){return strtolower(preg_replace('/[^a-z0-9_-]/','',strtolower((string)$x)));}
function sanitize_text_field($x){return trim((string)$x);}
function sanitize_title($x){return trim(preg_replace('/[^a-z0-9-]+/','-',strtolower(remove_accents($x))),'-');}
function absint($x){return abs((int)$x);}
function is_wp_error($x){return $x instanceof WP_Error;}
class WP_Error {private $c,$m;function __construct($c,$m){$this->c=$c;$this->m=$m;}function get_error_code(){return $this->c;}function get_error_message(){return $this->m;}}
require __DIR__.'/../ebay_qa9_kiss/affiliate-portal-router/includes/trait-ppar-ebay.php';
require __DIR__.'/../ebay_qa9_kiss/affiliate-portal-router/includes/trait-ppar-ebay-run.php';
class NoLoopAudit { use PPAR_Ebay_Trait, PPAR_Ebay_Run_Trait;
    public $lastSaved=null;public $failure=null;
    private function ebay_portal_catalog(){return json_decode(file_get_contents(__DIR__.'/../ebay_qa9_kiss/affiliate-portal-router/assets/ebay-portal-catalog-v2.json'),true);}
    private function ebay_run_save($run){$this->lastSaved=$run;return $run;}
    private function ebay_run_fail($code,$message,$details=[]){$this->failure=[$code,$message,$details];}
    public function manifest(){ $m=new ReflectionMethod($this,'ebay_business_required_product_concept_ids');return $m->invoke($this); }
    public function rediscover($run,$coverage){$m=new ReflectionMethod($this,'ebay_run_schedule_new_business_gap_revalidation');return $m->invoke($this,$run,$coverage,'coverage_verify');}
}
$a=new NoLoopAudit;
$r=$a->manifest();
$excluded=['concept-pferde-op-versicherung','concept-pferdekrankenversicherung','concept-pferdehaftpflicht','concept-haltungsberatung','concept-einstellvertrag-vorlagen'];
function check($condition,$label){echo ($condition?'PASS ':'FAIL ').$label."\n";if(!$condition){exit(2);}}
check(count($r)===298,'298 actual required product families');
foreach($excluded as $id){check(!in_array($id,$r,true),'excluded: '.$id);}
check(in_array('concept-anhangerkameras',$r,true),'real camera goods must remain');
$run=['gapfill'=>['attempts'=>1,'missing'=>['concept-anhangerkameras']]];
$coverage=['missing'=>['concept-anhangerkameras']];
check($a->rediscover($run,$coverage)===false,'already-searched family does not restart inside run');
check($a->lastSaved===null,'no background job scheduled for already-searched family');
$new=['missing'=>['concept-anhangerkameras','concept-pferdesattel']];
check($a->rediscover($run,$new)===true,'only genuinely newly-missing family may trigger bounded delta search');
check($a->lastSaved['gapfill']['discovery_missing']===['concept-pferdesattel'],'only one new family is searched');
check(count($a->lastSaved['gapfill']['missing'])===2,'previous missing scope preserved');
check($a->rediscover($a->lastSaved,$new)===false,'no repeat when coverage unchanged after delta search');
check($a->failure===null,'no errors in normal safety cases');