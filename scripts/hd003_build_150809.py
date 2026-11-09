#!/usr/bin/env python3
"""HD003 1.50.809: only mobile category-intro font unification; preserve Hobbyfinder output."""
from pathlib import Path
import zipfile, hashlib, subprocess, tempfile, json, re
ROOT = Path(__file__).resolve().parents[1]
OFFICE = ROOT/'protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/PLUGINS/ISOLIERTE_PLUGINS/HD-003-DESIGN-TEMPLATE-KIT'
SRC = OFFICE/'HOBBY_DEPOT_DESIGN_HD003_1.50.808.zip'
OUT = ROOT/'dist/HOBBY_DEPOT_DESIGN_HD003_1.50.809_MOBILE_14PX.zip'
ORIGINAL_SHA = 'cbf03e54dd7bf4ae44ea6beac66f1ee53d188732d6da4b6c1c92df1b9b5b8f15'
ENTRY = 'affiliate-portal-template-kit/pferde-template-kit.php'
PROFILE = 'affiliate-portal-template-kit/includes/class-hobby-depot-profile-v150709.php'
assert SRC.is_file(), str(SRC)
assert hashlib.sha256(SRC.read_bytes()).hexdigest() == ORIGINAL_SHA, 'incorrect 1.50.808 starting ZIP'
assert (OFFICE/'CURRENT.zip').read_bytes() == SRC.read_bytes(), 'current archive differs from verified original'
original_bytes = {}
anchor = '  .hd-content-v150616 .hd-catlevel-lead,.hd-content-v150616 .hd-catlevel-more p{font-size:14px!important;line-height:1.52!important}'
addition = '''
  /* 1.50.809: mobile only; align visible category intro and expanded intro at exactly 14px across hub2/leaf/special pages. */
  .hd-content-v150616 .hd-hub2-longcopy-benchmark-v150698 .hd-hub2-longcopy-lead,
  .hd-content-v150616 .hd-hub2-longcopy-benchmark-v150698 .hd-hub2-longcopy-lead>p,
  .hd-content-v150616 .hd-hub2-longcopy-benchmark-v150698 .hd-hub2-more>div>p,
  .hd-content-v150616 .hd-catlevel-intro .hd-catlevel-lead,
  .hd-content-v150616 .hd-catlevel-intro .hd-catlevel-more>div>p,
  .hd-content-v150616 .hd-catlevel-intro.hd-catlevel-intro-schuhmacherei-v150695 .hd-catlevel-lead,
  .hd-content-v150616 .hd-catlevel-intro.hd-ketten-faq-pilot-v150746 .hd-catlevel-lead{font-size:14px!important}
'''
with zipfile.ZipFile(SRC) as source:
    assert source.testzip() is None
    assert len(source.namelist()) == 1291
    assert ENTRY in source.namelist() and PROFILE in source.namelist()
    original_entry = source.read(ENTRY).decode('utf-8')
    original_profile = source.read(PROFILE).decode('utf-8')
    assert original_profile.count(anchor) == 1
    # The anchor is inside the EXISTING max-width:760px block. Never touch desktop or unrelated CSS.
    i = original_profile.index(anchor)
    before = original_profile[:i]
    tail = original_profile[i:i+len(anchor)+700]
    assert '@media(max-width:760px){' in before[-1300:]
    assert '\n}' not in tail[:len(anchor)+120], 'anchor not inside selected mobile media'
    assert 'hd-hf-visual img{display:block' in original_profile, 'Hobbyfinder image output altered unexpectedly'
    assert 'function resultVisual(h){return h.image?' in original_profile
    assert '.hd-hf-choices,.hd-hf-grid{grid-template-columns:1fr}' in original_profile
    altered_profile = original_profile.replace(anchor, anchor + '\n' + addition, 1)
    assert altered_profile.replace(anchor + '\n' + addition, anchor, 1) == original_profile
    assert re.search(r'Version:\s*1\.50\.808\b', original_entry)
    altered_entry = original_entry.replace('1.50.808','1.50.809')
    assert altered_entry != original_entry
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(OUT,'w') as output:
        for item in source.infolist():
            data = source.read(item.filename)
            if item.filename == ENTRY:
                data = altered_entry.encode('utf-8')
            elif item.filename == PROFILE:
                data = altered_profile.encode('utf-8')
            output.writestr(item, data)
with zipfile.ZipFile(SRC) as prev, zipfile.ZipFile(OUT) as current:
    assert current.testzip() is None, 'invalid new archive'
    assert current.namelist() == prev.namelist(), 'new ZIP lost or added items'
    changed = [n for n in prev.namelist() if prev.read(n) != current.read(n)]
    assert sorted(changed) == sorted([ENTRY, PROFILE]), changed
    assert current.read(PROFILE).decode('utf-8').count('1.50.809: mobile only') == 1
    assert current.read(PROFILE).decode('utf-8').replace(anchor + '\n' + addition, anchor,1) == original_profile
    assert '<div class="hd-hf-grid">' in original_profile
    assert current.read(PROFILE).decode('utf-8').count('function resultVisual(h)') == original_profile.count('function resultVisual(h)')
    phps=[n for n in current.namelist() if n.endswith('.php')]
    assert len(phps) == 13
    with tempfile.TemporaryDirectory() as td:
        for i, name in enumerate(phps):
            pp=Path(td)/f'{i}.php'
            pp.write_bytes(current.read(name))
            q=subprocess.run(['php','-l',str(pp)],capture_output=True,text=True)
            assert q.returncode == 0,(name,q.stdout,q.stderr)
report={
 'version':'1.50.809', 'source_version':'1.50.808',
 'file':str(OUT),'size_bytes':OUT.stat().st_size,
 'sha256':hashlib.sha256(OUT.read_bytes()).hexdigest(),
 'source_sha256':ORIGINAL_SHA,
 'files':1291,'php_syntax':'13/13 PASS','zip_integrity':'1291/1291 PASS',
 'changed_files':[ENTRY,PROFILE],
 'scope':'mobile <=760px; category intro visible and expanded paragraphs only; 14px',
 'Hobbyfinder':'byte-identical renderer; img only if exact hobby has verified source image',
 'no_production_deploy':True,
}
(OUT.parent/'HD003_150809_REPORT.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
print('ZIP_INTEGRITY_PASS 1291/1291')
print('PHP_SYNTAX_PASS 13/13')
print('CHANGE_SCOPE_PASS only ENTRY and PROFILE')
print('HOBBYFINDER_PHOTOS_UNMODIFIED_PASS')
print(json.dumps(report,ensure_ascii=False,indent=2))
