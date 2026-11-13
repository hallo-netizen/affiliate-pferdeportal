#!/usr/bin/env python3
"""Minimal HD003 1.50.815: show an honest, compact, logged-in-only product placement hint.
No fake product cards and absolutely no change to public zero-product output.
"""
from pathlib import Path
from zipfile import ZipFile
import hashlib,io,sys
p=Path('protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/PLUGINS/ISOLIERTE_PLUGINS/HD-003-DESIGN-TEMPLATE-KIT/CURRENT.zip')
sha=lambda x:hashlib.sha256(x).hexdigest()
expected='263284e057b9c2a3cc57cc4807301ab2e74c1daeae8dfeb0a16191c49a9dc18f'
assert sha(p.read_bytes())==expected,'Original HD003 1.50.814 must remain untouched'
profile='affiliate-portal-template-kit/includes/class-hobby-depot-profile-v150709.php'
main='affiliate-portal-template-kit/pferde-template-kit.php'
with ZipFile(p) as z:
    assert z.testzip() is None and len(z.namelist())==1291
    infos=z.infolist();data={e.filename:z.read(e.filename) for e in infos}
s=data[profile].decode()
a=s.index('    private static function render_category_level_product_row_v150687(')
b=s.index('    private static function direct_child_category_ids_v150687(',a)
block=s[a:b]
assert block.count("if (!$cards) { return ''; }")==1
block=block.replace(
    "if (!$cards) { return ''; }",
    """if (!$cards) {
            if (!self::logged_in_preview()) { return ''; }
            // This is NOT a merchandise card, and must never be rendered
            // publicly. Keep the area identifiable for the logged-in editor.
            return '<section class="hd-portal-section hd-catlevel-products hd-admin-product-preview"><header><span>Vorschau</span><h2>Empfehlungen</h2></header><p class="hd-admin-product-slot-note">Drei Produktplätze sind derzeit frei. Noch keine passenden Produkte zugeordnet. Nur für angemeldete Benutzer sichtbar.</p></section>';
        }""",1)
s=s[:a]+block+s[b:]
css=r'''
/* HD003 1.50.815: restrained admin-only empty product placement note,
   never three full-height fake item cards. */
.hd-content-v150616 .hd-portal-section.hd-admin-product-preview{
  min-height:0!important;height:auto!important;max-height:none!important;
  margin-top:16px!important;margin-bottom:18px!important;
}
.hd-content-v150616 .hd-admin-product-slot-note{
  display:block!important;box-sizing:border-box!important;
  margin:8px 0 0!important;padding:12px 14px!important;
  background:#EFE6DA!important;border:1px dashed #B4A894!important;
  color:#36494A!important;font-size:13px!important;line-height:1.5!important;
  width:100%!important;height:auto!important;min-height:0!important;
}
/* End HD003 1.50.815 editor-only placement hint. */
'''
marker='/* End HD003 1.50.813 category card design. */'
assert s.count(marker)==1
s=s.replace(marker,marker+'\n'+css,1)
data[profile]=s.encode()
head=data[main].decode()
assert '1.50.814' in head
data[main]=head.replace('1.50.814','1.50.815').encode()
with ZipFile(p) as z:
    diff=[k for k in data if data[k]!=z.read(k)]
    assert set(diff)=={profile,main},diff
b=io.BytesIO()
with ZipFile(b,'w') as z:
    for entry in infos:z.writestr(entry,data[entry.filename])
out=Path(sys.argv[1])
out.parent.mkdir(parents=True,exist_ok=True)
out.write_bytes(b.getvalue())
with ZipFile(out) as z:
    assert z.testzip() is None and len(z.namelist())==1291 and b'1.50.815' in z.read(main)
print('HD003_150815_SHA',sha(out.read_bytes()),'BYTES',out.stat().st_size)
print('DIFF_ONLY_TWO_EXISTING_FILES',diff)
