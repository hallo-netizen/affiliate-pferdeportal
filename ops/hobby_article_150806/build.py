#!/usr/bin/env python3
"""HD003 1.50.806: actual Hab article structure for all WordPress posts.
One title/photo above the reading copy inside the LEFT grid column, real
related links only in the RIGHT; same post, no 2nd hero and no fake products.
Exact source version check prevents overwriting unrelated plugin work.
"""
from pathlib import Path
from zipfile import ZipFile
from hashlib import sha256
from io import BytesIO
from tempfile import TemporaryDirectory
import re,subprocess

ROOT=Path("protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/PLUGINS/ISOLIERTE_PLUGINS/HD-003-DESIGN-TEMPLATE-KIT")
SOURCE=ROOT/"HOBBY_DEPOT_DESIGN_HD003_1.50.805.zip"
CURRENT=ROOT/"CURRENT.zip"
OUT=ROOT/"HOBBY_DEPOT_DESIGN_HD003_1.50.806.zip"
BASE_HASH="e90b7e220fca7226b75da8ec7adabb80407e18576350744b1dd37346b37c7a72"
MAIN="affiliate-portal-template-kit/pferde-template-kit.php"
PROFILE="affiliate-portal-template-kit/includes/class-hobby-depot-profile-v150709.php"
HERO="affiliate-portal-template-kit/includes/hobby-depot-article-hero-v150789.php"
assert sha256(SOURCE.read_bytes()).hexdigest()==BASE_HASH,"Original 1.50.805 mismatch"
assert CURRENT.read_bytes()==SOURCE.read_bytes(),"Current changed: do not overwrite"
def one(s,b,a,why):
    n=s.count(b)
    assert n==1,(why,"count",n,b[:130])
    return s.replace(b,a)

content_regex=r'''
function hd003_article_single_hero_v150806($html, $post) {
    if (!($post instanceof WP_Post) || !is_string($html)) { return $html; }
    // Actual existing title/hero source from the Bildzentrale takes priority.
    // The FIRST Gutenberg figure is removed only if it displays precisely
    // the same image as the hero (not a technical illustration or another photo).
    $hero=hd003_article_hero_data_v150789($post);
    $src=(string)($hero['src'] ?? '');
    if ($src === '') { return $html; }
    $removed=false;
    return preg_replace_callback(
        '~<figure\b(?=[^>]*class=["\'][^"\']*\bwp-block-image\b)[^>]*>.*?</figure>~is',
        static function ($m) use ($src,&$removed) {
            if ($removed || !preg_match('~<img\b[^>]*\bsrc=["\']([^"\']+)["\']~is',$m[0],$match)) {
                return $m[0];
            }
            $body_src=html_entity_decode((string)$match[1],ENT_QUOTES,'UTF-8');
            if ($body_src === $src ||
                (function_exists('get_post_thumbnail_id') && function_exists('wp_get_attachment_url') &&
                 get_post_thumbnail_id($GLOBALS['post']->ID ?? 0) &&
                 $body_src === (string)wp_get_attachment_url(get_post_thumbnail_id($GLOBALS['post']->ID ?? 0)))) {
                $removed=true;
                return '';
            }
            return $m[0];
        },
        $html
    );
}
'''
# Avoid using the global $post inside the dedup callback. It is not necessarily
# the queried post in secondary loops, and we already have the hero URL.
content_regex=content_regex.replace(
"""            if ($body_src === $src ||
                (function_exists('get_post_thumbnail_id') && function_exists('wp_get_attachment_url') &&
                 get_post_thumbnail_id($GLOBALS['post']->ID ?? 0) &&
                 $body_src === (string)wp_get_attachment_url(get_post_thumbnail_id($GLOBALS['post']->ID ?? 0)))) {""",
"""            if ($body_src === $src) {""")

