#!/usr/bin/env python3
"""One combined read-only regression of QA72 against QA73 with original PHP methods.
WordPress, eBay, and database faults are modelled; NO live acceptance.
"""
import subprocess, pathlib, json, hashlib, sys
P=pathlib.Path('/mnt/data/ebay_qa73')
B=pathlib.Path('/mnt/data/ebay_qa72/affiliate-portal-router/includes/trait-ppar-ebay-run.php')
N=P/'affiliate-portal-router/includes/trait-ppar-ebay-run.php'
R=pathlib.Path('/mnt/data/ebay_qa71/evidence/tests/QA50_REAL_FULL_PHASE_CHAIN.php')
S=P/'QA73_POST_COMMIT_REALISTIC_TEST.php'
C=P/'QA73_CLEANUP_LAST_WRITEFAIL_TEST.php'
errors=[];checks=0

def ck(v,reason):
 global checks
 checks+=1
 if not v:errors.append(reason)
def run(harness,trait,scenario):
 proc=subprocess.run(['php',str(harness),str(trait),scenario],text=True,capture_output=True,timeout=30)
 try:d=json.loads(proc.stdout)
 except Exception as ex:
  errors.append('non-JSON '+scenario+str(ex)+proc.stderr[-300:]);return {'bad':True,'raw':proc.stdout[-500:]}
 return d['summary']

before={};after={}
for scenario in ['normal','old_blocked','new_blocked','db_down','churn','no_new','save_fail']:
 x=run(R,B,scenario);y=run(R,N,scenario)
 before[scenario]=x;after[scenario]=y
 for fld in ['status','public_count','new_ids','lost_old_ids','error','selection_calls','families_covered_in_run']:
  ck(x.get(fld)==y.get(fld),'regression '+scenario+' '+fld+' '+str(x.get(fld))+' vs '+str(y.get(fld)))
 ck(y.get('status')==('failed' if scenario in ('db_down','save_fail') else 'completed'),'terminal mismatch '+scenario)

base_commit=run(S,B,'post_commit_state_save_fail')
fixed_commit=run(S,N,'post_commit_state_save_fail')
ck(base_commit['commit_transition_fail_injected'] and fixed_commit['commit_transition_fail_injected'],'real postcommit fault not injected')
ck(base_commit['public_writes']==3 and fixed_commit['public_writes']==2,'repeated publication not eliminated')
ck(fixed_commit['status']=='completed' and fixed_commit['error'] is None,'resume did not complete safely')
ck(fixed_commit['lost_old_ids']==0,'lost published old cards at resume')

base_cleanup=run(C,B,'cleanup_final_save_fail')
fixed_cleanup=run(C,N,'cleanup_final_save_fail')
ck(base_cleanup['cleanup_fail_injected'] and fixed_cleanup['cleanup_fail_injected'],'real cleanup fault not injected')
ck(base_cleanup['status']=='completed' and base_cleanup['error'] is None,'missing original false-green reproduction')
ck(fixed_cleanup['status']=='failed' and fixed_cleanup['error']=='checkpoint_business_cleanup_state_save_failed','failure incorrectly completed/hidden')
ck(fixed_cleanup['lost_old_ids']==0,'old safe inventory was lost')
ck(fixed_cleanup['public_count']==base_cleanup['public_count'],'published checkpoint changed on failed cleanup')

for trait in P.glob('affiliate-portal-router/**/*.php'):
 p=subprocess.run(['php','-l',str(trait)],capture_output=True,text=True,timeout=10)
 ck(p.returncode==0,'PHP parse '+str(trait))

changed=[];oldroot=pathlib.Path('/mnt/data/ebay_qa72/affiliate-portal-router')
for f in (P/'affiliate-portal-router').rglob('*'):
 if f.is_file():
  rel=f.relative_to(P/'affiliate-portal-router')
  if f.read_bytes() != (oldroot/rel).read_bytes():changed.append(str(rel))
ck(changed==['includes/trait-ppar-ebay-run.php'],'unexpected edited source files: '+str(changed))
report={
 'qa':'QA73', 'scope':'full QA72 end-to-end regression plus original-PHP storage-failure proof',
 'original_source_sha256':hashlib.sha256(B.read_bytes()).hexdigest(),
 'patched_source_sha256':hashlib.sha256(N.read_bytes()).hexdigest(),
 'changes_from_QA72':changed, 'existing_7_scenarios_before':before,'existing_7_scenarios_after':after,
 'post_commit_write_failure_original':base_commit,'post_commit_write_failure_fixed':fixed_commit,
 'final_cleanup_state_write_failure_original':base_cleanup,'final_cleanup_state_write_failure_fixed':fixed_cleanup,
 'checks':checks,'failed':errors,'local_pass':len(errors)==0, 'live_accepted':False,
 'limitations':'Historical eBay getItem, WP DB snapshot, live GH schedule, real public final checkpoint and cleanup absent. Scripts reproduce PHP methods with mocked WP and eBay, not live production.'
}
(P/'QA73_ZUSATZREGRESSION.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'checks':checks,'failures':errors,'old_postcommit_writes':base_commit['public_writes'],'fixed_postcommit_writes':fixed_commit['public_writes'],'old_cleanup':base_cleanup['status'],'fixed_cleanup':fixed_cleanup['status'],'changed':changed,'live_accepted':False},ensure_ascii=False))
sys.exit(bool(errors))