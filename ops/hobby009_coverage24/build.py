#!/usr/bin/env python3
"""HD009: one native fallback, existing WP/HD003 slot contracts, no second engine."""
from pathlib import Path
from zipfile import ZipFile
from io import BytesIO
from tempfile import TemporaryDirectory
from hashlib import sha256
import subprocess

ROOT=Path("protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/PLUGINS/ISOLIERTE_PLUGINS/HD-009-AFFILIATE-ZENTRALE")
ZIP=ROOT/"CURRENT.zip"
BASE_SHA="9e533d1f47b03c41078baf9260887e4945591244c75fd386a759ab1f9fb11ff1"
MAIN="affiliate-portal-router/hobby-depot-affiliate-router.php"
CSS="affiliate-portal-router/assets/hdar-amazon-start.css"
CACHE="affiliate-portal-router/includes/class-hdar-amazon-start.php"
NAME="HOBBY_DEPOT_AFFILIATE_HD009_0.1.24.zip"

STYLE=r"""
/* HD009 0.1.24: brand-only alternative when a second hobby photo repeats
   the hero, or no approved image exists. Provider selection is unchanged. */
a.hdar-ci-amazon-banner.hdar-ci-amazon-banner-text{
  border:1px solid rgba(23,49,60,.1)!important;background:#f5f1e9!important;
}
a.hdar-ci-amazon-banner-text .hdar-ci-photo{
  background:linear-gradient(118deg,#f5f1e9 0%,#e7eeea 55%,#c9ddd8 100%)!important;
}
a.hdar-ci-amazon-banner-text .hdar-ci-photo::after{
  background:linear-gradient(90deg,rgba(245,241,233,.58),rgba(245,241,233,0))!important;
}
a.hdar-ci-amazon-banner-text.hdar-ci-amazon-banner-square .hdar-ci-content{
  top:9%!important;padding:0 7%!important;
}
a.hdar-ci-amazon-banner-text.hdar-ci-amazon-banner-square .hdar-ci-title{
  font-size:clamp(17px,calc(8.5cqw * var(--hdar-title-scale,1)),33px)!important;
}
a.hdar-ci-amazon-banner-text .hdar-ci-subtitle{
  display:block!important;color:#207b82!important;font-family:Montserrat,Arial,sans-serif!important;
  font-weight:600!important;letter-spacing:.01em!important;
  font-size:clamp(11px,3.2cqw,16px)!important;line-height:1.25!important;
  margin-top:12px!important;
}
a.hdar-ci-amazon-banner-text.hdar-ci-amazon-banner-wide .hdar-ci-subtitle{
  margin-top:2px!important;font-size:clamp(10px,1.3cqw,15px)!important;
}
@container (max-width:600px){
 a.hdar-ci-amazon-banner-text.hdar-ci-amazon-banner-wide .hdar-ci-subtitle{display:none!important;}
}
"""

def replace1(s,a,b,reason):
    n=s.count(a)
    if n!=1: raise AssertionError((reason,"Expected once, got",n,a[:110]))
    return s.replace(a,b)

