#!/usr/bin/env python3
"""HD003 v1.50.798: ALL HivePress listing-category archive levels get current Hobby Depot market layout.
The source is the exact verified 1.50.797 FULL plugin ZIP. Other 1288 entries must remain byte-identical.
"""
import hashlib
import pathlib
import subprocess
import tempfile
import zipfile

INPUT = pathlib.Path("input/HOBBY_DEPOT_HD003_1.50.797_AGB2_HERO_TEXTKORREKTUR_VOLLPLUGIN.zip")
OUTPUT = pathlib.Path("dist/HOBBY_DEPOT_HD003_1.50.798_ANZEIGENMARKT_ALLE_KATEGORIEEBENEN_VOLLPLUGIN.zip")
EXPECTED = "6b4220080a551a58b7535b1b4ab79d1f0120d05025f74bdb7c6f313c32f90858"
ROOT = "affiliate-portal-template-kit/"
MAIN = ROOT + "pferde-template-kit.php"
PROFILE = ROOT + "includes/class-hobby-depot-profile-v150709.php"

def one(text, old, new, label):
    n = text.count(old)
    assert n == 1, f"{label}: anchor expected once, got {n}"
    return text.replace(old, new, 1)

CATEGORY_METHODS = r'''
    /**
     * All genuine HivePress listing-category archives, independent of root/parent/child.
     * No slug lists, no hard-coded term IDs, no new plugin, and no DB writes.
     */
    private static function is_hivepress_market_category_v150798() {
        if (is_admin() || !function_exists('is_tax') || !is_tax('hp_listing_category')) { return false; }
        $term = get_queried_object();
        return $term instanceof WP_Term && (string)$term->taxonomy === 'hp_listing_category';
    }

    public static function render_market_category_top_v150798() {
        if (!self::is_hivepress_market_category_v150798()) { return; }
        $term = get_queried_object();
        $title = trim((string)$term->name);
        if ($title === '') { return; }

        $submit = self::hivepress_submit_url_v150742();
        $hero = self::asset_url('anzeigenmarkt-hero-v150744.webp');
        $description = trim(wp_strip_all_tags((string)($term->description ?? '')));
        if ($description === '') { $description = 'Angebote und Anzeigen rund um dieses Hobby entdecken.'; }

        echo '<div class="hd-market-shell-v150743 hd-market-category-shell-v150798">';
        echo '<nav class="hd-market-breadcrumb-v150743" aria-label="Breadcrumb">';
        echo '<a href="' . esc_url(home_url('/')) . '">Startseite</a><span>›</span>';
        echo '<a href="' . esc_url(self::hivepress_listings_url_v150742()) . '">Anzeigenmarkt</a>';
        $ancestors = function_exists('get_ancestors') ? (array)get_ancestors((int)$term->term_id, 'hp_listing_category', 'taxonomy') : [];
        foreach (array_reverse($ancestors) as $ancestor_id) {
            $ancestor = get_term((int)$ancestor_id, 'hp_listing_category');
            if (!$ancestor instanceof WP_Term || is_wp_error($ancestor)) { continue; }
            $url = get_term_link($ancestor);
            if (is_wp_error($url) || !is_string($url) || $url === '') { continue; }
            echo '<span>›</span><a href="' . esc_url($url) . '">' . esc_html($ancestor->name) . '</a>';
        }
        echo '<span>›</span><strong>' . esc_html($title) . '</strong></nav>';
        echo '<section class="hd-market-hero-v150744"><div class="hd-market-hero-copy-v150744"><span>Anzeigenmarkt</span>';
        echo '<h1>' . esc_html($title) . '</h1><p>' . esc_html($description) . '</p>';
        if ($submit !== '') { echo '<a class="hd-market-submit-v150743" href="' . esc_url($submit) . '">Anzeige aufgeben</a>'; }
        echo '</div><div class="hd-market-hero-image-v150744"><img src="' . esc_url($hero) . '" alt="Historisches Anzeigenblatt auf einem Tisch" width="1030" height="210" decoding="async" fetchpriority="high"></div></section>';
        echo self::render_market_search_v150743((int)$term->term_id);
        echo '<section class="hd-market-native-head-v150744"><h2>Anzeigen in ' . esc_html($title) . '</h2><a href="' . esc_url(self::hivepress_listings_url_v150742()) . '">Alle Anzeigen ansehen →</a></section>';
        echo '</div>';
    }
'''

