#!/usr/bin/env python3
"""QA-only truth table for existing complete PHP plugin + original audit events.
A green result here is NOT a real end-to-end acceptance; the truthful E2E gate
remains BLOCKED until actual WP/database and eBay source/response snapshots exist.
"""
import csv,json,hashlib,subprocess,pathlib,zipfile,sys,re,datetime
ROOT=pathlib.Path('/mnt/data/ebay_contract_real')
SRC=ROOT/'src/affiliate-portal-router'
FIX=ROOT/'fixed/affiliate-portal-router'
TEST=ROOT/'tests'
OUT=pathlib.Path('/mnt/data/ebay_contract_real/results');OUT.mkdir(exist_ok=True)
errors=[];mat={}
def good(p,msg):
 if not p:errors.append(msg)
def proc(args,timeout=60):
 p=subprocess.run([str(a) for a in args],capture_output=True,text=True,timeout=timeout)
 good(p.returncode==0,'Process error '+str(args)+' '+p.stderr[-400:]);return p
def phpjson(cmd):
 p=proc(['php',*cmd]);r=[]
 for x in p.stdout.splitlines():
  try:r.append(json.loads(x))
  except Exception as e:errors.append('Malformed JSON '+x[:150])
 return r
# FIRST replay actual 2,769 real events from the uploaded CSV + actual 278 family IDs.
proc(['python',TEST/'QA69_REAL_LOG_REPLAY.py'])
actual=json.loads((ROOT/'QA69_REAL_LOG_REPLAY.json').read_text())
good(actual['replayed_event_count']==2769,'Not every real event replayed')
good(actual['pre_public_cleanup_actual']['unique_worker_ticks']==196,'Wrong real cleanup ticks')
good(actual['full_1_to_1_e2e_acceptance'] is False,'False live endorsement')
mat['original_real_csv_replay']=actual
# Original method tests, old vs modified (not summaries).
sel_old=phpjson([TEST/'QA69_SELECTION_NO_PREPUBLIC_PRUNE.php',SRC/'includes/trait-ppar-ebay.php'])
sel_new=phpjson([TEST/'QA69_SELECTION_NO_PREPUBLIC_PRUNE.php',FIX/'includes/trait-ppar-ebay.php'])
for x in sel_old:good(x['run_uuid']==actual['same_run_uuid'],'Old test wrong UUID')
for x in sel_new:good(x['run_uuid']==actual['same_run_uuid'],'New test wrong UUID')
so={x['name']:x for x in sel_old};sn={x['name']:x for x in sel_new}
good(len(so)==5 and len(sn)==5,'Expected 5 exact original selector method cases')
good(so['full_old_prune_phase_recovery']['db_queries']==1 and sn['full_old_prune_phase_recovery']['db_queries']==0,'Canonical legacy prune not eliminated')
good(so['full_materialization_finishes_without_prune']['end']=='business_prune' and sn['full_materialization_finishes_without_prune']['end']=='complete','Canonical fresh materialization not streamlined')
good(sn['gapfill_after_reuse_finishes_without_prune']['db_queries']==0,'Gapfill after reuse still prunes')
good(so['standalone_keeps_existing_prune']['db_queries']==sn['standalone_keeps_existing_prune']['db_queries']==1,'Independent selection unexpectedly modified')
good(sn['standalone_materialization_still_enters_prune']['end']=='business_prune','Standalone behavior changed')
mat['original_php_selector_red_green']={'baseline':sel_old,'fixed':sel_new,'note':'Original source method executed with fake DB; NOT a real 196-tick WordPress DB replay'}
# Original PHP public append method, same known SAFE product IDs must not repeat whole gate.
ga_old=phpjson([TEST/'QA69_NO_REPEATED_GATE.php',SRC/'includes/trait-ppar-ebay-run.php'])
ga_new=phpjson([TEST/'QA69_NO_REPEATED_GATE.php',FIX/'includes/trait-ppar-ebay-run.php'])
go={x['case']:x for x in ga_old};gn={x['case']:x for x in ga_new}
good(go['duplicate_known_578_no_second_gate']['gate_calls']==1 and gn['duplicate_known_578_no_second_gate']['gate_calls']==0,'Repeated public decision not eliminated')
good(go['one_new_candidate_proven_once']['gate_calls']==gn['one_new_candidate_proven_once']['gate_calls']==1,'Valid new campaign no longer checked')
good(gn['unsafe_previous_checkpoint_not_overwritten']['save_calls']==0,'Unsafe checkpoint overwritten')
mat['original_php_public_gate_red_green']={'baseline':ga_old,'fixed':ga_new,'note':'Real PHP method with fake already-safe campaign IDs and mocked gate output'}
# Existing real PHP run orchestration, all main phases, with synthetic DB/provider payloads.
scenarios=['normal','old_blocked','new_blocked','db_down','churn','no_new','save_fail']
models=[]
for case in scenarios:
 results=[]
 for trait in [SRC/'includes/trait-ppar-ebay-run.php',FIX/'includes/trait-ppar-ebay-run.php']:
  p=subprocess.run(['php',str(TEST/'QA67_REAL_SYNC_FULL_PHASE_CHAIN.php'),str(trait),case],capture_output=True,text=True,timeout=35)
  good(p.returncode==(1 if case in ('db_down','save_fail') else 0),f'{case}: unexpected PHP harness exit code {p.returncode}')
  try:r=json.loads(p.stdout)
  except Exception:errors.append('Model result invalid '+case);continue
  results.append(r)
 if len(results)==2:
  a,b=results
  fields=['status','public_count','lost_old_ids','error','worker_tickets','families_covered_in_run']
  for field in fields:good(a['summary'][field]==b['summary'][field],f'{case} broken summary {field}')
  good([z['before'] for z in a['trace']]==[z['before'] for z in b['trace']],f'{case}: modeled orchestration phase diverged')
  models.append({'case':case,'baseline':a['summary'],'patched':b['summary']})
