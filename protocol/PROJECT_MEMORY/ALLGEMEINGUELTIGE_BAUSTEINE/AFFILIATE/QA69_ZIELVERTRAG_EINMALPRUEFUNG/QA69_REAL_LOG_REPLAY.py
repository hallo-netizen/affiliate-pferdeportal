#!/usr/bin/env python3
"""Lossless event-by-event replay of REAL uploaded CSV, no synthetic items.
This can replay observed transitions but CANNOT reproduce unavailable provider/WP inputs.
Fail closed for 1:1 E2E acceptance.
"""
import csv,hashlib,json,collections,datetime,pathlib
base=pathlib.Path('/mnt/data')
log=base/'pferdeatelier-ebay-lauf-574cb003b132.csv'
missing=base/'Pferdeatelier_eBay_fehlende_Produktfamilien_97507628-4f4.csv'
rows=list(csv.DictReader(log.open(encoding='utf-8-sig',newline=''),delimiter=';'))
items=list(csv.DictReader(missing.open(encoding='utf-8-sig',newline=''),delimiter=';'))
errors=[]
def assert_(p,msg):
 if not p:errors.append(msg)
assert_(len(rows)==2769,'Real audit event count is not 2769')
assert_(len(items)==278,'Real missing family count is not 278')
uuids={r['run_uuid'] for r in rows}
assert_(len(uuids)==1,'Several run UUIDs present')
uuid=next(iter(uuids)) if uuids else ''
assert_(all(i['run_uuid']==uuid for i in items),'Missing families reference another run')
assert_(len({i['familien_id'] for i in items})==278,'Duplicate or missing family ID')
# Replay EVERY real event in sequence. For each event, remember real durable values
# (not invented values), check monotonic counters, and verify legal temporal order.
state={}; history=[]; last_event=0; last_tick=0; last_progress=0; last_at=0
for r in rows:
 n=int(r['event_number']);t=int(r['transport_ticks']);p=int(r['progress_seq']);at=int(r['at'])
 assert_(n==last_event+1,f'event number jump at {n}')
 assert_(t>=last_tick,f'transport ticks rolled back at {n}')
 assert_(p>=last_progress,f'progress seq rolled back at {n}')
 assert_(at>=last_at,f'timestamp rolled back at {n}')
 last_event=n;last_tick=t;last_progress=p;last_at=at
 # The full authoritative recorded state at THAT time; no state synthesized.
 state={k:v for k,v in r.items()}
 history.append((n,at,r['phase'],r['phase_status'],t,p))
assert_(state.get('status')=='running' and state.get('phase')=='gapfill_discovery','last durable status incorrect')
assert_(state.get('covered')=='5' and state.get('required')=='283','final observed cover mismatch')
assert_(state.get('selection_scanned')=='155' and state.get('selection_materialized')=='2','final materialization mismatch')
assert_(state.get('skipped_item_errors_count')=='153','skipped count mismatch')
prune=[x for x in rows if x['phase_status']=='business_prune']
prune_ticks=sorted({int(x['transport_ticks']) for x in prune})
assert_(len(prune)==395 and len(prune_ticks)==196,'Actual preliminary cleanup count changed')
assert_(max(prune_ticks)-min(prune_ticks)+1==196,'Prune package ticks not consecutive')
classifications=collections.Counter(i['bewertung'] for i in items)
assert_(classifications=={
 'Kein zugeordneter Einzelabruf in diesem Teilstand':215,
 'Abruf hat zulässige Angebote; trotzdem nicht in dieser Abdeckung':32,
 'Angebote im Suchausschnitt, aber nicht angenommen':31},'Authentic missing family classification changed')
# These input fields are absent from BOTH exports; never replace with fabricated products.
needed={'item_id','source_payload','creative_identity_hash','policy_state','fresh_until',
        'source_state','output_object','public_checkpoint','source_rating','wp_options_snapshot'}
known=set(rows[0])|set(items[0]);absent=sorted(needed-known)
verdict='NOT_ACCEPTED_NO_REAL_WP_AND_EBAY_ITEM_SNAPSHOT'
result={
 'type':'REAL_AUDIT_EVENT_REPLAY_ONLY',
 'user_input_files':[
  {'filename':p.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size}
  for p in [log,missing]],
 'replayed_event_count':len(history),
 'replayed_real_state_count':len(history),
 'same_run_uuid':uuid,
 'real_observed_final':{k:state[k] for k in ('status','phase','progress_seq','transport_ticks','selection_scanned','selection_materialized','skipped_item_errors_count','covered','required')},
 'pre_public_cleanup_actual':{'audit_events':len(prune),'unique_worker_ticks':len(prune_ticks),'from_utc':datetime.datetime.fromtimestamp(int(prune[0]['at']),datetime.timezone.utc).isoformat(),'to_utc':datetime.datetime.fromtimestamp(int(prune[-1]['at']),datetime.timezone.utc).isoformat(),'note':'Audited real stages; removed code branch prevents the same scan in future canonical selection; an exact total time saving cannot be inferred'},
 'missing_families_actual':dict(classifications),'missing_family_count':len(items),
 'forbidden_claims':['Real 283-family eBay product simulation','Real WordPress DB/public output test','Real 153 item revalidation','Live workflow success'],
 'unavailable_original_inputs':absent,
 'real_inputs_complete_for_product_decision_reexecution':len(absent)==0,
 'replay_integrity_pass':len(errors)==0,
 'replay_errors':errors,
 'full_1_to_1_e2e_acceptance':False,
 'full_1_to_1_e2e_verdict':verdict,
 'next_evidence_needed':'Current read-only WordPress source/creative/output/options snapshot plus full non-secret original eBay responses for same time-window, with real public results and scheduler ticks.'
}
out=pathlib.Path('/mnt/data/ebay_contract_real/QA69_REAL_LOG_REPLAY.json')
out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'events_replayed':result['replayed_event_count'],'real_prune_ticks':result['pre_public_cleanup_actual']['unique_worker_ticks'],'missing_families':len(items),'missing_input_fields':len(absent),'e2e_verdict':verdict,'integrity_pass':not errors,'errors':errors},ensure_ascii=False))
raise SystemExit(0 if not errors else 1)