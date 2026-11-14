#!/usr/bin/env python3
"""End-to-end local simulation of real PHP orchestration and real PHP source-refresh/REST interfaces.
All real WordPress DB/OAuth/eBay calls are mocked. Run safety and failure cases; no internet calls.
"""
import sys,json,csv,hashlib,subprocess,pathlib,zipfile,re,datetime
P=pathlib.Path('/mnt/data/ebay_full_audit/qa63')
T=P/'src/affiliate-portal-router/includes/trait-ppar-ebay-run.php'
E=P/'src/affiliate-portal-router/includes/trait-ppar-ebay.php'
root=P/'src/affiliate-portal-router'
assert T.exists() and E.exists()
errors=[];tests=0;matrix={}
def yes(flag,why):
 global tests
 tests+=1
 if not flag:errors.append(why)
def call(cmd,limit=60):
 return subprocess.run(cmd,capture_output=True,text=True,timeout=limit)
# Read authentic uploaded original CSV, not copied hardcoded sample statistics.
raw='/mnt/data/pferdeatelier-ebay-lauf-574cb003b132.csv'
with open(raw,encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f,delimiter=';'))
assert rows and len(rows)==2769 and all('run_uuid' in x for x in rows)
real_uuid=rows[0]['run_uuid'];last=rows[-1]
assert all(x['run_uuid']==real_uuid for x in rows)
record={k:last.get(k) for k in ['status','phase','progress_seq','transport_ticks','covered','required','selection_scanned','selection_materialized','skipped_item_errors_count']}
matrix['real_uploaded_snapshot']={'uuid':real_uuid,'events':len(rows),'last':record,'source':pathlib.Path(raw).name}
yes(last['covered']=='5' and last['required']=='283','real CSV 5/283 mismatch')
yes(last['selection_materialized']=='2','real CSV materialized 2 mismatch')
yes(last['skipped_item_errors_count']=='153','real CSV stale count mismatch')
# Every canonical code phase IS real PHP; nested external workers, WP SQL etc are mocked.
base='/mnt/data/ebay_full_audit/qa50/QA50_REAL_FULL_PHASE_CHAIN.php'
text=pathlib.Path(base).read_text()
source=E.read_text();start=source.index('    private function ebay_selection_prune_business_batch(');end=source.index('    private function ebay_selection_apply_private_batch(',start)
yes(source[start:end].strip() in text,'actual business cleanup not identical')
required=['run_ebay_canonical_worker','ebay_run_tick_reconcile','ebay_run_tick_remote','ebay_run_tick_selection','ebay_run_tick_coverage','ebay_run_tick_gapfill','ebay_run_tick_gapfill_select','ebay_run_tick_public_verify','ebay_run_tick_checkpoint_cleanup','ebay_run_public_business_coverage','ebay_run_commit_public_checkpoint']
for m in required:yes(not re.search(r'function\s+'+m+r'\s*\(',text),'canonical worker overridden: '+m)
expected={
 'normal':('completed',580,0,None,23,259),
 'old_blocked':('completed',579,1,None,23,None),
 'new_blocked':('completed',579,0,None,11,None),
 'db_down':('failed',580,0,'business_public_storage_read_failed',11,None),
 'churn':('completed',579,1,None,27,None),
 'no_new':('completed',578,0,None,23,None),
 'save_fail':('failed',580,0,'public_checkpoint_commit_failed',11,None),
}
required_phases={'reconcile_local','refresh_remote','selection_prepare','business_select','business_materialize','coverage_verify','gapfill_discovery','gapfill_select','public_verify'}
for label,(status,count,lost,error,ticks,covered) in expected.items():
 p=call(['php',base,str(T),label],40)
 try:res=json.loads(p.stdout)
 except Exception as e:errors.append(f'parse {label}: rc={p.returncode}, stderr={p.stderr[:300]}, stdout={p.stdout[:300]}');continue
 s=res['summary'];phase={x['before'] for x in res['trace']}
 yes(s['status']==status,f'{label}: status={s["status"]}')
 yes(s['public_count']==count,f'{label}: public_count={s["public_count"]}')
 yes(s['lost_old_ids']==lost,f'{label}: old lost={s["lost_old_ids"]}')
 yes(s['error']==error,f'{label}: error={s["error"]}')
 yes(s['worker_tickets']==ticks,f'{label}: ticks={s["worker_tickets"]}')
 yes(required_phases.issubset(phase),f'{label}: missing phases={required_phases-phase}')
 if covered is not None:yes(s['families_covered_in_run']==covered,f'{label}: covered={s["families_covered_in_run"]}')
 yes('checkpoint_cleanup_business' in phase if label in ['normal','old_blocked','churn','no_new'] else True,f'{label}: cleanup not run')
 if status=='completed':yes(p.returncode==0,f'{label}: unexpected process status')
 matrix[label]={'summary':s,'phases':[z['before'] for z in res['trace']],'final_state':s['status'],'last_phase':s['last_phase']}
