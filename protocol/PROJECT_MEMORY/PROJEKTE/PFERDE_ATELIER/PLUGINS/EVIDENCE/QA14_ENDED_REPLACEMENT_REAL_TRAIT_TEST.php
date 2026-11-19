<?php
error_reporting(E_ALL);
define('ABSPATH','/wp/');
define('ARRAY_A','ARRAY_A');
function absint($v){return abs((int)$v);}
function sanitize_key($v){return preg_replace('/[^a-z0-9_\-]/','',strtolower((string)$v));}
function sanitize_text_field($v){return trim((string)$v);}
function is_wp_error($x){return $x instanceof WP_Error;}
class WP_Error{public function __construct($why=''){} }
class FakeDb {
  public $last_error='';public $rows=[];public $campaign_ids=[];public $read_error=false;
  public function prepare($sql,...$args){return $sql;}
  public function get_results($sql,$mode=null){return $this->rows;}
  public function get_col($sql){$this->last_error=$this->read_error?'sql_failed':'';return $this->campaign_ids;}
}
function check($ok,$desc){if(!$ok)throw new Exception('FAIL '.$desc);echo "PASS $desc\n";}
require __DIR__.'/affiliate-portal-router/includes/trait-ppar-ebay.php';
class T {
  use PPAR_Ebay_Trait;
  public $next_results=[];public $append_count=0;public $append_value=1;public $rebuild_count=0;public $routes=0;public $purge_count=0;
  public function promote($row){return $this->ebay_business_promote_ended_replacement($row,['business_enabled'=>1]);}
  public function ended($row){return $this->ebay_refresh_mark_ended($row,'ENDED',['business_enabled'=>1]);}
  private function ebay_normalize_settings($s,$strict=true){return $s;}
  private function ebay_items_table(){return 'items';}
  private function output_objects_table(){return 'outputs';}
  private function ebay_business_source_row_item($row,$s){return ['portal_classification'=>['product_concept_id'=>'concept-a']];}
  private function ebay_business_quality_assess($item,$class,$rule,$s,$limit=0){return ['score'=>100];}
  private function ebay_rule_by_id($id,$s){return ['id'=>$id];}
  private function ebay_business_candidate_sort(&$rows){}
  private function ebay_business_persist_quality_on_source_row($row,$quality,$role,$rank){return true;}
  private function ebay_business_item_with_quality($item,$quality){return $item;}
  private function ebay_route_business($row,$item,$rule,$uuid,$class){$this->routes++;return array_shift($this->next_results);}
  private function ebay_public_checkpoint_add_verified_business_ids($ids,$reason){$this->append_count++;return $this->append_value;}
  private function ebay_purge_item_content($row,$scope,$reason){$this->purge_count++;return ['status'=>'purged'];}
  private function article_hybrid_enabled(){return true;}
  private function article_plan_campaign_revision(){return 1;}
  private function article_plan_rebuild_request($reason,$revision=0,$mode='full'){$this->rebuild_count++;return ['reason'=>$reason];}
}
$payload=json_encode(['portal_classification'=>['product_concept_id'=>'concept-a']]);
$ended=['seller_account_type'=>'BUSINESS','output_state'=>'creative_ready','source_payload'=>$payload,'item_id'=>'old','rule_id'=>'concept-a'];
$row=['seller_account_type'=>'BUSINESS','output_state'=>'reserve','item_id'=>'new','rule_id'=>'concept-a', 'policy_state'=>'allowed','source_state'=>'available','route_state'=>'ready','source_payload'=>$payload];
function resetFixture($rows,$results,$ids=[123],$append=1){global $wpdb;$wpdb=new FakeDb;$wpdb->rows=$rows;$wpdb->campaign_ids=$ids;$t=new T;$t->next_results=$results;$t->append_value=$append;return $t;}
$ok=['state'=>'created','creative_identity_hash'=>str_repeat('a',64),'plan'=>['active'=>1]];
$t=resetFixture([$row],[$ok]);$r=$t->ended($ended);
check($r['replacement']['promoted']===1,'verified replacement actually entered public checkpoint');
check($t->append_count===1,'uses the EXISTING single append gate');
check($t->rebuild_count===1,'ended old article campaign triggers existing article-plan refresh');
check($t->purge_count===1,'old ended campaign still removed');
$t=resetFixture([$row],[['last_good_preserved'=>1,'state'=>'last_good_preserved','plan'=>['active'=>0]]]);$r=$t->promote($ended);
check($r['promoted']===0 && $t->append_count===0,'non-error soft review is NOT a successful replacement');
$t=resetFixture([$row],[$ok],[]);$r=$t->promote($ended);
check($r['promoted']===0 && $r['status']==='public_checkpoint_pending','materialized but unproven publication not reported as promoted');
$t=resetFixture([$row],[$ok],[123],0);$r=$t->promote($ended);
check($r['promoted']===0 && $r['status']==='public_checkpoint_pending','failed public append not declared as public replacement');
$t=resetFixture([$row],[$ok]);$GLOBALS['wpdb']->read_error=true;$r=$t->promote($ended);
check($r['promoted']===0 && $r['status']==='public_link_storage_error','database read failure cannot become fake replacement');
$t=resetFixture([$row],[$ok]);$x=$ended;$x['output_state']='candidate';$r=$t->ended($x);
check($r['replacement']['promoted']===0 && $t->rebuild_count===0,'unpublished candidate does not start article refresh');
$t=resetFixture([$row],[$ok]);$r=$t->ended($ended);
check($t->rebuild_count===1 && $t->purge_count===1,'published product revoked once and same worker refresh requested');
$t=resetFixture([$row,$row],[['last_good_preserved'=>1,'plan'=>['active'=>0]],$ok]);$r=$t->promote($ended);
check($r['promoted']===1 && $t->routes===2,'a soft-review reserve is skipped in favor of a truly published reserve');
check($t->append_count===1,'no duplicate public append worker when second reserve succeeds');
print "ALL QA14 ENDED-REPLACEMENT ORIGINAL-TRAIT TESTS PASS\n";