good(len(models)==7,'7 original worker model cases incomplete')
mat['original_canonical_php_full_model']={'cases':models,'note':'Real PHP phase methods but WordPress SQL, provider and nested selection services intentionally MOCKED; not actual E2E'}
# Existing original PHP 153 stale selected item rechecks (provider replies mocked).
p=proc(['php','/mnt/data/ebay_qafix/qa62/QA58_SELECTED_FRESHNESS_REAL_TRAIT_TEST.php',FIX/'includes/trait-ppar-ebay.php'],timeout=50)
good('TOTAL 9/9' in p.stdout,'Actual stale source trait suite failed')
good('"fetches":153' in p.stdout and '"materialized":153' in p.stdout,'153 mock rechecks incomplete')
mat['source_freshness_original_php']={'suite':'9/9','original_php':True,'ebay_api_payload':'MOCKED','model_stale_items':153}
# Existing real controller REST lifecycle and due scheduling with WP options mocked.
sa=phpjson(['/mnt/data/ebay_kiss_final/qa68/QA62_REAL_EBAY_TRAIT_TICK_TEST.php',FIX/'includes/trait-ppar-ebay-run.php'])
good(len(sa)==16,'16 original PHP REST status cases not complete')
good(all(x.get('old_safe_untouched') for x in sa),'REST status modified old SAFE')
du=proc(['php','/mnt/data/ebay_kiss_final/qa68/QA63_REAL_DUE_CONTRACT.php',FIX/'includes/trait-ppar-ebay-run.php'])
dus=[json.loads(x) for x in du.stdout.splitlines() if x.startswith('{')]
good(len(dus)==11 and all(x['pass'] for x in dus),'11 due decisions not complete')
mat['original_controller_lifecycle']={'status_cases':len(sa),'due_cases':len(dus),'provider_and_wordpress_live':False}
# Whole complete package syntax, file count, archive byte verification.
phps=sorted(FIX.rglob('*.php'))
for f in phps:proc(['php','-l',f],timeout=15)
good(len(phps)==23,'Expected exactly 23 PHP sources')
oldzip=pathlib.Path('/mnt/data/Affiliate_6.72.347_EBAY_KISS_GESAMTABLAUF_NUR_TEST.zip')
with zipfile.ZipFile(oldzip) as z:baseline={x.filename:z.read(x.filename) for x in z.infolist() if not x.is_dir()}
new={str(p.relative_to(ROOT/'fixed')):p.read_bytes() for p in (ROOT/'fixed').rglob('*') if p.is_file()}
good(baseline.keys()==new.keys(),'ZIP entry set unexpectedly changed')
changed=[x for x in sorted(baseline) if baseline[x]!=new[x]]
expected=["affiliate-portal-router/includes/trait-ppar-ebay.php","affiliate-portal-router/includes/trait-ppar-ebay-run.php","affiliate-portal-router/includes/trait-ppar-automation-suite.php","affiliate-portal-router/pferdeportal-affiliate-router.php","affiliate-portal-router/readme.txt"]
good(changed==sorted(expected),'Changes outside 5 authorized files')
zfile=pathlib.Path('/mnt/data/Affiliate_6.72.348_EBAY_EINMALPRUEFUNG_QA_KEINE_LIVEABNAHME.zip')
with zipfile.ZipFile(zfile,'w',zipfile.ZIP_DEFLATED,compresslevel=7) as z:
 for name in sorted(new):z.writestr(name,new[name])
