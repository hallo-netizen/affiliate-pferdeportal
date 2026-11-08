#!/usr/bin/env python3
"""Execute actual added PHP article-content filter, with read-only WP stubs.
Ensure only the existing design test article gets a redesigned layout.
"""
from pathlib import Path
from zipfile import ZipFile
from tempfile import TemporaryDirectory
import subprocess
base=Path("protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/PLUGINS/ISOLIERTE_PLUGINS/HD-003-DESIGN-TEMPLATE-KIT/CURRENT.zip")
phpname="affiliate-portal-template-kit/includes/hobby-depot-article-hero-v150789.php"
with ZipFile(base) as z:
    code=z.read(phpname)
    assert b"hd003_hab_article_content_v150804" in code
stubs=r"""<?php
error_reporting(E_ALL);
define('ABSPATH','/tmp');
class WP_Post{
 public $ID=904015,$post_type='post',$post_title='Zweileiner oder Vierleiner?';
}
class WP_Term{
 public $term_id=651,$name='Drachen & Leinen',$taxonomy='category';
}
$GLOBALS['test_post']=new WP_Post;
$GLOBALS['demo']=true;
function is_singular($kind){return $kind==='post';}
function is_admin(){return false;}
function is_feed(){return false;}
function in_the_loop(){return true;}
function is_main_query(){return true;}
function get_queried_object(){return $GLOBALS['test_post'];}
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
"""
body=r"""
$html='<p class="hddemo-kicker">Hobby Depot · Design</p>'
    .'<p class="has-large-font-size">Zwei oder vier Leinen?</p>'
    .'<nav aria-label="Inhaltsverzeichnis des Testartikels"><strong>In diesem Artikel</strong><ol><li>1</li><li>2</li></ol></nav>'
    .'<h2 id="ziel">Auf einen Blick</h2><p>Die wichtigsten Fakten.</p>'
    .'<ol class="wp-block-list"><li>Echte Anleitung: ersten Schritt beachten</li></ol>'
    .'<figure><img src="https://www.hobby-depot.de/wp-content/uploads/2026/11/test.jpg"></figure>';
assert(hd003_hab_article_preview_v150804()===true);
$classes=hd003_hab_article_body_class_v150804(['single-post']);
assert(in_array('hd-article-hab-preview-v150804',$classes,true));
$out=hd003_hab_article_content_v150804($html);
assert(substr_count($out,'hd-article-body-grid-v150804')===1);
assert(strpos($out,'hd-article-reading-v150804')!==false);
assert(strpos($out,'hd-article-sidebar-card-v150804')!==false);
assert(strpos($out,'Drachen &amp; Leinen')!==false);
assert(strpos($out,'Inhaltsverzeichnis des Testartikels')===false);
assert(strpos($out,'Die wichtigsten Fakten.')!==false);
assert(strpos($out,'Echte Anleitung: ersten Schritt beachten')!==false);
assert(substr_count($out,'<img')===1);
assert(strpos($out,'Passende Produkte')===false);
assert(strpos($out,'DESIGNVORSCHAU')===false);
assert(hd003_hab_article_content_v150804($out)===$out,'Re-wrap prevented');
print("PREVIEW_POST_SERVER_RENDER_PASS\n");
$GLOBALS['demo']=false;
assert(hd003_hab_article_preview_v150804()===false);
assert(hd003_hab_article_content_v150804($html)===$html,'Other published posts untouched');
assert(!in_array('hd-article-hab-preview-v150804',hd003_hab_article_body_class_v150804(['single-post']),true));
print("ALL_OTHER_POSTS_UNTOUCHED_PASS\n");
"""
with TemporaryDirectory() as td:
    p=Path(td)
    f=p/"article-hero.php";f.write_bytes(code)
    t=p/"test.php"
    t.write_text(stubs+"require __DIR__.'/article-hero.php';\n"+body)
    lint=subprocess.run(['php','-l',str(t)],capture_output=True,text=True)
    assert lint.returncode==0,(lint.stdout,lint.stderr)
    run=subprocess.run(['php','-d','zend.assertions=1','-d','assert.exception=1',str(t)],capture_output=True,text=True)
    assert run.returncode==0,(run.stdout,run.stderr)
    print(run.stdout.strip())
print("HD003_ARTICLE_SERVER_PHP_TESTS_PASS")
