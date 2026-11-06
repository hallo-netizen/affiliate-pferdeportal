<?php
// Run as CLI on GitHub Actions. No WordPress DB or external API needed.
error_reporting(E_ALL);
define('ABSPATH','/mock/');
$GLOBALS['hb_mode'] = $argv[1] ?? 'valid';
$GLOBALS['hb_hooks'] = [];
function add_filter($hook,$callback,$priority=10,$args=1) {$GLOBALS['hb_hooks'][$hook] = array($callback,$args); }
class WP_Error {
    private $code; public function __construct($code, $message=''){$this->code=$code;}
    public function get_error_code(){return $this->code;}
}
function is_wp_error($v){return $v instanceof WP_Error;}
function absint($x){return abs((int)$x);}
function sanitize_text_field($x){return trim(strip_tags((string)$x));}
function sanitize_title($x){$x=remove_accents((string)$x);$x=strtolower($x);return trim(preg_replace('/[^a-z0-9]+/','-',$x),'-');}
function sanitize_key($x){return preg_replace('/[^a-z0-9_\-]/','',strtolower((string)$x));}
function remove_accents($x){return strtr((string)$x,['ä'=>'a','ö'=>'o','ü'=>'u','Ä'=>'A','Ö'=>'O','Ü'=>'U','ß'=>'ss']);}
function get_post_status($id){return 'publish';}
function wp_json_encode($v){return json_encode($v,JSON_UNESCAPED_UNICODE);}
function get_post_type($id){return $id > 30000 ? 'post' : 'page';}
function get_post_meta($id,$key,$single=true){return '';}
function get_post($id){return (object) ['ID'=>$id,'post_name'=>'test'];}
final class Portal_Affiliate_Router {
    private static $self;
    public static function instance(){if(!self::$self)self::$self=new self();return self::$self;}
    public function hab_bw_article_slot($id,$kind){return 'ARTICLE-'.$kind.'-'.$id;}
    public function hab_bw_area_slot($id,$kind){return 'AREA-'.$kind.'-'.$id;}
}
function get_option($key,$default=null) {
    if ($key==='apkw_target_tree_active_revision_v1') {return $GLOBALS['hb_mode']==='invalid' ? '' : 'hab-revision-tested';}
    if ($key!=='apkw_target_tree_active_snapshot_v1') {return $default;}
    $nodes=[];$mapping=[];
    $push = static function($id,$type,$name,$parent,$wp_id) use (&$nodes,&$mapping) {
        $nodes[]=array('node_id'=>$id,'pillar'=>'core','display_name'=>$name,'slug'=>sanitize_title($name).'-'.str_replace(':','-',$id),'parent_id'=>$parent,'object_type'=>$type);
        $mapping[$id]=array('object_type'=>$type,'object_id'=>$wp_id);
    };
    $products=['Wassermelder','Rauchmelder / Vernetzung','Tresor','Gaswarnmelder','Alarmanlage bei Stromausfall','Bewegungsmelder & Licht'];
    $push('core:hub','page','Hab & Bewahr','',99);
    for($i=0;$i<6;$i++){
        $w='core:world:'.$i;$a='core:area:'.$i;$t='core:topic:'.$i;
        $push($w,'page','Welt '.$i,'core:hub',100+$i);
        $push($a,'page','Bereich '.$i,$w,200+$i);
        $push($t,'page',$products[$i],$a,300+$i);
        for($n=0;$n<7;$n++){
            $push('core:cat:'.$i.':'.$n,'category',($n===0 ? $products[$i] : 'Kategorie '.$i.'-'.$n),$t,400+($i*7)+$n);
        }
    }
    for($i=0;$i<20;$i++){$push('core:extra:'.$i,'page','Notiz '.$i,'core:area:0',800+$i);}
    return ['revision'=>$GLOBALS['hb_mode']==='wrong_revision'?'bad':'hab-revision-tested','nodes'=>$nodes,'mapping'=>$mapping];
}
require __DIR__.'/../_build/affiliate-portal-router/includes/class-ppar-hab-bewahr-bridge.php';
PPAR_HB_Integration::bootstrap();
$expected=['ppar_portal_source_catalog','ppar_affiliate_slot_matrix','hbdp_article_product_cards_html','hbdp_article_auto_banner_html','hbdp_area_product_cards_html','hbdp_area_auto_banner_html'];
foreach($expected as $hook){if(!isset($GLOBALS['hb_hooks'][$hook]))throw new Exception('Missing registered bridge '.$hook);}
$catalog=PPAR_HB_Integration::catalog();
if($GLOBALS['hb_mode']!=='valid'){
   if(!is_wp_error($catalog) || !in_array($catalog->get_error_code(),['hb_active_tree_missing','hb_worlds_unexpected'],true))throw new Exception('Fail closed broken');
   echo "HB_BRIDGE_NEGATIVE_PASS\n";exit(0);
}
if(!is_array($catalog) || count($catalog['product_targets'])<3 || count($catalog['article_targets'])!==42)throw new Exception('No matching product/category catalog');
if(PPAR_HB_Design_Contract::affiliate_page_type(300)!=='leaf') throw new Exception('Missing original page classification');
if(PPAR_HB_Integration::article_products('',30001)!=='ARTICLE-products-30001')throw new Exception('Missing article product slot');
if(PPAR_HB_Integration::article_banner('',30001)!=='ARTICLE-banner-30001')throw new Exception('Missing article banner slot');
if(PPAR_HB_Integration::area_products('','core:topic:0')!=='AREA-products-300')throw new Exception('Missing area product slot');
if(PPAR_HB_Integration::area_banner('','core:topic:0')!=='AREA-banner-300')throw new Exception('Missing area banner slot');
if(PPAR_HB_Integration::area_banner('','unknown')!=='')throw new Exception('Unknown area must be blank');
if(PPAR_HB_Integration::world_banner('','core:world:0')!=='AREA-banner-100')throw new Exception('World banner missing');
if(PPAR_HB_Integration::world_banner('','core:cat:0:0')!=='')throw new Exception('World banner should reject category');
if(PPAR_HB_Integration::editorial_banner('','bad-slot','core:topic:0')!=='')throw new Exception('Unknown editorial slot should reject');
if(PPAR_HB_Integration::page_for_id(300)['name']!=='Wassermelder')throw new Exception('Page lookup mismatch');
$matrix=PPAR_HB_Integration::slot_matrix([],['adapter'=>'wordpress_local'],'1.0');
foreach(['post_bottom_products','post_inline_banner','hub_after_cards','category_product_1','glossary_single_desktop_banner'] as $slot)if(!isset($matrix[$slot]))throw new Exception('Missing slot: '.$slot);
if(PPAR_HB_Integration::slot_matrix([],['adapter'=>'external_portal'],'1.0')!==[])throw new Exception('External portal slot contamination');
echo "HB_BRIDGE_POSITIVE_PASS worlds=6 products=".count($catalog['product_targets'])." categories=".count($catalog['article_targets'])."\n";
