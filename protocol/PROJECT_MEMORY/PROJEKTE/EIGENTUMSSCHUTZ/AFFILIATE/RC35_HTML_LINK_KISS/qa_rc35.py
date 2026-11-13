#!/usr/bin/env python3
"""Run all original RC31 single-owner PHP mapping tests after RC35, with
extra real PHP cases: HTML deep target, first party path, HTML anchor text.
Do not count synthetic records as 160 LIVE banners.
"""
from pathlib import Path
from tempfile import TemporaryDirectory
from subprocess import run
import sys
from zipfile import ZipFile
R=Path("protocol/PROJECT_MEMORY/PROJEKTE/EIGENTUMSSCHUTZ")
Z=R/"PLUGINS/ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip"
with ZipFile(Z) as z:
    assert z.testzip() is None
    out=z.read("affiliate-portal-router/includes/trait-ppar-output-objects.php").decode()
    cr=z.read("affiliate-portal-router/includes/trait-ppar-creative-library.php").decode()
    main=z.read("affiliate-portal-router/affiliate-portal-router.php").decode()
    assert "Version: 0.1.32-rc35" in main
    assert "original_anchor_text" in out
    assert "$host==='a.partner-versicherung.de'" in out
    assert "$final_host !== $initial_host" not in cr
source=(R/"AFFILIATE/RC31_INSURANCE_CASCADE/qa_rc31.py").read_text()
assert source.count("0.1.28-rc31")>=1
source=source.replace("0.1.28-rc31","0.1.32-rc35")
# The inherited, one-time migration already has its RC34 checkpoint key.
source=source.replace("ppar_hab_rc31_tarifcheck_reconcile_v1","ppar_hab_rc34_tarifcheck_reconcile_v1")
anchor="$motor=banner('motorradversicherung/','Motorradversicherung vergleichen');"
assert source.count(anchor)==1
checks=r'''
// Real unchanged PHP functions and verified-node matcher from RC31.
// The genuine original HTML link contains deep=, no made-up Banner title.
$deepRow=banner('generic','Tarifcheck Banner');
$deepRow['tracking_url']='https://a.partner-versicherung.de/click.php?partner_id=0&ad_id=15&deep=hausratversicherung&model=3';
$deepRow['destination_url']=$deepRow['tracking_url'];
$deepRow['payload']=json_encode(array('_destination_source'=>'tracking_checked',
 '_dimension_state'=>'verified','title_source'=>'manual_missing'));
$deepPlan=$o->hb_rc31_insurance_banner_plan($deepRow,$portal,$GLOBALS['targets'],array('page','category'));
ok($deepPlan['status']==='ready' && $deepPlan['target']['id']===111,
  'Existing raw HTML href deep=hausratversicherung maps directly to real Hausrat R3');

// Keep real category tree binding also for original Tarifcheck Kfz deep-link.
$kfzRow=$deepRow;
$kfzRow['tracking_url']='https://a.partner-versicherung.de/click.php?partner_id=0&ad_id=15&deep=kfz-versicherung&model=3';
$kfzRow['destination_url']=$kfzRow['tracking_url'];
$kfzPlan=$o->hb_rc31_insurance_banner_plan($kfzRow,$portal,$GLOBALS['targets'],array('page','category'));
ok($kfzPlan['status']==='ready' && $kfzPlan['target']['id']===101,
  'Kfz deep target matches verified existing Kfz-Versicherungen R2');

// When the original anchor contains words, the existing saved HTML is enough.
$textRow=banner('generic','Tarifcheck Banner');
$textRow['destination_url']='https://tracker.invalid/click';
$textRow['tracking_url']=$textRow['destination_url'];
$textRow['payload']=json_encode(array('_destination_source'=>'tracking_checked',
 '_dimension_state'=>'verified','title_source'=>'manual_missing',
 'html'=>'<a href="https://tracker.invalid/click">Hausratversicherung <img src="https://tracker.invalid/a.png" alt=""></a>'));
$textPlan=$o->hb_rc31_insurance_banner_plan($textRow,$portal,$GLOBALS['targets'],array('page','category'));
ok($textPlan['status']==='ready' && $textPlan['target']['id']===111,
  'Already saved HTML anchor text classifies once without reimport');

// A fake hostile tracking domain deep= does not create insurance evidence.
$fakeRow=$deepRow;
$fakeRow['tracking_url']='https://stranger.example/click?deep=hausratversicherung';
$fakeRow['destination_url']=$fakeRow['tracking_url'];
$fakeRow['payload']=json_encode(array('_destination_source'=>'tracking_checked',
 '_dimension_state'=>'verified','title_source'=>'manual_missing'));
$fakePlan=$o->hb_rc31_insurance_banner_plan($fakeRow,$portal,$GLOBALS['targets'],array('page','category'));
ok($fakePlan['status']==='blocked',
  'Unknown tracking domain cannot invent Hausrat evidence');
'''
source=source.replace(anchor,checks+"\n"+anchor,1)
with TemporaryDirectory() as td:
    p=Path(td)/"qa_rc35_original_php.py"
    p.write_text(source)
    result=run([sys.executable,str(p)],capture_output=True,text=True)
    print(result.stdout)
    if result.returncode:
        print(result.stderr)
    assert result.returncode==0,(result.stdout[-6000:],result.stderr[-5000:])
    assert "Existing raw HTML href" in result.stdout
print("RC35_ORIGINAL_PHP_HTML_EVIDENCE_FULL_REGRESSION_PASS")
