#!/usr/bin/env python3
"""Focused HD009/HD007 update: no claim punctuation and less tall horizontal banner."""
from pathlib import Path
from zipfile import ZipFile
from io import BytesIO
from tempfile import TemporaryDirectory
from hashlib import sha256
import subprocess

ROOT=Path("protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/PLUGINS/ISOLIERTE_PLUGINS")
ITEMS={
 "HD-009-AFFILIATE-ZENTRALE":{
  "hash":"019926c8bc2d09a7c206da93cd3a10e262329435f1acca8cd09bae352238e1b9",
  "version_before":"0.1.22","version_after":"0.1.23",
  "filename":"HOBBY_DEPOT_AFFILIATE_HD009_0.1.23.zip",
  "main":"affiliate-portal-router/hobby-depot-affiliate-router.php",
  "style":"affiliate-portal-router/assets/hdar-amazon-start.css",
  "stylesheet_loader":"affiliate-portal-router/includes/class-hdar-amazon-start.php",
  "entries":33,"php":24
 },
 "HD-007-HOBBYREGISTER-CORE":{
  "hash":"e1b63a3c54819427314956e8f05db522b3c76768b0164662c33e7f76f9782e3c",
  "version_before":"1.2.20","version_after":"1.2.21",
  "filename":"HOBBY_DEPOT_HOBBYREGISTER_HD007_1.2.21.zip",
  "main":"hd-hobbyregister-core/hobby-depot-hobbyregister-core.php",
  "front":"hd-hobbyregister-core/includes/class-hd-hobbyregister-frontend.php",
  "entries":93,"php":4
 }
}
def one(s,before,after,where):
 n=s.count(before)
 assert n==1,(where,n,before)
 return s.replace(before,after)
for plugin,p in ITEMS.items():
 path=ROOT/plugin/"CURRENT.zip"
 data=path.read_bytes()
 assert sha256(data).hexdigest()==p["hash"],plugin+" source hash mismatch"
 changed=[]
 outb=BytesIO()
 with ZipFile(BytesIO(data)) as old,ZipFile(outb,"w") as out:
  assert old.testzip() is None
  assert len(old.namelist())==p["entries"]
  for info in old.infolist():
   before=old.read(info.filename)
   s=before.decode("utf-8") if info.filename.endswith((".css",".php")) else None
   if info.filename==p["main"]:
    s=one(s," * Version: "+p["version_before"]," * Version: "+p["version_after"],"WordPress header "+plugin)
   if info.filename==p.get("style"):
    s=one(s,"a.hdar-ci-amazon-banner-wide{aspect-ratio:3/1!important;min-height:0!important;}",
            "a.hdar-ci-amazon-banner-wide{aspect-ratio:4.2/1!important;min-height:0!important;}","banner geometry")
   if info.filename==p.get("stylesheet_loader"):
    s=one(s,"'0.1.22'","'0.1.23'","style cache")
   if info.filename==p.get("front"):
    s=one(s,"Entdecke neue und ungewöhnliche Hobbys.","Entdecke neue und ungewöhnliche Hobbys","index claim")
   after=s.encode("utf-8") if s is not None else before
   if after!=before:changed.append(info.filename)
   out.writestr(info,after)
  out.comment=old.comment
 expected={p["main"]}
 expected.update({p[k] for k in ("style","stylesheet_loader","front") if k in p})
 assert set(changed)==expected,(plugin,changed,expected)
 payload=outb.getvalue()
 with ZipFile(BytesIO(payload)) as new:
  assert new.testzip() is None and len(new.namelist())==p["entries"]
  assert " * Version: "+p["version_after"] in new.read(p["main"]).decode().split("*/",1)[0]
  if "style" in p:
   css=new.read(p["style"]).decode()
   assert "aspect-ratio:4.2/1!important;min-height:0!important;" in css
   assert "aspect-ratio:3/1!important;min-height:0!important;" not in css
  if "front" in p:
   s=new.read(p["front"]).decode()
   assert "Entdecke neue und ungewöhnliche Hobbys.</p>" not in s
   assert "Entdecke neue und ungewöhnliche Hobbys</p>" in s
  with TemporaryDirectory() as temp:
   phps=[n for n in new.namelist() if n.endswith(".php")]
   assert len(phps)==p["php"]
   for n in phps:
    f=Path(temp)/n;f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes(new.read(n))
    result=subprocess.run(["php","-l",str(f)],capture_output=True,text=True)
    assert result.returncode==0,(n,result.stderr)
 path.write_bytes(payload)
 named=path.parent/p["filename"];named.write_bytes(payload)
 assert path.read_bytes()==named.read_bytes()
 print("RELEASE_OK",plugin,p["version_after"],p["filename"],len(payload),sha256(payload).hexdigest(),"files_changed",changed)
print("FULL_ZIP_CRC_PHP_VERSION_AND_DISTINCT_FILENAME_PASS")
