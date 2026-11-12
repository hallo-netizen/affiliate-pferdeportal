#!/usr/bin/env python3
"""Minimum HAB-004 RC22: CSS asset cache key follows the real plugin header.
RC21 PHP/category source, image metadata, insurance gates, provider/GTIN untouched.
"""
from io import BytesIO
from zipfile import ZipFile
from pathlib import Path
import hashlib
root=Path("protocol/PROJECT_MEMORY/PROJEKTE/EIGENTUMSSCHUTZ")
p=root/"PLUGINS/ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip"
data=p.read_bytes()
sha=lambda v:hashlib.sha256(v).hexdigest()
assert sha(data)=="0f40eddb4526434c03acdd370d2763ac5a01eaea862a40cb9ae25bb8754363bf",("Unexpected RC21 base",sha(data))
folder="affiliate-portal-router/"
main=folder+"affiliate-portal-router.php"
readme=folder+"readme.txt"
css=folder+"assets/frontend.css"
with ZipFile(BytesIO(data)) as archive:
    assert archive.testzip() is None and len(archive.namelist())==36
    files={i.filename:archive.read(i.filename) for i in archive.infolist()}
    code=files[main].decode("utf8")
    assert code.count("Version: 0.1.18-rc21")==1
    code=code.replace("Version: 0.1.18-rc21","Version: 0.1.19-rc22",1)
    before="self::VERSION . '-hb-rc16-20261108'"
    after="self::VERSION . '-hb-plugin-' . (string) (get_file_data(__FILE__, array('Version' => 'Version'), 'plugin')['Version'] ?? '')"
    assert code.count(before)==1
    code=code.replace(before,after,1)
    # WordPress get_file_data is a native core function, reads only the file header.
    # All remaining PHP is byte identical to RC21.
    files[main]=code.encode("utf8")
    read=files[readme].decode("utf8")
    assert read.count("Stable tag: 0.1.18-rc21")==1
    files[readme]=read.replace("Stable tag: 0.1.18-rc21","Stable tag: 0.1.19-rc22",1).encode("utf8")
    for name in archive.namelist():
        if name not in (main,readme):
            assert archive.read(name)==files[name]
    assert b".ppar-hb-category-products-grid" in files[css]
    assert b"feed_id'] ?? '') === '2901'" not in files[folder+"includes/trait-ppar-idealo.php"]
    out=BytesIO()
    with ZipFile(out,"w") as archive_out:
        for member in archive.infolist():archive_out.writestr(member,files[member.filename])
    built=out.getvalue()
with ZipFile(BytesIO(built)) as archive:
    assert archive.testzip() is None
    assert len(archive.namelist())==36
    php=archive.read(main).decode("utf8")
    assert php.count("Version: 0.1.19-rc22")==1
    assert before not in php and after in php
p.write_bytes(built)
print("RC22_RELEASE",len(built),"SHA256",sha(built),"36 CRC PASS, only main and readme changed, native get_file_data asset version")
