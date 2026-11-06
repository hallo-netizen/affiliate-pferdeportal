#!/usr/bin/env python3
from pathlib import Path
from zipfile import ZipFile
from hashlib import sha256
import json
root=Path("protocol/PROJECT_MEMORY/PROJEKTE/EIGENTUMSSCHUTZ")
out=root/"AFFILIATE/HAB_BAU/HAB_UND_BEWAHR_AFFILIATE_0.1.0_RC3.zip"
old=root/"PLUGINS/ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip"
with ZipFile(out) as z, ZipFile(old) as previous:
    assert z.testzip() is None and previous.testzip() is None
    assert len(z.namelist())==27 and set(z.namelist())==set(previous.namelist())
    changed=[name for name in z.namelist() if z.read(name)!=previous.read(name)]
    assert set(changed)=={
     "affiliate-portal-router/affiliate-portal-router.php",
     "affiliate-portal-router/includes/class-ppar-hab-bewahr-bridge.php",
     "affiliate-portal-router/readme.txt"},changed
    assert b"Version: 0.1.0-rc3" in z.read("affiliate-portal-router/affiliate-portal-router.php")
manifest=json.loads((root/"AFFILIATE/HAB_BAU/build_report.json").read_text())
assert not manifest["functions_removed"]
assert manifest["sha256"]==sha256(out.read_bytes()).hexdigest()
print("HB_RC3_FULL_FUNCTION_AND_24_UNCHANGED_FILES_PASS",manifest["sha256"],manifest["size_bytes"])
