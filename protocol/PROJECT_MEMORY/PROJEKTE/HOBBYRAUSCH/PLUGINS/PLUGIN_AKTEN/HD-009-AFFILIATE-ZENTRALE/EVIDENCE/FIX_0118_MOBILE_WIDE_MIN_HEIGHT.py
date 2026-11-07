#!/usr/bin/env python3
"""Final mobile/wide test: prevent old fixed partner strip from reducing photo below recognisable height."""
from pathlib import Path
import zipfile,hashlib
ROOT=Path("protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH")
Z=ROOT/"PLUGINS/ISOLIERTE_PLUGINS/HD-009-AFFILIATE-ZENTRALE/CURRENT.zip"
CSS="affiliate-portal-router/assets/hdar-amazon-start.css"
with zipfile.ZipFile(Z) as z:
    assert z.testzip() is None
    files={i.filename:z.read(i.filename) for i in z.infolist() if not i.is_dir()}
s=files[CSS].decode("utf8")
assert "HD009 0.1.18" in s and "official badge min-width repair" in s
assert "/* HD009 0.1.18 min wide photo height */" not in s
s+=r"""
/* HD009 0.1.18 min wide photo height: real 355px narrow content still usable.
   Flexible slot keeps chosen width; only a floor for legible photo. */
a.hdar-ci-amazon-banner-wide{min-height:135px!important;}
@media(max-width:640px){a.hdar-ci-amazon-banner-wide{min-height:145px!important;}}
"""
files[CSS]=s.encode("utf8")
out=Z.with_suffix(".final.zip")
with zipfile.ZipFile(out,"w",zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for n,v in sorted(files.items()):z.writestr(n,v)
with zipfile.ZipFile(out) as z:
    assert z.testzip() is None and set(z.namelist())==set(files)
out.replace(Z)
sha=hashlib.sha256(Z.read_bytes()).hexdigest()
report=ROOT/"PLUGINS/PLUGIN_AKTEN/HD-009-AFFILIATE-ZENTRALE/EVIDENCE/HD009_0118_CI_REPORT.txt"
old=report.read_text()
old=old.replace(next(x for x in old.splitlines() if x.startswith("ZIP bytes:")),f"ZIP bytes: {Z.stat().st_size}")
old=old.replace(next(x for x in old.splitlines() if x.startswith("SHA256:")),f"SHA256: {sha}")
report.write_text(old+"Wide creatives now have a small flexible min-height (135px, 145px on phone) to ensure recognisable image and legible CTA.\n")
print("MIN WIDE PHOTO QA FIX",Z.stat().st_size,sha)
