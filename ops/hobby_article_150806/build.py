#!/usr/bin/env python3
"""HD003 1.50.806: enforce single Hero photo + Hab style content policy.

Exact 1.50.805 is source. One existing Design plugin only.
All single posts: remove duplicate inline hero photo and generic auto post banner.
The approved two-column Hab-style layout remains limited to its one design test.
Never add a photo in article sidebar. All category/registration/home pages unchanged.
"""
from pathlib import Path
from zipfile import ZipFile
from io import BytesIO
from tempfile import TemporaryDirectory
from hashlib import sha256
import subprocess

ROOT=Path("protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/PLUGINS/ISOLIERTE_PLUGINS/HD-003-DESIGN-TEMPLATE-KIT")
SOURCE=ROOT/"HOBBY_DEPOT_DESIGN_HD003_1.50.805.zip"
CURRENT=ROOT/"CURRENT.zip"
RELEASE=ROOT/"HOBBY_DEPOT_DESIGN_HD003_1.50.806.zip"
EXPECTED="e90b7e220fca7226b75da8ec7adabb80407e18576350744b1dd37346b37c7a72"
MAIN="affiliate-portal-template-kit/pferde-template-kit.php"
HERO="affiliate-portal-template-kit/includes/hobby-depot-article-hero-v150789.php"

def once(s,old,new,label):
    count=s.count(old)
    assert count==1,(label,count,old[:135])
    return s.replace(old,new)
assert sha256(SOURCE.read_bytes()).hexdigest()==EXPECTED,"Source ZIP changed, stop"
with ZipFile(SOURCE) as zin:
    assert zin.testzip() is None and len(zin.namelist())==1290
    src=zin.read(HERO).decode("utf8")
    main=zin.read(MAIN).decode("utf8")
    assert "const VERSION = '1.50.805';" in main

# The sidebar currently hard-codes the Sportdrachen image for any category:
# wrong for other hobbies, and creates a third photograph here. Follow Hab:
# text-only navigation plus real related links, not an invented image.
start=src.index("    $cat_url=get_category_link((int)$first->term_id);",src.index("function hd003_hab_article_sidebar_v150804("))
end=src.index("    $out.='</aside>';",start)
old=src[start:end]
assert "hd-article-sidebar-photo-v150805" in old
replacement=r"""    $cat_url=get_category_link((int)$first->term_id);
    if ($cat_url && !is_wp_error($cat_url)) {
        $out.='<nav class="hd-article-sidebar-card-v150804" aria-label="Passende Kategorie">'
            .'<h2>Mehr zum Thema</h2><a href="'.esc_url($cat_url).'">'
            .esc_html($first->name).' ansehen</a></nav>';
    }
"""
src=src[:start]+replacement+src[end:]
# Remove two non-working old methods instead of layering another workaround:
# ListingHive uses .post__text, not Astra .entry-content; its footer JS
# and first-of-type CSS never stopped the actual duplicated photo.
old_begin=src.index("function hd003_article_hero_deduplicate_inline_v150789(")
old_end=src.index("/* HD003 1.50.804 – article only",old_begin)
assert "add_action('wp_footer', 'hd003_article_hero_deduplicate_inline_v150789', 998);" in src[old_begin:old_end]
src=src[:old_begin]+src[old_end:]
old_css='''/* Inline image was re-used as hero. Keep content but avoid its duplicate photograph. */
html body.pftk-design-profile-hobby-depot.single-post.hd-article-inline-image-v150789 #content article.post .entry-content figure.wp-block-image:first-of-type{display:none!important}
html body.pftk-design-profile-hobby-depot.single-post.hd-article-inline-image-v150789 #content article.post .entry-content>.wp-block-image:first-of-type{display:none!important}
'''
src=once(src,old_css,'/* One Hero, no duplicate in content: enforced on the real post HTML by HD003 1.50.806. */\n',"obsolete Astra CSS")
photo_start=src.index("/* 1.50.805: photo-led related category card, not unlicensed product tiles.")
photo_end=src.index("/* Only as a defensive fallback for cached older design-test HTML.",photo_start)
src=src[:photo_start]+src[photo_end:]
assert "hd-article-sidebar-photo-v150805" not in src, "Old picture card CSS still active"
assert "function hd003_hab_article_content_v150804(" in src

