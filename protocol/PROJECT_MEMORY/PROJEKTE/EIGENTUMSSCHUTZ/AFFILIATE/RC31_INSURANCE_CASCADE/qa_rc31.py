#!/usr/bin/env python3
"""HAB RC31 real PHP regression: insurance banner R1/R2/R3/leaf ancestry,
no cross-selling, no generic contamination, stored-original reclassification
without new imports, existing Idealo products/GTIN untouched.
"""
from pathlib import Path
from zipfile import ZipFile
from tempfile import TemporaryDirectory
from subprocess import run
import re, hashlib
R=Path("protocol/PROJECT_MEMORY/PROJEKTE/EIGENTUMSSCHUTZ")
P=R/"PLUGINS/ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip"
with ZipFile(P) as z:
    assert z.testzip() is None and len(z.namelist())==36
    t=z.read("affiliate-portal-router/includes/trait-ppar-output-objects.php").decode()
    main=z.read("affiliate-portal-router/affiliate-portal-router.php").decode()
    idealo=z.read("affiliate-portal-router/includes/trait-ppar-idealo.php").decode()
    assert "Version: 0.1.28-rc31" in main
    assert "hb_rc31_reconcile_stored_tarifcheck_once" in main
    assert "Idealo-Feedabdeckung" in idealo
    assert "Nur bei Idealo ohne nachgewiesenen Feedtreffer" in idealo
    assert "'core:world:insurance'" in t
    assert "hab_insurance_specific_verified" in t
    assert "hab_insurance_general_verified" in t

    def m(name):
        pat=re.compile(r"(?:public|private|protected)(?:\s+static)?\s+function\s+"+re.escape(name)+r"\s*\(")
        match=pat.search(t)
        assert match,name
        p=t.index("{",match.end());depth=0
        for i in range(p,len(t)):
            if t[i]=="{":depth+=1
            elif t[i]=="}":
                depth-=1
                if depth==0:
                    return t[match.start():i+1].replace("private function","public function",1)
        raise AssertionError(name)
    methods="\n".join(m(n) for n in [
        "output_text","output_comparison_banner_partner",
        "output_tarifcheck_banner_family","output_destination_semantic_text",
        "output_campaign_target_key","hb_rc31_insurance_banner_plan",
        "output_assign_banner_targets_from_destination_once",
        "output_banner_stored_destination_classification",
        "output_banner_library_records","output_resolve_target_key",
        "output_target_key_matches","output_target_identity_keys",
        "output_banner_target_path_keys","hb_rc31_reconcile_stored_tarifcheck_once"
    ])
    harness=r'''<?php
define('ARRAY_A','ARRAY_A');
function absint($x){return abs((int)$x);}
function sanitize_key($x){return strtolower(preg_replace('/[^a-z0-9_\-]/','',strtolower((string)$x)));}
function sanitize_text_field($x){return trim(strip_tags((string)$x));}
function wp_strip_all_tags($x){return strip_tags((string)$x);}
function remove_accents($x){return str_replace(
  array('ä','ö','ü','ß','Ä','Ö','Ü'),
  array('ae','oe','ue','ss','Ae','Oe','Ue'),(string)$x);}
function esc_url_raw($x){return (string)$x;}
function wp_parse_url($x,$what=-1){return parse_url($x,$what);}
function wp_json_encode($x,$flags=0){return json_encode($x,$flags);}
function is_wp_error($x){return false;}
function current_user_can($s){return true;}
function is_admin(){return true;}
function get_option($k,$d=null){return $GLOBALS['opts'][$k]??$d;}
function update_option($k,$v,$a=false){$GLOBALS['opts'][$k]=$v;}
function ok($condition,$name) {if(!$condition){fwrite(STDERR,"FAIL: ".$name."\n");exit(2);}echo "PASS: ".$name."\n";}
class PPAR_HB_Integration {public static function verified_nodes(){return $GLOBALS['nodes'];}}
class TestDB {
  public $rows=array(),$saved=array(),$prefix='wp_';
  public function prepare($sql,...$args){return vsprintf(str_replace(array('%d','%s'),array('%d',"'%s'"),$sql),$args);}
  public function update($table,$values,$where){
     $id=(int)$where['id']; $this->saved[$id]=$values;
     foreach($this->rows as &$r)if($r['id']===$id){$r=array_merge($r,$values);}
     return 1;
  }
  public function get_results($sql,$type) {
     preg_match('/id>(\d+)/',$sql,$m);$last=(int)($m[1]??0);
     preg_match('/LIMIT (\d+)/',$sql,$n);$limit=(int)($n[1]??60);
     return array_slice(array_values(array_filter($this->rows,fn($x)=>$x['id']>$last)),0,$limit);
  }
}
$GLOBALS['wpdb']=new TestDB();
$GLOBALS['opts']=array();
$GLOBALS['nodes']=array(
 'core:world:insurance'=>array('id'=>'core:world:insurance','parent'=>'','type'=>'page',
    'name'=>'Versicherungen','slug'=>'versicherungen','wp_id'=>100),
 'ins:r2:kfz'=>array('id'=>'ins:r2:kfz','parent'=>'core:world:insurance','type'=>'page',
    'name'=>'Kfz-Versicherungen','slug'=>'kfz-versicherungen','wp_id'=>101),
 'ins:r3:moto'=>array('id'=>'ins:r3:moto','parent'=>'ins:r2:kfz','type'=>'page',
    'name'=>'Motorradversicherung','slug'=>'motorradversicherung','wp_id'=>102),
 'ins:leaf:moto'=>array('id'=>'ins:leaf:moto','parent'=>'ins:r3:moto','type'=>'category',
    'name'=>'Motorrad vergleichen','slug'=>'motorrad-vergleichen','wp_id'=>103),
 'ins:r3:auto'=>array('id'=>'ins:r3:auto','parent'=>'ins:r2:kfz','type'=>'page',
    'name'=>'Autoversicherung','slug'=>'autoversicherung','wp_id'=>104),
 'ins:leaf:auto'=>array('id'=>'ins:leaf:auto','parent'=>'ins:r3:auto','type'=>'category',
    'name'=>'Autoversicherung Kosten','slug'=>'auto-kosten','wp_id'=>105),
 'ins:r2:sach'=>array('id'=>'ins:r2:sach','parent'=>'core:world:insurance','type'=>'page',
    'name'=>'Sachversicherungen','slug'=>'sachversicherungen','wp_id'=>110),
 'ins:r3:hausrat'=>array('id'=>'ins:r3:hausrat','parent'=>'ins:r2:sach','type'=>'page',
    'name'=>'Hausratversicherung','slug'=>'hausratversicherung','wp_id'=>111),
 'ins:leaf:hausrat'=>array('id'=>'ins:leaf:hausrat','parent'=>'ins:r3:hausrat','type'=>'category',
    'name'=>'Hausrat vergleichen','slug'=>'hausrat-vergleichen','wp_id'=>112),
 'other:world'=>array('id'=>'other:world','parent'=>'','type'=>'page',
    'name'=>'Wasser und Feuchtigkeit','slug'=>'wasser-und-feuchtigkeit','wp_id'=>200),
 'other:leaf'=>array('id'=>'other:leaf','parent'=>'other:world','type'=>'category',
    'name'=>'Wassermelder vergleichen','slug'=>'wassermelder-vergleichen','wp_id'=>201),
);
$GLOBALS['targets']=array();
foreach($GLOBALS['nodes'] as $node){
 $GLOBALS['targets'][]=array('type'=>$node['type'],'key'=>$node['type'].':'.$node['wp_id'],
   'id'=>$node['wp_id'],'slug'=>$node['slug'],'label'=>$node['name'],
   'context'=>$node['type']==='category'?'leaf_category':'page','depth'=>2);
}
class ActualCodeHarness {
  public function creative_library_table(){return 'wp_ppar_creative_library';}
  public function output_portal_registry(){return array('hab'=>array('key'=>'hab','local'=>true,
     'enabled'=>true,'banner_target_types'=>array('page','category')));}
  public function output_portal_targets($portal){return $GLOBALS['targets'];}
  public function output_banner_destination_source($row){return 'provider_explicit';}
  public function control_prime_portal_decision_cache($portal,$force){return true;}
  public function control_target_gate($portal,$key){return true;}
  public function output_plan_creative($row,$materialize){$GLOBALS['planned'][]=$row;return array();}
  public function output_banner_import_classification($row,$portal,$targets){return null;}
  METHODS
}
$portal=array('key'=>'hab','local'=>true,'enabled'=>true,'banner_target_types'=>array('page','category'));
$o=new ActualCodeHarness;
function banner($path,$title='') {
  return array('id'=>55,'creative_type'=>'banner','partner_name'=>'Tarifcheck',
    'partner_external_id'=>'tarifcheck',
    'destination_url'=>'https://www.tarifcheck.de/'.$path,
    'tracking_url'=>'https://www.tarifcheck.de/link',
    'title'=>$title,'description'=>'','tags'=>'',
    'payload'=>json_encode(array('_destination_source'=>'provider_explicit',
           '_dimension_state'=>'verified','title_source'=>'manual')),
    'width'=>728,'height'=>90);
}
$motor=banner('motorradversicherung/','Motorradversicherung vergleichen');
$p=$o->hb_rc31_insurance_banner_plan($motor,$portal,$GLOBALS['targets'],array('page','category'));
ok($p['status']==='ready' && $p['target']['id']===102,
   'Motorcycle original chooses actual dedicated R3');
ok(in_array('page:motorradversicherung',$p['path_target_keys'],true)
   && in_array('category:motorrad-vergleichen',$p['path_target_keys'],true),
   'Same verified R3 banner goes down to its OWN leaf');
ok(!in_array('page:autoversicherung',$p['path_target_keys'],true)
   && !in_array('category:hausrat-vergleichen',$p['path_target_keys'],true)
   && !in_array('category:wassermelder-vergleichen',$p['path_target_keys'],true),
   'No motorcycle banner leaked into insurance siblings or physical products');
$mapped=$o->output_assign_banner_targets_from_destination_once($motor);
ok($mapped['updated']===1 && $mapped['mapped']===1 && count($mapped['targets'])===1,
   'Single stored verified branch record, no hundreds of duplicated ads');
ok(($mapped['targets'][0]['target_key']??'')==='page:102','Original banner assigned to real WP page ID');
$record=$motor;$record['topic_targets']=json_encode($mapped['targets']);
$stored=$o->output_banner_stored_destination_classification($record,$portal);
ok($stored['status']==='ready' && count($stored['_ppar_banner_target_keys'])===2,
   'Existing campaign materializer inherits exact R3 and its end category');
$haus=banner('hausratversicherung/','Hausratversicherung');
$p=$o->hb_rc31_insurance_banner_plan($haus,$portal,$GLOBALS['targets'],array('page','category'));
ok($p['target']['id']===111 && in_array('category:hausrat-vergleichen',$p['path_target_keys'],true)
   && !in_array('category:motorrad-vergleichen',$p['path_target_keys'],true),
   'Hausrat cascades only within Hausrat branch');
$generic=banner('versicherungsvergleich/','Alle Versicherungen vergleichen');
$p=$o->hb_rc31_insurance_banner_plan($generic,$portal,$GLOBALS['targets'],array('page','category'));
ok($p['target']['id']===100 && count($p['path_target_keys'])===9
   && in_array('page:autoversicherung',$p['path_target_keys'],true),
   'Only explicit general insurance comparison reaches all insurance descendants');
$wrong=banner('motorradversicherung/','Motorradversicherung und Hausratversicherung');
$p=$o->hb_rc31_insurance_banner_plan($wrong,$portal,$GLOBALS['targets'],array('page','category'));
ok($p['status']==='blocked','Conflicting specialty names do not fan out');
$unknown=banner('tarifcheck-werbung/','Tarifcheck Angebot');
$p=$o->hb_rc31_insurance_banner_plan($unknown,$portal,$GLOBALS['targets'],array('page','category'));
ok($p['status']==='blocked','Unknown creative gets NO automatic guess');
$fin=banner('kreditvergleich/','Kreditvergleich');
ok($o->hb_rc31_insurance_banner_plan($fin,$portal,$GLOBALS['targets'],array('page','category'))===null,
   'Finance type is outside insurance automatic routing; previous path unchanged');
$other=$motor;$other['partner_name']='idealo';$other['destination_url']='https://www.idealo.de/preisvergleich/tresor';
ok($o->hb_rc31_insurance_banner_plan($other,$portal,$GLOBALS['targets'],array('page','category'))===null,
   'Physical product provider unaffected');
$badportal=$portal;$badportal['local']=false;
ok($o->hb_rc31_insurance_banner_plan($motor,$badportal,$GLOBALS['targets'],array('page','category'))['status']==='blocked',
   'No changes to other portal instances');
$GLOBALS['wpdb']->rows=array();
for($i=1;$i<=65;$i++){$v=$motor;$v['id']=$i;$GLOBALS['wpdb']->rows[]=$v;}
$_GET['page']='affiliate-portal-creative-library';
$GLOBALS['planned']=array();
$o->hb_rc31_reconcile_stored_tarifcheck_once();
ok(count($GLOBALS['planned'])===60,'First admin request recalculates only 60 existing banner rows');
ok($GLOBALS['opts']['ppar_hab_rc31_tarifcheck_reconcile_v1']['cursor']===60,
   'Batch migration cursor saved without new database table');
$o->hb_rc31_reconcile_stored_tarifcheck_once();
ok(count($GLOBALS['planned'])===65 && !empty($GLOBALS['opts']['ppar_hab_rc31_tarifcheck_reconcile_v1']['complete']),
   'All 65 existing imported originals reclassified on second visit; no reimport');
$o->hb_rc31_reconcile_stored_tarifcheck_once();
ok(count($GLOBALS['planned'])===65,'Finished migration does not repeat on future visits');
echo "HAB_RC31_REAL_PHP_CONTRACT_PASS\n";
'''
    harness=harness.replace("METHODS",methods)
    with TemporaryDirectory() as d:
        phps=[n for n in z.namelist() if n.endswith(".php")]
        assert len(phps)==25
        for i,n in enumerate(phps):
            pp=Path(d)/f"{i}.php";pp.write_bytes(z.read(n))
            result=run(["php","-l",str(pp)],capture_output=True,text=True)
            assert result.returncode==0,(n,result.stdout,result.stderr)
        path=Path(d)/"qa.php"
        path.write_text(harness)
        result=run(["php","-l",str(path)],capture_output=True,text=True)
        assert result.returncode==0,(result.stdout,result.stderr)
        result=run(["php",str(path)],capture_output=True,text=True)
        print(result.stdout)
        assert result.returncode==0,(result.stdout,result.stderr)
        print("HAB_RC31_PHP_LINT_25_PASS")
print("HAB_RC31_QA_PASS",hashlib.sha256(P.read_bytes()).hexdigest())
