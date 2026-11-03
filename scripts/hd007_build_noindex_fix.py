#!/usr/bin/env python3
"""Rebuild complete HD-007 from the immutable verified 1.2.17 source ZIP."""
import hashlib, json, re, zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
ORIGINAL=ROOT/"protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/PLUGINS/ISOLIERTE_PLUGINS/HD-007-HOBBYREGISTER-CORE/CURRENT.zip"
FRONT="hd-hobbyregister-core/includes/class-hd-hobbyregister-frontend.php"
MAIN="hd-hobbyregister-core/hobby-depot-hobbyregister-core.php"
REG="hd-hobbyregister-core/data/hobby-register.json"
SHA="433a642aac02439c74b85653c49c9c8ac62e6de5ea82be42ce58ce53537e8488"
OUT=ROOT/"dist/HOBBY_DEPOT_HD007_1.2.18_SEO_OWNER_KORREKTUR_VOLLPLUGIN.zip"
UNPACK=ROOT/"dist/unpacked"
replacement=r'''    // Authoritative relationship from the single existing 862-hobby register.
    // The top CORE hobby page takes SEO priority only when it exists in the current mapping.
    private static function profile_has_core_owner($row) {
        if (!is_array($row)) { return false; }
        $identity = $row['source_identity'] ?? [];
        return is_array($identity)
            && ($identity['current_terminal_hobby_page'] ?? false) === true
            && is_string($identity['target_node_id'] ?? null)
            && $identity['target_node_id'] !== '';
    }

    public static function head_meta() {
        $route = self::route();
        if ($route['type'] !== 'profile') { return; }
        $row = self::record_by_slug($route['slug']);
        if (!self::profile_has_core_owner($row)) { return; }
        echo "<meta name=\"robots\" content=\"noindex,follow\">\n";
    }
'''
def sha(b): return hashlib.sha256(b).hexdigest()
raw=ORIGINAL.read_bytes()
assert sha(raw)==SHA, "Original version does not match known SHA256; refuse build"
OUT.parent.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(ORIGINAL) as z:
    assert z.testzip() is None
    info=z.infolist()
    assert len(info)==93, f"Unexpected ZIP structure: {len(info)}"
    assert FRONT in z.namelist() and MAIN in z.namelist() and REG in z.namelist()
    rows=json.loads(z.read(REG))['records']
    assert len(rows)==862
    owned=[r for r in rows if (r.get('source_identity',{}).get('current_terminal_hobby_page') is True and
           isinstance(r.get('source_identity',{}).get('target_node_id'),str) and
           r['source_identity']['target_node_id'])]
    free=len(rows)-len(owned)
    assert owned and free, 'Both ownership classes must be present'
    print('REGISTRY',len(rows),'CORE OWNERS',len(owned),'REGISTER INDEXABLE',free)
    front=z.read(FRONT).decode('utf-8')
    head_pat=re.compile(r'^    public static function head_meta\(\) \{\n.*?^    \}\n',re.M|re.S)
    front,n=head_pat.subn(lambda _:replacement,front)
    assert n==1,'Expected one, and only one, original head_meta()'
    assert 'const VERSION = ' in front
    assert "const VERSION = '1.2.16';" in front
    front=front.replace("1.2.16","1.2.18")
    assert 'const VERSION = '+"'1.2.18';" in front
    assert front.count('noindex,follow')==1
    main=z.read(MAIN).decode('utf-8')
    assert 'Version: 1.2.17' in main
    main=main.replace('Version: 1.2.17','Version: 1.2.18',1)
    mods={FRONT:front.encode('utf-8'),MAIN:main.encode('utf-8')}
    with zipfile.ZipFile(OUT,'w') as output:
        for member in info:
            if member.is_dir():
                output.writestr(member,b'')
                continue
            contents=mods.get(member.filename)
            if contents is None:contents=z.read(member)
            output.writestr(member,contents)
    with zipfile.ZipFile(OUT) as rebuilt:
        assert rebuilt.testzip() is None
        assert rebuilt.namelist()==z.namelist()
        for member in info:
            if member.filename not in mods and not member.is_dir():
                assert rebuilt.read(member.filename)==z.read(member.filename),'Unwanted modified entry: '+member.filename
        for name in [FRONT,MAIN,REG]:
            p=UNPACK/name
            p.parent.mkdir(parents=True,exist_ok=True)
            p.write_bytes(rebuilt.read(name))
        # Extract all PHP files only for syntax checking.
        for name in rebuilt.namelist():
            if name.endswith('.php') and name not in [FRONT,MAIN]:
                p=UNPACK/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(rebuilt.read(name))
    manifest={
      'source':'HD-007 1.2.17 verified original',
      'source_sha256':SHA,
      'generated_version':'1.2.18',
      'archive_sha256':sha(OUT.read_bytes()),
      'archive_size':OUT.stat().st_size,
      'archive_entries':len(info),
      'changed_files':[MAIN,FRONT],
      'byte_identical_other_entries':len(info)-2,
      'register_records':len(rows),
      'with_core_owner_noindex':len(owned),
      'without_core_owner_indexable':len(free)
    }
    (ROOT/'dist/HD007_1.2.18_TESTBELEG.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    print('BUILD PASS',json.dumps(manifest,ensure_ascii=False))
