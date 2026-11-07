#!/usr/bin/env python3
"""HAB-004 isolated source-only RC11 build. No API calls, no paid searches."""
from pathlib import Path
import argparse, hashlib, os, re, shutil, subprocess, sys, tempfile, zipfile

PROJECT = Path("protocol/PROJECT_MEMORY/PROJEKTE/EIGENTUMSSCHUTZ")
HAB = PROJECT/"PLUGINS/ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip"
DESIGN = PROJECT/"PLUGINS/ISOLIERTE_PLUGINS/HAB-001-DESIGN/CURRENT.zip"
OLD_TESTS = PROJECT/"AFFILIATE/IMPLEMENTIERUNG_RC10/VOLLSTAENDIGE_SIMULATION_TESTBELEGE.zip"
EXPECTED_HAB = "f3b6b0ac4fd05310fa32ce68e2715b29d022003ac68f32ceb051443832364ced"

def sha(data):
    return hashlib.sha256(data).hexdigest()

def replace_method(code, start, end, new):
    if code.count(start)!=1 or code.count(end)!=1: raise AssertionError(("method anchors",start,end))
    i=code.index(start);j=code.index(end,i)
    return code[:i]+new+"\n\n"+code[j:]

BRIDGE_START = "    private static function area($html, $node_id, $kind) {"
BRIDGE_END = "    public static function world_banner($html, $node_id = '') {"
BRIDGE_NEW = r'''    private static function area($html, $node_id, $kind) {
        if (is_string($html) && trim($html) !== '') { return $html; }
        $nodes=self::verified_nodes();
        $node=$nodes[(string)$node_id] ?? array();
        if (!class_exists('Portal_Affiliate_Router')) { return ''; }
        $id=absint($node['wp_id'] ?? 0);
        if (!$id) { return ''; }
        if (($node['type'] ?? '') === 'category') {
            if ($kind !== 'products') { return ''; }
            $router=Portal_Affiliate_Router::instance();
            $output='';
            for ($i=1; $i<=3; $i++) {
                $part=$router->provide_leaf_category_affiliate_slot_html(
                    '', $id, 'category_product_'.$i
                );
                if (trim((string)$part) !== '') { $output.=$part; }
            }
            return $output;
        }
        if (($node['type'] ?? '') !== 'page') { return ''; }
        if (function_exists('get_post_status') && get_post_status($id) !== 'publish') { return ''; }
        return Portal_Affiliate_Router::instance()->hab_bw_area_slot($id,$kind);
    }'''

