#!/usr/bin/env python3
"""Fix obsolete image-less fake Hobby Depot demo product tiles in HD003 1.50.805.

Source is the verified current 1.50.804 full ZIP, not another plugin.
Only the single official design test article is affected by existing conditional.
"""
from pathlib import Path
from zipfile import ZipFile
from tempfile import TemporaryDirectory
from io import BytesIO
from hashlib import sha256
import subprocess
ROOT=Path("protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/PLUGINS/ISOLIERTE_PLUGINS/HD-003-DESIGN-TEMPLATE-KIT")
ORIG=ROOT/"HOBBY_DEPOT_DESIGN_HD003_1.50.804.zip"
CUR=ROOT/"CURRENT.zip"
OUT=ROOT/"HOBBY_DEPOT_DESIGN_HD003_1.50.805.zip"
HASH="ea85bde0f9bc48d679112df2dac5a6b9d53f63379f9a4633979b7be126b04a52"
MAIN="affiliate-portal-template-kit/pferde-template-kit.php"
HERO="affiliate-portal-template-kit/includes/hobby-depot-article-hero-v150789.php"
PHOTO="affiliate-portal-template-kit/assets/hobby-depot-v150780/hobby-masters/sportdrachen.webp"
def one(s,a,b,label):
    assert s.count(a)==1,(label,s.count(a),a[:75])
    return s.replace(a,b)
assert sha256(ORIG.read_bytes()).hexdigest()==HASH
with ZipFile(ORIG) as z:
    assert z.testzip() is None and len(z.namelist())==1290 and PHOTO in z.namelist()
    current_main=z.read(MAIN).decode('utf8')
    assert " * Version: 1.50.804" in current_main[:1000]
    body=z.read(HERO).decode('utf8')
    assert body.count("function hd003_hab_article_content_v150804(")==1
    assert body.count("function hd003_hab_article_sidebar_v150804(")==1

ADD_STYLE=r"""
/* 1.50.805: photo-led related category card, not unlicensed product tiles.
   Scope matches previous v150804 design-test condition; no global CSS. */
body.pftk-design-profile-hobby-depot.single-post.hd-article-hab-preview-v150804 #content
.hd-article-sidebar-photo-v150805{
 display:block!important;
 width:100%!important;
 overflow:hidden!important;
 border-radius:4px!important;
 margin:0 0 12px!important;
 background:#e2efec!important;
}
body.pftk-design-profile-hobby-depot.single-post.hd-article-hab-preview-v150804 #content
.hd-article-sidebar-photo-v150805 img{
 display:block!important;
 width:100%!important;
 aspect-ratio:16/9!important;
 height:auto!important;
 object-fit:cover!important;
 object-position:center!important;
 border:0!important;
 margin:0!important;
}
body.pftk-design-profile-hobby-depot.single-post.hd-article-hab-preview-v150804 #content
.hd-article-sidebar-card-v150804{
 overflow:hidden!important;
}
body.pftk-design-profile-hobby-depot.single-post.hd-article-hab-preview-v150804 #content
.hd-article-sidebar-photo-v150805:hover img{
 opacity:.93!important;
}
/* Only as a defensive fallback for cached older design-test HTML.
   Server-side filter removes the same obsolete sections from WP output. */
body.hd-article-hab-preview-v150804 .hddemo-product-grid,
body.hd-article-hab-preview-v150804 #hddemo-produkte,
body.hd-article-hab-preview-v150804 #hddemo-produkte + p,
body.hd-article-hab-preview-v150804 .hddemo-related,
body.hd-article-hab-preview-v150804 aside[aria-label="Bannerplatz Testartikel"]{
 display:none!important;
}
"""

