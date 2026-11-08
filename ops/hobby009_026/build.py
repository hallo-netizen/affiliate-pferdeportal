#!/usr/bin/env python3
"""HD009 0.1.26 - only reduce excessive top space above native register inline banner."""
from pathlib import Path
from zipfile import ZipFile
from tempfile import TemporaryDirectory
from io import BytesIO
from hashlib import sha256
import subprocess
root=Path("protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/PLUGINS/ISOLIERTE_PLUGINS/HD-009-AFFILIATE-ZENTRALE")
base=root/"CURRENT.zip"
named=root/"HOBBY_DEPOT_AFFILIATE_HD009_0.1.26.zip"
assert sha256(base.read_bytes()).hexdigest()=="c82b75f9f485eec43f6b8626ff4a6748f3610c0093e61616d4bdd8d4d62204d0", "Unexpected baseline"
main="affiliate-portal-router/hobby-depot-affiliate-router.php"
css="affiliate-portal-router/assets/hdar-amazon-start.css"
loader="affiliate-portal-router/includes/class-hdar-amazon-start.php"
addon="""

/* HD009 0.1.26: compact space directly above the in-text banner in
   hobbyregister single profiles only. The register article uses a 28px
   row-gap; the banner has its own Anzeige label. Do not touch generic
   categories, profile sections, banner dimensions or partner selection. */
body .hdr-profile-grid .hdr-article > .hdar-ci-register-inline:not([hidden]){
  margin-top:-30px!important;
}
@media(max-width:820px){
  body .hdr-profile-grid .hdr-article > .hdar-ci-register-inline:not([hidden]){
    margin-top:-36px!important;
    margin-bottom:10px!important;
  }
}
"""
def once(s,b,a,name):
  assert s.count(b)==1,(name,s.count(b))
  return s.replace(b,a)
changed=[];out=BytesIO()
with ZipFile(base) as src,ZipFile(out,"w") as dest:
  assert src.testzip() is None
  assert len(src.namelist())==41
  for info in src.infolist():
    data=src.read(info.filename);updated=data
    if info.filename==main:
      updated=once(data.decode(),"* Version: 0.1.25","* Version: 0.1.26","header").encode()
    elif info.filename==loader:
      updated=once(data.decode(),"'0.1.25'","'0.1.26'","stylesheet cache version").encode()
    elif info.filename==css:
      decoded=data.decode()
      assert "HD009 0.1.26" not in decoded
      updated=(decoded+addon).encode()
    if data!=updated:changed.append(info.filename)
    dest.writestr(info,updated)
  dest.comment=src.comment
assert set(changed)=={main,loader,css},changed
data=out.getvalue()
with ZipFile(BytesIO(data)) as z:
  assert z.testzip() is None and len(z.namelist())==41
  assert "* Version: 0.1.26" in z.read(main).decode().split("*/",1)[0]
  assert "margin-top:-36px!important;" in z.read(css).decode()
  with TemporaryDirectory() as td:
    names=[name for name in z.namelist() if name.endswith(".php")]
    assert len(names)==24
    for name in names:
      file=Path(td)/name;file.parent.mkdir(parents=True,exist_ok=True);file.write_bytes(z.read(name))
      r=subprocess.run(["php","-l",str(file)],capture_output=True,text=True)
      assert r.returncode==0,(name,r.stderr)
base.write_bytes(data);named.write_bytes(data)
assert base.read_bytes()==named.read_bytes()
print("HD009_026_ZIP_PASS",sha256(data).hexdigest(),"bytes",len(data),"41 entries, 24 PHP PASS, changed",changed)