AMAZON_MARKUP_START = "    private function hb_amazon_product_family_markup($slug, $name, $slot_type) {"
AMAZON_MARKUP_END = "    /** Genuine WordPress category archive with an existing authorized Hab family. */"
AMAZON_MARKUP_NEW = r'''    /** Use only saved verified ASIN/title. The original campaign renderer remains in charge. */
    private function hb_amazon_product_family_markup($slug, $name, $slot_type, $offer_index = null) {
        if (!$this->hb_amazon_ready()) { return ''; }
        $slug = sanitize_key((string)$slug);
        $name = sanitize_text_field((string)$name);
        $slot_type = sanitize_key((string)$slot_type);
        $product_card = preg_match('/^category_product_([123])$/D', $slot_type, $match);
        if ($name === '' || strlen($name)>150
            || (!$product_card && !in_array($slot_type,
                array('product_after_category_tiles','category_recommendation'), true))) { return ''; }
        $url = 'https://www.amazon.de/s?k='.rawurlencode($name).'&tag='.rawurlencode($this->hb_amazon_tag());
        $c = get_option(self::HB_AMAZON_CONTROL,array());
        $saved = (array)($c['category_products'] ?? array());
        $listing = (array)($saved[$slug] ?? array());
        $verified = array();
        if (absint($listing['at'] ?? 0)>time()-14*DAY_IN_SECONDS) {
            foreach ((array)($listing['items'] ?? array()) as $item) {
                $asin = strtoupper((string)($item['asin'] ?? ''));
                $title = sanitize_text_field((string)($item['title'] ?? ''));
                if (!preg_match('/^[A-Z0-9]{10}$/D',$asin) || $title === '') { continue; }
                $direct = $this->hb_amazon_direct_url($asin);
                if ($direct !== '') { $verified[]=array('url'=>$direct,'title'=>$title); }
            }
        }
        if ($product_card) {
            $index = ($offer_index === null) ? ((int)$match[1]-1) : absint($offer_index);
            if (!isset($verified[$index])) {
                if ($index !== 0 || $verified) { return ''; }
                $search = '<a href="'.esc_url($url).'" target="_blank" rel="sponsored nofollow noopener noreferrer">Passende Angebote bei Amazon suchen</a>';
                return '<div class="ppar-affiliate-slot ppar-slot-'.$slot_type.' ppar-hab-amazon-search" data-ppar-slot="'.$slot_type.'">'
                    .'<div class="ppar-affiliate-label">Anzeige</div><div class="ppar-affiliate-content">'.$search.'</div></div>';
            }
            $item=$verified[$index];
            $banner=array('mode'=>'image_link','creative_type'=>'product','network'=>'amazon',
                'url'=>$item['url'],'title'=>$item['title'],'button_text'=>'Bei Amazon ansehen',
                'image_url'=>'','price'=>'','availability'=>'');
            $context=array('primary_slug'=>$slug,'primary_name'=>$name,'post_type'=>'category_archive',
                'post_id'=>0,'slugs'=>array($slug),'names'=>array($name));
            $creative=$this->render_banner($banner,0,$context,array('id'=>'hab-amazon-verified'),$slot_type);
            if (trim((string)$creative) === '') { return ''; }
            return '<div class="ppar-affiliate-slot ppar-slot-'.$slot_type.' ppar-hab-amazon-verified" data-ppar-slot="'.$slot_type.'">'
                .'<div class="ppar-affiliate-label">Anzeige</div>'
                .'<div class="ppar-affiliate-content">'.$creative.'</div></div>';
        }
        $parts=array();
        foreach ($verified as $item) {
            $parts[]='<a href="'.esc_url($item['url']).'" target="_blank" rel="sponsored nofollow noopener noreferrer">'.esc_html($item['title']).'</a>';
        }
        $body=$parts ? implode(' · ',$parts)
            : '<a href="'.esc_url($url).'" target="_blank" rel="sponsored nofollow noopener noreferrer">Passende Angebote bei Amazon suchen</a>';
        return '<div class="ppar-affiliate-slot ppar-slot-'.$slot_type.' ppar-hab-amazon-search" data-ppar-slot="'.$slot_type.'">'
            .'<div class="ppar-affiliate-label">Anzeige</div>'
            .'<div class="ppar-affiliate-content">'.$body.'</div></div>';
    }'''

CATEGORY_FALLBACK_START = "    private function hb_amazon_category_search_fallback($context, $slot_type) {"
CATEGORY_FALLBACK_END = "    /** Existing Hab product page hook works even when article categories are empty. */"
CATEGORY_FALLBACK_NEW = r'''    private function hb_amazon_category_search_fallback($context, $slot_type) {
        $slot_type=sanitize_key((string)$slot_type);
        if (!$this->hb_amazon_ready() || !is_array($context)
            || (!in_array($slot_type,array('product_after_category_tiles','category_recommendation'),true)
                && !preg_match('/^category_product_[123]$/D',$slot_type))
            || ($context['post_type'] ?? '') !== 'category_archive'
            || sanitize_key((string)($context['product_family_slug'] ?? '')) === '') { return ''; }
        return $this->hb_amazon_product_family_markup($context['primary_slug'] ?? '',
            $context['primary_name'] ?? '',$slot_type);
    }'''

AREA_FALLBACK_START = "    private function hb_amazon_area_product_fallback($page_id) {"
AREA_FALLBACK_END = "    public function hb_amazon_admin_menu() {"
AREA_FALLBACK_NEW = r'''    private function hb_amazon_area_product_fallback($page_id) {
        if (!$this->hb_amazon_ready() || !class_exists('PPAR_HB_Integration')
            || !class_exists('PPAR_Portal_Source')) { return ''; }
        $node=PPAR_HB_Integration::page_for_id(absint($page_id));
        if (!is_array($node) || ($node['type'] ?? '') !== 'page') { return ''; }
        $catalog=PPAR_Portal_Source::catalog();
        if (is_wp_error($catalog) || !is_array($catalog)) { return ''; }
        $parts=array();$seen=array();
        foreach ((array)($catalog['product_targets'] ?? array()) as $row) {
            if (!is_array($row) || (string)($row['node_id'] ?? '') !== (string)($node['id'] ?? '')) { continue; }
            $slug=sanitize_key((string)($row['category_slug'] ?? ''));
            if ($slug === '' || isset($seen[$slug])) { continue; }
            $seen[$slug]=true;
            for ($j=0; $j<3 && count($parts)<3; $j++) {
                $slot='category_product_'.(count($parts)+1);
                $html=$this->hb_amazon_product_family_markup($slug,$row['title'] ?? '',$slot,$j);
                if ($html !== '') { $parts[]=$html; }
            }
            if (count($parts)>=3) { break; }
        }
        return implode('',$parts);
    }'''

