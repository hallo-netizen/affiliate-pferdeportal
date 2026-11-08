#!/usr/bin/env python3
"""HD003 1.50.804 – Hab-inspired Hobby Depot article design, test article only.
No change to editorial content, existing Hero picture, SEO, ad routing, navigation,
home, category, Hobbyregister, or any other plugin. One update of existing HD003.
"""
from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZipFile
from io import BytesIO
from hashlib import sha256
import subprocess

ROOT=Path("protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/PLUGINS/ISOLIERTE_PLUGINS/HD-003-DESIGN-TEMPLATE-KIT")
SRC=ROOT/"CURRENT.zip"
NAME="HOBBY_DEPOT_DESIGN_HD003_1.50.804.zip"
EXPECTED="06e412f04fd3768477c6e825b39708baed0927be68260fce55fd316dff14d95f"
MAIN="affiliate-portal-template-kit/pferde-template-kit.php"
HERO="affiliate-portal-template-kit/includes/hobby-depot-article-hero-v150789.php"

# One dedicated design namespace. Reuses actual ListingHive .post__text,
# not incorrect horse-portal selectors like article.post .entry-content.
STYLE=r"""
/* HD003 1.50.804 – Hab & Bewahr article reading pattern, translated to
   Hobby Depot. Intentionally confined to the already-published design test.
   No global cascade to categories, register or unrelated single posts. */
body.pftk-design-profile-hobby-depot.single-post.hd-article-hab-preview-v150804 .hd-article-kicker-v150789{
 display:none!important;
}
body.pftk-design-profile-hobby-depot.single-post.hd-article-hab-preview-v150804 .hd-article-heading-v150789{
 padding:9px 0 17px!important;
 background:transparent!important;
}
body.pftk-design-profile-hobby-depot.single-post.hd-article-hab-preview-v150804 .hd-article-heading-v150789 h1{
 font-family:Montserrat,"Segoe UI",Arial,sans-serif!important;
 font-size:clamp(30px,2.55vw,36px)!important;
 font-weight:800!important;
 line-height:1.23!important;
 letter-spacing:-.025em!important;
 max-width:930px!important;
}
body.pftk-design-profile-hobby-depot.single-post.hd-article-hab-preview-v150804 .hd-article-photo-hero-v150789{
 height:clamp(240px,25vw,345px)!important;
}
body.pftk-design-profile-hobby-depot.single-post.hd-article-hab-preview-v150804 #content.site-content{
 padding-top:20px!important;
}
body.pftk-design-profile-hobby-depot.single-post.hd-article-hab-preview-v150804 #content .row > main.col-sm-8.col-sm-offset-2{
 float:none!important;
 flex:0 0 100%!important;
 width:100%!important;
 max-width:100%!important;
 margin-left:0!important;
}
body.pftk-design-profile-hobby-depot.single-post.hd-article-hab-preview-v150804 #content .post--single{
 width:100%!important;
 max-width:none!important;
}
body.pftk-design-profile-hobby-depot.single-post.hd-article-hab-preview-v150804 #content .post__text{
 width:100%!important;
 max-width:none!important;
 color:#27434a!important;
 margin:0!important;
 padding:0!important;
 font-family:Montserrat,"Segoe UI",Arial,sans-serif!important;
 font-size:16px!important;
 line-height:1.7!important;
}
body.pftk-design-profile-hobby-depot.single-post.hd-article-hab-preview-v150804 #content .hd-article-body-grid-v150804{
 display:grid!important;
 grid-template-columns:minmax(0,1fr) minmax(265px,292px)!important;
 gap:32px!important;
 align-items:start!important;
 width:100%!important;
}
body.pftk-design-profile-hobby-depot.single-post.hd-article-hab-preview-v150804 #content .hd-article-reading-v150804{min-width:0!important}
body.pftk-design-profile-hobby-depot.single-post.hd-article-hab-preview-v150804 #content .hd-article-reading-v150804>p.hddemo-kicker{
 display:none!important;
}
body.pftk-design-profile-hobby-depot.single-post.hd-article-hab-preview-v150804 #content .hd-article-reading-v150804 p{
 font-family:inherit!important;
 font-size:16px!important;
 line-height:1.72!important;
 margin:0 0 1.13em!important;
 letter-spacing:0!important;
}
body.pftk-design-profile-hobby-depot.single-post.hd-article-hab-preview-v150804 #content .hd-article-reading-v150804>p.has-large-font-size{
 font-size:18px!important;
 font-weight:500!important;
 line-height:1.6!important;
 margin:0 0 21px!important;
 color:#345056!important;
}
body.pftk-design-profile-hobby-depot.single-post.hd-article-hab-preview-v150804 #content .hd-article-reading-v150804 h2,
body.pftk-design-profile-hobby-depot.single-post.hd-article-hab-preview-v150804 #content .hd-article-reading-v150804 h2.wp-block-heading{
 font-family:Montserrat,"Segoe UI",Arial,sans-serif!important;
 position:relative!important;
 font-size:23px!important;
 line-height:1.32!important;
 font-weight:750!important;
 color:#173b40!important;
 letter-spacing:-.015em!important;
 padding:13px 0 0!important;
 margin:32px 0 13px!important;
}
body.pftk-design-profile-hobby-depot.single-post.hd-article-hab-preview-v150804 #content .hd-article-reading-v150804 h2::before{
 content:""!important;
 position:absolute!important;
 top:0!important;
 left:0!important;
 width:38px!important;
 height:3px!important;
 border-radius:2px!important;
 background:#2f9a9a!important;
}
body.pftk-design-profile-hobby-depot.single-post.hd-article-hab-preview-v150804 #content .hd-article-reading-v150804 h3{
 font-family:Montserrat,"Segoe UI",Arial,sans-serif!important;
 font-size:19px!important;
 line-height:1.35!important;
 font-weight:750!important;
 margin:26px 0 12px!important;
 padding:0!important;
 color:#1c4148!important;
}
body.pftk-design-profile-hobby-depot.single-post.hd-article-hab-preview-v150804 #content .hd-article-reading-v150804 .wp-block-group h3{
 margin:0 0 12px!important;
}
body.pftk-design-profile-hobby-depot.single-post.hd-article-hab-preview-v150804 #content .hd-article-reading-v150804 ul,
body.pftk-design-profile-hobby-depot.single-post.hd-article-hab-preview-v150804 #content .hd-article-reading-v150804 ol{
 margin:12px 0 22px!important;
 padding-left:25px!important;
 font-size:16px!important;
 line-height:1.65!important;
}
body.pftk-design-profile-hobby-depot.single-post.hd-article-hab-preview-v150804 #content .hd-article-reading-v150804 li{margin-bottom:8px!important}
body.pftk-design-profile-hobby-depot.single-post.hd-article-hab-preview-v150804 #content .hd-article-reading-v150804 .wp-block-quote{
 margin:23px 0!important;
 padding:17px 20px!important;
 background:#edf5f3!important;
 border-left:4px solid #479e93!important;
}
body.pftk-design-profile-hobby-depot.single-post.hd-article-hab-preview-v150804 #content .hd-article-reading-v150804 .wp-block-image,
body.pftk-design-profile-hobby-depot.single-post.hd-article-hab-preview-v150804 #content .hd-article-reading-v150804 .wp-block-table{
 max-width:100%!important;
 margin:22px 0!important;
}
body.pftk-design-profile-hobby-depot.single-post.hd-article-hab-preview-v150804 #content .hd-article-reading-v150804 table{
 width:100%!important;
 border-collapse:collapse!important;
 font-size:14px!important;
 line-height:1.45!important;
}
body.pftk-design-profile-hobby-depot.single-post.hd-article-hab-preview-v150804 #content .hd-article-reading-v150804 th{
 background:#214d54!important;
 color:#fff!important;
}
body.pftk-design-profile-hobby-depot.single-post.hd-article-hab-preview-v150804 #content .hd-article-reading-v150804 th,
body.pftk-design-profile-hobby-depot.single-post.hd-article-hab-preview-v150804 #content .hd-article-reading-v150804 td{
 padding:10px 12px!important;
 border:1px solid #d7e2de!important;
}
body.pftk-design-profile-hobby-depot.single-post.hd-article-hab-preview-v150804 #content .hd-article-reading-v150804 .wp-block-table{
 overflow-x:auto!important;
 -webkit-overflow-scrolling:touch!important;
}
body.pftk-design-profile-hobby-depot.single-post.hd-article-hab-preview-v150804 #content .hd-article-sidebar-v150804{
 min-width:0!important;
 display:flex!important;
 flex-direction:column!important;
 gap:18px!important;
}
body.pftk-design-profile-hobby-depot.single-post.hd-article-hab-preview-v150804 #content .hd-article-sidebar-card-v150804{
 border:1px solid #dce8e5!important;
 background:#f4f8f6!important;
 border-radius:5px!important;
 padding:20px 20px 22px!important;
}
body.pftk-design-profile-hobby-depot.single-post.hd-article-hab-preview-v150804 #content .hd-article-sidebar-card-v150804 h2{
 margin:0 0 12px!important;
 padding:0!important;
 color:#1d4146!important;
 font-family:Montserrat,"Segoe UI",Arial,sans-serif!important;
 font-size:19px!important;
 font-weight:750!important;
 line-height:1.3!important;
}
body.pftk-design-profile-hobby-depot.single-post.hd-article-hab-preview-v150804 #content .hd-article-sidebar-card-v150804 a{
 color:#166b77!important;
 font-size:14px!important;
 line-height:1.48!important;
 font-weight:650!important;
 text-decoration:none!important;
}
body.pftk-design-profile-hobby-depot.single-post.hd-article-hab-preview-v150804 #content .hd-article-sidebar-card-v150804 a:hover{
 text-decoration:underline!important;
}
body.pftk-design-profile-hobby-depot.single-post.hd-article-hab-preview-v150804 #content .hd-article-sidebar-card-v150804 ul{
 list-style:none!important;
 margin:0!important;
 padding:0!important;
}
body.pftk-design-profile-hobby-depot.single-post.hd-article-hab-preview-v150804 #content .hd-article-sidebar-card-v150804 li{
 margin:0!important;
 border-top:1px solid #e0e9e5!important;
 padding:10px 0!important;
}
body.pftk-design-profile-hobby-depot.single-post.hd-article-hab-preview-v150804 #content .hd-article-sidebar-card-v150804 li:first-child{border-top:0!important;padding-top:0!important}
body.pftk-design-profile-hobby-depot.single-post.hd-article-hab-preview-v150804 #content .hd-article-sidebar-card-v150804 li:last-child{padding-bottom:0!important}
@media(max-width:920px){
 body.pftk-design-profile-hobby-depot.single-post.hd-article-hab-preview-v150804 #content .hd-article-body-grid-v150804{
  grid-template-columns:minmax(0,1fr)!important;
  gap:20px!important;
 }
 body.pftk-design-profile-hobby-depot.single-post.hd-article-hab-preview-v150804 #content .hd-article-sidebar-v150804{
  display:grid!important;
  grid-template-columns:repeat(auto-fit,minmax(230px,1fr))!important;
  gap:14px!important;
 }
}
@media(max-width:760px){
 body.pftk-design-profile-hobby-depot.single-post.hd-article-hab-preview-v150804 .hd-article-heading-v150789 h1{
  font-size:clamp(24px,6.2vw,29px)!important;
  line-height:1.25!important;
 }
 body.pftk-design-profile-hobby-depot.single-post.hd-article-hab-preview-v150804 .hd-article-photo-hero-v150789{
  height:275px!important;
 }
 body.pftk-design-profile-hobby-depot.single-post.hd-article-hab-preview-v150804 #content.site-content{
  padding-top:12px!important;
 }
 body.pftk-design-profile-hobby-depot.single-post.hd-article-hab-preview-v150804 #content .hd-article-reading-v150804 p{
  font-size:16px!important;line-height:1.65!important;
 }
 body.pftk-design-profile-hobby-depot.single-post.hd-article-hab-preview-v150804 #content .hd-article-reading-v150804>p.has-large-font-size{
  font-size:17px!important;line-height:1.57!important;
 }
 body.pftk-design-profile-hobby-depot.single-post.hd-article-hab-preview-v150804 #content .hd-article-reading-v150804 h2{
  font-size:21px!important;margin-top:28px!important;padding-top:12px!important;
 }
 body.pftk-design-profile-hobby-depot.single-post.hd-article-hab-preview-v150804 #content .hd-article-reading-v150804 h3{
  font-size:18px!important;
 }
 body.pftk-design-profile-hobby-depot.single-post.hd-article-hab-preview-v150804 #content .hd-article-sidebar-v150804{
  display:flex!important;flex-direction:column!important;
 }
 body.pftk-design-profile-hobby-depot.single-post.hd-article-hab-preview-v150804 #content .hd-article-sidebar-card-v150804{
  padding:18px!important;
 }
}
"""

