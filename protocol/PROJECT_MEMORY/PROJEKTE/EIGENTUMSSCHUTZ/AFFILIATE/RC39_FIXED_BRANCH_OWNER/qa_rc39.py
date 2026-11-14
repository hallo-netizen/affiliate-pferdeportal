#!/usr/bin/env python3
"""Run ACTUAL PHP extracted from one packed plugin. Test fixed aliases,
real dynamically verified R2/R3/leaf owner fallback, no cross-world pollution.
Never use fake demo targets to claim the 160 live creatives are mapped.
"""
from pathlib import Path
from zipfile import ZipFile
from tempfile import TemporaryDirectory
from subprocess import run
import sys
R=Path("protocol/PROJECT_MEMORY/PROJEKTE/EIGENTUMSSCHUTZ")
Z=R/"PLUGINS/ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip"
with ZipFile(Z) as z:
    assert z.testzip() is None and len(z.namelist())==36
    o=z.read("affiliate-portal-router/includes/trait-ppar-output-objects.php").decode()
    main=z.read("affiliate-portal-router/affiliate-portal-router.php").decode()
    assert "Version: 0.1.36-rc39" in main
    assert "ppar_hab_rc39_tarifcheck_reconcile_v1" in o
    assert "fixed_aliases" in o and "parent_groups" in o
    assert "No verified specific/general insurance" in o
# Reuse only the real previous original PHP harness.
source=(R/"AFFILIATE/RC31_INSURANCE_CASCADE/qa_rc31.py").read_text()
assert "0.1.28-rc31" in source
source=source.replace("0.1.28-rc31","0.1.36-rc39")
source=source.replace("ppar_hab_rc31_tarifcheck_reconcile_v1",
                      "ppar_hab_rc39_tarifcheck_reconcile_v1")
