#!/usr/bin/env python3
"""QA74 combined proof; original PHP helpers for SAFE and membership, no live claims."""
import json, pathlib, subprocess, hashlib, difflib, sys
p=pathlib.Path('/mnt/data/ebay_qa74')
prev=pathlib.Path('/mnt/data/ebay_qa73/affiliate-portal-router/includes/trait-ppar-ebay-run.php')
fixed=p/'affiliate-portal-router/includes/trait-ppar-ebay-run.php'
checks=0;errors=[];tests=[]
def ck(v,why):
 global checks
 checks+=1
 if not v:errors.append(why)
def run(test,src,scenario=None):
 args=['php',str(test),str(src)]
 if scenario:args.append(scenario)
 q=subprocess.run(args,capture_output=True,text=True,timeout=60)
 try: val=json.loads(q.stdout)
 except Exception as e:
  errors.append(f'Invalid JSON {test} {scenario} {e}: {q.stdout[-200:]} {q.stderr[-200:]}'); return None
 return val
# The former QA73 mock silently ignored the real safe-checkpoint condition.
# This modified copy uses the unchanged PHP helpers from the actual trait.
mem_before=run(p/'QA74_MEMBERSHIP_REAL_HELPERS_TEST.php',prev)
mem_after=run(p/'QA74_MEMBERSHIP_REAL_HELPERS_TEST.php',fixed)
ck(mem_before is not None and mem_after is not None,'direct membership tests callable')
if mem_before and mem_after:
 ck(mem_before['same_run_same_membership']['writes']==1,'original duplicate-commit failure not reproduced')
 ck(mem_after['same_run_same_membership']['writes']==0,'corrected identical membership rewritten')
 for c in ['same_run_different_membership','different_run_same_membership','different_source_same_membership']:
  ck(mem_before[c]['writes']==mem_after[c]['writes']==1,f'new source/run blocked: {c}')
 ck(mem_after['same_run_same_membership']['checkpoint_id']=='already-final','existing final checkpoint ID not reused')
 ck(mem_after['same_run_same_membership']['published_count']==578,'old safe membership lost in reuse')
for scenario in ['normal','old_blocked','new_blocked','db_down','churn','no_new','save_fail','post_commit_state_save_fail']:
 old=run(p/'QA74_REAL_HELPERS_TEST.php',prev,scenario)
 new=run(p/'QA74_REAL_HELPERS_TEST.php',fixed,scenario)
 ck(old is not None and new is not None,'full real-helper scenario output '+scenario)
 if not old or not new: continue
 a,b=old['summary'],new['summary']
 for key in ['status','last_phase','public_count','new_ids','lost_old_ids','selection_calls','error','families_covered_in_run']:
  ck(a.get(key)==b.get(key),'scenario regression '+scenario+' '+key)
 if scenario=='post_commit_state_save_fail':
  ck(a['public_writes']==3 and b['public_writes']==2,'original duplicated publication not fixed')
  ck(a['commit_transition_fail_injected'] and b['commit_transition_fail_injected'],'postcommit save failure not injected')
 else:ck(a['public_writes']==b['public_writes'],'unexpected published write '+scenario)
 tests.append({'scenario':scenario,'before':{k:a.get(k) for k in ['status','error','public_writes','public_count','lost_old_ids']},'after':{k:b.get(k) for k in ['status','error','public_writes','public_count','lost_old_ids']}})
# The second lost-save path caused a false-green terminal state.
old=run(p/'QA74_DEFERRED_SAVE_TEST.php',prev,'deferred_save_fail')
new=run(p/'QA74_DEFERRED_SAVE_TEST.php',fixed,'deferred_save_fail')
if old and new:
 a,b=old['summary'],new['summary']
 ck(a['commit_transition_fail_injected'] and b['commit_transition_fail_injected'],'deferred save loss not injected')
 ck(a['status']=='completed' and a['error'] is None,'original false green not reproduced')
 ck(b['status']=='failed' and b['error']=='unverified_search_deferred_state_save_failed','deferred failure incorrectly reported completed')
 ck(a['lost_old_ids']==b['lost_old_ids']==0,'old safe inventory was removed')
 ck(a['public_count']==b['public_count'],'unchanged public safe shelf was replaced')
 tests.append({'scenario':'deferred_save_fail','before':{k:a.get(k) for k in ['status','error','public_writes','public_count','lost_old_ids']},'after':{k:b.get(k) for k in ['status','error','public_writes','public_count','lost_old_ids']}})
