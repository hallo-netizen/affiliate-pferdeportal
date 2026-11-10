from pathlib import Path
import subprocess,json,hashlib,re
R=Path('/mnt/data/ebay_qa5_verified')
Q6=R/'inspectqa6/affiliate-portal-router/includes'
Q7=R/'inspectqa7/affiliate-portal-router/includes'
T=R/'qa6_tests'
OUT=R/'qa7_tests'
OUT.mkdir(exist_ok=True)
paths=['EBAY_319_KISS_16_KANONISCHE_TESTS_20261110.php','EBAY_319_KISS_QA2_TEST_EINZELFEHLER_20261110.php','EBAY_319_KISS_QA3_TEST_EFFIZIENZ_20261110.php','EBAY_KISS_TEST_END_TO_END_MOCK_20261110.php','EBAY_KISS_TEST_PERSISTENZ_20261110.php']
results=[]
for filename in paths:
    txt=(T/filename).read_text()
    txt=txt.replace('/mnt/data/ebay_kiss_single_workflow_stage/affiliate-portal-router/includes/',str(Q7)+'/')
    txt=txt.replace('/mnt/data/ebay_kiss_opt_stage/affiliate-portal-router/includes/',str(Q7)+'/')
    txt=txt.replace('/mnt/data/ebay_kiss_integrated_stage/affiliate-portal-router/includes/',str(Q7)+'/')
    assert '/mnt/data/ebay_kiss_' not in txt, filename
    target=OUT/filename
    target.write_text(txt)
    p=subprocess.run(['php',str(target)],capture_output=True,text=True,timeout=35)
    if p.returncode: print('FAILED',filename,p.stdout[-400:],p.stderr[-900:]);raise SystemExit(1)
    match=re.findall(r'(\d+)/(\d+) PASS',p.stdout)
    num=sum(int(a) for a,b in match) if match else None
    results.append({'case':filename,'pass':True,'individual_checks':num,'last_line':p.stdout.strip().split('\n')[-1]})
print('FACHPROBEN:')
for x in results: print(x)
assert sum(x['individual_checks'] or 0 for x in results)==61
# 13 direct parity tests, same existing original PHP test files, QA6 vs QA7
parity=[]
for script,kind,scenarios in [
('EBAY_KISS_QA4_TEST_PARITAET_20261110.php','trait-ppar-ebay-run.php',['normal','allow','source-error','creative-error']),
('EBAY_319_KISS_QA5_TEST_PRUNE_PARITAET_20261110.php','trait-ppar-ebay.php',['gapfill','gapfill_empty','gapfill_resume','gapfill_single','gapfill_sparse_tail','checkpoint_gapfill','full','checkpoint','error'])]:
 for s in scenarios:
  vals=[]
  for d in (Q6,Q7):
   args=['php',str(T/script),str(d/kind)]
   if s!='normal':args.append(s)
   p=subprocess.run(args,capture_output=True,text=True,timeout=35)
   if p.returncode: print('PARITY_FAIL',script,s,d,p.stderr[-1000:]);raise SystemExit(1)
   vals.append(json.loads(p.stdout))
  if vals[0]!=vals[1]:
   print('PARITY_DIFFERENCE',script,s,vals[0],vals[1]);raise SystemExit(2)
  parity.append({'scenario':s,'source':kind,'identical':True})
print('PARITY:',len(parity),'PASSED')
# Typed input and no extra WordPress option read on verified save.
probetpl='''<?php
error_reporting(E_ALL); define('ABSPATH','/');
$GLOBALS['opts']=[]; $GLOBALS['reads']=0;$GLOBALS['fake_refuse']=false;
function get_option($k,$d=false){$GLOBALS['reads']++;return $GLOBALS['opts'][$k]??$d;}
function update_option($k,$v,$autoload=false){if($GLOBALS['fake_refuse'])return false;$GLOBALS['opts'][$k]=$v;return true;}
function absint($x){return abs((int)$x);}
function sanitize_key($x){return strtolower(preg_replace('/[^a-z0-9_-]/','',strtolower((string)$x)));}
function sanitize_text_field($x){return trim((string)$x);}
require '{src}';
class Probe{{use PPAR_Ebay_Run_Trait; const EBAY_RUNTIME_BUILD='qa';
 public function put($k,$v){{return $this->ebay_run_phase_state_save($k,$v);}}
 public function get(){{return $this->ebay_run_load();}}
}}
$x=new Probe();$out=[];
$cases=[['valid',['cursor'=>3],false,true],['empty',[],false,true],['null',null,false,true],['scalar',5,false,true],['badobject',(object)['cursor'=>3],false,true],['refused',['cursor'=>33],true,true],['missing-schema',['cursor'=>5],false,false],['bad-key',['cursor'=>9],false,true]];
foreach($cases as [$label,$value,$refuse,$schema]){{
 $GLOBALS['opts']=$schema?['ppar_ebay_run_state_v1'=>['schema'=>'1.0','status'=>'running','run_uuid'=>'abc']]:[];
 $GLOBALS['reads']=0;$GLOBALS['fake_refuse']=$refuse;
 $res=$x->put($label==='bad-key'?'':$label,$value);
 $out[]=['case'=>$label,'result'=>$res,'stored'=>$GLOBALS['opts'],'reads'=>$GLOBALS['reads']];
}}
echo json_encode($out);
'''
opts=[]
for d in (Q6,Q7):
 pfile=OUT/('phase_probe_'+('qa6' if d==Q6 else 'qa7')+'.php')
 pfile.write_text(probetpl.replace('{src}',str(d/'trait-ppar-ebay-run.php')).replace('{{','{').replace('}}','}'))
 p=subprocess.run(['php',str(pfile)],capture_output=True,text=True)
 if p.returncode:print('STATE_PROBE_FAIL',p.stderr);raise SystemExit(1)
 opts.append(json.loads(p.stdout))
for a,b in zip(*opts):
 assert a['case']==b['case'] and a['result']==b['result'] and a['stored']==b['stored'],(a,b)
 if a['case'] in ('valid','empty','null','scalar','badobject'): assert a['reads']-b['reads']==1,(a,b)
 else:assert a['reads']==b['reads'],(a,b)
print('STATE_SAVE_PARITY:',len(opts[0]),'PASSED; second read eliminated on 5 successful writes')
result={'qa7_php_tests':results,'qa6_qa7_existing_tests_parity':parity,'qa6_qa7_persistence_cases':[{'case':a['case'],'q6_reads':a['reads'],'q7_reads':b['reads'],'return_same':True,'state_same':True} for a,b in zip(*opts)],'all_pass':True,'wordpress_real_test':False}
(R/'EBAY_319_KISS_QA7_REGRESSION_20261110.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))