css_add=r"""
/* HD003 1.50.806 – use Hab's actual columns: title/hero INSIDE article left,
   rather than a site-wide image above the two columns. Only single posts. */
body.pftk-design-profile-hobby-depot.single-post.hd-article-hab-preview-v150804
#content .hd-article-reading-v150804>.hd-article-top-v150789{
 width:100%!important;max-width:none!important;
 margin:0 0 21px!important;
 padding:0!important;
}
body.pftk-design-profile-hobby-depot.single-post.hd-article-hab-preview-v150804
#content .hd-article-reading-v150804>.hd-article-top-v150789 .hd-article-heading-v150789{
 padding:5px 0 17px!important;margin:0!important;
}
body.pftk-design-profile-hobby-depot.single-post.hd-article-hab-preview-v150804
#content .hd-article-reading-v150804>.hd-article-top-v150789 .hd-article-photo-hero-v150789{
 height:clamp(245px,28vw,350px)!important;
 border-radius:5px!important;
 margin:0!important;
}
body.pftk-design-profile-hobby-depot.single-post.hd-article-hab-preview-v150804
#content .hd-article-reading-v150804>.hd-article-top-v150789+.has-large-font-size{
 margin-top:20px!important;
}
/* Only hero-photo as editorial image on this test: no secondary kite picture.
   Any DIFFERENT instructional figure remains part of original article. */
body.pftk-design-profile-hobby-depot.single-post.hd-article-hab-preview-v150804
#content .hd-article-sidebar-photo-v150805{display:none!important}
/* Hab places real products alongside editorial content, not empty banners.
   Until HD009 provides an approved image, don't display an image-less
   'Amazon' creative in normal articles, especially not above the intro. */
body.pftk-design-profile-hobby-depot.single-post.hd-article-hab-preview-v150804
#content .ppar-affiliate-slot:has(.hdar-ci-amazon-banner-text){
 display:none!important;
}
body.pftk-design-profile-hobby-depot.single-post.hd-article-hab-preview-v150804
#content .hd-article-sidebar-card-v150804{
 background:#f4f8f6!important;
}
@media(max-width:920px){
 body.pftk-design-profile-hobby-depot.single-post.hd-article-hab-preview-v150804
 #content .hd-article-reading-v150804>.hd-article-top-v150789{margin-bottom:16px!important}
}
@media(max-width:760px){
 body.pftk-design-profile-hobby-depot.single-post.hd-article-hab-preview-v150804
 #content .hd-article-reading-v150804>.hd-article-top-v150789 .hd-article-photo-hero-v150789{
 height:255px!important;
 }
}
"""

def update_profile(src):
    s=src.decode()
    # This is the *existing* sole output site for the article hero.
    # Keep the breadcrumb, but move title+hero into the left Hab column.
    target="""                echo '<div class="hd-universal-top-v150616">'.self::render_breadcrumb()
                    . (function_exists('hd003_article_hero_markup_v150789') ? hd003_article_hero_markup_v150789($obj) : '')
                    . '</div>';"""
    new="""                // HD003 1.50.806: Hab article columns render the sole
                // title/hero inside their left editorial column.
                echo '<div class="hd-universal-top-v150616">'.self::render_breadcrumb().'</div>';"""
    return one(s,target,new,"move only post hero (category/page untouched)").encode()

