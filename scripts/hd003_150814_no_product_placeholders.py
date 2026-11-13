#!/usr/bin/env python3
"""HD003 1.50.814: remove fake product placeholders at their single source.

Exact byte-locked 1.50.813 full plugin; do not alter provider/real product
HTML, banners, any other placeholder type, the mobile design or affiliate feed.
"""
from pathlib import Path
from zipfile import ZipFile
import hashlib,io,sys
office=Path('protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/PLUGINS/ISOLIERTE_PLUGINS/HD-003-DESIGN-TEMPLATE-KIT')
src=office/'CURRENT.zip'
sha=lambda b:hashlib.sha256(b).hexdigest()
oldhash='5fb7053f31d705b9c2001fbcdfecf518c05d8c1fe52283f058943ca48f6eba73'
assert sha(src.read_bytes())==oldhash,'Cannot patch unexpected HD003 version'
path='affiliate-portal-template-kit/includes/class-hobby-depot-profile-v150709.php'
main='affiliate-portal-template-kit/pferde-template-kit.php'
with ZipFile(src) as z:
    assert z.testzip() is None and len(z.namelist())==1291
    infos=z.infolist()
    files={i.filename:z.read(i.filename) for i in infos}
content=files[path].decode('utf8')
def single(old,new,desc):
    global content
    n=content.count(old)
    assert n==1,f'{desc}: expected single exact occurrence, found {n}'
    content=content.replace(old,new,1)
# Root cause: a missing shortcode result gets converted to a fake card *solely*
# when the editor is logged in. Never create product cards from absence.
single(
    "if($html==='' && self::logged_in_preview()){$html=self::affiliate_preview_placeholder('Affiliate-Produkt',$slot);$preview=$html!=='';}",
    "if($html===''){continue;}",
    "inline product slots – suppress false logged-in preview before arrays are populated"
)
# Same legacy problem on homepage product grid, no need to burden site with fake
# merchandise on any path. Banner / editorial placeholders stay unchanged.
single(
    "if ($html === '') { $html = self::affiliate_preview_placeholder('product', $slot); }",
    "if ($html === '') { continue; }",
    "legacy homepage product slots"
)
single(
    "$note = self::logged_in_preview() ? '<span class=\"hd-admin-preview-note\">Leere Produktplätze siehst du nur im eingeloggten Zustand.</span>' : '';",
    "$note = '';",
    "do not claim that logged in users see non-existent product slots"
)
files[path]=content.encode('utf8')
head=files[main].decode('utf8')
assert '1.50.813' in head
files[main]=head.replace('1.50.813','1.50.814').encode('utf8')
with ZipFile(src) as z:
    diff=[n for n in files if files[n]!=z.read(n)]
    assert set(diff)=={main,path},diff
out=Path(sys.argv[1] if len(sys.argv)>1 else '/tmp/HOBBY_DEPOT_DESIGN_HD003_1.50.814_OHNE_LEERKARTEN.zip')
out.parent.mkdir(parents=True,exist_ok=True)
buf=io.BytesIO()
with ZipFile(buf,'w') as z:
    for info in infos:z.writestr(info,files[info.filename])
out.write_bytes(buf.getvalue())
with ZipFile(out) as z:
    assert len(z.namelist())==1291 and z.testzip() is None
    assert b'1.50.814' in z.read(main)
print('HD003_150814_SHA',sha(out.read_bytes()),'BYTES',out.stat().st_size)
print('ONLY_VERSION_AND_EXISTING_PRODUCT_PROFILE_CHANGED',diff)
