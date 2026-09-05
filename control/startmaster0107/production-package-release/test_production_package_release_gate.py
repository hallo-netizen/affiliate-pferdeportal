#!/usr/bin/env python3
from __future__ import annotations
import copy, hashlib, importlib.util, json, shutil, sys, tempfile
from pathlib import Path

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[2]
spec=importlib.util.spec_from_file_location('release_gate',HERE/'production_package_release_gate.py')
gate=importlib.util.module_from_spec(spec);sys.modules['release_gate']=gate;spec.loader.exec_module(gate)

def stable(o): return hashlib.sha256(json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def current_batch():
    state=json.loads((REPO/'control/startmaster0107/runtime_inbox/RUNTIME_INBOX_STATE.json').read_text())
    snap=json.loads((REPO/state['source_snapshot_ref']).read_text())
    return state,snap['next_textmachine_metadata_batch']

def make_full_package(path:Path):
    state,batch=current_batch(); slots=[x['plan_slot'] for x in batch['items']]
    packs=[]; plan_items=[]; release_items=[]
    for i,slot in enumerate(slots,1):
        fid=f'F{i}'; cid=f'article:test{i:02d}'; scope=f'Scope {i}'; name=f'Category {i}'
        packs.append({'contract':'canonical_fact_pack_v1','fact_pack_id':fid,'title_scope':scope})
        plan_items.append({'canonical_article_id':cid,'source_snapshot_id':fid,'runtime_order':{'subject_scope':scope},'quality_binding':{'wordpress_category':{'name':name,'slug':f'category-{i}','taxonomy':'category','hierarchy_path':f'Root > {name}','category_source_snapshot_hash':hashlib.sha256(name.encode()).hexdigest()}}})
        release_items.append({'plan_slot':slot,'canonical_article_id':cid})
    bundle={'contract':'canonical_fact_pack_import_v1','fact_packs':packs}; plan={'contract':'production_plan_v4','items':plan_items}; bh,ph=stable(bundle),stable(plan)
    release={'contract':'WORKFLOW_SUPERVISOR_RELEASE_V2_HASH_BOUND','status':'PASS','fact_pack_bundle_sha256':bh,'production_plan_sha256':ph,'exact_five_batch_sha256':state['batch_sha256'],'exact_five_item_count':len(slots),'items':release_items}
    rh=stable(release)
    env={'contract':'PSERC_APPROVED_PRODUCTION_PACKAGE_V1','fact_pack_bundle_sha256':bh,'production_plan_sha256':ph,'workflow_release_sha256':rh,'package_id':stable({'contract':'PSERC_APPROVED_PRODUCTION_PACKAGE_V1','fact_pack_bundle_sha256':bh,'production_plan_sha256':ph,'workflow_release_sha256':rh}),'source':'TEST_CURRENT_GENERATION','fact_pack_bundle':bundle,'production_plan':plan,'workflow_release':release}
    env['package_payload_sha256']=stable(env); path.write_text(json.dumps(env,ensure_ascii=False,indent=2)+'\n'); return env

def make_recovery_plan(path:Path):
    state,batch=current_batch(); bindings=[]; items=[]
    for i,meta in enumerate(batch['items'],1):
        cid=f'article:recovery{i:02d}'; body=f'<article><p>Locked fixture {i}</p></article>'; text=f'Locked fixture {i}'
        bindings.append({**meta,'canonical_article_id':cid,'plan_item_key':f'fixture-{i}'})
        items.append({'article_type':meta['article_type'],'canonical_article_id':cid,'plan_item_key':f'fixture-{i}','canonical_article':{'title':meta['title'],'target_keyword':meta['target_keyword'],'body_html':body,'body_html_sha256':hashlib.sha256(body.encode()).hexdigest(),'body_text':text}})
    plan={'contract':'production_plan_v4','source_ready_batch':{'generation':state['generation'],'batch_sha256':state['batch_sha256'],'bindings':bindings},'items':items}
    path.write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n'); return plan

def expect_block(fn,contains):
    try: fn()
    except Exception as e:
        assert contains in str(e),(contains,str(e)); return
    raise AssertionError('expected block '+contains)

def run():
    checks=[]
    def ok(name): checks.append({'name':name,'status':'PASS'})
    with tempfile.TemporaryDirectory() as td:
        td=Path(td); pkg=td/'full.json'; env=make_full_package(pkg); planp=td/'plan.json'; make_recovery_plan(planp)
        p=gate.validate_package(pkg,REPO,True); assert p['status']=='UPLOAD_ARTIFACT_RELEASE_PASS' and p['current_generation']==1 and p['publish_allowed'] is False; ok('POSITIVE_FULL_PACKAGE_CURRENT_GENERATION')
        out=td/'released.json'; shutil.copyfile(pkg,out); assert pkg.read_bytes()==out.read_bytes(); ok('RELEASE_COPY_BYTE_IDENTICAL')
        expect_block(lambda: gate.validate_package(planp,REPO,True),'INTERMEDIATE_PRODUCTION_PLAN_NOT_UPLOADABLE'); ok('NEGATIVE_PRODUCTION_PLAN_BLOCKED')
        tam=copy.deepcopy(env); tam['source']='TAMPER'; tp=td/'tamper.json';tp.write_text(json.dumps(tam)); expect_block(lambda: gate.validate_package(tp,REPO,True),'HANDOFF_PACKAGE_PAYLOAD_HASH_MISMATCH'); ok('NEGATIVE_TAMPER_BLOCKED')
        bad=copy.deepcopy(env); bad['workflow_release']['contract']='WORKFLOW_SUPERVISOR_RELEASE_V2_SIGNED'; bad['workflow_release']['signature_b64']='legacy-internal-signer'; bad['workflow_release_sha256']=stable(bad['workflow_release']); bad['package_id']=stable({'contract':bad['contract'],'fact_pack_bundle_sha256':bad['fact_pack_bundle_sha256'],'production_plan_sha256':bad['production_plan_sha256'],'workflow_release_sha256':bad['workflow_release_sha256']}); bad['package_payload_sha256']=stable({k:v for k,v in bad.items() if k!='package_payload_sha256'}); bp=td/'legacy-signed.json';bp.write_text(json.dumps(bad)); expect_block(lambda: gate.validate_package(bp,REPO,True),'WORKFLOW_RELEASE_CONTRACT_INVALID'); ok('NEGATIVE_LEGACY_INTERNAL_SIGNER_BLOCKED')
        statep=REPO/'control/startmaster0107/runtime_inbox/RUNTIME_INBOX_STATE.json'; orig=statep.read_bytes(); snapp=REPO/'control/startmaster0107/runtime_inbox/generations/000001/SOURCE_SNAPSHOT.json'; sorig=snapp.read_bytes(); sobj=json.loads(sorig); sobj['next_textmachine_metadata_batch']['items'][0]['plan_slot']='e'*64; snapp.write_text(json.dumps(sobj)); st=json.loads(statep.read_text()); st['source_snapshot_sha256']=gate.file_sha(snapp); statep.write_text(json.dumps(st))
        try: expect_block(lambda: gate.validate_package(pkg,REPO,True),'PACKAGE_NOT_EXACT_CURRENT_GENERATION'); ok('NEGATIVE_CURRENT_BATCH_DRIFT_BLOCKED')
        finally: snapp.write_bytes(sorig); statep.write_bytes(orig)
        manifest=gate.build_recovery_manifest(planp,REPO); assert manifest['item_count']==7 and manifest['content_mutation_allowed'] is False and manifest['metadata_reselection_allowed'] is False and manifest['new_topic_research_allowed'] is False; ok('POSITIVE_EXISTING_TEXT_RECOVERY_LOCK')
        mp=td/'recovery.json';mp.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n'); assert gate.verify_recovery_manifest(mp,planp,REPO)['ok']; ok('POSITIVE_RECOVERY_LOCK_REVERIFY')
        changed=json.loads(planp.read_text()); changed['items'][0]['canonical_article']['body_html']+='x'; cp1=td/'changed-plan.json';cp1.write_text(json.dumps(changed)); expect_block(lambda: gate.verify_recovery_manifest(mp,cp1,REPO),'RECOVERY_BODY_HTML_HASH_INVALID'); ok('NEGATIVE_ARTICLE_MUTATION_BLOCKED')
        changed=json.loads(planp.read_text()); changed['source_ready_batch']['bindings'][0]['title']='Changed'; cp2=td/'changed-meta.json';cp2.write_text(json.dumps(changed)); expect_block(lambda: gate.build_recovery_manifest(cp2,REPO),'RECOVERY_METADATA_DRIFT:title'); ok('NEGATIVE_METADATA_DRIFT_BLOCKED')
        u=td/'unknown.json';u.write_text(json.dumps({'contract':'OTHER'})); expect_block(lambda: gate.validate_package(u,REPO,False),'UPLOAD_ARTIFACT_CONTRACT_INVALID'); ok('NEGATIVE_UNKNOWN_CONTRACT_BLOCKED')
        assert p['publish_allowed'] is False and p['content_semantics_inspected'] is False and p['content_mutation_performed'] is False; ok('SCOPE_NO_CONTENT_NO_PUBLISH')
    assert len(checks)==12
    return {'contract':'PFERDE_ATELIER_PRODUCTION_PACKAGE_RELEASE_ROOTFIX_TEST_V1','status':'PASS','checks_passed':len(checks),'checks_total':len(checks),'checks':checks}

if __name__=='__main__': print(json.dumps(run(),ensure_ascii=False,indent=2))
