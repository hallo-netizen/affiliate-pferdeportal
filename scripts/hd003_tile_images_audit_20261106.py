from pathlib import Path
from collections import Counter
from zipfile import ZipFile
import json,re,hashlib
root=Path("protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/PLUGINS/ISOLIERTE_PLUGINS")
p=root/"HD-003-DESIGN-TEMPLATE-KIT/CURRENT.zip"
assert p.is_file()
print("HD003_BYTES",p.stat().st_size,"SHA256",hashlib.sha256(p.read_bytes()).hexdigest(),flush=True)
with ZipFile(p) as z:
    bad=z.testzip()
    print("ZIP_CRC",bad or "PASS", "FILES",len(z.namelist()),flush=True)
    images=[i for i in z.infolist() if i.filename.lower().endswith((".webp",".jpg",".jpeg",".png",".avif",".gif"))]
    print("DESIGN_IMAGES",len(images),"UNIQUE_NAMES",len({Path(i.filename).name for i in images}),flush=True)
    print("DESIGN_BY_IMAGE_FOLDER_3",Counter("/".join(i.filename.split("/")[:3]) for i in images).most_common(28),flush=True)
    print("DESIGN_BY_IMAGE_FOLDER_4",Counter("/".join(i.filename.split("/")[:4]) for i in images).most_common(35),flush=True)
    wanted=("sportdrachen","spielkarten","tarot","modellauto","mineral","fossil","meteorit","reklame","filmplakat","blechschild","werkzeug","rc-")
    for item in wanted:
        found=[i.filename for i in images if item in i.filename.lower()]
        print("MOTIF",item,"MATCHES",len(found),"EXAMPLES",found[:5],flush=True)
    php=[(i.filename,z.read(i).decode("utf8","replace")) for i in z.infolist() if i.filename.endswith(".php")]
    print("PHP_FILES",len(php),flush=True)
    pats=[r'get_term_meta',r'thumbnail_id',r'term_image',r'category.image',r'kachel',r'picture',r'hero',r'wp_get_attachment_image',r'assets/hobby-depot',r'file_exists\(']
    for pat in pats:
        counts=[(f,len(re.findall(pat,txt,re.I))) for f,txt in php]
        print("PHP_PATTERN",pat,sorted([x for x in counts if x[1]],key=lambda x:-x[1])[:5],flush=True)
    for f,txt in php:
        for i,line in enumerate(txt.splitlines()):
            if re.search(r'Sportdrachen|Spielkarten|Tarotdecks|Kachelfoto|Kategoriebild',line,re.I):
                print("PHP_HIT",f,"LINE",i+1,"TEXT",line.strip()[:330],flush=True)
    # asset naming patterns and likely theme images
    print("SAMPLE_THEME_IMAGE_PATHS",[i.filename for i in images if re.search(r'(hobby-depot|sportdrachen|kachel|category|hero)',i.filename,re.I)][:85],flush=True)
    print("SAMPLE_ALL_IMAGES",[i.filename for i in images][:35],flush=True)

# The HD-007 hobbyregister master status is distinct from page category tiles.
p=root/"HD-007-HOBBYREGISTER-CORE/CURRENT.zip"
if p.exists():
    with ZipFile(p) as z:
        found=[x for x in z.namelist() if x.endswith("hobby-image-production-status-v1.json")]
        if found:
            data=json.loads(z.read(found[0]))
            print("HD007_STATUS_STRUCTURE",type(data).__name__,list(data.keys())[:20] if isinstance(data,dict) else "list",flush=True)
            print("HD007_STATUS_BYTES",len(z.read(found[0])),flush=True)


# Additional mapping audit: which images are used and how category ownership is resolved.
with ZipFile(root/"HD-003-DESIGN-TEMPLATE-KIT/CURRENT.zip") as z:
    name="affiliate-portal-template-kit/includes/class-hobby-depot-profile-v150709.php"
    lines=z.read(name).decode("utf8","replace").splitlines()
    for i,l in enumerate(lines,1):
        if re.search(r'hobby-masters|hero-masters|subcategories/|bildarchiv|category_image|category.*image.*map|image.*map.*category|thumbnail_id',l,re.I):
            print("MAPPING_HIT",i,l.strip()[:370],flush=True)
    for a,b in [(4600,4760)]:
        for j in range(a,min(b,len(lines))+1):
            print("MAPPING_SOURCE",j,lines[j-1][:250],flush=True)
with ZipFile(root/"HD-007-HOBBYREGISTER-CORE/CURRENT.zip") as z:
    name=[x for x in z.namelist() if x.endswith("hobby-image-production-status-v1.json")][0]
    d=json.loads(z.read(name))
    print("REGISTER_SUMMARY",str(d.get("summary"))[:1000],flush=True)
    print("REGISTER_ITEM_COUNT",len(d.get("items",[])),flush=True)

with ZipFile(root/'HD-003-DESIGN-TEMPLATE-KIT/CURRENT.zip') as z:
    code=z.read('affiliate-portal-template-kit/includes/class-hobby-depot-profile-v150709.php').decode('utf8','replace').splitlines()
    for j in range(4751,4822): print('CATEGORY_BINDING',j,code[j-1],flush=True)
