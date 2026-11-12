from pathlib import Path
import json,subprocess,hashlib
base=Path('/mnt/data/ebay_kiss_public_QA4_stage/affiliate-portal-router/includes/trait-ppar-ebay.php')
new=Path('/mnt/data/ebay_kiss_QA5_stage/affiliate-portal-router/includes/trait-ppar-ebay.php')
script='/mnt/data/qa5_prune_parity.php'
records=[]
for scenario in ['gapfill','gapfill_empty','gapfill_resume','gapfill_single','gapfill_sparse_tail','checkpoint_gapfill','full','checkpoint','error']:
 results=[]
 for path in [base,new]:
  p=subprocess.run(['php',script,str(path),scenario],capture_output=True,text=True,timeout=20)
  if p.returncode:raise RuntimeError(f'{path.name} {scenario}: {p.stderr}')
  d=json.loads(p.stdout);results.append(d)
 x,y=results
 if scenario in ('gapfill_sparse_tail','gapfill_single'):
  # A complete targeted cleanup intentionally leaves its last matching ID as
  # the final cursor, rather than scanning unrelated trailing catalog rows.
  assert x['state']['status']==y['state']['status']=='complete'
  assert x['state']['business_prune_cursor']>=y['state']['business_prune_cursor']
  for key in set(x['state'])|set(y['state']):
   if key!='business_prune_cursor': assert x['state'].get(key)==y['state'].get(key),(scenario,key)
 else:
  assert x['state']==y['state'],f'state difference {scenario}'
 assert x['actions']==y['actions'],f'actions difference {scenario}'
 records.append({'case':scenario,'parity':True,'old_queries':x['queries'],'new_queries':y['queries'],'old_scanned_rows':x['read_rows'],'new_scanned_rows':y['read_rows'],'actions':len(x['actions'])})
 print(f"PASS {scenario:<17} same stored state/actions; SQL {x['queries']} -> {y['queries']}, read {x['read_rows']} -> {y['read_rows']}")
assert records[0]['new_queries']<records[0]['old_queries']
assert records[0]['new_scanned_rows']<records[0]['old_scanned_rows']
Path('/mnt/data/EBAY_319_KISS_QA5_PRUNE_PARITAET_20261110.json').write_text(json.dumps(records,ensure_ascii=False,indent=2))