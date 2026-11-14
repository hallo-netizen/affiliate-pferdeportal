#!/usr/bin/env python3
"""Original PHP import -> storage -> campaign path, including failures.

Only local synthetic CSV and fake WordPress DB; no private Idealo credentials.
Tests the ONE storage boundary, no late topical re-decision.
"""
from pathlib import Path
from zipfile import ZipFile
import re,sys

with ZipFile(Path(sys.argv[1])) as z:
    idealo=z.read('affiliate-portal-router/includes/trait-ppar-idealo.php').decode()
    network=z.read('affiliate-portal-router/includes/trait-ppar-network-sync.php').decode()

def method(source,name):
    a=re.search(r'^    (?:private|protected|public) function '+re.escape(name)+r'\(',source,re.M)
    assert a, "Original method missing: "+name
    b=re.search(r'^    (?:private|protected|public) function ',source[a.end():],re.M)
    return source[a.start():a.end()+b.start()] if b else source[a.start():]

names=['idealo_match_contract_revision','idealo_import_feed_file','idealo_materialize_campaigns',
       'idealo_target_keys_for_concept','idealo_payload_rank_tuple','idealo_campaigns_should_be_active']
source="\n".join(method(idealo,n) for n in names)+"\n"+method(network,'network_sync_upsert_products')
assert 'idealo_staging_write_failed' in source
assert 'idealo_staging_read_failed' in source
assert "if (is_wp_error($counts)) { return $counts; }" in source

