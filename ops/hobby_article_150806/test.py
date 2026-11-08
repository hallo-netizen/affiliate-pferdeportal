#!/usr/bin/env python3
"""Run the actual 1.50.806 PHP functions with WordPress API stubs.
Checks all-post behavior, safety of other images, unrelated ad slots,
the existing Hab-style sidebar and plugin version.
"""
from pathlib import Path
from zipfile import ZipFile
from tempfile import TemporaryDirectory
import subprocess
ROOT=Path("protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/PLUGINS/ISOLIERTE_PLUGINS/HD-003-DESIGN-TEMPLATE-KIT")
with ZipFile(ROOT/"CURRENT.zip") as zipf:
    name="affiliate-portal-template-kit/includes/hobby-depot-article-hero-v150789.php"
    source=zipf.read(name)
    main=zipf.read("affiliate-portal-template-kit/pferde-template-kit.php").decode()
    assert " * Version: 1.50.806" in main[:800]
    assert "const VERSION = '1.50.806';" in main
    assert b"function hd003_article_single_hero_clean_v150806(" in source
stubs=r"""<?php
error_reporting(E_ALL);
define('ABSPATH', '/tmp');
class WP_Post {
 public $ID=904015,$post_type='post',$post_excerpt='';
 public $post_content='';
}
class WP_Term {
 public $term_id=651,$name='Drachen & Leinen',$taxonomy='category';
}
$GLOBALS['post']=new WP_Post;

$GLOBALS['ispost']=true;
$GLOBALS['featured']='';
function is_admin(){return false;}
function is_feed(){return false;}
function is_singular($kind){return $GLOBALS['ispost'] && $kind==='post';}
function in_the_loop(){return true;}
function is_main_query(){return true;}
function get_queried_object(){return $GLOBALS['post'];}
function get_the_post_thumbnail_url($id,$size){return $GLOBALS['featured'];}
function get_post_meta($id,$key,$single=true){
 if($key==='_hddemo_layout_key')return 'hddemo-zw-vl-20261101';
 return '';
}
function get_the_title($post){return "Zweileiner oder Vierleiner?";}
function get_the_category($id){return [new WP_Term];}
function get_posts($args){return [];}
function get_category_link($id){return 'https://www.hobby-depot.de/category/sportdrachen-drachen-leinen/';}
function get_permalink($id){return 'https://www.hobby-depot.de/a/';}
function is_wp_error($o){return false;}
function esc_url($s){return (string)$s;}
function esc_attr($s){return htmlspecialchars((string)$s,ENT_QUOTES);}
function esc_html($s){return htmlspecialchars((string)$s,ENT_QUOTES);}
function esc_url_raw($s,$protocols=[]){return (string)$s;}
function wp_strip_all_tags($s){return strip_tags((string)$s);}
function wp_trim_words($s,$count,$more){return substr((string)$s,0,50);}
function add_filter(...$args){return true;}
function add_action(...$args){return true;}
"""
tests=r"""
$hero='https://www.hobby-depot.de/wp-content/uploads/2026/11/hobby-depot-designtest-lenkdrachen.jpg';
$other='https://www.hobby-depot.de/wp-content/uploads/2026/11/andere-skizze.jpg';
$figure='<figure class="wp-block-image size-full"><img src="'.$hero.'" alt="Zweileiner">'
      .'<figcaption>Rechte zum Bild</figcaption></figure>';
$otherFigure='<figure class="wp-block-image size-full"><img src="'.$other.'"></figure>';
$ad='<div class="ppar-affiliate-slot hdar-ci-amazon-slot hdar-ci-amazon-slot-wide" data-ppar-slot="post_inline_banner">'
 .'<span class="hdar-ci-label">Anzeige</span>'
 .'<a class="hdar-ci-amazon-banner-text" href="https://www.amazon.de/s?k=test"><span>Link</span></a></div>';
$archiveAd='<div data-ppar-slot="hub_mid_banner">Archivbanner bleibt</div>';
$GLOBALS['post']->post_content='<p>Einleitung</p>'.$figure.'<p>Schluss</p>';
$input='<div class="hd-article-reading-v150804"><h2>Auf einen Blick</h2>'.$ad.$figure
    .'<p>Mehr dazu</p>'.$otherFigure
    .'<ol><li>Prüfe die Windstärke</li></ol>'.$archiveAd.'</div>';
$output=hd003_article_single_hero_clean_v150806($input);
assert(strpos($output,'hdar-ci-amazon-slot-wide')===false,'no photo-less Amazon banner');
assert(strpos($output,$hero)===false,'no repeated Hero in article');
assert(strpos($output,$other)!==false,'other factual image must survive');
assert(strpos($output,'Auf einen Blick')!==false,'reading content must survive');
assert(strpos($output,'Prüfe die Windstärke')!==false,'real checklists must survive');
assert(strpos($output,'Archivbanner bleibt')!==false,'unrelated ad slot untouched');
assert(substr_count($output,'wp-block-image')===1,'exactly one distinct figure in the content');
assert(hd003_article_single_hero_clean_v150806($output)===$output,'idempotent');
echo "HERO_DUPLICATE_REMOVED_AND_OTHER_IMAGE_PRESERVED_PASS\n";

$sidebar=hd003_hab_article_sidebar_v150804($GLOBALS['post']);
assert(strpos($sidebar,'Mehr zum Thema')!==false,'real category link');
assert(strpos($sidebar,'sportdrachen.webp')===false,'no third photo');
assert(strpos($sidebar,'<img')===false,'no sidebar photo');
assert(strpos($sidebar,'Drachen &amp; Leinen ansehen')!==false,'escaped real category label');
echo "HAB_STYLE_RIGHT_SIDEBAR_TEXT_ONLY_PASS\n";

$GLOBALS['featured']=$other; // featured image wins over inline photo
$output=hd003_article_single_hero_clean_v150806($input);
assert(strpos($output,$hero)!==false,'do not remove non-hero inline photo');
assert(strpos($output,'hdar-ci-amazon-slot-wide')===false);
echo "DIFFERENT_INLINE_IMAGE_PRESERVED_PASS\n";
$GLOBALS['featured']='';

$GLOBALS['ispost']=false;
assert(hd003_article_single_hero_clean_v150806($input)===$input,'no category/page changes');
$GLOBALS['ispost']=true;
$GLOBALS['post']->post_type='page';
assert(hd003_article_single_hero_clean_v150806($input)===$input,'no page changes');
$GLOBALS['post']->post_type='post';
echo "NON_POSTS_AND_CATEGORY_BANNERS_UNTOUCHED_PASS\n";
"""
with TemporaryDirectory() as td:
    folder=Path(td)
    php=folder/"hobby-depot-article-hero-v150789.php"
    php.write_bytes(source)
    test=folder/"test.php"
    # Keep the stubs local, never write into user-provided WordPress.
    test.write_text(stubs+"\nrequire __DIR__.'/hobby-depot-article-hero-v150789.php';\n"+tests)
    run=subprocess.run(["php","-l",str(test)],capture_output=True,text=True)
    assert run.returncode==0,(run.stdout,run.stderr)
    run=subprocess.run(["php","-d","zend.assertions=1","-d","assert.exception=1",str(test)],capture_output=True,text=True)
    assert run.returncode==0,(run.stdout,run.stderr)
    print(run.stdout.strip())
print("HD003_150806_PHP_FUNCTIONAL_PASS")
