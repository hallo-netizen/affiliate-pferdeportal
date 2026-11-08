#!/usr/bin/env python3
"""Execute actual HD009 0.1.31 PHP worker with WP API and DataForSEO fixtures.

No real credentials, no paid API, no frontend network, and no production changes.
Official HD007 and HD003 JSON files are used to exercise catalog eligibility.
"""
from pathlib import Path
from zipfile import ZipFile
from tempfile import TemporaryDirectory
import subprocess
r=Path('protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/PLUGINS/ISOLIERTE_PLUGINS')
with ZipFile(r/'HD-009-AFFILIATE-ZENTRALE/CURRENT.zip') as z:
    code=z.read('affiliate-portal-router/includes/class-hdar-amazon-start.php')
    version=z.read('affiliate-portal-router/hobby-depot-affiliate-router.php').decode()
    assert ' * Version: 0.1.31' in version[:350]
with ZipFile(r/'HD-007-HOBBYREGISTER-CORE/CURRENT.zip') as z:
    registry=z.read('hd-hobbyregister-core/data/hobby-register.json')
with ZipFile(r/'HD-003-DESIGN-TEMPLATE-KIT/CURRENT.zip') as z:
    leaf=z.read('affiliate-portal-template-kit/assets/hobby-depot-v150750/leaf-category-map-v150750.json')
