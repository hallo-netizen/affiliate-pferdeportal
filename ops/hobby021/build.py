#!/usr/bin/env python3
"""Rebuild only the two existing Hobby Depot plugins from exact byte-verified CURRENT ZIPs."""
from pathlib import Path
from io import BytesIO
from zipfile import ZipFile
from hashlib import sha256
import re, subprocess, tempfile

ROOT=Path("protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/PLUGINS/ISOLIERTE_PLUGINS")
HD009=ROOT/"HD-009-AFFILIATE-ZENTRALE"/"CURRENT.zip"
HD007=ROOT/"HD-007-HOBBYREGISTER-CORE"/"CURRENT.zip"
ORIGINAL={
  HD009: "cd6cb75f3ef0f393f94f3f93b974f3663ffa1f449c579886ae9520bc3d920cbb",
  HD007: "433a642aac02439c74b85653c49c9c8ac62e6de5ea82be42ce58ce53537e8488",
}
AD_MAIN="affiliate-portal-router/hobby-depot-affiliate-router.php"
AD_CSS="affiliate-portal-router/assets/hdar-amazon-start.css"
REG_MAIN="hd-hobbyregister-core/hobby-depot-hobbyregister-core.php"
REG_FRONT="hd-hobbyregister-core/includes/class-hd-hobbyregister-frontend.php"

