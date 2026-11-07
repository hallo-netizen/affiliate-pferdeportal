<?php
// Offline positive/negative tests of the exact new category fallback and official DataForSEO field.
define('ABSPATH',__DIR__);
define('DAY_IN_SECONDS',86400);
$GLOBALS['opts']=array();
function get_option($k,$d=array()){return $GLOBALS['opts'][$k]??$d;}
function sanitize_key($s){return preg_replace('/[^a-z0-9_\-]/','',strtolower((string)$s));}
function sanitize_text_field($s){return strip_tags((string)$s);}
function esc_url($s){return htmlspecialchars((string)$s,ENT_QUOTES,'UTF-8');}
function wp_parse_url($u,$component){return parse_url($u,$component);}
require dirname(__DIR__).'/affiliate-portal-router/includes/trait-ppar-hb-amazon.php';
class Tester {use PPAR_HB_Amazon_Trait;
 public function link($ctx,$slot){return $this->hb_amazon_category_search_fallback($ctx,$slot);}
 public function asin($title,$items){return $this->hb_amazon_exact_match_asin($title,$items);}
}
function pass($name,$yes){if (!$yes) {echo "FAIL $name\n"; exit(1);}echo "PASS $name\n";}
$t=new Tester();
$ctx=['post_type'=>'category_archive','primary_name'=>'Wassermelder','product_family_slug'=>'wassermelder'];
pass('disabled no fallback',$t->link($ctx,'product_after_category_tiles')==='');
$GLOBALS['opts']['ppar_hab_amazon_settings_v1']=['enabled'=>true,'tag'=>'habundbewahr-21'];
$html=$t->link($ctx,'product_after_category_tiles');
pass('category generates only Amazon search',$html!=='' && str_contains($html,'https://www.amazon.de/s?k=Wassermelder&amp;tag=habundbewahr-21'));
pass('not a product detail link',!str_contains($html,'/dp/'));
pass('ad label',$html!=='' && str_contains($html,'Anzeige'));
pass('sponsored link',$html!=='' && str_contains($html,'rel="sponsored nofollow noopener noreferrer"'));
pass('no broad page',$t->link(['post_type'=>'page','primary_name'=>'Wassermelder','product_family_slug'=>'wassermelder'],'product_after_category_tiles')==='');
pass('no unspecified category',$t->link(['post_type'=>'category_archive','primary_name'=>'Einbruchschutz'],'product_after_category_tiles')==='');
pass('no product-card injection',$t->link($ctx,'category_product_1')==='');
pass('no unknown slots',$t->link($ctx,'hub_after_cards')==='');
$GLOBALS['opts']['ppar_hab_amazon_settings_v1']=['enabled'=>true,'tag'=>'pferdeatelier-21'];
pass('foreign tag blocked',$t->link($ctx,'product_after_category_tiles')==='');
$GLOBALS['opts']['ppar_hab_amazon_settings_v1']=['enabled'=>true,'tag'=>'habundbewahr-21'];
$one=['type'=>'amazon_serp','title'=>'Türalarm Smart 4er Set','url'=>'https://www.amazon.de/dp/B0ABCD1234','data_asin'=>'B0ABCD1234'];
pass('DataForSEO data_asin field',$t->asin('Türalarm Smart 4er Set',[$one])==='B0ABCD1234');
pass('wrong variant rejected',$t->asin('Türalarm Smart 2er Set',[$one])==='');
pass('different ASIN ambiguous',$t->asin('Türalarm Smart 4er Set',[$one,['type'=>'amazon_serp','title'=>'Türalarm Smart 4er Set','url'=>'https://www.amazon.de/dp/B0ABCD5678','data_asin'=>'B0ABCD5678']])==='');
pass('foreign domain rejected',$t->asin('Türalarm Smart 4er Set',[['type'=>'amazon_serp','title'=>'Türalarm Smart 4er Set','url'=>'https://www.amazon.com/dp/B0ABCD1234','data_asin'=>'B0ABCD1234']])==='');
pass('nonproduct type rejected',$t->asin('Türalarm Smart 4er Set',[['type'=>'amazon_paid','title'=>'Türalarm Smart 4er Set','url'=>'https://www.amazon.de/dp/B0ABCD1234','data_asin'=>'B0ABCD1234']])==='');
pass('bad ASIN rejected',$t->asin('Türalarm Smart 4er Set',[['type'=>'amazon_serp','title'=>'Türalarm Smart 4er Set','url'=>'https://www.amazon.de/s?k=turalarm','data_asin'=>'NOTANASIN']])==='');