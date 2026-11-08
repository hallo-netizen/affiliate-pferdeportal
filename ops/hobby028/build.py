#!/usr/bin/env python3
"""HD009 0.1.28: one shared category photo source for all hierarchy levels.
The existing 3,376-entry HD003 leaf map is already the system authority; use
its full tree (world, group, hobby, leaf), not only the leaf key.
No other plugin changes; preserve existing contracts and all other ad slots.
"""
from pathlib import Path
from zipfile import ZipFile
from tempfile import TemporaryDirectory
from io import BytesIO
from hashlib import sha256
import subprocess

ROOT=Path("protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/PLUGINS/ISOLIERTE_PLUGINS/HD-009-AFFILIATE-ZENTRALE")
FILE=ROOT/"HOBBY_DEPOT_AFFILIATE_HD009_0.1.27.zip"
EXPECTED="bba83f67e48039bf921709823d81fc00b7658b7e9c825a833314f6821ff0a2fd"
MAIN="affiliate-portal-router/hobby-depot-affiliate-router.php"
CACHE="affiliate-portal-router/includes/class-hdar-amazon-start.php"
OUT="HOBBY_DEPOT_AFFILIATE_HD009_0.1.28.zip"

def once(src,before,after,why):
  n=src.count(before)
  assert n==1,(why,n,before[:100])
  return src.replace(before,after)

# The previously leaf-only lookup is replaced with one index that also serves
# hub group pages and hobby pages, from the same file already shipped in HD003.
full_method=r'''    // Existing eight-world resolver is preserved verbatim.
    private function hdar_ci_banner_world($context, $register_row = null) {
        $allowed = array('gestalten','fertigen','technik','forschen',
                         'pflanzen','tiere','bewegen','sammeln');
        if (is_array($register_row)) {
            $w = sanitize_key((string)($register_row['source_identity']['natural_world'] ?? ''));
            if (in_array($w,$allowed,true)) { return $w; }
        }
        foreach ((array)($context['slugs'] ?? array()) as $slug) {
            $slug = sanitize_key((string)$slug);
            if (in_array($slug,$allowed,true)) { return $slug; }
        }
        return '';
    }

    // Exactly one source of hierarchy truth across the whole Hobby Depot.
    // The official HD003 leaf map contains world, middle group and hobby for
    // every leaf. Build shared indices once per request and use at all tiers.
    private function hdar_ci_category_photo_meta($context) {
        $post_type = (string)($context['post_type'] ?? '');
        if (!in_array($post_type, array('page','category_archive'), true)) { return array(); }
        $slug = sanitize_key((string)($context['primary_slug'] ?? ''));
        if ($slug === '' || !defined('WP_PLUGIN_DIR')) { return array(); }
        static $catalog = null;
        if ($catalog === null) {
            $catalog = array('leaf'=>array(),'hobby'=>array(),'group'=>array());
            $file = WP_PLUGIN_DIR . '/affiliate-portal-template-kit/assets/hobby-depot-v150750/leaf-category-map-v150750.json';
            if (is_file($file)) {
                $entries = json_decode((string)file_get_contents($file),true);
                if (is_array($entries)) {
                    $valid = array('gestalten','fertigen','technik','forschen',
                                   'pflanzen','tiere','bewegen','sammeln');
                    foreach ($entries as $leaf_slug=>$entry) {
                        if (!is_array($entry)) { continue; }
                        $chain = (array)($entry['chain'] ?? array());
                        $root_path = trim((string)($chain[0]['path'] ?? ''),'/');
                        $world = sanitize_key(explode('/', $root_path)[0]);
                        if (!in_array($world,$valid,true)) { continue; }
                        $group_path = trim((string)($chain[1]['path'] ?? ''),'/');
                        $group = sanitize_key((string)basename($group_path));
                        $hobby = sanitize_key((string)($entry['parent_slug'] ?? ''));
                        if ($group === '' || $hobby === '') { continue; }
                        // Invalid/colliding source records must not silently
                        // overwrite the hierarchy chosen by HD003.
                        $info = array('world'=>$world,'subgroup'=>$group,'parent'=>$hobby);
                        $catalog['leaf'][sanitize_key((string)$leaf_slug)] = $info;
                        if (!isset($catalog['hobby'][$hobby])) {
                            $catalog['hobby'][$hobby] = $info;
                        }
                        if (!isset($catalog['group'][$group])) {
                            $catalog['group'][$group] = array('world'=>$world,'subgroup'=>$group,'parent'=>'');
                        }
                    }
                }
            }
        }
        if ($post_type === 'category_archive') {
            return $catalog['leaf'][$slug] ?? array();
        }
        // A hub 2 page (e.g. /bewegen/wind-drachen/) is indexed by
        // the real subgroup slug; a hub 3 page by its hobby slug.
        if (isset($catalog['group'][$slug])) {
            $meta=$catalog['group'][$slug];
            $meta['level']='group';
            return $meta;
        }
        if (isset($catalog['hobby'][$slug])) {
            $meta=$catalog['hobby'][$slug];
            $meta['level']='hobby';
            return $meta;
        }
        // Main world pages need only their already packaged universal photo.
        if (in_array($slug,array('gestalten','fertigen','technik','forschen',
            'pflanzen','tiere','bewegen','sammeln'),true)) {
            return array('world'=>$slug,'subgroup'=>'','parent'=>'','level'=>'world');
        }
        // If this published page was not part of the audited tree, do
        // not guess from its title or unrelated body text.
        return array();
    }

'''
with ZipFile(FILE) as z:
  assert z.testzip() is None
  s=z.read(MAIN).decode()
  old_start=s.index("    private function hdar_ci_leaf_category_photo_meta(")
  old_end=s.index("    /** HD007 owns the register markup",old_start)
  segment=s[old_start:old_end]
  assert segment.startswith("    private function hdar_ci_leaf_category_photo_meta")
  assert "private function hdar_ci_amazon_banner(" in segment
  photo_index=segment.index("    private function hdar_ci_amazon_banner(")
  banner=segment[photo_index:]
  assert "hdar_ci_leaf_category_photo_meta($context)" in banner
  banner=once(banner,"hdar_ci_leaf_category_photo_meta($context)","hdar_ci_category_photo_meta($context)","new all tiers mapping")
  # Need world metadata for all page types without changes to category slot ownership.
  before="""        if ($world === '' && !empty($leaf_photo['world'])) { $world = (string)$leaf_photo['world']; }"""
  after="""        if ($world === '' && !empty($leaf_photo['world'])) { $world = (string)$leaf_photo['world']; }"""
  assert banner.count(before)==1
  # Rewrite existing previously leaf-only photo override. The first world
  # photo remains the guaranteed relevant image for all eight core worlds.
  photo_start=banner.index("        // The HD003 world image is the guaranteed baseline.")
  photo_end=banner.index("        // Register square: use the approved topic photo",photo_start)
  replacement=r'''        // Central image policy for all category levels: approved group image
        // overrides broad eight-world fallback. This is NOT limited to WP terms.
        // On the group page itself avoid the same hero; for Wind & Drachen,
        // HD003 already contains a distinct, accurate Lenkdrachen test photo.
        if ($category_banner && $world !== '' && !empty($leaf_photo['subgroup'])) {
            $group = sanitize_key((string)$leaf_photo['subgroup']);
            $root = defined('WP_PLUGIN_DIR') ? WP_PLUGIN_DIR . '/affiliate-portal-template-kit/assets/' : '';
            if ($root !== '' && $group !== '') {
                $relative = 'hobby-depot-v150617/hero-masters-v150684/' . $group . '.webp';
                if (($leaf_photo['level'] ?? '') === 'group' && $group === 'wind-drachen') {
                    $alternate = 'hobby-depot-v150787/lenkdrachen-testfoto.jpg';
                    if (is_file($root.$alternate)) { $relative = $alternate; }
                }
                if (is_file($root.$relative)) {
                    $photo = plugins_url('affiliate-portal-template-kit/assets/'.$relative);
                }
            }
        }
        // Other known pages already use a world-specific photo. Do not
        // emit a text-only category banner when a category lacks an image:
        // fail closed rather than present an unapproved, photo-less creative.
        if ($category_banner && $photo === '') { return ''; }
'''
  banner=banner[:photo_start]+replacement+banner[photo_end:]
  updated=s[:old_start]+full_method+banner+s[old_end:]
  updated=once(updated," * Version: 0.1.27"," * Version: 0.1.28","WP Header")
  if " * Version: 0.1.27" in updated: raise AssertionError("Plugin version still old")
  assert updated.count("hdar_ci_category_photo_meta($context)")==2
  assert updated.count("hdar_ci_leaf_category_photo_meta(")==0

