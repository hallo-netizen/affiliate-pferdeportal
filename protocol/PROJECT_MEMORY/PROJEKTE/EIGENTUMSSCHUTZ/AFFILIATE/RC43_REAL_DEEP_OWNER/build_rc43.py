#!/usr/bin/env python3
"""RC43: ONE original source, ONE verified WordPress insurance owner.
Fix only the ten ACTUAL blocked 'deep=' products from the real uploaded
160-row WP JSON report. Does not change other portal/provider logic.
No new worker, matcher, frontend writes or WP table.
"""
from io import BytesIO
from pathlib import Path
from zipfile import ZipFile
from hashlib import sha256
R=Path("protocol/PROJECT_MEMORY/PROJEKTE/EIGENTUMSSCHUTZ")
P=R/"PLUGINS/ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip"
raw=P.read_bytes()
assert sha256(raw).hexdigest()=="10d6ccfc5b334880040c8aeaf44498c533b0e81f135ac0c34e5da4696967f504","Exact RC42 required"
B="affiliate-portal-router/"
OUT=B+"includes/trait-ppar-output-objects.php"
MAIN=B+"affiliate-portal-router.php"
README=B+"readme.txt"
def replace_one(s,old,new):
    assert s.count(old)==1,("Unexpected owner source",s.count(old),old[:180])
    return s.replace(old,new,1)
with ZipFile(BytesIO(raw)) as src:
    assert len(src.namelist())==36 and src.testzip() is None
    files={i.filename:src.read(i.filename) for i in src.infolist()}
    o=files[OUT].decode()
    anchor="""        $candidate_matches=array();
        foreach ($eligible as $key=>$item) {"""
    change=r'''        $candidate_matches=array();
        // Real 14.11.2026 WP source export: ALL 80 formerly blocked banners
        // already contain ONE proven, specific deep= product name. This
        // stable relation resolves that ORIGINAL product into an existing,
        // actual verified R3 or R2; it is NOT a second classifier.
        // Only exact source names are eligible, never ad_id or image size.
        $fixed_original_deep_to_existing_wp_slug=array(
            'riester-rente'=>'krankenversicherung-und-vorsorge',
            'ruerup-rente'=>'krankenversicherung-und-vorsorge',
            'rentenversicherung'=>'krankenversicherung-und-vorsorge',
            'lebensversicherung'=>'krankenversicherung-und-vorsorge',
            'krankenzusatzversicherung'=>'krankenversicherung-und-vorsorge',
            'hundekrankenversicherung'=>'tierkrankenversicherung',
            'haftpflichtversicherung'=>'haftpflicht-und-rechtsschutz',
            'hundeversicherung'=>'haftpflicht-und-rechtsschutz',
            'grundbesitzerhaftpflicht'=>'haus-und-grundbesitzerhaftpflichtversicherung',
            'firmenversicherung'=>'gewerbeversicherungen-und-finanzen',
        );
        $original_deep=is_array($source_evidence)
            ? sanitize_key(trim((string)($source_evidence['destination']??''))) : '';
        $known_wp_slug=(string)($fixed_original_deep_to_existing_wp_slug[$original_deep]??'');
        if($known_wp_slug!=='') {
            // Real runtime nodes, NO guessed/stored WP numeric identifiers.
            foreach($eligible as $key=>$item) {
                $n=$item['node'];
                if(($n['type']??'')!=='page')continue;
                if(sanitize_key((string)($n['slug']??''))!==$known_wp_slug)continue;
                // Parent R1 / R2 / R3 ancestry has already been verified
                // while building $eligible from the live WordPress snapshot.
                $candidate_matches[$key]=array(
                    'depth'=>$item['depth'],'length'=>strlen($original_deep));
                break;
            }
        }
        // Backwards-compatible exact page matcher, but it must NEVER
        // choose a second independent category when the fixed original
        // deep= source already selected an owner.
        if(!$candidate_matches)foreach ($eligible as $key=>$item) {'''
    o=replace_one(o,anchor,change)
    o=replace_one(o,"$option='ppar_hab_rc41_tarifcheck_reconcile_v1';",
                  "$option='ppar_hab_rc43_tarifcheck_reconcile_v1';")
    files[OUT]=o.encode()
    m=files[MAIN].decode()
    m=replace_one(m,"Version: 0.1.39-rc42","Version: 0.1.40-rc43")
    files[MAIN]=m.encode()
    rd=files[README].decode()
    rd=replace_one(rd,"Stable tag: 0.1.39-rc42","Stable tag: 0.1.40-rc43")
    files[README]=rd.encode()
    changed={OUT,MAIN,README}
    assert all(files[n]==src.read(n) for n in src.namelist() if n not in changed)
    buf=BytesIO()
    with ZipFile(buf,"w") as out:
        for entry in src.infolist():out.writestr(entry,files[entry.filename])
    target=buf.getvalue()
with ZipFile(BytesIO(target)) as z:
    assert len(z.namelist())==36 and z.testzip() is None
    assert b"ppar_hab_rc43_tarifcheck_reconcile_v1" in z.read(OUT)
    assert b"0.1.40-rc43" in z.read(MAIN)
P.write_bytes(target)
print("RC43_SINGLE_OWNER_80_REAL_DEEP_TARGETS_BUILD_PASS",len(target),sha256(target).hexdigest())
