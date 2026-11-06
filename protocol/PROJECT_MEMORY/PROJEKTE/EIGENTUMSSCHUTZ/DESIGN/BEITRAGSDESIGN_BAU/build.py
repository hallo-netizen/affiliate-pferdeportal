#!/usr/bin/env python3
"""Build the in-place Hab & Bewahr design plugin update from the verified original ZIP.
No other portal, category, WordPress content or K0 is modified.
"""
from pathlib import Path
import hashlib
import re
import zipfile

ROOT = Path(__file__).resolve().parent
CAMPUS = ROOT.parents[1]
SOURCE = CAMPUS / "PLUGINS/ISOLIERTE_PLUGINS/HAB-001-DESIGN/CURRENT.zip"
OUT = ROOT / "HAB_UND_BEWAHR_DESIGN_0.1.185_BEITRAEGE.zip"
PREFIX = "hab-bewahr-design-vorschau/"
MAIN = PREFIX + "hab-bewahr-design-vorschau.php"
TEMPLATE = PREFIX + "templates/site.php"
EXPECTED_SHA = "76043e5c093058a4d8aff8fd6642307cade951c8267641dc710b8ed70cd323e3"

def replace_once(value, old, new, where):
    count = value.count(old)
    if count != 1:
        raise AssertionError(f"{where}: expected unique pattern; got {count}: {old[:100]}")
    return value.replace(old, new)

def patch_main(value):
    value = replace_once(
        value,
        "if(is_singular('post') && get_post_meta(get_queried_object_id(),'_hbdp_demo',true)==='1') return 'article';",
        "if(is_singular('post')) return 'article';",
        "regular posts routing",
    )
    value = replace_once(
        value,
        "add_filter('template_include','hbdp_preview_template',99);",
        """require_once HBDP_ROOT.'includes/article-page.php';
add_filter('template_include','hbdp_preview_template',99);
add_action('wp_enqueue_scripts', static function () {
    if (!is_singular('post') || get_post_meta(get_queried_object_id(),'_hbdp_demo',true)==='1') return;
    wp_enqueue_style('hbdp-article-design', HBDP_URL.'assets/article-design.css', array('hbdp-site'), '0.1.185');
}, 100);""",
        "add shared post template and scoped assets",
    )
    changed, amount = re.subn(r"(?m)^(\s*\*\s*Version:\s*)0\.1\.184(\s*)$",r"\g<1>0.1.185\g<2>",value)
    if amount != 1:
        raise AssertionError("Could not upgrade plugin version header exactly once")
    return changed

def patch_site(value):
    value = replace_once(
        value,
        "<?php elseif($section==='article'): $post=get_queried_object();$spec=null;",
        """<?php elseif($section==='article' && get_post_meta(get_queried_object_id(),'_hbdp_demo',true)!=='1'): ?>
<?php hbdp_render_article_page(); ?>
<?php elseif($section==='article'): $post=get_queried_object();$spec=null;""",
        "normal article vs. historic demo article",
    )
    value = replace_once(
        value, "<title><?php",
        "<?php if ($section !== 'article' || !defined('WPSEO_VERSION')): ?><title><?php",
        "Yoast-controlled article title begins",
    )
    value = replace_once(
        value, "?> – Hab & Bewahr</title><?php wp_head();",
        "?> – Hab & Bewahr</title><?php endif; wp_head();",
        "Yoast-controlled article title ends",
    )
    return value

def main():
    if SOURCE.stat().st_size != 84339643:
        raise AssertionError("Original plugin size differs from Campus Current")
    sha = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    if sha != EXPECTED_SHA:
        raise AssertionError("Original plugin ZIP was replaced; refusing unsafe build")
    with zipfile.ZipFile(SOURCE) as zin:
        if zin.testzip() is not None:
            raise AssertionError("Original plugin ZIP is corrupt")
        infos = zin.infolist()
        oldnames = {z.filename for z in infos}
        if len(oldnames) != 426 or MAIN not in oldnames or TEMPLATE not in oldnames:
            raise AssertionError("Unexpected original plugin structure")
        with zipfile.ZipFile(OUT,"w") as zout:
            changed = []
            for info in infos:
                data = zin.read(info.filename)
                if info.filename == MAIN:
                    data = patch_main(data.decode("utf-8")).encode("utf-8")
                    changed.append(info.filename)
                elif info.filename == TEMPLATE:
                    data = patch_site(data.decode("utf-8")).encode("utf-8")
                    changed.append(info.filename)
                zout.writestr(info, data)
            additions = {
                PREFIX + "includes/article-page.php": (ROOT / "article-page.php").read_bytes(),
                PREFIX + "assets/article-design.css": (ROOT / "article-design.css").read_bytes(),
            }
            if any(n in oldnames for n in additions):
                raise AssertionError("Extra module filename already exists in original")
            for name, data in additions.items():
                zout.writestr(name, data, compress_type=zipfile.ZIP_DEFLATED)
    with zipfile.ZipFile(OUT) as z:
        if len(z.namelist()) != 428 or z.testzip() is not None:
            raise AssertionError("Final ZIP count/integrity failed")
        # Absolute freeze: unchanged original data must be byte identical.
        with zipfile.ZipFile(SOURCE) as old:
            diffs = [n for n in old.namelist() if z.read(n) != old.read(n)]
        if set(diffs) != {MAIN, TEMPLATE}:
            raise AssertionError("Unexpected original file changes: "+repr(diffs))
    print("PASS: Original checked SHA256, CRC, 426 -> 428 entries")
    print("PASS: Exactly 2 modified original files + 2 new article files")
    print("NO WP content/category/other plugin/K0 changed")
    print("RESULT:",OUT,OUT.stat().st_size,"bytes")
    print("SHA256:",hashlib.sha256(OUT.read_bytes()).hexdigest())

if __name__ == "__main__":
    main()
