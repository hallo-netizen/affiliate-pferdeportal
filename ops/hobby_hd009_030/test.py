#!/usr/bin/env python3
"""Run actual modified HD009 class and provider card method in PHP.
Provider photos and links stay paired; Amazon Mediathek photo fallback is
automatically suppressed when a verified eBay/idealo card is already present.
No API calls or database mutations.
"""
from zipfile import ZipFile
from pathlib import Path
from tempfile import TemporaryDirectory
import re,subprocess
base=Path("protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/PLUGINS/ISOLIERTE_PLUGINS/HD-009-AFFILIATE-ZENTRALE/CURRENT.zip")
with ZipFile(base) as z:
    cls=z.read("affiliate-portal-router/includes/class-hdar-amazon-start.php").decode()
    article=z.read("affiliate-portal-router/includes/trait-ppar-article-plans.php").decode()
    main=z.read("affiliate-portal-router/hobby-depot-affiliate-router.php").decode()
    assert " * Version: 0.1.30" in main[:400]
    assert cls.count("function provider_article_cards_first(")==1
    assert article.count("// HD009 0.1.30: the feed provider")==1
p=article.find("    private function article_plan_render_product_card_markup(")
assert p>=0
q=article.find("\n    private function ",p+70)
assert q>p
func=article[p:q]

