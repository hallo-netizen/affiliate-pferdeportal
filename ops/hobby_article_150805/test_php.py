#!/usr/bin/env python3
"""Run original HD003 PHP output on the design test before release.
WordPress APIs only stubbed; actual plugin method and file path retained.
"""
from pathlib import Path
from zipfile import ZipFile
from tempfile import TemporaryDirectory
import subprocess
ROOT=Path("protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/PLUGINS/ISOLIERTE_PLUGINS/HD-003-DESIGN-TEMPLATE-KIT")
z=ZipFile(ROOT/"CURRENT.zip")
p="affiliate-portal-template-kit/includes/hobby-depot-article-hero-v150789.php"
source=z.read(p)
stubs=r"""<?php
error_reporting(E_ALL);
define('ABSPATH','/tmp');
class WP_Post{public $ID=904015,$post_type='post',$post_title='Zweileiner oder Vierleiner?';}
class WP_Term{public $term_id=651,$name='Drachen & Leinen',$taxonomy='category';}
$GLOBALS['post']=new WP_Post;
$GLOBALS['demo']=true;
function is_singular($kind){return $kind==='post';}
function is_admin(){return false;}
function is_feed(){return false;}
function in_the_loop(){return true;}
function is_main_query(){return true;}
function get_queried_object(){return $GLOBALS['post'];}
function get_post_meta($id,$key,$single=true){
 if($key==='_hddemo_layout_key')return ($GLOBALS['demo']&&$id===904015)?'hddemo-zw-vl-20261101':'';
 return '';
}
function add_filter(...$args){return true;}
function add_action(...$args){return true;}
function get_the_category($post_id){return [new WP_Term];}
function get_posts($args){return [];}
function get_permalink($post_id){return 'https://www.hobby-depot.de/sample-'.$post_id.'/';}
function get_the_title($post_id){return 'Thema';}
function get_category_link($id){return 'https://www.hobby-depot.de/category/sportdrachen-drachen-leinen/';}
function is_wp_error($o){return false;}
function esc_url($s){return (string)$s;}
function esc_html($s){return htmlspecialchars((string)$s,ENT_QUOTES,'UTF-8');}
function plugins_url($file,$plugin){return 'https://www.hobby-depot.de/wp-content/plugins/affiliate-portal-template-kit/'.ltrim($file,'/');}
"""
body=r"""
$html='<p class="hddemo-kicker"><strong>HOBBY DEPOT · DESIGNTEST · SPORTDRACHEN</strong></p>'
 .'<p class="has-large-font-size">Einleitung</p>'
 .'<nav aria-label="Inhaltsverzeichnis des Testartikels"><ol><li>A</li><li>B</li></ol></nav>'
 .'<h3>Auf einen Blick</h3><p>Wissenswertes</p>'
 .'<h2 id="hddemo-unterschied">Was unterscheidet?</h2><p>Echte Beschreibung</p>'
 .'<aside aria-label="Bannerplatz Testartikel"><div>Fake partner/banner</div></aside>'
 .'<h2 id="hddemo-produkte" class="wp-block-heading">Drei konkrete Modelle als Muster für Produktkacheln</h2>'
 .'<p>Die Modelle und Herstellerlinks sind real, aber Layoutprüfung.</p>'
 .'<div class="hddemo-product-grid"><article><div class="demo">PRODUKTKACHEL · ZWEILEINER</div></article>'
 .'<article><div class="demo">PRODUKTKACHEL · VIERLEINER</div></article></div>'
 .'<h2 class="wp-block-heading">Passende Themen bei Hobby Depot</h2><p>Der alte Linkplatz</p>'
 .'<div class="hddemo-related"><ul><li>Link zum selben Artikel</li></ul></div>'
 .'<h2 id="hddemo-faq">Häufige Fragen</h2><p>FAQ Inhalt</p>'
 .'<ol class="wp-block-list"><li>Schritt 1</li><li>Schritt 2</li></ol>';
assert(hd003_hab_article_preview_v150804()===true);
$out=hd003_hab_article_content_v150804($html);
$checks=array(
 'previewLayout'=>substr_count($out,'hd-article-body-grid-v150804')===1,
 'noFakeProducts'=>strpos($out,'hddemo-product-grid')===false&&strpos($out,'PRODUKTKACHEL')===false,
 'noEmptyProductHeading'=>strpos($out,'Drei konkrete Modelle')===false,
 'noDuplicateRelatedPlaceholder'=>strpos($out,'hddemo-related')===false&&strpos($out,'Passende Themen bei Hobby Depot')===false,
 'noUnapprovedBanner'=>strpos($out,'Bannerplatz Testartikel')===false,
 'heroContentNotTouched'=>strpos($out,'Auf einen Blick')!==false,
 'realTextUntouched'=>strpos($out,'Echte Beschreibung')!==false&&strpos($out,'FAQ Inhalt')!==false,
 'realStepListUntouched'=>strpos($out,'Schritt 1')!==false,
 'realCategoryCard'=>strpos($out,'category/sportdrachen-drachen-leinen/')!==false,
 'photoCard'=>substr_count($out,'class="hd-article-sidebar-photo-v150805"')===1&&
  strpos($out,'sportdrachen.webp')!==false,
 'noSecondWrap'=>hd003_hab_article_content_v150804($out)===$out
);
foreach($checks as $test=>$pass) {
 assert($pass,$test);
 echo "PHP_CARD_PASS ".$test."\n";
}
$GLOBALS['demo']=false;
assert(hd003_hab_article_content_v150804($html)===$html);
echo "PHP_OTHER_ARTICLES_UNTOUCHED_PASS\n";
"""
with TemporaryDirectory() as td:
    root=Path(td)/"affiliate-portal-template-kit"
    includes=root/"includes";includes.mkdir(parents=True)
    script=includes/"hobby-depot-article-hero-v150789.php"
    script.write_bytes(source)
    img=root/"assets/hobby-depot-v150780/hobby-masters/sportdrachen.webp"
    img.parent.mkdir(parents=True)
    img.write_bytes(z.read("affiliate-portal-template-kit/assets/hobby-depot-v150780/hobby-masters/sportdrachen.webp"))
    test=root/"test.php";test.write_text(stubs+"require __DIR__.'/includes/hobby-depot-article-hero-v150789.php';\n"+body)
    lint=subprocess.run(['php','-l',str(test)],capture_output=True,text=True)
    assert lint.returncode==0,(lint.stdout,lint.stderr)
    run=subprocess.run(['php','-d','zend.assertions=1','-d','assert.exception=1',str(test)],capture_output=True,text=True)
    assert run.returncode==0,(run.stdout,run.stderr)
    print(run.stdout.strip())
print("HD003_150805_REAL_PHP_METHODS_PASS")
