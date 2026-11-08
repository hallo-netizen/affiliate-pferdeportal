#!/usr/bin/env python3
"""HD009 v0.1.30: fix provider-first picture-backed article card pipeline.

The 0.1.29 ZIP and existing provider campaign/feed logic are the sole source.
No new table, media downloads or WordPress setting mutations.
Provider cards (eBay/idealo if currently approved and enabled) outrank manual
Amazon photo fallback and are placed in the existing Hab-like article sidebar.
"""
from pathlib import Path
from zipfile import ZipFile
from io import BytesIO
from hashlib import sha256
from tempfile import TemporaryDirectory
import subprocess
ROOT=Path("protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/PLUGINS/ISOLIERTE_PLUGINS/HD-009-AFFILIATE-ZENTRALE")
SRC=ROOT/"HOBBY_DEPOT_AFFILIATE_HD009_0.1.29.zip"
CUR=ROOT/"CURRENT.zip"
OUT=ROOT/"HOBBY_DEPOT_AFFILIATE_HD009_0.1.30.zip"
EXPECTED="56aa1338e27bf0582a24e82f20184bccca782555028d9104efee96d0d2059dce"
MAIN="affiliate-portal-router/hobby-depot-affiliate-router.php"
CLASS="affiliate-portal-router/includes/class-hdar-amazon-start.php"
ARTICLE="affiliate-portal-router/includes/trait-ppar-article-plans.php"
CSS="affiliate-portal-router/assets/hdar-amazon-start.css"
def once(text,old,new,reason):
    n=text.count(old)
    assert n==1,(reason,n,old[:165])
    return text.replace(old,new)
assert sha256(SRC.read_bytes()).hexdigest()==EXPECTED,"Original current changed; stop before modification"
with ZipFile(SRC) as z:
    assert z.testzip() is None and len(z.namelist())==41
    main=z.read(MAIN).decode()
    cls=z.read(CLASS).decode()
    article=z.read(ARTICLE).decode()
    css=z.read(CSS).decode()

main=once(main," * Version: 0.1.29"," * Version: 0.1.30","WordPress plugin header")
cls=once(cls,"'0.1.29'","'0.1.30'","Asset cache version")
# Root cause 1: article provider renderer permitted text-only card markup.
# Respect existing validated feed images and verified business images but
# never display a pictureless ad.
a="""        if (method_exists($this, 'multiprovider_runtime_image_url')) {
            $image_url = $this->multiprovider_runtime_image_url($image_url, (string)($banner['network'] ?? ''), absint($banner['campaign_post_id'] ?? 0));
        }
        $title = isset($banner['title']) ? trim(strtr((string) $banner['title'], $replacements)) : '';"""
b="""        if (method_exists($this, 'multiprovider_runtime_image_url')) {
            $image_url = $this->multiprovider_runtime_image_url($image_url, (string)($banner['network'] ?? ''), absint($banner['campaign_post_id'] ?? 0));
        }
        // HD009 0.1.30: the feed provider must supply its *own* approved
        // product photo. Do not degrade the article layout to a text-only
        // offer, generic Hobby Hero, or a picture from another merchant.
        if ($image_url === '') { return ''; }
        $title = isset($banner['title']) ? trim(strtr((string) $banner['title'], $replacements)) : '';"""
article=once(article,a,b,"real provider card image gate")

# Root cause 2: 0.1.29 looked for non-existent generic names but provider
# produces .ppar-article-product-block (verified exact renderer).
# Make the actual provider's block THE article product output; when
# a Hab sidebar exists move the one existing verified block into it.
# This is a pure markup move: no new campaign queries, no new creative.
helper=r'''
    /** Existing eBay/idealo (or other already approved provider) product
     * cards have priority. Never mix an Amazon Media Library fallback into
     * an already-populated product area. Keep the provider's own verified
     * image and link together, without borrowing it for an Amazon offer. */
    private static function provider_article_cards_first($content) {
        if (strpos($content, 'ppar-article-product-block') === false) {
            return null;
        }
        $start = '<section class="ppar-article-product-block"';
        $offset = strpos($content, $start);
        if ($offset === false) { return $content; }
        $end = strpos($content, '</section>', $offset);
        if ($end === false) { return $content; }
        $end += strlen('</section>');
        $block = substr($content, $offset, $end - $offset);
        // The provider's own renderer never creates empty blocks.
        // Defend against outdated admin/placeholder markup in a public post.
        if (strpos($block, 'ppar-article-product-image') === false ||
            strpos($block, 'ppar-article-product-card') === false) {
            return $content;
        }
        $aside = '<aside class="hd-article-sidebar-v150804"';
        if (strpos($content, $aside) === false) { return $content; }
        $content = substr_replace($content, '', $offset, $end - $offset);
        $pos = strpos($content, $aside);
        $after = strpos($content, '>', $pos);
        if ($after === false) { return $content . $block; }
        return substr($content, 0, $after + 1)
           . $block . substr($content, $after + 1);
    }

'''
cls=once(cls,"    public static function render_article_cards($content) {",helper+"    public static function render_article_cards($content) {","Article provider priority helper")
# Provider priority check must not depend on Amazon launch mode: if eBay
# is enabled in a different existing provider mode, its real cards can be
# relocated; then do NOT also show manual Amazon media fallback.
old="""        if (!is_string($content) || !self::launch_active() || is_admin() ||
            is_feed() || !is_singular('post') || !in_the_loop() || !is_main_query()) {
            return $content;
        }
        $id = absint(get_the_ID());"""