def patch_main(s):
    s=replace1(s," * Version: 0.1.23"," * Version: 0.1.24","version")
    before="""        $post_id = get_the_ID();
        if (!$post_id) {
            return '';
        }

        return $this->render_affiliate_slot($post_id, sanitize_key($atts['type']), sanitize_key($atts['intent']), sanitize_key($atts['group']));
    }"""
    after="""        $slot_type = sanitize_key($atts['type']);
        $intent = sanitize_key($atts['intent']);
        $group = sanitize_key($atts['group']);
        // HD003 leaf category uses a real WP_Term, not a WordPress page.
        // Keep the taxonomy context even when there is no global post in the loop.
        if (function_exists('is_category') && is_category()) {
            $term = function_exists('get_queried_object') ? get_queried_object() : null;
            if ($term instanceof WP_Term && (string) $term->taxonomy === 'category' && !is_wp_error($term)) {
                return $this->render_affiliate_slot_for_context(
                    'term_' . absint($term->term_id),
                    $this->get_category_archive_context($term),
                    $slot_type, $intent, $group
                );
            }
        }
        $post_id = get_the_ID();
        if (!$post_id) { return ''; }
        return $this->render_affiliate_slot($post_id, $slot_type, $intent, $group);
    }"""
    s=replace1(s,before,after,"taxonomy native shortcode")
    before="""        $content = $this->auto_inject_template_affiliate_slots($content);
        if ($this->article_hybrid_enabled()) {
            return $this->auto_inject_article_hybrid($content);
        }
        $content = $this->auto_inject_affiliate_slots($content);
        return $content;
    }"""
    after="""        $content = $this->auto_inject_template_affiliate_slots($content);
        if ($this->article_hybrid_enabled()) {
            $content = $this->auto_inject_article_hybrid($content);
        } else {
            $content = $this->auto_inject_affiliate_slots($content);
        }
        // Existing article/partner placements remain authoritative. Fill only
        // a truly empty published post; no campaign, plan, or template rebuild.
        return $this->hdar_ci_article_empty_banner($content);
    }

    private function hdar_ci_article_empty_banner($content) {
        if (!HDAR_Amazon_Start::launch_active() || !$this->is_enabled() ||
            !function_exists('is_singular') || !is_singular('post') ||
            !in_the_loop() || !is_main_query() || is_admin() || is_feed() || is_preview()) {
            return $content;
        }
        $post_id = absint(get_the_ID());
        if (!$post_id || post_password_required($post_id)) { return $content; }
        $raw = (string)get_post_field('post_content',$post_id);
        if (has_shortcode($raw,'pp_affiliate_slot') ||
            has_shortcode($raw,'affiliate_portal_slot') ||
            has_shortcode($raw,'affiliate_rechner')) { return $content; }
        if (strpos((string)$content,'ppar-affiliate-slot') !== false ||
            strpos((string)$content,'hdar-amazon-product') !== false) {
            return $content;
        }
        $banner = $this->render_affiliate_slot($post_id,'post_inline_banner','portal_context','');
        if (strpos((string)$banner,'ppar-affiliate-slot') === false) { return $content; }
        $paragraphs = substr_count(strtolower((string)$content),'</p>');
        if ($paragraphs < 1) { return $content."\\n".$banner; }
        return $this->insert_after_paragraph((string)$content,$banner,min(2,$paragraphs));
    }"""
    s=replace1(s,before,after,"article fallback after existing insertion")
    before="""        if ($topic === '' || in_array(strtolower($topic), array('hobbyregister','glossar','hobby depot','hobbys'), true)) { return ''; }"""
    after="""        if ($slot === 'start_after_topics' &&
            ($topic === '' || in_array(strtolower($topic),array('hobby depot','hobbys'),true))) {
            $topic = 'Hobby-Ausrüstung';
        }
        if ($topic === '' || in_array(strtolower($topic), array('hobbyregister','glossar','hobby depot','hobbys'), true)) { return ''; }"""
    s=replace1(s,before,after,"home landing search topic")
    before="""        if ($photo === '') { return ''; } // No matching photograph = no invented banner.
        $scheme = strtolower((string)wp_parse_url($photo,PHP_URL_SCHEME));
        if (!in_array($scheme,array('http','https'),true)) { return ''; }"""
    after="""        // Square register ad is intentionally text-only: no triple use of hero
        // image. Article fallback is text-only too. A wide register ad may
        // reuse the one approved motif; no wrong/guessed image is introduced.
        $use_photo = $photo !== '' && !$square &&
            (string)($context['post_type'] ?? '') !== 'post';
        if ($use_photo) {
            $scheme = strtolower((string)wp_parse_url($photo,PHP_URL_SCHEME));
            if (!in_array($scheme,array('http','https'),true)) { $use_photo = false; }
        }"""
    s=replace1(s,before,after,"text-only when image duplicate/missing")
    before="""        $size = $square ? 'square' : 'wide';
        // The same self-contained banner scales to each slot."""
    after="""        $size = $square ? 'square' : 'wide';
        $mode_class = $use_photo ? '' : ' hdar-ci-amazon-banner-text';
        $photo_markup = $use_photo
            ? '<img src="'.esc_url($photo).'" alt="'.esc_attr($topic).'" loading="lazy" decoding="async">'
            : '';
        $text_markup = $use_photo ? '' :
            '<span class="hdar-ci-subtitle">Passende Ausrüstung entdecken</span>';
        // The same self-contained banner scales to each slot."""
    s=replace1(s,before,after,"class and asset html")
    before="""            .'<a class="hdar-ci-amazon-banner hdar-ci-amazon-banner-'.$size.'" href="'.esc_url($url).'" rel="sponsored nofollow noopener noreferrer" target="_blank" aria-label="'.esc_attr($topic.' – Zubehör bei Amazon entdecken').'">'
            .'<span class="hdar-ci-content"><strong class="hdar-ci-title'.$title_class.'" style="'.esc_attr($title_style).'">'.esc_html($topic).'</strong></span>'
            .'<span class="hdar-ci-photo"><img src="'.esc_url($photo).'" alt="'.esc_attr($topic).'" loading="lazy" decoding="async">'"""
    after="""            .'<a class="hdar-ci-amazon-banner hdar-ci-amazon-banner-'.$size.$mode_class.'" href="'.esc_url($url).'" rel="sponsored nofollow noopener noreferrer" target="_blank" aria-label="'.esc_attr($topic.' – Zubehör bei Amazon entdecken').'">'
            .'<span class="hdar-ci-content"><strong class="hdar-ci-title'.$title_class.'" style="'.esc_attr($title_style).'">'.esc_html($topic).'</strong>'.$text_markup.'</span>'
            .'<span class="hdar-ci-photo">'.$photo_markup"""
    s=replace1(s,before,after,"render text-only variant")
    return s

