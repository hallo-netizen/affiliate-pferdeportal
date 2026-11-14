#!/usr/bin/env python3
"""Exact replay of every REAL user-uploaded eBay audit event and all 283 concept IDs.
No historical eBay provider payloads or WP-source records are inferred or fabricated.
"""
import csv,json,pathlib,collections,datetime,hashlib
ROOT=pathlib.Path('/mnt/data/ebay_qa71/evidence/original')
CAT=pathlib.Path('/mnt/data/ebay_work/QA75/verified_apply/assets/ebay-portal-catalog-v2.json')
OUT=pathlib.Path('/mnt/data/ebay_work/QA76_ECHTDATEN')
AUDIT=ROOT/'pferdeatelier-ebay-lauf-574cb003b132.csv'
MISSING=ROOT/'Pferdeatelier_eBay_fehlende_Produktfamilien_97507628-4f4.csv'
def load(path):
 with path.open(newline='',encoding='utf-8-sig') as fh: return list(csv.DictReader(fh,delimiter=';'))
audit=load(AUDIT);gaps=load(MISSING);cat=json.loads(CAT.read_text())
ids=cat['business_supply_contract']['required_product_concept_ids']
excluded=set(cat['ebay_non_goods_concept_ids']); wanted=[x for x in ids if x not in excluded]
expected_uuid='97507628-4f4d-4527-bd77-fa573bce7067'
errors=[];checks=0
def ck(t,m):
 global checks;checks+=1
 if not t:errors.append(m)
ck(len(audit)==2769,'audit count must 2769');ck(len(gaps)==278,'missing must be 278');ck(len(wanted)==283,'required goods must 283');ck(len(set(wanted))==len(wanted),'catalog duplicated goods')
ck({x['run_uuid'] for x in audit}=={expected_uuid},'audit UUID contradiction')
ck({x['run_uuid'] for x in gaps}=={expected_uuid},'gap UUID contradiction')
ck(len({x['familien_id'] for x in gaps})==278,'duplicated gap family')
ck(set(x['familien_id'] for x in gaps)<=set(wanted),'missing not subset of actual goods')
ck(audit[-1]['status']=='running' and audit[-1]['phase']=='gapfill_discovery','not still running last event')
ck((int(audit[-1]['covered']),int(audit[-1]['required']))==(5,283),'covered/required mismatch')
ck(int(audit[-1]['skipped_item_errors_count'])==153,'stale skipped counter discrepancy')
prev_ts=0;prev_step=0;prev_transport=0;pauses=[];skips=[];reasons=collections.Counter();counters=collections.Counter()
for i,row in enumerate(audit):
 ck(int(row['event_number'])==i+1,'event number missing '+str(i+1))
 ts=int(row['at']);seq=int(row['progress_seq']);transport=int(row['transport_ticks']);skip=int(row['skipped_item_errors_count'])
 ck(ts>=prev_ts,'time backwards at '+str(i+1))
 ck(seq>=prev_step,'progress backwards at '+str(i+1))
 ck(transport>=prev_transport,'transport counter backwards at '+str(i+1))
 if i and ts-prev_ts>300:
  pauses.append({'before_event':i,'after_event':i+1,'seconds':ts-prev_ts,'before_at':prev_ts,'after_at':ts,'phase_before':audit[i-1]['phase'],'phase_after':row['phase']})
 if i and skip>int(audit[i-1]['skipped_item_errors_count']):
  skips.append({'event':i+1,'at':ts,'added':skip-int(audit[i-1]['skipped_item_errors_count']),'cumulative':skip})
 prev_ts,prev_step,prev_transport=ts,seq,transport
sample={}
for row in audit:
 raw=row.get('skipped_item_examples') or '[]'
 try:s=json.loads(raw)
 except:continue
 for x in s:
  if not isinstance(x,dict) or not x.get('item_id'):continue
  k=x['item_id'];
  if k in sample:ck(x['code']==sample[k]['code'] and x['concept']==sample[k]['concept'],'inconsistent duplicate error '+k)
  sample[k]=x
