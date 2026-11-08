#!/usr/bin/env python3
"""Execute the exact changed methods from both candidate WordPress plugin ZIPs."""
from pathlib import Path
from zipfile import ZipFile
from tempfile import TemporaryDirectory
from hashlib import sha256
import subprocess,json,re

BASE=Path("protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/PLUGINS/ISOLIERTE_PLUGINS")
AD=BASE/"HD-009-AFFILIATE-ZENTRALE"/"CURRENT.zip"
DESIGN=BASE/"HD-003-DESIGN-TEMPLATE-KIT"/"CURRENT.zip"
with ZipFile(AD) as ad,ZipFile(DESIGN) as design:
    a=ad.read("affiliate-portal-router/hobby-depot-affiliate-router.php").decode()
    d=design.read("affiliate-portal-template-kit/includes/class-hobby-depot-profile-v150709.php").decode()
    leaf=design.read("affiliate-portal-template-kit/assets/hobby-depot-v150750/leaf-category-map-v150750.json")
    group=design.read("affiliate-portal-template-kit/assets/hobby-depot-v150617/hero-masters-v150684/wind-drachen.webp")
    hobby=design.read("affiliate-portal-template-kit/assets/hobby-depot-v150780/hobby-masters/sportdrachen.webp")
    world=design.read("affiliate-portal-template-kit/assets/hobby-depot-v150617/start-world-v150691/bewegen.webp")
    badge=ad.read("affiliate-portal-router/assets/hdar-amazon-available-at-amazon-de-official.png")
    for row in ("sportdrachen-drachen-leinen","sportdrachen-steuerung-figuren","sportdrachen-einstieg-wind"):
        entry=json.loads(leaf)[row]
        assert entry['chain'][0]['path']=='bewegen'
        assert entry['chain'][1]['path']=='bewegen/wind-drachen'
        assert entry['parent_slug']=='sportdrachen'
    print("AUTHORITATIVE_SPORTDRACHEN_MAP_PASS",len(json.loads(leaf)),"entries")
    assert a.count('function hdar_ci_leaf_category_photo_meta(')==1
    assert d.count('function post_preview_photo_v150803(')==1
    assert a.count('hdar_ci_leaf_category_photo_meta($context)')==2
    assert d.count('self::post_preview_photo_v150803($post)')==3

