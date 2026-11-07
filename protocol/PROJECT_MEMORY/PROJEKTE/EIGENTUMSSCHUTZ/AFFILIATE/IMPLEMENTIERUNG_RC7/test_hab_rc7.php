<?php
error_reporting(E_ALL); define('ABSPATH','/'); define('DAY_IN_SECONDS',86400); define('HOUR_IN_SECONDS',3600);
$GLOBALS['opts']=[];$GLOBALS['calls']=[];$GLOBALS['transients']=[];$GLOBALS['posts']=[];$GLOBALS['post_cats']=[];$GLOBALS['post_meta']=[];
function ok($v,$msg){if(!$v){echo "FAIL $msg\n";exit(1);} echo "PASS $msg\n";}
function get_option($k,$d=array()){return $GLOBALS['opts'][$k]??$d;}
function update_option($k,$v,$autoload=false){$GLOBALS['opts'][$k]=$v;return true;}
function absint($v){return abs((int)$v);}function sanitize_key($v){return strtolower(preg_replace('/[^a-z0-9_\-]/','',(string)$v));}
function sanitize_text_field($v){return strip_tags((string)$v);}
function esc_url($v){return htmlspecialchars((string)$v,ENT_QUOTES,'UTF-8');}function esc_html($v){return htmlspecialchars((string)$v,ENT_QUOTES,'UTF-8');}
function wp_parse_url($v,$part){return parse_url($v,$part);}function wp_json_encode($v){return json_encode($v);}
function get_post($id){return $GLOBALS['posts'][$id]??null;}
function get_post_status($id){return get_post($id)->post_status ?? '';}
function get_post_type($id){return get_post($id)->post_type ?? '';}
function get_post_meta($id,$key,$single=true){return $GLOBALS['post_meta'][$id][$key]??'';}
function get_the_terms($id,$tax){return array_map(static function($s){return (object)['slug'=>$s];},$GLOBALS['post_cats'][$id]??[]);}
function get_posts($args){
 $items=array_filter($GLOBALS['posts'],static function($p)use($args){return $p->post_type===($args['post_type']??'post') && $p->post_status===($args['post_status']??'publish');});
 ksort($items);return array_slice(array_values($items),(int)($args['offset']??0),(int)($args['posts_per_page']??100));
}
function get_transient($k){return $GLOBALS['transients'][$k]??false;}function set_transient($k,$v,$ttl){$GLOBALS['transients'][$k]=$v;}function delete_transient($k){unset($GLOBALS['transients'][$k]);}
function is_wp_error($v){return $v instanceof WP_Error;}
function wp_remote_request($url,$args){
 $GLOBALS['calls'][]=['url'=>$url,'args'=>$args];
 if(str_contains($url,'task_post')){
   return ['code'=>200,'body'=>json_encode(['status_code'=>20000,'tasks'=>[['status_code'=>20100,'id'=>'12345678-1234-1234-1234-123456789abc']]])];
 }
 return ['code'=>200,'body'=>json_encode(['status_code'=>20000,'tasks'=>[['status_code'=>20000,'result'=>[['items'=>[
   ['type'=>'amazon_serp','url'=>'https://www.amazon.de/dp/B011111111','title'=>'Wassermelder Smart Funk Sensor','data_asin'=>'B011111111'],
   ['type'=>'amazon_serp','url'=>'https://www.amazon.de/dp/B022222222','title'=>'Wassermelder ohne WLAN Sensor','data_asin'=>'B022222222'],
   ['type'=>'amazon_serp','url'=>'https://www.amazon.de/dp/B033333333','title'=>'Rauchmelder Smart Funk','data_asin'=>'B033333333'],
   ['type'=>'amazon_paid','url'=>'https://www.amazon.de/dp/B044444444','title'=>'Wassermelder Smart Anzeigen','data_asin'=>'B044444444'],
   ['type'=>'amazon_serp','url'=>'https://www.amazon.com/dp/B055555555','title'=>'Wassermelder Smart Foreign','data_asin'=>'B055555555']
 ]]]]]])];
}
function wp_remote_retrieve_response_code($r){return $r['code'];}function wp_remote_retrieve_body($r){return $r['body'];}
class WP_Error {private $message;function __construct($a,$b){$this->message=$b;}function get_error_message(){return $this->message;}}
class PPAR_Portal_Source {
 public static $catalog=['product_targets'=>[['title'=>'Wassermelder','category_slug'=>'wassermelder'],['title'=>'Rauchmelder','category_slug'=>'rauchmelder']]];
 public static function catalog(){return self::$catalog;}
}
require dirname(__DIR__).'/affiliate-portal-router/includes/trait-ppar-hb-amazon.php';
class TestAmazon {use PPAR_HB_Amazon_Trait;const CAMPAIGN_POST_TYPE='ap_campaign';
 public function campaign_from_post($p){return null;}
 public function go(){return $this->hb_amazon_dfs_tick();}
 public function candidate(&$control){return $this->hb_amazon_article_candidate($control);}
 public function topic($p){return $this->hb_amazon_article_topic($p);}
 public function offers($post_id){return $this->hb_amazon_article_fallback($post_id);}
 public function filter($topic,$items){return $this->hb_amazon_article_results($topic,$items);}
}
function put($id,$title,$status='publish',$categories=['wassermelder']){
 $GLOBALS['posts'][$id]=(object)['ID'=>$id,'post_type'=>'post','post_status'=>$status,'post_title'=>$title,'post_content'=>'Testinhalt'];
 $GLOBALS['post_cats'][$id]=$categories;
}
$t=new TestAmazon();
$GLOBALS['opts'][TestAmazon::HB_AMAZON_OPTION]=['enabled'=>true,'tag'=>'habundbewahr-21','dfs_enabled'=>true,'login'=>'test','password'=>'pass'];
put(101,'Wassermelder Smart im Keller');put(102,'Wassermelder ohne WLAN','draft');put(103,'Haus vor Einbruch schützen');put(104,'Wassermelder Smart Auswahl','publish',['andere']);
$state=[];$c=$t->candidate($state);
ok(is_array($c)&&$c['id']===101&&$c['source']==='hab_article','published matching article automatically eligible');
ok($c['category_slug']==='wassermelder'&&str_contains($c['title'],'Wassermelder'),'real portal family plus article title selected');
ok($t->topic(get_post(102))===null,'draft excluded');
ok($t->topic(get_post(103))===null,'generic advice without product name excluded');
ok($t->topic(get_post(104))===null,'product title with unrelated category excluded');
$GLOBALS['post_meta'][101]['_hbdp_article_no_ads']='1';ok($t->topic(get_post(101))===null,'ad-free post excluded');unset($GLOBALS['post_meta'][101]);
$GLOBALS['opts'][TestAmazon::HB_AMAZON_OPTION]['enabled']=false;ok($t->offers(101)==='','disabled Amazon renders nothing');
$GLOBALS['opts'][TestAmazon::HB_AMAZON_OPTION]['enabled']=true;
ok(str_contains($t->offers(101),'Passende Angebote bei Amazon suchen'),'published article gets fallback search before paid match');
ok(str_contains($t->offers(101),'habundbewahr-21')&&!str_contains($t->offers(101),'pferdeatelier-21'),'only Hab tracking on article');
$t->go();$s=get_option(TestAmazon::HB_AMAZON_CONTROL);
ok(count($GLOBALS['calls'])===1 && $s['pending_source']==='hab_article' && $s['pending_post_id']===101,'same existing worker launches article request');
ok(json_decode($GLOBALS['calls'][0]['args']['body'],true)[0]['keyword']==='Wassermelder Smart im Keller','search query depends on article title');
$t->go();$s=get_option(TestAmazon::HB_AMAZON_CONTROL);
ok($s['count']===1 && count($GLOBALS['calls'])===2,'GET result retrieval without another paid POST');
ok(count($s['article_products'][101]['items'])===1,'modifier Smart filters broad category results');
ok(str_contains($t->offers(101),'/dp/B011111111?tag=habundbewahr-21'),'stored article-only Amazon link appears');
ok(!str_contains($t->offers(101),'B022222222')&&!str_contains($t->offers(101),'B033333333'),'irrelevant variant and different product family excluded');
ok(str_contains($t->offers(101),'Anzeige')&&str_contains($t->offers(101),'sponsored nofollow'),'article link disclosed');
$seen=get_option(TestAmazon::HB_AMAZON_CONTROL);ok($t->candidate($seen)===null,'matched article not re-searched needlessly');
put(101,'Wassermelder ohne WLAN');$before=$t->offers(101);
ok(!str_contains($before,'/dp/B011111111'),'article title edit invalidates outdated links immediately');
$rec=$t->candidate($seen);ok($rec && $rec['id']===101 && $rec['hash']!==$c['hash'],'article edit schedules fresh search');
$t->go();$ss=get_option(TestAmazon::HB_AMAZON_CONTROL);ok($ss['count']===2,'changed article makes exactly one new paid POST');
$t->go();$ss=get_option(TestAmazon::HB_AMAZON_CONTROL);ok(count($ss['article_products'][101]['items'])===1,'article query without WLAN allows only matching without-WLAN product');
ok(str_contains($t->offers(101),'/dp/B022222222')&&!str_contains($t->offers(101),'/dp/B011111111'),'negative variant remains accurate');
put(101,'Wassermelder ohne WLAN','publish',['rauchmelder']);ok($t->topic(get_post(101))===null,'category change invalidates article relevance');
ok($t->offers(101)==='','category change removes affiliate fallback');
put(110,'Rauchmelder mit Batterie','publish',['rauchmelder']);
$ss=get_option(TestAmazon::HB_AMAZON_CONTROL);$pick=$t->candidate($ss);ok($pick && $pick['id']===110,'new published article discovered without new hooks');
$GLOBALS['opts'][TestAmazon::HB_AMAZON_CONTROL]['day']=gmdate('Y-m-d');$GLOBALS['opts'][TestAmazon::HB_AMAZON_CONTROL]['count']=5;
$before=count($GLOBALS['calls']);$t->go();ok(count($GLOBALS['calls'])===$before,'article research obeys original daily cap');
$GLOBALS['opts'][TestAmazon::HB_AMAZON_OPTION]['tag']='pferdeatelier-21';ok($t->offers(110)==='','foreign tracking ID suppresses output');

