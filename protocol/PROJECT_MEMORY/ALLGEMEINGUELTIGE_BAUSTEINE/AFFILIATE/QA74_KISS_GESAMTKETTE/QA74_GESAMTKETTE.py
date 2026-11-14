#!/usr/bin/env python3
"""QA72: ONE consolidated regression of the original real audit and actual PHP methods.
Real eBay/WP provider payloads and live GitHub delivery are unavailable: NOT an E2E acceptance.
"""
import csv, json, subprocess, pathlib, collections, hashlib, re, sys
P=pathlib.Path('/mnt/data/ebay_qa74'); SRC=P/'affiliate-portal-router'; T=SRC/'includes/trait-ppar-ebay-run.php'; E=SRC/'includes/trait-ppar-ebay.php'; B=pathlib.Path('/mnt/data/ebay_qa72/trait-ppar-ebay.BASELINE.php'); QA=pathlib.Path('/mnt/data/ebay_qa71/evidence/tests'); DATA=pathlib.Path('/mnt/data/ebay_qa71/evidence/original')
fail=[]; checks=0
def ck(x,msg):
 global checks
 checks+=1
 if not x:fail.append(msg)
def cmd(*args):
 return subprocess.run([str(z) for z in args],capture_output=True,text=True,timeout=90)
def lines(proc):
 return [json.loads(l) for l in proc.stdout.splitlines() if l.lstrip().startswith('{')]
with (DATA/'pferdeatelier-ebay-lauf-574cb003b132.csv').open(encoding='utf-8-sig',newline='') as f: rows=list(csv.DictReader(f,delimiter=';'))
with (DATA/'Pferdeatelier_eBay_fehlende_Produktfamilien_97507628-4f4.csv').open(encoding='utf-8-sig',newline='') as f: families=list(csv.DictReader(f,delimiter=';'))
ck(len(rows)==2769,'real events count not 2769');ck(len(families)==278,'family count not 278')
uuids={x['run_uuid'] for x in rows};ck(len(uuids)==1 and len({x['run_uuid'] for x in families})==1 and next(iter(uuids))==families[0]['run_uuid'],'real UUID mismatch')
for i,row in enumerate(rows):
 ck(int(row['event_number'])==i+1,'event order '+str(i))
 if i: ck(int(row['at'])>=int(rows[i-1]['at']),'event time backwards '+str(i))
last=rows[-1];ck((last['status'],last['phase'],int(last['progress_seq']),int(last['transport_ticks']),int(last['covered']),int(last['required']))==('running','gapfill_discovery',474,468,5,283),'real terminal unexpectedly different')
ck(not any(x['phase'] in ('public_verify','checkpoint_cleanup_business','completed') for x in rows),'real live completion not in original CSV')
ck(len({x['familien_id'] for x in families})==278,'family duplicates')
family_outcomes=collections.Counter(str(x['bewertung']) for x in families)
# Each family must be counted; no simulated product data is used here.
ck(sum(family_outcomes.values())==278,'family outcomes not fully classified')

orig=cmd('php',pathlib.Path('/mnt/data/ebay_qa72/QA72_SINGLE_OWNER_PHP.php'),B);new=cmd('php',pathlib.Path('/mnt/data/ebay_qa72/QA72_SINGLE_OWNER_PHP.php'),E)
ck(orig.returncode==0 and new.returncode==0,'QA72 PHP source comparison failure '+orig.stderr[-300:]+new.stderr[-300:])
a=json.loads(orig.stdout) if orig.returncode==0 else {}; b=json.loads(new.stdout) if new.returncode==0 else {}
ck(a.get('quality_calls')==9 and b.get('quality_calls')==5,'quality assessor not single-pass')
ck(a.get('primary_plan_active')==b.get('primary_plan_active'),'candidate rank selection changed in matched-source model')
ck(a.get('secondary_planning_classify_calls')==1 and b.get('secondary_planning_classify_calls')==0,'extra family planned twice')
ck(a.get('secondary_attach_classify_calls')==6 and b.get('secondary_attach_classify_calls')==0,'extra family reclassified at attach')
ck(b.get('secondary_same_source_success') and b.get('secondary_different_source_rejected') and b.get('writes_after_good')==1,'stored source evidence gate invalid')
ck(a.get('upsert_same_classify_calls')==1 and b.get('upsert_same_classify_calls')==0 and b.get('upsert_unchanged_extra_preserved'),'unchanged eBay source reclassified at upsert')
ck(b.get('upsert_changed_classify_calls')==1,'new source version no longer classified')

models={}
for scenario in ['normal','old_blocked','new_blocked','db_down','churn','no_new','save_fail']:
 proc=cmd('php',QA/'QA50_REAL_FULL_PHASE_CHAIN.php',T,scenario)
 ck(proc.returncode==(1 if scenario in ('db_down','save_fail') else 0),'full PHP flow return '+scenario)
 try: model=json.loads(proc.stdout); summary=model['summary']; models[scenario]={'status':summary['status'],'safe_public_count':summary.get('public_count'),'error':summary.get('error'),'ticks':summary.get('worker_tickets'),'phases':list(dict.fromkeys(x['before'] for x in model.get('trace',[])))}
 except Exception as ex: fail.append('PHP full phase output '+scenario+str(ex));continue
 ck(summary['status']==('failed' if scenario in ('db_down','save_fail') else 'completed'),'full phase terminal '+scenario)
 ck('public_verify' in models[scenario]['phases'],'public verify missing '+scenario)
 ck(scenario in ('db_down','save_fail','new_blocked') or 'checkpoint_cleanup_business' in models[scenario]['phases'],'cleanup phase missing '+scenario)

