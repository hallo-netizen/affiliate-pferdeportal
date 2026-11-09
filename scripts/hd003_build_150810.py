#!/usr/bin/env python3
"""HD003 1.50.810 – mobile Hobbyfinder Weiter button scrolls to next question/options."""
from pathlib import Path
import zipfile,hashlib,json,tempfile,subprocess,re
ROOT=Path(__file__).resolve().parents[1]
OFFICE=ROOT/'protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/PLUGINS/ISOLIERTE_PLUGINS/HD-003-DESIGN-TEMPLATE-KIT'
SRC=OFFICE/'HOBBY_DEPOT_DESIGN_HD003_1.50.809.zip'
OUT=ROOT/'dist/HOBBY_DEPOT_DESIGN_HD003_1.50.810_MOBILE_WEITER_SCROLL.zip'
PROFILE='affiliate-portal-template-kit/includes/class-hobby-depot-profile-v150709.php'
ENTRY='affiliate-portal-template-kit/pferde-template-kit.php'
PRE_SHA='3814889dd2178d1af3674a119284cab8d7317c7a70679ed835fb616fe0bbe79b'
assert SRC.is_file()
assert hashlib.sha256(SRC.read_bytes()).hexdigest()==PRE_SHA,'Wrong verified 1.50.809 starting point'
assert (OFFICE/'CURRENT.zip').read_bytes()==SRC.read_bytes(),'Current HD003 not 1.50.809; abort'
before='function next(){if(hasSel(qs[step])){step++;render()}}function back()'
helper="""function mobileScrollToNextStepV150810(){
  if(!window.matchMedia||!window.matchMedia('(max-width:720px)').matches)return;
  requestAnimationFrame(function(){
    const target=app.querySelector('.hd-hf-panel,.hd-hf-results-head');
    if(!target)return;
    // The sticky site header must not cover the next question.
    const header=document.querySelector('.hd-head-v150616');
    const headerHeight=header?header.getBoundingClientRect().height:0;
    const y=window.pageYOffset+target.getBoundingClientRect().top-headerHeight-14;
    window.scrollTo(0,Math.max(0,Math.round(y)));
  });
}
"""
after=helper+'function next(){if(hasSel(qs[step])){step++;render();mobileScrollToNextStepV150810()}}function back()'
with zipfile.ZipFile(SRC) as z:
    assert z.testzip() is None
    assert len(z.namelist())==1291
    entry=z.read(ENTRY).decode('utf8')
    original=z.read(PROFILE).decode('utf8')
    assert original.count(before)==1,original.count(before)
    assert 'mobileScrollToNextStepV150810' not in original
    assert '/* 1.50.809: mobile only;' in original,'Lost 14px mobile typography fix'
    assert 'function resultVisual(h){return h.image?' in original,'Lost Hobbyfinder result photos'
    revised=original.replace(before,after,1)
    assert revised.replace(after,before,1)==original,'Unexpected source changes'
    assert re.search(r'Version:\s*1\.50\.809\b',entry),'Wrong source header'
    newentry=entry.replace('1.50.809','1.50.810')
    assert newentry!=entry
    OUT.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(OUT,'w') as dst:
        for item in z.infolist():
            contents=z.read(item.filename)
            if item.filename==PROFILE:contents=revised.encode('utf8')
            elif item.filename==ENTRY:contents=newentry.encode('utf8')
            dst.writestr(item,contents)
with zipfile.ZipFile(SRC) as orig,zipfile.ZipFile(OUT) as updated:
    assert updated.testzip() is None
    assert updated.namelist()==orig.namelist()
    changed=[n for n in orig.namelist() if orig.read(n)!=updated.read(n)]
    assert sorted(changed)==sorted([PROFILE,ENTRY]),changed
    assert updated.read(PROFILE).decode('utf8').replace(after,before,1)==original
    assert updated.read(PROFILE).decode('utf8').count('function resultVisual(h)')==original.count('function resultVisual(h)')
    php=[n for n in updated.namelist() if n.endswith('.php')]
    assert len(php)==13
    with tempfile.TemporaryDirectory() as td:
        for i,n in enumerate(php):
            tmp=Path(td)/f'{i}.php'
            tmp.write_bytes(updated.read(n))
            process=subprocess.run(['php','-l',str(tmp)],text=True,capture_output=True)
            assert process.returncode==0,(n,process.stdout,process.stderr)
report={'version':'1.50.810','file':str(OUT),'source_version':'1.50.809','size_bytes':OUT.stat().st_size,'sha256':hashlib.sha256(OUT.read_bytes()).hexdigest(),'source_sha256':PRE_SHA,'changed_files':[PROFILE,ENTRY],'zip_crc':'1291/1291 PASS','php_syntax':'13/13 PASS','behavior':'on mobile <=720px, after each Weiter scroll to next question/options; results heading on final Weiter; desktop unchanged','category_font':'14px original fix preserved','hobbyfinder_images':'unchanged'}
(OUT.parent/'HD003_150810_REPORT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('HD003_150810_BUILD_PASS',json.dumps(report,ensure_ascii=False))