php=r'''<?php
error_reporting(E_ALL);ini_set('display_errors','1');
define('ARRAY_A','ARRAY_A'); define('HOUR_IN_SECONDS',3600);
class WP_Error {
 private $code,$message;
 function __construct($c,$m){$this->code=$c;$this->message=$m;}
 function get_error_code(){return $this->code;}
 function get_error_message(){return $this->message;}
}
function is_wp_error($x){return $x instanceof WP_Error;}
function absint($x){return abs((int)$x);}
function sanitize_text_field($x){return trim(strip_tags((string)$x));}
function sanitize_key($x){return preg_replace('/[^a-z0-9_\-]/','',strtolower((string)$x));}
function sanitize_title($x){return preg_replace('/[^a-z0-9_\-]/','',strtolower((string)$x));}
function esc_url_raw($x){return (string)$x;}
function wp_json_encode($v,$flags=0){return json_encode($v,$flags);}
function get_option($k,$default=null){return $GLOBALS['options'][$k]??$default;}
function update_option($k,$v,$autoload=false){$GLOBALS['options'][$k]=$v;$GLOBALS['option_writes']++;return true;}
function get_posts($args){
  $out=array();
  foreach($GLOBALS['campaigns'] as $id=>$campaign){
    $key=(string)($args['meta_key']??'');
    $value=$args['meta_value']??null;
    if($key!==''&&($GLOBALS['postmeta'][$id][$key]??null)!==$value){continue;}
    $out[]=$id;
  }
  return isset($args['posts_per_page'])&&$args['posts_per_page']===1?array_slice($out,0,1):$out;
}
function get_post($id){return (object)array('ID'=>$id);}
function get_post_meta($id,$key,$single=true){return $GLOBALS['postmeta'][$id][$key]??'';}
function update_post_meta($id,$key,$value){$GLOBALS['postmeta'][$id][$key]=$value;}
function delete_post_meta($id,$key){unset($GLOBALS['postmeta'][$id][$key]);}
function add_post_meta($id,$key,$value,$unique=false){$GLOBALS['postmeta'][$id][$key]=$value;}

class TestDB {
 public $last_error='',$mode='', $products=array(), $next=1,$write_count=0;
 function prepare($sql,...$args){return vsprintf(str_replace(array('%s','%d'),array("'%s'",'%d'),$sql),$args);}
 function get_row($sql,$fmt=null){
   preg_match("/external_key='([^']+)'/",$sql,$m);$key=$m[1]??'';
   foreach($this->products as $p)if(($p['external_key']??'')===$key)return array('id'=>$p['id'],'source_hash'=>$p['source_hash'],'first_seen'=>$p['first_seen']);
   return null;
 }
 function insert($table,$row){
   $this->write_count++;
   if($this->mode==='write'){$this->last_error='Simulated failed INSERT';return false;}
   $this->last_error='';$id=$this->next++;$row['id']=$id;$this->products[$id]=$row;return 1;
 }
 function update($table,$data,$where){
   $this->write_count++;
   if($this->mode==='write'){$this->last_error='Simulated failed UPDATE';return false;}
   $this->last_error='';$id=(int)($where['id']??0);
   if(!isset($this->products[$id]))return false;
   $this->products[$id]=array_merge($this->products[$id],$data);return 1;
 }
 function get_results($sql,$fmt=null){
   if($this->mode==='read'){$this->last_error='Simulated failed SELECT';return null;}
   $this->last_error='';
   $start=0;if(preg_match('/last_seen >= (\d+)/',$sql,$m))$start=(int)$m[1];
   return array_values(array_filter($this->products,static function($p)use($start){return $p['network']==='idealo'&&$p['quality_status']==='pass'&&(int)$p['last_seen']>=$start;}));
 }
}
$GLOBALS['wpdb']=new TestDB();
$GLOBALS['options']=array();
$GLOBALS['option_writes']=0;
$GLOBALS['postmeta']=array();
$GLOBALS['campaigns']=array();
$GLOBALS['provider_updates']=0;$GLOBALS['sync_calls']=0;

class OriginalIdealoPipeline {
 const OPTION_NETWORK_IDEALO='idealo_settings_test';
 const CAMPAIGN_POST_TYPE='campaign';
 function __construct(){
   $GLOBALS['options'][self::OPTION_NETWORK_IDEALO]=array(
     'enabled'=>true,'api_key'=>'dummy','adspace_id'=>'568912','feed_id'=>'2747',
     'hobby_feed_verified'=>true,'api_last_checked_at'=>time(),
     'output_mode'=>'automatic','link_strategy'=>'products','api_last_advertiser_id'=>'84749',
     'last_import_at'=>0,'last_import_started_at'=>0,'last_import_feed_id'=>'',
     'last_import_adspace_id'=>'','last_match_revision'=>'');
 }
 private function idealo_settings(){return $GLOBALS['options'][self::OPTION_NETWORK_IDEALO];}
 private function idealo_credentials_present($s){return !empty($s['api_key'])&&!empty($s['hobby_feed_verified']);}
 private function idealo_sanitize_output_mode($s){return (string)$s;}
 private function idealo_portal_supply_catalog(){return array('_idealo_required_concepts'=>array());}
 private function idealo_match_index(){return array('concepts'=>array('concept-airbrush'=>array('id'=>'concept-airbrush','title'=>'Airbrush','main_hub'=>'Gestalten','hub'=>'Airbrush','target_pages'=>array(array('slug'=>'airbrush','main_slug'=>'gestalten','hub_slug'=>'airbrush')))));}
 private function idealo_match_feed_row_to_concept($r){
   // The original matcher has already been executed separately with real HD007
   // data; this fixture tests staging and materialization, not a second decision.
   if(strpos((string)($r['product_title']??''),'Airbrush')===false)return array('status'=>'none');
   return array('status'=>'matched','score'=>250,'context'=>2,'concept'=>array('id'=>'concept-airbrush','title'=>'Airbrush','main_hub'=>'Gestalten','hub'=>'Airbrush'));
 }
 private function idealo_open_feed_stream($path){return fopen($path,'rb');}
 private function idealo_stream_close($stream){fclose($stream);}
 private function idealo_direct_image_url($x){return strpos((string)$x,'https://cdn.idealo.com/')===0?(string)$x:'';}
 private function idealo_normalize_gtins_from_values($v){
   $a=array();foreach((array)$v as $z)foreach(preg_split('/[^0-9]+/',(string)$z) as $piece)
   if(in_array(strlen($piece),array(8,12,13,14),true))$a['g:'.$piece]=$piece;
   return array_values($a);
 }
 private function idealo_normalize_asins_from_values($v){return array();}
 private function network_sync_table($kind){return 'hd_test_'.$kind;}
 private function network_sync_mapped_value($row,$map,$key){$v=$map[$key]['source']??'';return (string)($row[$v]??'');}
 private function network_sync_quality_status($title,$tracking,$destination,$image){return $title!==''&&$tracking!==''&&$image!==''?'pass':'fail';}
 private function idealo_target_keys_for_product_slug($slug){return array('page:'.sanitize_title($slug));}
 private function idealo_comparison_deeplink_from_product_url($url,$concept){return (string)$url;}
 private function idealo_link_strategy(){return 'products';}
 private function central_blank_campaign(){return array();}
 private function save_campaign_record($campaign,$post_id=0){
   $id=absint($post_id);if(!$id)$id=count($GLOBALS['campaigns'])+1;
   $campaign['post_id']=$id;$GLOBALS['campaigns'][$id]=$campaign;return $id;
 }
 private function campaign_from_post($post){return $GLOBALS['campaigns'][$post->ID]??null;}
 private function idealo_sync_campaign_activation(){$GLOBALS['sync_calls']++;}
 private function provider_set_access_state($provider,$state,$msg){$GLOBALS['provider_updates']++;}
__ORIGINAL_METHODS__
 public function import($path){return $this->idealo_import_feed_file($path,'Synthetic feed');}
 public function materialize(){return $this->idealo_materialize_campaigns();}
}
function ck($yes,$label){static $i=0;$i++;if(!$yes){fwrite(STDERR,"FAIL $i: $label\n");exit(1);}echo "PASS $i: $label\n";}
$p=new OriginalIdealoPipeline();
$csv=tempnam(sys_get_temp_dir(),'hd009-case');
$headers=array('id','product_title','product_deeplink','ean','gtins_product','asins_product','main_category','sub_category','brand_name','image_url');
function makefile($file,$headers,$items){
  $f=fopen($file,'wb');fputcsv($f,$headers);
  foreach($items as $item)fputcsv($f,array_map(static function($col)use($item){return $item[$col]??'';},$headers));
  fclose($f);
}
$good=array(
 'id'=>'a','product_title'=>'Airbrush Pistole 0.3 mm',
 'product_deeplink'=>'https://ipn.idealo.de/click?test=1',
 'ean'=>'4006381333931','main_category'=>'Malen','sub_category'=>'Airbrush',
 'brand_name'=>'ACME','image_url'=>'https://cdn.idealo.com/a.jpg');
makefile($csv,$headers,array($good));
$state=$GLOBALS['options'][OriginalIdealoPipeline::OPTION_NETWORK_IDEALO];
$GLOBALS['wpdb']->mode='write';
$r=$p->import($csv);
ck(is_wp_error($r)&&$r->get_error_code()==='idealo_staging_write_failed','Failed DB INSERT must fail at its single write owner');
ck($GLOBALS['options'][OriginalIdealoPipeline::OPTION_NETWORK_IDEALO]===$state,'Failed DB stage never changes import revision, feed or activation');
ck(count($GLOBALS['campaigns'])===0&&$GLOBALS['provider_updates']===0,'Failed storage never calls downstream materialization');
$GLOBALS['wpdb']->mode='read';
$r=$p->materialize();
ck(is_wp_error($r)&&$r->get_error_code()==='idealo_staging_read_failed','DB SELECT error must not masquerade as zero products');
ck(count($GLOBALS['campaigns'])===0,'Failed DB read must not delete existing product cards');
$GLOBALS['wpdb']->mode='';
$r=$p->import($csv);
ck(!is_wp_error($r)&&($r['status']??'')==='success','Original feed importer finishes successfully with real DB writes');
ck(($r['details']['matching_rows']??0)===1,'Exactly one accepted source row reaches the storage owner');
ck(count($GLOBALS['campaigns'])===2,'Original materializer generates a family comparison and one GTIN product card');
ck(($GLOBALS['options'][OriginalIdealoPipeline::OPTION_NETWORK_IDEALO]['last_match_revision']??'')==='hd009-match-0.1.41','Matcher contract revised exactly once after staging');
$found=false;
foreach($GLOBALS['campaigns'] as $c)if(($c['source']??'')==='idealo_product_feed_v1'){
 $found=($c['active']??false)===true
  && in_array('page:airbrush',$c['automation_target_keys']??array(),true)
  && ($c['product_gtins'][0]??'')==='4006381333931'
  && ($c['image_url']??'')==='https://cdn.idealo.com/a.jpg';
}
ck($found,'Stored original campaign keeps the one imported hobby target, real image and GTIN');
unlink($csv);
echo "ONE_DECISION_TO_STORED_CARD_ORIGINAL_PHP_PIPELINE_PASS\n";
'''.replace('__ORIGINAL_METHODS__',source)
dest=Path(sys.argv[2]);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(php)
print('ORIGINAL_PHP_METHOD_COUNT',len(names)+1,'SIZE',len(php))