stubs=r"""<?php
error_reporting(E_ALL);
define('ABSPATH','/tmp');
class WP_Post {public $ID=123,$post_type='post',$post_status='publish';}
$GLOBALS['post']=new WP_Post;
$GLOBALS['launch']=true;
$GLOBALS['settings']=[
  'hdar_launch_partners_v1'=>'amazon_idealo',
  'ppar_amazon_search_v1'=>['enabled'=>true,'tracking_id'=>'example-21'],
  'hdar_amazon_approved_v1'=>['post:123'=>['items'=>[
    ['asin'=>'B012345678','title'=>'Lenkdrachen Einsteiger','image_id'=>22,
      'image_source'=>'own_or_licensed']
  ]]]
];
function get_option($key,$fallback=null){return $GLOBALS['settings'][$key]??$fallback;}
function is_admin(){return false;}
function is_feed(){return false;}
function is_singular($type){return $type==='post';}
function in_the_loop(){return true;}
function is_main_query(){return true;}
function get_the_ID(){return $GLOBALS['post']->ID;}
function get_post_status($id){return 'publish';}
function post_password_required($id){return false;}
function wp_attachment_is_image($id){return $id===22;}
function wp_get_attachment_image_url($id,$size){return $id===22?'https://example.org/authorized-photo.jpg':false;}
function absint($v){return abs((int)$v);}
function sanitize_key($s){return strtolower(preg_replace('/[^a-zA-Z0-9_-]/','',str_replace(' ','-',(string)$s)));}
function sanitize_text_field($s){return (string)$s;}
function esc_attr($v){return htmlspecialchars((string)$v,ENT_QUOTES,'UTF-8');}
function esc_html($v){return htmlspecialchars((string)$v,ENT_QUOTES,'UTF-8');}
function esc_url($v){return (string)$v;}
function add_action(...$args){return true;}
function add_filter(...$args){return true;}
function add_shortcode(...$args){return true;}
function get_the_title($id){return 'Lenkdrachen';}
"""
tests=r"""
$provider='<section class="ppar-article-product-block" data-ppar-product-count="1">'
 .'<div class="ppar-article-section-label">Produktvorschläge</div>'
 .'<div class="ppar-article-product-grid"><div class="ppar-article-product-card">'
 .'<a class="ppar-article-product-link" href="https://www.idealo.de/test">'
 .'<span class="ppar-article-product-media"><img class="ppar-article-product-image" '
 .'src="https://cdn.idealo.com/approved-feed-photo.jpg" alt="Lenkdrachen"></span>'
 .'<span class="ppar-article-product-title">Ein passendes Angebot</span></a>'
 .'</div></div></section>';
$content='<div class="hd-article-body-grid-v150804"><div class="hd-article-reading-v150804">'
 .'<h2>Auf einen Blick</h2>'.$provider
 .'</div><aside class="hd-article-sidebar-v150804"><nav>Mehr zum Thema</nav></aside></div>';
$out=HDAR_Amazon_Start::render_article_cards($content);
assert(substr_count($out,'ppar-article-product-block')===1,'only existing provider block');
assert(strpos($out,'hdar-amazon-article-products')===false,'Amazon Media Library fallback auto-hides');
assert(strpos($out,'authorized-photo.jpg')===false,'no Amazon manual photo when provider exists');
$aside=strpos($out,'<aside class="hd-article-sidebar-v150804"');
$product=strpos($out,'ppar-article-product-block');
$nav=strpos($out,'<nav>Mehr zum Thema');
assert($aside<$product && $product<$nav,'provider card moved into actual Hab right sidebar');
assert(strpos($out,'https://cdn.idealo.com/approved-feed-photo.jpg')!==false);
assert(strpos($out,'https://www.idealo.de/test')!==false);
assert(HDAR_Amazon_Start::render_article_cards($out)===$out,'idempotent');
echo "REAL_IDEALO_PROVIDER_CARD_WINS_AND_MEDIA_FALLBACK_DISAPPEARS_PASS\n";

$standard='<p>Artikeltext</p>'.$provider;
assert(HDAR_Amazon_Start::render_article_cards($standard)===$standard,'standard article provider card stays intact');
echo "STANDARD_ARTICLE_PROVIDER_CARDS_UNCHANGED_PASS\n";

$no_provider='<div class="hd-article-body-grid-v150804"><div class="hd-article-reading-v150804"><p>Artikeltext</p></div><aside class="hd-article-sidebar-v150804"><nav>Mehr zum Thema</nav></aside></div>';
$out=HDAR_Amazon_Start::render_article_cards($no_provider);
assert(strpos($out,'hdar-amazon-photo-product')!==false,'own licensed image used when no provider');
assert(strpos($out,'authorized-photo.jpg')!==false);
assert(strpos($out,'https://www.amazon.de/dp/B012345678')!==false);
echo "AUTHORIZED_MEDIA_AMAZON_FALLBACK_WHEN_NO_PROVIDER_PASS\n";

$badprovider='<section class="ppar-article-product-block"><div class="ppar-article-product-grid"><div class="ppar-article-product-card">text only</div></div></section>';
$out=HDAR_Amazon_Start::render_article_cards($badprovider);
assert(strpos($out,'hdar-amazon-article-products')===false,'never layer fake Amazon boxes over an incomplete provider block');
echo "NO_FAKE_IMAGELESS_PROVIDER_CARD_MIX_PASS\n";

$GLOBALS['settings']['hdar_launch_partners_v1']='off';
$out=HDAR_Amazon_Start::render_article_cards($content);
assert(strpos($out,'ppar-article-product-block')!==false,'provider remains regardless Amazon launch flag');
assert(strpos($out,'hdar-amazon-photo-product')===false,'Amazon disabled');
echo "PROVIDER_CARDS_INDEPENDENT_OF_AMAZON_MODE_PASS\n";
"""
provider_stubs=r"""
class ArticleCardFixture {
    private function build_subid($a,$b,$c,$d){return 'sub';}
    private function apply_subid_to_url($url,$subid,$key){return $url;}
    private function multiprovider_runtime_tracking_url($url,$provider){return $url;}
    private function multiprovider_runtime_image_url($url,$provider,$id=0){return $url;}
    private function multiprovider_matching_offers_for_banner($banner,$context,$slot){return [];}
    private function multiprovider_render_offer_buttons($offers,$surface){return '';}
    private function get_post_id(){return 123;}
"""
test_provider=r"""
$fixture=new ArticleCardFixture;
$group=['id'=>'g1'];
$context=['primary_slug'=>'sportdrachen'];
$blank=['url'=>'https://www.idealo.de/test','image_url'=>'','title'=>'Passender Lenkdrachen',
  'network'=>'idealo','creative_type'=>'product'];
assert($fixture->test_card($blank,$context,$group)==='','no image => no product card');
$blank['image_url']='https://cdn.idealo.com/approved-feed-photo.jpg';
$good=$fixture->test_card($blank,$context,$group);
assert(strpos($good,'ppar-article-product-image')!==false);
assert(strpos($good,'cdn.idealo.com')!==false);
assert(strpos($good,'idealo.de')!==false);
assert(strpos($good,'amazon.de')===false,'provider image not falsely relabelled Amazon');
echo "PROVIDER_OWN_IMAGE_REQUIRED_AND_OWN_OFFER_PAIRED_PASS\n";
"""
# The function is unmodified except its new explicit image guard, and is
# executed inside a fixture using only minimal WordPress API shims.
func=func.replace("private function article_plan_render_product_card_markup(","public function test_card(")
func=func.replace("$post_id, $context, $group, $slot_type = 'post_bottom_products'","$context, $group, $slot_type = 'post_bottom_products'")
func=func.replace("$subid = $this->build_subid($post_id, $context, $group, $slot_type);","$post_id=123;\n        $subid = $this->build_subid($post_id, $context, $group, $slot_type);")
with TemporaryDirectory() as td:
    f=Path(td)/"class-hdar-amazon-start.php"
    f.write_text(cls)
    fixture=Path(td)/"article-method.php"
    fixture.write_text("<?php\n"+provider_stubs+func+"\n}\n")
    test=Path(td)/"test.php"
    test.write_text(stubs+"\nrequire __DIR__.'/class-hdar-amazon-start.php';\n"+tests+"\nrequire __DIR__.'/article-method.php';\n"+test_provider)
    lint=subprocess.run(['php','-l',str(test)],capture_output=True,text=True)
    assert lint.returncode==0,(lint.stdout,lint.stderr)
    run=subprocess.run(['php','-d','zend.assertions=1','-d','assert.exception=1',str(test)],capture_output=True,text=True)
    assert run.returncode==0,(run.stdout,run.stderr)
    print(run.stdout.strip())
print("HD009_030_REAL_PHP_PROVIDER_FIRST_TESTS_PASS")