CSS = r'''
/* 1.50.798: genuine HivePress category archives, every level, same marketplace design. */
body.hd-market-category-v150798 .site-content .widget-area,
body.hd-market-category-v150798 .site-content #secondary,
body.hd-market-category-v150798 .site-content .sidebar-main,
body.hd-market-category-v150798 .site-content .site-sidebar,
body.hd-market-category-v150798 .site-content .widget_archive,
body.hd-market-category-v150798 .site-content .widget_categories{display:none!important}
body.hd-market-category-v150798 .site-content .content-area,
body.hd-market-category-v150798 .site-content #primary,
body.hd-market-category-v150798 .site-content .site-main{
 float:none!important;width:100%!important;max-width:1200px!important;
 margin-left:auto!important;margin-right:auto!important;min-width:0!important
}
body.hd-market-category-v150798 .site-content .hp-page__title,
body.hd-market-category-v150798 .site-content .page-title,
body.hd-market-category-v150798 .site-content .hp-form--listing-search{display:none!important}
body.hd-market-category-v150798 .site-content .hp-listing-category,
body.hd-market-category-v150798 .site-content .hp-listing--view-block{
 border:1px solid rgba(63,71,75,.12)!important;border-radius:5px!important;
 background:#fff!important;box-shadow:0 4px 16px rgba(35,53,60,.035)!important
}
body.hd-market-category-v150798 .site-content .hp-listing-category__name,
body.hd-market-category-v150798 .site-content .hp-listing__title{
 color:#17313c!important;font-weight:800!important
}
body.hd-market-category-v150798 .site-content .hp-listing-categories{width:100%!important;max-width:none!important}
body.hd-market-category-v150798 .site-content .hp-page__content{width:100%!important;max-width:none!important}
.hd-market-category-shell-v150798 .hd-market-native-head-v150744{margin-bottom:18px}
@media(max-width:760px){
 body.hd-market-category-v150798 .site-content .content-area,
 body.hd-market-category-v150798 .site-content #primary,
 body.hd-market-category-v150798 .site-content .site-main{max-width:100%!important}
 .hd-market-category-shell-v150798 .hd-market-breadcrumb-v150743{flex-wrap:wrap}
 .hd-market-category-shell-v150798 .hd-market-native-head-v150744{align-items:start;gap:9px}
}
'''

def patch_profile(source):
    source = one(source,
        "        add_action('wp_body_open', [__CLASS__, 'render_market_top_v150743'], 25);",
        "        add_action('wp_body_open', [__CLASS__, 'render_market_top_v150743'], 25);\n"
        "        add_action('wp_body_open', [__CLASS__, 'render_market_category_top_v150798'], 26);",
        "One archive mount at the existing market root hook")
    source = one(source,
        "        if (self::is_hivepress_market_root_v150742()) { $classes[] = 'hd-market-root-v150744'; }",
        "        if (self::is_hivepress_market_root_v150742()) { $classes[] = 'hd-market-root-v150744'; }\n"
        "        if (self::is_hivepress_market_category_v150798()) { $classes[] = 'hd-market-category-v150798'; }",
        "Archive-only CSS class")
    source = one(source,
        "    public static function render_market_top_v150743() {",
        CATEGORY_METHODS + "\n    public static function render_market_top_v150743() {",
        "One method pair before original market root")
    source = one(source,
        "/* 1.50.746 – Pilot Unterseite:",
        CSS + "\n/* 1.50.746 – Pilot Unterseite:",
        "Scoped CSS in original central style sheet")
    assert source.count("private static function is_hivepress_market_category_v150798()") == 1
    assert source.count("public static function render_market_category_top_v150798()") == 1
    return source