with zipfile.ZipFile(zfile) as z:
 good(z.testzip() is None,'ZIP CRC failure')
 good({x.filename:z.read(x.filename) for x in z.infolist() if not x.is_dir()}==new,'ZIP readback differs from code')
mat['package_integrity']={'name':zfile.name,'sha256':hashlib.sha256(zfile.read_bytes()).hexdigest(),'files':len(new),'changed_files':changed,'unchanged_files':len(new)-len(changed),'php_lint_files':len(phps),'zip_crc_ok':True,'bytes':zfile.stat().st_size}
# STRONG STATED INVARIANTS: a green synthetic suite does not release a real run.
good(not any(x for x in mat['original_real_csv_replay']['unavailable_original_inputs'] if x in set(actual['original_real_inputs'] if 'original_real_inputs' in actual else [])), 'unexpected incorrect absent list')
result={
 'qa':'QA69','test_status':'PASS' if not errors else 'FAIL',
 'failures':errors,'e2e_product_test':'BLOCKED_NOT_ENOUGH_REAL_INPUTS',
 'e2e_production_release':'NOT_APPROVED',
 'no_synthetic_data_claimed_as_real':True,
 'real_original_2769_event_replay':actual['replay_integrity_pass'],
 'root_problem_actual_saved':{'unnecessary_pre_public_cleanup_ticks':196,'skipped_at_selection':153,'covered':'5/283'},
 'tested':mat,
 'acceptance_missing':['Real WP eBay source rows with source_payload and timestamps','Real published campaign/creative/output rows','Real WP run/selection/SAFE options','Original real provider response records for source freshening and verification','Verified public output for same run','Proven delivery of external GitHub heartbeat at runtime'],
}
(OUT/'QA69_MATRIX.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'test_status':result['test_status'],'failures':errors,'events_replayed':2769,'prune_worker_tics_real':196,'red_green_selector_cases':5,'red_green_public_gate_cases':3,'full_original_php_model_cases':7,'rest_status_cases':len(sa),'due_clock_cases':len(dus),'source_freshness':'9/9 MOCKED API','php_lints':len(phps),'zip_bytes':zfile.stat().st_size,'release_status':result['e2e_production_release']},ensure_ascii=False,indent=2))
raise SystemExit(0 if not errors else 1)