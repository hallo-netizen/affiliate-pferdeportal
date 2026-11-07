#!/usr/bin/env python3
"""PHP execution checks for exact existing HD009 methods with minimal WP stubs."""
from pathlib import Path
from zipfile import ZipFile
from tempfile import TemporaryDirectory
import subprocess,json,re

ROOT=Path("protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/PLUGINS/ISOLIERTE_PLUGINS/HD-009-AFFILIATE-ZENTRALE")
ZIP=ROOT/"HOBBY_DEPOT_AFFILIATE_HD009_0.1.24.zip"
MAIN="affiliate-portal-router/hobby-depot-affiliate-router.php"
BADGE="affiliate-portal-router/assets/hdar-amazon-available-at-amazon-de-official.png"

with ZipFile(ZIP) as z:
    s=z.read(MAIN).decode()
    badge=z.read(BADGE)

def src(beg,end):
    i=s.index("    "+beg)
    j=s.index(end,i+len(beg))
    return s[i:j].strip()

builder=src("private function hdar_ci_amazon_banner(", "    /** HD007 owns the register markup")
shortcode=src("public function shortcode_affiliate_slot(","    private static function article_hybrid_defaults")
fallback=src("private function hdar_ci_article_empty_banner(","    /**")
# End method PHP syntax verified by real PHP below.

FAKES=r"""
<?php
error_reporting(E_ALL);
define('ABSPATH','/tmp/');
class WP_Term {
  public $term_id=27;public $taxonomy='category';public $name='Münzen';public $slug='muenzen';
}
class HDAR_Amazon_Start {
  public static function launch_active(){return true;}
}
class HD_Hobbyregister_Core_Stable127{
  public static function image_entry($id){
    return [
      'source'=>'hd007','path'=>'portraits/test.webp',
      'production_status'=>'PASS','core_audit_semantic_fit'=>'PASS',
      'core_audit_final_verdict'=>'PASS'
    ];
  }
}
function sanitize_key($v){return strtolower(preg_replace('/[^a-zA-Z0-9_-]/','',str_replace(' ','-',(string)$v)));}
function sanitize_title($v){return sanitize_key($v);}
function sanitize_text_field($v){return trim((string)$v);}
function wp_parse_url($s,$p=-1){return parse_url($s,$p);}
function absint($x){return abs((int)$x);}
function esc_attr($v){return htmlspecialchars((string)$v,ENT_QUOTES|ENT_SUBSTITUTE,'UTF-8');}
function esc_html($v){return htmlspecialchars((string)$v,ENT_QUOTES|ENT_SUBSTITUTE,'UTF-8');}
function esc_url($v){return (string)$v;}
function plugin_dir_path($f){return __DIR__.'/';}
function plugins_url($p,$f=null){return 'https://www.hobby-depot.de/wp-content/plugins/'.ltrim($p,'/');}
function get_the_post_thumbnail_url($id,$size){return $GLOBALS['thumbnail']??'';}
function get_the_ID(){return $GLOBALS['post_id']??0;}
function shortcode_atts($defs,$atts,$name){return array_merge($defs,$atts);}
function is_category(){return (bool)($GLOBALS['archive']??false);}
function get_queried_object(){return $GLOBALS['archive'] ? new WP_Term():null;}
function is_wp_error($v){return false;}
function is_singular($type){return $type==='post' && (bool)($GLOBALS['ispost']??false);}
function in_the_loop(){return true;}
function is_main_query(){return true;}
function is_admin(){return false;}
function is_feed(){return false;}
function is_preview(){return false;}
function post_password_required($id){return false;}
function get_post_field($field,$id){return ($field==='post_content')?'Dummy content':'';}
function has_shortcode($s,$name){return false;}
?>
"""

stub=r"""
class TestAffiliate {
  private function is_enabled(){return true;}
  private function overview_wide_banner_slot($slot){return in_array($slot,['product_after_category_tiles','hub_after_cards','start_after_topics'],true);}
  private function amazon_settings(){return ['enabled'=>true,'tracking_id'=>'testtracking-21'];}
  private function get_category_archive_context($term){return ['post_type'=>'category_archive','primary_name'=>$term->name,'primary_slug'=>$term->slug,'post_id'=>0];}
  private function get_content_context($id){return ['post_type'=>'post','primary_name'=>'Kettenhemdflechten','primary_slug'=>'kettenhemdflechten','post_id'=>$id];}
  private function render_affiliate_slot($id,$slot,$intent,$group){return $this->hdar_ci_amazon_banner($this->get_content_context($id),$slot,(string)$id);}
  private function render_affiliate_slot_for_context($id,$context,$slot,$intent,$group){return $this->hdar_ci_amazon_banner($context,$slot,(string)$id);}
  private function insert_after_paragraph($content,$html,$number){$parts=explode('</p>',$content);if(count($parts)<2)return $content.$html;$pos=max(0,min($number,count($parts)-1));$parts[$pos-1].='</p>'.$html;return implode('</p>',array_filter($parts,fn($x)=>$x!==''));}
"""
# The simplified insertion stub is used only to prove HTML fallback invocation.
# It never replaces real HD009's existing insertion routine.

