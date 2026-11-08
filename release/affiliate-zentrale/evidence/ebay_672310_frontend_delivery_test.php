<?php
/* Test-only: real trait methods, mocked WP/DB. No original 6.72.308, no production side effects. */
error_reporting(E_ALL);
if (!defined('ABSPATH')) define('ABSPATH','/');
if (!defined('ARRAY_A')) define('ARRAY_A','ARRAY_A');
$META=array();
function absint($v){return abs((int)$v);}
function sanitize_key($v){return strtolower(preg_replace('/[^a-z0-9_-]/','',strtolower((string)$v)));}
function sanitize_text_field($v){return trim((string)$v);}
function get_post_meta($id,$key,$single=true){global $META;return $META[$id][$key]??'';}
class TestDB {
    public $row=array(),$reads=0,$last_error='';
    function prepare($sql,...$args){if(count($args)===1 && is_array($args[0]))$args=$args[0];
        foreach($args as $v)$sql=preg_replace('/%s/',"'".addslashes((string)$v)."'",$sql,1);
        return $sql;
    }
    function project($sql){
        $this->reads++;
        if(!preg_match('/SELECT\s+(.*?)\s+FROM\s/is',$sql,$m))throw new RuntimeException('Bad SQL '.$sql);
        $cols=array_map('trim',explode(',',$m[1]));
        return array_intersect_key($this->row,array_flip($cols));
    }
    function get_row($sql,$m){return $this->project($sql);}
    function get_results($sql,$m){return array($this->project($sql));}
}
require __DIR__ . '/affiliate-portal-router/includes/trait-ppar-ebay.php';
class TestBusiness {
    use PPAR_Ebay_Trait;
    public $checkpoint=true,$blocked=false;
    private function ebay_items_table(){return 'items_test';}
    private function ebay_public_content_policy_reason_from_source_row($row,$title){return $this->blocked?'blocked':'';}
    private function ebay_public_checkpoint_allows_business_campaign($id){return $this->checkpoint;}
    public function allowed($c){return $this->ebay_business_campaign_source_allows_delivery($c);}
    public function prime($c){return $this->ebay_prime_business_campaign_source_row_cache_for_campaigns(array($c));}
    public function reset(){ $this->ebay_business_campaign_source_row_cache=array();$this->ebay_business_campaign_source_allowed_request_cache=array();}
}
function check($x,$name){if(!$x){fwrite(STDERR,"FAIL ".$name."\n");exit(2);}echo "PASS ".$name."\n";}
global $wpdb,$META;$wpdb=new TestDB();
$hash=str_repeat('a',64);
$META[101]=array('_ppar_ebay_business_auto'=>1,'_ppar_creative_identity_hash'=>$hash,'_ppar_ebay_business_match_contract'=>'concept_v3');
$wpdb->row=array('id'=>1,'item_id'=>'ebay-business','creative_identity_hash'=>$hash,'seller_account_type'=>'BUSINESS',
'source_state'=>'available','policy_state'=>'allowed','route_state'=>'ready','fresh_until'=>time()+300,
'item_end_at'=>0,'source_payload'=>'','title'=>'Sattel','short_description'=>'');
$campaign=array('network'=>'ebay','creative_type'=>'product','post_id'=>101,'title'=>'Sattel');$app=new TestBusiness();
check($app->allowed($campaign)===true,'fresh BUSINESS product is public');
check($wpdb->reads===1,'single source lookup uses one SQL query');
$app->reset();$wpdb->row['fresh_until']=time()-1;
check($app->allowed($campaign)===false,'six-hour source expiry hides BUSINESS product');
$app->reset();$wpdb->row['fresh_until']=0;
check($app->allowed($campaign)===false,'unknown source freshness never appears as public');
$app->reset();$wpdb->row['fresh_until']=time()+300;$app->prime($campaign);
check($app->allowed($campaign)===true,'prefetched fresh source still visible');
check($wpdb->reads===4,'prefetched source uses one bulk SQL without extra per-card query');
$app->reset();$wpdb->row['fresh_until']=time()-2;$app->prime($campaign);
check($app->allowed($campaign)===false,'prefetched expired source cannot bypass gate');
$app->reset();$wpdb->row['fresh_until']=time()+300;$app->checkpoint=false;
check($app->allowed($campaign)===false,'no safe checkpoint blocks publication');
$app->reset();$app->checkpoint=true;$app->blocked=true;
check($app->allowed($campaign)===false,'hard forbidden-content gate takes priority');
$app->reset();$app->blocked=false;$wpdb->row['source_state']='ended';
check($app->allowed($campaign)===false,'ended eBay source cannot be shown');
$app->reset();$wpdb->row['source_state']='available';$wpdb->row['item_end_at']=time()-1;
check($app->allowed($campaign)===false,'expired itemEndDate blocks publication');
$app->reset();$wpdb->row['item_end_at']=0;$wpdb->row['policy_state']='blocked';
check($app->allowed($campaign)===false,'hard blocked policy blocks public card');
echo "EBAY_FRONTEND_SOURCE_CONTRACT 12/12 PASS; full original and live end-to-end still required\n";