// Integrate against the REAL hab_bw_article_slot method extracted from the
// original Hab WordPress router, not a reimplemented copy.
$main=file_get_contents(dirname(__DIR__).'/affiliate-portal-router/affiliate-portal-router.php');
$start=strpos($main,'    public function hab_bw_article_slot($post_id, $kind) {');
$end=strpos($main,'    /** Reuse the existing campaign-selection engine',$start);
ok($start!==false&&$end>$start,'real article-slot implementation available for integration');
$method=substr($main,$start,$end-$start);
eval('class ArticleSlotTest { use PPAR_HB_Amazon_Trait;
 public function is_enabled(){return $GLOBALS["slot_enabled"] ?? true;}
 private function article_hybrid_enabled(){return $GLOBALS["slot_hybrid"] ?? true;}
 private function article_plan_get($post_id){return ["products"=>["status"=>$GLOBALS["slot_product_status"]??"none", "campaign_post_ids"=>[123]], "banner"=>["status"=>"none"]];}
 private function article_plan_is_current($post_id,$plan){return !($GLOBALS["slot_stale"]??false);}
 private function article_plan_render_products($post_id,$ids){return $GLOBALS["slot_product_html"]??"";}
 private function article_plan_render_banner_campaign($id,$cid){return "<div>Existing banner</div>";}
 private function render_affiliate_slot($a,$b,$c,$d){return $GLOBALS["slot_old_html"]??"<!-- no result -->";}
 '.$method.'}');
