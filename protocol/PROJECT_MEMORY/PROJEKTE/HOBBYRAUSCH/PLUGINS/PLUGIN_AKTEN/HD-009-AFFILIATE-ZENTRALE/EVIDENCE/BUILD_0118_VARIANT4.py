#!/usr/bin/env python3
"""KISS: HD009 0.1.18; current existing affiliate banner slots, variant 4 square layout, fixed parent flex height."""
from pathlib import Path
import hashlib,io,subprocess,tempfile,urllib.request,zipfile
ROOT=Path("protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH")
Z=ROOT/"PLUGINS/ISOLIERTE_PLUGINS/HD-009-AFFILIATE-ZENTRALE/CURRENT.zip"
PHP="affiliate-portal-router/hobby-depot-affiliate-router.php"
CSS="affiliate-portal-router/assets/hdar-amazon-start.css"
README="affiliate-portal-router/readme.txt"
BADGE="affiliate-portal-router/assets/hdar-amazon-available-at-amazon-de-official.png"
with zipfile.ZipFile(Z) as z:
    assert z.testzip() is None
    files={i.filename:z.read(i.filename) for i in z.infolist() if not i.is_dir()}
assert PHP in files and CSS in files and README in files
s=files[PHP].decode("utf-8")
assert s.count("Version: 0.1.17-dev")==1
assert "hdar_approved_rental_banner_fallback" not in s
s=s.replace("Version: 0.1.17-dev","Version: 0.1.18-dev",1)
m0=s.index("    private function hdar_ci_amazon_banner(")
m1=s.index("    /** HD007 owns",m0)
before,body,after=s[:m0],s[m0:m1],s[m1:]
assert body.count("        $logo_file = plugin_dir_path(__FILE__).'assets/hdar-ci-logo-original.png';")==1
body=body.replace(
"        $logo_file = plugin_dir_path(__FILE__).'assets/hdar-ci-logo-original.png';\n        if (!is_file($logo_file)) { return ''; }",
"        // Use only the exact original German Amazon-approved advertising lockup.\n        $official_badge = plugin_dir_path(__FILE__).'assets/hdar-amazon-available-at-amazon-de-official.png';\n        if (!is_file($official_badge)) { return ''; }",
1)
assert "$topic = trim(sanitize_text_field" in body
token="        if ($topic === '' || in_array("
assert body.count(token)==1
body=body.replace(token,
"        // Real page titles such as Malen & Zeichnen may arrive HTML entity-encoded.\n"
"        $topic = html_entity_decode($topic, ENT_QUOTES | ENT_HTML5, 'UTF-8');\n"
+token,1)
start=body.index("        $html='<div class=\"ppar-affiliate-slot hdar-ci-amazon-slot")
end=body.index("        $shown[$key] = true;",start)
old_markup=body[start:end]
assert 'hdar-ci-logo-original.png' in old_markup
assert "Entdecke deine Ausrüstung" in old_markup
markup="""        $html='<div class="ppar-affiliate-slot hdar-ci-amazon-slot hdar-ci-amazon-slot-'.$size.'" data-ppar-slot="'.esc_attr($slot).'">'
            .'<span class="hdar-ci-label">Anzeige</span>'
            .'<a class="hdar-ci-amazon-banner hdar-ci-amazon-banner-'.$size.'" href="'.esc_url($url).'" rel="sponsored nofollow noopener noreferrer" target="_blank" aria-label="'.esc_attr($topic.' – Zubehör bei Amazon entdecken').'">'
            .'<span class="hdar-ci-content"><strong class="hdar-ci-title">'.esc_html($topic).'</strong></span>'
            .'<span class="hdar-ci-photo"><img src="'.esc_url($photo).'" alt="'.esc_attr($topic).'" loading="lazy" decoding="async">'
            .'<span class="hdar-ci-button">'
            .'<img class="hdar-ci-amazon-official" src="'.esc_url(plugins_url('assets/hdar-amazon-available-at-amazon-de-official.png',__FILE__)).'" alt="Erhältlich bei Amazon" loading="lazy" decoding="async">'
            .'<span class="hdar-ci-amazon-arrow" aria-hidden="true">→</span></span>'
            .'</span></a></div>';
"""
body=body[:start]+markup+body[end:]
assert "Entdecke deine Ausrüstung" not in body
assert "hdar-ci-logo-original.png" not in body
assert "hdar-ci-amazon-official" in body
s=before+body+after
files[PHP]=s.encode("utf-8")
# The house logo is neither rendered nor required in the Amazon creative.
files.pop("affiliate-portal-router/assets/hdar-ci-logo-original.png",None)
# Only Amazon-provided, unmodified "Erhältlich bei Amazon" German brand asset.
url="https://m.media-amazon.com/images/G/01/AdProductsWebsite/images/ad-specs/available_at_amazon___de_3f5c5e60.zip"
with urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0"}),timeout=35) as r:official_zip=r.read()
name="DE/Screen/Horizontal/Squid Ink/AvailableAt_Amazon_DE_HorizontalLogo_Rgb_SquidInk.png"
with zipfile.ZipFile(io.BytesIO(official_zip)) as logo_zip:
    assert name in logo_zip.namelist(),"Official DE artwork not found"
    logo_png=logo_zip.read(name)
