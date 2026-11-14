#!/usr/bin/env python3
"""QA68: full existing WordPress/eBay PHP release, source comparison and real CSV gate.
Isolated PHP tests mock WP DB & eBay API; no network or WP writes.
"""
import csv,datetime,hashlib,json,os,pathlib,subprocess,sys,zipfile
ROOT=pathlib.Path('/mnt/data/ebay_kiss_final')
SRC=ROOT/'affiliate-portal-router'
OUT=ROOT/'qa68'
OLD=pathlib.Path('/mnt/data/Affiliate_6.72.346_EBAY_GESAMTWORKFLOW_TEST.zip')
ZIP=pathlib.Path('/mnt/data/Affiliate_6.72.347_EBAY_KISS_GESAMTABLAUF_NUR_TEST.zip')
errors=[];results={}
def check(yes,name):
 if not yes:errors.append(name)
def run(cmd,timeout=75):
 p=subprocess.run(list(map(str,cmd)),capture_output=True,text=True,timeout=timeout)
 if p.returncode:errors.append(' '.join(map(str,cmd))+' returncode '+str(p.returncode)+' '+p.stderr[-600:])
 return p
# 1. Actual original PHP full orchestration all release candidate code.
p=run([sys.executable,ROOT/'qa/qa67_matrix.py'],115)
qa67=json.loads((ROOT/'qa/QA67_TEST_RESULT.json').read_text())
check(len(qa67['cases'])==7 and qa67['all_cases_same_final_public_and_errors'],'7 actual PHP full phase comparison')
results['full_phase_cases']=[x['case'] for x in qa67['cases']]
results['full_phase_same_safe_results']=qa67['all_cases_same_final_public_and_errors']
# 2. Source and lifecycle constraints, actual PHP trait with WP mocked.
T=SRC/'includes/trait-ppar-ebay-run.php';E=SRC/'includes/trait-ppar-ebay.php'
p=run(['php',OUT/'QA62_REAL_EBAY_TRAIT_TICK_TEST.php',T],45)
states=[json.loads(x) for x in p.stdout.splitlines() if x.strip()]
check(len(states)==16 and all(x.get('old_safe_untouched') for x in states),'16 REST state transitions')
check(all(x.get('new_run_calls',0)==0 for x in states if x['name'].startswith(('invalid','bad_','incoherent'))),'incoherent state never restarts')
results['run_states']=len(states)
p=run(['php',OUT/'QA63_REAL_DUE_CONTRACT.php',T],45)
due=[json.loads(x) for x in p.stdout.splitlines() if x.startswith('{')]
check(len(due)==11 and all(x['pass'] for x in due),'11 complete-cycle start decisions')
results['due_clock']=len(due)
p=run(['php','/mnt/data/ebay_qafix/qa62/QA58_SELECTED_FRESHNESS_REAL_TRAIT_TEST.php',E],65)
check('TOTAL 9/9' in p.stdout,'9 selected item freshness')
check('"materialized":153' in p.stdout,'153 individually revalidated mock items')
results['selected_source_check']='9/9 including 153 individually rechecked model items'
# 3. Real PHP init-hook pool migration comparison.
p=run([sys.executable,OUT/'test_pool_update.py'],25)
migration=json.loads((OUT/'POOL_UPDATE_RESULTS.json').read_text())
check(migration.get('passed')==5,'WP init pool cases')
check(all(x['after_automatic_jobs']==0 and x['idempotent'] for x in migration['cases']),'no automatic full-pool auto scheduling')
results['wp_init_cases']=len(migration['cases'])
# 4. Actual original CSV, no synthetic assumptions about duration of inventory.
raw=pathlib.Path('/mnt/data/pferdeatelier-ebay-lauf-574cb003b132.csv')
with raw.open(newline='',encoding='utf-8-sig') as f:rows=list(csv.DictReader(f,delimiter=';'))
check(len(rows)==2769 and len(set(x['run_uuid'] for x in rows))==1,'original CSV 2769 events one run')
last=rows[-1];check(last['covered']=='5' and last['required']=='283' and last['selection_materialized']=='2' and last['skipped_item_errors_count']=='153','original real source outcome 5/283 2/155')
remote=[x for x in rows if x['phase']=='refresh_remote']
check(len(remote)==1692,'original CSV remote section')
search_end=next(x for x in remote if x['search_requests']=='355')
results['real_source']={'run_uuid':last['run_uuid'],'events':len(rows),'last_phase':last['phase'],'covered':int(last['covered']),'required':int(last['required']),'selected_materialized':int(last['selection_materialized']),'selected_skipped':int(last['skipped_item_errors_count']),'refresh_remote_events_including_search_and_inventory':len(remote),'first_search_counter_final_at_utc':datetime.datetime.fromtimestamp(int(search_end['at']),datetime.timezone.utc).isoformat(),'remote_phase_done_utc':datetime.datetime.fromtimestamp(int(remote[-1]['at']),datetime.timezone.utc).isoformat(),'time_attribution_note':'refresh_remote includes both discovery and inventory: 3h40 must NOT be labelled inventory-only'}
# 5. PHP lint and absolute byte integrity against original ZIP.
php_files=sorted(SRC.rglob('*.php'))
for f in php_files:
 p=run(['php','-l',f],15)
