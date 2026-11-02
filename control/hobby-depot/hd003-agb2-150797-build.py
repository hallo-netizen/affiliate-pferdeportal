#!/usr/bin/env python3
"""Exact full-ZIP update: only the published /agb-2/ page presentation."""
import hashlib
import pathlib
import subprocess
import tempfile
import zipfile

INPUT = pathlib.Path("input/HOBBY_DEPOT_HD003_1.50.796_FOOTER_RECHTLICHES_SERVICE_FIX_VOLLPLUGIN.zip")
OUTPUT = pathlib.Path("dist/HOBBY_DEPOT_HD003_1.50.797_AGB2_HERO_TEXTKORREKTUR_VOLLPLUGIN.zip")
EXPECTED = "e1ff0d4636cbfe43a303d54328d0b2026eb75e4f6084b8ce99e061eee2471cd4"
ROOT = "affiliate-portal-template-kit/"
MAIN = ROOT + "pferde-template-kit.php"
PROFILE = ROOT + "includes/class-hobby-depot-profile-v150709.php"

def one(source, old, new, label):
    count = source.count(old)
    assert count == 1, f"{label}: expected 1 anchor, found {count}"
    return source.replace(old, new, 1)

def patch_profile(source):
    source = one(
        source, "'impressum', 'agb', 'disclaimer',",
        "'impressum', 'agb', 'agb-2', 'disclaimer',",
        "Only the additional published AGB slug")
    source = one(
        source,
        "            if (self::is_magazine_root_page_v150717($page)",
        "            if ($page instanceof WP_Post && sanitize_title((string)$page->post_name) === 'agb-2') { return false; }\n"
        "            if (self::is_magazine_root_page_v150717($page)",
        "Ensure normal WordPress page template, no duplicate category intro")
    source = one(
        source,
        "        // Doppelte Leerzeilen des Imports begrenzen, ohne Inhalte umzuschreiben.",
        """        // Exclusively AGB-2: remove the outdated last line, not any legal clauses.
        if ($slug === 'agb-2') {
            $content = preg_replace(
                '~(?:\\s*<br\\s*/?>){0,2}\\s*(?:<p\\b[^>]*>\\s*)?<strong\\b[^>]*>\\s*Stand\\s*:\\s*</strong>\\s*Juli\\s+2016\\s*(?:</p>\\s*)?$~iu',
                '',
                $content,
                1
            );
        }

        // Doppelte Leerzeilen des Imports begrenzen, ohne Inhalte umzuschreiben.""",
        "Only strip exact July 2016 ending")
    source = one(
        source,
        "$agb_url = self::page_link(['agb']);",
        "$agb_url = self::page_link(['agb-2', 'agb']);",
        "Prefer actual published page")
    source = one(
        source,
        "if ($agb_url === '') { $agb_url = home_url('/agb/'); }",
        "if ($agb_url === '') { $agb_url = home_url('/agb-2/'); }",
        "Fallback to demonstrated /agb-2/ URL")
    return source

def php_function(s, marker):
    i=s.index(marker)
    j=s.index("\n    }\n",i)
    return s[i:j+7]

