<?php
// Exercise actual QA7 plugin trait's public product safety gates under controlled input.
define('ABSPATH','/tmp');
function absint($v){return abs((int)$v);}
function sanitize_key($v){return preg_replace('/[^a-z0-9_-]/','', strtolower((string)$v));}
function sanitize_text_field($v){return (string)$v;}
function get_post_meta($id,$key,$single=true){
    $values=['_ppar_ebay_business_auto'=>1,'_ppar_ebay_business_match_contract'=>'concept_v3'];
    return $values[$key]??'';
}
require '/mnt/data/ebay_current_inspect/affiliate-portal-router/includes/trait-ppar-ebay.php';
class RealSourceGateHarness{
  use PPAR_Ebay_Trait;
  public array $source=[];
  public array $allowed=[123];
  private function ebay_business_campaign_source_row($campaign){return $this->source;}
  private function ebay_public_content_policy_reason_from_source_row($row,$title){return '';}
  private function ebay_request_local_read_cache_allowed(){return false;}
  private function ebay_public_checkpoint_allows_business_campaign($id){return in_array((int)$id, $this->allowed, true);}
  public function probe($campaign){return $this->ebay_business_campaign_source_allows_delivery($campaign);}
}
$h=new RealSourceGateHarness();
$c=['network'=>'ebay','creative_type'=>'product','post_id'=>123,'title'=>'Schabracke'];
$h->source=['source_state'=>'available','policy_state'=>'allowed','route_state'=>'ready','fresh_until'=>time()+3600,'item_end_at'=>0];
if(!$h->probe($c)) throw new RuntimeException('Fresh expected visible');
echo "PASS: fresh allowed campaign visible\n";
$h->source['fresh_until']=time()-1;
if($h->probe($c)) throw new RuntimeException('Stale expected hidden');
echo "PASS: same campaign hidden exactly when source is stale\n";
$h->source['fresh_until']=time()+3600;
$h->allowed=[];
if($h->probe($c)) throw new RuntimeException('Checkpoint not-listed expected hidden');
echo "PASS: same fresh campaign hidden when checkpoint excludes campaign ID\n";
$h->allowed=[123];
if(!$h->probe($c)) throw new RuntimeException('Recovery expected visible');
echo "PASS: same fresh campaign and checkpoint-allowed visible\n";