ADDON=r"""
/* HD003 1.50.804 – article only, no additional plugin or duplicate template. */
function hd003_hab_article_preview_v150804($post = null) {
    if (!function_exists('is_singular') || !is_singular('post') ||
        !function_exists('get_post_meta')) { return false; }
    if (!($post instanceof WP_Post)) {
        $post = function_exists('get_queried_object') ? get_queried_object() : null;
    }
    return $post instanceof WP_Post &&
        (string)get_post_meta($post->ID,'_hddemo_layout_key',true) === 'hddemo-zw-vl-20261101';
}
function hd003_hab_article_body_class_v150804($classes) {
    if (!is_admin() && hd003_hab_article_preview_v150804()) {
        $classes[]='hd-article-hab-preview-v150804';
    }
    return $classes;
}
add_filter('body_class','hd003_hab_article_body_class_v150804',100);

function hd003_hab_article_sidebar_v150804($post) {
    if (!($post instanceof WP_Post)) { return ''; }
    $cats = get_the_category($post->ID);
    $first = null;
    foreach ((array)$cats as $term) {
        if ($term instanceof WP_Term && (string)$term->taxonomy === 'category') {
            $first=$term;break;
        }
    }
    if (!($first instanceof WP_Term)) { return ''; }
    $links=array();
    // Related articles only if truly published, in exactly this category.
    $related=get_posts(array(
        'post_type'=>'post','post_status'=>'publish','category__in'=>array((int)$first->term_id),
        'post__not_in'=>array((int)$post->ID),'posts_per_page'=>3,'orderby'=>'date',
        'order'=>'DESC','suppress_filters'=>false
    ));
    foreach ((array)$related as $other) {
        if (!($other instanceof WP_Post) || (int)$other->ID === (int)$post->ID) { continue; }
        // No hidden design-test duplicate recommendations.
        if (get_post_meta($other->ID,'_hddemo_layout_key',true)) { continue; }
        $link=get_permalink($other->ID);
        $title=get_the_title($other->ID);
        if ($link && $title) {
            $links[]='<li><a href="'.esc_url($link).'">'.esc_html($title).'</a></li>';
        }
    }
    $out='<aside class="hd-article-sidebar-v150804" aria-label="Weiterführende Themen">';
    if ($links) {
        $out.='<nav class="hd-article-sidebar-card-v150804" aria-label="Verwandte Beiträge">'
            .'<h2>Weiterlesen</h2><ul>'.implode('',$links).'</ul></nav>';
    }
    $cat_url=get_category_link((int)$first->term_id);
    if ($cat_url && !is_wp_error($cat_url)) {
        $out.='<nav class="hd-article-sidebar-card-v150804" aria-label="Passende Kategorie">'
            .'<h2>Mehr zum Thema</h2><a href="'.esc_url($cat_url).'">'
            .esc_html($first->name).' ansehen</a></nav>';
    }
    $out.='</aside>';
    return $out;
}
function hd003_hab_article_content_v150804($content) {
    if (is_admin() || is_feed() || !hd003_hab_article_preview_v150804() ||
        !in_the_loop() || !is_main_query() || !is_string($content)) { return $content; }
    if (strpos($content,'hd-article-body-grid-v150804') !== false) { return $content; }
    $post=get_queried_object();
    if (!($post instanceof WP_Post)) { return $content; }
    // The design-test's 1–5 table of contents is duplicative for a short
    // article. Numbered instructions inside the text remain untouched.
    $content=preg_replace('~<nav\b(?=[^>]*aria-label=["\']Inhaltsverzeichnis des Testartikels["\'])[^>]*>.*?</nav>~is','',$content,1);
    $sidebar=hd003_hab_article_sidebar_v150804($post);
    if ($sidebar === '') { return '<div class="hd-article-reading-v150804">'.$content.'</div>'; }
    return '<div class="hd-article-body-grid-v150804"><div class="hd-article-reading-v150804">'
      .$content.'</div>'.$sidebar.'</div>';
}
add_filter('the_content','hd003_hab_article_content_v150804',1200);
"""

