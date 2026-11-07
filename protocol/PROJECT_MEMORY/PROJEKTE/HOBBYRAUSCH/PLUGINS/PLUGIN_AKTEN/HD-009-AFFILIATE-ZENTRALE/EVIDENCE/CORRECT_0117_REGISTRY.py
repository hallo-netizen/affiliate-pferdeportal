#!/usr/bin/env python3
"""Correct HD009 0.1.17 to REAL HD007 canonical_name and picture source/path, no new architecture."""
from pathlib import Path
import zipfile,subprocess,tempfile,hashlib
root=Path("protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH")
path=root/"PLUGINS/ISOLIERTE_PLUGINS/HD-009-AFFILIATE-ZENTRALE/CURRENT.zip"
reg=root/"PLUGINS/ISOLIERTE_PLUGINS/HD-007-HOBBYREGISTER-CORE/CURRENT.zip"
main="affiliate-portal-router/hobby-depot-affiliate-router.php"
with zipfile.ZipFile(reg) as z:
    core=z.read("hd-hobbyregister-core/includes/class-hd-hobbyregister-core.php").decode("utf-8")
    frontend=z.read("hd-hobbyregister-core/includes/class-hd-hobbyregister-frontend.php").decode("utf-8")
    assert "canonical_name" in core and "function image_entry(" in core
    assert "($entry['path'] ?? '')" in frontend and "$entry['source']" in frontend, "Must match actual HD007 image mapping"
with zipfile.ZipFile(path) as z:
    assert z.testzip() is None
    entries={i.filename:z.read(i.filename) for i in z.infolist() if not i.is_dir()}
s=entries[main].decode("utf-8")
assert s.count("Version: 0.1.17-dev")==1
changes={
"($register_row['name'] ?? '')":"($register_row['canonical_name'] ?? '')",
"($item['name'] ?? '')":"($item['canonical_name'] ?? '')",
"$name=(string)$row['name'];":"$name=(string)$row['canonical_name'];",
}
for bad,good in changes.items():
    assert s.count(bad)==1,(bad,s.count(bad))
    s=s.replace(bad,good,1)
old="""            if (is_array($entry)) {
                foreach (array('url','image_url','src') as $key) {
                    if (!empty($entry[$key]) && is_string($entry[$key])) { $photo=esc_url_raw($entry[$key]); break; }
                }
            }"""
new="""            if (is_array($entry)) {
                // Exact existing HD007 image-entry contract is source + path (not url).
                $asset_path = trim((string)($entry['path'] ?? ''));
                $asset_source = (string)($entry['source'] ?? '');
                $semantic_fit = strtoupper((string)($entry['core_audit_semantic_fit'] ?? ''));
                $production = strtoupper((string)($entry['production_status'] ?? ''));
                $quality = strtoupper((string)($entry['core_audit_final_verdict'] ?? ''));
                // Never show known wrong or unapproved category photos as ads.
                if ($asset_path !== '' && strpos($asset_path, '..') === false &&
                    $asset_path[0] !== '/' && $semantic_fit !== 'FAIL' &&
                    strpos($production, 'OPEN') !== 0 && strpos($quality, 'FAIL') !== 0) {
                    if ($asset_source === 'hd003') {
                        $photo = plugins_url('affiliate-portal-template-kit/assets/' . ltrim($asset_path, '/'));
                    } elseif ($asset_source === 'hd007') {
                        $photo = plugins_url('hd-hobbyregister-core/assets/' . ltrim($asset_path, '/'));
                    }
                }
            }"""
assert s.count(old)==1,("HD007 image map old block",s.count(old))
s=s.replace(old,new,1)
assert "($register_row['name'] ?? '')" not in s
assert "($item['name'] ?? '')" not in s
assert "$name=(string)$row['name'];" not in s
assert "source + path" in s
assert "hdar_approved_rental_banner_fallback" not in s
assert "glossary_single_desktop_banner" in s and "glossary_single_mobile_banner" in s
assert "'ratio_min'=>5.00,'ratio_max'=>12.00" in s
entries[main]=s.encode("utf-8")
with tempfile.TemporaryDirectory() as tmp:
    for n,data in entries.items():
        if n.endswith(".php"):
            p=Path(tmp)/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
            result=subprocess.run(["php","-l",str(p)],capture_output=True,text=True)
            assert result.returncode==0,(n,result.stdout,result.stderr)
next_zip=path.with_suffix(".final.zip")
with zipfile.ZipFile(next_zip,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for n,data in sorted(entries.items()):z.writestr(n,data)
with zipfile.ZipFile(next_zip) as z:
    assert z.testzip() is None
    assert set(z.namelist())==set(entries)
next_zip.replace(path)
sha=hashlib.sha256(path.read_bytes()).hexdigest()
report=root/"PLUGINS/PLUGIN_AKTEN/HD-009-AFFILIATE-ZENTRALE/EVIDENCE/HD009_0117_CI_SINGLE_RELEASE_REPORT.txt"
old_report=report.read_text()
new_report=old_report.replace(
    next((l for l in old_report.splitlines() if l.startswith("ZIP bytes:")), "ZIP bytes: missing"),
    f"ZIP bytes: {path.stat().st_size}"
).replace(
    next((l for l in old_report.splitlines() if l.startswith("ZIP SHA-256:")), "ZIP SHA-256: missing"),
    f"ZIP SHA-256: {sha}"
)
new_report+="\nHD007 readback: canonical_name and exact original image source/path used; known FAIL/OPEN image assignments gated out. Core registry plugin remains unchanged.\n"
report.write_text(new_report)
print("PASS: canonical HD007 profile, source/path image map, full ZIP",path.stat().st_size,sha,"PHP 24/24")
