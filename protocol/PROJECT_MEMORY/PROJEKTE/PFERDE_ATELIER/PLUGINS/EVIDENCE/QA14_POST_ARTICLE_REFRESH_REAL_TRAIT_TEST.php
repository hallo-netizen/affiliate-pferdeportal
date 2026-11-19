<?php
error_reporting(E_ALL);
define('ABSPATH','/wp/');
$GLOBALS['o']=[];$GLOBALS['scheduled']=[];
function get_option($k,$default=false){return $GLOBALS['o'][$k]??$default;}
function update_option($k,$v,$autoload=false){$GLOBALS['o'][$k]=$v;return true;}
function wp_parse_args($a,$b){return array_merge($b,$a);}
function absint($x){return abs((int)$x);}
function sanitize_text_field($s){return trim((string)$s);}
function sanitize_key($s){return preg_replace('/[^a-z0-9_\-]/','',strtolower((string)$s));}
function wp_next_scheduled($hook){return isset($GLOBALS['scheduled'][$hook]);}
function wp_schedule_single_event($time,$hook){$GLOBALS['scheduled'][$hook]=$time;return true;}
function is_wp_error($v){return $v instanceof WP_Error;}
class WP_Error {public function __construct($code=''){} }
require __DIR__.'/affiliate-portal-router/includes/trait-ppar-article-plans.php';
class RealSourceFixture {
  use PPAR_Article_Plans_Trait;
  const OPTION_ARTICLE_REBUILD_STATE='state';
  const OPTION_ARTICLE_PLAN_REVISION='rev';
  const ARTICLE_REBUILD_HOOK='article_worker';
  public $scans=[];
  public function request($reason,$revision=1,$mode='products_only'){return $this->article_plan_rebuild_request($reason,$revision,$mode);}
  public function tick($limit=25){return $this->article_plan_rebuild_batch($limit);}
  public function state(){return $this->article_plan_rebuild_state_load();}
  private function article_hybrid_enabled(){return true;}
  private function article_plan_rebuild_post_ids_after($cursor,$limit){return array_slice(array_values(array_filter(range(1,60),fn($id)=>$id>$cursor)),0,$limit);}
  private function article_plan_refresh_saved_products_only($post_id){$this->scans[]=$post_id;return ['status'=>'ready'];}
  private function article_plan_build($post_id,$reason='manual'){$this->scans[]=$post_id;return ['status'=>'ready'];}
}
function test_assert($bool,$why){if(!$bool){echo "FAIL $why\n";exit(1);}echo "PASS $why\n";}
$GLOBALS['o']=['rev'=>1];$t=new RealSourceFixture;
$t->request('ebay_verified_business_incremental');
$first=$t->tick();
test_assert($first['cursor']===25,'first page advances to post 25');
for($i=0;$i<7;$i++)$t->request('ebay_verified_business_incremental');
$open=$t->state();
test_assert($open['cursor']===25 && $open['pending_ebay_product_pass']===1,'seven eBay append signals neither reset cursor nor add seven passes');
$t->tick();$p=$t->tick();test_assert($p['status']==='running' && $p['cursor']===0 && $p['reason']==='ebay_checkpoint_tail_refresh','after reaching post 60 exactly one second pass starts');
$t->tick();$t->tick();$done=$t->tick();
test_assert($done['status']==='complete' && count($t->scans)===120,'both complete 60-post passes finish, no starvation');
test_assert(count(array_unique($t->scans))===60,'all 60 original articles reached');
test_assert(empty($done['pending_ebay_product_pass']),'pending flag cleared at finish');
$t->request('ebay_public_checkpoint_changed');$t->tick();$v=$t->state();$t->request('v_campaign_revision',1,'full');
test_assert($t->state()['cursor']===0 && $t->state()['mode']==='full','ordinary full rebuild still restarts as before');
$t->tick();$t->request('ebay_public_checkpoint_changed');$p=$t->state();
test_assert($p['cursor']===25 && !empty($p['pending_ebay_product_pass']),'eBay append cannot reset an ordinary full rebuild');
// If the scheduled event was lost, the existing worker must be requeued.
$GLOBALS['scheduled']=[];
$t->request('ebay_verified_business_incremental');
test_assert(isset($GLOBALS['scheduled']['article_worker']) && $t->state()['cursor']===25,'lost WP-Cron event requeued without resetting the same cursor');
$t->tick();$p=$t->tick();test_assert($p['mode']==='products_only' && $p['cursor']===0,'post-full eBay-only pass scheduled');
$t->tick();$t->tick();$end=$t->tick();test_assert($end['status']==='complete','pending article-only pass also finishes');
$GLOBALS['o']=['rev'=>1];$t=new RealSourceFixture;$t->request('ebay_verified_business_incremental');$t->tick();$GLOBALS['o']['rev']=2;
$t->tick();test_assert($t->state()['revision']===2 && $t->state()['cursor']===25,'revision supersession resets to new revision and resumes first batch');
print "ALL QA14 ARTICLE REFRESH CASES PASS\n";