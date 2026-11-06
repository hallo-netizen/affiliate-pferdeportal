from pathlib import Path
from collections import Counter,defaultdict
from zipfile import ZipFile
import hashlib,re,json,os
base=Path('protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/PLUGINS/ISOLIERTE_PLUGINS')
p=base/'HD-003-DESIGN-TEMPLATE-KIT/CURRENT.zip'
with ZipFile(p) as z:
 files=[x for x in z.infolist() if x.filename.lower().endswith(('.webp','.png','.jpg','.jpeg','.avif','.gif'))]
 sha=defaultdict(list)
 for x in files: sha[hashlib.sha256(z.read(x)).hexdigest()].append(x.filename)
 print('TOTAL_IMAGE_FILES',len(files),'DISTINCT_IMAGE_BYTES',len(sha),'EXTRA_EXACT_COPIES',len(files)-len(sha),flush=True)
 groups=Counter('hobby-depot-v150617/subcategories' if '/subcategories/' in x.filename else 'hobby-depot-v150617/hero-masters' if '/hero-masters-v150684/' in x.filename else 'hobby-masters' if '/hobby-masters/' in x.filename else 'bildarchiv' if '/bildarchiv/' in x.filename else 'other' for x in files)
 print('IMAGE_GROUPS',json.dumps(groups,ensure_ascii=False),flush=True)
 cat=[x for x in files if '/subcategories/' in x.filename]
 def slot(x):
  leaf=Path(x.filename).stem
  return (Path(x.filename).parent.name,re.sub(r'-v\d+$','',leaf))
 slot_counts=Counter(slot(x) for x in cat)
 print('CATEGORY_STORED_FILES',len(cat),'CATEGORY_UNIQUE_SLOTS',len(slot_counts),'CATEGORY_VERSIONS_HISTOGRAM',sorted(Counter(slot_counts.values()).items()),flush=True)
 print('CATEGORY_SLOT_EXAMPLES',slot_counts.most_common(14),flush=True)
 masters=[x for x in files if '/hero-masters-v150684/' in x.filename]
 print('CATEGORY_HERO_MASTERS',len(masters),'UNIQUE_SLUGS',len(set(Path(x.filename).stem for x in masters)),flush=True)
 hobbys=[x for x in files if '/hobby-masters/' in x.filename]
 print('HOBBY_MASTERS_FILES',len(hobbys),'HOBBY_MASTERS_UNIQUE_SLUGS',len(set(Path(x.filename).stem for x in hobbys)),flush=True)
 archive=[x for x in files if '/bildarchiv/' in x.filename]
 print('BILDARCHIV_FILES',len(archive),'SAMPLE_PATHS',[x.filename for x in archive[:16]],flush=True)
 print('EXACT_DUPLICATE_GROUPS',sum(len(a)>1 for a in sha.values()),'TOP_DUPLICATES',[v[:5] for v in sorted(sha.values(),key=len,reverse=True)[:10] if len(v)>1],flush=True)
 print('IMAGE_EXTENSION_COUNTS',Counter(Path(x.filename).suffix.lower() for x in files),flush=True)
 print('HOBBY_MASTERS_BY_VERSION',Counter(x.filename.split('/hobby-masters/')[0].split('/')[-1] for x in hobbys),flush=True)
