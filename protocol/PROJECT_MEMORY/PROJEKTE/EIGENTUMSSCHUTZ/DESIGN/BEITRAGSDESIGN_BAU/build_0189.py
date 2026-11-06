#!/usr/bin/env python3
"""Deterministically rebuild the exact Hab & Bewahr Design 0.1.189 ZIP.
Source and all changes are authenticated and rechecked. No WordPress writes.
"""
from pathlib import Path
import base64,hashlib,lzma,subprocess,tempfile,zipfile

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1] # EIGENTUMSSCHUTZ
BASE=HERE/"HAB_UND_BEWAHR_DESIGN_0.1.185_BEITRAEGE.zip"
PATCH=HERE/"patch_0189.xz.b64"
DEST=ROOT/"PLUGINS/ISOLIERTE_PLUGINS/HAB-001-DESIGN/CURRENT.zip"
HASH_BASE="0cdcaa71ef522347e6e0c2b9c54754becbcf488bedd31c2215fa69eda7b1c390"
HASH_PATCH="d65b830e76d4c23bb89d4bc8b8bf341ba1381b2410077c3992352b4ae0dfa442"
HASH_TARGET="947a950273edb6bf47e76ffeef67ff51425db620adc2650c742831e73093134c"
SIZE_TARGET=84349647

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()

assert digest(BASE)==HASH_BASE,"0.1.185 base mismatch"
patch_encoded=PATCH.read_text(encoding="ascii").strip()
assert len(patch_encoded)==13584,"Incomplete patch"
patch_bytes=base64.b64decode(patch_encoded,validate=True)
assert hashlib.sha256(patch_bytes).hexdigest()==HASH_PATCH,"Patch bytes differ from locally tested source"
patch= lzma.decompress(patch_bytes)
assert patch.startswith(b'--- a/hab-bewahr-design-vorschau/'),"Wrong patch"
original=ROOT/"PLUGINS/ISOLIERTE_PLUGINS/HAB-001-DESIGN/CURRENT.zip"
assert original.stat().st_size==84339643,"Unexpected previous Campus original"
assert digest(original)=="76043e5c093058a4d8aff8fd6642307cade951c8267641dc710b8ed70cd323e3","Wrong verified original"

with tempfile.TemporaryDirectory() as td:
    temp=Path(td)
    with zipfile.ZipFile(BASE) as z:
        assert z.testzip() is None
        entries=z.infolist()
        assert len(entries)==428
        z.extractall(temp)
    sub=subprocess.run(["patch","-p1","--batch","--forward"],input=patch,cwd=temp,capture_output=True,check=True)
    print(sub.stdout.decode("utf-8","replace"))
    built=temp/"new.zip"
    with zipfile.ZipFile(built,"w") as z:
        for info in entries:
            contents=(temp/info.filename).read_bytes() if not info.is_dir() else b""
            z.writestr(info,contents)
        extras={
          "hab-bewahr-design-vorschau/includes/article-undated-seo.php":(2026,11,6,10,46,54),
          "hab-bewahr-design-vorschau/assets/article-mobile-affiliate.js":(2026,11,6,11,45,6)
        }
        for name,ts in extras.items():
            info=zipfile.ZipInfo(name,date_time=ts)
            info.compress_type=zipfile.ZIP_DEFLATED
            info.create_system=3
            info.external_attr=25165824
            z.writestr(info,(temp/name).read_bytes())
    assert built.stat().st_size==SIZE_TARGET,"Unexpected ZIP size"
    assert digest(built)==HASH_TARGET,"ZIP SHA differs from installed-candidate artifact"
    with zipfile.ZipFile(built) as z:
        assert len(z.namelist())==430 and z.testzip() is None
        assert z.namelist()[0].startswith("hab-bewahr-design-vorschau/")
        assert b"Version: 0.1.189" in z.read("hab-bewahr-design-vorschau/hab-bewahr-design-vorschau.php")
    DEST.write_bytes(built.read_bytes())

print("PASS: exact installable 0.1.189, 430 entries, 84349647 bytes, sha256="+HASH_TARGET)
print("Saved in existing Hab & Bewahr Design office at",DEST)