def extract_function(source, signature):
    i = source.index(signature)
    start = source.index("{", i)
    # The method definitions are intentionally simple: their closing braces occur at 4-space indent.
    end = source.index("\n    }\n", start) + len("\n    }\n")
    return source[i:end]

def test_rendered_pages(source):
    methods = [extract_function(source, "private static function is_hivepress_market_category_v150798()"),
               extract_function(source, "public static function render_market_category_top_v150798()"),
               extract_function(source, "private static function render_market_search_v150743(")]
    methods[0] = methods[0].replace("private static function", "public static function", 1)
    methods[2] = methods[2].replace("private static function", "public static function", 1)
    php = r'''<?php
error_reporting(E_ALL);
class WP_Term {
    public $taxonomy='hp_listing_category'; public $term_id=33; public $name='Vereine & Gruppen';
    public $description='Treffen, Kurse und Kontakte.';
}
$GLOBALS['archive']=new WP_Term(); $GLOBALS['tax']=true; $GLOBALS['admin']=false;
function is_admin(){return $GLOBALS['admin'];}
function is_tax($tax){return $GLOBALS['tax'] && $tax==='hp_listing_category';}
function get_queried_object(){return $GLOBALS['archive'];}
function get_ancestors($id,$tax,$type){return $id===33 ? [22,11] : ($id===22 ? [11] : []);}
function get_term($id,$tax){$o=new WP_Term();$o->term_id=$id;$o->name=$id===11?'Hobbywelten':'Vereine';return $o;}
function get_term_link($term){return '/listing-category/term-'.$term->term_id.'/';}
function is_wp_error($v){return false;}
function esc_html($s){return htmlspecialchars((string)$s,ENT_QUOTES,'UTF-8');}
function esc_attr($s){return esc_html($s);}
function esc_url($s){return esc_html($s);}
function home_url($s){return 'https://hobby-depot.de'.$s;}
function wp_strip_all_tags($s){return strip_tags($s);}
function absint($x){return abs((int)$x);}
function sanitize_text_field($s){return trim($s);}
function wp_unslash($s){return $s;}
class Fixture {
    private static function hivepress_listings_url_v150742(){return '/listings/';}
    private static function hivepress_submit_url_v150742(){return '/submit-listing/';}
    private static function asset_url($s){return '/assets/'.$s;}
''' + "\n".join(methods) + r'''
}
function check($ok,$msg){if(!$ok)throw new RuntimeException($msg);}
check(Fixture::is_hivepress_market_category_v150798(),'archive recognized');
ob_start(); Fixture::render_market_category_top_v150798(); $html=ob_get_clean();
check(substr_count($html,'<h1>Vereine &amp; Gruppen</h1>')===1,'one H1 title');
check(strpos($html,'/assets/anzeigenmarkt-hero-v150744.webp')!==false,'existing market hero reused');
check(strpos($html,'>Hobbywelten</a>')!==false && strpos($html,'>Vereine</a>')!==false,'ancestry breadcrumbs');
check(strpos($html,'name="_category" value="33"')!==false,'category search scoped');
check(strpos($html,'>Anzeige aufgeben</a>')!==false,'native submit link');
check(strpos($html,'>Alle Anzeigen ansehen')!==false,'return to market');
check(strpos($html,'<h2>Anzeigen in Vereine &amp; Gruppen</h2>')!==false,'native ads heading');
$GLOBALS['archive']->term_id=11;
ob_start(); Fixture::render_market_category_top_v150798(); $root=ob_get_clean();
check(strpos($root,'name="_category" value="11"')!==false,'top-level archive');
check(strpos($root,'>Hobbywelten</a>')===false,'no duplicate parent on top-level');
$GLOBALS['archive']->term_id=22;
ob_start(); Fixture::render_market_category_top_v150798(); $middle=ob_get_clean();
check(strpos($middle,'>Hobbywelten</a>')!==false,'middle level ancestor');
$GLOBALS['tax']=false;
check(!Fixture::is_hivepress_market_category_v150798(),'normal pages unaffected');
ob_start(); Fixture::render_market_category_top_v150798(); check(ob_get_clean()==='','no hero on regular pages');
$GLOBALS['tax']=true;$GLOBALS['admin']=true;
check(!Fixture::is_hivepress_market_category_v150798(),'admin unaffected');
print("PASS category top, mid, deep; existing hero/search/submit; correct taxonomy guard; no normal-page/admin output\n");
'''
    with tempfile.TemporaryDirectory() as d:
        p = pathlib.Path(d)/"test-hd003-category.php"
        p.write_text(php,encoding="utf-8")
        r = subprocess.run(["php",str(p)],capture_output=True,text=True)
        assert r.returncode == 0, r.stdout+r.stderr
        print(r.stdout.strip())

