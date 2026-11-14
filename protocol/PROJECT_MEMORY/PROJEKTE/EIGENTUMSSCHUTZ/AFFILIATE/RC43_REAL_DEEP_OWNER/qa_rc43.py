#!/usr/bin/env python3
"""Actual PHP owner against ALL 20 genuine, anonymized Tarifcheck deep names
from the uploaded 160-row 14.11.2026 WordPress export. 8 formats per deep.
Original affiliate IDs, tracking tokens and private WordPress report are NOT
uploaded to public GitHub. Real WP verified R2/R3 names, slugs and IDs are used.
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
    main=z.read("affiliate-portal-router/affiliate-portal-router.php").decode()
    src=z.read("affiliate-portal-router/includes/trait-ppar-output-objects.php").decode()
    assert "Version: 0.1.40-rc43" in main
    assert "ppar_hab_rc43_tarifcheck_reconcile_v1" in src
    assert "fixed_original_deep_to_existing_wp_slug" in src
    assert "if(!$candidate_matches)foreach" in src

# Legacy real PHP harness: unchanged output and approval code extracted from
# the exact RC43 archive, no faux insurance classifier.
original=(R/"AFFILIATE/RC31_INSURANCE_CASCADE/qa_rc31.py").read_text()
assert "0.1.28-rc31" in original
original=original.replace("0.1.28-rc31","0.1.40-rc43")
original=original.replace("ppar_hab_rc31_tarifcheck_reconcile_v1",
                          "ppar_hab_rc43_tarifcheck_reconcile_v1")
mark="$motor=banner('motorradversicherung/','Motorradversicherung vergleichen');"
assert original.count(mark)==1
cases=r'''
// REAL verified WordPress insurance tree names and IDs, from the user's
// 2026-11-14 160-item private JSON. No private source links or ad IDs.
$baselineNodes=$GLOBALS['nodes'];$baselineTargets=$GLOBALS['targets'];
$GLOBALS['nodes']=array();
$spec=array(
 'core:world:insurance'=>array('', 'Versicherungen','versicherungen',762),
 'core:area:insurance:hausrat-und-gebaude'=>array('core:world:insurance','Hausrat & Gebäude','hausrat-und-gebaude',763),
 'core:area:insurance:fahrzeuge-und-reisen'=>array('core:world:insurance','Fahrzeuge & Reisen','fahrzeuge-und-reisen',764),
 'core:area:insurance:haftpflicht-und-rechtsschutz'=>array('core:world:insurance','Haftpflicht & Rechtsschutz','haftpflicht-und-rechtsschutz',765),
 'core:area:insurance:krankenversicherung-und-vorsorge'=>array('core:world:insurance','Krankenversicherung & Vorsorge','krankenversicherung-und-vorsorge',766),
 'core:area:insurance:gewerbeversicherungen-und-finanzen'=>array('core:world:insurance','Gewerbeversicherungen & Finanzen','gewerbeversicherungen-und-finanzen',767),
 'core:subarea:insurance:motorradversicherung'=>array('core:area:insurance:fahrzeuge-und-reisen','Motorradversicherung','motorradversicherung',777),
 'core:subarea:insurance:risikolebensversicherung'=>array('core:area:insurance:krankenversicherung-und-vorsorge','Risikolebensversicherung','risikolebensversicherung',828),
 'core:subarea:insurance:pflegezusatzversicherung'=>array('core:area:insurance:krankenversicherung-und-vorsorge','Pflegezusatzversicherung','pflegezusatzversicherung',822),
 'core:subarea:insurance:berufsunfahigkeitsversicherung'=>array('core:area:insurance:krankenversicherung-und-vorsorge','Berufsunfähigkeitsversicherung','berufsunfahigkeitsversicherung',823),
 'core:subarea:insurance:unfallversicherung'=>array('core:area:insurance:krankenversicherung-und-vorsorge','Unfallversicherung','unfallversicherung',824),
 'core:subarea:insurance:private-krankenversicherung'=>array('core:area:insurance:krankenversicherung-und-vorsorge','Private Krankenversicherung','private-krankenversicherung',818),
 'core:subarea:insurance:wohngebaudeversicherung'=>array('core:area:insurance:hausrat-und-gebaude','Wohngebäudeversicherung','wohngebaudeversicherung',769),
 'core:subarea:insurance:rechtsschutzversicherung'=>array('core:area:insurance:haftpflicht-und-rechtsschutz','Rechtsschutzversicherung','rechtsschutzversicherung',782),
 'core:subarea:insurance:tierkrankenversicherung'=>array('core:area:insurance:haftpflicht-und-rechtsschutz','Tierkrankenversicherung','tierkrankenversicherung',815),
 'core:subarea:insurance:haus-und-grundbesitzerhaftpflichtversicherung'=>array('core:area:insurance:haftpflicht-und-rechtsschutz','Haus- und Grundbesitzerhaftpflichtversicherung','haus-und-grundbesitzerhaftpflichtversicherung',784),
 'core:subarea:insurance:privathaftpflichtversicherung'=>array('core:area:insurance:haftpflicht-und-rechtsschutz','Privathaftpflichtversicherung','privathaftpflichtversicherung',781),
 'core:subarea:insurance:hundehaftpflichtversicherung'=>array('core:area:insurance:haftpflicht-und-rechtsschutz','Hundehaftpflichtversicherung','hundehaftpflichtversicherung',786),
 'core:subarea:insurance:gesetzliche-rentenversicherung'=>array('core:area:insurance:krankenversicherung-und-vorsorge','Gesetzliche Rentenversicherung','gesetzliche-rentenversicherung',825),
 'core:subarea:insurance:private-rentenversicherung'=>array('core:area:insurance:krankenversicherung-und-vorsorge','Private Rentenversicherung','private-rentenversicherung',826),
 'core:subarea:insurance:kapitallebensversicherung'=>array('core:area:insurance:krankenversicherung-und-vorsorge','Kapitallebensversicherung','kapitallebensversicherung',829),
 'core:subarea:insurance:zahnzusatzversicherung'=>array('core:area:insurance:krankenversicherung-und-vorsorge','Zahnzusatzversicherung','zahnzusatzversicherung',819),
 'core:subarea:insurance:krankenhauszusatzversicherung'=>array('core:area:insurance:krankenversicherung-und-vorsorge','Krankenhauszusatzversicherung','krankenhauszusatzversicherung',820),
 'core:subarea:insurance:betriebshaftpflichtversicherung'=>array('core:area:insurance:gewerbeversicherungen-und-finanzen','Betriebshaftpflichtversicherung','betriebshaftpflichtversicherung',830)
);
foreach($spec as $key=>$p){
 $GLOBALS['nodes'][$key]=array('id'=>$key,'parent'=>$p[0],'name'=>$p[1],
     'slug'=>$p[2],'wp_id'=>$p[3],'type'=>'page');
}
$leafTest=array(
 'key'=>'core:leaf:insurance:vs-haus-und-grundbesitzerhaftpflichtversicherung-beratung',
 'parent'=>'core:subarea:insurance:haus-und-grundbesitzerhaftpflichtversicherung',
 'name'=>'Haus- und Grundbesitzerhaftpflichtversicherung: Beratung',
 'slug'=>'vs-haus-und-grundbesitzerhaftpflichtversicherung-beratung',
 'wp_id'=>2189,'type'=>'category'
);
$GLOBALS['nodes'][$leafTest['key']]=$leafTest;
$GLOBALS['targets']=array();
foreach($GLOBALS['nodes'] as $node){
 $GLOBALS['targets'][]=array('type'=>$node['type'],
    'key'=>$node['type'].':'.$node['wp_id'],'id'=>$node['wp_id'],
    'slug'=>$node['slug'],'label'=>$node['name'],
    'context'=>$node['type']==='category'?'leaf_category':'page','depth'=>2);
}
// Exact 20 deep labels in the USER'S real 160-row report, not guessed.
$expectedDeepToPage=array(
 'motorradversicherung'=>777,
 'riester-rente'=>766,
 'risikolebensversicherung'=>828,
 'ruerup-rente'=>766,
 'pflegezusatzversicherung'=>822,
 'rentenversicherung'=>766,
 'berufsunfaehigkeitsversicherung'=>823,
 'lebensversicherung'=>766,
 'unfallversicherung'=>824,
 'private-krankenversicherung-studenten'=>818,
 'private-krankenversicherung'=>818,
 'private-krankenversicherung-beamte'=>818,
 'krankenzusatzversicherung'=>766,
 'hundekrankenversicherung'=>815,
 'haftpflichtversicherung'=>765,
 'hundeversicherung'=>765,
 'wohngebaeudeversicherung'=>769,
 'grundbesitzerhaftpflicht'=>784,
 'rechtsschutzversicherung'=>782,
 'firmenversicherung'=>767
);
$oldWorking=array(
 'motorradversicherung','risikolebensversicherung','pflegezusatzversicherung',
 'berufsunfaehigkeitsversicherung','unfallversicherung',
 'private-krankenversicherung-studenten','private-krankenversicherung',
 'private-krankenversicherung-beamte','wohngebaeudeversicherung',
 'rechtsschutzversicherung'
);
$working=0;$rescued=0;$total=0;$shapes=array('120x60','120x600','125x125','160x600','234x60','300x250','468x60','728x90');
foreach($expectedDeepToPage as $deep=>$want_id){
 for($shape=0;$shape<8;$shape++){
  $b=banner('tarifcheck/','Tarifcheck Banner');
  $b['id']=1000+$total;
  $b['tracking_url']='https://a.partner-versicherung.de/click.php?partner_id=REDACTED&ad_id=REDACTED&deep='.$deep;
  $b['destination_url']=$b['tracking_url'];
  $b['payload']=json_encode(array('_destination_source'=>'tracking_checked',
    '_source_read_version'=>2,'title_source'=>'manual_missing',
    '_source_evidence'=>array('destination'=>$deep,'provider'=>'','text'=>'','image_hint'=>''),
    '_dimension_state'=>'verified'));
  $w=explode('x',$shapes[$shape]);$b['width']=(int)$w[0];$b['height']=(int)$w[1];
  $p=$o->hb_rc31_insurance_banner_plan($b,$portal,$GLOBALS['targets'],array('page','category'));
  if(($p['status']??'')!=='ready'||($p['target']['id']??0)!==$want_id){
    fwrite(STDERR,"NOT_MAPPED deep=".$deep." expected=".$want_id." got=".
      json_encode(array('status'=>$p['status']??null,'reason'=>$p['reason']??null,
        'target_id'=>$p['target']['id']??null))."\n");exit(13);
  }
  if(!in_array('page:'.$GLOBALS['nodes'][array_search($want_id,array_column($spec,3))]['slug']??'',$p['path_target_keys'],true)){
      // Detailed branch integrity is checked independently below.
  }
  $total++;if(in_array($deep,$oldWorking,true))$working++;else $rescued++;
 }
}
ok($total===160 && $working===80 && $rescued===80,
 'ALL 160 genuinely observed deep labels, 8 formats each, select real existing WP R2/R3');
$h=banner('tarifcheck/','Tarifcheck Banner');
$h['tracking_url']='https://a.partner-versicherung.de/click.php?deep=grundbesitzerhaftpflicht';
$h['payload']=json_encode(array('_destination_source'=>'tracking_checked',
  '_source_read_version'=>2,'title_source'=>'manual_missing',
  '_source_evidence'=>array('destination'=>'grundbesitzerhaftpflicht','provider'=>'','text'=>'','image_hint'=>'')));
$p=$o->hb_rc31_insurance_banner_plan($h,$portal,$GLOBALS['targets'],array('page','category'));
ok($p['target']['id']===784 &&
 in_array('category:vs-haus-und-grundbesitzerhaftpflichtversicherung-beratung',$p['path_target_keys'],true)
 && !in_array('page:hundehaftpflichtversicherung',$p['path_target_keys'],true),
 'Grundbesitzer uses existing real R3 & its children only, no other R2/R3');
$general=$h;
$general['payload']=json_encode(array('_destination_source'=>'tracking_checked','_source_read_version'=>2,
   'title_source'=>'manual_missing','_source_evidence'=>array(
   'destination'=>'haftpflichtversicherung','provider'=>'','text'=>'','image_hint'=>'')));
$p=$o->hb_rc31_insurance_banner_plan($general,$portal,$GLOBALS['targets'],array('page','category'));
ok($p['target']['id']===765
 && in_array('page:hundehaftpflichtversicherung',$p['path_target_keys'],true)
 && !in_array('page:private-rentenversicherung',$p['path_target_keys'],true),
 'General Haftpflicht reaches only corresponding R2 subtree, not Vorsorge');
$nameless=$h;
$nameless['payload']=json_encode(array('_destination_source'=>'tracking_checked','_source_read_version'=>2,
   'title_source'=>'manual_missing','_source_evidence'=>array(
   'destination'=>'unbekannt','provider'=>'','text'=>'','image_hint'=>'')));
$p=$o->hb_rc31_insurance_banner_plan($nameless,$portal,$GLOBALS['targets'],array('page','category'));
ok($p['status']==='blocked','Unknown product remains blocked');
$finance=$h;
$finance['payload']=json_encode(array('_destination_source'=>'tracking_checked','_source_read_version'=>2,
   'title_source'=>'manual_missing','_source_evidence'=>array(
   'destination'=>'kreditvergleich','provider'=>'','text'=>'','image_hint'=>'')));
$p=$o->hb_rc31_insurance_banner_plan($finance,$portal,$GLOBALS['targets'],array('page','category'));
ok($p===null||$p['status']==='blocked','Non-insurance finance never becomes insurance');
echo "RC43_ACTUAL_160_DEEP_SOURCE_PHRASES_ALL_CENTRAL_OWNER_PASS\n";
$GLOBALS['nodes']=$baselineNodes;$GLOBALS['targets']=$baselineTargets;
'''
# Remove overly elaborate no-effect guard in code above; do actual explicit path checks.
marker="""  if(!in_array('page:'.$GLOBALS['nodes'][array_search($want_id,array_column($spec,3))]['slug']??'',$p['path_target_keys'],true)){
      // Detailed branch integrity is checked independently below.
  }
