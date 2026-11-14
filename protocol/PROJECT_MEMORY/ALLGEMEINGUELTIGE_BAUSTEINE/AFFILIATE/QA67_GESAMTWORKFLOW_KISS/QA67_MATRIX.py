#!/usr/bin/env python3
import subprocess,json,zipfile,tempfile,pathlib,difflib
root=pathlib.Path('/mnt/data/ebay_kiss_final')
original_zip='/mnt/data/Affiliate_6.72.346_EBAY_GESAMTWORKFLOW_TEST.zip'
original_name='affiliate-portal-router/includes/trait-ppar-ebay-run.php'
original=root/'qa/QA67_ORIGINAL_V346.php'
with zipfile.ZipFile(original_zip) as z: original.write_bytes(z.read(original_name))
modified=root/'affiliate-portal-router/includes/trait-ppar-ebay-run.php'
harness=root/'qa/QA67_REAL_SYNC_FULL_PHASE_CHAIN.php'
scenarios=['normal','old_blocked','new_blocked','db_down','churn','no_new','save_fail']
entries=[]
for mode in scenarios:
 data={}
 for ver,path in [('before',original),('after',modified)]:
  cmd=['php',str(harness),str(path),mode]
  proc=subprocess.run(cmd,text=True,capture_output=True,timeout=30)
  try:raw=json.loads(proc.stdout)
  except Exception as ex:raise RuntimeError(f'{mode} {ver} invalid output: {proc.stderr[:300]} {proc.stdout[:300]}') from ex
  data[ver]=raw
  assert proc.returncode==0 if mode not in ['db_down','save_fail'] else proc.returncode!=0,(mode,ver,proc.returncode)
 a=data['before']['summary'];b=data['after']['summary'];ta=data['before']['trace'];tb=data['after']['trace']
 for field in ['status','last_phase','candidate_count','public_count','new_searches','lost_old_ids','new_ids','families_covered_in_run','selection_calls','public_writes','published_outputs','error']:
  assert a[field]==b[field],(mode,field,a[field],b[field])
 before_phases=[x['before'] for x in ta];after_phases=[x['before'] for x in tb]
 assert before_phases.count('refresh_remote')==2,(mode,before_phases)
 assert after_phases.count('refresh_remote')==1,(mode,after_phases)
 assert 'business_materialize' in after_phases and 'public_verify' in after_phases,(mode,after_phases)
 assert any(x['after']=='selection_prepare' for x in tb if x['before']=='refresh_remote'),(mode,after_phases)
 entries.append({'case':mode,'status':b['status'],'public_items_before':a['public_count'],'public_items_after':b['public_count'],'old_safe_removed':b['lost_old_ids'],'old_ticks':a['worker_tickets'],'new_ticks':b['worker_tickets'],'full_sync_discovery_done':True,'skipped_bulk_refresh':True})
# Legacy/explicit refresh operation uses the existing inventory worker, no bypass:
# eBay source code conditional only recognizes operation==sync, and the refresh job section is byte identical.
a=original.read_text();b=modified.read_text()
old_start=a.index("        $job=$this->ebay_refresh_job_load();",a.index('private function ebay_run_tick_remote('));new_start=b.index("        $job=$this->ebay_refresh_job_load();",b.index('private function ebay_run_tick_remote('));
old_end=a.index("    private function ebay_run_tick_selection(",old_start);new_end=b.index("    private function ebay_run_tick_selection(",new_start)
assert a[old_start:old_end]==b[new_start:new_end]
# exact single source difference across both traits and maintenance functions
list_changes=list(difflib.unified_diff(a.splitlines(),b.splitlines(),fromfile='v346/ebay-run',tofile='v347/ebay-run'))
assert len([x for x in list_changes if x.startswith('@@')])==1
# 9 selected-source freshness tests already in place in v346; reexecute original user acceptance.
qa58='/mnt/data/ebay_qafix/qa62/QA58_SELECTED_FRESHNESS_REAL_TRAIT_TEST.php'
source=root/'affiliate-portal-router/includes/trait-ppar-ebay.php'
p=subprocess.run(['php',qa58,str(source)],capture_output=True,text=True,timeout=40)
assert p.returncode==0 and 'TOTAL 9/9' in p.stdout,(p.returncode,p.stdout[-500:],p.stderr[-500:])
# Lint all source files in the real package
files=list((root/'affiliate-portal-router').rglob('*.php'))
for f in files:
 p=subprocess.run(['php','-l',str(f)],capture_output=True,text=True,timeout=15)
 assert p.returncode==0,(str(f),p.stderr)
result={'purpose':'One full sync, no redundant inventory-wide refresh after discovery; selected items are still rechecked before materialisation and public commit.', 'cases':entries,'all_cases_same_final_public_and_errors':True,'independent_inventory_refresh_unchanged':True,'freshness_test':'9/9','php_files_lint':len(files),'original_php_phase_chain':True,'mocked_service_boundary':'Real WordPress SQL/eBay network/GitHub schedule are NOT tested.','live_verified':False,'plugin_release':False,'status':'QA_ONLY'}
out=root/'qa/QA67_TEST_RESULT.json'
out.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
(root/'qa/QA67_SINGLE_PASS.patch').write_text(''.join(list_changes))
print(json.dumps({'total':len(entries),'cases':entries,'patch_lines':len(list_changes),'php_lint':len(files),'selected_freshness':'9/9'},ensure_ascii=False,indent=2))