def run():
    assert hashlib.sha256(INPUT.read_bytes()).hexdigest()==EXPECTED,"Incorrect source full ZIP"
    with zipfile.ZipFile(INPUT) as source:
        assert source.testzip() is None,"Source ZIP CRC"
        infos=source.infolist()
        assert len(infos)==1290,"Source entry count"
        files={entry.filename:source.read(entry.filename) for entry in infos}
    assert MAIN in files and PROFILE in files
    changed=dict(files)
    profile=changed[PROFILE].decode("utf-8")
    assert "const RELEASE = '1.50.797';" in profile
    profile=patch_profile(profile)
    profile=one(profile,"const RELEASE = '1.50.797';","const RELEASE = '1.50.798';","Profile version")
    changed[PROFILE]=profile.encode("utf-8")
    main=changed[MAIN].decode("utf-8")
    assert "1.50.797" in main
    main=main.replace("1.50.797","1.50.798")
    changed[MAIN]=main.encode("utf-8")
    assert {f for f in files if files[f]!=changed[f]}=={MAIN,PROFILE},"Unexpected modified ZIP entries"
    for f in (MAIN,PROFILE):
        with tempfile.TemporaryDirectory() as d:
            p=pathlib.Path(d)/pathlib.Path(f).name
            p.write_bytes(changed[f])
            r=subprocess.run(["php","-l",str(p)],capture_output=True,text=True)
            assert r.returncode==0,f+" "+r.stdout+r.stderr
    test_rendered_pages(profile)
    # Hard safety: the entire 13-file PHP stack must lint on the SAME PHP as user's server.
    with tempfile.TemporaryDirectory() as d:
        count=0
        for f,payload in changed.items():
            if not f.endswith(".php"):continue
            path=pathlib.Path(d)/f
            path.parent.mkdir(parents=True,exist_ok=True)
            path.write_bytes(payload)
            result=subprocess.run(["php","-l",str(path)],capture_output=True,text=True)
            assert result.returncode==0,f+" "+result.stdout+result.stderr
            count+=1
        assert count==13,count
        print("PASS: all 13 PHP files lint on server PHP 8.5.12")
    assert "body.hd-market-category-v150798 .site-content .widget-area" in profile
    assert "body.hd-market-root-v150744 .site-content .widget-area" in profile
    assert "function render_market_top_v150743()" in profile
    assert "public static function render_market_category_top_v150798()" in profile
    OUTPUT.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(OUTPUT,"w") as target:
        for info in infos:
            target.writestr(info,changed[info.filename])
    with zipfile.ZipFile(OUTPUT) as check:
        assert check.testzip() is None
        assert check.namelist()==[i.filename for i in infos]
        for key in files:
            assert check.read(key)==changed[key],"Archive content mismatch "+key
    print("PASS 1290 ZIP entries; 1288 byte-identical other files; full release source pinned")
    print("ZIP_SHA256:",hashlib.sha256(OUTPUT.read_bytes()).hexdigest())
    print("ZIP_PATH:",OUTPUT,"SIZE:",OUTPUT.stat().st_size)

if __name__=="__main__":run()