def run(command, *args, cwd=None):
    p=subprocess.run([command,*args],cwd=cwd,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    if p.returncode: raise AssertionError("FAILED: "+' '.join([command,*args])+"\n"+p.stdout[-4500:])
    return p.stdout

def prepare_harness(temp, original, patched, design):
    with zipfile.ZipFile(OLD_TESTS) as z: z.extractall(temp)
    # Original RC10 stubs did not require the standard WP renderer's sanitizer.
    for harness in (temp/'RC10_TESTS').glob('*.php'):
        src=harness.read_text()
        assert src.startswith('<?php'),harness
        src=src.replace('<?php',"<?php\nfunction esc_url_raw($value){return $value;}\n",1)
        harness.write_text(src)
    with zipfile.ZipFile(design) as z:
        n=next(n for n in z.namelist() if n.endswith("/includes/area-design-prototype.php"))
        dest=temp/"hab-design/includes/area-design-prototype.php"
        dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(z.read(n))
    testpath=temp/"RC10_TESTS/full_plugin_harness_rc9.php"
    h=testpath.read_text()
    old="require dirname(__DIR__).'/affiliate-portal-router/affiliate-portal-router.php';"
    assert h.count(old)==1
    h=h.replace(old,'''function get_term($id,$tax='category'){if($tax!=='category'||(int)$id!==201)return null;return (object)['term_id'=>201,'slug'=>'wassermelder','name'=>'Wassermelder','description'=>''];}
function wp_kses_post($html){return $html;} function esc_url_raw($url){return $url;}
require dirname(__DIR__).'/hab-design/includes/area-design-prototype.php';
'''+old)
    marker="echo 'FULL_PLUGIN_ASSERTIONS '.$GLOBALS['assertions'].\"\\n\";"
    assert h.count(marker)==1
    if original:
        append=r'''
$category_html=apply_filters('hbdp_area_product_cards_html','','core:category:1');
pass(trim($category_html)==='', 'Baseline: original category node is incorrectly rejected');
$old_page=$app->hab_bw_area_slot(501,'products');
pass(str_contains($old_page,' · '), 'Baseline: several verified ASINs jammed into one text box');
'''
    else:
        append=r'''
$before_calls=count($GLOBALS['remote']);
$category_html=hbdp_area_product_markup(['id'=>'core:category:1']);
pass(substr_count($category_html,'data-ppar-category-product-card="1"')===2,'Existing original design hook receives two individual product cards');
pass(str_contains($category_html,'/dp/B011111111?tag=habundbewahr-21') && str_contains($category_html,'/dp/B022222222?tag=habundbewahr-21'),'Both verified ASINs are separate tracked cards');
pass(substr_count($category_html,'ppar-banner-title')===2,'Existing campaign banner renderer used twice');
pass(!str_contains($category_html,' · '),'Category has no bundled Amazon text row');
pass(!str_contains($category_html,'<img'),'No fake product picture');
pass(count($GLOBALS['remote'])===$before_calls,'Rendering costs zero new API calls');
pass(hbdp_area_product_markup(['id'=>'not-a-verified-node'])==='','Unknown category fails closed');
pass(hbdp_area_product_markup(['id'=>'core:c22:topic:1'])!=='','Existing R3 topic page remains active');
pass(hbdp_area_product_markup(['id'=>'core:category:1'])===$category_html,'Rendering is deterministic');
pass(apply_filters('hbdp_area_product_cards_html','<div>Gebuchte Werbung</div>','core:category:1')==='<div>Gebuchte Werbung</div>','Booked design slot takes priority on category');
$GLOBALS['opts']['ppar_enabled']='0';
pass(hbdp_area_product_markup(['id'=>'core:category:1'])==='','Global off is honored on category');
$GLOBALS['opts']['ppar_enabled']='1';
'''
    testpath.write_text(h.replace(marker,append+"\n"+marker))
    return testpath

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",default="/tmp/hab004_rc11_candidate.zip")
    a=parser.parse_args()
    assert sha(HAB.read_bytes())==EXPECTED_HAB,"Baseline HAB zip changed; stop"
    assert OLD_TESTS.exists() and DESIGN.exists()
    with zipfile.ZipFile(HAB) as zin:
        names=zin.namelist()
        assert len(names)==28 and zin.testzip() is None
        raw={name:zin.read(name) for name in names}
        info={name:zin.getinfo(name) for name in names}
    bridge=next(n for n in names if n.endswith("/class-ppar-hab-bewahr-bridge.php"))
    amazon=next(n for n in names if n.endswith("/trait-ppar-hb-amazon.php"))
    mainphp=next(n for n in names if n.endswith("/affiliate-portal-router.php"))
    readme=next(n for n in names if n.endswith("/readme.txt"))
    modified={}
    x=raw[bridge].decode("utf8")
    assert "($node['type'] ?? '') !== 'page'" in x
    modified[bridge]=replace_method(x,BRIDGE_START,BRIDGE_END,BRIDGE_NEW).encode("utf8")
    x=raw[amazon].decode("utf8")
    assert "implode(' · ',$parts)" in x
    x=replace_method(x,AMAZON_MARKUP_START,AMAZON_MARKUP_END,AMAZON_MARKUP_NEW)
    x=replace_method(x,CATEGORY_FALLBACK_START,CATEGORY_FALLBACK_END,CATEGORY_FALLBACK_NEW)
    x=replace_method(x,AREA_FALLBACK_START,AREA_FALLBACK_END,AREA_FALLBACK_NEW)
    modified[amazon]=x.encode("utf8")
    for f in [mainphp,readme]:
        x=raw[f].decode("utf8")
        assert "0.1.7-rc10" in x, f
        modified[f]=x.replace("0.1.7-rc10","0.1.8-rc11").encode("utf8")
    output=Path(a.output)
    output.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(output,"w") as z:
        for f in names:z.writestr(info[f],modified.get(f,raw[f]))
    assert zipfile.ZipFile(output).testzip() is None
    with zipfile.ZipFile(output) as z:
        assert z.namelist()==names and len(z.namelist())==28
        assert all(z.read(f)==raw[f] for f in names if f not in modified)
    print("PACKAGE",output,output.stat().st_size,sha(output.read_bytes()),"changed:",list(modified),flush=True)
    with tempfile.TemporaryDirectory() as td:
        base=Path(td)/"baseline";candidate=Path(td)/"candidate"
        base.mkdir();candidate.mkdir()
        with zipfile.ZipFile(HAB) as z:z.extractall(base)
        with zipfile.ZipFile(output) as z:z.extractall(candidate)
        for temp,orig in [(base,True),(candidate,False)]:
            test=prepare_harness(temp,orig,not orig,DESIGN)
            res=run("php",str(test.resolve()),"valid",cwd=temp)
            print("BASELINE" if orig else "RC11 E2E",res[-1250:],flush=True)
        for f in candidate.rglob("*.php"):
            run("php","-l",str(f.resolve()))
        print("PHP LINT PASS",len(list(candidate.rglob("*.php"))),flush=True)
        testdir=candidate/"RC10_TESTS"
        regcases=[
          ("full_plugin_harness_rc9.php",["six_worlds","eight_worlds","unmapped_insurance","wrong_revision","missing_snapshot","no_products","too_few"]),
          ("full_workflow_rc10.php",["valid","get_pending","get_error","invalid_pending","expired_pending","manual_poll_only","cron_works"])
        ]
        cases=0
        for name,variants in regcases:
            for variant in variants:
                if name=="full_plugin_harness_rc9.php" and variant in ["wrong_revision","missing_snapshot","no_products","too_few"]:
                    # Extended category checks require a valid snapshot; use original unextended harness for these.
                    with zipfile.ZipFile(OLD_TESTS) as z:
                        script=z.read("RC10_TESTS/full_plugin_harness_rc9.php")
                    other=testdir/"full_plugin_harness_unextended.php"
                    other.write_bytes(script)
                    target=other
                else: target=testdir/name
                result=run("php",str(target.resolve()),variant,cwd=candidate)
                cases+=1
        for name in ["test_hab_amazon.php","test_hab_rc5.php","test_hab_rc6.php","test_hab_rc7.php"]:
            target=testdir/name
            print("TEST",name,run("php",str(target.resolve()),cwd=candidate).splitlines()[-1:],flush=True)
            cases+=1
        print("REGRESSION PASS",cases,"independent PHP processes",flush=True)
    print("RC11 TESTS ALL PASS",flush=True)

if __name__=="__main__":
    main()