anchor="$mapped=$o->output_assign_banner_targets_from_destination_once($motor);"
assert source.count(anchor)==1
checks=r'''
$baselineNodes=$GLOBALS['nodes']; $baselineTargets=$GLOBALS['targets'];
// Shorthand must be normalized in exactly the existing importer decision.
$shortHaus=banner('tarifcheck/','Hausrat');
$shortPlan=$o->hb_rc31_insurance_banner_plan($shortHaus,$portal,$GLOBALS['targets'],array('page','category'));
ok($shortPlan['status']==='ready' && $shortPlan['target']['id']===111,'Real R3 Hausrat from shorthand');

// Stable synonym Kfz => Autoversicherung; never moto sibling.
$car=banner('tarifcheck/','Kfz-Versicherung');
$carPlan=$o->hb_rc31_insurance_banner_plan($car,$portal,$GLOBALS['targets'],array('page','category'));
ok($carPlan['status']==='ready' && $carPlan['target']['id']===104,'Kfz fixed alias -> existing Autoversicherung R3');
ok(!in_array('category:motorrad-vergleichen',$carPlan['path_target_keys'],true),
  'Kfz exact child excludes Moto and other sibling products');

// The dynamic active tree (not a hand-picked WP ID list) has PKV R3.
$GLOBALS['nodes']['ins:r2:health']=array('id'=>'ins:r2:health','parent'=>'core:world:insurance',
 'type'=>'page','name'=>'Gesundheit & Vorsorge','slug'=>'gesundheit-und-vorsorge','wp_id'=>130);
$GLOBALS['nodes']['ins:r3:pkv']=array('id'=>'ins:r3:pkv','parent'=>'ins:r2:health',
 'type'=>'page','name'=>'Private Krankenversicherung','slug'=>'private-krankenversicherung','wp_id'=>131);
$GLOBALS['nodes']['ins:leaf:pkv']=array('id'=>'ins:leaf:pkv','parent'=>'ins:r3:pkv',
 'type'=>'category','name'=>'Private Krankenversicherung: Beratung','slug'=>'private-krankenversicherung-beratung','wp_id'=>132);
foreach(array('ins:r2:health','ins:r3:pkv','ins:leaf:pkv') as $key){
 $node=$GLOBALS['nodes'][$key];$GLOBALS['targets'][]=array('type'=>$node['type'],
 'key'=>$node['type'].':'.$node['wp_id'],'id'=>$node['wp_id'],'slug'=>$node['slug'],
 'label'=>$node['name'],'context'=>'page','depth'=>2);
}
$pkv=banner('tarifcheck/','PKV vergleichen');
$pkvPlan=$o->hb_rc31_insurance_banner_plan($pkv,$portal,$GLOBALS['targets'],array('page','category'));
ok($pkvPlan['status']==='ready' && $pkvPlan['target']['id']===131,
   'PKV uniquely maps to real Private Krankenversicherung R3');
ok(!in_array('page:hausratversicherung',$pkvPlan['path_target_keys'],true),
   'PKV cannot leak to Sach');

// No specific R3 exists; named exact leaf identifies the only existing R2.
// User-approved fallback: selected parent and its own descendants.
$GLOBALS['nodes']['ins:r2:reise']=array('id'=>'ins:r2:reise','parent'=>'core:world:insurance',
 'type'=>'page','name'=>'Reisen & Mobilität','slug'=>'reisen-und-mobilitaet','wp_id'=>140);
$GLOBALS['nodes']['ins:leaf:reise']=array('id'=>'ins:leaf:reise','parent'=>'ins:r2:reise',
 'type'=>'category','name'=>'Reiseversicherung: Beratung','slug'=>'reiseversicherung-beratung','wp_id'=>141);
$GLOBALS['nodes']['ins:leaf:reise2']=array('id'=>'ins:leaf:reise2','parent'=>'ins:r2:reise',
 'type'=>'category','name'=>'Reisen & Mobilität: Allgemein','slug'=>'reisen-mobilitaet-allgemein','wp_id'=>142);
foreach(array('ins:r2:reise','ins:leaf:reise','ins:leaf:reise2') as $key){
 $node=$GLOBALS['nodes'][$key];$GLOBALS['targets'][]=array('type'=>$node['type'],
 'key'=>$node['type'].':'.$node['wp_id'],'id'=>$node['wp_id'],'slug'=>$node['slug'],
 'label'=>$node['name'],'context'=>'page','depth'=>2);
}
$reise=banner('tarifcheck/','Reiseversicherung');
$reisePlan=$o->hb_rc31_insurance_banner_plan($reise,$portal,$GLOBALS['targets'],array('page','category'));
ok($reisePlan['status']==='ready' && $reisePlan['target']['id']===140,
 'Real named leaf without R3 selects its verified parent R2 once');
ok(in_array('category:reiseversicherung-beratung',$reisePlan['path_target_keys'],true)
 && in_array('category:reisen-mobilitaet-allgemein',$reisePlan['path_target_keys'],true)
 && !in_array('category:hausrat-vergleichen',$reisePlan['path_target_keys'],true),
 'Parent path covers own subtree and no other insurance area');

// No R3 or named leaf; fixed specialty -> matching existing named R2 only.
$missingR3=banner('tarifcheck/','Wohngebäudeversicherung');
$parentPlan=$o->hb_rc31_insurance_banner_plan($missingR3,$portal,$GLOBALS['targets'],array('page','category'));
ok($parentPlan['status']==='ready' && $parentPlan['target']['id']===110,
 'Missing specific R3 uses fixed real Sachversicherungen parent');
ok(in_array('category:hausrat-vergleichen',$parentPlan['path_target_keys'],true)
 && !in_array('category:reiseversicherung-beratung',$parentPlan['path_target_keys'],true),
 'Fallback populates ONLY that parent existing insurance subtree');

// Even with dynamic insurance nodes, no proof => NO default full tree mapping.
$unknownNoProof=banner('tarifcheck/','Tarifcheck Banner');
$blocked=$o->hb_rc31_insurance_banner_plan($unknownNoProof,$portal,$GLOBALS['targets'],array('page','category'));
ok($blocked['status']==='blocked','Unverified Tarifcheck creative NEVER becomes a generic insurance banner');

// No broad fallback when distinct, conflicting specialist products coexist.
$two=banner('tarifcheck/','Wohngebäudeversicherung und Reiseversicherung');
$both=$o->hb_rc31_insurance_banner_plan($two,$portal,$GLOBALS['targets'],array('page','category'));
ok($both['status']==='blocked','Two unrelated specialists never become one broad parent');
// Restore original RC31 fixture before its own unchanged general 9-node test.
$GLOBALS['nodes']=$baselineNodes; $GLOBALS['targets']=$baselineTargets;
'''
source=source.replace(anchor,checks+"\n"+anchor,1)
with TemporaryDirectory() as td:
    p=Path(td)/"qa_single_php.py"
    p.write_text(source)
    res=run([sys.executable,str(p)],capture_output=True,text=True)
    print(res.stdout)
    if res.returncode:print(res.stderr)
    assert res.returncode==0,(res.stdout[-9000:],res.stderr[-3000:])
    assert "Missing specific R3 uses fixed real Sachversicherungen parent" in res.stdout
    assert "Unverified Tarifcheck creative NEVER becomes a generic insurance banner" in res.stdout
# Recheck existing RC38 format and zero-upscale on the same source output.
old=(R/"AFFILIATE/RC38_PFERDE_CENTRAL_FORMAT/qa_rc38.py").read_text()
old=old.replace("0.1.35-rc38","0.1.36-rc39")
old=old.replace("ppar_hab_rc38_tarifcheck_reconcile_v1","ppar_hab_rc39_tarifcheck_reconcile_v1")
# The historical RC37 gate was replaced exactly once with RC39 as well.
# Preserve the historical RC37 source assertion; its replacement target
# is already RC39 from the two lines above.
with TemporaryDirectory() as td:
    p=Path(td)/"qa_rc38_on_rc39.py"
    p.write_text(old)
    res=run([sys.executable,str(p)],capture_output=True,text=True)
    print(res.stdout[-3000:])
    if res.returncode:print(res.stderr)
    assert res.returncode==0,(res.stdout[-9000:],res.stderr[-2500:])
print("RC39_REAL_ORIGINAL_PHP_FIXED_MAPPING_AND_RC38_REGRESSION_PASS")