put(101,'Wassermelder Smart im Keller');
$GLOBALS['opts'][TestAmazon::HB_AMAZON_OPTION]['tag']='habundbewahr-21';
$GLOBALS['slot_hybrid']=true;$GLOBALS['slot_product_status']='none';$GLOBALS['slot_stale']=false;
$slot=new ArticleSlotTest();
ok(str_contains($slot->hab_bw_article_slot(101,'products'),'Passende Angebote bei Amazon suchen'),
    'existing article hybrid slot uses Amazon fallback only when no real product exists');
$GLOBALS['slot_product_status']='ready';$GLOBALS['slot_product_html']='<div>Original verified provider product</div>';
ok($slot->hab_bw_article_slot(101,'products')==='<div>Original verified provider product</div>',
    'original verified article product remains first priority');
$GLOBALS['slot_product_status']='none';$GLOBALS['slot_stale']=true;
ok($slot->hab_bw_article_slot(101,'products')==='','stale existing article plan remains blocked');
$GLOBALS['slot_stale']=false;$GLOBALS['slot_hybrid']=false;
$GLOBALS['slot_old_html']='<div>Existing nonhybrid ad</div>';
ok($slot->hab_bw_article_slot(101,'products')==='<div>Existing nonhybrid ad</div>',
    'existing nonhybrid campaign not overridden');
$GLOBALS['slot_old_html']='<!-- no result -->';
ok(str_contains($slot->hab_bw_article_slot(101,'products'),'Passende Angebote bei Amazon suchen'),
    'legacy selector uses same fallback when no real campaign exists');
$GLOBALS['slot_enabled']=false;
ok($slot->hab_bw_article_slot(101,'products')==='','global affiliate disabled remains disabled');

echo "ALL RC7 TESTS PASS\n";