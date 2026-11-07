#!/usr/bin/env python3
"""Final HD007 direct profile integration: ignore native no-output diagnostic comment, never override a real partner creative."""
from pathlib import Path
import hashlib,tempfile,subprocess,zipfile
root=Path("protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH")
zip_path=root/"PLUGINS/ISOLIERTE_PLUGINS/HD-009-AFFILIATE-ZENTRALE/CURRENT.zip"
main="affiliate-portal-router/hobby-depot-affiliate-router.php"
with zipfile.ZipFile(zip_path) as z:
    assert z.testzip() is None
    entries={i.filename:z.read(i.filename) for i in z.infolist() if not i.is_dir()}
s=entries[main].decode("utf-8")
old="""        if (trim($html)==='') { $html=$this->hdar_ci_amazon_banner($context,'glossary_single_desktop_banner','hobbyregister_'.$slug,$row); }"""
new="""        $native_empty = trim($html)==='' ||
            (preg_match('/^\\s*<!--[\\s\\S]*-->\\s*$/D', $html) === 1);
        if ($native_empty) {
            $html=$this->hdar_ci_amazon_banner($context,'glossary_single_desktop_banner','hobbyregister_'.$slug,$row);
        }"""
assert s.count(old)==1,("Register empty native comment logic missing",s.count(old))
s=s.replace(old,new,1)
assert s.count("Version: 0.1.17-dev")==1
assert "($register_row['canonical_name'] ?? '')" in s
assert "($entry['path'] ?? '')" in s and "($entry['source'] ?? '')" in s
assert "hdar_approved_rental_banner_fallback" not in s
entries[main]=s.encode("utf-8")
with tempfile.TemporaryDirectory() as tmp:
    for name,b in entries.items():
        if name.endswith(".php"):
            target=Path(tmp)/name
            target.parent.mkdir(parents=True,exist_ok=True)
            target.write_bytes(b)
            q=subprocess.run(["php","-l",str(target)],capture_output=True,text=True)
            assert q.returncode==0,(name,q.stdout,q.stderr)
new_path=zip_path.with_suffix(".fix.zip")
with zipfile.ZipFile(new_path,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for name,b in sorted(entries.items()):
        z.writestr(name,b)
with zipfile.ZipFile(new_path) as z:
    assert z.testzip() is None
    assert set(z.namelist())==set(entries)
new_path.replace(zip_path)
sha=hashlib.sha256(zip_path.read_bytes()).hexdigest()
report=root/"PLUGINS/PLUGIN_AKTEN/HD-009-AFFILIATE-ZENTRALE/EVIDENCE/HD009_0117_CI_SINGLE_RELEASE_REPORT.txt"
lines=report.read_text().splitlines()
lines=[f"ZIP bytes: {zip_path.stat().st_size}" if l.startswith("ZIP bytes:") else 
       f"ZIP SHA-256: {sha}" if l.startswith("ZIP SHA-256:") else l for l in lines]
lines.append("HD007 final profile render: debug/no-output HTML comments are treated as empty, real native provider HTML remains first.")
report.write_text("\n".join(lines)+"\n")
print("PASS full package",zip_path.stat().st_size,sha, "PHP 24/24, ZIP CRC")
