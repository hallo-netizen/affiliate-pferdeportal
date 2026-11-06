<?php
/**
 * Real Hab & Bewahr design corpus verification (not a claim of live WP data).
 * Input is the active project's bundled nodes.json, converted to WP snapshot.
 */
error_reporting(E_ALL);
set_error_handler(static function($severity,$message){throw new ErrorException($message,0,$severity);});
define('ABSPATH','/mock/');
$path=$argv[1] ?? '';
$real=json_decode((string)file_get_contents($path),true);
if(!is_array($real)||empty($real['nodes'])||empty($real['mapping']))throw new RuntimeException('Real portal nodes missing');
$GLOBALS['hb_realcats']=$real;
$GLOBALS['hb_option_reads']=0;
function get_option($key,$default=null){
    ++$GLOBALS['hb_option_reads'];
    if($key==='apkw_target_tree_active_revision_v1')return 'real-hab-category-test';
    if($key==='apkw_target_tree_active_snapshot_v1')return $GLOBALS['hb_realcats'];
    return $default;
}
function absint($x){return abs((int)$x);}
function sanitize_text_field($v){return trim(strip_tags((string)$v));}
function remove_accents($v){return strtr((string)$v,['ä'=>'a','ö'=>'o','ü'=>'u','Ä'=>'A','Ö'=>'O','Ü'=>'U','ß'=>'ss']);}
function sanitize_title($v){$v=remove_accents($v);return trim(preg_replace('/[^a-z0-9]+/','-',strtolower((string)$v)),'-');}
function sanitize_key($v){return preg_replace('/[^a-z0-9_\-]/','',strtolower((string)$v));}
function wp_json_encode($v){return json_encode($v,JSON_UNESCAPED_UNICODE);}
function get_post_status($id){return 'publish';}
function get_post_type($id){return 'page';}
function add_filter($tag,$callback,$priority=10,$count=1){return true;}
class WP_Error{
 private $key;
 public function __construct($key,$message=''){$this->key=$key;}
 public function get_error_code(){return $this->key;}
}
function is_wp_error($v){return $v instanceof WP_Error;}
require __DIR__.'/../_build/affiliate-portal-router/includes/class-ppar-hab-bewahr-bridge.php';
$catalog=PPAR_HB_Integration::catalog();
if(is_wp_error($catalog))throw new RuntimeException('Hab corpus failed: '.$catalog->get_error_code());
if(count($catalog['private_bucket_profiles'])!==6)throw new RuntimeException('Six real worlds missing');
if(count($catalog['article_targets'])<200)throw new RuntimeException('Lost >200 real article categories');
if(count($catalog['product_targets'])<8)throw new RuntimeException('Real product-category discovery too narrow');
if(count($catalog['search_rules'])>50)throw new RuntimeException('Unbounded eBay query plan');
if(count($catalog['product_targets'])!==count($catalog['business_concepts']))throw new RuntimeException('Missing product concepts');
$labels=array_column($catalog['article_targets'],'category_name');
foreach(array('Wassermelder','Camping & Wohnmobil','Rauchmelder / Vernetzung','Kameras & Datenschutz') as $label){
 if(!in_array($label,$labels,true))throw new RuntimeException('Real category missing: '.$label);
}
$families=array_column($catalog['business_concepts'],'title');
foreach(array('Wassermelder','Rauchmelder','Gaswarnmelder') as $label){
 if(!in_array($label,$families,true))throw new RuntimeException('Core product category missing: '.$label);
}
$article_by_name=array();
foreach($catalog['article_targets'] as $a){$article_by_name[$a['category_name']]=$a;}
if(($article_by_name['SIM-Karten für Alarmmelder']['product_slug'] ?? '')!=='')throw new RuntimeException('Accessory category misclassified');
if(PPAR_HB_Design_Contract::affiliate_page_type(99)!=='hub1')throw new RuntimeException('Original world page missing');
if(PPAR_HB_Integration::page_for_id(99)['name']!=='Einbruch & Diebstahl')throw new RuntimeException('World name incorrect');
$reads=$GLOBALS['hb_option_reads'];
PPAR_HB_Integration::catalog();
PPAR_HB_Integration::page_for_id(99);
if($GLOBALS['hb_option_reads']!==$reads)throw new RuntimeException('Repeated expensive options reads per request');
$targets=array_column($catalog['product_targets'],'slug');
foreach($targets as $slug){if($slug==='')throw new RuntimeException('Unresolved product target page');}
echo 'HB_REAL_CATEGORY_CORPUS_PASS worlds=6 articles='.count($catalog['article_targets']).' verified_product_categories='.count($catalog['product_targets']).' cached_reads='.$reads."\n";
