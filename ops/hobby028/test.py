#!/usr/bin/env python3
"""Prove the real 0.1.28 PHP map + banner code works on all four category tiers.
No mock replacement of the two changed methods; stubs only for WordPress APIs.
"""
from pathlib import Path
from zipfile import ZipFile
from tempfile import TemporaryDirectory
import json,subprocess,collections,hashlib

ROOT=Path('protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/PLUGINS/ISOLIERTE_PLUGINS')
with ZipFile(ROOT/'HD-003-DESIGN-TEMPLATE-KIT'/'CURRENT.zip') as des, ZipFile(ROOT/'HD-009-AFFILIATE-ZENTRALE'/'CURRENT.zip') as ad:
  source=ad.read('affiliate-portal-router/hobby-depot-affiliate-router.php').decode()
  adworld={n.split('/')[-1]:ad.read(n) for n in ad.namelist() if n.startswith('affiliate-portal-router/assets/hdar-world-')}
  badge=ad.read('affiliate-portal-router/assets/hdar-amazon-available-at-amazon-de-official.png')
  data=des.read('affiliate-portal-template-kit/assets/hobby-depot-v150750/leaf-category-map-v150750.json')
  entries=json.loads(data)
  page_map=json.loads(des.read('affiliate-portal-template-kit/assets/hobby-depot-v150687/category-level-copy-v150687.json'))
  allfiles=set(des.namelist())
  print('METHOD_DEBUG',source.find('hdar_ci_banner_world'),source[source.find('hdar_ci_banner_world')-90:source.find('hdar_ci_banner_world')+120])
  begin=source.index('private function hdar_ci_banner_world(')
  end=source.index('    /** HD007 owns the register markup',begin)
  methods=source[begin:end]
  assert methods.count('function hdar_ci_amazon_banner(')==1
  assert methods.count('function hdar_ci_category_photo_meta(')==1
  assert len(adworld)==8

  def lookup(row):
    chain=row.get('chain') or []
    world=(chain[0].get('path') or '').split('/')[0] if chain else ''
    group=(chain[1].get('path') or '').split('/')[-1] if len(chain)>1 else ''
    hobby=row.get('parent_slug','')
    return world,group,hobby
  worlds={'gestalten','fertigen','technik','forschen','pflanzen','tiere','bewegen','sammeln'}
  grouped={}
  groupworld={}
  for leaf,item in entries.items():
    w,g,h=lookup(item)
    assert w in worlds and g and h,(leaf,w,g,h)
    assert g not in groupworld or groupworld[g]==w,(leaf,g,groupworld.get(g),w)
    assert h not in grouped or grouped[h]==(w,g),(leaf,h,grouped.get(h),(w,g))
    groupworld[g]=w
    grouped[h]=w,g
  assert len(entries)==3376
  print('LEVEL_COUNTS',{'worlds':len(worlds),'groups':len(groupworld),'hobbies':len(grouped),'leaf_categories':len(entries),'page_definitions':len(page_map)})
  # Every canonical hobby page belongs to the existing authoritative leaf map.
  known_hobbies={slug for slug,obj in page_map.items() if obj.get('object_type')=='page'}
  absent=known_hobbies-set(grouped)
  print('HOBBY_PAGE_MAPPING_GAPS',len(absent),sorted(absent)[:16])
  direct_categories={slug:row for slug,row in page_map.items() if row.get('object_type')=='category'}
  print('DIRECT_CATEGORY_DEFINITIONS',len(direct_categories),[(k,v.get('world'),v.get('parent')) for k,v in list(direct_categories.items())[:28]])
  print('DIRECT_CATEGORY_UNMAPPED',[(slug,entry.get('world'),entry.get('parent')) for slug,entry in direct_categories.items() if slug not in entries])
  available_master={n.rsplit('/',1)[-1].removesuffix('.webp') for n in allfiles if '/hobby-masters/' in n and n.endswith('.webp')}
  alt_counts=collections.Counter()
  missing_alt=[]
  for group,world in groupworld.items():
    alternates=[h for h,(w,g) in grouped.items() if g==group and h in available_master]
    alt_counts[len(alternates)>0]+=1
    if not alternates:missing_alt.append((world,group))
  print('GROUP_ALTERNATE_HOBBY_PHOTOS',dict(alt_counts),'WITHOUT',missing_alt[:30])

  # The existing category image collection must be complete for group-level photos.
  missing_group_photos=[(w,g) for g,w in groupworld.items()
    if 'affiliate-portal-template-kit/assets/hobby-depot-v150617/hero-masters-v150684/'+g+'.webp' not in allfiles]
  print('MISSING_GROUP_PHOTOS',len(missing_group_photos),missing_group_photos[:18])
  assert not missing_group_photos, "No generic hiking images as replacements for a known group."
  # HD003 catalog is still the authority, not inferred from blog text.
  assert not absent, "All 395 canonical hobby pages must be covered."

  stubs=r"""<?php
error_reporting(E_ALL);
define('ABSPATH','/tmp/');
define('WP_PLUGIN_DIR', dirname(__DIR__));
class HDAR_Amazon_Start {public static function launch_active(){return true;}}
function sanitize_key($v){return strtolower(preg_replace('/[^a-zA-Z0-9_-]/','',str_replace(' ','-',(string)$v)));}
function sanitize_title($v){return sanitize_key($v);}
function sanitize_text_field($v){return trim((string)$v);}
function absint($v){return abs((int)$v);}
function esc_attr($v){return htmlspecialchars((string)$v,ENT_QUOTES|ENT_SUBSTITUTE,'UTF-8');}
function esc_html($v){return htmlspecialchars((string)$v,ENT_QUOTES|ENT_SUBSTITUTE,'UTF-8');}
function esc_url($v){return (string)$v;}
function wp_parse_url($x,$component=-1){return parse_url($x,$component);}
function is_wp_error($x){return false;}
function plugin_dir_path($file){return dirname($file).'/';}
function plugins_url($file,$plugin=null){return 'https://www.hobby-depot.de/wp-content/plugins/'.ltrim($file,'/');}
function get_the_post_thumbnail_url($id,$size){return '';}
class Test {
  private function is_enabled(){return true;}
  private function overview_wide_banner_slot($slot){return in_array($slot,['product_after_category_tiles','hub_after_cards','start_after_topics'],true);}
  private function amazon_settings(){return ['enabled'=>true,'tracking_id'=>'example-21'];}
""" +methods+"""
  public function banner($c,$id){return $this->hdar_ci_amazon_banner($c,'product_after_category_tiles',$id);}
  public function meta($c){return $this->hdar_ci_category_photo_meta($c);}
}
$p=new Test();
"""
  cases=[
   ('welt_bewegen',{'post_type':'page','primary_slug':'bewegen','primary_name':'Bewegen','slugs':['bewegen'],'post_id':1},'hdar-world-bewegen.webp'),
   ('welt_technik',{'post_type':'page','primary_slug':'technik','primary_name':'Technik','slugs':['technik'],'post_id':2},'hdar-world-technik.webp'),
   ('gruppe_wind_drachen',{'post_type':'page','primary_slug':'wind-drachen','primary_name':'Wind & Drachen','slugs':['wind-drachen','bewegen'],'post_id':3},'lenkdrachen-testfoto.jpg'),
   ('hobby_sportdrachen',{'post_type':'page','primary_slug':'sportdrachen','primary_name':'Sportdrachen','slugs':['sportdrachen','wind-drachen','bewegen'],'post_id':4},'hero-masters-v150684/wind-drachen.webp'),
   ('blatt_drachen_leinen',{'post_type':'category_archive','primary_slug':'sportdrachen-drachen-leinen','primary_name':'Drachen & Leinen','slugs':['sportdrachen-drachen-leinen'],'post_id':0},'hero-masters-v150684/wind-drachen.webp'),
   ('hobby_architekturmodellbau',{'post_type':'page','primary_slug':'architekturmodellbau','primary_name':'Architekturmodellbau','slugs':['architekturmodellbau','miniaturen-szenen','gestalten'],'post_id':5},'hero-masters-v150684/miniaturen-szenen.webp'),
   ('gruppe_minis',{'post_type':'page','primary_slug':'miniaturen-szenen','primary_name':'Miniaturen & Szenen','slugs':['miniaturen-szenen','gestalten'],'post_id':6},'hero-masters-v150684/miniaturen-szenen.webp'),
   ('blatt_muenzen',{'post_type':'category_archive','primary_slug':'sportdrachen-einstieg-wind','primary_name':'Einstieg & Wind','slugs':['sportdrachen-einstieg-wind'],'post_id':0},'hero-masters-v150684/wind-drachen.webp'),
  ]
  with TemporaryDirectory() as tmp:
    root=Path(tmp)
    asset=root/'affiliate-portal-template-kit/assets/hobby-depot-v150750/leaf-category-map-v150750.json'
    asset.parent.mkdir(parents=True);asset.write_bytes(data)
    for w,g in set((w,g) for w,g,_ in [lookup(v) for v in entries.values()]):
      name='affiliate-portal-template-kit/assets/hobby-depot-v150617/hero-masters-v150684/'+g+'.webp'
      path=root/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(des.read(name))
    alt='affiliate-portal-template-kit/assets/hobby-depot-v150787/lenkdrachen-testfoto.jpg'
    p=root/alt;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(des.read(alt))
    pdir=root/'affiliate-portal-router';pdir.mkdir()
    (pdir/'assets').mkdir()
    for name,data in adworld.items():(pdir/'assets'/name).write_bytes(data)
    (pdir/'assets/hdar-amazon-available-at-amazon-de-official.png').write_bytes(badge)
    for name,context,want in cases:
      php=pdir/(name+'.php')
      php.write_text(stubs+'\n'+ '$ctx=json_decode('+json.dumps(json.dumps(context,ensure_ascii=False)) +',true);'+r"""
$meta=$p->meta($ctx);
assert(is_array($meta));
$markup=$p->banner($ctx,'id');
assert($markup!=='','No banner');
assert(strpos($markup,'hdar-ci-amazon-banner-text')===false,'Text-only banner forbidden');
assert(substr_count($markup,'<img')===2,'Exact thematic photo + official Amazon badge');
assert(strpos($markup,'hdar-ci-amazon-banner-category')!==false,'Category style missing');
echo $markup;
""")
      lint=subprocess.run(['php','-l',str(php)],capture_output=True,text=True)
      assert lint.returncode==0,(name,lint.stderr)
      run=subprocess.run(['php','-d','zend.assertions=1','-d','assert.exception=1',str(php)],capture_output=True,text=True)
      assert run.returncode==0,(name,run.stderr[:1000])
      assert want in run.stdout,(name,want,run.stdout[:1100])
      print('PHP_ALL_TIERS_PASS',name,'photo',want)
print('HD009_028_ALL_TIERS_COMPLETE_TESTS_PASS')
