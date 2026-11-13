#!/usr/bin/env python3
"""HD003 1.50.812 – supplier card layout matching Pferde Atelier structure and HAB color style.
Only scoped existing category recommendation CSS changes. No other frontend.
"""
from pathlib import Path
from zipfile import ZipFile
import hashlib,io,sys
root=Path('protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/PLUGINS/ISOLIERTE_PLUGINS/HD-003-DESIGN-TEMPLATE-KIT')
p=root/'CURRENT.zip'
sha=lambda b:hashlib.sha256(b).hexdigest()
expected='3cc8118ed5d9d22acadfd2e9aa9184068f71cbe9ccb2574bcffacdd16d8ac6df'
assert sha(p.read_bytes())==expected,'Original HD003 version must be 1.50.811'
main='affiliate-portal-template-kit/pferde-template-kit.php'
profile='affiliate-portal-template-kit/includes/class-hobby-depot-profile-v150709.php'
with ZipFile(p) as z:
  assert len(z.namelist())==1291 and z.testzip() is None
  infos=z.infolist();files={i.filename:z.read(i.filename) for i in infos}
src=files[profile].decode()
marker='/* End scoped HD003 recommendations. */'
assert src.count(marker)==1
css=r'''
/* HD003 1.50.812: genuine product cards – explicit vertically stacked image,
   verified facts, price, and one or more affiliate buttons at the card bottom.
   All selectors are scoped to ONE already-labeled category recommendation group. */
.hd-content-v150616 .hd-portal-section.hd-catlevel-products .hd-catlevel-product-grid{
  display:grid!important;grid-template-columns:repeat(3,minmax(0,1fr))!important;
  gap:14px!important;align-items:stretch!important;
}
.hd-content-v150616 .hd-portal-section.hd-catlevel-products .hd-catlevel-product-grid .hd-next-partner-product{
  display:block!important;min-width:0!important;grid-column:auto!important;
  height:auto!important;min-height:438px!important;overflow:hidden!important;
  padding:0!important;background:#fff!important;
  border:1px solid rgba(63,71,75,.12)!important;border-radius:1px!important;
}
.hd-content-v150616 .hd-portal-section.hd-catlevel-products .hd-next-partner-label,
.hd-content-v150616 .hd-portal-section.hd-catlevel-products .ppar-affiliate-disclosure,
.hd-content-v150616 .hd-portal-section.hd-catlevel-products .ppar-affiliate-label{
  display:none!important;
}
.hd-content-v150616 .hd-portal-section.hd-catlevel-products .hd-next-partner-content,
.hd-content-v150616 .hd-portal-section.hd-catlevel-products .ppar-affiliate-slot{
  width:100%!important;height:100%!important;min-height:438px!important;
  max-height:none!important;overflow:visible!important;
}
.hd-content-v150616 .hd-portal-section.hd-catlevel-products .ppar-affiliate-content{
  grid-row:1 / span 2!important;align-self:stretch!important;
  display:block!important;width:100%!important;height:100%!important;
  min-height:438px!important;margin:0!important;padding:0!important;
}
.hd-content-v150616 .hd-portal-section.hd-catlevel-products .ppar-banner-link[data-ppar-category-product-card="1"]{
  display:grid!important;grid-template-columns:minmax(0,1fr)!important;
  width:100%!important;height:100%!important;min-height:438px!important;
  max-height:none!important;margin:0!important;padding:0 0 16px!important;
  align-items:stretch!important;background:#fff!important;
  text-decoration:none!important;overflow:visible!important;
}
.hd-content-v150616 .hd-portal-section.hd-catlevel-products .ppar-banner-image-wrap[data-ppar-category-product-image-frame]{
  display:flex!important;align-items:center!important;justify-content:center!important;
  margin:0 auto!important;padding:10px 0!important;background:#fff!important;
}
.hd-content-v150616 .hd-portal-section.hd-catlevel-products .ppar-banner-image[data-ppar-category-product-image-fit]{
  width:150px!important;height:150px!important;max-width:150px!important;max-height:150px!important;
  object-fit:contain!important;object-position:center center!important;
  border-radius:0!important;
}
.hd-content-v150616 .hd-portal-section.hd-catlevel-products .ppar-banner-text[data-ppar-category-product-text]{
  display:flex!important;flex-direction:column!important;align-items:stretch!important;
  justify-content:flex-start!important;box-sizing:border-box!important;
  height:100%!important;min-height:0!important;width:100%!important;
  padding:12px 18px 0!important;overflow:visible!important;
}
.hd-content-v150616 .hd-portal-section.hd-catlevel-products .ppar-banner-title{
  display:block!important;font-size:14px!important;line-height:1.4!important;
  max-height:none!important;white-space:normal!important;overflow:visible!important;
  font-weight:700!important;color:#17313c!important;
}
.hd-content-v150616 .hd-portal-section.hd-catlevel-products .ppar-product-facts{
  display:flex!important;flex-direction:column!important;
  gap:5px!important;width:100%!important;max-height:none!important;
  margin:12px 0 4px!important;overflow:visible!important;
}
.hd-content-v150616 .hd-portal-section.hd-catlevel-products .ppar-product-facts-heading{
  display:block!important;color:#17313c!important;font-size:12px!important;
  font-weight:750!important;line-height:1.35!important;
}
.hd-content-v150616 .hd-portal-section.hd-catlevel-products .ppar-product-fact{
  display:block!important;max-height:none!important;overflow:visible!important;
  font-size:12px!important;line-height:1.35!important;color:#52646c!important;
}
.hd-content-v150616 .hd-portal-section.hd-catlevel-products .ppar-banner-description{
  display:block!important;font-size:12px!important;line-height:1.35!important;
  max-height:54px!important;overflow:hidden!important;
}
.hd-content-v150616 .hd-portal-section.hd-catlevel-products .ppar-banner-meta{
  display:flex!important;gap:8px!important;align-items:center!important;
  margin:8px 0 10px!important;max-height:none!important;
}
.hd-content-v150616 .hd-portal-section.hd-catlevel-products .ppar-banner-price{
  font-size:13px!important;line-height:1.4!important;color:#17313c!important;
}
.hd-content-v150616 .hd-portal-section.hd-catlevel-products .ppar-banner-availability{
  display:none!important;
}
.hd-content-v150616 .hd-portal-section.hd-catlevel-products .ppar-banner-actions{
  display:flex!important;flex-direction:column!important;gap:7px!important;
  width:100%!important;margin-top:auto!important;
  max-height:none!important;overflow:visible!important;
}
.hd-content-v150616 .hd-portal-section.hd-catlevel-products .ppar-banner-actions .ppar-banner-offer-button,
.hd-content-v150616 .hd-portal-section.hd-catlevel-products .ppar-banner-text .ppar-banner-button{
  box-sizing:border-box!important;display:flex!important;align-items:center!important;justify-content:center!important;
  width:100%!important;min-height:34px!important;height:auto!important;
  padding:7px 10px!important;margin:0!important;
  border:1px solid #b7d7d4!important;border-radius:1px!important;
  background:#FAF8F4!important;color:#0f8f95!important;
  font-size:12px!important;font-weight:700!important;line-height:1.3!important;
  text-align:center!important;text-decoration:none!important;
  max-height:none!important;white-space:normal!important;overflow:visible!important;
}
.hd-content-v150616 .hd-portal-section.hd-catlevel-products .ppar-banner-text .ppar-banner-button{
  margin-top:auto!important;
}
.hd-content-v150616 .hd-portal-section.hd-catlevel-products .ppar-banner-actions .ppar-banner-offer-button:hover,
.hd-content-v150616 .hd-portal-section.hd-catlevel-products .ppar-banner-text .ppar-banner-button:hover{
  background:#e8f5f3!important;color:#086d72!important;border-color:#0f8f95!important;
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
/* End HD003 1.50.812 category card design. */
'''
src=src.replace(marker,marker+'\n'+css,1)
files[profile]=src.encode()
head=files[main].decode()
assert '1.50.811' in head
files[main]=head.replace('1.50.811','1.50.812').encode()
with ZipFile(p) as z:
 diff=[n for n in files if files[n]!=z.read(n)]
 assert set(diff)=={main,profile},diff
out=Path(sys.argv[1] if len(sys.argv)>1 else '/tmp/HOBBY_DEPOT_DESIGN_HD003_1.50.812_PRODUCT_KARTEN_VOLL.zip')
out.parent.mkdir(parents=True,exist_ok=True)
bio=io.BytesIO()
with ZipFile(bio,'w') as z:
 for i in infos:z.writestr(i,files[i.filename])
out.write_bytes(bio.getvalue())
with ZipFile(out) as z:
 assert z.testzip() is None and len(z.namelist())==1291
 assert b'1.50.812' in z.read(main)
print('HD003_150812_SHA',sha(out.read_bytes()),'BYTES',out.stat().st_size,'ONLY_CHANGED',diff)
