#!/usr/bin/env python3
"""RC37 actual PHP source tests: cause recorded during one import decision.
No duplicate mapping in the admin report; no blanked source HTML/URL.
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
    o=z.read("affiliate-portal-router/includes/trait-ppar-output-objects.php").decode()
    c=z.read("affiliate-portal-router/includes/trait-ppar-creative-library.php").decode()
    m=z.read("affiliate-portal-router/affiliate-portal-router.php").decode()
    assert "Version: 0.1.34-rc37" in m
    assert "_hb_insurance_reason" in o
    assert "ppar_hab_rc37_tarifcheck_reconcile_v1" in o
    assert "$hb_missing_reasons" in c
    admin_report=c[c.index("private function hab_rc34_tarifcheck_report()"):c.index("public function render_creative_library_page()")]
    assert "hb_rc31_insurance_banner_plan" not in admin_report
    assert "output_assign_banner_targets_from_destination_once" not in admin_report
    assert "https://" not in c[c.index("$hb_missing_reasons"):c.index("$hb_missing_reasons")+1200]
    # existing original test executes the EXACT PHP methods, not a rewrite
    source=(R/"AFFILIATE/RC31_INSURANCE_CASCADE/qa_rc31.py").read_text()
    assert source.count("0.1.28-rc31")>=1
    source=source.replace("0.1.28-rc31","0.1.34-rc37")
    source=source.replace("ppar_hab_rc31_tarifcheck_reconcile_v1",
                          "ppar_hab_rc37_tarifcheck_reconcile_v1")
    anchor="$mapped=$o->output_assign_banner_targets_from_destination_once($motor);"
    assert source.count(anchor)==1
    check=r'''
$unmatched=banner('unknown/', 'Tarifcheck Banner');
$unmatched['id']=555;
$unmatched['payload']=json_encode(array('_destination_source'=>'provider_explicit',
 '_dimension_state'=>'verified','title_source'=>'manual_missing'));
$originalUrl=$unmatched['destination_url'];
$unmatchedResult=$o->output_assign_banner_targets_from_destination_once($unmatched);
$trace=json_decode((string)($GLOBALS['wpdb']->saved[555]['payload']??''),true);
ok(is_array($trace) && isset($trace['_hb_insurance_reason'])
   && is_string($trace['_hb_insurance_reason'])
   && strlen($trace['_hb_insurance_reason'])>0,
   'Unmapped original records exact single decision reason');
ok($unmatchedResult['mapped']===0,'Unknown creative remains blocked, no guessed category');
ok(($GLOBALS['wpdb']->saved[555]['destination_url']??$originalUrl)===$originalUrl,
   'Diagnostics do not change the source destination URL');
ok(!isset($trace['tracking_url']) && !isset($trace['private_id']),
   'Only reason and original payload, no new private tracking copy');
'''
    source=source.replace(anchor,check+"\n"+anchor,1)
    with TemporaryDirectory() as tmp:
        p=Path(tmp)/"qa_rc37.py";p.write_text(source)
        result=run([sys.executable,str(p)],capture_output=True,text=True)
        print(result.stdout)
        if result.returncode:print(result.stderr)
        assert result.returncode==0,(result.stdout[-6000:],result.stderr[-3000:])
        assert "Unmapped original records exact single decision reason" in result.stdout
    # PHP lint all 25 actual packed source files (also done in inherited QA).
print('RC37_PHP_SINGLE_IMPORT_REASON_AND_PROTECTED_ORIGINAL_PASS')
