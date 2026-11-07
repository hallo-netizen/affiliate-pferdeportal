#!/usr/bin/env python3
"""Only HD009 0.1.25: use dedicated non-hero world photos for flatter category banners.
Keep the exact original Amazon badge, typography, gradient, provider selection and slots.
Register images: preserve approved topic photos and restore an alternate hero crop
for image-less profiles in the pre-existing register footer mount.
"""
from pathlib import Path
from zipfile import ZipFile
from io import BytesIO
from tempfile import TemporaryDirectory
from hashlib import sha256
import subprocess

ROOT=Path("protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/PLUGINS/ISOLIERTE_PLUGINS")
SRC=ROOT/"HD-009-AFFILIATE-ZENTRALE"/"CURRENT.zip"
WORLD_SRC=ROOT/"HD-003-DESIGN-TEMPLATE-KIT"/"CURRENT.zip"
TARGET=SRC.parent/"HOBBY_DEPOT_AFFILIATE_HD009_0.1.25.zip"
EXPECTED="e1bc7cc4d7ab69bc711c424c3d1a612c4710f66155eba7a401552329a800f3a6"
MAIN="affiliate-portal-router/hobby-depot-affiliate-router.php"
CSS="affiliate-portal-router/assets/hdar-amazon-start.css"
CACHE="affiliate-portal-router/includes/class-hdar-amazon-start.php"
WORLDS=("gestalten","fertigen","technik","forschen","pflanzen","tiere","bewegen","sammeln")
WORLDS_CSS=r"""
/* HD009 0.1.25: category-only visual contract.
 * Existing banner button, original Amazon badge and cream-to-photo gradient unchanged.
 * Category/world banners 6:1 on desktop; preserve legibility on narrow screens.
 */
a.hdar-ci-amazon-banner.hdar-ci-amazon-banner-category{
  aspect-ratio:6/1!important;min-height:0!important;
}
a.hdar-ci-amazon-banner-category .hdar-ci-content{top:10%!important;width:63%!important;}
a.hdar-ci-amazon-banner-category .hdar-ci-title{
  font-size:clamp(16px,calc(2.9cqw * var(--hdar-title-scale,1)),38px)!important;
}
a.hdar-ci-amazon-banner-category .hdar-ci-subtitle{
  display:block!important;margin-top:3px!important;
  font-size:clamp(11px,1.15cqw,15px)!important;
  font-weight:600!important;color:#207b82!important;
}
a.hdar-ci-amazon-banner-category .hdar-ci-photo>img{
  object-position:75% 50%!important;
}
a.hdar-ci-amazon-banner-square .hdar-ci-photo>img{
  object-position:66% 42%!important;transform:scale(1.08)!important;
}
@media(max-width:720px){
  a.hdar-ci-amazon-banner.hdar-ci-amazon-banner-category{aspect-ratio:4.2/1!important;}
  a.hdar-ci-amazon-banner-category .hdar-ci-content{top:8%!important;width:64%!important;}
  a.hdar-ci-amazon-banner-category .hdar-ci-title{font-size:clamp(11px,3.1vw,21px)!important;}
  a.hdar-ci-amazon-banner-category .hdar-ci-subtitle{display:none!important;}
  a.hdar-ci-amazon-banner-category .hdar-ci-button{bottom:5%!important;}
}
"""

def once(s,a,b,reason):
    n=s.count(a)
    assert n==1,(reason,"expected 1 got",n,a[:180])
    return s.replace(a,b)