# Keep QA73 cleanup-failure fix; no new helper, worker or DB table.
clean=run(pathlib.Path('/mnt/data/ebay_qa73/QA73_CLEANUP_LAST_WRITEFAIL_TEST.php'),fixed,'cleanup_final_save_fail')
if clean:
 a=clean['summary']
 ck(a.get('status')=='failed' and a.get('error')=='checkpoint_business_cleanup_state_save_failed','cleanup false green regressed')
 ck(a.get('lost_old_ids')==0,'cleanup removed last-good membership')
 ck(a.get('cleanup_fail_injected') is True,'cleanup storage failure not injected')
 tests.append({'scenario':'cleanup_final_save_fail','after':{k:a.get(k) for k in ['status','error','public_count','lost_old_ids']}})
# One bundled source change beyond QA73; all other PHP files identical.
root=p/'affiliate-portal-router';base=pathlib.Path('/mnt/data/ebay_qa73/affiliate-portal-router')
changed=sorted(str(f.relative_to(root)) for f in root.rglob('*') if f.is_file() and f.read_bytes()!=(base/f.relative_to(root)).read_bytes())
ck(changed==['includes/trait-ppar-ebay-run.php'],'QA74 changed outside canonical run trait: '+str(changed))
full=subprocess.run(['python',str(p/'QA74_GESAMTKETTE.py')],capture_output=True,text=True,timeout=120)
try:full_result=json.loads(full.stdout)
except:full_result={'raw':full.stdout,'stderr':full.stderr}
ck(full.returncode==0 and full_result.get('local_pass') is True and full_result.get('checks')==5627,'previous full chain failed '+str(full_result)[:250])
ck(full_result.get('real_events')==2769,'historical event count mismatch')
ck(full_result.get('live_accepted') is False,'model incorrectly certified as live')
# Generate a canonical patch with stable repository paths.
patch=''.join(difflib.unified_diff(prev.read_text().splitlines(keepends=True),fixed.read_text().splitlines(keepends=True),fromfile='a/affiliate-portal-router/includes/trait-ppar-ebay-run.php',tofile='b/affiliate-portal-router/includes/trait-ppar-ebay-run.php'))
(p/'QA74_ZU_QA73.patch').write_text(patch)
ck(len(patch)>200 and 'candidate_ids' in patch and 'unverified_search_deferred_state_save_failed' in patch,'patch missing required fixes')
report={'teststand':'QA74','date':'2026-11-14','actual_test_methods':'Original PHP `ebay_public_checkpoint_is_safe` and `ebay_public_checkpoint_business_ids` retained; original engine PHP phases executed with mocked WP + eBay responses','changed_files_vs_QA73':changed,'QA73_checkpoint_bug_reproduced':True,'direct_real_helper_test_before':mem_before,'direct_real_helper_test_after':mem_after,'full_scenarios_real_helpers':tests,'previous_QA73_full_chain':full_result,'additional_assertions':checks,'additional_errors':errors,'local_pass':not errors,'historical_real_events':2769,'historical_public_coverage':'5/283','live_full_contract_pass':False,'reason_no_acceptance':'Historical real run has no final public/cleanup events and lacks historical item responses; QA is mock and source replay only. Protected GitHub PR #759 is not merged.'}
(p/'QA74_GESAMTVERIFIKATION.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'additional_checks':checks,'additional_failed':len(errors),'previous_full_checks':full_result.get('checks'),'all_local_pass':not errors,'diff_files':changed,'true_live_accepted':False,'errors':errors[:4]},ensure_ascii=False))
if errors:sys.exit(1)