#!/usr/bin/env python3
"""Minimal HAB-004 RC20 hotfix: feed ID 2901 is legitimately shared across iPN adspaces.
The actual account/website identity is the adspace ID; only 568313 must be rejected.
"""
from pathlib import Path
from io import BytesIO
from zipfile import ZipFile
import hashlib

root=Path("protocol/PROJECT_MEMORY/PROJEKTE/EIGENTUMSSCHUTZ")
source=root/"PLUGINS/ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip"
old=source.read_bytes()
h=lambda b:hashlib.sha256(b).hexdigest()
expected="6d72fcd41a8b365e84815770014098946774bab7f2425c3546e48da66cd262f0"
assert h(old)==expected, ("Do not modify unknown base",h(old))
name="affiliate-portal-router/"
paths={
 "adapter":name+"includes/trait-ppar-idealo.php",
 "bootstrap":name+"affiliate-portal-router.php",
 "readme":name+"readme.txt",
}
with ZipFile(BytesIO(old)) as z:
 assert z.testzip() is None and len(z.namelist())==36
 files={v.filename:z.read(v.filename) for v in z.infolist()}
 before=files[paths["adapter"]].decode("utf8")
 oldline="""if ((string)($settings['adspace_id'] ?? '') === '568313' || (string)($settings['feed_id'] ?? '') === '2901') {"""
 newline="""if ((string)($settings['adspace_id'] ?? '') === '568313') {"""
 assert before.count(oldline)==1, "the exact Idealo blocker has unexpectedly changed"
 after=before.replace(oldline,newline,1)
 comment="Old neutral-stem defaults belonged to another portal; never authorize them for Hab."
 improved="The other portal's ADSPACE is forbidden. Feed 2901 is allowed with Hab's own adspace."
 assert after.count(comment)==1
 after=after.replace(comment,improved,1)
 files[paths["adapter"]]=after.encode("utf8")
 main=files[paths["bootstrap"]].decode("utf8")
 assert main.count("Version: 0.1.16-rc19")==1, "different plugin version"
 files[paths["bootstrap"]]=main.replace("Version: 0.1.16-rc19","Version: 0.1.17-rc20",1).encode("utf8")
 readme=files[paths["readme"]].decode("utf8")
 assert readme.count("Stable tag: 0.1.16-rc19")==1, "unknown readme version"
 files[paths["readme"]]=readme.replace("Stable tag: 0.1.16-rc19","Stable tag: 0.1.17-rc20",1).encode("utf8")
 allowed=set(paths.values())
 for k in files:
    if k not in allowed:
       assert files[k] == z.read(k), "unrelated file changed"
 out=BytesIO()
 with ZipFile(out,"w") as newzip:
    for member in z.infolist():
       newzip.writestr(member,files[member.filename])
 data=out.getvalue()
with ZipFile(BytesIO(data)) as z2:
 assert z2.testzip() is None and len(z2.namelist())==36
 assert b"'adspace_id'] ?? '') === '568313' ||" not in z2.read(paths["adapter"])
 assert b"0.1.17-rc20" in z2.read(paths["bootstrap"])
source.write_bytes(data)
print("RC20 ZIP BUILT; bytes",len(data),"SHA256",h(data),"entries",36)
print("CHANGED FILES:",", ".join(sorted(k.removeprefix(name) for k in allowed)))
