#!/usr/bin/env python3
"""Minimal HD009 repair: preserve existing horse-origin campaign/category/slot system; remove misplaced rental graphic."""
from pathlib import Path
import zipfile
import hashlib
import subprocess
import tempfile

root=Path("protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH")
path=root/"PLUGINS/ISOLIERTE_PLUGINS/HD-009-AFFILIATE-ZENTRALE/CURRENT.zip"
main="affiliate-portal-router/hobby-depot-affiliate-router.php"
readme="affiliate-portal-router/readme.txt"
wrong_asset="affiliate-portal-router/assets/hdar-approved-own-ad-original-2170x725.png"
with zipfile.ZipFile(path) as z:
    assert z.testzip() is None, "Original ZIP CRC failure"
    entries={i.filename:z.read(i.filename) for i in z.infolist() if not i.is_dir()}
assert main in entries and readme in entries and wrong_asset in entries
original=entries[main].decode("utf-8")
assert original.count("Version: 0.1.15-dev")==1, "Wrong source version"
s=original.replace("Version: 0.1.15-dev","Version: 0.1.16-dev",1)
old=(
"            if ($launch && $selection && !$this->hdar_launch_public_campaign_allowed($selection['campaign'] ?? null)) {\n"
"                // Selected campaign belongs to an inactive partner; NEVER display it.\n"
"                return $this->hdar_approved_rental_banner_fallback($slot_type);\n"
"            }"
)
new=(
"            if ($launch && $selection && !$this->hdar_launch_public_campaign_allowed($selection['campaign'] ?? null)) {\n"
"                // Inactive partners remain hidden. HD003 rental creatives must not enter affiliate slots.\n"
"                return '';\n"
"            }"
)
assert s.count(old)==1, "Unexpected provider-gate code"
s=s.replace(old,new,1)
wrong_block=(
"        if ($this->overview_wide_banner_slot($slot_type)) {\n"
"            // Existing real-banner selection already ran; fill only an empty wide spot.\n"
"            $approved_own_ad = $this->hdar_approved_rental_banner_fallback($slot_type);\n"
"            if ($approved_own_ad !== '') { return $approved_own_ad; }\n"
"        }\n"
)
assert s.count(wrong_block)==1, "Unexpected banner fallback code"
s=s.replace(wrong_block,"",1)
helper="    private function hdar_approved_rental_banner_fallback($slot_type) {"
assert s.count(helper)==1
i=s.index(helper)
begin=s.rfind("    /**",0,i)
end=s.index("    private function render_placeholder_slot($slot_type) {",i)
assert begin>0 and end>i and end-begin<6500
s=s[:begin]+s[end:]
assert "hdar_approved_rental_banner_fallback" not in s
assert "overview_wide_banner_campaign_eligible" in s
assert "'ratio_min'=>5.00,'ratio_max'=>12.00" in s
assert "category_large_banner_rule" in s
assert "glossary_single_desktop_banner" in s and "glossary_single_mobile_banner" in s
assert "hdar_launch_public_campaign_allowed" in s
entries[main]=s.encode("utf-8")
a=entries[readme].decode("utf-8")
assert a.count("Stable tag: 0.1.15-dev")==1
a=a.replace("Stable tag: 0.1.15-dev","Stable tag: 0.1.16-dev",1)
a+=("\n== 0.1.16-dev ==\n"
    "KISS: falschen Eigenwerbungs-Fallback aus Affiliate-Bannerplaetzen entfernt. "
    "Freie Mietwerbung mit Original-Logo bleibt allein beim bestehenden HD003-Designplugin. "
    "Vorhandener Themenabgleich, Kategorie/Elternpfad, Formatschutz und Produktplaetze bleiben erhalten. "
    "Keine neuen Partner, Tabellen oder Ausgabewege.\n")
entries[readme]=a.encode("utf-8")
del entries[wrong_asset]
with tempfile.TemporaryDirectory() as tmp:
    d=Path(tmp)
    php_files=[n for n in entries if n.endswith(".php")]
    for name in php_files:
        f=d/name
        f.parent.mkdir(parents=True,exist_ok=True)
        f.write_bytes(entries[name])
        p=subprocess.run(["php","-l",str(f)],capture_output=True,text=True)
        assert p.returncode==0,(name,p.stdout,p.stderr)
next_zip=path.with_suffix(".repaired.zip")
with zipfile.ZipFile(next_zip,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for name,data in sorted(entries.items()):
        z.writestr(name,data)
with zipfile.ZipFile(next_zip) as z:
    assert z.testzip() is None
    assert set(z.namelist())==set(entries)
    assert z.read(main)==entries[main]
    assert wrong_asset not in z.namelist()
next_zip.replace(path)
sha=hashlib.sha256(path.read_bytes()).hexdigest()
report=root/"PLUGINS/PLUGIN_AKTEN/HD-009-AFFILIATE-ZENTRALE/EVIDENCE/HD009_0116_SLOT_FIX_PASS.txt"
report.parent.mkdir(parents=True,exist_ok=True)
report.write_text(
    "Version: 0.1.16-dev\n"
    f"ZIP bytes: {path.stat().st_size}\n"
    f"ZIP SHA-256: {sha}\n"
    f"PHP syntax: {len(php_files)}/{len(php_files)} PASS\n"
    "ZIP CRC: PASS\n"
    "Regression: native banner campaign eligibility, ratio 5..12, categories/parent path, glossary slots retained.\n"
    "Removed: incorrect HD003 rental creative fallback from affiliate campaign output.\n"
    "HD003 design and reserved rental slots: unchanged.\n"
    "WordPress frontend live: NOT TESTED.\n",
    encoding="utf-8"
)
print("HD009 0.1.16-dev",path.stat().st_size,sha,"PHP",len(php_files),"PASS; ZIP CRC PASS")