def patch_main(s):
    s=once(s,"* Version: 0.1.24","* Version: 0.1.25","Plugin header")
    mark="""    private function hdar_ci_amazon_banner($context, $slot_type, $content_id, $register_row = null) {"""
    helper="""    // Use the authoritative category/ancestor path already collected by HD009.
    // Never guess a world from unrelated words in the hobby title.
    private function hdar_ci_banner_world($context, $register_row = null) {
        $allowed = array('gestalten','fertigen','technik','forschen',
                         'pflanzen','tiere','bewegen','sammeln');
        if (is_array($register_row)) {
            $w = sanitize_key((string)($register_row['source_identity']['natural_world'] ?? ''));
            if (in_array($w,$allowed,true)) { return $w; }
        }
        foreach ((array)($context['slugs'] ?? array()) as $slug) {
            $slug = sanitize_key((string)$slug);
            if (in_array($slug,$allowed,true)) { return $slug; }
        }
        return '';
    }

"""
    s=once(s,mark,helper+mark,"Insert one reusable world matcher")
    mark="""        $slug = sanitize_title($topic);
        $post_id = absint($context['post_id'] ?? 0);"""
    replacement="""        $slug = sanitize_title($topic);
        $category_banner = $wide && $this->overview_wide_banner_slot($slot)
            && (string)($context['post_type'] ?? '') !== 'hobbyregister_profile';
        $world = $this->hdar_ci_banner_world($context,$register_row);
        $post_id = absint($context['post_id'] ?? 0);"""
    s=once(s,mark,replacement,"Category/wide route")
    mark="""        // Square register ad is intentionally text-only: no triple use of hero
        // image. Article fallback is text-only too. A wide register ad may
        // reuse the one approved motif; no wrong/guessed image is introduced.
        $use_photo = $photo !== '' && !$square &&
            (string)($context['post_type'] ?? '') !== 'post';"""
    replacement="""        // Category banners always use a separate *world* photo, never their
        // own hero/master picture. These eight self-contained photos are
        // reproduced from the existing approved HD003 collection, not guessed.
        if ($category_banner && $world !== '') {
            $world_file = 'assets/hdar-world-' . $world . '.webp';
            if (is_file(plugin_dir_path(__FILE__) . $world_file)) {
                $photo = plugins_url($world_file,__FILE__);
            }
        }
        // Register square: use the approved topic photo with a different crop.
        // Without a photograph, the pre-existing footer mount reads the real
        // HD007 hero photo and sets it on both ad shapes.
        $use_photo = $photo !== '' &&
            (string)($context['post_type'] ?? '') !== 'post';"""
    s=once(s,mark,replacement,"Image source fallback")
    mark="""        $size = $square ? 'square' : 'wide';
        $mode_class = $use_photo ? '' : ' hdar-ci-amazon-banner-text';"""
    repl="""        $size = $square ? 'square' : 'wide';
        $category_class = $category_banner ? ' hdar-ci-amazon-banner-category' : '';
        $mode_class = $use_photo ? '' : ' hdar-ci-amazon-banner-text';"""
    s=once(s,mark,repl,"Category class")
    mark="""        $text_markup = $use_photo ? '' :
            '<span class="hdar-ci-subtitle">Passende Ausrüstung entdecken</span>';"""
    repl="""        $text_markup = $category_banner
            ? '<span class="hdar-ci-subtitle">Ausrüstung und Zubehör entdecken</span>'
            : ($use_photo ? '' :
                '<span class="hdar-ci-subtitle">Passende Ausrüstung entdecken</span>');"""
    s=once(s,mark,repl,"Category subheading")
    mark="""            .'<a class="hdar-ci-amazon-banner hdar-ci-amazon-banner-'.$size.$mode_class.'" href="'.esc_url($url).'"""
    repl="""            .'<a class="hdar-ci-amazon-banner hdar-ci-amazon-banner-'.$size.$category_class.$mode_class.'" href="'.esc_url($url).'"""
    s=once(s,mark,repl,"Visual class")
    mark="""            .'var root=document.querySelector("[data-hd-register-profile] .hdr-profile-grid");if(!root)return;'
            .'var aside=root.querySelector("aside"),article=root.querySelector("main .hdr-article");'"""
    repl="""            .'var root=document.querySelector("[data-hd-register-profile] .hdr-profile-grid");if(!root)return;'
            .'var aside=root.querySelector("aside"),article=root.querySelector("main .hdr-article");'
            .'var hero=root.closest("[data-hd-register-profile]").querySelector(".hdr-hero.is-profile figure img");'
            .'if(hero){["hdar-ci-register-side-'.$slug.'","hdar-ci-register-inline-'.$slug.'"].forEach(function(id){'
            .'var wrap=document.getElementById(id),banner=wrap?wrap.querySelector(".hdar-ci-amazon-banner"):null;'
            .'var photo=wrap?wrap.querySelector(".hdar-ci-photo"):null;'
            .'if(!banner||!photo||photo.querySelector("img:not(.hdar-ci-amazon-official)"))return;'
            .'var img=document.createElement("img");img.src=hero.currentSrc||hero.src;img.alt=hero.alt||"";'
            .'img.loading="lazy";img.decoding="async";photo.insertBefore(img,photo.firstChild);'
            .'banner.classList.remove("hdar-ci-amazon-banner-text");'
            .'var sub=banner.querySelector(".hdar-ci-subtitle");if(sub)sub.remove();'
            .'});}'"""
    s=once(s,mark,repl,"Register actual hero fallback")
    return s

