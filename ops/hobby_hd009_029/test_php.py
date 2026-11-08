#!/usr/bin/env python3
"""Test exact HD009 0.1.29 PHP output with WordPress stubs and no remote API.
Checks only licensed product images appear, exact per-post targeting, article
sidebar handling, duplicate suppression and empty-card rejection.
"""
from pathlib import Path
from zipfile import ZipFile
from tempfile import TemporaryDirectory
import subprocess
ROOT=Path('protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/PLUGINS/ISOLIERTE_PLUGINS/HD-009-AFFILIATE-ZENTRALE/CURRENT.zip')
with ZipFile(ROOT) as z:
    actual=z.read('affiliate-portal-router/includes/class-hdar-amazon-start.php')
    body=z.read('affiliate-portal-router/hobby-depot-affiliate-router.php').decode()
    assert ' * Version: 0.1.29' in body[:300]
stubs=r"""<?php
error_reporting(E_ALL);
define('ABSPATH', '/tmp');
class WP_Post {public $ID=123,$post_type='post',$post_status='publish';}
$GLOBALS['post']=new WP_Post;
$GLOBALS['settings']=array(
    'hdar_launch_partners_v1'=>'amazon_idealo',
    'ppar_amazon_search_v1'=>array('enabled'=>true,'tracking_id'=>'example-21'),
    'hdar_amazon_approved_v1'=>array('post:123'=>array(
      'label'=>'Sportdrachen',
      'items'=>array(
        array('asin'=>'B012345678','title'=>'Lenkdrachen Einsteiger mit Tasche',
          'image_id'=>22,'image_source'=>'own_or_licensed'),
        array('asin'=>'B012345679','title'=>'Leinenset',
          'image_id'=>0,'image_source'=>''),
        array('asin'=>'B012345680','title'=>'Zweiter Lenkdrachen',
          'image_id'=>23,'image_source'=>'own_or_licensed')
      )
    ))
);
function get_option($key,$fallback=null){return $GLOBALS['settings'][$key]??$fallback;}
function is_admin(){return false;}
function is_feed(){return false;}
function is_singular($post_type){return $GLOBALS['singular']??true;}
function in_the_loop(){return true;}
function is_main_query(){return true;}
function get_the_ID(){return $GLOBALS['post']->ID;}
function get_post_status($id){return $GLOBALS['post']->post_status;}
function post_password_required($id){return false;}
function wp_attachment_is_image($id){return in_array($id,[22,23],true);}
function wp_get_attachment_image_url($id,$size){return wp_attachment_is_image($id)?'https://www.hobby-depot.de/wp-content/uploads/licensed-'.$id.'.jpg':false;}
function sanitize_key($s){return strtolower(preg_replace('/[^a-zA-Z0-9_-]/','',str_replace(' ','-',(string)$s)));}
function sanitize_text_field($s){return (string)$s;}
function absint($v){return abs((int)$v);}
function get_the_title($id){return 'Sportdrachen';}
function esc_html($v){return htmlspecialchars((string)$v,ENT_QUOTES|ENT_SUBSTITUTE,'UTF-8');}
function esc_attr($v){return htmlspecialchars((string)$v,ENT_QUOTES|ENT_SUBSTITUTE,'UTF-8');}
function esc_url($v){return htmlspecialchars((string)$v,ENT_QUOTES|ENT_SUBSTITUTE,'UTF-8');}
function wp_unslash($x){return $x;}
function add_action(...$args){return true;}
function add_filter(...$args){return true;}
function add_shortcode(...$args){return true;}
"""
tests=r"""
$article='<p>Der Artikel erklärt den Sportdrachen.</p>'
  .'<h2>Auf einen Blick</h2><p>Welcher Drachen passt?</p>';
$out=HDAR_Amazon_Start::render_article_cards($article);
assert(strpos($out,'hdar-amazon-article-products')!==false,'one article block');
assert(substr_count($out,'hdar-amazon-photo-product')===2,'two licensed photo cards');
assert(substr_count($out,'<img')===2,'two images');
assert(strpos($out,'licensed-22.jpg')!==false);
assert(strpos($out,'licensed-23.jpg')!==false);
assert(strpos($out,'Leinenset')===false,'missing image blocked');
assert(strpos($out,'tag=example-21')!==false,'affiliate ID');
assert(strpos($out,'sponsored nofollow')!==false,'advertising disclosure');
assert(strpos($out,'Anzeige')!==false);
assert(HDAR_Amazon_Start::render_article_cards($out)===$out,'no duplicate on rerender');
echo "EXACT_POST_LICENSED_AMAZON_ARTICLE_CARDS_PASS\n";

$hab='<div class="hd-article-body-grid-v150804"><div class="hd-article-reading-v150804">'
  .$article.'</div><aside class="hd-article-sidebar-v150804"><nav>Mehr zum Thema</nav></aside></div>';
$rendered=HDAR_Amazon_Start::render_article_cards($hab);
assert(substr_count($rendered,'hdar-amazon-article-products')===1);
$start=strpos($rendered,'<aside class="hd-article-sidebar-v150804"');
$cards=strpos($rendered,'hdar-amazon-article-products');
assert($cards>$start && $cards<strpos($rendered,'<nav>Mehr zum Thema',$start),'inside Hab sidebar');
assert(strpos($rendered,'hd-article-reading-v150804')!==false);
echo "HAB_DESIGN_RIGHT_COLUMN_INTEGRATION_PASS\n";

$without='<p>Text</p><div class="ppar-article-products">Existing Idealo products</div>';
assert(HDAR_Amazon_Start::render_article_cards($without)===$without,'existing provider cards have priority');
echo "NO_DUPLICATE_EXISTING_PRODUCT_CARDS_PASS\n";

$GLOBALS['post']->ID=124;
assert(HDAR_Amazon_Start::render_article_cards($article)===$article,'no broad category fallback');
$GLOBALS['post']->ID=123;
$GLOBALS['singular']=false;
assert(HDAR_Amazon_Start::render_article_cards($article)===$article,'no category/archive product boxes');
$GLOBALS['singular']=true;
echo "EXACT_TARGET_AND_POST_ONLY_GUARDS_PASS\n";

$GLOBALS['settings']['hdar_amazon_approved_v1']['post:123']['items'][0]['image_source']='';
$GLOBALS['settings']['hdar_amazon_approved_v1']['post:123']['items'][2]['image_id']=0;
assert(HDAR_Amazon_Start::render_article_cards($article)===$article,'no empty image-free cards');
echo "NO_IMAGE_NO_CARD_PASS\n";
"""
with TemporaryDirectory() as td:
    path=Path(td)/'class-hdar-amazon-start.php'
    path.write_bytes(actual)
    test=Path(td)/'test.php'
    test.write_text(stubs+"require __DIR__.'/class-hdar-amazon-start.php';\n"+tests)
    p=subprocess.run(['php','-l',str(test)],capture_output=True,text=True)
    assert p.returncode==0,(p.stdout,p.stderr)
    r=subprocess.run(['php','-d','zend.assertions=1','-d','assert.exception=1',str(test)],capture_output=True,text=True)
    assert r.returncode==0,(r.stdout,r.stderr)
    print(r.stdout.strip())
print('HD009_029_ORIGINAL_PHP_METHODS_PASS')
