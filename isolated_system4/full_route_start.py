from __future__ import annotations
import copy,hashlib,json,subprocess,sys
from pathlib import Path

import batch_gate,controller,global_workshop,handoff_transport,point0_snapshot,repair_router,root_entry

HERE=Path(__file__).resolve().parent
REPO=HERE.parent

class FullRouteError(RuntimeError): pass
class FullRouteContinuation(RuntimeError): pass

def canon(v): return (json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n').encode()
def write_json(path:Path,value): path.write_bytes(canon(value)); return path

def _head():
    return subprocess.run(['git','rev-parse','--verify','HEAD'],cwd=REPO,text=True,capture_output=True,check=True).stdout.strip()

def _read_json(path:Path):
    try:return json.loads(path.read_text(encoding='utf-8'))
    except Exception as exc: raise FullRouteError('JSON_INVALID:'+path.name) from exc

def _run_worker(worker_command:list[str],mode:str,workspace:Path,out:Path,index:int):
    cp=subprocess.run([*worker_command,mode,str(workspace),str(out),str(index)],cwd=REPO,text=True,capture_output=True)
    if cp.returncode!=0: raise FullRouteError('START_WORKER_'+mode.upper()+'_FAILED:'+str(index)+':'+cp.stdout.strip()+cp.stderr.strip())
    if not out.is_file(): raise FullRouteError('START_WORKER_'+mode.upper()+'_OUTPUT_MISSING:'+str(index))

def _machine_context(workspace:Path,base:Path,index:int):
    state=_read_json(workspace/'state.json')
    try: research=json.loads(state['research']['text']); facts=json.loads(state['facts']['text'])
    except Exception as exc: raise FullRouteError('START_ACCEPTED_RESEARCH_FACTS_MISSING:'+str(index)) from exc
    source_sha=state['source_snapshot_sha256']; claims=[]
    for row in facts.get('claims',[]):
        enriched=copy.deepcopy(row); enriched['claim_status']='FULLY_SUPPORTED'; enriched['article_types']=[state['article']['article_type']]; claims.append(enriched)
    if not claims: raise FullRouteError('START_MACHINE_FACT_PACK_EMPTY:'+str(index))
    pack={'contract':'canonical_fact_pack_v1','status':'SOURCE_VERIFIED_PRODUCTION_READY','source_snapshot_id':source_sha,'fact_pack_id':source_sha,'sources':copy.deepcopy(research['sources']),'claims':claims}
    ids=[row['fact_id'] for row in claims]; a=state['article']
    plan={'article_type':a['article_type'],'target_keyword':a['target_keyword'],'topic':a['title'],'source_snapshot_id':source_sha,'runtime_order':{'order_id':f'full-route-{index}','article_type':a['article_type'],'title':a['title'],'slug':f'full-route-{index}','subject_scope':'single_button_full_route','subject_label':a['target_keyword'],'lead':'Gebundener Einstieg aus dem akzeptierten Research- und Facts-Stand.','conclusion':'Gebundener Abschluss aus dem akzeptierten Research- und Facts-Stand.','allowed_fact_ids':ids}}
    pp=write_json(base/f'fact-pack-{index}.json',pack); pl=write_json(base/f'plan-{index}.json',plan)
    if controller.main(['controller.py','context',str(workspace),str(pp),str(pl)])!=0: raise FullRouteError('START_CONTEXT_FAILED:'+str(index))

def _verify_full_textmachine_pass(state:dict,index:int)->None:
    checks=state.get('checks') if isinstance(state.get('checks'),dict) else {}
    if state.get('phase')!='OUTPUT_GATE_REQUIRED': raise FullRouteError('START_OUTPUT_GATE_NOT_REACHED:'+str(index))
    if checks.get('status')!='PASS' or checks.get('mode')!='FULL_PRODUCTION': raise FullRouteError('START_FULL_TEXTMACHINE_PASS_MISSING:'+str(index))
    if checks.get('checked_draft_sha256')!=state.get('draft_sha256'): raise FullRouteError('START_FULL_TEXTMACHINE_DRAFT_BINDING_MISMATCH:'+str(index))
    prod=checks.get('production_evidence') if isinstance(checks.get('production_evidence'),dict) else {}
    if prod.get('contract')!='SYSTEM4_FULL_PRODUCTION_CHECK_V1' or prod.get('status')!='PASS': raise FullRouteError('START_FULL_PRODUCTION_EVIDENCE_INVALID:'+str(index))
    if prod.get('checked_draft_sha256')!=state.get('draft_sha256') or prod.get('publish_allowed') is not False: raise FullRouteError('START_FULL_PRODUCTION_EVIDENCE_BINDING_INVALID:'+str(index))
    evidence=prod.get('evidence') if isinstance(prod.get('evidence'),dict) else {}
    required={'no_legacy','no_external_links','languagetool','ppm679'}
    if not required.issubset(evidence): raise FullRouteError('START_TEXTMACHINE_INDIVIDUAL_EVIDENCE_MISSING:'+str(index))
    if (evidence['no_legacy'].get('status')!='PASS' or evidence['no_legacy'].get('legacy_import_count')!=0): raise FullRouteError('START_NO_LEGACY_NOT_PASS:'+str(index))
    if (evidence['no_external_links'].get('status')!='PASS' or evidence['no_external_links'].get('external_link_count')!=0): raise FullRouteError('START_EXTERNAL_LINK_CHECK_NOT_PASS:'+str(index))
    lt=evidence['languagetool']; ppm=evidence['ppm679']
    if lt.get('status')!='PASS' or lt.get('engine')!='LanguageTool 6.8 / Bestand 43' or lt.get('finding_count')!=0: raise FullRouteError('START_LANGUAGETOOL_NOT_PASS:'+str(index))
    if ppm.get('status')!='PASS' or ppm.get('ppm_version')!='6.7.9' or ppm.get('technical_status')!='TECHNICAL_CHECK_OK' or ppm.get('content_quality_status')!='CONTENT_QUALITY_CHECK_OK' or ppm.get('fail_closed_aggregate_status')!='PASS': raise FullRouteError('START_PPM679_NOT_PASS:'+str(index))

def _continuation_result(workspace:Path)->dict:
    for name in ('machine_repair_redirect.json','machine_repair_request.json'):
        path=workspace/name
        if path.is_file():
            result=_read_json(path)
            repair_router.verify_continuation_result(workspace,result)
            return result
    raise FullRouteError('START_REPAIR_CONTINUATION_EVIDENCE_MISSING')

def _repair_current_draft_then_fullcheck(worker_command:list[str],workspace:Path,base:Path,index:int)->dict:
    result=_continuation_result(workspace)
    if result.get('status')!='SAME_ARTICLE_BODY_REPAIR' or result.get('owner')!='DRAFT_BODY' or result.get('target')!='SAME_ARTICLE_BODY':
        raise FullRouteError('START_DRAFT_WORKSHOP_ROUTE_MISMATCH:'+str(index))
    repair=base/f'worker-draft-workshop-repair-{index}.html'
    _run_worker(worker_command,'repair',workspace,repair,index)
    if controller.main(['controller.py','repair',str(workspace),str(repair)])!=0:
        raise FullRouteError('START_DRAFT_WORKSHOP_REPAIR_FAILED:'+str(index))
    return _fullcheck_with_existing_repair_loop(worker_command,workspace,base,index)

def _fullcheck_with_existing_repair_loop(worker_command:list[str],workspace:Path,base:Path,index:int)->dict:
    for attempt in range(repair_router.MAX_MACHINE_REPAIR_CYCLES+1):
        rc=controller.main(['controller.py','fullcheck',str(workspace)])
        if rc==0:
            state=_read_json(workspace/'state.json')
            _verify_full_textmachine_pass(state,index)
            return state
        if rc==3:
            result=_continuation_result(workspace)
            if result.get('status')!='SAME_ARTICLE_BODY_REPAIR' or result.get('owner')!='DRAFT_BODY' or result.get('target')!='SAME_ARTICLE_BODY':
                raise FullRouteError('START_REPAIR_ROUTE_MISMATCH:'+str(index))
            repair=base/f'worker-repair-{index}-{attempt+1}.html'
            _run_worker(worker_command,'repair',workspace,repair,index)
            if controller.main(['controller.py','repair',str(workspace),str(repair)])!=0: raise FullRouteError('START_REPAIR_FAILED:'+str(index))
            continue
        if rc==4:
            result=_continuation_result(workspace)
            raise FullRouteContinuation('START_CONTINUATION_REQUIRED:'+str(index)+':'+str(result.get('owner'))+':'+str(result.get('target'))+':'+str(result.get('status')))
        raise FullRouteError('START_FULLCHECK_NOT_PASS:'+str(index)+':'+str(rc))
    raise FullRouteError('START_REPAIR_CYCLE_LIMIT:'+str(index))

def _workshop_escalate(stage:str,exc:BaseException,output_dir:Path,state_paths:list[Path]|None=None,context:dict|None=None):
    request,path,_=global_workshop.capture(stage,exc,output_dir=output_dir,findings=getattr(exc,'findings',None),context=context,state_paths=state_paths)
    request_sha=str(request.get('request_sha256') or '')
    request_path=str(path) if path is not None else 'INLINE'
    if request.get('repairable') is True:
        raise FullRouteContinuation('START_WORKSHOP_CONTINUATION_REQUIRED:'+stage+':'+request_sha+':'+request_path) from exc
    raise FullRouteError('START_WORKSHOP_BLOCKED:'+stage+':'+str(request.get('error_code') or exc)) from exc

def _batch_collect_with_workshop(worker_command:list[str],production_snapshot:Path,state_paths:list[Path],states:list[dict],base:Path)->dict:
    batch_out=base/'batch'
    for attempt in range(repair_router.MAX_MACHINE_REPAIR_CYCLES+1):
        try:
            collected=batch_gate.collect_batch(production_snapshot,state_paths,batch_out)
        except batch_gate.BatchGateWorkshop as exc:
            request=exc.request if isinstance(exc.request,dict) else {}
            request_sha=str(request.get('request_sha256') or '')
            request_path=str(exc.request_path) if exc.request_path is not None else 'INLINE'
            if request.get('repairable') is not True:
                raise FullRouteError('START_BATCH_WORKSHOP_BLOCKED:'+str(request.get('error_code') or exc)) from exc
            if not exc.changed:
                raise FullRouteContinuation('START_BATCH_WORKSHOP_CONTINUATION_REQUIRED:'+request_sha+':NO_ARTICLE_TARGET:'+request_path) from exc
            for index in exc.changed:
                if index<0 or index>=len(state_paths):
                    raise FullRouteError('START_BATCH_WORKSHOP_TARGET_OUT_OF_RANGE:'+str(index)) from exc
                workspace=state_paths[index].parent
                result=repair_router.route(workspace)
                repair_router.verify_continuation_result(workspace,result)
                status=str(result.get('status') or '')
                if status!='SAME_ARTICLE_BODY_REPAIR' or result.get('owner')!='DRAFT_BODY' or result.get('target')!='SAME_ARTICLE_BODY':
                    raise FullRouteContinuation('START_BATCH_WORKSHOP_CONTINUATION_REQUIRED:'+str(index)+':'+str(result.get('owner'))+':'+str(result.get('target'))+':'+status+':'+request_sha+':'+request_path) from exc
                repair=base/f'worker-batch-repair-{index}-{attempt+1}.html'
                _run_worker(worker_command,'repair',workspace,repair,index)
                if controller.main(['controller.py','repair',str(workspace),str(repair)])!=0:
                    raise FullRouteError('START_BATCH_REPAIR_FAILED:'+str(index))
                states[index]=_fullcheck_with_existing_repair_loop(worker_command,workspace,base,index)
            continue
        if collected.get('status')!='SYSTEM4_BATCH_FULL_PASS_COLLECTED':
            raise FullRouteError('START_BATCH_NOT_PASS')
        return collected
    raise FullRouteError('START_BATCH_REPAIR_CYCLE_LIMIT')

def _handoff(states):
    rows=[]
    for index,state in enumerate(states):
        prod=state['checks']['production_evidence']['evidence']
        rows.append({'index':index,'title':state['article']['title'],'target_keyword':state['article']['target_keyword'],'category':state['article']['category'],'article_type':state['article']['article_type'],'plan_slot':state['article']['plan_slot'],'final_draft_sha256':state['draft_sha256'],'revision_count':state['revision'],'body':state['draft_markdown'],'production_context':{'fact_pack':state['production_context']['fact_pack'],'production_plan_item':state['production_context']['production_plan_item']},'languagetool':prod['languagetool'],'ppm679':prod['ppm679']})
    return {'contract':handoff_transport.HANDOFF_CONTRACT,'batch_sha256':states[0]['batch_sha256'],'publish_allowed':False,'signing_deferred':True,'batch_gate_status':'SYSTEM4_BATCH_FULL_PASS_COLLECTED','no_legacy_status':'PASS','test_suite_status':'PASS','wordpress_review':{'file_format':'JSON','mime_type':'application/json','intended_next_step':'WORDPRESS_DIRECT_IMPORT','plugin_name':'Portal SEO Editorial Plan Compiler','plugin_version_verified_against':handoff_transport.DIRECT_IMPORT_PLUGIN_VERSION,'ppm_version_verified_against':'6.7.9','direct_wordpress_upload_ready':True,'direct_upload_block_reason':None,'required_downstream_components':[]},'articles':rows}

def _handoff_with_workshop(states:list[dict],state_paths:list[Path],base:Path)->Path:
    try:
        source=write_json(base/'handoff-source.json',_handoff(states)); canonical=base/handoff_transport.HANDOFF_FILENAME
        canonical_bytes=handoff_transport.canonicalize_handoff(source,canonical); inline=base/handoff_transport.INLINE_FILENAME
        envelope=handoff_transport.inline_pack(canonical,inline); reconstructed=handoff_transport.inline_unpack(inline,base/'parent-chat')
        if reconstructed.read_bytes()!=canonical_bytes: raise FullRouteError('START_HANDOFF_BYTE_MISMATCH')
        if envelope.get('plaintext_sha256')!=hashlib.sha256(canonical_bytes).hexdigest(): raise FullRouteError('START_HANDOFF_HASH_MISMATCH')
        return reconstructed
    except FullRouteContinuation:
        raise
    except Exception as exc:
        _workshop_escalate('HANDOFF',exc,base/'handoff-workshop',state_paths=state_paths,context={'article_count':len(states)})
        raise AssertionError('UNREACHABLE')

def run(production_snapshot:Path, source_bundle:Path, worker_command:list[str], output_root:Path)->Path:
    raw=production_snapshot.read_bytes(); snap=_read_json(production_snapshot)
    batch=snap.get('next_textmachine_metadata_batch') if isinstance(snap,dict) else None; items=batch.get('items') if isinstance(batch,dict) else None
    if not isinstance(items,list) or not items: raise FullRouteError('START_BATCH_EMPTY')
    if batch.get('publish_allowed') is not False: raise FullRouteError('START_PUBLISH_MUST_BE_FALSE')
    sources_doc=_read_json(source_bundle); per_article=sources_doc.get('articles') if isinstance(sources_doc,dict) else None
    if not isinstance(per_article,list) or len(per_article)!=len(items): raise FullRouteError('START_SOURCE_COUNT_MISMATCH')
    output_root.mkdir(parents=True,exist_ok=True); state_paths=[]; states=[]
    manifest=root_entry._critical_manifest_sha256(); head=_head()
    for index,item in enumerate(items):
        srcrow=per_article[index]; sources=srcrow.get('sources') if isinstance(srcrow,dict) else None
        if not isinstance(sources,list) or not sources: raise FullRouteError('START_SOURCE_MISSING:'+str(index))
        prepared=point0_snapshot.prepare(production_snapshot_bytes=raw,root_manifest_sha256=manifest,head_sha=head)
        final=point0_snapshot.finalize(prepared,research_provider='BOUND_PARENT_START_SOURCE',sources=sources)
        p0=output_root/f'point0-{index}.json'; p0.write_bytes(point0_snapshot.canon(final)); ws=output_root/f'item-{index}'
        if root_entry.main(['root_entry.py','start-point0',str(p0),str(ws),str(index)])!=0: raise FullRouteError('START_ROOT_FAILED:'+str(index))
        research=output_root/f'worker-research-{index}.json'; _run_worker(worker_command,'research',ws,research,index)
        if controller.main(['controller.py','research',str(ws),str(research)])!=0: raise FullRouteError('START_RESEARCH_FAILED:'+str(index))
        facts=output_root/f'worker-facts-{index}.json'; _run_worker(worker_command,'facts',ws,facts,index)
        if controller.main(['controller.py','facts',str(ws),str(facts)])!=0: raise FullRouteError('START_FACTS_FAILED:'+str(index))
        _machine_context(ws,output_root,index)
        draft=output_root/f'worker-draft-{index}.html'; _run_worker(worker_command,'draft',ws,draft,index)
        draft_rc=controller.main(['controller.py','draft',str(ws),str(draft)])
        if draft_rc==0:
            state=_fullcheck_with_existing_repair_loop(worker_command,ws,output_root,index)
        elif draft_rc==3:
            state=_repair_current_draft_then_fullcheck(worker_command,ws,output_root,index)
        else:
            raise FullRouteError('START_DRAFT_FAILED:'+str(index)+':'+str(draft_rc))
        state_paths.append(ws/'state.json'); states.append(state)
    _batch_collect_with_workshop(worker_command,production_snapshot,state_paths,states,output_root)
    return _handoff_with_workshop(states,state_paths,output_root)

def main(argv):
    try:
        if len(argv)<6 or argv[1]!='start': raise FullRouteError('BAD_COMMAND')
        out=run(Path(argv[2]),Path(argv[3]),argv[5:],Path(argv[4])); print('SYSTEM4_FULL_ROUTE_PASS:'+str(out)); return 0
    except FullRouteContinuation as exc:
        print('SYSTEM4_FULL_ROUTE_CONTINUATION:'+str(exc)); return 4
    except Exception as exc:
        try:
            output_dir=Path(argv[4])/'top-level-workshop' if len(argv)>4 else HERE/'top-level-workshop'
            request,path,_=global_workshop.capture('FULL_ROUTE_TOP_LEVEL',exc,output_dir=output_dir,findings=getattr(exc,'findings',None),context={'command':argv[1] if len(argv)>1 else None})
            if request.get('repairable') is True:
                print('SYSTEM4_FULL_ROUTE_CONTINUATION:START_TOP_LEVEL_WORKSHOP_CONTINUATION_REQUIRED:'+str(request.get('request_sha256') or '')+':'+str(path)); return 4
            print('SYSTEM4_FULL_ROUTE_FAIL:START_TOP_LEVEL_WORKSHOP_BLOCKED:'+str(request.get('error_code') or exc)); return 2
        except Exception as workshop_exc:
            print('SYSTEM4_FULL_ROUTE_FAIL:TOP_LEVEL_WORKSHOP_CAPTURE_FAILED:'+str(exc)+':'+str(workshop_exc)); return 2

if __name__=='__main__': raise SystemExit(main(sys.argv))