BANNER_CSS=r"""
/* HD009 0.1.21: native full-bleed hero look from HD007.
   One photo, same cream background as the real Hobbyregister hero.
   No separate assignment logic, imports, new creatives or fonts. */
a.hdar-ci-amazon-banner{
  display:block!important;position:relative!important;isolation:isolate!important;
  border:0!important;border-radius:2px!important;box-shadow:none!important;
  background:#f5f1e9!important;overflow:hidden!important;container-type:inline-size!important;
}
a.hdar-ci-amazon-banner-square{aspect-ratio:1/1!important;min-height:0!important;}
a.hdar-ci-amazon-banner-wide{aspect-ratio:3/1!important;min-height:0!important;}
a.hdar-ci-amazon-banner .hdar-ci-photo{
  display:block!important;position:absolute!important;inset:0!important;grid-row:auto!important;
  box-sizing:border-box!important;width:100%!important;height:100%!important;
  max-height:none!important;min-height:0!important;overflow:hidden!important;background:#f5f1e9!important;
}
a.hdar-ci-amazon-banner .hdar-ci-photo>img{
  display:block!important;position:absolute!important;inset:0!important;
  width:100%!important;height:100%!important;max-width:none!important;max-height:none!important;
  object-fit:cover!important;object-position:center center!important;transform:none!important;
}
a.hdar-ci-amazon-banner .hdar-ci-photo::after{
  content:"";position:absolute!important;inset:0!important;z-index:1!important;
  pointer-events:none!important;width:100%!important;height:100%!important;
  background:linear-gradient(180deg,rgba(245,241,233,.98) 0%,rgba(245,241,233,.85) 17%,rgba(245,241,233,.38) 35%,rgba(245,241,233,0) 59%,rgba(23,49,60,.16) 100%)!important;
}
a.hdar-ci-amazon-banner-wide .hdar-ci-photo::after{
  background:linear-gradient(90deg,#f5f1e9 0%,rgba(245,241,233,.98) 12%,rgba(245,241,233,.87) 28%,rgba(245,241,233,.57) 43%,rgba(245,241,233,.10) 58%,rgba(245,241,233,0) 75%)!important;
}
a.hdar-ci-amazon-banner .hdar-ci-content{
  display:flex!important;box-sizing:border-box!important;position:absolute!important;
  z-index:3!important;top:5%!important;bottom:auto!important;left:0!important;
  width:100%!important;height:auto!important;min-height:0!important;
  align-items:flex-start!important;justify-content:flex-start!important;flex-direction:column!important;
  text-align:left!important;padding:0 6%!important;background:transparent!important;
}
a.hdar-ci-amazon-banner .hdar-ci-title{
  display:block!important;box-sizing:border-box!important;min-width:0!important;
  color:#17313c!important;font-family:Montserrat,Arial,sans-serif!important;
  font-weight:800!important;line-height:1.06!important;letter-spacing:-.025em!important;
  overflow-wrap:normal!important;word-break:normal!important;white-space:normal!important;
  font-size:clamp(13px,calc(6.9cqw * var(--hdar-title-scale,1)),28px)!important;
}
a.hdar-ci-amazon-banner-wide .hdar-ci-content{
  top:11%!important;width:56%!important;padding:0 0 0 4.2%!important;
}
a.hdar-ci-amazon-banner-wide .hdar-ci-title{
  max-width:100%!important;
  white-space:nowrap!important;
  font-size:clamp(11px,calc(3.35cqw * var(--hdar-title-scale,1)),44px)!important;
  overflow:visible!important;
}
a.hdar-ci-amazon-banner .hdar-ci-button{
  display:flex!important;position:absolute!important;z-index:4!important;box-sizing:border-box!important;
  align-items:center!important;justify-content:center!important;gap:4px!important;
  left:auto!important;right:5.5%!important;bottom:8%!important;transform:none!important;
  width:max-content!important;max-width:calc(100% - 14px)!important;min-height:0!important;
  padding:4px 6px!important;background:#ffbe38!important;
  border:1px solid rgba(97,56,4,.11)!important;border-radius:2px!important;
  box-shadow:0 2px 8px rgba(0,0,0,.15)!important;white-space:nowrap!important;
}
a.hdar-ci-amazon-banner-wide .hdar-ci-button{
  left:4.2%!important;right:auto!important;bottom:10%!important;
}
a.hdar-ci-amazon-banner .hdar-ci-amazon-official{
  display:block!important;width:clamp(140px,15cqw,160px)!important;
  min-width:140px!important;max-width:160px!important;height:auto!important;
  max-height:35px!important;object-fit:contain!important;flex:0 0 auto!important;
}
a.hdar-ci-amazon-banner .hdar-ci-amazon-arrow{
  font-size:18px!important;margin-left:2px!important;line-height:1!important;
}
@container (max-width:700px){
 a.hdar-ci-amazon-banner-wide .hdar-ci-content{width:59%!important;}
 a.hdar-ci-amazon-banner-wide .hdar-ci-title-long{
   white-space:normal!important;max-height:2.15em!important;overflow:hidden!important;
   font-size:clamp(11px,2.6cqw,17px)!important;line-height:1.04!important;
   overflow-wrap:anywhere!important;
 }
}
@container (max-width:480px){
 a.hdar-ci-amazon-banner-wide .hdar-ci-content{width:63%!important;top:8%!important;}
 a.hdar-ci-amazon-banner-wide .hdar-ci-title-long{font-size:11px!important;}
 a.hdar-ci-amazon-banner-wide .hdar-ci-button{left:4.2%!important;bottom:7%!important;}
 a.hdar-ci-amazon-banner .hdar-ci-button{padding:3px 4px!important;gap:2px!important;}
 a.hdar-ci-amazon-banner .hdar-ci-amazon-arrow{font-size:15px!important;}
}
body .hd-next-partner-banner:has(.hdar-ci-amazon-slot){
  min-width:0!important;max-width:100%!important;width:100%!important;
}
@media(max-width:640px){
  body .hd-next-partner-banner:has(.hdar-ci-amazon-slot){
    max-width:calc(100vw - 24px)!important;
  }
}
"""

HERO_CSS="""
/* HD007 1.2.18: index hero only, mobile copy always readable. */
@media(max-width:760px){
 .hdr-hero:not(.is-profile) .hdr-hero-copy{
   width:74%!important;padding:13px 16px!important;transform:none!important;
 }
 .hdr-hero:not(.is-profile) h1{font-size:clamp(27px,7.4vw,36px)!important;line-height:1.08!important;}
 .hdr-hero:not(.is-profile) .hdr-brush-claim{
   font-size:clamp(17px,5vw,21px)!important;margin-bottom:12px!important;
 }
 .hdr-hero:not(.is-profile) p{
   max-width:27ch!important;font-size:clamp(11px,3.1vw,13px)!important;
   line-height:1.34!important;
 }
}
"""

def replace_single(s, before, after, label):
    n=s.count(before)
    assert n==1,(label,n)
    return s.replace(before,after)