start=a.index("    private function hdar_ci_leaf_category_photo_meta(")
end=a.index("    /** HD007 owns the register markup",start)
ad_methods=a[start:end]
helper_start=d.index("    private static function post_preview_photo_v150803(")
helper_end=d.index("    private static function render_post_previews(",helper_start)
card_method=d[helper_start:helper_end]
stubs=r"""<?php
error_reporting(E_ALL);
define('ABSPATH','/tmp/');
define('WP_PLUGIN_DIR', dirname(dirname(__DIR__)));
class WP_Term {
 public $slug='sportdrachen-drachen-leinen',$taxonomy='category',$term_id=5112;
}
class WP_Post {
 public $ID=904015;
}
class HDAR_Amazon_Start {public static function launch_active(){return true;}}
function sanitize_key($v){return strtolower(preg_replace('/[^a-zA-Z0-9_-]/','',str_replace(' ','-',(string)$v)));}
function sanitize_title($v){return sanitize_key($v);}
function sanitize_text_field($v){return trim((string)$v);}
function absint($v){return abs((int)$v);}
function esc_html($v){return htmlspecialchars((string)$v,ENT_QUOTES|ENT_SUBSTITUTE,'UTF-8');}
function esc_attr($v){return htmlspecialchars((string)$v,ENT_QUOTES|ENT_SUBSTITUTE,'UTF-8');}
function esc_url($v){return (string)$v;}
function wp_parse_url($x,$component=-1){return parse_url($x,$component);}
function plugins_url($path,$source=null){return 'https://www.hobby-depot.de/wp-content/plugins/'.ltrim($path,'/');}
function plugin_dir_path($file){return WP_PLUGIN_DIR.'/';}
function get_the_post_thumbnail_url($id,$size){return $GLOBALS['thumb']??'';}
function get_the_category($id){return [new WP_Term];}
function is_wp_error($v){return false;}
"""
# Plugin-dir relative to __FILE__ test file needs the HD009 images copied into
# test root/assets. In real WP, the files sit inside affiliate-portal-router/.
with TemporaryDirectory() as td:
    root=Path(td)
    (root/"affiliate-portal-template-kit/assets/hobby-depot-v150750").mkdir(parents=True)
    (root/"affiliate-portal-template-kit/assets/hobby-depot-v150750/leaf-category-map-v150750.json").write_bytes(leaf)
    (root/"affiliate-portal-template-kit/assets/hobby-depot-v150617/hero-masters-v150684").mkdir(parents=True)
    (root/"affiliate-portal-template-kit/assets/hobby-depot-v150617/hero-masters-v150684/wind-drachen.webp").write_bytes(group)
    (root/"affiliate-portal-template-kit/assets/hobby-depot-v150780/hobby-masters").mkdir(parents=True)
    (root/"affiliate-portal-template-kit/assets/hobby-depot-v150780/hobby-masters/sportdrachen.webp").write_bytes(hobby)
    (root/"affiliate-portal-template-kit/assets/hobby-depot-v150617/start-world-v150691").mkdir(parents=True)
    (root/"affiliate-portal-template-kit/assets/hobby-depot-v150617/start-world-v150691/bewegen.webp").write_bytes(world)
    (root/"assets").mkdir()
    (root/"assets/hdar-amazon-available-at-amazon-de-official.png").write_bytes(badge)
    with ZipFile(AD) as ad:
        for n in ad.namelist():
            if "/assets/hdar-world-" in n:
                (root/"assets"/n.split("/")[-1]).write_bytes(ad.read(n))
    code=stubs+"""
class BannerFixture {
  private function is_enabled(){return true;}
  private function overview_wide_banner_slot($slot){return in_array($slot,['product_after_category_tiles','hub_after_cards','start_after_topics'],true);}
  private function amazon_settings(){return ['enabled'=>true,'tracking_id'=>'hobbydepot-21'];}
"""+ad_methods+"""
  public function render($ctx){return $this->hdar_ci_amazon_banner($ctx,'product_after_category_tiles','term_5112');}
}
class CardFixture {
  private static function leaf_category_meta_v150750($term){
    $map=json_decode(file_get_contents(WP_PLUGIN_DIR.'/affiliate-portal-template-kit/assets/hobby-depot-v150750/leaf-category-map-v150750.json'),true);
    return $map[$term->slug]??null;
  }
  private static function asset_url($name){return plugins_url('affiliate-portal-template-kit/assets/hobby-depot-v150617/'.ltrim($name,'/'));}
"""+card_method+"""
  public static function photo($post){return self::post_preview_photo_v150803($post);}
}
$banner=(new BannerFixture)->render(['post_type'=>'category_archive',
  'primary_name'=>'Drachen & Leinen','primary_slug'=>'sportdrachen-drachen-leinen',
  'slugs'=>['sportdrachen-drachen-leinen'],'post_id'=>0]);
assert(strpos($banner,'hero-masters-v150684/wind-drachen.webp')!==false,'wrong banner photo');
assert(strpos($banner,'hdar-ci-amazon-banner-text')===false,'unwanted text-only banner');
assert(strpos($banner,'hdar-ci-amazon-banner-category')!==false);
assert(substr_count($banner,'<img')===2,'must be one topic photo + one official Amazon badge');
print("SPORT_KITE_CATEGORY_BANNER_HAS_CORRECT_PHOTO_PASS\\n");
$post=new WP_Post;
$GLOBALS['thumb']='';
$preview=CardFixture::photo($post);
assert(strpos($preview,'hobby-masters/sportdrachen.webp')!==false,'wrong article preview fallback');
assert($preview!=='' && strpos($preview,'wind-drachen.webp')===false);
print("ARTICLE_WITHOUT_FEATURED_IMAGE_USES_MATCHING_KITE_PHOTO_PASS\\n");
$GLOBALS['thumb']='https://example.org/my-real-featured-photo.jpg';
$preview=CardFixture::photo($post);
assert($preview===$GLOBALS['thumb'],'featured image must win');
print("EXISTING_ARTICLE_FEATURED_IMAGE_PRECEDENCE_PASS\\n");
"""
    # The helper includes no dynamic memory; all 3 renderers call it by static name.
    for case in ["all"]:
        f=root/"affiliate-portal-template-kit/includes/test.php";f.parent.mkdir(parents=True,exist_ok=True);f.write_text(code)
        p=subprocess.run(["php","-l",str(f)],text=True,capture_output=True)
        assert p.returncode==0,(p.stdout,p.stderr)
        r=subprocess.run(["php","-d","zend.assertions=1","-d","assert.exception=1",str(f)],text=True,capture_output=True)
        assert r.returncode==0,(r.stdout,r.stderr)
        print(r.stdout.strip())
print("HD009_HD003_BOTH_PLUGIN_FUNCTION_TESTS_PASS")