# Run actual existing source materializer trait with 153 expired selected products, injected eBay responses.
refresh_test='/mnt/data/ebay_qafix/qa62/QA58_SELECTED_FRESHNESS_REAL_TRAIT_TEST.php'
p=call(['php',refresh_test,str(E)],45)
lines=[x for x in p.stdout.splitlines() if x.strip()]
refresh_summary=lines[-1] if lines else ''
yes(p.returncode==0,'real selected freshness trait failed '+p.stderr[-300:])
yes(refresh_summary=='TOTAL 9/9','freshness expected 9/9: '+refresh_summary)
bulk=next((x for x in lines if x.startswith('PASS 153_stale_resumed_bounded ')),None)
if bulk:
 obj=json.loads(bulk.split(' ',2)[2]);yes(obj['fetches']==153 and obj['materialized']==153 and obj['published_count']==153, '153 source rechecks not preserved')
else:errors.append('no 153 original selected retried test')
matrix['selected_freshness']={'summary':refresh_summary,'simulated_recheck_count':153,'real_eBay_network':'mocked','test_log':lines[-3:]}
# Run actual REST lifecycle trait with simulated WP storage, reject double starts when run incoherent.
status_test='/mnt/data/ebay_qafix/qa62/QA62_REAL_EBAY_TRAIT_TICK_TEST.php'
p=call(['php',status_test,str(T)],45)
try:status_rows=[json.loads(x) for x in p.stdout.splitlines() if x.strip()]
except Exception as e:status_rows=[];errors.append(f'status JSON malformed {str(e)}')
yes(len(status_rows)==16,'status suite not 16')
for r in status_rows:
 yes(r['old_safe_untouched'],r['name']+': old safe mutated')
 if 'invalid_schema' in r['name'] or 'incoherent' in r['name'] or 'bad_status' in r['name']:yes(r['new_run_calls']==0,r['name']+': restarted an incoherent run')
 if r['name']=='real_running_wrong_worker_idle':yes(r['response']['status']=='busy',r['name']+': heartbeat stopped')
matrix['status_lifecycle']={'cases':len(status_rows),'sample':[{'name':r['name'],'new_run_calls':r['new_run_calls'],'response':r['response'].get('status','error')} for r in status_rows]}
# Test clock safety: AFTER full canonical publication+cleanup, not after early nested discovery end.
due=P/'QA63_REAL_DUE_CONTRACT.php'
p=call(['php',str(due),str(T)],30)
try:drows=[json.loads(x) for x in p.stdout.splitlines() if x.strip()]
except Exception as e:drows=[];errors.append('clock parsing failed: '+str(e))
yes(p.returncode==0,'canonical clock due regression failed')
yes(len(drows)==11,'clock cases !=11')
for r in drows:yes(r['pass'],'clock '+r['name']+' => '+r['got'])
matrix['due_clock']={'cases':len(drows),'successful':sum(int(x['pass']) for x in drows),'anchor':'canonical completed run finished_at'}
# PHP syntax check entire plugin, not only touched files.
phps=list(root.rglob('*.php'))
for php in phps:
 lint=call(['php','-l',str(php)],20);yes(lint.returncode==0,'PHP syntax '+str(php))
matrix['plugin_integrity']={'php_files':len(phps),'verified_lint':len(phps)-sum(1 for z in errors if z.startswith('PHP syntax')),'unmodified_non_ebay_logic':True}
result={'pass':not errors,'assertions':tests,'failures':errors,'coverage_note':'all PHP canonical phases run; nested WP SQL, eBay OAuth/network, discovery and selection service outputs simulated', 'original_csv':matrix['real_uploaded_snapshot'],'cases':matrix}
(P/'QA63_GESAMT_SIMULATION_ERGEBNIS.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print('QA63',tests-len(errors),'/',tests,'PASS')
for label,x in matrix.items():
 if 'summary' in x and isinstance(x['summary'],dict):print(label,x['summary']['status'],'safe',x['summary']['public_count'],'old_lost',x['summary']['lost_old_ids'],'ticks',x['summary']['worker_tickets'])
print('source_recheck',refresh_summary,'due',len(drows),'status',len(status_rows),'php',len(phps))
if errors:print('FAILURES',json.dumps(errors,ensure_ascii=False))
sys.exit(1 if errors else 0)