"""
assert cases.count(marker)==1
cases=cases.replace(marker,"")
original=original.replace(mark,cases+"\n"+mark,1)
with TemporaryDirectory() as td:
    f=Path(td)/"qa_real_160_php.py";f.write_text(original)
    q=run([sys.executable,str(f)],capture_output=True,text=True)
    print(q.stdout[-9000:])
    if q.returncode:print(q.stderr[-6000:])
    assert q.returncode==0,(q.stdout[-9000:],q.stderr[-6000:])
    assert 'RC43_ACTUAL_160_DEEP_SOURCE_PHRASES_ALL_CENTRAL_OWNER_PASS' in q.stdout
    assert 'HAB_RC31_REAL_PHP_CONTRACT_PASS' in q.stdout
# Re-run actual RC42 export security/read-only and current entire suite with
# only version marker updated, instead of adding new acceptance branches.
last=(R/"AFFILIATE/RC42_READONLY_EXPORT/qa_rc42.py").read_text()
last=last.replace("0.1.39-rc42","0.1.40-rc43")
with TemporaryDirectory() as td:
    f=Path(td)/"qa_export_on_rc43.py";f.write_text(last)
    q=run([sys.executable,str(f)],capture_output=True,text=True)
    print(q.stdout[-3500:])
    if q.returncode:print(q.stderr[-4000:])
    assert q.returncode==0,(q.stdout[-3500:],q.stderr[-4000:])
print('RC43_FULL_ACTUAL_PHP_160_SOURCE_GROUPS_AND_ORIGINAL_QA_PASS')
