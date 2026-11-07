#!/usr/bin/env python3
from pathlib import Path
from io import BytesIO
from zipfile import ZipFile
from hashlib import sha256
from tempfile import TemporaryDirectory
import subprocess

ROOT=Path("protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/PLUGINS/ISOLIERTE_PLUGINS")
PACKAGES={
    "HD-009-AFFILIATE-ZENTRALE": {
        "oldsha":"f6dd1cb301dbe661b63a9dd6b7890d0363c3317f025ee8617a94348b6001a002",
        "old":"0.1.21-dev","new":"0.1.22",
        "filename":"HOBBY_DEPOT_AFFILIATE_HD009_0.1.22.zip",
        "rootfile":"affiliate-portal-router/hobby-depot-affiliate-router.php",
        "stylefile":"affiliate-portal-router/includes/class-hdar-amazon-start.php",
        "files":33,"php":24,
    },
    "HD-007-HOBBYREGISTER-CORE": {
        "oldsha":"1908ff82d348993bb5012fad9357e67a4580170fa40d9710fc03084f26d64935",
        "old":"1.2.18","new":"1.2.20",
        "filename":"HOBBY_DEPOT_HOBBYREGISTER_HD007_1.2.20.zip",
        "rootfile":"hd-hobbyregister-core/hobby-depot-hobbyregister-core.php",
        "files":93,"php":4,
    },
}
for plugin,p in PACKAGES.items():
    current=ROOT/plugin/"CURRENT.zip"
    original=current.read_bytes()
    assert sha256(original).hexdigest()==p['oldsha'],f"Source mismatch {plugin}"
    result=BytesIO(); changed=[]
    with ZipFile(BytesIO(original)) as z,ZipFile(result,"w") as out:
        assert z.testzip() is None and len(z.namelist())==p['files']
        assert len(set(z.namelist()))==len(z.namelist())
        for f in z.infolist():
            before=z.read(f.filename);after=before
            if f.filename==p['rootfile']:
                s=before.decode()
                o=f" * Version: {p['old']}"
                n=f" * Version: {p['new']}"
                assert s.count(o)==1,(plugin,"header",s[:290])
                after=s.replace(o,n).encode()
            elif f.filename==p.get('stylefile'):
                s=before.decode()
                # Fresh stylesheet version prevents browser/cache from using the preceding banner.
                o="'0.1.21'"
                assert s.count(o)==1,(plugin,"style version")
                after=s.replace(o,"'0.1.22'").encode()
            if before!=after:changed.append(f.filename)
            out.writestr(f,after)
        out.comment=z.comment
    assert set(changed)==set([p['rootfile']]+([p['stylefile']] if 'stylefile' in p else [])),(plugin,changed)
    payload=result.getvalue()
    with ZipFile(BytesIO(payload)) as z:
        assert z.testzip() is None and len(z.namelist())==p['files']
        with TemporaryDirectory() as temp:
            count=0
            for n in z.namelist():
                if not n.endswith(".php"):continue
                f=Path(temp)/n;f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes(z.read(n))
                check=subprocess.run(["php","-l",str(f)],capture_output=True,text=True)
                assert check.returncode==0,(n,check.stderr)
                count+=1
            assert count==p['php'],(plugin,count)
        header=z.read(p['rootfile']).decode().split("*/",1)[0]
        assert f" * Version: {p['new']}" in header,header[:300]
    # Two links with the very same bytes: CURRENT for Campus, unique filename for user downloads.
    current.write_bytes(payload)
    named=current.parent/p['filename']
    named.write_bytes(payload)
    assert current.read_bytes()==named.read_bytes()
    print("PACKAGE_PASS",plugin,"version",p["new"],"name",p["filename"],"bytes",len(payload),"sha256",sha256(payload).hexdigest(),"php",p["php"],"files",p["files"],"changes",changed)
print("DISTINCT_NAMES_AND_BYTE_IDENTICAL_CURRENT_PASS")
