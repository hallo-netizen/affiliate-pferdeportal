#!/usr/bin/env python3
"""HD003 1.50.811: category recommendation card layout and one ad label.
Built only from exact 1.50.810 complete plugin; no unrelated changes.
"""
import hashlib,io,sys
from pathlib import Path
from zipfile import ZipFile
base=Path('protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/PLUGINS/ISOLIERTE_PLUGINS/HD-003-DESIGN-TEMPLATE-KIT')
source=base/'CURRENT.zip'
sha=lambda b:hashlib.sha256(b).hexdigest()
expected='d63c2c7413f1f3d8ac635abffd3ec7ea69ea0fddff5b4fc6dd4e676ac9c7b1c6'
assert sha(source.read_bytes())==expected,'HD003 1.50.810 source differs'
out=Path(sys.argv[1] if len(sys.argv)>1 else '/tmp/HOBBY_DEPOT_DESIGN_HD003_1.50.811_PRODUKTKARTEN.zip')
with ZipFile(source) as z:
    assert len(z.namelist())==1291 and z.testzip() is None
    infos=z.infolist()
    files={i.filename:z.read(i.filename) for i in infos}
main='affiliate-portal-template-kit/pferde-template-kit.php'
profile='affiliate-portal-template-kit/includes/class-hobby-depot-profile-v150709.php'
code=files[profile].decode()
def once(t,before,after,label):
    assert t.count(before)==1,f'{label} requires 1 exact anchor, has {t.count(before)}'
    return t.replace(before,after,1)
code=once(code,
    """return '<section class="hd-portal-section hd-catlevel-products"><header><span>Anzeige · Partner</span><h2>Empfehlungen</h2></header><div class="hd-catlevel-product-grid">';""",
    """return '<section class="hd-portal-section hd-catlevel-products"><header><span>Anzeige</span><h2>Empfehlungen</h2></header><div class="hd-catlevel-product-grid">';""",
    "one ad disclosure above recommendations") if False else code
# Actual code is concatenated HTML at this exact line; replace just this one context string.
code=once(code,
    """<header><span>Anzeige · Partner</span><h2>Empfehlungen</h2></header><div class="hd-catlevel-product-grid">""",
    """<header><span>Anzeige</span><h2>Empfehlungen</h2></header><div class="hd-catlevel-product-grid">""",
    "one Anzeige header")

# The per-card labels have an accessible label in the original slot; visually hide
# just within this once-labeled category section. No other advertising disclosures
# on other page types are removed.
styles=r'''
/* HD003 1.50.811: Hobby category product recommendations – original 3/2/1 provider cards.
   Same 416px product slots as actual reference providers; not the historic 84px clipping.
   ONLY hd-catlevel-products; hero, rental ads, affiliate pages and footer unaffected. */
.hd-content-v150616 .hd-portal-section.hd-catlevel-products .hd-catlevel-product-grid{
  display:grid!important;grid-template-columns:repeat(3,minmax(0,1fr))!important;gap:14px!important;align-items:stretch!important;
}
.hd-content-v150616 .hd-portal-section.hd-catlevel-products .hd-next-partner-product{
  display:block!important;grid-column:auto!important;height:auto!important;min-height:416px!important;
  overflow:visible!important;background:#fff!important;border:1px solid rgba(63,71,75,.12)!important;
  border-radius:4px!important;box-shadow:none!important;
}
.hd-content-v150616 .hd-portal-section.hd-catlevel-products .hd-next-partner-label{
  display:none!important;
}
.hd-content-v150616 .hd-portal-section.hd-catlevel-products .hd-next-partner-content{
  display:block!important;width:100%!important;height:auto!important;min-height:416px!important;overflow:visible!important;
}
.hd-content-v150616 .hd-portal-section.hd-catlevel-products .hd-next-partner-product .ppar-affiliate-slot{
  width:100%!important;min-height:416px!important;max-height:none!important;overflow:visible!important;
}
.hd-content-v150616 .hd-portal-section.hd-catlevel-products .hd-next-partner-product .ppar-banner-link{
  width:100%!important;height:auto!important;min-height:360px!important;max-height:none!important;
  margin:0!important;padding:0 12px 14px!important;background:#fff!important;
}
.hd-content-v150616 .hd-portal-section.hd-catlevel-products .hd-next-partner-product .ppar-banner-image-wrap{
  min-height:155px!important;background:#fff!important;
}
.hd-content-v150616 .hd-portal-section.hd-catlevel-products .hd-next-partner-product img.ppar-banner-image{
  max-width:150px!important;max-height:150px!important;object-fit:contain!important;
}
.hd-content-v150616 .hd-portal-section.hd-catlevel-products .hd-next-partner-product .ppar-banner-text{
  width:100%!important;height:auto!important;min-height:145px!important;
  overflow:visible!important;padding:14px 12px!important;align-items:stretch!important;
}
.hd-content-v150616 .hd-portal-section.hd-catlevel-products .hd-next-partner-product .ppar-banner-title{
  font-size:14px!important;line-height:1.35!important;max-height:none!important;
}
.hd-content-v150616 .hd-portal-section.hd-catlevel-products .hd-next-partner-product .ppar-banner-price{
  font-size:13px!important;line-height:1.4!important;
}
@media(max-width:960px){
 .hd-content-v150616 .hd-portal-section.hd-catlevel-products .hd-catlevel-product-grid{
   grid-template-columns:repeat(2,minmax(0,1fr))!important;
 }
}
@media(max-width:650px){
 .hd-content-v150616 .hd-portal-section.hd-catlevel-products .hd-catlevel-product-grid{
   grid-template-columns:minmax(0,1fr)!important;
 }
}
/* End scoped HD003 recommendations. */
'''
# Insert before original catlevel rule, and never disturb existing responsive rules.
marker='.hd-content-v150616 .hd-catlevel-products{margin-top:16px!important}'
code=once(code,marker,styles+marker,'scoped catlevel CSS')
files[profile]=code.encode()
head=files[main].decode()
assert '1.50.810' in head,'Original plugin not 1.50.810'
head=head.replace('1.50.810','1.50.811')
files[main]=head.encode()
with ZipFile(source) as z:
    diff=[n for n in files if files[n]!=z.read(n)]
    assert set(diff)=={main,profile},diff
out.parent.mkdir(parents=True,exist_ok=True)
b=io.BytesIO()
with ZipFile(b,'w') as z:
    for i in infos:z.writestr(i,files[i.filename])
out.write_bytes(b.getvalue())
with ZipFile(out) as z:
    assert len(z.namelist())==1291 and z.testzip() is None
    assert b'1.50.811' in z.read(main)
    assert b'<header><span>Anzeige</span><h2>Empfehlungen</h2>' in z.read(profile)
print('HD003_INPUT_SHA',expected,'HD003_811_SHA',sha(out.read_bytes()),'BYTES',out.stat().st_size)
print('DIFF_ONLY',diff,'1291_CRC_PASS')