def once(s,a,b,name):
    n=s.count(a)
    if n != 1:raise AssertionError((name,n,a[:85]))
    return s.replace(a,b)

data=SRC.read_bytes()
assert sha256(data).hexdigest()==EXPECTED,"Plugin source has changed since checked CURRENT"
with ZipFile(BytesIO(data)) as z:
    assert z.testzip() is None
    total=len(z.namelist())
    phpcount=sum(x.endswith('.php') for x in z.namelist())
    assert total==1290 and phpcount==13,(total,phpcount)
out=BytesIO()
changed=[]
with ZipFile(BytesIO(data)) as old,ZipFile(out,'w') as new:
    for info in old.infolist():
        b=old.read(info.filename);a=b
        if info.filename==MAIN:
            s=b.decode('utf-8')
            s=once(s," * Version: 1.50.803"," * Version: 1.50.804","WordPress header")
            s=once(s,"const VERSION = '1.50.803';","const VERSION = '1.50.804';","plugin cache version")
            a=s.encode('utf-8')
        if info.filename==HERO:
            s=b.decode('utf-8')
            target="</style>\n<?php\n}\nadd_action('wp_head', 'hd003_article_hero_style_v150789', 999999);"
            s=once(s,target,STYLE+"\n"+target,"one single-post style block")
            assert "function hd003_hab_article_content_v150804" not in s
            s+="\n"+ADDON
            a=s.encode('utf-8')
        if a!=b:changed.append(info.filename)
        new.writestr(info,a)
    new.comment=old.comment
