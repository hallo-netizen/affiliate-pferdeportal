<?php
error_reporting(E_ALL);
define('ABSPATH','/');define('DAY_IN_SECONDS',86400);define('HOUR_IN_SECONDS',3600);
$GLOBALS['opts']=[];$GLOBALS['hooks']=[];$GLOBALS['calls']=[];$GLOBALS['transients']=[];
function get_option($k,$d=array()){return $GLOBALS['opts'][$k]??$d;}
function update_option($k,$v,$autoload=false){$GLOBALS['opts'][$k]=$v;return true;}
function sanitize_key($v){return strtolower(preg_replace('/[^a-z0-9_\-]/','',(string)$v));}
function sanitize_text_field($v){return strip_tags((string)$v);}
function esc_url($v){return htmlspecialchars((string)$v,ENT_QUOTES,'UTF-8');}
function esc_html($v){return htmlspecialchars((string)$v,ENT_QUOTES,'UTF-8');}
function absint($v){return abs((int)$v);}
function wp_parse_url($v,$part){return parse_url($v,$part);}
function wp_json_encode($v){return json_encode($v);}
function get_posts($args){return [];} // no eBay/idealo, real first-run situation
function get_transient($k){return $GLOBALS['transients'][$k]??false;}
function set_transient($k,$v,$ttl){$GLOBALS['transients'][$k]=$v;}
function delete_transient($k){unset($GLOBALS['transients'][$k]);}
function is_wp_error($v){return $v instanceof WP_Error;}
function add_action($hook,$cb,$priority=10){$GLOBALS['hooks'][]=$hook;}
function wp_remote_request($url,$args){
 $GLOBALS['calls'][]=['url'=>$url,'args'=>$args];
 if(str_contains($url,'task_post')){
  $request=json_decode($args['body'],true);
  if(empty($request[0]['keyword']) || $request[0]['se_domain']!=='amazon.de') return ['code'=>400,'body'=>'{}'];
  return ['code'=>200,'body'=>json_encode(['status_code'=>20000,'tasks'=>[['status_code'=>20100,'id'=>'12345678-1234-1234-1234-123456789abc']]])];
 }
 return ['code'=>200,'body'=>json_encode(['status_code'=>20000,'tasks'=>[['status_code'=>20000,'result'=>[['items'=>[
  ['type'=>'amazon_paid','url'=>'https://www.amazon.de/dp/B012345678','title'=>'Wassermelder Werbung','data_asin'=>'B012345678','image_url'=>'https://external/img.jpg','price_from'=>29],
  ['type'=>'amazon_serp','url'=>'https://www.amazon.de/dp/B011111111','title'=>'Wassermelder Smart Funk Sensor','data_asin'=>'B011111111','image_url'=>'https://external/img2.jpg','price_from'=>20],
  ['type'=>'amazon_serp','url'=>'https://www.amazon.de/dp/B011111111','title'=>'Wassermelder Smart Funk Sensor','data_asin'=>'B011111111'],
  ['type'=>'amazon_serp','url'=>'https://www.amazon.de/dp/B022222222','title'=>'Wassermelder Kabel Alarm','data_asin'=>'B022222222'],
  ['type'=>'amazon_serp','url'=>'https://www.amazon.com/dp/B033333333','title'=>'Wassermelder Fremdmarkt','data_asin'=>'B033333333'],
  ['type'=>'amazon_serp','url'=>'https://www.amazon.de/dp/B044444444','title'=>'Frostwächter Smart','data_asin'=>'B044444444'],
 ]]]]]])];
}
function wp_remote_retrieve_response_code($r){return $r['code'];}
function wp_remote_retrieve_body($r){return $r['body'];}
class WP_Error {private $message;function __construct($a,$b){$this->message=$b;}function get_error_message(){return $this->message;}}
class PPAR_Portal_Source {public static $catalog=['product_targets'=>[['title'=>'Wassermelder','category_slug'=>'wassermelder'],['title'=>'Rauchmelder','category_slug'=>'rauchmelder']]];public static function catalog(){return self::$catalog;}}
require dirname(__DIR__).'/affiliate-portal-router/includes/trait-ppar-hb-amazon.php';
class TestAmazon {use PPAR_HB_Amazon_Trait;const CAMPAIGN_POST_TYPE='ap_campaign';
 public function campaign_from_post($p){return null;}
 public function go(){return $this->hb_amazon_dfs_tick();}
 public function fallback($ctx,$slot){return $this->hb_amazon_category_search_fallback($ctx,$slot);}
 public function select($family,$items){return $this->hb_amazon_category_results($family,$items);}
}
function ok($v,$msg){if(!$v){echo "FAIL $msg\n";exit(1);}echo "PASS $msg\n";}
$t=new TestAmazon();$t->hb_amazon_register_hooks();
ok(in_array('admin_post_ppar_hb_amazon_run',$GLOBALS['hooks'],true),'Manual test button action registered');
ok(in_array('ppar_hab_amazon_dfs_tick_v1',$GLOBALS['hooks'],true),'Existing cron action preserved');
$GLOBALS['opts'][TestAmazon::HB_AMAZON_OPTION]=['enabled'=>true,'tag'=>'habundbewahr-21','dfs_enabled'=>true,'login'=>'test','password'=>'pass'];
$t->go();$c=get_option(TestAmazon::HB_AMAZON_CONTROL);
ok(count($GLOBALS['calls'])===1 && str_contains($GLOBALS['calls'][0]['url'],'task_post'),'Zero campaign candidate triggers 1 paid POST');
ok(json_decode($GLOBALS['calls'][0]['args']['body'],true)[0]['keyword']==='Wassermelder','Query from own portal category family');
ok(!empty($c['pending_id']) && $c['pending_source']==='hab_category','Single pending category task');
ok($c['count']===1 && !empty($c['last_tick_at']),'Cost count reserved and run timestamp recorded');
$t->go();$c=get_option(TestAmazon::HB_AMAZON_CONTROL);
ok(count($GLOBALS['calls'])===2 && empty($c['pending_id']),'Existing GET worker completes category task');
ok($c['count']===1,'GET does not cost a second POST');
ok(count($c['category_products']['wassermelder']['items'])===2,'2 distinct valid organic links stored');
ok(!isset($c['category_products']['rauchmelder']),'No cross-category findings');
$ctx=['post_type'=>'category_archive','primary_slug'=>'wassermelder','primary_name'=>'Wassermelder','product_family_slug'=>'wasserschutz'];
$html=$t->fallback($ctx,'product_after_category_tiles');
ok(str_contains($html,'/dp/B011111111?tag=habundbewahr-21'),'First genuine direct link attributed');
ok(str_contains($html,'/dp/B022222222?tag=habundbewahr-21'),'Second genuine direct link attributed');
ok(!str_contains($html,'B012345678') && !str_contains($html,'B033333333'),'Paid/foreign results excluded');
ok(!str_contains($html,'price') && !str_contains($html,'img'),'No prices, images or stock claims');
ok(str_contains($html,'Anzeige') && str_contains($html,'rel="sponsored nofollow noopener noreferrer"'),'Disclosure and sponsored attribution');
ok($t->fallback(['post_type'=>'page','primary_slug'=>'wassermelder','primary_name'=>'Wassermelder','product_family_slug'=>'wasserschutz'],'product_after_category_tiles')==='','No search on arbitrary page');
$t->go();$c=get_option(TestAmazon::HB_AMAZON_CONTROL);
ok(count($GLOBALS['calls'])===3 && json_decode($GLOBALS['calls'][2]['args']['body'],true)[0]['keyword']==='Rauchmelder','Next independent real category candidate without duplicate Wassermelder');
$t->go();$c=get_option(TestAmazon::HB_AMAZON_CONTROL);
ok($c['count']===2,'Two paid tasks only after independent categories');
$GLOBALS['opts'][TestAmazon::HB_AMAZON_CONTROL]=['count'=>5,'day'=>gmdate('Y-m-d')];$before=count($GLOBALS['calls']);$t->go();
ok(count($GLOBALS['calls'])===$before,'Daily cap 5 blocks further paid calls');
$GLOBALS['opts'][TestAmazon::HB_AMAZON_OPTION]['dfs_enabled']=false;$t->go();
ok(count($GLOBALS['calls'])===$before,'Disabled worker cannot pay');
$GLOBALS['opts'][TestAmazon::HB_AMAZON_OPTION]['dfs_enabled']=true;$GLOBALS['opts'][TestAmazon::HB_AMAZON_OPTION]['tag']='pferdeatelier-21';$t->go();
ok(count($GLOBALS['calls'])===$before,'Foreign Amazon ID does not enable worker');
$wrong=$t->select('Wassermelder',[['type'=>'amazon_serp','url'=>'https://www.amazon.de/dp/B055555555','title'=>'Rauchmelder Produkt','data_asin'=>'B055555555']]);
ok(count($wrong)===0,'Wrong product family rejected');
$invalid=$t->select('Wassermelder',[['type'=>'amazon_serp','url'=>'https://www.amazon.de/dp/B055555555','title'=>'Wassermelder Produkt','data_asin'=>'INVALID']]);
ok(count($invalid)===0,'Invalid ASIN rejected');
echo "ALL RC6 TESTS PASS\n";