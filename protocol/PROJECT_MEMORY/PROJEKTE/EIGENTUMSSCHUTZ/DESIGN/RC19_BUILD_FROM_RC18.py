from pathlib import Path
from zipfile import ZipFile
import json, io, hashlib, os

path=Path("protocol/PROJECT_MEMORY/PROJEKTE/EIGENTUMSSCHUTZ/PLUGINS/ISOLIERTE_PLUGINS/HAB-001-DESIGN/CURRENT.zip")
data=path.read_bytes()
sha=lambda x:hashlib.sha256(x).hexdigest()
assert sha(data)=="def9ceb5a99eb965aa55805038d92e93e53747191786edc9f44fe74bbe560a7e", "Official design Current changed: abort"
prefix="hab-bewahr-design-vorschau/"
before={
 "includes/world-layout.php":"aff57bfde7e831fbadcb1a2e9d561bc8ad63167ed9649fcaa6d42cbf05325ef4",
 "data/area-photo-identities.json":"19204800af85b683ccf00600aea667bfb2888f3b7f450a8ebdd75ebb52441dad",
 "assets/style.css":"fa8205eddf08a408dc1f1362937ebd5c18e073bf376b58a4ab2c963176ac807b",
 "assets/area-prototype.css":"c976d1a6189af562847a88aa017a827ef166d7473a303fd75897520a07cc4286",
 "assets/detail-categories.css":"729371e8be0171fdd33e514ef53418650ca128ea5af82be55898bd6e54afd99f",
 "hab-bewahr-design-vorschau.php":"256f59f723d444e3e318f4ff28c33cdf235b828a2e1f27b7b2ed0fbc606d8e01"
}
after={
 "includes/world-layout.php":"21ee18315316cbafdb5dba0fba61907869ff7a5f926e6415eb488e21f2b8a776",
 "data/area-photo-identities.json":"8dbec3e195cf96210b4546e133292bfdcc33dc86d561167934d354f274d2fc99",
 "assets/style.css":"5c28b11ae081fe5b7549e6c2f9b68269f28adc3022a32ddee69174772d426710",
 "assets/area-prototype.css":"87afb43cdab2aba95e8885cae2f1b0bc14f59599eb42759f01c4db82b686b4cf",
 "assets/detail-categories.css":"cc1d9f45c1350579544aaf4c4e54b41c5249a7e6a3b5b952a145c5178097a8d3",
 "hab-bewahr-design-vorschau.php":"fbca1e8be62dbf6a7e6c2406951508c75a398d6edf20053b4c2715ba699dc9d0"
}
with ZipFile(io.BytesIO(data)) as src:
 assert src.testzip() is None and len(src.namelist())==432
 entries={i.filename:src.read(i.filename) for i in src.infolist()}
 for p,expected in before.items(): assert sha(entries[prefix+p])==expected,("Unexpected source file",p)
 p=prefix+"includes/world-layout.php";s=entries[p].decode()
 old="'Gebäude & Ausstattung'=>'curated-20261019-16.webp'"
 assert s.count(old)==1
 entries[p]=s.replace(old,"'Gebäude & Ausstattung'=>'topic-62-innenwand-vandalismus.webp'").encode()
 p=prefix+"data/area-photo-identities.json";obj=json.loads(entries[p])
 assert obj["curated-20261019-16.webp"]=="curated-20261019-16.webp"
 obj["curated-20261019-16.webp"]="fix-130-vandal-fassade.webp"
 entries[p]=(json.dumps(obj,ensure_ascii=False,indent=2)+"\n").encode()
 world_css="""
/* RC19: mobile category-world heroes: keep the approved desktop hero unchanged.
 * The original mobile 90deg wash covered the ENTIRE narrow photo. A short,
 * top-only fade protects the headline; the lower image remains clear. */
@media (max-width:760px){
 .hbdp-world-page .hbdp-world-hero{height:clamp(252px,78vw,320px)!important;min-height:252px;overflow:hidden}
 .hbdp-world-page .hbdp-world-hero-image{width:100%;height:100%;max-width:none;object-fit:cover;object-position:60% 52%;filter:none!important;image-rendering:auto}
 .hbdp-world-page .hbdp-world-hero--light .hbdp-world-hero-shade{background:linear-gradient(180deg,rgba(250,250,248,.97) 0%,rgba(250,250,248,.94) 27%,rgba(250,250,248,.66) 44%,rgba(250,250,248,.10) 67%,rgba(250,250,248,0) 82%)!important}
 .hbdp-world-page .hbdp-world-hero--dark .hbdp-world-hero-shade{background:linear-gradient(180deg,rgba(9,23,29,.95) 0%,rgba(9,23,29,.88) 27%,rgba(9,23,29,.62) 44%,rgba(9,23,29,.09) 67%,rgba(9,23,29,0) 82%)!important}
 .hbdp-world-page .hbdp-world-hero-inner{justify-content:flex-start;align-items:flex-start;width:100%;height:100%;padding:19px 19px 8px;min-width:0}
 .hbdp-world-page .hbdp-world-hero h1{font-size:clamp(27px,7.5vw,39px);line-height:1.12;max-width:100%;overflow-wrap:break-word;margin:7px 0}
 .hbdp-world-page .hbdp-world-hero p{font-size:clamp(12px,3.3vw,14px);line-height:1.4;max-width:100%;margin:3px 0}
}
"""
 entries[prefix+"assets/style.css"]+=world_css.encode()
 area_css="""
/* RC19: consistent sharp mobile area and R3 category heroes, no desktop change.
 * Previous 90deg fade had >30% solid overlay even on the far right side. */
@media (max-width:760px){
 .hbdp-area-page .hbdp-area-demo-hero,.hbdp-r3-page .hbdp-area-demo-hero{height:clamp(255px,80vw,330px)!important;min-height:255px;overflow:hidden}
 .hbdp-area-page .hbdp-area-demo-hero>img,.hbdp-r3-page .hbdp-area-demo-hero>img{display:block;width:100%;height:100%;max-width:none;object-fit:cover!important;object-position:62% 51%!important;filter:none!important;image-rendering:auto}
 .hbdp-area-page .hbdp-area-demo-shade,.hbdp-r3-page .hbdp-area-demo-shade{background:linear-gradient(180deg,rgba(249,250,248,.97) 0%,rgba(249,250,248,.93) 27%,rgba(249,250,248,.68) 44%,rgba(249,250,248,.10) 68%,rgba(249,250,248,0) 83%)!important}
 .hbdp-area-page .hbdp-area-demo-hero-text,.hbdp-r3-page .hbdp-area-demo-hero-text{display:flex;justify-content:flex-start;align-items:flex-start;width:100%;height:100%;padding:20px 18px 8px!important;min-width:0;box-sizing:border-box}
 .hbdp-area-page .hbdp-area-demo-hero h1,.hbdp-r3-page .hbdp-area-demo-hero h1{font-size:clamp(27px,7.4vw,38px);line-height:1.12;max-width:100%;overflow-wrap:break-word;margin:7px 0}
 .hbdp-area-page .hbdp-area-demo-hero p,.hbdp-r3-page .hbdp-area-demo-hero p{font-size:clamp(12px,3.3vw,14px);line-height:1.4;white-space:normal;max-width:100%;margin:3px 0}
}
"""
 entries[prefix+"assets/area-prototype.css"]+=area_css.encode()
 font_css="""
/* RC19: one actual text size for the visible and expanded top introductions.
 * Applies to every WordPress leaf category and R3, only on phones. */
@media (max-width:760px){
 .hbdp-detail-category .hbdp-detail-intro .hbdp-detail-lead,
 .hbdp-detail-category .hbdp-detail-intro .hbdp-detail-expansion,
 .hbdp-detail-category .hbdp-detail-intro .hbdp-detail-expansion p{
   font-size:16px!important;
   line-height:1.72!important;
   font-weight:400;
   letter-spacing:normal;
 }
}
"""
 entries[prefix+"assets/detail-categories.css"]+=font_css.encode()
 p=prefix+"hab-bewahr-design-vorschau.php";s=entries[p].decode()
 assert s.count("Version: 0.1.191")==1 and s.count("'0.1.191'")==3
 entries[p]=s.replace("Version: 0.1.191","Version: 0.1.192").replace("'0.1.191'","'0.1.192'").encode()
 assert prefix+"assets/topic-62-innenwand-vandalismus.webp" in entries
 for key,expected in after.items(): assert sha(entries[prefix+key])==expected,("Release content mismatch",key,sha(entries[prefix+key]))
 buf=io.BytesIO()
 with ZipFile(buf,"w") as out:
  for info in src.infolist():out.writestr(info,entries[info.filename])
 result=buf.getvalue()
 with ZipFile(io.BytesIO(result)) as z:assert z.testzip() is None and len(z.namelist())==432
 path.write_bytes(result)
 print("HAB DESIGN RC19",len(result),"SHA",sha(result),"432 entries; exactly 6 original files modified")
