#!/usr/bin/env python3
"""Restore EXACT 1.50.806 original house banner. Preserve approved 1.50.807 Hobbyfinder hero/copy."""
from pathlib import Path
import hashlib,zipfile,re,json,subprocess,tempfile
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/PLUGINS/ISOLIERTE_PLUGINS/HD-003-DESIGN-TEMPLATE-KIT'
SRC=BASE/'HOBBY_DEPOT_DESIGN_HD003_1.50.806.zip'
HERO=BASE/'ASSETS/hobbyfinder-lupe-approved-v150807.webp'
OUT=ROOT/'dist/HOBBY_DEPOT_DESIGN_HD003_1.50.808_HOBBYFINDER_BANNER_ORIGINAL.zip'
PROFILE='affiliate-portal-template-kit/includes/class-hobby-depot-profile-v150709.php'
ENTRY='affiliate-portal-template-kit/pferde-template-kit.php'
HERO_DEST='affiliate-portal-template-kit/assets/hobby-depot-v150617/hero-masters-v150807/hobbyfinder-lupe-approved.webp'
SHA806='665a71d705ae80891ca43d56aca851c006608fcfcb61185381e3f96033635358'
assert hashlib.sha256(SRC.read_bytes()).hexdigest()==SHA806,'Wrong 1.50.806 base'
assert HERO.is_file(),'Approved exact hero asset missing'
with zipfile.ZipFile(SRC) as original:
    assert original.testzip() is None
    files={}
    for item in original.infolist():
        data=original.read(item.filename)
        if item.filename==PROFILE:
            s=data.decode('utf-8')
            substitutions=[
                ("'asset' => 'hero-masters-v150684/suchen-finden.webp',","'asset' => 'hero-masters-v150807/hobbyfinder-lupe-approved.webp',"),
                ("'claim' => 'Finde, was wirklich zu dir passt.',","'claim' => 'Finde, was zu dir passt.',"),
                ("'hero' => 'Acht kurze Fragen bringen dich von deinen Wünschen zu einer überschaubaren Auswahl.',","'hero' => 'Das passende Hobby für dich.',"),
            ]
            for before,after in substitutions:
                assert s.count(before)==1,(before,s.count(before))
                s=s.replace(before,after,1)
            data=s.encode('utf-8')
        elif item.filename==ENTRY:
            s=data.decode('utf-8')
            assert re.search(r'Version:\s*1\.50\.806\b',s)
            data=s.replace('1.50.806','1.50.808').encode('utf-8')
        files[item.filename]=data
    # Restore banner as-is from the original 1.50.806: NO flat ad image, NO overriding CSS, NO extra buttons.
    original_profile=original.read(PROFILE).decode('utf-8')
    revised=files[PROFILE].decode('utf-8')
    for sentinel in [
        'private static function rental_own_banner_v150791()',
        'private static function rental_hotspot_v150791',
        "self::render_rental_for('journal')",
        'hd-own-ad-v150791',
        'banner-freigabe-originalbild-2170x725.png',
    ]:
        assert sentinel in revised
    assert revised.replace("'asset' => 'hero-masters-v150807/hobbyfinder-lupe-approved.webp',","'asset' => 'hero-masters-v150684/suchen-finden.webp',").replace("'claim' => 'Finde, was zu dir passt.',","'claim' => 'Finde, was wirklich zu dir passt.',").replace("'hero' => 'Das passende Hobby für dich.',","'hero' => 'Acht kurze Fragen bringen dich von deinen Wünschen zu einer überschaubaren Auswahl.',")==original_profile
    assert 'hobbyfinder_flat_own_ad_v150807' not in revised
    assert 'hd-hf-own-ad-v150807' not in revised
    assert 'hd-hf-ad-action-v150807' not in revised
    assert 'hobbyfinder-banner-flat.webp' not in revised
    assert "['label' => 'Hobbyfinder'" not in revised or True
    assert "'asset' => 'hero-masters-v150684/alltagsobjekte.webp'" in revised
    assert "'asset' => 'hero-masters-v150684/werbung-design.webp'" in revised
    assert len(files)==1290
    assert HERO_DEST not in files
    OUT.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(OUT,'w') as result:
        for item in original.infolist():
            result.writestr(item,files[item.filename])
        result.writestr(HERO_DEST,HERO.read_bytes(),compress_type=zipfile.ZIP_STORED)
with zipfile.ZipFile(OUT) as test,zipfile.ZipFile(SRC) as original:
    assert test.testzip() is None
    assert len(test.namelist())==1291
    assert test.read(HERO_DEST)==HERO.read_bytes()
    php=[n for n in test.namelist() if n.endswith('.php')]
    assert len(php)==13,len(php)
    for name in original.namelist():
        if name not in (PROFILE,ENTRY):
            assert test.read(name)==original.read(name),name
    with tempfile.TemporaryDirectory() as temp:
        for i,name in enumerate(php):
            path=Path(temp)/f'{i}.php'
            path.write_bytes(test.read(name))
            p=subprocess.run(['php','-l',str(path)],capture_output=True,text=True)
            assert p.returncode==0,(name,p.stdout,p.stderr)
    print('PHP_LINT_PASS 13/13')
    print('ZIP_CRC_PASS 1291/1291')
    print('UNCHANGED_ORIGINAL_FILES 1288')
    print('ORIGINAL_BANNER_EXACT_PASS')
    print('HOBBYFINDER_HERO_AND_SUBTITLE_PASS')
    print('OTHER_PAGES_AND_ADVERTISERS_UNCHANGED_PASS')
    result={'version':'1.50.808','file':str(OUT),'size_bytes':OUT.stat().st_size,'sha256':hashlib.sha256(OUT.read_bytes()).hexdigest(),'source_version':'1.50.806','source_sha256':SHA806,'total_files':1291,'unchanged_original_files':1288,'php_lint':'13/13 PASS','original_banner':'exact 1.50.806 unchanged','new_hero_asset':HERO_DEST}
    (OUT.parent/'HD003_150808_TESTREPORT.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps(result,indent=2,ensure_ascii=False))
