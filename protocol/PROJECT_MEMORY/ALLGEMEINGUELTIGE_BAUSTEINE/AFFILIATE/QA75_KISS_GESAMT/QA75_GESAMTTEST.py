#!/usr/bin/env python3
"""QA75 one end-to-end verification of original QA71 source + QA72-75 patch chain.
Historical source events are real; WordPress and eBay production I/O are simulated.
Never claim full live acceptance on the basis of these tests.
"""
import csv,hashlib,io,json,pathlib,subprocess,sys
R=pathlib.Path('/mnt/data/ebay_work')
C=R/'QA75/affiliate-portal-router'
OLD=pathlib.Path('/mnt/data/ebay_qa74/affiliate-portal-router')
SRC=C/'includes/trait-ppar-ebay-run.php'
MODEL=R/'QA75_FULL_CONTRACT_TEST.php'
failed=[];checks=0;scenarios=[]
def ck(ok,why):
 global checks
 checks+=1
 if not ok:failed.append(why)
def run(*args):
 return subprocess.run([str(a) for a in args],text=True,capture_output=True,timeout=60)
# Run real PHP orchestration, no mocked out phase-method implementations.
for case in ['normal','old_blocked','new_blocked','db_down','churn','no_new','save_fail','post_commit_state_save_fail','collision_retry_state_save_fail']:
 x=run('php',MODEL,SRC,case)
 try:d=json.loads(x.stdout)
 except Exception as exc:ck(False,f'{case}: invalid PHP output '+str(exc)+str(x.stderr[-250:]));continue
 a=d['summary']; b=d['end_business_contract'];b=b if isinstance(b,dict) else {};cp=d['public_checkpoint'];cleanup=d['cleanup'];
 ck(a['status']==('failed' if case in ['db_down','save_fail','post_commit_state_save_fail','collision_retry_state_save_fail'] else 'completed'),f'{case} wrong terminal: {a["status"]}')
 ck((x.returncode==0)==(a['status']=='completed'),f'{case} process exit code contradicts durable final status')
 ck(a['lost_old_ids']==(1 if case in ['old_blocked','churn'] else 0),f'{case} unexpectedly withdrew verified old stock')
 ck(a['public_count']>=578-1, f'{case} unnecessarily removed previously safe stock')
 ck(a['new_searches']==1, f'{case} restarted full discovery')
 if a['status']=='completed':
  required=b.get('required');covered=b.get('covered');missing=b.get('missing',[]);exceptions=b.get('exceptions',{})
  ck(required==283, f'{case} required family manifest not exactly 283')
  ck(isinstance(missing,list) and covered+len(missing)==283,f'{case} not exactly 283 family results')
  ck(isinstance(exceptions,dict) and set(missing)==set(exceptions),f'{case} lacks one saved reason for each missing family')
  ck(not any(x.get('approved') for x in exceptions.values()),f'{case} improperly approved missing families')
  ck(b.get('open_gap_count')==len(missing),f'{case} incorrect family gap count')
  ck(b.get('safe_gap_count',0)+b.get('technical_gap_count',0)+b.get('public_pending_count',0)==len(missing),f'{case} missing family reason types')
  ck(not any(v>3 for v in b.get('counts',{}).values()),f'{case} >3 public ads per family')
  if cp.get('source')=='canonical_public_verify':
   ids=cp.get('business_campaign_ids',[]);source_proof=b.get('verified_source_items',{})
   ck(set(map(int,ids))==set(map(int,b.get('verified_campaign_ids',[]))),f'{case} published membership differs from final public proof')
   ck(set(map(int,ids))==set(map(int,source_proof)),f'{case} source evidence not present for published members')
   keep=cleanup.get('business_active',{})
   ck(len(ids)==len(keep),f'{case} cleanup does not use exactly the public set')
   ck(set(map(int,ids))=={int(v.get('post_id',0)) for v in keep.values()},f'{case} cleanup would withdraw a public-approved item')
   ck(d['run_end_manifest']['checkpoint_id']==cp['checkpoint_id'],f'{case} run termination disconnected from public checkpoint')
 if case=='post_commit_state_save_fail':
  ck(a['error']=='public_checkpoint_cleanup_handoff_save_failed', 'post-public state failure did not fail closed')
  ck(a['public_writes']==2,'post-public state failure repeated public commit')
  ck(cp['source']=='canonical_public_verify', 'post-public state failure removed newly approved SAFE public membership')
 if case=='collision_retry_state_save_fail':
  ck(a['error']=='public_checkpoint_collision_state_save_failed','collision retry failure did not fail closed')
  ck(cp['source']=='independent_publisher' and cp['checkpoint_id']=='other-publisher-newer-safe', 'concurrent new SAFE checkpoint was overwritten')
  ck(a['public_writes']==1,'collision rollback wrote an unauthorized public checkpoint')
 if case=='db_down':ck(a['error']=='business_public_storage_read_failed','DB error code wrong')
 if case=='save_fail':ck(a['error']=='public_checkpoint_commit_failed','CAS error code wrong')
 scenarios.append(dict(name=case,status=a['status'],error=a['error'],families_covered=b.get('covered'),families_with_reasons=len(b.get('exceptions',{})),public_count=a['public_count'],public_writes=a['public_writes'],lost_old_ids=a['lost_old_ids']))