check(len(php_files)==23,'23 PHP source files')
with zipfile.ZipFile(OLD) as z:
 before={x.filename:z.read(x.filename) for x in z.infolist() if not x.is_dir()}
after={str(p.relative_to(ROOT)):p.read_bytes() for p in SRC.rglob('*') if p.is_file()}
check(before.keys()==after.keys(),'same exact 66 package file names')
changed=[name for name in sorted(before) if before[name]!=after[name]]
expected=['affiliate-portal-router/includes/trait-ppar-automation-suite.php','affiliate-portal-router/includes/trait-ppar-ebay-run.php','affiliate-portal-router/pferdeportal-affiliate-router.php','affiliate-portal-router/readme.txt']
check(changed==sorted(expected),'only four changed source files')
check(len(before)==66,'66 files')
check(b"'6.72.347'" in (SRC/'includes/trait-ppar-automation-suite.php').read_bytes(),'v347 skip WP pool routine')
check(b'6.72.347' in (SRC/'pferdeportal-affiliate-router.php').read_bytes(),'version header updated')
with zipfile.ZipFile(ZIP,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=7) as z:
 for name in sorted(after):z.writestr(name,after[name])
with zipfile.ZipFile(ZIP) as z:
 check(z.testzip() is None,'ZIP integrity')
 check({x.filename:z.read(x.filename) for x in z.infolist() if not x.is_dir()}==after,'ZIP readback byte-identical')
results['integrity']={'package':str(ZIP),'sha256':hashlib.sha256(ZIP.read_bytes()).hexdigest(),'size_bytes':ZIP.stat().st_size,'php_lints':len(php_files),'total_package_files':len(before),'changed_files':changed,'unchanged_files':len(before)-len(changed),'zip_crc_ok':True}
results.update({'pass':not errors,'failures':errors,'qa_status':'QA_ONLY_NOT_LIVE','live_wordpress_tested':False,'live_ebay_api_tested':False,'live_github_delivery_tested':False,'real_public_family_coverage_verified':False})
(OUT/'QA68_GESAMTABNAHME_ERGEBNIS.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'pass':not errors,'errors':errors,'php_phase_cases':len(qa67['cases']),'rest_states':len(states),'due':len(due),'source':'9/9, 153 synthetic','wordpress_init':migration['passed'],'php_lint':len(php_files),'modified_files':changed,'zip_sha256':results['integrity']['sha256'],'zip_bytes':ZIP.stat().st_size},ensure_ascii=False,indent=2))
sys.exit(1 if errors else 0)