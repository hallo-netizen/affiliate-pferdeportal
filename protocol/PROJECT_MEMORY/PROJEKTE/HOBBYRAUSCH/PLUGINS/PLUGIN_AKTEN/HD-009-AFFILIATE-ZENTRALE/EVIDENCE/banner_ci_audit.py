#!/usr/bin/env python3
from pathlib import Path
import zipfile, re, hashlib
base=Path("protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/PLUGINS/ISOLIERTE_PLUGINS")
targets={
"HD-003-DESIGN-TEMPLATE-KIT":["hobbyregister","get_post_thumbnail","post_thumbnail","featured_image","hero_image","get_the_post_thumbnail","pftk_hobby","register_post_type","square","quadrat","rental_slot","werbe","amazon","logo"],
"HD-007-HOBBYREGISTER-CORE":["register_post_type","hobbyregister","register_single","get_post_thumbnail","post_thumbnail","featured_image","hero_image","hobby","register", "uge_term","shortcode"],
"HD-009-AFFILIATE-ZENTRALE":["hobbyregister","glossary_single","overview_wide_banner","hdar_launch","banner_distribution","Amazon","render_slot"],
}
report=[]
for plugin,keys in targets.items():
    zpath=base/plugin/"CURRENT.zip"
    report.extend(["### "+plugin,f"ZIP exists {zpath.exists()}"])
    if not zpath.exists():continue
    with zipfile.ZipFile(zpath) as z:
        names=z.namelist()
        report.append("ZIP files "+str(len(names)))
        for name in names:
            if "/assets/" in name and name.lower().endswith((".png",".webp",".jpg")):
                if any(t in name.lower() for t in ["logo","eigenwerbung","banner","malen","zeichnen","modellbau"]):
                    report.append("ASSET "+name+" "+str(z.getinfo(name).file_size))
        for name in names:
            if not name.lower().endswith(".php"):continue
            raw=z.read(name)
            if len(raw)>2200000:continue
            s=raw.decode("utf-8","replace").splitlines()
            hits=[(i+1,line) for i,line in enumerate(s) if any(k.lower() in line.lower() for k in keys)]
            if not hits:continue
            report.append("FILE "+name+" bytes "+str(len(raw))+" hits "+str(len(hits)))
            high= [h for h in hits if re.search(r"(register_post_type|get_post_thumbnail|post_thumbnail|hero_image|rental_slot|register_single|hobbyregister|uge_term|render_slot|glossary_single|render_affiliate)",h[1], re.I)]
            high=high[:85] if high else hits[:20]
            report.extend(f" {i}: {line[:260]}" for i,line in high)
out=Path("protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/PLUGINS/PLUGIN_AKTEN/HD-009-AFFILIATE-ZENTRALE/EVIDENCE/BANNER_CI_EXISTING_CODE_AUDIT.txt")
out.write_text("\n".join(report),encoding="utf8")
print("AUDIT",len(report),"lines",out,hashlib.sha256(out.read_bytes()).hexdigest())

# Exact HD007 image-entry return shape and route layout; no assumptions.
regzip=base/"HD-007-HOBBYREGISTER-CORE"/"CURRENT.zip"
with zipfile.ZipFile(regzip) as z:
    for file in ("hd-hobbyregister-core/includes/class-hd-hobbyregister-core.php",
                 "hd-hobbyregister-core/includes/class-hd-hobbyregister-frontend.php"):
        c=z.read(file).decode("utf8","replace")
        for token in ("function image_entry(", "function route(", "function render_profile("):
            i=c.find(token)
            if i>=0:
                out.write_text(out.read_text(encoding="utf8")+"\n\nHD007 EXCERPT "+file+" "+token+"\n"+c[max(0,i-130):i+2450],encoding="utf8")

with zipfile.ZipFile(regzip) as z:
    core=z.read("hd-hobbyregister-core/includes/class-hd-hobbyregister-core.php").decode("utf8","replace")
    front=z.read("hd-hobbyregister-core/includes/class-hd-hobbyregister-frontend.php").decode("utf8","replace")
    for name,body,tokens in [
        ("image_map",core,["function image_map(","function records("]),
        ("image_entry_use",front,["$entry=HD_Hobbyregister_Core_Stable127::image_entry"])
    ]:
        for token in tokens:
            i=body.find(token)
            if i>=0:out.write_text(out.read_text(encoding="utf8")+"\n\nMORE HD007 "+name+" "+token+"\n"+body[max(0,i-120):i+2350],encoding="utf8")
    for n in z.namelist():
        if n.endswith(".json") and any(t in n for t in ("image","map","portraits")) and z.getinfo(n).file_size<3000000:
            out.write_text(out.read_text(encoding="utf8")+"\n\nHD007 IMAGE JSON "+n+"\n"+z.read(n).decode("utf8","replace")[:1350],encoding="utf8")


import json
with zipfile.ZipFile(regzip) as z:
    m=json.loads(z.read("hd-hobbyregister-core/data/hobby-image-map-v1.json"))
    records=json.loads(z.read("hd-hobbyregister-core/data/hobby-register-v1.json")) if "hd-hobbyregister-core/data/hobby-register-v1.json" in z.namelist() else {}
    sample=[]
    for id in ("hobby:airbrush-modellbau","hobby:modellbau","hobby:malen","hobby:acrylmalerei","hobby:air-dry-clay"):
        entry=m.get(id)
        sample.append((id,entry))
    out.write_text(out.read_text(encoding="utf8")+"\n\nREAL HD007 IMAGE MAP SAMPLES:\n"+json.dumps(sample,ensure_ascii=False,indent=2),encoding="utf8")