stubs=r"""<?php
error_reporting(E_ALL);
define('ABSPATH','/tmp');
define('DAY_IN_SECONDS',86400);
define('HOUR_IN_SECONDS',3600);
define('WP_PLUGIN_DIR', __DIR__.'/plugins');
define('HDAR_DATAFORSEO_LOGIN','fake-only-login');
define('HDAR_DATAFORSEO_PASSWORD','fake-only-password');
class WP_Error {
    private $c,$msg;
    function __construct($code,$msg){$this->c=$code;$this->msg=$msg;}
    function get_error_message(){return $this->msg;}
}
class WP_Post {
    public $ID=123,$post_name='zweileiner-vierleiner',$post_title='Zweileiner oder Vierleiner – welcher Lenkdrachen passt zu dir?',
        $post_status='publish',$post_type='post';
}
class WP_Term {
    public $slug='sportdrachen-drachen-leinen',$term_id=17,$name='Drachen & Leinen';
}
$GLOBALS['opts']=array('ppar_amazon_search_v1'=>array('tracking_id'=>'example-21'));
$GLOBALS['transients']=array();
$GLOBALS['requests']=array();
$GLOBALS['response_mode']='happy';
$GLOBALS['posts']=array(new WP_Post);
$GLOBALS['categories']=array(new WP_Term);
$GLOBALS['test_now']=null;
function get_option($name,$default=null){return $GLOBALS['opts'][$name]??$default;}
function update_option($name,$val,$autoload=false){$GLOBALS['opts'][$name]=$val;return true;}
function get_transient($key){return $GLOBALS['transients'][$key]??false;}
function set_transient($key,$val,$ttl){$GLOBALS['transients'][$key]=$val;return true;}
function delete_transient($key){unset($GLOBALS['transients'][$key]);return true;}
function sanitize_title($s){
    $s=strtolower(str_replace(array('Ä','Ö','Ü','ä','ö','ü','ß'),array('ae','oe','ue','ae','oe','ue','ss'),(string)$s));
    return trim(preg_replace('/[^a-z0-9]+/','-',$s),'-');
}
function sanitize_key($s){return strtolower(preg_replace('/[^a-zA-Z0-9_-]/','',(string)$s));}
function sanitize_text_field($s){return (string)$s;}
function is_wp_error($v){return $v instanceof WP_Error;}
function get_posts($args){return array_slice($GLOBALS['posts'],$args['offset']??0,$args['posts_per_page']??100);}
function get_post($id){return (int)$id===123?$GLOBALS['posts'][0]:null;}
function get_post_status($id){return 'publish';}
function get_the_title($id){return 'Zweileiner oder Vierleiner – welcher Lenkdrachen passt zu dir?';}
function get_permalink($id){return 'https://www.hobby-depot.de/designtest-zweileiner-oder-vierleiner-hobby-depot/';}
function get_the_terms($id,$tax){return $GLOBALS['categories'];}
function get_ancestors($id,$tax,$type){return array();}
function get_term($id,$tax){return null;}
function absint($v){return abs((int)$v);}
function wp_parse_url($url,$component=-1){return parse_url($url,$component);}
function wp_json_encode($v){return json_encode($v);}
function add_filter(...$a){return true;}
function add_action(...$a){return true;}
function add_shortcode(...$a){return true;}
function wp_next_scheduled($hook){return false;}
function wp_schedule_event(...$args){return true;}
function wp_clear_scheduled_hook($hook){return true;}
function wp_remote_request($url,$args){
    $GLOBALS['requests'][]=array('url'=>$url,'method'=>$args['method']);
    if ($GLOBALS['response_mode']==='error')return new WP_Error('remote','simulated outage');
    if ($args['method']==='POST') {
      return array('response_code'=>200,'body'=>json_encode(array(
       'status_code'=>20000,
       'tasks'=>array(array('status_code'=>20100,'id'=>'12345678-1234-1234-1234-123456789012')))));
    }
    return array('response_code'=>200,'body'=>json_encode(array(
      'status_code'=>20000,
      'tasks'=>array(array('status_code'=>20000,'result'=>array(array(
         'items'=>array(
           array('type'=>'amazon_serp','title'=>'HQ Lenkdrachen Einsteiger Modell',
             'data_asin'=>'B012345678','url'=>'https://www.amazon.de/dp/B012345678',
             'image_url'=>'https://example.org/not-authorized.jpg','price'=>44),
           array('type'=>'amazon_serp','title'=>'Drachen ohne passende Klasse',
             'data_asin'=>'B012345679','url'=>'https://www.amazon.de/dp/B012345679'),
           array('type'=>'amazon_serp','title'=>'Lenkdrachen falscher Anbieter',
             'data_asin'=>'B012345680','url'=>'https://www.ebay.de/itm/123')
         ))))))));
}
function wp_remote_retrieve_response_code($r){return $r['response_code'];}
function wp_remote_retrieve_body($r){return $r['body'];}
function is_admin(){return false;}
function is_feed(){return false;}
function is_singular($kind){return $kind==='post';}
function in_the_loop(){return true;}
function is_main_query(){return true;}
function get_the_ID(){return 123;}
function post_password_required($id){return false;}
function wp_attachment_is_image($id){return false;}
function esc_attr($v){return htmlspecialchars((string)$v,ENT_QUOTES);}
function esc_html($v){return htmlspecialchars((string)$v,ENT_QUOTES);}
function esc_url($v){return (string)$v;}
"""
tests=r"""
function invoke($method,...$args) {
    $m=new ReflectionMethod('HDAR_Amazon_Start',$method);
    return $m->invokeArgs(null,$args);
}
$mode=(new ReflectionClass('HDAR_Amazon_Start'))->getConstant('MODE_OPTION');
$GLOBALS['opts'][$mode]='amazon_idealo';
$auto=(new ReflectionClass('HDAR_Amazon_Start'))->getConstant('DFS_AUTO_OPTION');
$catalog=invoke('auto_hobby_catalog');
assert(is_array($catalog) && count($catalog)>=130 && count($catalog)<=381);
assert(isset($catalog['sportdrachen']) && $catalog['sportdrachen']['keyword']==='Lenkdrachen');
assert(isset($catalog['3d-druck']) && $catalog['3d-druck']['keyword']==='3D-Drucker');
assert(!isset($catalog['architekturmodellbau']),'generic carton should be blocked');
echo "REAL_862_REGISTER_381_HOBBY_PRECHECK_PASS ".count($catalog)."\n";

$candidate=invoke('auto_post_hobby',$GLOBALS['posts'][0],$catalog);
assert(is_array($candidate) && $candidate['id']===123 && $candidate['keyword']==='Lenkdrachen');
$GLOBALS['categories'][0]->slug='garten';
assert(invoke('auto_post_hobby',$GLOBALS['posts'][0],$catalog)===null);
$GLOBALS['categories'][0]->slug='sportdrachen-drachen-leinen';
echo "EXACT_HOBBY_CATEGORY_AND_TITLE_MATCH_PASS\n";

assert(invoke('auto_match_results','Lenkdrachen',array(
 array('type'=>'amazon_serp','title'=>'HQ Lenkdrachen Einsteiger','data_asin'=>'B012345678','url'=>'https://www.amazon.de/dp/B012345678'),
 array('type'=>'amazon_serp','title'=>'Lenkdrachen Ebay','data_asin'=>'B012345679','url'=>'https://www.ebay.de/itm/1'),
 array('type'=>'amazon_serp','title'=>'Drachen Maske','data_asin'=>'B012345680','url'=>'https://amazon.de/dp/B012345680'),
 array('type'=>'amazon_serp','title'=>'Lenkdrachen keine ASIN','data_asin'=>'wrong','url'=>'https://amazon.de/')
 ))===array(array('asin'=>'B012345678','title'=>'HQ Lenkdrachen Einsteiger','source'=>'dataforseo_hobby_auto_v1')));
echo "EXACT_AMAZON_DE_ASIN_TITLE_NO_IMAGE_COPY_PASS\n";

// Default disabled: one hourly tick must not incur any DataForSEO expense.
HDAR_Amazon_Start::auto_cron();
assert(count($GLOBALS['requests'])===0);
echo "DEFAULT_OFF_NO_NETWORK_PASS\n";

$state=invoke('auto_state');$state['enabled']=true;$state['status']='idle';
$GLOBALS['opts'][$auto]=$state;
HDAR_Amazon_Start::auto_cron();
assert(count($GLOBALS['requests'])===1 && $GLOBALS['requests'][0]['method']==='POST');
$state=invoke('auto_state');
assert($state['count']===1 && $state['status']==='pending' && !empty($state['pending']['id']));
assert(!isset($GLOBALS['opts'][(new ReflectionClass('HDAR_Amazon_Start'))->getConstant('PRODUCTS_OPTION')]));
echo "ONE_PAID_TASK_RESERVED_BEFORE_POST_PASS\n";

// Pending task: GET only, no second paid POST.
HDAR_Amazon_Start::auto_cron();
assert(count($GLOBALS['requests'])===2 && $GLOBALS['requests'][1]['method']==='GET');
$state=invoke('auto_state');
assert($state['count']===1 && $state['status']==='success' && empty($state['pending']));
$product_option=(new ReflectionClass('HDAR_Amazon_Start'))->getConstant('PRODUCTS_OPTION');
$stored=$GLOBALS['opts'][$product_option];
assert(count($stored['post:123']['items'])===1);
assert($stored['post:123']['items'][0]['asin']==='B012345678');
assert(!isset($stored['post:123']['items'][0]['image_url']));
assert(!isset($stored['post:123']['items'][0]['price']));
assert(strpos(HDAR_Amazon_Start::render_article_cards('<p>Text</p>'),'hdar-amazon-article-products')===false,
       'without licensed photo no deceptive product tile');
echo "FREE_POLL_AND_APPROVED_ASIN_SAVED_NO_IMAGE_NO_PUBLIC_CARD_PASS\n";

HDAR_Amazon_Start::auto_cron();
assert(count($GLOBALS['requests'])===2,'no repeated paid task for existing data');
echo "IDEMPOTENT_NO_DUPLICATE_PAID_TASK_PASS\n";

$state=invoke('auto_state');
$state['count']=5;$state['day']=gmdate('Y-m-d');
$state['scan_offset']=0;
$state['checked']=array();
$GLOBALS['opts'][$product_option]=array();$GLOBALS['opts'][$auto]=$state;
HDAR_Amazon_Start::auto_cron();
assert(count($GLOBALS['requests'])===2);
assert(invoke('auto_state')['status']==='limit');
echo "UTC_DAILY_BUDGET_FIVE_STRICT_PASS\n";

$state=invoke('auto_state');
$state['count']=0;$state['scan_offset']=0;$state['status']='idle';
$GLOBALS['opts'][$auto]=$state;
$GLOBALS['response_mode']='error';
HDAR_Amazon_Start::auto_cron();
$state=invoke('auto_state');
assert($state['enabled']===false && $state['status']==='error' && $state['count']===1,
    'reserve failed POST and disable to prevent repeated billing');
$before=count($GLOBALS['requests']);
HDAR_Amazon_Start::auto_cron();
assert(count($GLOBALS['requests'])===$before);
echo "ON_ERROR_STOP_AUTOMATIC_PAID_QUERIES_PASS\n";
"""
with TemporaryDirectory() as td:
    folder=Path(td)
    plugins=folder/'plugins'
    rpath=plugins/'hd-hobbyregister-core/data/hobby-register.json'
    rpath.parent.mkdir(parents=True);rpath.write_bytes(registry)
    mpath=plugins/'affiliate-portal-template-kit/assets/hobby-depot-v150750/leaf-category-map-v150750.json'
    mpath.parent.mkdir(parents=True);mpath.write_bytes(leaf)
    file=folder/'class-hdar-amazon-start.php'
    file.write_bytes(code)
    f=folder/'test.php'
    f.write_text(stubs+"\nrequire __DIR__.'/class-hdar-amazon-start.php';\n"+tests)
    lint=subprocess.run(['php','-l',str(f)],capture_output=True,text=True)
    assert lint.returncode==0,(lint.stdout,lint.stderr)
    test=subprocess.run(['php','-d','zend.assertions=1','-d','assert.exception=1',str(f)],
                        capture_output=True,text=True)
    assert test.returncode==0,(test.stdout,test.stderr)
    print(test.stdout.strip())
print("HD009_031_DFS_WORKER_REAL_PHP_TEST_PASS")
