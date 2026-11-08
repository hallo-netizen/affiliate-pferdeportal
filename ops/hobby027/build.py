#!/usr/bin/env python3
"""One shared source-of-truth: the existing HD003 leaf-category-map.
HD009 0.1.27 fixes photo-less category banners.
HD003 1.50.803 fixes photo-less article preview cards (only when post has no thumbnail).
Nothing else is changed.
"""
from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZipFile
from io import BytesIO
from hashlib import sha256
import subprocess

ROOT=Path("protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/PLUGINS/ISOLIERTE_PLUGINS")
AD=ROOT/"HD-009-AFFILIATE-ZENTRALE"/"CURRENT.zip"
DESIGN=ROOT/"HD-003-DESIGN-TEMPLATE-KIT"/"CURRENT.zip"
assert sha256(AD.read_bytes()).hexdigest()=="a627e35a9e8d20f34616c1ead4bc1b7d180e40a8f74abb985c7311b60dcfcd8f", "HD009 original changed; abort"
assert sha256(DESIGN.read_bytes()).hexdigest()=="05ea37f040c1189ea9fda29c2dd795740351d83fe8022f8d966a453679fec7a8", "HD003 original changed; abort"

AD_MAIN="affiliate-portal-router/hobby-depot-affiliate-router.php"
AD_LOAD="affiliate-portal-router/includes/class-hdar-amazon-start.php"
DESIGN_MAIN="affiliate-portal-template-kit/pferde-template-kit.php"
DESIGN_PROFILE="affiliate-portal-template-kit/includes/class-hobby-depot-profile-v150709.php"

def single(s,b,a,reason):
    assert s.count(b)==1,(reason,"match count",s.count(b),b[:170])
    return s.replace(b,a)

CATEGORY_META = '''
    // WordPress leaf categories have no WP parent. Reuse the exact 3,376-entry
    // mapping already owned by HD003; never guess from title fragments.
    private function hdar_ci_leaf_category_photo_meta($context) {
        if ((string)($context['post_type'] ?? '') !== 'category_archive') { return array(); }
        $slug = sanitize_key((string)($context['primary_slug'] ?? ''));
        if ($slug === '' || !defined('WP_PLUGIN_DIR')) { return array(); }
        static $map = null;
        if ($map === null) {
            $map = array();
            $file = WP_PLUGIN_DIR . '/affiliate-portal-template-kit/assets/hobby-depot-v150750/leaf-category-map-v150750.json';
            if (is_file($file)) {
                $data = json_decode((string)file_get_contents($file),true);
                if (is_array($data)) { $map = $data; }
            }
        }
        $entry = $map[$slug] ?? null;
        if (!is_array($entry)) { return array(); }
        $chain = (array)($entry['chain'] ?? array());
        $world_path = sanitize_key((string)($chain[0]['path'] ?? ''));
        $world = explode('/', $world_path)[0];
        $subgroup_path = trim((string)($chain[1]['path'] ?? ''),'/');
        $subgroup = sanitize_key((string)basename($subgroup_path));
        $parent = sanitize_key((string)($entry['parent_slug'] ?? ''));
        if (!in_array($world,array('gestalten','fertigen','technik','forschen',
          'pflanzen','tiere','bewegen','sammeln'),true)) { return array(); }
        return array('world'=>$world,'subgroup'=>$subgroup,'parent'=>$parent);
    }

'''
# Avoid sanitizing 'bewegen/wind-drachen' before extraction.
CATEGORY_META=CATEGORY_META.replace("sanitize_key((string)($chain[0]['path'] ?? ''))","(string)($chain[0]['path'] ?? '')")

AD_INSERT_PHOTO = '''
        // The HD003 world image is the guaranteed baseline. Where an exact
        // approved group/hobby photo exists, it is more precise and remains
        // different from the article-preview hobby-master image when possible.
        if ($category_banner && $world !== '' && is_array($leaf_photo)) {
            $group = (string)($leaf_photo['subgroup'] ?? '');
            $parent = (string)($leaf_photo['parent'] ?? '');
            $root = defined('WP_PLUGIN_DIR') ? WP_PLUGIN_DIR . '/affiliate-portal-template-kit/assets/' : '';
            if ($root !== '' && $group !== '') {
                $relative = 'hobby-depot-v150617/hero-masters-v150684/' . $group . '.webp';
                if (is_file($root.$relative)) {
                    $photo = plugins_url('affiliate-portal-template-kit/assets/'.$relative);
                }
            }
            if ($root !== '' && $photo === '' && $parent !== '') {
                $relative = 'hobby-depot-v150780/hobby-masters/' . $parent . '.webp';
                if (is_file($root.$relative)) {
                    $photo = plugins_url('affiliate-portal-template-kit/assets/'.$relative);
                }
            }
        }
'''
# Ensure parent photo can take priority only if group is absent; group is
# preferred to keep banner and post thumbnail visually distinct.

def patch_ad(name,data):
    if name==AD_MAIN:
        s=data.decode()
        s=single(s,"* Version: 0.1.26","* Version: 0.1.27","HD009 plugin header")
        before="    private function hdar_ci_banner_world($context, $register_row = null) {"
        s=single(s,before,CATEGORY_META+before,"Photo meta helper")
        before="        $world = $this->hdar_ci_banner_world($context,$register_row);"
        after=before+"""
        $leaf_photo = $category_banner ? $this->hdar_ci_leaf_category_photo_meta($context) : array();
        if ($world === '' && !empty($leaf_photo['world'])) { $world = (string)$leaf_photo['world']; }"""
        s=single(s,before,after,"HD003 leaf world mapping")
        before="""        // Register square: use the approved topic photo with a different crop."""
        s=single(s,before,AD_INSERT_PHOTO+before,"HD003 topic photo before register")
        return s.encode()
    if name==AD_LOAD:
        s=data.decode()
        s=single(s,"'0.1.26'","'0.1.27'","HD009 cache version")
        return s.encode()
    return data

