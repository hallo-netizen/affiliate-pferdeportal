<?php
error_reporting(E_ALL);
define('ABSPATH','/');define('DAY_IN_SECONDS',86400);define('HOUR_IN_SECONDS',3600);
$GLOBALS['options']=[];$GLOBALS['meta']=[];$GLOBALS['posts']=[];$GLOBALS['post_save']=[];$GLOBALS['http_mode']='post';$GLOBALS['calls']=0;
function get_option($k,$d=null){return $GLOBALS['options'][$k]??$d;}
function update_option($k,$v,$autoload=false){$GLOBALS['options'][$k]=$v;return true;}
function sanitize_key($k){return strtolower(preg_replace('/[^a-z0-9_-]/','',(string)$k));}
function absint($v){return abs((int)$v);}
function get_post_meta($id,$key,$single=false){return $GLOBALS['meta'][$id][$key]??null;}
function update_post_meta($id,$key,$value){$GLOBALS['meta'][$id][$key]=$value;return true;}
function wp_parse_url($url,$part){return parse_url($url,$part);}
function get_post($id){return $GLOBALS['posts'][$id]??null;}
function get_posts($args){$all=array_values($GLOBALS['posts']);$offset=$args['offset']??0;return array_slice($all,$offset,$args['posts_per_page']??100);}
function get_transient($k){return $GLOBALS['transient'][$k]??false;}
function set_transient($k,$v,$e){$GLOBALS['transient'][$k]=$v;}
function delete_transient($k){unset($GLOBALS['transient'][$k]);}
function wp_json_encode($v){return json_encode($v);}
function wp_remote_request($url,$args){$GLOBALS['calls']++;if(strpos($url,'task_post')!==false){return ['code'=>200,'body'=>json_encode(['status_code'=>20000,'tasks'=>[['status_code'=>20100,'id'=>'12345678-1234-1234-1234-123456789abc']]])];}return ['code'=>200,'body'=>json_encode(['status_code'=>20000,'tasks'=>[['status_code'=>20000,'result'=>[['items'=>[['type'=>'amazon_serp','url'=>'https://www.amazon.de/dp/B012345678?th=1','title'=>'Sicherheitskamera Muster Modell 420']]]]]]])];}
function wp_remote_retrieve_response_code($r){return $r['code'];}
function wp_remote_retrieve_body($r){return $r['body'];}
function is_wp_error($r){return $r instanceof WP_Error;}
class WP_Error {private $s;function __construct($a,$s){$this->s=$s;}function get_error_message(){return $this->s;}}
require dirname(__DIR__).'/affiliate-portal-router/includes/trait-ppar-hb-amazon.php';
class Tester {use PPAR_HB_Amazon_Trait;const CAMPAIGN_POST_TYPE='ap_campaign';function campaign_from_post($p){return $GLOBALS['post_save'][$p->ID]??null;}function save_campaign_record($r,$id){$GLOBALS['post_save'][$id]=$r;return $id;}function link($a,$s=null){return $this->hb_amazon_direct_url($a,$s);}function offer($o,$c){return $this->hb_amazon_add_offer($o,$c,[], 'category_product_1');}function matching($t,$arr){return $this->hb_amazon_exact_match_asin($t,$arr);}function ready(){return $this->hb_amazon_dfs_ready();}}
function check($yes,$name){if(!$yes){echo 'FAIL '.$name.PHP_EOL;exit(1);}echo 'PASS '.$name.PHP_EOL;}
$x=new Tester();
check($x->link('B012345678')==='','disabled default prevents link');
$GLOBALS['options'][Tester::HB_AMAZON_OPTION]=['enabled'=>true,'tag'=>'pferdeatelier-21','dfs_enabled'=>true,'login'=>'test','password'=>'pass'];
check($x->link('B012345678')==='','foreign portal tracking tag forbidden');
$GLOBALS['options'][Tester::HB_AMAZON_OPTION]['tag']='habundbewahr-21';
check($x->link('B012345678')==='https://www.amazon.de/dp/B012345678?tag=habundbewahr-21','correct exact tag');
check($x->link('x')==='','invalid ASIN blocked');
$base=[['network'=>'idealo','url'=>'https://ipn.idealo.de','label'=>'Bei idealo vergleichen']];
$c=['active'=>true,'creative_type'=>'product','network'=>'idealo','source'=>'idealo_product_feed_v1','product_identity_source'=>'gtin','product_gtins'=>['1234567890123'],'product_asins'=>['B012345678']];
$offers=$x->offer($base,$c);
check(count($offers)===2 && $offers[1]['network']==='amazon','auto Amazon add to verified idealo product');
check(count($x->offer($offers,$c))===2,'no duplicate Amazon button');
$c['product_asins']=['B012345678','B076543210'];check(count($x->offer($base,$c))===1,'ambiguous ASIN rejected');
$c['product_asins']=['B012345678'];$c['source']='unverified';check(count($x->offer($base,$c))===1,'wrong source rejected');
$c['source']='output_object_v4';$c['network']='ebay';$c['post_id']=42;
check(count($x->offer($base,$c))===1,'unverified eBay ASIN rejected');
$one=[['type'=>'amazon_serp','url'=>'https://www.amazon.de/dp/B012345678','title'=>'Sicherheitskamera Muster Modell 420']];
check($x->matching('Sicherheitskamera Muster Modell 420',$one)==='B012345678','exact DataForSEO title accepted');
check($x->matching('Sicherheitskamera Muster Modell 420',array_merge($one,[['type'=>'amazon_serp','url'=>'https://www.amazon.de/dp/B076543210','title'=>'Sicherheitskamera Muster Modell 420']]))==='','ambiguous matches rejected');
check($x->matching('Sicherheitskamera Muster Modell 420',[['type'=>'amazon_serp','url'=>'https://www.amazon.de/dp/B012345678','title'=>'Sicherheitskamera Muster Modell 420 Lite']])==='','variant Lite rejected');
check($x->matching('Sicherheitskamera Muster Modell 420',[['type'=>'amazon_serp','url'=>'https://www.amazon.com/dp/B012345678','title'=>'Sicherheitskamera Muster Modell 420']])==='','foreign domain rejected');
check($x->matching('Sicherheitskamera Muster Modell 420',[['type'=>'amazon_paid','url'=>'https://www.amazon.de/dp/B012345678','title'=>'Sicherheitskamera Muster Modell 420']])==='','paid ad results rejected');
$GLOBALS['posts'][42]=(object)['ID'=>42];$GLOBALS['post_save'][42]=['post_id'=>42,'active'=>true,'creative_type'=>'product','network'=>'ebay','source'=>'output_object_v4','product_gtins'=>['1234567890123'],'product_asins'=>[],'title'=>'Sicherheitskamera Muster Modell 420'];
check($x->ready(),'DataForSEO settings ready');
$x->hb_amazon_dfs_tick();$state=get_option(Tester::HB_AMAZON_CONTROL);check($GLOBALS['calls']===1 && !empty($state['pending_id']) && (int)$state['count']===1,'one paid POST and pending state');
$x->hb_amazon_dfs_tick();$state=get_option(Tester::HB_AMAZON_CONTROL);check($GLOBALS['calls']===2 && empty($state['pending_id']) && (int)$state['count']===1,'GET reuses task at no additional paid POST');
check($GLOBALS['post_save'][42]['product_asins']===['B012345678'] && !empty($state['last_match_at']),'verified ASIN stored in existing campaign');
check(count($x->offer($base,$GLOBALS['post_save'][42]))===2,'DataForSEO match activates existing product card');
$x->hb_amazon_dfs_tick();check($GLOBALS['calls']===2,'verified campaign not researched twice');
$GLOBALS['options'][Tester::HB_AMAZON_OPTION]['dfs_enabled']=false;$x->hb_amazon_dfs_tick();check($GLOBALS['calls']===2,'disabled DFS cannot pay');
$GLOBALS['options'][Tester::HB_AMAZON_OPTION]['dfs_enabled']=true;
$GLOBALS['options'][Tester::HB_AMAZON_CONTROL]=['day'=>gmdate('Y-m-d'),'count'=>5,'checked'=>[]];
$x->hb_amazon_dfs_tick();check($GLOBALS['calls']===2,'daily paid search cap');
check(empty($GLOBALS['transient']),'lock released');
echo 'ALL TESTS PASS'.PHP_EOL;