assert sha256(SRC.read_bytes()).hexdigest()==EXPECTED,"Current HD009 changed since audit"
output=BytesIO();changed=[]
with ZipFile(SRC) as inp,ZipFile(WORLD_SRC) as hd003,ZipFile(output,"w") as new:
    assert inp.testzip() is None
    assert hd003.testzip() is None
    for entry in inp.infolist():
        before=inp.read(entry.filename)
        after=before
        if entry.filename==MAIN:after=patch_main(before.decode()).encode()
        if entry.filename==CACHE:after=once(before.decode(),"'0.1.24'","'0.1.25'","CSS cache").encode()
        if entry.filename==CSS:
            css=before.decode()
            assert "HD009 0.1.25" not in css
            after=(css+WORLDS_CSS).encode()
        new.writestr(entry,after)
        if after!=before:changed.append(entry.filename)
    for world in WORLDS:
        if world=="tiere":
            # Existing terrarium photo: no dog/cat/horses.
            source="affiliate-portal-template-kit/assets/hobby-depot-v150617/hero-masters-v150684/terraristik.webp"
        else:
            source=f"affiliate-portal-template-kit/assets/hobby-depot-v150617/start-world-v150691/{world}.webp"
        assert source in hd003.namelist(),source
        data=hd003.read(source)
        assert len(data)>10000,(world,len(data))
        name=f"affiliate-portal-router/assets/hdar-world-{world}.webp"
        assert name not in inp.namelist(),name
        new.writestr(name,data)
        print("WORLD_PHOTO",world,"bytes",len(data),"source",source,"sha256",sha256(data).hexdigest())
    new.comment=inp.comment
assert set(changed)=={MAIN,CSS,CACHE},changed
payload=output.getvalue()
with ZipFile(BytesIO(payload)) as z:
    assert len(z.namelist())==41
    assert z.testzip() is None
    with TemporaryDirectory() as tmp:
        phps=[n for n in z.namelist() if n.endswith(".php")]
        assert len(phps)==24
        for name in phps:
            file=Path(tmp)/name;file.parent.mkdir(parents=True,exist_ok=True);file.write_bytes(z.read(name))
            result=subprocess.run(["php","-l",str(file)],capture_output=True,text=True)
            assert result.returncode==0,(name,result.stderr)
    source=z.read(MAIN).decode()
    assert "* Version: 0.1.25" in source.split("*/",1)[0]
    assert source.count("hdar_ci_banner_world(")==2
    assert "hdar-ci-amazon-banner-category" in source
    css=z.read(CSS).decode()
    assert "aspect-ratio:6/1!important;" in css
    assert "aspect-ratio:4.2/1!important;" in css
SRC.write_bytes(payload)
TARGET.write_bytes(payload)
assert SRC.read_bytes()==TARGET.read_bytes()
print("FULL_ZIP_PASS",TARGET,len(payload),sha256(payload).hexdigest(),"PHP",len(phps),"files",41)