assert set(changed)=={MAIN,HERO},changed
payload=out.getvalue()
with ZipFile(BytesIO(payload)) as z:
    assert len(z.namelist())==1290 and z.testzip() is None
    head=z.read(MAIN).decode()
    assert ' * Version: 1.50.804' in head.split('*/',1)[0]
    assert "const VERSION = '1.50.804';" in head
    body=z.read(HERO).decode()
    assert 'hd003_hab_article_content_v150804' in body
    assert 'hd-article-hab-preview-v150804' in body
    assert "Inhaltsverzeichnis des Testartikels" in body
    assert "p.has-large-font-size" in body
    with TemporaryDirectory() as td:
        all_php=[n for n in z.namelist() if n.endswith('.php')]
        assert len(all_php)==13
        for n in all_php:
            file=Path(td)/n
            file.parent.mkdir(parents=True,exist_ok=True)
            file.write_bytes(z.read(n))
            result=subprocess.run(['php','-l',str(file)],capture_output=True,text=True)
            assert result.returncode==0,(n,result.stderr)
SRC.write_bytes(payload)
TARGET=ROOT/NAME
TARGET.write_bytes(payload)
assert TARGET.read_bytes()==SRC.read_bytes()
print('HD003_HAB_ARTICLE_BUILD_PASS',NAME,'size',len(payload),'sha256',sha256(payload).hexdigest(),
      'php',13,'entries',1290,'modified',changed)
