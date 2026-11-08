#!/usr/bin/env python3
"""Reproducible QA-only PSERC 0.28.54 -> 0.28.55, within existing plugin.
Run python this.py EXACT_PSERC_02854_QA.zip PSERC_02855_QA.zip.
Does not install, publish, change K0, change WP, or create a new plan.
"""
from pathlib import Path
from zipfile import ZipFile
import hashlib
import json
import subprocess
import sys
import tempfile

SOURCE_SHA='2c31ae1bf89613abf456576039f9bd52ef6ed41c1f84c28fd0c57410846033a1'
EXPECTED_OUTPUT='5fb82d0b35346d71d1cc0d9a796e5ca19d1ac3ad595ec5aab9643154db8a8578'
ROOT='portal-seo-editorial-plan-compiler/'
READER=ROOT+'includes/class-pserc-seo-reader.php'
MAIN=ROOT+'portal-seo-editorial-plan-compiler.php'
MANIFEST=ROOT+'contracts/compiler-package-binding-v1.json'
STABLE=ROOT+'includes/class-pserc-stable-json.php'
ANCHOR="        $normalized=[\n            'single_external_seo_owner_receipt'=>$single,"
REPLACEMENT="""        // A candidate already claimed by the ONE external SEO owner must not
        // silently fall back to PSERC's legacy semantic duplicate evaluator
        // when its source-bound proof disappears or becomes stale. Fail closed
        // on this exact topic; every unrelated legacy topic stays unchanged.
        $ownerGate=(array)($candidate['planning_readiness_gate']??[]);
        $externalOwnerClaimed=array_key_exists('external_editorial_receipt',$ownerGate)
            ||array_key_exists('external_seo_owner_verdict',$ownerGate)
            ||in_array('PSTE_SINGLE_EXTERNAL_SEO_DECISION',
                (array)($ownerGate['reason_codes']??[]),true);
        if($externalOwnerClaimed&&!$single){
            $eligible=false;
            $reasons[]='SEO_EXTERNAL_SINGLE_OWNER_PROOF_MISSING_OR_STALE';
        }
        $normalized=[
            'single_external_seo_owner_receipt'=>$single,"""

def build(inp: Path, out: Path):
    if hashlib.sha256(inp.read_bytes()).hexdigest()!=SOURCE_SHA:
        raise RuntimeError('EXACT_PSERC_0.28.54_SOURCE_REQUIRED')
    with ZipFile(inp) as src:
        if len(src.namelist())!=63 or src.testzip() is not None:
            raise RuntimeError('PSERC_54_ZIP_INTEGRITY_FAILED')
        infos=list(src.infolist())
        payload={info.filename:src.read(info.filename) for info in infos}
    reader=payload[READER].decode('utf-8')
    if reader.count(ANCHOR)!=1 or 'SEO_EXTERNAL_SINGLE_OWNER_PROOF_MISSING_OR_STALE' in reader:
        raise RuntimeError('PSERC_READER_ANCHOR_MISSING_OR_ALREADY_PATCHED')
    payload[READER]=reader.replace(ANCHOR,REPLACEMENT).encode('utf-8')
    main=payload[MAIN].decode('utf-8')
    assert main.count("define('PSERC_VERSION', '0.28.54');")==1
    assert main.count("define('PSERC_BUILD','0.28.54-central-owner-kiss');")==1
    payload[MAIN]=main.replace(
        "define('PSERC_VERSION', '0.28.54');",
        "define('PSERC_VERSION', '0.28.55');").replace(
        "define('PSERC_BUILD','0.28.54-central-owner-kiss');",
        "define('PSERC_BUILD','0.28.55-one-owner-no-fallback');").encode('utf-8')
    manifest=json.loads(payload[MANIFEST])
    assert manifest['package_version']=='0.28.54' and manifest['required_file_count']==61
    manifest['package_version']='0.28.55'
    manifest['package_build']='0.28.55-one-owner-no-fallback'
    for rel, description in manifest['required_files'].items():
        data=payload[ROOT+rel]
        description['sha256']=hashlib.sha256(data).hexdigest()
        description['bytes']=len(data)
    manifest.pop('binding_sha256',None)
    with tempfile.TemporaryDirectory() as directory:
        temp=Path(directory)
        (temp/'stable.php').write_bytes(payload[STABLE])
        m=temp/'manifest.json'
        m.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        php=("define('ABSPATH','/qa/');require $argv[1];"
             "$x=json_decode(file_get_contents($argv[2]),true,512,JSON_THROW_ON_ERROR);"
             "echo PSERC_Stable_Json::hash($x);")
        manifest['binding_sha256']=subprocess.check_output(
            ['php','-r',php,str(temp/'stable.php'),str(m)],text=True).strip()
    payload[MANIFEST]=(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
    out.parent.mkdir(parents=True,exist_ok=True)
    with ZipFile(out,'w') as dst:
        for info in infos: dst.writestr(info,payload[info.filename])
    actual=hashlib.sha256(out.read_bytes()).hexdigest()
    if actual!=EXPECTED_OUTPUT:
        raise RuntimeError('REPRODUCIBLE_OUTPUT_MISMATCH '+actual)
    with ZipFile(out) as final:
        assert final.testzip() is None and len(final.namelist())==63
    print('REPRODUCIBLE_PSERC_02855_QA_PASS',actual)
    print('NO SECOND SEMANTIC REVIEW; NO RUNTIME CLASS; NO K0 OR SAVED PLAN EDIT')

if __name__=='__main__':
    if len(sys.argv)!=3: raise SystemExit(__doc__)
    build(Path(sys.argv[1]),Path(sys.argv[2]))