old=ZIP.read_bytes()
assert sha256(old).hexdigest()==BASE_SHA,(sha256(old).hexdigest(),"Wrong/current ZIP changed")
output=BytesIO();changed=[]
with ZipFile(BytesIO(old)) as z,ZipFile(output,'w') as new:
    assert z.testzip() is None and len(z.namelist())==33
    for info in z.infolist():
        data=z.read(info.filename);patched=data
        if info.filename==MAIN:patched=patch_main(data.decode("utf8")).encode("utf8")
        elif info.filename==CSS:
            s=data.decode("utf8")
            assert "HD009 0.1.24" not in s
            patched=(s+STYLE).encode("utf8")
        elif info.filename==CACHE:
            s=data.decode("utf8")
            patched=replace1(s,"'0.1.23'","'0.1.24'","CSS version").encode("utf8")
        if patched!=data:changed.append(info.filename)
        new.writestr(info,patched)
    new.comment=z.comment
assert set(changed)=={MAIN,CSS,CACHE},changed
payload=output.getvalue()
with ZipFile(BytesIO(payload)) as z:
    assert z.testzip() is None and len(z.namelist())==33
    with TemporaryDirectory() as td:
        php=[x for x in z.namelist() if x.endswith(".php")]
        assert len(php)==24
        for name in php:
            p=Path(td)/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(z.read(name))
            c=subprocess.run(["php","-l",str(p)],capture_output=True,text=True)
            assert c.returncode==0,(name,c.stderr)
        print("PHP_SYNTAX_PASS",len(php))
    main=z.read(MAIN).decode()
    assert "HD009 0.1.24" in z.read(CSS).decode()
    assert "hdar_ci_article_empty_banner" in main
    assert "get_category_archive_context($term)" in main
    assert "hdar-ci-amazon-banner-text" in main
    assert "* Version: 0.1.24" in main.split("*/",1)[0]
ZIP.write_bytes(payload)
named=ROOT/NAME;named.write_bytes(payload)
assert ZIP.read_bytes()==named.read_bytes()
print("HD009_COVERAGE_BUILD_PASS","version","0.1.24","length",len(payload),"sha256",sha256(payload).hexdigest(),"changed",changed,"name",NAME)