def update_hero(src):
    s=src.decode()
    # Frontend-only visible title. No stale "Fachartikel" label.
    s=one(s,
        """$html = '<div class="hd-article-top-v150789"><div class="hd-article-heading-v150789">'
      . '<span class="hd-article-kicker-v150789">Fachartikel</span>'
      . '<h1>' . esc_html($title) . '</h1></div>';""",
        """$html = '<div class="hd-article-top-v150789"><div class="hd-article-heading-v150789">'
      . '<h1>' . esc_html($title) . '</h1></div>';""",
        "remove label from actual hero markup")
    # Reuse translated Hab CSS; the existing sidebar photo is removed below.
    s=one(s,"</style>\n<?php\n}\nadd_action('wp_head', 'hd003_article_hero_style_v150789', 999999);",
          css_add+"</style>\n<?php\n}\nadd_action('wp_head', 'hd003_article_hero_style_v150789', 999999);",
          "append scoped Hab article CSS")
    # Enable Hab-inspired article style on all genuine posts instead of the
    # one DESIGNTEST; still never on pages/categories/Hobbyregister.
    s=one(s,
        """    return $post instanceof WP_Post &&
        (string)get_post_meta($post->ID,'_hddemo_layout_key',true) === 'hddemo-zw-vl-20261101';""",
        """    return $post instanceof WP_Post && (string)$post->post_type === 'post';""",
        "all regular posts use same Hab layout")
    # Remove a hardcoded, story-specific second hero from the sidebar.
    sidebar_old="""        // Existing category-image library, original separate sport kite photo;
        // never pretend this is an Amazon product photo.
        $photo='assets/hobby-depot-v150780/hobby-masters/sportdrachen.webp';
        $photo_on_disk=dirname(__DIR__).'/'.$photo;
        $photo_url=is_file($photo_on_disk)
          ? plugins_url($photo,dirname(__DIR__).'/pferde-template-kit.php') : '';
        $out.='<nav class="hd-article-sidebar-card-v150804" aria-label="Passende Kategorie">'
            .'<h2>Mehr zum Thema</h2>';
        if ($photo_url !== '') {
            $out.='<a class="hd-article-sidebar-photo-v150805" href="'.esc_url($cat_url).'">'
                .'<img src="'.esc_url($photo_url).'" alt="Lenkdrachen im Flug" loading="lazy" decoding="async">'
                .'</a>';
        }
        $out.='<a href="'.esc_url($cat_url).'">'
            .esc_html($first->name).' ansehen</a></nav>';"""
    sidebar_new="""        // Hab original: simple real category link. No duplicate hero
        // picture, fabricated product photo, or universal kite image.
        $out.='<nav class="hd-article-sidebar-card-v150804" aria-label="Passende Kategorie">'
            .'<h2>Mehr zum Thema</h2><a href="'.esc_url($cat_url).'">'
            .esc_html($first->name).' ansehen</a></nav>';"""
    s=one(s,sidebar_old,sidebar_new,"copy original Hab sidebar, not extra photo card")
    # Source-level hero dedup covers featured images AND inline-as-hero fallback,
    # unlike old JS which only covered fallback and wrong theme selector.
    def_prefix="function hd003_hab_article_content_v150804($content) {"
    s=one(s,def_prefix,content_regex+"\n"+def_prefix,"dedup function")
    s=one(s,
        """    $sidebar=hd003_hab_article_sidebar_v150804($post);
    if ($sidebar === '') { return '<div class="hd-article-reading-v150804">'.$content.'</div>'; }
    return '<div class="hd-article-body-grid-v150804"><div class="hd-article-reading-v150804">'
      .$content.'</div>'.$sidebar.'</div>';""",
        """    // Copy Hab article layout structure: heading + ONE hero + reading
    // inside left column, sidebar contains only actual matching links.
    $content=hd003_article_single_hero_v150806($content,$post);
    $hero=hd003_article_hero_markup_v150789($post);
    $sidebar=hd003_hab_article_sidebar_v150804($post);
    return '<div class="hd-article-body-grid-v150804"><div class="hd-article-reading-v150804">'
      .$hero.$content.'</div>'.$sidebar.'</div>';""",
        "actual Hab two-column structure instead of post-footer sidebar")
    # No changes to post_content; Gutenberg body and editorial source preserved.
    assert s.count('function hd003_article_single_hero_v150806(')==1
    return s.encode()

data=SOURCE.read_bytes()
output=BytesIO();changed=[]
with ZipFile(BytesIO(data)) as orig, ZipFile(output,"w") as new:
    assert orig.testzip() is None
    assert len(orig.namelist())==1290
    for info in orig.infolist():
        b=orig.read(info.filename);a=b
        if info.filename==MAIN:
            s=b.decode()
            s=one(s," * Version: 1.50.805"," * Version: 1.50.806","WordPress version")
            s=one(s,"const VERSION = '1.50.805';","const VERSION = '1.50.806';","cache version")
            a=s.encode()
        if info.filename==PROFILE:a=update_profile(b)
        if info.filename==HERO:a=update_hero(b)
        if a!=b:changed.append(info.filename)
        new.writestr(info,a)
    new.comment=orig.comment
assert set(changed)=={MAIN,PROFILE,HERO},changed
payload=output.getvalue()
with ZipFile(BytesIO(payload)) as z:
    assert z.testzip() is None and len(z.namelist())==1290
    with TemporaryDirectory() as tmp:
        names=[n for n in z.namelist() if n.endswith(".php")]
        assert len(names)==13
        for n in names:
            file=Path(tmp)/n
            file.parent.mkdir(parents=True,exist_ok=True)
            file.write_bytes(z.read(n))
            r=subprocess.run(["php","-l",str(file)],capture_output=True,text=True)
            assert r.returncode==0,(n,r.stderr)
CURRENT.write_bytes(payload)
OUT.write_bytes(payload)
assert CURRENT.read_bytes()==OUT.read_bytes()
print("HD003_150806_BUILD_PASS",len(payload),"sha256",sha256(payload).hexdigest(),"changed",changed)
print("PHP_PASS 13","CRC_PASS 1290","ONLY_EXISTING_DESIGN_PLUGIN_MODIFIED")