# The historic evidence is not forged as provider individual item answers.
with (R/'qa71/original/pferdeatelier-ebay-lauf-574cb003b132.csv').open(newline='',encoding='utf-8-sig') as f: events=list(csv.DictReader(f,delimiter=';'))
with (R/'qa71/original/Pferdeatelier_eBay_fehlende_Produktfamilien_97507628-4f4.csv').open(newline='',encoding='utf-8-sig') as f:missing_real=list(csv.DictReader(f,delimiter=';'))
ck(len(events)==2769,'real events count');ck(len(missing_real)==278,'real family gap count');ck(len(set(e['run_uuid'] for e in events))==1,'more than one historic run')
ck(events[-1]['status']=='running' and events[-1]['phase']=='gapfill_discovery','historic run not still open')
ck(events[-1]['covered']=='5' and events[-1]['required']=='283','historic family counts differ')
for i,e in enumerate(events):
 ck(int(e['event_number'])==i+1,'historic sequence not gap-free')
 if i:ck(int(e['at'])>=int(events[i-1]['at']), 'historic time went backwards')
# No added run worker, table, frontend or provider files.
changed=sorted(str(f.relative_to(C)) for f in C.rglob('*') if f.is_file() and f.read_bytes() != (OLD/f.relative_to(C)).read_bytes())
ck(changed==['includes/trait-ppar-ebay-run.php'],f'changed files vs QA74: {changed}')
php=list(C.rglob('*.php'))
for f in php:ck(run('php','-l',f).returncode==0,'PHP syntax '+str(f))
ck(len(php)==23,'PHP source file count changed')
# Regression with original final public check and original storage helpers.
for suite,scenario in [('QA74_MEMBERSHIP_REAL_HELPERS_TEST.php',None),('QA74_DEFERRED_SAVE_TEST.php','deferred_save_fail')]:
 args=['php',str(pathlib.Path('/mnt/data/ebay_qa74')/suite),str(SRC)];
 if scenario: args.append(scenario)
 r=run(*args)
 try:o=json.loads(r.stdout)
 except Exception:ck(False,f'{suite} invalid JSON '+r.stderr[-250:]);continue
 if scenario:
  a=o['summary'];ck(a['status']=='failed' and a['error']=='unverified_search_deferred_state_save_failed', 'unsafely marked deferred save completed')
 else:
  ck(o['same_run_same_membership']['writes']==0,'duplicate SAFE publication after retry')
  for key in ('same_run_different_membership','different_run_same_membership','different_source_same_membership'):
   ck(o[key]['writes']==1, 'new verified publisher blocked '+key)
  ck(o['same_run_same_membership']['published_count']==578,'old SAFE checkpoint lost')
r=run('php','/mnt/data/ebay_qa73/QA73_CLEANUP_LAST_WRITEFAIL_TEST.php',SRC,'cleanup_final_save_fail')
try:o=json.loads(r.stdout)['summary'];ck(o['status']=='failed' and o['error']=='checkpoint_business_cleanup_state_save_failed','final cleanup write failure not failed');ck(o['lost_old_ids']==0,'last-good lost during failed cleanup')
except Exception:ck(False,'cleanup final save test PHP error '+r.stderr[-250:])
# Direct invocation of unchanged original WordPress SQL compare-and-swap,
# including a competing publisher interleaving between load and UPDATE.
cas=run('php',R/'QA75/QA75_EIN_ATOMARER_PUBLIC_SPEICHER_TEST.php',SRC)
try:
 evidence=json.loads(cas.stdout)
 ck(cas.returncode==0 and evidence['pass'] is True,'actual PHP atomic public checkpoint saver failed '+cas.stderr[-120:])
 ck(evidence['concurrent_updated_shelf_retained'] and evidence['stale_snapshot_rejected'],'stale worker overwrote newer publisher')
except Exception:ck(False,'native PHP CAS saver test invalid JSON '+cas.stderr[-200:])
# The original full orchestration, freshness, public gate and item classifier suite:
regression=run('python','/mnt/data/ebay_qa74/QA74_GESAMTKETTE.py')
try:d=json.loads(regression.stdout);ck(regression.returncode==0 and d['checks']==5627 and d['failed']==0,'QA74 original full chain regressed')
except Exception:ck(False,'QA74 original full chain result missing '+regression.stderr[-180:])
# The previous extra 102 tests are intentionally baseline only: QA75 changes
# *expected* error outcome on the public-commit-to-cleanup save fault.
report={'name':'QA75 VERIFIED FULL CONTRACT QA ONLY','qa71_plugin_sha256':'e2d04337bf0d2c3ca8176059231b317f3682343239cef03bb68e4a57fa78c6b6','original_real_event_count':len(events),'original_real_gap_family_count':len(missing_real),'original_real_run_uuid':events[0]['run_uuid'],'original_real_ending':'running / gapfill_discovery / 5 of 283','original_php_full_chain_regression_checks':5627,'additional_checks':checks,'additional_failed':len(failed),'additional_failures':failed,'scenarios':scenarios,'patched_php_files_vs_QA74':changed,'full_live_acceptance':False,'reason_live_acceptance_blocked':'Real 283-family endpoint and public checkpoint, corresponding individual live eBay response and authorized working GitHub timer not proven.'}
(R/'QA75/QA75_GESAMTPRUEFUNG.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'additional_checks':checks,'additional_failed':len(failed),'scenarios':len(scenarios),'real_events':len(events),'mock_completed_283_outcomes':sum(s['status']=='completed' and s.get('families_with_reasons') is not None for s in scenarios),'total_baseline_checks':5627,'full_live_acceptance':False,'first_failures':failed[:8]},ensure_ascii=False))
if failed:sys.exit(1)