# Hab design contract: a banner/product offer only when there is
# real approved material. Auto generic Amazon search banners inserted
# inline aren't offer cards. Remove post_inline_banner from the ARTICLE,
# never from category, Hobbyregister, home or non-post content.
# When the hero came from a Gutenberg inline picture, remove its rendered
# block instead of relying on broken Astra .entry-content CSS/JS selectors.
added=r'''
/**
 * HD003 1.50.806 – one-Hero article guarantee, independent of theme classes.
 * Hab & Bewahr pattern: normal reading content and links at right, no
 * second photo and no generic affiliate creative without a real image.
 * Runs on public post main loop only, after the old template and ad filter.
 */
function hd003_article_single_hero_clean_v150806($content) {
    if (!is_string($content) || $content === '' || is_admin() ||
        is_feed() || !function_exists('is_singular') ||
        !is_singular('post') || !in_the_loop() || !is_main_query()) {
        return $content;
    }
    $post = function_exists('get_queried_object') ? get_queried_object() : null;
    if (!($post instanceof WP_Post) || (string)$post->post_type !== 'post') {
        return $content;
    }

    // HD009's generic text-only Amazon search banner does not belong in
    // the article body. Its real product approval is a separate workflow.
    // Restrict to the exact post_inline_banner slot: never touch a category
    // banner, manually inserted product comparison or partner text link.
    $content=preg_replace(
        '~<div\b(?=[^>]*\bdata-ppar-slot\s*=\s*["\']post_inline_banner["\'])[^>]*>.*?</div>~is',
        '', $content
    );

    $hero=hd003_article_hero_data_v150789($post);
    $src=html_entity_decode((string)($hero['src'] ?? ''),ENT_QUOTES,'UTF-8');
    if ($src === '') { return $content; }
    $src=urldecode(preg_replace('~[?#].*$~','',$src));

    // A single exact source is used as Hero. Remove ONLY rendered Gutenberg
    // image figures with the same URL; all other relevant images stay.
    $content=preg_replace_callback(
        '~<figure\b(?=[^>]*\bclass\s*=\s*["\'][^"\']*\bwp-block-image\b[^"\']*["\'])[^>]*>.*?</figure>~is',
        static function($match) use ($src) {
            if (!preg_match('~<img\b[^>]*\bsrc\s*=\s*["\']([^"\']+)["\']~is',$match[0],$image)) {
                return $match[0];
            }
            $value=html_entity_decode((string)$image[1],ENT_QUOTES,'UTF-8');
            $value=urldecode(preg_replace('~[?#].*$~','',$value));
            return $src === $value ? '' : $match[0];
        },$content
    );

    return $content;
}
add_filter('the_content','hd003_article_single_hero_clean_v150806',9500);

/* Last-resort guard for a later-loaded affiliate slot. The real fix above
   removes its markup before output; this affects posts only, not archives. */
function hd003_article_one_hero_css_v150806() {
    if (is_admin() || !is_singular('post')) { return; }
    echo '<style id="hd003-one-hero-guard-v150806">body.pftk-design-profile-hobby-depot.single-post [data-ppar-slot="post_inline_banner"]{display:none!important}</style>';
}
add_action('wp_head','hd003_article_one_hero_css_v150806',999999);
'''
assert "function hd003_article_single_hero_clean_v150806(" not in src
src += "\n"+added

main=once(main," * Version: 1.50.805"," * Version: 1.50.806","header")
main=once(main,"const VERSION = '1.50.805';","const VERSION = '1.50.806';","cache version")
out=BytesIO();changes=[]
with ZipFile(SOURCE) as zin,ZipFile(out,"w") as zout:
    for item in zin.infolist():
        old=zin.read(item.filename)
        val=main.encode("utf8") if item.filename==MAIN else (
            src.encode("utf8") if item.filename==HERO else old)
        if val!=old:changes.append(item.filename)
        zout.writestr(item,val)
    zout.comment=zin.comment
assert set(changes)=={MAIN,HERO},changes
payload=out.getvalue()
with ZipFile(BytesIO(payload)) as z:
    assert len(z.namelist())==1290 and z.testzip() is None
    php=[n for n in z.namelist() if n.endswith(".php")]
    assert len(php)==13
    with TemporaryDirectory() as td:
        for n in php:
            dest=Path(td)/n;dest.parent.mkdir(parents=True,exist_ok=True)
            dest.write_bytes(z.read(n))
            check=subprocess.run(["php","-l",str(dest)],capture_output=True,text=True)
            assert check.returncode==0,(n,check.stderr)
CURRENT.write_bytes(payload)
RELEASE.write_bytes(payload)
assert CURRENT.read_bytes()==RELEASE.read_bytes()
print("HD003_150806_FULL_PLUGIN_PASS",
      "files",1290,"php",13,"bytes",len(payload),
      "sha256",sha256(payload).hexdigest(),"changed",changes)