def test_actual_page_renderer(profile):
    methods = [
        php_function(profile, "private static function is_plain_service_page("),
        php_function(profile, "private static function is_owned_content_route("),
        php_function(profile, "public static function render_universal_top("),
        php_function(profile, "public static function normalize_service_content_v150741("),
    ]
    php = """<?php
error_reporting(E_ALL);
class WP_Post {
    public $post_type = 'page';
    public $post_name = 'agb-2';
    public $post_title = 'AGB';
}
$GLOBALS['page'] = new WP_Post();
function is_admin(){return false;}
function is_front_page(){return false;}
function is_singular($value){return true;}
function get_queried_object(){return $GLOBALS['page'];}
function get_queried_object_id(){return 7751;}
function get_the_title($page){return $page->post_title;}
function sanitize_title($v){return strtolower(trim(preg_replace('~[^a-z0-9-]+~i','-',(string)$v),'-'));}
function esc_html($v){return htmlspecialchars((string)$v,ENT_QUOTES);}
function esc_url($v){return htmlspecialchars((string)$v,ENT_QUOTES);}
function esc_attr($v){return htmlspecialchars((string)$v,ENT_QUOTES);}
function wp_strip_all_tags($v){return strip_tags($v);}
class Fixture {
    public static $top_rendered=false;
    private static function asset_url($name){return '/plugin-assets/'.$name;}
    public static function render_breadcrumb(){return '<nav>Startseite › AGB</nav>';}
    private static function magazine_request_slug_v150722(){return '';}
""" + "\n".join(methods).replace("self::$top_rendered", "self::$top_rendered") + """
}
function check($ok, $message){if(!$ok)throw new Exception($message);}
check(Fixture::is_owned_content_route() === false,'AGB-2 must not use category page renderer');
ob_start(); Fixture::render_universal_top(); $top=ob_get_clean();
check(substr_count($top,'<h1>AGB</h1>')===1,'exactly one title');
check(substr_count($top,'alltagsobjekte.webp')===1,'one existing real photo hero');
check(strpos($top,'Mehr erfahren')===false,'no intro expansion');
$sample='<strong>Allgemeine Geschäftsbedingungen</strong><br><br><strong>1. Geltungsbereich</strong><br>Die AGB gelten.<br><br><strong>Stand:</strong> Juli 2016'."\\n".'<!-- /wp:kubio/text -->';
$rendered=Fixture::normalize_service_content_v150741($sample);
check(strpos($rendered,'1. Geltungsbereich')!==false,'original clauses preserved');
check(strpos($rendered,'Juli 2016')===false,'old date removed');
check(strpos($rendered,'Stand:')===false,'old date label removed');
check(strpos($rendered,'<details')===false,'no More expansion');
$GLOBALS['page']->post_name='kontakt';
check(Fixture::normalize_service_content_v150741('Test')==='<div class="hd-service-body-v150741">Test</div>','other service pages unchanged');
print("PASS: AGB-2 hero, no duplicate intro, no More, old date removed, other service unchanged\\n");
"""
    with tempfile.TemporaryDirectory() as d:
        path=pathlib.Path(d)/"test.php"
        path.write_text(php, encoding="utf-8")
        r=subprocess.run(["php",str(path)],capture_output=True,text=True)
        assert r.returncode==0, (r.stdout + r.stderr)
        print(r.stdout.strip())

def run():
    assert hashlib.sha256(INPUT.read_bytes()).hexdigest() == EXPECTED, "Wrong 1.50.796 source SHA"
    with zipfile.ZipFile(INPUT) as zipin:
        assert zipin.testzip() is None, "Source ZIP CRC"
        infos=zipin.infolist()
        assert len(infos) == 1290, len(infos)
        files={x.filename: zipin.read(x.filename) for x in infos}
    assert len(files)==len(infos)
    assert MAIN in files and PROFILE in files
    changed=dict(files)
    src=changed[PROFILE].decode("utf-8")
    src=patch_profile(src)
    assert "1.50.796" in src
    changed[PROFILE]=src.replace("1.50.796","1.50.797").encode("utf-8")
    main=changed[MAIN].decode("utf-8")
    assert "1.50.796" in main
    changed[MAIN]=main.replace("1.50.796","1.50.797").encode("utf-8")
    assert {p for p in files if files[p]!=changed[p]}=={MAIN,PROFILE}
    for name in (MAIN,PROFILE):
        with tempfile.TemporaryDirectory() as tmp:
            path=pathlib.Path(tmp)/pathlib.Path(name).name
            path.write_bytes(changed[name])
            p=subprocess.run(["php","-l",str(path)],capture_output=True,text=True)
            assert p.returncode==0,p.stdout+p.stderr
    test_actual_page_renderer(changed[PROFILE].decode("utf-8"))
    OUTPUT.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(OUTPUT,"w") as zipout:
        for info in infos:
            zipout.writestr(info,changed[info.filename])
    with zipfile.ZipFile(OUTPUT) as check:
        assert check.testzip() is None
        assert check.namelist()==[z.filename for z in infos]
        for path in files:
            if path not in (MAIN,PROFILE):
                assert check.read(path)==files[path],path
    print("PASS: original release validated; 1290 files; PHP syntax; all other ZIP entries byte-identical")
    print("SHA256:", hashlib.sha256(OUTPUT.read_bytes()).hexdigest())
    print("OUTPUT:", OUTPUT, "SIZE:", OUTPUT.stat().st_size)

if __name__ == "__main__":
    run()