PREVIEW_HELPER='''
    // One rule for all three existing article-card renderers. A real featured
    // image always wins. Only absent thumbnails use an existing, approved
    // hobby-master picture from HD003's canonical leaf-category mapping.
    private static function post_preview_photo_v150803($post) {
        if (!$post instanceof WP_Post) { return ''; }
        $img = (string)get_the_post_thumbnail_url($post->ID,'medium_large');
        if ($img !== '') { return $img; }
        $terms = get_the_category($post->ID);
        if (!is_array($terms)) { return ''; }
        foreach ($terms as $term) {
            if (!$term instanceof WP_Term || (string)$term->taxonomy !== 'category') { continue; }
            $entry = self::leaf_category_meta_v150750($term);
            if (!is_array($entry)) { continue; }
            $parent = sanitize_title((string)($entry['parent_slug'] ?? ''));
            if ($parent !== '') {
                $relative = 'hobby-depot-v150780/hobby-masters/'.$parent.'.webp';
                if (is_file(dirname(__DIR__).'/assets/'.$relative)) {
                    return plugins_url('affiliate-portal-template-kit/assets/'.$relative);
                }
            }
            $chain = (array)($entry['chain'] ?? array());
            $world_path = trim((string)($chain[0]['path'] ?? ''));
            $world = sanitize_key(explode('/',$world_path)[0]);
            if (in_array($world,array('gestalten','fertigen','technik','forschen',
                  'pflanzen','tiere','bewegen','sammeln'),true)) {
                $relative = 'hobby-depot-v150617/start-world-v150691/'.$world.'.webp';
                if (is_file(dirname(__DIR__).'/assets/'.$relative)) {
                    return self::asset_url('start-world-v150691/'.$world.'.webp');
                }
            }
        }
        return '';
    }

'''
def patch_design(name,data):
    if name==DESIGN_MAIN:
        s=data.decode()
        s=single(s," * Version: 1.50.798"," * Version: 1.50.803","HD003 header")
        s=single(s,"const VERSION = '1.50.798';","const VERSION = '1.50.803';","HD003 const VERSION")
        return s.encode()
    if name==DESIGN_PROFILE:
        s=data.decode()
        s=single(s,"    private static function render_post_previews(",
                 PREVIEW_HELPER+"    private static function render_post_previews(","single card fallback helper")
        old="$img=(string)get_the_post_thumbnail_url($post->ID,'medium_large');"
        assert s.count(old)==3,("Wrong article card renderer count",s.count(old))
        s=s.replace(old,"$img=self::post_preview_photo_v150803($post);")
        return s.encode()
    return data

def build(source,transform,expected_changes,expected_entries,php_count):
    memory=BytesIO();changed=[]
    with ZipFile(source) as z,ZipFile(memory,"w") as out:
        assert z.testzip() is None
        assert len(z.namelist())==expected_entries,(len(z.namelist()),expected_entries)
        for member in z.infolist():
            before=z.read(member.filename)
            after=transform(member.filename,before)
            if before!=after:changed.append(member.filename)
            out.writestr(member,after)
        out.comment=z.comment
    assert set(changed)==set(expected_changes),(changed,expected_changes)
    result=memory.getvalue()
    with ZipFile(BytesIO(result)) as z:
        assert z.testzip() is None and len(z.namelist())==expected_entries
        with TemporaryDirectory() as td:
            names=[n for n in z.namelist() if n.endswith('.php')]
            assert len(names)==php_count,(len(names),php_count)
            for n in names:
                path=Path(td)/n;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(z.read(n))
                p=subprocess.run(["php","-l",str(path)],capture_output=True,text=True)
                assert p.returncode==0,(n,p.stderr,p.stdout)
            print("PHP_PASS",source.parent.name,len(names))
    source.write_bytes(result)
    print("BUILD_PASS",source.parent.name,"bytes",len(result),"sha256",sha256(result).hexdigest(),"changes",changed)
    return result

with ZipFile(DESIGN) as z:
    assert z.testzip() is None
    des_count=len(z.namelist())
    des_php=sum(1 for n in z.namelist() if n.endswith(".php"))
with ZipFile(AD) as z:
    assert z.testzip() is None
    ad_count=len(z.namelist())
    ad_php=sum(1 for n in z.namelist() if n.endswith(".php"))

ad=build(AD,patch_ad,[AD_MAIN,AD_LOAD],ad_count,ad_php)
design=build(DESIGN,patch_design,[DESIGN_MAIN,DESIGN_PROFILE],des_count,des_php)

ad_path=AD.parent/"HOBBY_DEPOT_AFFILIATE_HD009_0.1.27.zip"
design_path=DESIGN.parent/"HOBBY_DEPOT_DESIGN_HD003_1.50.803.zip"
ad_path.write_bytes(ad);design_path.write_bytes(design)
assert ad_path.read_bytes()==AD.read_bytes()
assert design_path.read_bytes()==DESIGN.read_bytes()
print("DISTINCT_WORDPRESS_PLUGINS_PASS",ad_path.name,design_path.name)
