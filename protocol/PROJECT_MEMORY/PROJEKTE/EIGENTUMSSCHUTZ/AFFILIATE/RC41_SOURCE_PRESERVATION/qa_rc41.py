#!/usr/bin/env python3
"""Fix must pass actual PHP source parse->full normalization->source decision
and old RC23-RC40 owner/format regressions. No private live source invented.
"""
from pathlib import Path
from zipfile import ZipFile
from tempfile import TemporaryDirectory
from subprocess import run
import sys
R=Path("protocol/PROJECT_MEMORY/PROJEKTE/EIGENTUMSSCHUTZ")
P=R/"PLUGINS/ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip"
with ZipFile(P) as z:
    assert z.testzip() is None and len(z.namelist())==36
    src=z.read("affiliate-portal-router/includes/trait-ppar-creative-library.php").decode()
    assert "creative_library_read_original_banner_once($normalized,$html)" in src
    assert "_source_read_version']=2" in src
    assert "Version: 0.1.38-rc41" in z.read("affiliate-portal-router/affiliate-portal-router.php").decode()
    assert "ppar_hab_rc41_tarifcheck_reconcile_v1" in z.read("affiliate-portal-router/includes/trait-ppar-output-objects.php").decode()

old=(R/"AFFILIATE/RC40_SOURCE_LOSS_PROOF/qa_source_loss.py").read_text()
assert "RC40_ACTUAL_PHP_FULL_IMPORT_SOURCE_LOSS_PROVEN" in old
old=old.replace(
    """ok(($payload['_source_read_version']??0)===1,
  'RC40 irrevocably marks this source as already read');
ok(trim((string)($payload['_source_evidence']['text']??''))==='',
  'First source read cannot recover insurance from discarded anchor title');""",
    """ok(($payload['_source_read_version']??0)===2,
  'RC41 marks genuine first source read AFTER all HTML attributes extracted');
ok(str_contains((string)($payload['_source_evidence']['text']??''),'Hausratversicherung'),
  'Full import NOW retains original anchor title as safe source evidence');""")
old=old.replace(
    """ok($rerun['payload']===$normalized['payload'],
  'Later RC40 rebind skips read and cannot reconstruct deleted original attributes');""",
    """ok($rerun['payload']===$normalized['payload'],
  'Later rebind reads stored canonical evidence without repeating source extraction');""")
old=old.replace(
    """echo "RC40_ACTUAL_PHP_FULL_IMPORT_SOURCE_LOSS_PROVEN\\n";""",
    """// Original HTML already lost in an old record is not reconstructible.
$legacy=$normalized;
$legacyPayload=json_decode((string)$legacy['payload'],true);
$legacyPayload['html']='';
$legacyPayload['_source_read_version']=1;
$legacyPayload['_source_evidence']=array('destination'=>'','provider'=>'','text'=>'','image_hint'=>'');
$legacy['payload']=json_encode($legacyPayload);
$oldRead=$o->creative_library_read_original_banner_once($legacy);
$oldProof=json_decode((string)$oldRead['payload'],true);
ok(($oldProof['_source_read_version']??0)===2
    && trim((string)$oldProof['_source_evidence']['text'])===''
    && ($oldProof['_original_html_attributes_available']??1)===0,
   'Already destroyed original attribute cannot be fabricated on legacy rebind');
echo "RC41_ACTUAL_PHP_COMPLETE_IMPORT_PRESERVATION_PASS\\n";""")
old=old.replace('"RC40_ACTUAL_PHP_FULL_IMPORT_SOURCE_LOSS_PROVEN" in v.stdout',
                '"RC41_ACTUAL_PHP_COMPLETE_IMPORT_PRESERVATION_PASS" in v.stdout')
old=old.replace("NO_NEW_PLUGIN_RELEASE_NO_LIVE_DATA_INVENTED",
                "RC41_SOURCE_FIX_TESTED_NO_LIVE_DATA_INVENTED")
with TemporaryDirectory() as td:
    f=Path(td)/"qa_full_import.py"
    f.write_text(old)
    p=run([sys.executable,str(f)],capture_output=True,text=True)
    print(p.stdout)
    if p.returncode:print(p.stderr)
    assert p.returncode==0,(p.stdout[-6000:],p.stderr[-5000:])
    assert "RC41_ACTUAL_PHP_COMPLETE_IMPORT_PRESERVATION_PASS" in p.stdout

qa=(R/"AFFILIATE/RC40_SOURCE_FIRST/qa_rc40.py").read_text()
assert "0.1.37-rc40" in qa
qa=qa.replace("0.1.37-rc40","0.1.38-rc41")
qa=qa.replace("ppar_hab_rc40_tarifcheck_reconcile_v1",
              "ppar_hab_rc41_tarifcheck_reconcile_v1")
qa=qa.replace("'_source_read_version']??0)!==1","'_source_read_version']??0)!==2")
qa=qa.replace("'_source_read_version']??0)===1","'_source_read_version']??0)===2")
with TemporaryDirectory() as td:
    f=Path(td)/"qa_rc40_on_rc41.py"
    f.write_text(qa)
    p=run([sys.executable,str(f)],capture_output=True,text=True)
    print(p.stdout[-5800:])
    if p.returncode:print(p.stderr[-5000:])
    assert p.returncode==0,(p.stdout[-8500:],p.stderr[-5000:])
    assert "RC40_SINGLE_CENTRAL_OWNER_WRITE_ONCE_PASS" in p.stdout
print("RC41_ORIGINAL_PHP_IMPORT_FIRST_AND_ALL_OLD_RC23_RC40_QA_PASS")
