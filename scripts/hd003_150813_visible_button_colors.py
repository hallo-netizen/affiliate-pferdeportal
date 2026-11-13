#!/usr/bin/env python3
"""HD003 1.50.813 scoped color correction to actually visible warm beige and teal.
Only original HD003 category recommendation CSS; all other design unchanged.
"""
from pathlib import Path
from zipfile import ZipFile
import hashlib,io,sys
base=Path('protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/PLUGINS/ISOLIERTE_PLUGINS/HD-003-DESIGN-TEMPLATE-KIT/CURRENT.zip')
sha=lambda b:hashlib.sha256(b).hexdigest()
expected='1a5cad59bf033780abcc08f3ae70f7e7fbaf6a8c209d4cd97371e5828287dafc'
assert sha(base.read_bytes())==expected,'Unexpected HD003 CURRENT; refuse update'
main='affiliate-portal-template-kit/pferde-template-kit.php'
profile='affiliate-portal-template-kit/includes/class-hobby-depot-profile-v150709.php'
with ZipFile(base) as z:
    assert len(z.namelist())==1291 and z.testzip() is None
    infos=z.infolist();files={i.filename:z.read(i.filename) for i in infos}
s=files[profile].decode()
a=s.index('/* HD003 1.50.812: genuine product cards')
b=s.index('/* End HD003 1.50.812 category card design. */',a)+len('/* End HD003 1.50.812 category card design. */')
part=s[a:b]
assert part.count('background:#FAF8F4!important;')==1
assert part.count('color:#0f8f95!important;')==1
assert part.count('border:1px solid #b7d7d4!important;')==1
part=part.replace('background:#FAF8F4!important;', 'background:#EFDECA!important;')
part=part.replace('color:#0f8f95!important;', 'color:#00777D!important;')
part=part.replace('border:1px solid #b7d7d4!important;', 'border:1px solid #81AAA8!important;')
# Be explicit in one place, no !important duplications or new design system.
part=part.replace('/* HD003 1.50.812: genuine product cards','/* HD003 1.50.813: genuine product cards')
part=part.replace('/* End HD003 1.50.812 category card design. */','/* End HD003 1.50.813 category card design. */')
s=s[:a]+part+s[b:]
files[profile]=s.encode()
header=files[main].decode()
assert '1.50.812' in header
files[main]=header.replace('1.50.812','1.50.813').encode()
with ZipFile(base) as z:
    diff=[x for x in files if files[x]!=z.read(x)]
    assert set(diff)=={main,profile},diff
buf=io.BytesIO()
with ZipFile(buf,'w') as z:
    for info in infos:z.writestr(info,files[info.filename])
out=Path(sys.argv[1] if len(sys.argv)>1 else '/tmp/HOBBY_DEPOT_DESIGN_HD003_1.50.813_SICHTBARE_FARBEN.zip')
out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(buf.getvalue())
with ZipFile(out) as z:
    assert len(z.namelist())==1291 and z.testzip() is None
    assert b'1.50.813' in z.read(main)
print('BUILD_HD003_1.50.813',sha(out.read_bytes()),out.stat().st_size,'DIFF',diff)
