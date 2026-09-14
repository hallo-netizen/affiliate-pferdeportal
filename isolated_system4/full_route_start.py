from __future__ import annotations
import hashlib,json,subprocess,sys
from pathlib import Path

import batch_gate,codex_entry,controller,handoff_transport,point0_snapshot,root_entry

HERE=Path(__file__).resolve().parent
REPO=HERE.parent

class FullRouteError(RuntimeError): pass

def canon(v): return (json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n').encode()
def write_json(path:Path,value): path.write_bytes(canon(value)); return path

def _head():
    return subprocess.run(['git','rev-parse','--verify','HEAD'],cwd=REPO,text=True,capture_output=True,check=True).stdout.strip()

def _read_json(path:Path):
    try:return json.loads(path.read_text(encoding='utf-8'))
    except Exception as exc: raise FullRouteError('JSON_INVALID:'+path.name) from exc

def _handoff(states):
    rows=[]
    for index,state in enumerate(states):
        prod=state['checks']['production_evidence']['evidence']
        rows.append({'index':index,'title':state['article']['title'],'target_keyword':state['article']['target_keyword'],'category':state['article']['category'],'article_type':state['article']['article_type'],'plan_slot':state['article']['plan_slot'],'final_draft_sha256':state['draft_sha256'],'revision_count':state['revision'],'body':state['draft_markdown'],'production_context':{'fact_pack':state['production_context']['fact_pack'],'production_plan_item':state['production_context']['production_plan_item']},'languagetool':prod['languagetool'],'ppm679':prod['ppm679']})
    return {'contract':handoff_transport.HANDOFF_CONTRACT,'batch_sha256':states[0]['batch_sha256'],'publish_allowed':False,'signing_deferred':True,'batch_gate_status':'SYSTEM4_BATCH_FULL_PASS_COLLECTED','no_legacy_status':'PASS','test_suite_status':'PASS','wordpress_review':{'file_format':'JSON','mime_type':'application/json','intended_next_step':'WORDPRESS_DIRECT_IMPORT','plugin_name':'Portal SEO Editorial Plan Compiler','plugin_version_verified_against':handoff_transport.DIRECT_IMPORT_PLUGIN_VERSION,'ppm_version_verified_against':'6.7.9','direct_wordpress_upload_ready':True,'direct_upload_block_reason':None,'required_downstream_components':[]},'articles':rows}

def run(production_snapshot:Path, source_bundle:Path, worker_command:list[str], output_root:Path)->Path:
    raw=production_snapshot.read_bytes(); snap=_read_json(production_snapshot)
    batch=snap.get('next_textmachine_metadata_batch') if isinstance(snap,dict) else None
    items=batch.get('items') if isinstance(batch,dict) else None
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
        if codex_entry.main(['codex_entry.py','worker-start',str(ws)])!=0: raise FullRouteError('START_CODEX_WORKER_START_FAILED:'+str(index))
        worker_out=output_root/f'worker-{index}'; worker_out.mkdir()
        cp=subprocess.run([*worker_command,str(ws),str(worker_out)],cwd=REPO,text=True,capture_output=True)
        if cp.returncode!=0: raise FullRouteError('START_WORKER_FAILED:'+str(index)+':'+cp.stdout.strip()+cp.stderr.strip())
        required={name:worker_out/name for name in ('research.json','facts.json','fact_pack.json','plan.json','draft.html')}
        if not all(p.is_file() for p in required.values()): raise FullRouteError('START_WORKER_OUTPUT_MISSING:'+str(index))
        if controller.main(['controller.py','research',str(ws),str(required['research.json'])])!=0: raise FullRouteError('START_RESEARCH_FAILED:'+str(index))
        if controller.main(['controller.py','facts',str(ws),str(required['facts.json'])])!=0: raise FullRouteError('START_FACTS_FAILED:'+str(index))
        if controller.main(['controller.py','context',str(ws),str(required['fact_pack.json']),str(required['plan.json'])])!=0: raise FullRouteError('START_CONTEXT_FAILED:'+str(index))
        if controller.main(['controller.py','draft',str(ws),str(required['draft.html'])])!=0: raise FullRouteError('START_DRAFT_FAILED:'+str(index))
        rc=controller.main(['controller.py','fullcheck',str(ws)])
        if rc!=0: raise FullRouteError('START_FULLCHECK_NOT_PASS:'+str(index)+':'+str(rc))
        state=_read_json(ws/'state.json')
        if state.get('phase')!='OUTPUT_GATE_REQUIRED': raise FullRouteError('START_OUTPUT_GATE_NOT_REACHED:'+str(index))
        state_paths.append(ws/'state.json'); states.append(state)
    batch_out=output_root/'batch'; collected=batch_gate.collect_batch(production_snapshot,state_paths,batch_out)
    if collected.get('status')!='SYSTEM4_BATCH_FULL_PASS_COLLECTED': raise FullRouteError('START_BATCH_NOT_PASS')
    source=write_json(output_root/'handoff-source.json',_handoff(states)); canonical=output_root/handoff_transport.HANDOFF_FILENAME
    canonical_bytes=handoff_transport.canonicalize_handoff(source,canonical); inline=output_root/handoff_transport.INLINE_FILENAME
    envelope=handoff_transport.inline_pack(canonical,inline); reconstructed=handoff_transport.inline_unpack(inline,output_root/'parent-chat')
    if reconstructed.read_bytes()!=canonical_bytes: raise FullRouteError('START_HANDOFF_BYTE_MISMATCH')
    if envelope.get('plaintext_sha256')!=hashlib.sha256(canonical_bytes).hexdigest(): raise FullRouteError('START_HANDOFF_HASH_MISMATCH')
    return reconstructed

def main(argv):
    try:
        if len(argv)<6 or argv[1]!='start': raise FullRouteError('BAD_COMMAND')
        out=run(Path(argv[2]),Path(argv[3]),argv[5:],Path(argv[4])); print('SYSTEM4_FULL_ROUTE_PASS:'+str(out)); return 0
    except Exception as exc:
        print('SYSTEM4_FULL_ROUTE_FAIL:'+str(exc)); return 2

if __name__=='__main__': raise SystemExit(main(sys.argv))