CASES={
  "register_photo":r"""
    $ctx=['primary_name'=>'Alabasterschnitzen','post_type'=>'hobbyregister_profile','post_id'=>0];
    $row=['canonical_name'=>'Alabasterschnitzen','registry_id'=>'r1'];
    $square=$p->call_banner($ctx,'glossary_single_desktop_banner','hr',$row);
    $wide=$p->call_banner($ctx,'post_inline_banner','hr',$row);
    assert(strpos($square,'hdar-ci-amazon-banner-text')!==false);
    assert(substr_count($square,'<img')===1);
    assert(strpos($wide,'hdar-ci-amazon-banner-text')===false);
    assert(substr_count($wide,'<img')===2);
    assert(strpos($wide,'alabasterschnitzen')!==false || strpos($wide,'Alabasterschnitzen')!==false);
    print("REGISTER_PHOTO_VARIANT_PASS\n");
  """,
  "register_no_photo":r"""
    $ctx=['primary_name'=>'Münzen','post_type'=>'hobbyregister_profile','post_id'=>0];
    $square=$p->call_banner($ctx,'glossary_single_desktop_banner','hr');
    $wide=$p->call_banner($ctx,'post_inline_banner','hr');
    assert(substr_count($square,'<img')===1);
    assert(substr_count($wide,'<img')===1);
    assert(strpos($square,'hdar-ci-amazon-banner-text')!==false);
    assert(strpos($wide,'amazon.de/s?k=')!==false);
    print("REGISTER_NO_IMAGE_FALLBACK_PASS\n");
  """,
  "category_archive_no_global_post":r"""
    $GLOBALS['archive']=true;$GLOBALS['post_id']=0;
    $html=$p->shortcode_affiliate_slot(['type'=>'product_after_category_tiles','intent'=>'portal_context']);
    assert(strpos($html,'Münzen')!==false);
    assert(strpos($html,'hdar-ci-amazon-banner-text')!==false);
    print("CATEGORY_TERM_CONTEXT_PASS\n");
  """,
  "article_no_partner":r"""
    $GLOBALS['ispost']=true;$GLOBALS['post_id']=123;
    $h=$p->call_article('<p>Einleitung</p><p>Mehr Informationen</p><p>Weitere Details</p>');
    assert(strpos($h,'hdar-ci-amazon-banner-text')!==false);
    assert(strpos($h,'Kettenhemdflechten')!==false);
    assert(strpos($h,'amazon.de/s?k=')!==false);
    print("POST_EMPTY_FALLBACK_PASS\n");
  """,
  "article_existing_partner":r"""
    $GLOBALS['ispost']=true;$GLOBALS['post_id']=123;
    $h=$p->call_article('<div class="ppar-affiliate-slot">Bestehende Anzeige</div><p>Text</p>');
    assert(substr_count($h,'ppar-affiliate-slot')===1);
    assert(strpos($h,'hdar-ci-amazon-banner-text')===false);
    print("POST_PARTNER_PRIORITY_PASS\n");
  """,
  "home_broad_topic":r"""
    $ctx=['primary_name'=>'Hobby Depot','post_type'=>'page','post_id'=>0];
    $h=$p->call_banner($ctx,'start_after_topics','index');
    assert(strpos($h,'Hobby-Ausrüstung')!==false);
    assert(strpos($h,'hdar-ci-amazon-banner-text')!==false);
    print("HOME_EXISTING_SLOT_PASS\n");
  """
}

with TemporaryDirectory() as d:
    root=Path(d)
    (root/"assets").mkdir()
    (root/"assets"/Path(BADGE).name).write_bytes(badge)
    for case,code in CASES.items():
        class_code=stub+builder+"\n"+shortcode+"\n"+fallback+r"""
  public function call_banner($c,$slot,$id,$row=null){return $this->hdar_ci_amazon_banner($c,$slot,$id,$row);}
  public function call_article($html){return $this->hdar_ci_article_empty_banner($html);}
}
"""
        php=FAKES.replace("?>","")+ "\n"+class_code+"\n $p=new TestAffiliate;\n"+code
        path=root/f"test-{case}.php"
        path.write_text(php)
        lint=subprocess.run(['php','-l',str(path)],text=True,capture_output=True)
        assert lint.returncode==0,(case,lint.stderr)
        run=subprocess.run(['php','-d','zend.assertions=1','-d','assert.exception=1',str(path)],text=True,capture_output=True)
        assert run.returncode==0,(case,run.stderr,run.stdout)
        print(run.stdout.strip())
print("COVERAGE_PHP_UNIT_TESTS_PASS",len(CASES))
