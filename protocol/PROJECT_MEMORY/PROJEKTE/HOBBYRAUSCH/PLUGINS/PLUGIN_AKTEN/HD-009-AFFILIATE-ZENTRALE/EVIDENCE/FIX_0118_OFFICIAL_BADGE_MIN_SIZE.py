#!/usr/bin/env python3
"""Keep approved DE Amazon badge at >=140px; use text-only CTA when sidebar width cannot fit."""
from pathlib import Path
import hashlib,zipfile
root=Path("protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH")
f=root/"PLUGINS/ISOLIERTE_PLUGINS/HD-009-AFFILIATE-ZENTRALE/CURRENT.zip"
css_path="affiliate-portal-router/assets/hdar-amazon-start.css"
main="affiliate-portal-router/hobby-depot-affiliate-router.php"
with zipfile.ZipFile(f) as z:
    assert z.testzip() is None
    files={i.filename:z.read(i.filename) for i in z.infolist() if not i.is_dir()}
assert b"Version: 0.1.18-dev" in files[main]
css=files[css_path].decode("utf8")
assert "HD009 0.1.18" in css and "hdar-ci-amazon-official" in css
assert "/* HD009 0.1.18 official badge min-width repair */" not in css
css+=r"""
/* HD009 0.1.18 official badge min-width repair.
   Amazon logo is unchanged/unscaled below 140px; tiny cards show pure text. */
a.hdar-ci-amazon-banner .hdar-ci-button{
  padding-left:clamp(4px,1.1cqw,16px)!important;
  padding-right:clamp(4px,1.1cqw,16px)!important;
}
a.hdar-ci-amazon-banner .hdar-ci-amazon-official{
  width:clamp(140px,27cqw,215px)!important;min-width:140px!important;
  max-width:215px!important;flex:0 0 auto!important;
}
@container (max-width:178px){
  a.hdar-ci-amazon-banner .hdar-ci-amazon-official{display:none!important;}
  a.hdar-ci-amazon-banner .hdar-ci-button::before{
    content:"Bei Amazon entdecken";display:inline!important;
    font:700 12px/1.2 Montserrat,Arial,sans-serif;color:#17272c;
    white-space:nowrap;
  }
}
"""
files[css_path]=css.encode("utf8")
tmp=f.with_suffix(".fixed.zip")
with zipfile.ZipFile(tmp,"w",zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for n,v in sorted(files.items()):z.writestr(n,v)
with zipfile.ZipFile(tmp) as z:assert z.testzip() is None and set(z.namelist())==set(files)
tmp.replace(f)
sha=hashlib.sha256(f.read_bytes()).hexdigest()
report=root/"PLUGINS/PLUGIN_AKTEN/HD-009-AFFILIATE-ZENTRALE/EVIDENCE/HD009_0118_CI_REPORT.txt"
old=report.read_text()
old=old.replace(next(x for x in old.splitlines() if x.startswith("ZIP bytes:")),f"ZIP bytes: {f.stat().st_size}")
old=old.replace(next(x for x in old.splitlines() if x.startswith("SHA256:")),f"SHA256: {sha}")
report.write_text(old+"Official badge >=140px in real sidebar; under 178px text-only Amazon CTA fallback, never distort mark.\n")
print("OFFICIAL BADGE MIN SIZE FIX PASS",f.stat().st_size,sha)