suite=[('QA71_FINAL_SOURCE_SINGLE_DECISION.php',T,7),('QA71_BUSINESS_REFRESH_NO_REDECISION.php',E,1),('QA71_REAL_AVAILABILITY_HELPER.php',E,7),('QA69_SELECTION_NO_PREPUBLIC_PRUNE.php',E,5),('QA69_NO_REPEATED_GATE.php',T,3),('QA62_REAL_EBAY_TRAIT_TICK_TEST.php',T,16),('QA63_REAL_DUE_CONTRACT.php',T,11)]
php_suites=[]
for fn,trait,count in suite:
 proc=cmd('php',QA/fn,trait)
 try: output=lines(proc)
 except Exception as ex:output=[];fail.append('bad JSON '+fn+str(ex))
 ck(proc.returncode==0 and len(output)==count,'PHP suite count or failure '+fn+': '+proc.stderr[-250:]+str(len(output)))
 if fn=='QA71_FINAL_SOURCE_SINGLE_DECISION.php':ck(all(x['legacy_calls']==0 for x in output),'final source worker reclassified')
 if fn=='QA71_BUSINESS_REFRESH_NO_REDECISION.php':ck(output[0]['classified']==0 and output[0]['ranked']==0 and output[0]['upserted']==0,'regular source worker reclassified')
 if fn=='QA63_REAL_DUE_CONTRACT.php':ck(all(x['pass'] for x in output),'next due scenario failure')
 php_suites.append({'suite':fn,'cases':len(output),'expected':count,'pass':proc.returncode==0 and len(output)==count})
fresh_proc=cmd('php',QA/'QA58_SELECTED_FRESHNESS_REAL_TRAIT_TEST.php',E)
ck(fresh_proc.returncode==0 and 'TOTAL 9/9' in fresh_proc.stdout,'selected stale refresh helper 9 cases failed')

src=E.read_text();
def func_fragment(name):
 at=src.index('function '+name+'(')
 start=src.index('{',at);d=0
 for i in range(start,len(src)):
  if src[i]=='{':d+=1
  elif src[i]=='}':
   d-=1
   if d==0:return src[at:i+1]
 return ''
for name in ['ebay_business_selection_plan_concept','ebay_business_add_verified_secondary','ebay_route_business','ebay_business_source_row_item','ebay_selection_apply_business_batch']:
 ck(bool(func_fragment(name)),'missing original method '+name)
ck(func_fragment('ebay_business_selection_plan_concept').count('$this->ebay_business_quality_assess(')==1,'second whole quality assessor in planning')
ck('$this->ebay_business_classify_portal_item_strict(' not in func_fragment('ebay_business_add_verified_secondary'),'secondary reclassification in attach')
ck('$this->ebay_business_classify_portal_item_strict(' not in func_fragment('ebay_route_business'),'materialization reclassification')
ck('$this->ebay_business_classify_portal_item_strict(' not in func_fragment('ebay_business_source_row_item'),'stored-source reclassification')
ck('$this->ebay_business_quality_assess(' not in func_fragment('ebay_selection_apply_business_batch'),'apply re-ranking')
source_diff=cmd('diff','-u',B,E)
ck(source_diff.returncode==1,'original code comparison absent')
changed=[]
ORIG=pathlib.Path('/mnt/data/ebay_qa71/source/affiliate-portal-router')
for f in SRC.rglob('*'):
 if f.is_file():
  rel=f.relative_to(SRC)
  if f.read_bytes()!=(ORIG/rel).read_bytes():changed.append(str(rel))
ck(changed==['includes/trait-ppar-ebay-run.php','includes/trait-ppar-ebay.php'],'QA73 expected exactly QA72 eBay and QA73 orchestrator: '+str(changed))
php=list(SRC.rglob('*.php'))
for f in php:
 p=cmd('php','-l',f)
 ck(p.returncode==0,'PHP syntax '+str(f))
ck(len(php)==23,'unexpected PHP source count')
report={'name':'QA74 KISS full chain + terminal persistence / idempotent publication','original_data':{'events':len(rows),'uuid':next(iter(uuids)),'last_phase':last['phase'],'live_public_covered':int(last['covered']),'required':283,'missing_families':len(families),'family_status_values':dict(family_outcomes),'real_full_run_finished':False},'before_after_actual_trait_php':{'before':a,'after':b},'full_php_controller_scenarios_with_mock_wp_ebay':models,'other_php_suites':php_suites,'selected_freshness_cases':9 if fresh_proc.returncode==0 else 'UNKNOWN','changed_php_files':changed,'php_syntax_files':len(php),'checks':checks,'failures':fail,'local_test_pass':not fail,'full_contract_pass':False,'reason_not_accepted':'Original-CSV lacks original per-item eBay responses, WP snapshots, live GH ticks and completed public checkpoint. Real run stops at 5/283.'}
(P/'QA74_GESAMTRESULTAT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
(P/'QA74_QA72_EBAY_SOURCE_DIFF.patch').write_text('--- a/includes/trait-ppar-ebay.php\n+++ b/includes/trait-ppar-ebay.php\n' + ''.join(source_diff.stdout.splitlines(keepends=True)[2:]))
print(json.dumps({'checks':checks,'failed':len(fail),'model_runs':len(models),'other_suite_cases':sum(x['cases'] for x in php_suites),'real_events':len(rows),'local_pass':not fail,'live_accepted':False,'fail_examples':fail[:20]},ensure_ascii=False))
if fail:sys.exit(1)