out=BytesIO();changed=[]
with ZipFile(FILE) as z,ZipFile(out,'w') as dest:
  assert len(z.namelist())==41
  for info in z.infolist():
    b=z.read(info.filename);a=b
    if info.filename==MAIN:a=updated.encode()
    if info.filename==CACHE:a=once(b.decode(),"'0.1.27'","'0.1.28'","Stylesheet cache").encode()
    if b!=a:changed.append(info.filename)
    dest.writestr(info,a)
  dest.comment=z.comment
assert set(changed)=={MAIN,CACHE},changed
payload=out.getvalue()
with ZipFile(BytesIO(payload)) as z:
  assert z.testzip() is None and len(z.namelist())==41
  with TemporaryDirectory() as tmp:
    phps=[n for n in z.namelist() if n.endswith('.php')]
    assert len(phps)==24
    for n in phps:
      p=Path(tmp)/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(z.read(n))
      lint=subprocess.run(["php","-l",str(p)],capture_output=True,text=True)
      assert lint.returncode==0,(n,lint.stderr)
assert sha256(FILE.read_bytes()).hexdigest()==EXPECTED, "Original source modified"
(ROOT/'CURRENT.zip').write_bytes(payload)
target=ROOT/OUT;target.write_bytes(payload)
assert (ROOT/'CURRENT.zip').read_bytes()==target.read_bytes()
print("HD009_ALL_LEVELS_BUILD_PASS",OUT,"size",len(payload),"sha256",sha256(payload).hexdigest(),"files_changed",changed,"PHP_PASS 24","ZIP_PASS 41")