assert hashlib.sha256(logo_png).hexdigest()=="fb6db85f898078fa6df03740b58d65f431b8a6186c97f6b8a72e95f11b9ab8e5","Original Amazon brand image changed"
files[BADGE]=logo_png
STYLE=r"""
/* HD009 0.1.18 – variant 4, existing provider routing, one creative.
   The original site logo was deliberately omitted. One title, one photo, one authorized German Amazon badge.
   Aspect ratios and container sizes depend only on the available slot width. */
.ppar-affiliate-slot.hdar-ci-amazon-slot{
  display:block!important;box-sizing:border-box!important;width:100%!important;
  height:auto!important;max-height:none!important;min-height:0!important;overflow:visible!important;
  margin:0!important;padding:0!important;border:0!important;background:transparent!important;
}
a.hdar-ci-amazon-banner{
  box-sizing:border-box!important;display:grid!important;grid-template-columns:minmax(0,1fr)!important;
  grid-template-rows:auto minmax(0,1fr)!important;width:100%!important;height:auto!important;
  max-height:none!important;min-height:0!important;padding:0!important;gap:0!important;
  border:1px solid #e8dfd2!important;border-radius:9px!important;
  background:#f6efe5!important;overflow:hidden!important;
  container-type:inline-size;cursor:pointer;text-decoration:none!important;
}
a.hdar-ci-amazon-banner .hdar-ci-content{
  display:flex!important;box-sizing:border-box!important;grid-row:1!important;
  position:relative!important;align-items:center!important;justify-content:flex-start!important;
  background:linear-gradient(180deg,#fff9f1 0%,#efe5d8 100%)!important;
  width:100%!important;height:auto!important;min-height:0!important;max-height:none!important;
  padding:clamp(7px,2.5cqw,17px) clamp(9px,3cqw,22px)!important;gap:0!important;
  text-align:left!important;flex-direction:row!important;
}
a.hdar-ci-amazon-banner .hdar-ci-title{
  display:block!important;color:#17313c!important;font-family:Montserrat,Arial,sans-serif!important;
  font-weight:800!important;letter-spacing:-.022em!important;line-height:1.12!important;
  margin:0!important;padding:0!important;overflow-wrap:break-word!important;
}
a.hdar-ci-amazon-banner .hdar-ci-photo{
  box-sizing:border-box!important;display:block!important;grid-row:2!important;
  position:relative!important;width:100%!important;min-width:0!important;
  height:100%!important;max-height:none!important;min-height:0!important;flex:none!important;
  overflow:hidden!important;
}
a.hdar-ci-amazon-banner .hdar-ci-photo>img{
  display:block!important;position:absolute!important;inset:0!important;width:100%!important;
  height:100%!important;min-height:0!important;max-height:none!important;
  max-width:none!important;object-fit:cover!important;object-position:50% 48%!important;
  border:none!important;
}
a.hdar-ci-amazon-banner .hdar-ci-photo::after{
  content:"";pointer-events:none;position:absolute;z-index:1;left:0;right:0;bottom:0;height:32%;
  background:linear-gradient(0deg,rgba(0,0,0,.32),transparent);
}
a.hdar-ci-amazon-banner .hdar-ci-button{
  display:flex!important;position:absolute!important;z-index:3!important;box-sizing:border-box!important;
  align-items:center!important;justify-content:center!important;gap:clamp(4px,1.5cqw,12px)!important;
  left:50%!important;bottom:clamp(7px,3.5cqw,23px)!important;transform:translateX(-50%)!important;
  width:max-content!important;max-width:calc(100% - 8px)!important;min-width:0!important;
  min-height:0!important;height:auto!important;padding:clamp(5px,1.2cqw,10px) clamp(7px,2cqw,22px)!important;
  background:#ffbe38!important;border:1px solid rgba(97,56,4,.14)!important;
  border-radius:999px!important;color:#101820!important;
  box-shadow:0 4px 18px rgba(0,0,0,.20)!important;text-decoration:none!important;
  white-space:nowrap!important;
}
a.hdar-ci-amazon-banner .hdar-ci-amazon-official{
  display:block!important;position:static!important;object-fit:contain!important;
  width:clamp(140px,27cqw,215px)!important;max-width:min(215px,calc(100% - 24px))!important;
  height:auto!important;min-height:0!important;max-height:42px!important;flex:0 1 auto!important;
  background:transparent!important;
}
a.hdar-ci-amazon-banner .hdar-ci-amazon-arrow{
  font-family:Arial,sans-serif;font-weight:700;font-size:clamp(17px,3cqw,30px);
  line-height:1;color:#152c31;flex:none;margin-left:clamp(2px,.7cqw,7px);
}
a.hdar-ci-amazon-banner:hover .hdar-ci-button,
a.hdar-ci-amazon-banner:focus-visible .hdar-ci-button{background:#ffce60!important;}
a.hdar-ci-amazon-banner-square{
  aspect-ratio:1/1!important;max-width:100%!important;
}
a.hdar-ci-amazon-banner-square .hdar-ci-title{font-size:clamp(13px,5.4cqw,25px)!important;}
a.hdar-ci-amazon-banner-wide{
  aspect-ratio:4.2/1!important;max-width:100%!important;
}
a.hdar-ci-amazon-banner-wide .hdar-ci-content{
  padding:clamp(8px,1.8cqw,17px) clamp(12px,2.7cqw,23px)!important;
}
a.hdar-ci-amazon-banner-wide .hdar-ci-title{font-size:clamp(17px,3.5cqw,29px)!important;}
a.hdar-ci-amazon-banner-wide .hdar-ci-button{
  left:auto!important;right:clamp(7px,3cqw,28px)!important;transform:none!important;
}
/* Existing HD003 container forces 76px on the entire slot AND each image on phones.
   This is the demonstrated reason the original 0.1.17 wide creative was cut to a stripe.
   Correct that existing slot only when our own Amazon creative is its child. */
body .hd-next-partner-banner:has(.hdar-ci-amazon-slot),
body .hd-next-partner-banner:has(.hdar-ci-amazon-slot)>div,
body .hd-next-partner-banner:has(.hdar-ci-amazon-slot)>div>.ppar-affiliate-slot,
body .hd-next-partner-banner:has(.hdar-ci-amazon-slot) .ppar-affiliate-content,
body .hd-next-partner-banner:has(.hdar-ci-amazon-slot) .ppar-banner-link{
  height:auto!important;min-height:0!important;max-height:none!important;
  overflow:visible!important;aspect-ratio:auto!important;box-sizing:border-box!important;
}
body .hd-next-partner-banner:has(.hdar-ci-amazon-slot)>span{
  top:6px!important;right:8px!important;left:auto!important;z-index:8!important;
}
/* Only one advertising label: the original HD003 parent already says "Anzeige · Partner". */
body .hd-next-partner-banner:has(.hdar-ci-amazon-slot) .hdar-ci-label{display:none!important}
body .hd-next-partner-banner:has(.hdar-ci-amazon-slot) .hdar-ci-photo>img{
  height:100%!important;min-height:0!important;max-height:none!important;width:100%!important;
}
body .hd-next-partner-banner:has(.hdar-ci-amazon-slot) .hdar-ci-amazon-official{
  height:auto!important;min-height:0!important;max-height:42px!important;
}
/* All other banner and partner placements keep the old engine and existing format contracts. */
@media(max-width:640px){
  a.hdar-ci-amazon-banner-wide{aspect-ratio:3.15/1!important;min-height:0!important;}
  a.hdar-ci-amazon-banner-wide .hdar-ci-title{font-size:clamp(14px,4.7cqw,23px)!important;}
}
"""
files[CSS]+=("\n"+STYLE).encode("utf-8")
readme=files[README].decode("utf8")
assert readme.count("Stable tag: 0.1.17-dev")==1
files[README]=(readme.replace("Stable tag: 0.1.17-dev","Stable tag: 0.1.18-dev",1)+
"\n== 0.1.18-dev ==\nBanner 4: Hobby-Depot-Logo und doppelte Produkt-Slogans entfernt. Header nur Hobbythema im warmen Farbverlauf, grosseres passendes Hobbyfoto, orange-gelber CTA ueber dem Foto mit originalem, von Amazon freigegebenem deutschen 'Erhaeltlich bei Amazon'-Logo und Pfeil. Kein nicht genehmigtes normales Amazon-Logo. Responsive 1:1 fuer Register/Glossar, breite Form in nativen Seitenslots. Am durch echte HTML-Pruefung belegten HD003-Platz wird die alte starre 76px-Hoehe fuer unser Werbemittel aufgehoben. Kein neuer Import/Partner/Slot. Tracking-Code und Themenzuordnung bleiben unveraendert.\n").encode("utf8")
assert all(n in files for n in (PHP,README,CSS,BADGE))
with tempfile.TemporaryDirectory() as tmp:
    php_files=[n for n in files if n.endswith(".php")]
    for name in php_files:
        p=Path(tmp)/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(files[name])
        c=subprocess.run(["php","-l",str(p)],capture_output=True,text=True)
        assert c.returncode==0,(name,c.stdout,c.stderr)
