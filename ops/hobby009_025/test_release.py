#!/usr/bin/env python3
"""Executable PHP tests of the REAL HD009 image selection methods, not a mock rewrite."""
from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZipFile
import subprocess

ROOT=Path("protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/PLUGINS/ISOLIERTE_PLUGINS/HD-009-AFFILIATE-ZENTRALE")
with ZipFile(ROOT/"CURRENT.zip") as z:
    s=z.read("affiliate-portal-router/hobby-depot-affiliate-router.php").decode()
    p=z.read("affiliate-portal-router/assets/hdar-amazon-available-at-amazon-de-official.png")
    assets={n.split("/")[-1]:z.read(n) for n in z.namelist() if n.startswith("affiliate-portal-router/assets/hdar-world-")}
    assert len(assets)==8
a=s.index("    private function hdar_ci_banner_world(")
b=s.index("    /** HD007 owns the register markup",a)
methods=s[a:b]
assert methods.count("function hdar_ci_amazon_banner(")==1
php=r"""<?php
error_reporting(E_ALL);
define('ABSPATH','/tmp/');
class HDAR_Amazon_Start {
  public static function launch_active(){return true;}
}
class HD_Hobbyregister_Core_Stable127{
 public static function image_entry($id){return ['source'=>'hd007','path'=>'portraits/sample.webp','production_status'=>'PASS','core_audit_semantic_fit'=>'PASS','core_audit_final_verdict'=>'PASS'];}
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
function plugins_url($p,$f=null){return 'https://hobby-depot.de/wp-content/plugins/'.ltrim($p,'/');}
function get_the_post_thumbnail_url($id,$size){return 'https://hobby-depot.de/hero-original.webp';}
function is_wp_error($x){return false;}
class Test{
 private function is_enabled(){return true;}
 private function amazon_settings(){return ['enabled'=>true,'tracking_id'=>'example-21'];}
 private function overview_wide_banner_slot($slot){return in_array($slot,['hub_after_cards','product_after_category_tiles','start_after_topics','category_recommendation'],true);}
""" +methods+ """
 public function banner($context,$slot,$row=null){return $this->hdar_ci_amazon_banner($context,$slot,123,$row);}
}
$p=new Test();
"""
CASES={
"architekturmodellbau":r"""
$ctx=['post_type'=>'page','primary_name'=>'Architekturmodellbau','primary_slug'=>'architekturmodellbau','post_id'=>44,
'slugs'=>['architekturmodellbau','miniaturen-szenen','gestalten']];
$h=$p->banner($ctx,'product_after_category_tiles');
assert(strpos($h,'hdar-world-gestalten.webp')!==false);
assert(strpos($h,'hero-original.webp')===false);
assert(strpos($h,'hdar-ci-amazon-banner-category')!==false);
assert(strpos($h,'Ausrüstung und Zubehör entdecken')!==false);
assert(strpos($h,'hdar-amazon-available-at-amazon-de-official.png')!==false);
echo "ARCHITEKTUR_CATEGORY_PHOTO_DIFFERS_FROM_HERO_PASS\n";
""",
"tiere":r"""
$ctx=['post_type'=>'page','primary_name'=>'Terraristik','post_id'=>50,
'slugs'=>['terraristik','tiere']];
$h=$p->banner($ctx,'hub_after_cards');
assert(strpos($h,'hdar-world-tiere.webp')!==false);
assert(strpos($h,'hero-original.webp')===false);
echo "ANIMAL_WORLD_USES_TERRARIUM_PASS\n";
""",
"sammeln":r"""
$ctx=['post_type'=>'category_archive','primary_name'=>'Münzen','post_id'=>0,'slugs'=>['muenzen','sammeln']];
$h=$p->banner($ctx,'product_after_category_tiles');
assert(strpos($h,'hdar-world-sammeln.webp')!==false);
assert(strpos($h,'amazon.de/s?k=M')!==false);
echo "CATEGORY_TERM_WORLD_PHOTO_PASS\n";
""",
"register_square":r"""
$ctx=['post_type'=>'hobbyregister_profile','primary_name'=>'Kameras reparieren','post_id'=>0,'slugs'=>['kameras']];
$row=['canonical_name'=>'Kameras reparieren','registry_id'=>'hobby:camera',
'source_identity'=>['natural_world'=>null]];
$h=$p->banner($ctx,'glossary_single_desktop_banner',$row);
assert(strpos($h,'hdar-ci-amazon-banner-square')!==false);
assert(strpos($h,'portraits/sample.webp')!==false);
assert(strpos($h,'hdar-ci-amazon-banner-text')===false);
echo "REGISTER_SQUARE_USES_APPROVED_HERO_PHOTO_PASS\n";
""",
"register_wide":r"""
$ctx=['post_type'=>'hobbyregister_profile','primary_name'=>'Kameras reparieren','post_id'=>0,'slugs'=>['kameras']];
$row=['canonical_name'=>'Kameras reparieren','registry_id'=>'hobby:camera',
'source_identity'=>['natural_world'=>null]];
$h=$p->banner($ctx,'post_inline_banner',$row);
assert(strpos($h,'portraits/sample.webp')!==false);
assert(strpos($h,'hdar-ci-amazon-banner-category')===false);
echo "REGISTER_WIDE_UNCHANGED_RATIO_PASS\n";
"""
}
with TemporaryDirectory() as d:
    root=Path(d)
    (root/"assets").mkdir()
    (root/"assets"/"hdar-amazon-available-at-amazon-de-official.png").write_bytes(p)
    for filename,data in assets.items():(root/"assets"/filename).write_bytes(data)
    for name,case in CASES.items():
        file=root/f"{name}.php"
        file.write_text(php+case)
        lint=subprocess.run(["php","-l",str(file)],capture_output=True,text=True)
        assert lint.returncode==0,(name,lint.stderr)
        r=subprocess.run(["php","-d","zend.assertions=1","-d","assert.exception=1",str(file)],capture_output=True,text=True)
        assert r.returncode==0,(name,r.stderr,r.stdout)
        print(r.stdout.strip())
print("HD009_025_PHP_UNIT_TESTS_PASS",len(CASES))