def modify_009(name,raw):
    if name==AD_CSS:
        s=raw.decode("utf8")
        assert "HD009 0.1.20" in s and "HD009 0.1.21" not in s
        return (s+BANNER_CSS).encode()
    if name==AD_MAIN:
        s=raw.decode("utf8")
        s=replace_single(s,"* Version: 0.1.20-dev","* Version: 0.1.21-dev","version 009")
        mark="        $size = $square ? 'square' : 'wide';"
        inject="""        // The same self-contained banner scales to each slot. Longer hobby names
        // use a smaller title without manual per-hobby configuration.
        $title_length = function_exists('mb_strlen') ? mb_strlen($topic, 'UTF-8') : strlen($topic);
        $title_scale = max(0.36, min(1.35, 23 / max(12, $title_length)));
        $title_class = $title_length > 29 ? ' hdar-ci-title-long' : '';
        $title_style = '--hdar-title-scale:'.number_format($title_scale, 3, '.', '');
"""
        s=replace_single(s,mark,mark+"\n"+inject,"ad meta")
        before="""            .'<span class="hdar-ci-content"><strong class="hdar-ci-title">'.esc_html($topic).'</strong></span>'"""
        after="""            .'<span class="hdar-ci-content"><strong class="hdar-ci-title'.$title_class.'" style="'.esc_attr($title_style).'">'.esc_html($topic).'</strong></span>'"""
        s=replace_single(s,before,after,"ad markup")
        return s.encode()
    return raw

def modify_007(name,raw):
    if name==REG_MAIN:
        s=raw.decode()
        s=replace_single(s,"* Version: 1.2.17","* Version: 1.2.18","register version")
        return s.encode()
    if name==REG_FRONT:
        s=raw.decode()
        older="Entdecke bekannte, seltene und ungewöhnliche Hobbys. Suche direkt nach einem Namen oder stöbere nach Anfangsbuchstaben und Hobbygruppen."
        s=replace_single(s,older,"Entdecke neue und ungewöhnliche Hobbys.","register intro")
        assert s.count("</style>")==1,"Unexpected register stylesheet anchors"
        assert "'" not in HERO_CSS, "CSS literal contains apostrophe"
        s=s.replace("</style>",HERO_CSS+"</style>")
        return s.encode()
    return raw

def build(path,expected,transform,expected_mods,expected_entries):
    source=path.read_bytes()
    assert sha256(source).hexdigest()==expected,(str(path),"Wrong CURRENT baseline")
    buffer=BytesIO()
    changed=[]
    with ZipFile(BytesIO(source)) as inp, ZipFile(buffer,"w") as out:
        assert inp.testzip() is None
        assert len(inp.namelist())==expected_entries
        assert len(inp.namelist())==len(set(inp.namelist()))
        for member in inp.infolist():
            before=inp.read(member.filename)
            after=transform(member.filename,before)
            if before!=after:changed.append(member.filename)
            out.writestr(member,after)
        out.comment=inp.comment
    assert set(changed)==set(expected_mods),(changed,expected_mods)
    outbytes=buffer.getvalue()
    with ZipFile(BytesIO(outbytes)) as inp:
        assert inp.testzip() is None
        with tempfile.TemporaryDirectory() as dirname:
            names=[x for x in inp.namelist() if x.endswith(".php")]
            for name in names:
                filepath=Path(dirname)/name
                filepath.parent.mkdir(parents=True,exist_ok=True)
                filepath.write_bytes(inp.read(name))
                check=subprocess.run(["php","-l",str(filepath)],capture_output=True,text=True)
                assert check.returncode==0,(name,check.stderr)
        print("PHP_PASS",len(names))
    path.write_bytes(outbytes)
    print("ZIP_PASS",path.name,"bytes",len(outbytes),"sha256",sha256(outbytes).hexdigest(),"changed",changed)
    return sha256(outbytes).hexdigest()

def main():
    build(HD009,ORIGINAL[HD009],modify_009,{AD_CSS,AD_MAIN},33)
    build(HD007,ORIGINAL[HD007],modify_007,{REG_MAIN,REG_FRONT},93)
    print("Both source ZIPs verified; two independent existing plugins, no new plugin.")
if __name__=="__main__":
    main()
