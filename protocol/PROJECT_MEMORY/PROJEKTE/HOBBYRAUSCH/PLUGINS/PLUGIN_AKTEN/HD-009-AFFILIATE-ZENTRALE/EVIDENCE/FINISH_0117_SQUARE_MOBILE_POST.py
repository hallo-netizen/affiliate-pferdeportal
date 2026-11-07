#!/usr/bin/env python3
"""Keep user's CI contract: square Own-Amazon banners on Glossar desktop/mobile, actual featured photo on posts."""
from pathlib import Path
import hashlib,zipfile,tempfile,subprocess
root=Path("protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH")
f=root/"PLUGINS/ISOLIERTE_PLUGINS/HD-009-AFFILIATE-ZENTRALE/CURRENT.zip"
main="affiliate-portal-router/hobby-depot-affiliate-router.php"
with zipfile.ZipFile(f) as z:
    assert z.testzip() is None
    d={i.filename:z.read(i.filename) for i in z.infolist() if not i.is_dir()}
s=d[main].decode('utf8')
old="array('glossary_single_banner','glossary_single_desktop_banner'), true);"
new="array('glossary_single_banner','glossary_single_desktop_banner','glossary_single_mobile_banner'), true);"
assert s.count(old)==1
s=s.replace(old,new,1)
old="array('glossary_single_mobile_banner','post_inline_banner','hub_mid_banner','template_mid_banner'), true);"
new="array('post_inline_banner','hub_mid_banner','template_mid_banner'), true);"
assert s.count(old)==1
s=s.replace(old,new,1)
old="""        $post_id = absint($context['post_id'] ?? 0);"""
new="""        $post_id = absint($context['post_id'] ?? 0);
        if ($post_id === 0 && is_numeric($content_id)) { $post_id = absint($content_id); }"""
ci_start=s.index("    private function hdar_ci_amazon_banner(")
ci_end=s.index("    /** HD007 owns", ci_start)
ci=s[ci_start:ci_end]
assert ci.count(old)==1, "Need single post_id occurrence inside own Amazon CI method only"
ci=ci.replace(old,new,1)
s=s[:ci_start]+ci+s[ci_end:]
assert "hdar_approved_rental_banner_fallback" not in s
assert "Version: 0.1.17-dev" in s
assert "($register_row['canonical_name'] ?? '')" in s
d[main]=s.encode('utf8')
with tempfile.TemporaryDirectory() as tmp:
    for n,b in d.items():
        if n.endswith('.php'):
            p=Path(tmp)/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
            x=subprocess.run(['php','-l',str(p)],capture_output=True,text=True)
            assert x.returncode==0,(n,x.stdout,x.stderr)
n=f.with_suffix(".final.zip")
with zipfile.ZipFile(n,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for k,b in sorted(d.items()):z.writestr(k,b)
with zipfile.ZipFile(n) as z:
    assert z.testzip() is None and set(z.namelist())==set(d)
n.replace(f)
sha=hashlib.sha256(f.read_bytes()).hexdigest()
report=root/"PLUGINS/PLUGIN_AKTEN/HD-009-AFFILIATE-ZENTRALE/EVIDENCE/HD009_0117_CI_SINGLE_RELEASE_REPORT.txt"
lines=report.read_text().splitlines()
lines=[f"ZIP bytes: {f.stat().st_size}" if t.startswith('ZIP bytes:') else
       f"ZIP SHA-256: {sha}" if t.startswith('ZIP SHA-256:') else t for t in lines]
lines.append("CI: own Glossar banner square on both desktop and mobile. Existing native real partner creatives unaffected.")
lines.append("Optional article featured image: use actual content ID when context post_id absent.")
report.write_text('\n'.join(lines)+'\n')
print("CI END QA PASS",f.stat().st_size,sha)
