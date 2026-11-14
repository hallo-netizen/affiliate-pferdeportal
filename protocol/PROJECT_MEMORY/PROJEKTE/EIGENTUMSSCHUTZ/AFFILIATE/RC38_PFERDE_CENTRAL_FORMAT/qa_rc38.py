#!/usr/bin/env python3
"""Real packed PHP regression: every known real Tarifcheck size, true context,
stored format -> public selection. Pferde original no-upscale/no-crop layout.
"""
from pathlib import Path
from zipfile import ZipFile
from tempfile import TemporaryDirectory
from subprocess import run
import re,sys

R=Path("protocol/PROJECT_MEMORY/PROJEKTE/EIGENTUMSSCHUTZ")
P=R/"PLUGINS/ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip"
with ZipFile(P) as z:
    assert z.testzip() is None and len(z.namelist())==36
    base="affiliate-portal-router/"
    m=z.read(base+"affiliate-portal-router.php").decode()
    o=z.read(base+"includes/trait-ppar-output-objects.php").decode()
    css=z.read(base+"assets/frontend.css").decode()
    assert 'Version: 0.1.35-rc38' in m
    assert 'ppar_hab_rc38_tarifcheck_reconcile_v1' in o
    assert "'min_width'=>0,'min_height'=>0" in o
    assert "'_hb_original_format_approved'=>true" in o
    assert "&& empty($rule['_hb_original_format_approved'])" in o
    assert "if ($hb_single_original && !empty($slot['rule']['_hb_original_format_approved']))" in o
    assert "if($this->output_row_matches_slot_rule" not in m[m.index("private function campaign_matches_contract_slot_rule("):m.index("private function campaign_matches_contract_slot_rule(")+1250]
    assert "max-height:420px!important" in css
    assert ".ppar-hb-insurance-slot[data-ppar-slot] .ppar-overview-wide-banner-image" in css
    assert "width:auto!important;height:auto!important" in css
    assert "object-fit:contain!important" in css
    assert "object-position:center!important" in css

# Adapt the previously green *real packed PHP* verification, not a mock
# rewritten decision engine. Add all 4 actual previously blocked formats.
s=(R/"AFFILIATE/RC36_SLOT_SINGLE_PASS/qa_rc36.py").read_text()
before={
    '0.1.33-rc36':'0.1.35-rc38',
    'ppar_hab_rc36_tarifcheck_reconcile_v1':'ppar_hab_rc38_tarifcheck_reconcile_v1',
    'array(array(728,90),array(468,60),array(300,250),array(125,125))':
      'array(array(728,90),array(468,60),array(300,250),array(125,125),array(120,60),array(234,60),array(120,600),array(160,600))',
    'array(array(160,600),array(120,600),array(1,1))':
      'array(array(1,1),array(119,60),array(120,59))',
    "RC36_REAL_ORIGINAL_PHP_FORMAT_TO_PUBLIC_PASS":"RC38_REAL_ORIGINAL_PHP_FORMAT_TO_PUBLIC_PASS",
    "RC36_ALL_25_PACKED_PHP_LINT_PASS":"RC38_ALL_25_PACKED_PHP_LINT_PASS",
    "Tall/tiny formats have no invented category slot":"Too-small originals remain excluded without upscaling",
}
for a,b in before.items():
    assert a in s,(a,'original QA changed')
    s=s.replace(a,b)
# Use the exact old PHP harness with two extra original functions as well as
# its real slot, public format and safety methods.
anchor="    runtime=method(m,'campaign_matches_contract_slot_rule')"
assert s.count(anchor)==1
s=s.replace(anchor,anchor+"\n    runtime+='\\n'+method(m,'hb_insurance_original_inline_allowed')+'\\n'+method(m,'hb_insurance_original_wide_allowed')")
test_anchor="""ok($o->campaign_matches_contract_slot_rule($canonical,'product_after_category_tiles'),
   'Public runtime consumes stored category format without redecision');"""
assert s.count(test_anchor)==1
s=s.replace(test_anchor,r'''
$canonical['dimensions']='120x600';
ok(!$o->hb_insurance_original_wide_allowed($canonical,'product_after_category_tiles',array()),
   'Canonical insurance NEVER triggers old second wide format evaluator');
ok(!$o->hb_insurance_original_inline_allowed($canonical,'post_inline_banner',array()),
   'Canonical insurance NEVER triggers old second inline format evaluator');
''' + test_anchor)
with TemporaryDirectory() as d:
    p=Path(d)/"qa_rc38_pferde_original_php.py"
    p.write_text(s)
    r=run([sys.executable,str(p)],capture_output=True,text=True)
    print(r.stdout)
    if r.returncode:print(r.stderr)
    assert r.returncode==0,(r.stdout[-7000:],r.stderr[-3000:])
    assert r.stdout.count("PASS Real insurance slot ")==32,('expected 8 image sizes x 4 real areas',r.stdout.count("PASS Real insurance slot "))
    assert "Canonical insurance NEVER triggers old second wide" in r.stdout
# Also confirm the already-green original RC37 insurance diagnostics /
# no guessed target behavior on the exact final package.
rc37=(R/"AFFILIATE/RC37_ACTUAL_SOURCE_REASON/qa_rc37.py").read_text()
assert "0.1.34-rc37" in rc37 and "ppar_hab_rc37_tarifcheck_reconcile_v1" in rc37
rc37=rc37.replace("0.1.34-rc37","0.1.35-rc38")
rc37=rc37.replace("ppar_hab_rc37_tarifcheck_reconcile_v1","ppar_hab_rc38_tarifcheck_reconcile_v1")
with TemporaryDirectory() as d:
    p=Path(d)/"qa_rc37_on_rc38.py"
    p.write_text(rc37)
    r=run([sys.executable,str(p)],capture_output=True,text=True)
    print(r.stdout)
    if r.returncode:print(r.stderr)
    assert r.returncode==0,(r.stdout[-5000:],r.stderr[-3000:])
print('RC38_ONE_OWNER_32_REAL_PHP_FORMAT_CONTEXT_NO_UPSCALE_REGRESSIONS_PASS')