ck(len(sample)==95,'original code-specific sample count not 95')
ck(all(x['code']=='business_selected_stale_during_apply' for x in sample.values()),'stale exception has other code')
ck(sum(s['added'] for s in skips)==153,'nonmonotonic skip increases')
missing_map={x['familien_id']:x for x in gaps}
original_status=[]
for id in wanted:
 if id not in missing_map:
  status='covered_in_original_audit_inferred_from_missing_set';proof='in original 283 goods minus 278 missing; family ID inferred from catalog'
 else:
  x=missing_map[id]
  requests=int(x['anfragen']);accepted=int(x['davon_angenommen'])
  if requests==0:status='no_individual_search_in_this_snapshot'
  elif accepted>0:status='accepted_offers_but_not_publicly_covered'
  else:status='search_no_accepted_offer'
  proof='original gap CSV: '+x['bewertung']
  counters[status]+=1
 row=missing_map.get(id,{});fromcat=next((x for x in cat['business_concepts'] if x['id']==id),{})
 original_status.append({'id':id,'title':fromcat.get('title',row.get('produktfamilie','')),'original_snapshot_status':status,'requests':int(row.get('anfragen',0) or 0),'search_found':int(row.get('angebote_im_teilabschnitt',0) or 0),'accepted':int(row.get('davon_angenommen',0) or 0),'reasons':row.get('ablehnungsgruende',''),'evidence':proof,'run_uuid':expected_uuid})
ck(len(original_status)==283,'family ledger not 283')
ck(dict(counters)=={'no_individual_search_in_this_snapshot':215,'accepted_offers_but_not_publicly_covered':32,'search_no_accepted_offer':31},'status distribution unexpected: '+str(counters))
ck(len([x for x in original_status if 'covered_in_original' in x['original_snapshot_status']])==5,'five inferred covered mismatch')
ck(sum(x['requests'] for x in original_status)==120,'requests mismatch')
ck(sum(x['search_found'] for x in original_status)==2056,'found mismatch')
ck(sum(x['accepted'] for x in original_status)==201,'accepted mismatch')
ck(sum(int(x['seconds']) for x in pauses)==21324,'four long gaps duration drift')
err_ids=[{'item_id':v['item_id'],'family_id':v['concept'],'error_code':v['code'],'row_id':v.get('row_id',0)} for v in sample.values()]
result={'type':'QA76_REAL_HISTORICAL_EVENT_AND_FAMILY_REPLAY_NO_SYNTHETIC_PRODUCTS','inputs':{str(p.name):{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in (AUDIT,MISSING,CAT)},'run_uuid':expected_uuid,'actual_events':len(audit),'first_event':audit[0]['at'],'last_event':audit[-1]['at'],'last_recorded':{k:audit[-1][k] for k in ('status','phase','progress_seq','transport_ticks','covered','required','selection_scanned','selection_materialized','skipped_item_errors_count','resume_reason','error_code')},'real_family_statuses':dict(collections.Counter(x['original_snapshot_status'] for x in original_status)),'real_family_ledgers':original_status,'real_stale_items_identified':len(sample),'stale_item_ids_with_real_error_code':err_ids,'real_stale_failures_total_counter':153,'unidentified_individual_stale_failure_ids':153-len(sample),'skips_growth':skips,'historical_pauses':pauses,'historical_pauses_seconds':sum(x['seconds'] for x in pauses),'historical_pauses_hours':round(sum(x['seconds'] for x in pauses)/3600,2),'checks':checks,'failed_checks':len(errors),'failures':errors,'one_to_one_provider_response_replay_possible':False,'missing_for_one_to_one_replay':['original complete eBay item responses for all historical candidates','corresponding WordPress eBay sources and public campaign rows at the time','historical per-item public source checkpoints and auth/response timestamps'],'real_live_completed':False}
(OUT/'QA76_ORIGINAL_283_FAMILIEN_UND_95_FEHLARTIKEL.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
(OUT/'QA76_95_ORIGINALARTIKEL.json').write_text(json.dumps(err_ids,ensure_ascii=False,indent=2)+'\n')
(OUT/'QA76_283_ORIGINAL_FAMILIEN_IDS.json').write_text(json.dumps(wanted,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k in ('run_uuid','actual_events','real_family_statuses','real_stale_items_identified','real_stale_failures_total_counter','unidentified_individual_stale_failure_ids','historical_pauses_hours','historical_pauses_seconds','checks','failed_checks','failures','one_to_one_provider_response_replay_possible')},ensure_ascii=False,indent=2));raise SystemExit(bool(errors))