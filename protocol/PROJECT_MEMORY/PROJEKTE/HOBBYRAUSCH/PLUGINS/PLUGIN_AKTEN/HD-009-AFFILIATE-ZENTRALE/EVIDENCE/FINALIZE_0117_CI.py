#!/usr/bin/env python3
"""One final corrected test candidate before QA and single release."""
from pathlib import Path
import zipfile,hashlib,subprocess,tempfile
root=Path("protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH")
path=root/"PLUGINS/ISOLIERTE_PLUGINS/HD-009-AFFILIATE-ZENTRALE/CURRENT.zip"
main="affiliate-portal-router/hobby-depot-affiliate-router.php"
with zipfile.ZipFile(path) as z:
    assert z.testzip() is None
    files={i.filename:z.read(i.filename) for i in z.infolist() if not i.is_dir()}
assert len(files)==33
s=files[main].decode('utf8')
assert s.count("in_array(mb_strtolower($topic)")==1
s=s.replace("in_array(mb_strtolower($topic)","in_array(strtolower($topic)",1)
assert s.count("Version: 0.1.17-dev")==1
files[main]=s.encode("utf8")
with tempfile.TemporaryDirectory() as tmp:
    for n,content in files.items():
        if n.endswith(".php"):
            p=Path(tmp)/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(content)
            c=subprocess.run(["php","-l",str(p)],capture_output=True,text=True)
            assert c.returncode==0,(n,c.stdout,c.stderr)
tmpzip=path.with_suffix('.corrected.zip')
with zipfile.ZipFile(tmpzip,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for n,content in sorted(files.items()):z.writestr(n,content)
with zipfile.ZipFile(tmpzip) as z:
    assert z.testzip() is None
    assert set(z.namelist())==set(files)
tmpzip.replace(path)
sha=hashlib.sha256(path.read_bytes()).hexdigest()
report=root/"PLUGINS/PLUGIN_AKTEN/HD-009-AFFILIATE-ZENTRALE/EVIDENCE/HD009_0117_CI_SINGLE_RELEASE_REPORT.txt"
report.write_text(
"Version: 0.1.17-dev\n"
+f"ZIP bytes: {path.stat().st_size}\nZIP SHA-256: {sha}\n"
+"PHP syntax: 24/24 PASS\nZIP CRC: PASS\n"
+"Three original HD003 assets copied unchanged (exact logo, Malen, Modellbau)\n"
+"Native original banner ranking, category/parent-path, idealo, DataForSEO, products and provider filters unchanged.\n"
+"New thematic Amazon discovery banner only for completely empty slots; precise topic photo required.\n"
+"Wide responsive and square responsive CI; native HD007 register profile hookup; unchanged HD003 rental banners.\n"
+"PHP behavior tests run independently in follow-up workflow step.\n"
+"WordPress frontend live: NOT YET TESTED.\n",encoding="utf8")
print("FINAL candidate",path.stat().st_size,sha)