# Existing single scoped preview sidebar includes one canonical category text link.
before=r"""    $cat_url=get_category_link((int)$first->term_id);
    if ($cat_url && !is_wp_error($cat_url)) {
        $out.='<nav class="hd-article-sidebar-card-v150804" aria-label="Passende Kategorie">'
            .'<h2>Mehr zum Thema</h2><a href="'.esc_url($cat_url).'">'
            .esc_html($first->name).' ansehen</a></nav>';
    }
"""
after=r"""    $cat_url=get_category_link((int)$first->term_id);
    if ($cat_url && !is_wp_error($cat_url)) {
        // Existing category-image library, original separate sport kite photo;
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
            .esc_html($first->name).' ansehen</a></nav>';
    }
"""
assert body.count(before)==1,(body.count(before),"Sidebar target changed unexpectedly")
body=body.replace(before,after)
# The old design-test was imported into WordPress once; simply changing its
# source demo generator does not modify the existing WP post. Remove its fixed
# hardcoded fake products and generic manufacturer ad on render (read-only).
needle=r"""    $content=preg_replace('~<nav\b(?=[^>]*aria-label=["\']Inhaltsverzeichnis des Testartikels["\'])[^>]*>.*?</nav>~is','',$content,1);
    $sidebar=hd003_hab_article_sidebar_v150804($post);"""
replace=r"""    $content=preg_replace('~<nav\b(?=[^>]*aria-label=["\']Inhaltsverzeichnis des Testartikels["\'])[^>]*>.*?</nav>~is','',$content,1);
    // Remove only the obsolete demo product section (no product photos,
    // no live prices, no provider feed). Keep actual WordPress articles,
    // numbered safety steps, real HD009 Affiliate links and real content.
    $content=preg_replace('~<h2\b[^>]*\bid=["\']hddemo-produkte["\'][^>]*>.*?(?=<h2\b[^>]*>)~is','',$content,1);
    // This extra block linked back into the same article rather than to
    // actual related categories. The genuine category card is now at right.
    $content=preg_replace('~<h2\b[^>]*>\s*Passende Themen bei Hobby Depot\s*</h2>.*?(?=<h2\b[^>]*>)~is','',$content,1);
    $content=preg_replace('~<aside\b(?=[^>]*aria-label=["\']Bannerplatz Testartikel["\'])[^>]*>.*?</aside>~is','',$content,1);
    $sidebar=hd003_hab_article_sidebar_v150804($post);"""
body=one(body,needle,replace,"legacy inline demo card filter")
# Last style block is unique; add into existing v150789 style to outrank
# normal ListingHive styles, no new style file and no extra HTTP request.
body=one(body, "</style>\n<?php\n}\nadd_action('wp_head', 'hd003_article_hero_style_v150789', 999999);",
         ADD_STYLE+"</style>\n<?php\n}\nadd_action('wp_head', 'hd003_article_hero_style_v150789', 999999);","style")
with ZipFile(ORIG) as z,ZipFile(BytesIO(ORIG.read_bytes())) as verify:
    assert z.testzip() is None
out=BytesIO()
changes=[]
with ZipFile(ORIG) as z,ZipFile(out,'w') as w:
    for info in z.infolist():
        old=z.read(info.filename)
        new=old
        if info.filename==MAIN:
            s=old.decode('utf8')
            s=one(s," * Version: 1.50.804"," * Version: 1.50.805","header version")
            s=one(s,"const VERSION = '1.50.804';","const VERSION = '1.50.805';","cache version")
            new=s.encode('utf8')
        if info.filename==HERO:new=body.encode('utf8')
        if new!=old:changes.append(info.filename)
        w.writestr(info,new)
    w.comment=z.comment
assert set(changes)=={MAIN,HERO},changes
data=out.getvalue()
with ZipFile(BytesIO(data)) as z:
    assert z.testzip() is None and len(z.namelist())==1290
    with TemporaryDirectory() as temp:
        phpfiles=[x for x in z.namelist() if x.endswith('.php')]
        assert len(phpfiles)==13
        for path in phpfiles:
            f=Path(temp)/path
            f.parent.mkdir(parents=True,exist_ok=True)
            f.write_bytes(z.read(path))
            check=subprocess.run(['php','-l',str(f)],capture_output=True,text=True)
            assert check.returncode==0,(path,check.stderr)
CUR.write_bytes(data)
OUT.write_bytes(data)
assert OUT.read_bytes()==CUR.read_bytes()
print("HD003_150805_BUILD_PASS","size",len(data),"sha256",sha256(data).hexdigest(),"changed",changes)
print("PHP_PASS 13","ZIP_PASS 1290","APPROVED_CATEGORY_PHOTO_PRESENT")
