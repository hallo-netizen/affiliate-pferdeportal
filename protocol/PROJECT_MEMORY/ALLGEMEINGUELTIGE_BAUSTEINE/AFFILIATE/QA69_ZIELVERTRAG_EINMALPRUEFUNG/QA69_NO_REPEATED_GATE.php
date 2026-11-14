<?php
/** True unchanged PHP Run trait, only WP storage and public gate outcome mocked.
 * Verifies NO re-proof when the exact same already SAFE products reappear.
 * Does not claim actual product safety or live publication.
 */
define('ABSPATH',__DIR__.'/');
function sanitize_key($x){return preg_replace('/[^a-z0-9_-]/','',strtolower((string)$x));}
function sanitize_text_field($x){return trim(strip_tags((string)$x));}
function absint($x){return abs((int)$x);}
function wp_json_encode($x,$opts=0){return json_encode($x,$opts);}
function get_option($key,$fallback=array()){return $GLOBALS['OPTIONS'][$key]??$fallback;}
function update_option($key,$value,$aut=false){$GLOBALS['OPTIONS'][$key]=$value;return true;}
class WP_Error extends Exception {function get_error_code(){return 'qa_failure';}}
function is_wp_error($x){return $x instanceof WP_Error;}
$GLOBALS['OPTIONS']=[];
require $argv[1];
class QATest {
 use PPAR_Ebay_Run_Trait;
 const OPTION_EBAY_PUBLIC_CHECKPOINT='qa_public_checkpoint';
 public $gate_calls=0,$save_calls=0;
 private function ebay_run_public_business_coverage($ids=null){$this->gate_calls++;return ['verified_campaign_ids'=>$ids,'verified_source_items'=>[]];}
 private function ebay_public_checkpoint_save($cp,$before=null){$this->save_calls++;$GLOBALS['OPTIONS'][self::OPTION_EBAY_PUBLIC_CHECKPOINT]=$cp;return $cp;}
 private function article_hybrid_enabled(){return false;}
 public function run($ids){$m=new ReflectionMethod($this,'ebay_public_checkpoint_add_verified_business_ids');$m->setAccessible(true);return $m->invoke($this,$ids,'qa69');}
}
function c($name,$cp,$ids){$GLOBALS['OPTIONS']['qa_public_checkpoint']=$cp;$q=new QATest();$ret=$q->run($ids);return ['case'=>$name,'gate_calls'=>$q->gate_calls,'save_calls'=>$q->save_calls,'result'=>$ret,'post_count'=>count((array)($GLOBALS['OPTIONS']['qa_public_checkpoint']['business_campaign_ids']??[]))];}
$old=['schema'=>'1.0','status'=>'safe','checkpoint_id'=>'existing-verified-578','business_campaign_ids'=>range(1001,1578),'private_listing_ids'=>[]];
$a=[];$a[]=c('duplicate_known_578_no_second_gate',$old,[1001,1002]);
$a[]=c('one_new_candidate_proven_once',$old,[1579]);
$a[]=c('unsafe_previous_checkpoint_not_overwritten',['schema'=>'1.0','status'=>'bad','checkpoint_id'=>'legacy','business_campaign_ids'=>range(1001,1578)], [1580]);
foreach($a as $x){echo json_encode($x,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)."\n";}