new="""        if (!is_string($content) || is_admin() ||
            is_feed() || !is_singular('post') || !in_the_loop() || !is_main_query()) {
            return $content;
        }
        // The provider product area is rendered first by the existing
        // article-plan filter; it retains priority across all partner modes.
        $provider = self::provider_article_cards_first($content);
        if ($provider !== null) { return $provider; }
        if (!self::launch_active()) { return $content; }
        $id = absint(get_the_ID());"""
cls=once(cls,old,new,"Provider-before-Amazon order")
# Keep the current shortcodes/target checks intact, but accept both real
# provider class names in the duplicate protection. They are checked before
# the Amazon fallback code.
old="""        if (strpos($content,'hdar-amazon-article-products') !== false ||
            strpos($content,'ppar-article-products') !== false ||
            strpos($content,'post_bottom_products') !== false) { return $content; }"""
new="""        if (strpos($content,'hdar-amazon-article-products') !== false ||
            strpos($content,'ppar-article-product-block') !== false ||
            strpos($content,'ppar-article-product-grid') !== false ||
            strpos($content,'ppar-article-products') !== false ||
            strpos($content,'post_bottom_products') !== false) { return $content; }"""
cls=once(cls,old,new,"Correct provider markup recognition")

css += r'''

/* 0.1.30 – real feed product cards take precedence over Mediathek
   Amazon fallback. Existing provider picture + provider link stay paired.
   Use the current Hab-inspired right sidebar without changing HD003. */
.hd-article-sidebar-v150804 .ppar-article-product-block {
  box-sizing:border-box!important;max-width:100%!important;
  margin:0!important;padding:15px!important;
  border:1px solid #d7e7e3!important;border-radius:6px!important;
  background:#f7faf8!important;overflow:hidden!important;
}
.hd-article-sidebar-v150804 .ppar-article-product-grid {
  display:grid!important;grid-template-columns:minmax(0,1fr)!important;
  gap:12px!important;max-width:100%!important;
}
.hd-article-sidebar-v150804 .ppar-article-product-card {
  box-sizing:border-box!important;display:block!important;
  min-width:0!important;width:100%!important;
  margin:0!important;padding:0!important;
  border:1px solid #dde7e2!important;border-radius:4px!important;
  overflow:hidden!important;background:white!important;
}
.hd-article-sidebar-v150804 .ppar-article-product-link {
  box-sizing:border-box!important;display:flex!important;
  flex-direction:column!important;gap:10px!important;
  min-width:0!important;width:100%!important;padding:12px!important;
  text-decoration:none!important;
}
.hd-article-sidebar-v150804 .ppar-article-product-media {
  box-sizing:border-box!important;display:block!important;
  width:100%!important;aspect-ratio:4/3!important;
  background:#f5f8f6!important;overflow:hidden!important;
}
.hd-article-sidebar-v150804 .ppar-article-product-image {
  display:block!important;max-width:100%!important;
  width:100%!important;height:100%!important;
  object-fit:contain!important;
}
.hd-article-sidebar-v150804 .ppar-article-product-body {
  display:flex!important;flex-direction:column!important;
  gap:8px!important;max-width:100%!important;
  font-family:Montserrat,'Segoe UI',Arial,sans-serif!important;
  color:#23434a!important;
}
.hd-article-sidebar-v150804 .ppar-article-product-title {
  font-size:14px!important;line-height:1.4!important;
  overflow-wrap:anywhere!important;
}
.hd-article-sidebar-v150804 .ppar-article-product-cta,
.hd-article-sidebar-v150804 .ppar-article-product-offer-button {
  display:block!important;text-decoration:none!important;
  text-align:center!important;font-size:12px!important;
  font-weight:700!important;line-height:1.35!important;
  background:#e7ae62!important;color:#283c3a!important;
  border-radius:4px!important;padding:10px!important;
}
@media(max-width:760px) {
  .hd-article-sidebar-v150804 .ppar-article-product-block{
    padding:12px!important;
  }
}
'''
out=BytesIO()
changes=[]
with ZipFile(SRC) as z,ZipFile(out,'w') as w:
    for item in z.infolist():
        before=z.read(item.filename)
        after=(main.encode() if item.filename==MAIN else cls.encode() if item.filename==CLASS
            else article.encode() if item.filename==ARTICLE else css.encode() if item.filename==CSS
            else before)
        if after!=before:changes.append(item.filename)
        w.writestr(item,after)
    w.comment=z.comment
assert set(changes)=={MAIN,CLASS,ARTICLE,CSS},changes
data=out.getvalue()
with ZipFile(BytesIO(data)) as z:
    assert z.testzip() is None and len(z.namelist())==41
    php=[n for n in z.namelist() if n.endswith('.php')]
    assert len(php)==24
    with TemporaryDirectory() as td:
        for n in php:
            f=Path(td)/n
            f.parent.mkdir(parents=True,exist_ok=True)
            f.write_bytes(z.read(n))
            check=subprocess.run(['php','-l',str(f)],capture_output=True,text=True)
            assert check.returncode==0,(n,check.stderr)
CUR.write_bytes(data)
OUT.write_bytes(data)
assert OUT.read_bytes()==CUR.read_bytes()
print('HD009_030_FULL_BUILD_PASS','bytes',len(data),'sha256',sha256(data).hexdigest(),
      'entries',41,'php',24,'changes',changes)