tmp=Z.with_suffix(".next.zip")
with zipfile.ZipFile(tmp,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=6) as out:
    for name,b in sorted(files.items()):out.writestr(name,b)
with zipfile.ZipFile(tmp) as z:
    assert z.testzip() is None and set(z.namelist())==set(files)
    assert z.read(BADGE)==logo_png and "hdar-ci-logo-original.png" not in z.namelist()
tmp.replace(Z)
sha=hashlib.sha256(Z.read_bytes()).hexdigest()
report=ROOT/"PLUGINS/PLUGIN_AKTEN/HD-009-AFFILIATE-ZENTRALE/EVIDENCE/HD009_0118_CI_REPORT.txt"
report.write_text("HD009 0.1.18-dev – KISS variant 4\n"
+"ZIP bytes: "+str(Z.stat().st_size)+"\nSHA256: "+sha+"\n"
+f"PHP syntax: {len(php_files)}/{len(php_files)} PASS\nZIP CRC: PASS\n"
+"Original Amazon DE approved 'Erhaeltlich bei Amazon' PNG exact SHA256: fb6db85f898078fa6df03740b58d65f431b8a6186c97f6b8a72e95f11b9ab8e5\n"
+"Normal Amazon logo was NOT used because the trademark policy does not allow it in affiliate ads.\n"
+"Body: no Hobby Depot logo, no 'Entdecke deine Ausruestung', title bar + large photo + orange CTA with original approved badge and arrow.\n"
+"HTML direct audit: existing HD003 .hd-next-partner-banner and forced 76px height; CSS scoped override only when hdar-ci-amazon-slot present.\n"
+"The original provider, category, glossary and register logic remains in the existing plugin.\n"
+"WordPress live installation still NOT checked.\n")
print("PASS 0.1.18 ZIP",Z.stat().st_size,sha,"PHP",len(php_files),"original Amazon-DE logo validated")
