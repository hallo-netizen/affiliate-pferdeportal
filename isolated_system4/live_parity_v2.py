from __future__ import annotations
import copy, hashlib, json, os, re, shutil, subprocess, sys, tempfile
from pathlib import Path

import handoff_transport

HERE=Path(__file__).resolve().parent
REPO=HERE.parent
FIX=Path(os.environ.get('SYSTEM4_LIVE_PARITY_FIXTURE','')).expanduser()
TESTWORKER=HERE/'deterministic_test_worker.py'
FRESH_TOKEN_ENV='SYSTEM4_FRESH_RUN_TOKEN'

def fail(msg): raise RuntimeError(msg)
def env():
    jar=os.environ.get('SYSTEM4_LANGUAGETOOL_JAR','').strip()
    if not jar: fail('SYSTEM4_LANGUAGETOOL_JAR_REQUIRED')
    e=os.environ.copy(); e['PYTHONDONTWRITEBYTECODE']='1'; e['SYSTEM4_LANGUAGETOOL_JAR']=jar; return e
def run(args,e,check=True):
    cp=subprocess.run([str(x) for x in args],cwd=REPO,text=True,capture_output=True,env=e)
    if check and cp.returncode: fail('COMMAND_FAIL:'+cp.stdout.strip()+':'+cp.stderr.strip())
    return cp
def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def writej(p,v):
    p=Path(p); p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(v,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8')
def _sha_text(value:str)->str: return hashlib.sha256(value.encode('utf-8')).hexdigest()
def _fresh_token_sha()->str:
    token=str(os.environ.get(FRESH_TOKEN_ENV) or '').strip()
    if len(token)<16: fail('SYSTEM4_FRESH_RUN_TOKEN_REQUIRED')
    return _sha_text(token)

def _fixture()->Path:
    if not str(FIX) or str(FIX)=='.' or not FIX.is_dir(): fail('SYSTEM4_LIVE_PARITY_FIXTURE_REQUIRED')
    return FIX.resolve()

def _walk_json_bodies(value, path=''):
    if isinstance(value,dict):
        for key,child in value.items():
            p=(path+'.'+str(key)).strip('.')
            key_cf=str(key).casefold()
            if isinstance(child,str) and any(token in key_cf for token in ('body','content_html','draft','article_html','final_html')) and len(child.strip())>=80:
                yield p,child
            yield from _walk_json_bodies(child,p)
    elif isinstance(value,list):
        for index,child in enumerate(value):
            yield from _walk_json_bodies(child,path+'['+str(index)+']')

def _visible_hash(value:str)->str:
    text=re.sub(r'(?is)<script\b.*?</script>|<style\b.*?</style>',' ',value)
    text=re.sub(r'(?s)<[^>]+>',' ',text)
    text=' '.join(text.split()).casefold()
    return _sha_text(text) if text else ''

def _historical_article_hashes()->tuple[set[str],set[str]]:
    """Collect old article/body material already present in the checkout.

    This is deliberately repository-read-only. A current acceptance draft may not equal
    a historical body/recovery/candidate either byte-for-byte or as normalized visible
    text. This closes the old fixture/recovery/candidate reuse failure class.
    """
    exact:set[str]=set(); visible:set[str]=set()
    for path in REPO.rglob('*'):
        if not path.is_file(): continue
        rel=path.relative_to(REPO).as_posix().casefold()
        if rel.startswith('.git/'): continue
        suffix=path.suffix.casefold()
        interesting=(
            suffix in {'.html','.htm'} or
            ('recovery_sources/' in rel and suffix in {'.md','.txt'}) or
            ('article_' in path.name.casefold() and suffix in {'.md','.txt','.html'}) or
            ('candidate' in path.name.casefold() and suffix=='.json') or
            ('fixture' in rel and suffix=='.json')
        )
        if not interesting: continue
        try:
            raw=path.read_bytes()
        except OSError:
            continue
        if len(raw)>5_000_000: continue
        if suffix=='.json':
            try: obj=json.loads(raw.decode('utf-8'))
            except Exception: continue
            for _,body in _walk_json_bodies(obj):
                exact.add(_sha_text(body)); vh=_visible_hash(body)
                if vh: visible.add(vh)
        else:
            try: text=raw.decode('utf-8')
            except UnicodeDecodeError: continue
            if len(text.strip())>=80:
                exact.add(_sha_text(text)); vh=_visible_hash(text)
                if vh: visible.add(vh)
    return exact,visible

def _verify_fresh_fixture(fix:Path)->dict:
    proof_path=fix/'input_factory_proof.json'; freshness_path=fix/'freshness.json'
    if not proof_path.is_file(): fail('SYSTEM4_INPUT_FACTORY_PROOF_MISSING')
    if not freshness_path.is_file(): fail('SYSTEM4_FRESHNESS_PROOF_MISSING')
    proof=load(proof_path); fresh=load(freshness_path); expected=_fresh_token_sha()
    if proof.get('contract')!='SYSTEM4_TEST_ROUTE_INPUT_FACTORY_V5': fail('SYSTEM4_INPUT_FACTORY_CONTRACT_INVALID')
    if proof.get('freshness_required') is not True: fail('SYSTEM4_FRESHNESS_NOT_REQUIRED_BY_FACTORY')
    if proof.get('g9_candidate_used') is not False or proof.get('old_article_body_used') is not False: fail('SYSTEM4_OLD_ARTICLE_INPUT_FORBIDDEN')
    if proof.get('fresh_run_token_sha256')!=expected: fail('SYSTEM4_FRESH_RUN_TOKEN_BINDING_MISMATCH')
    if fresh.get('contract')!='SYSTEM4_FRESH_ARTICLE_INPUT_V1': fail('SYSTEM4_FRESHNESS_CONTRACT_INVALID')
    if fresh.get('fresh_run_token_sha256')!=expected: fail('SYSTEM4_FRESHNESS_TOKEN_MISMATCH')
    if fresh.get('article_body_source_allowed') is not False or fresh.get('old_article_fixture_allowed') is not False or fresh.get('recovery_article_allowed') is not False or fresh.get('ppm_candidate_article_allowed') is not False:
        fail('SYSTEM4_FRESHNESS_OLD_BODY_POLICY_INVALID')
    if fresh.get('pre_point0_article_body_count')!=0: fail('SYSTEM4_PRE_POINT0_ARTICLE_BODY_FORBIDDEN')
    snapshot=load(fix/'snapshot.template.json'); items=snapshot.get('next_textmachine_metadata_batch',{}).get('items') or []
    if [row.get('title') for row in items]!=fresh.get('titles'): fail('SYSTEM4_FRESHNESS_TITLE_BINDING_MISMATCH')
    if [row.get('plan_slot') for row in items]!=fresh.get('plan_slots'): fail('SYSTEM4_FRESHNESS_SLOT_BINDING_MISMATCH')
    acquired=load(fix/'acquired.json')
    actual_source_ids=[[s.get('source_id') for s in row.get('sources',[])] for row in acquired.get('items',[])]
    if actual_source_ids!=fresh.get('source_ids'): fail('SYSTEM4_FRESHNESS_SOURCE_BINDING_MISMATCH')
    if len(set(fresh.get('title_sha256') or []))!=len(items): fail('SYSTEM4_FRESHNESS_TITLE_COLLISION')
    return fresh

def prepare(runroot:Path)->dict:
    global FIX; FIX=_fixture()
    sys.path.insert(0,str(HERE)); import root_entry, machine_point0, point0_snapshot
    if runroot.exists() and any(runroot.iterdir()): fail('RUNROOT_NOT_EMPTY')
    runroot.mkdir(parents=True,exist_ok=True)
    fresh=_verify_fresh_fixture(FIX)
    start_file=FIX/'start_button.json'
    if not start_file.is_file(): fail('SYSTEM4_CHAT_START_BUTTON_FIXTURE_REQUIRED')
    if list(FIX.glob('**/article*.html')) or list(FIX.glob('**/draft*.html')) or list(FIX.glob('**/repair*.html')): fail('PRE_POINT0_ARTICLE_FIXTURE_FORBIDDEN')
    manifest=root_entry._critical_manifest_sha256(); head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip()
    snap=load(FIX/'snapshot.template.json'); snap=machine_point0.bind_chat_start(snap,load(start_file)); snap['system4_root_manifest_sha256']=manifest
    raw=(json.dumps(snap,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n').encode()
    p0=machine_point0.build_from_acquired(snapshot_bytes=raw,acquired_batch=load(FIX/'acquired.json'),prewrite_plan_batch=load(FIX/'plans.json'),provider='SYSTEM4_LIVE_PARITY_V2_MACHINE_ACQUIRED_TEST_SOURCES',manifest=manifest,head=head)
    (runroot/'snapshot.json').write_bytes(raw); (runroot/'point0.json').write_bytes(point0_snapshot.canon(p0))
    receipt=snap['system4_chat_start']
    meta={'head':head,'manifest':manifest,'article_count':len(snap['next_textmachine_metadata_batch']['items']),'point0_sha256':p0['point0_core_sha256'],'chat_start_receipt_sha256':receipt['receipt_sha256'],'pre_point0_article_body_count':0,'freshness_verified':True,'fresh_run_token_sha256':fresh['fresh_run_token_sha256'],'fresh_title_sha256':fresh['title_sha256'],'fresh_source_ids':fresh['source_ids']}; writej(runroot/'run_meta.json',meta)
    return meta

def _worker_generate(e,workspace:Path,generated:Path,stage:str,*outs:Path):
    generated.mkdir(parents=True,exist_ok=True)
    return run([sys.executable,TESTWORKER,stage,workspace,*outs],e)

def _stage_with_return(e,workspace:Path,generated:Path,stage:str,controller_args:list[Path|str],*outs:Path)->list[str]:
    """Execute one producer stage and honor rc=4 as a mandatory return, never a block."""
    events=[]
    for attempt in range(2):
        _worker_generate(e,workspace,generated,stage,*outs)
        cp=run([sys.executable,HERE/'controller.py',*controller_args],e,check=False)
        if cp.returncode==0: return events
        if cp.returncode==4 and 'SYSTEM4_STAGE_OWNER_RETURN:' in cp.stdout:
            events.append(cp.stdout.strip())
            print(cp.stdout.strip(),flush=True)
            # State is guaranteed unchanged by controller. Re-run the real producer once.
            # If the producer repeats the same invalid artifact, fail explicitly as a
            # producer repair failure rather than silently converting return into BLOCK.
            continue
        fail('UNEXPECTED_STAGE_BLOCK:'+stage+':'+cp.stdout.strip()+':'+cp.stderr.strip())
    fail('STAGE_OWNER_RETURN_REPAIR_NOT_EFFECTIVE:'+stage+':'+('|'.join(events)))

def _diagnose_fullcheck(state:dict,index:int)->None:
    sys.path.insert(0,str(HERE)); import production_checks
    ctx=state.get('production_context')
    if not isinstance(ctx,dict):
        print('SYSTEM4_FULLCHECK_DIAGNOSTIC:PRODUCTION_CONTEXT_MISSING',flush=True); return
    try:
        production_checks.run_all(REPO,state,ctx['fact_pack'],ctx['production_plan_item'])
        print('SYSTEM4_FULLCHECK_DIAGNOSTIC:NO_REPAIR_REPRODUCED',flush=True)
    except production_checks.RepairRequired as exc:
        print('SYSTEM4_FULLCHECK_DIAGNOSTIC:'+json.dumps({'article_index':index,'checker':exc.checker,'findings':exc.findings},ensure_ascii=False,sort_keys=True,default=str),flush=True)
    except Exception as exc:
        print('SYSTEM4_FULLCHECK_DIAGNOSTIC_ERROR:'+type(exc).__name__+':'+str(exc),flush=True)

def item(runroot:Path,i:int)->dict:
    e=env(); snap=load(runroot/'snapshot.json'); count=len(snap['next_textmachine_metadata_batch']['items'])
    if i<0 or i>=count: fail('ITEM_INDEX_INVALID')
    w=runroot/f'item-{i}'; generated=runroot/f'generated-{i}'
    if not (w/'state.json').is_file():
        root_cp=run([sys.executable,HERE/'root_entry.py','start-point0',runroot/'point0.json',w,str(i)],e)
        if 'SYSTEM4_ROOT_POINT0_PASS:WORKER_DISPATCH_READY' not in root_cp.stdout:
            fail('ROOT_DISPATCH_MARKER_MISSING:'+root_cp.stdout.strip())
        codex_cp=run([sys.executable,HERE/'codex_entry.py','worker-start',w],e)
        if 'SYSTEM4_CODEX_ENTRY_PASS:RESEARCH_REQUIRED' not in codex_cp.stdout:
            fail('CODEX_WORKER_START_MARKER_MISSING:'+codex_cp.stdout.strip())
        _worker_generate(e,w,generated,'gate')
    repair_events=[]; return_events=[]; cycles=0
    while True:
        cycles+=1
        if cycles>30: fail('ITEM_LOOP_LIMIT')
        s=load(w/'state.json'); phase=s['phase']
        if phase=='RESEARCH_REQUIRED':
            p=generated/'research.json'; return_events.extend(_stage_with_return(e,w,generated,'research',['research',w,p],p)); continue
        if phase=='FACT_CHECK_REQUIRED':
            p=generated/'facts.json'; return_events.extend(_stage_with_return(e,w,generated,'facts',['facts',w,p],p)); continue
        if phase=='CONTEXT_REQUIRED':
            pack=generated/'fact_pack.json'; plan=generated/'plan.json'; return_events.extend(_stage_with_return(e,w,generated,'context',['context',w,pack,plan],pack,plan)); continue
        if phase=='DRAFT_REQUIRED':
            p=generated/'draft.html'; return_events.extend(_stage_with_return(e,w,generated,'draft',['draft',w,p],p)); continue
        if phase=='CHECK_REQUIRED':
            cp=run([sys.executable,HERE/'controller.py','fullcheck',w],e,check=False)
            if cp.returncode==0: continue
            s=load(w/'state.json')
            if cp.returncode==4 and s.get('checks',{}).get('return_required') is True:
                event={'article_index':i,'repair_owners':s['checks'].get('repair_owners'),'return_route':s['checks'].get('return_route'),'last_error':s.get('last_error')}
                print('SYSTEM4_PARENT_RETURN_REQUIRED:'+json.dumps(event,ensure_ascii=False,sort_keys=True),flush=True)
                # A fullcheck parent/upstream return requires a NEW Point-0. The current
                # sealed generation may not be mutated in place. The positive acceptance
                # therefore stops this item as RETURN_REQUIRED for the parent restart
                # orchestrator; this is not a HARD_BLOCK or owner conflict.
                return {'index':i,'title':s['article']['title'],'phase':phase,'revision':s['revision'],'status':'PARENT_RETURN_REQUIRED','repair_events':repair_events,'return_events':return_events+[cp.stdout.strip()],'return_required':True,'return_route':s['checks'].get('return_route'),'repair_owners':s['checks'].get('repair_owners')}
            if s.get('phase')!='REPAIR_REQUIRED':
                _diagnose_fullcheck(s,i)
                fail('UNEXPECTED_FULLCHECK_BLOCK:'+cp.stdout.strip()+':'+cp.stderr.strip())
            repair_events.append(cp.stdout.strip()); continue
        if phase=='REPAIR_REQUIRED':
            print('SYSTEM4_TESTWORKER_REPAIR_REQUEST:'+json.dumps({'article_index':i,'last_error':s.get('last_error'),'checks':s.get('checks')},ensure_ascii=False,sort_keys=True),flush=True)
            rp=generated/f'repair-{s["revision"]}.html'; _worker_generate(e,w,generated,'repair',rp); run([sys.executable,HERE/'controller.py','repair',w,rp],e); continue
        if phase=='OUTPUT_GATE_REQUIRED':
            if s.get('checks',{}).get('status')!='PASS': fail('OUTPUT_GATE_WITHOUT_PASS')
            return {'index':i,'title':s['article']['title'],'phase':phase,'revision':s['revision'],'status':'PASS','repair_events':repair_events,'return_events':return_events}
        fail('UNEXPECTED_PHASE:'+phase)

def _handoff_payload(states:list[dict],items:list[dict],batch_sha:str)->dict:
    rows=[]
    for i,(s,itemrow) in enumerate(zip(states,items)):
        ev=s['checks']['production_evidence']['evidence']
        rows.append({'index':i,'title':itemrow['title'],'target_keyword':itemrow['target_keyword'],'category':itemrow['category'],'article_type':itemrow['article_type'],'plan_slot':itemrow['plan_slot'],'final_draft_sha256':s['draft_sha256'],'revision_count':s['revision'],'body':s['draft_markdown'],'production_context':s['production_context'],'languagetool':ev['languagetool'],'ppm679':ev['ppm679']})
    return {'contract':'SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2','batch_sha256':batch_sha,'publish_allowed':False,'signing_deferred':True,'batch_gate_status':'SYSTEM4_BATCH_FULL_PASS_COLLECTED','no_legacy_status':'PASS','test_suite_status':'PASS','wordpress_review':handoff_transport.wordpress_review(),'articles':rows}

def _assert_fresh_final_states(runroot:Path,state_values:list[dict],meta:dict)->dict:
    if meta.get('freshness_verified') is not True or meta.get('fresh_run_token_sha256')!=_fresh_token_sha():
        fail('SYSTEM4_FINAL_FRESHNESS_BINDING_INVALID')
    exact_old,visible_old=_historical_article_hashes()
    draft_hashes=[]; visible_hashes=[]
    expected_sources=meta.get('fresh_source_ids') or []
    for i,s in enumerate(state_values):
        body=str(s.get('draft_markdown') or '')
        dh=_sha_text(body); vh=_visible_hash(body)
        if dh!=s.get('draft_sha256'): fail('SYSTEM4_FINAL_DRAFT_HASH_BINDING_INVALID:'+str(i))
        if dh in exact_old: fail('SYSTEM4_HISTORICAL_ARTICLE_BODY_REUSED:'+str(i))
        if vh and vh in visible_old: fail('SYSTEM4_HISTORICAL_VISIBLE_ARTICLE_REUSED:'+str(i))
        if i>=len(expected_sources) or not expected_sources[i]: fail('SYSTEM4_FRESH_SOURCE_SET_MISSING:'+str(i))
        # Source ids are derived from the current fresh-run token and must be carried
        # into the current article's PPM traces. Old article bodies cannot satisfy this.
        missing=[sid for sid in expected_sources[i] if sid not in body]
        if missing: fail('SYSTEM4_CURRENT_RUN_SOURCE_TRACE_MISSING:'+str(i)+':'+','.join(missing))
        draft_hashes.append(dh); visible_hashes.append(vh)
    if len(draft_hashes)!=len(set(draft_hashes)): fail('SYSTEM4_CURRENT_BATCH_DRAFT_HASH_COLLISION')
    if len([v for v in visible_hashes if v])!=len(set(v for v in visible_hashes if v)): fail('SYSTEM4_CURRENT_BATCH_VISIBLE_ARTICLE_COLLISION')
    return {'freshness_status':'PASS','fresh_run_token_sha256':meta['fresh_run_token_sha256'],'historical_exact_body_reuse_blocked':True,'historical_visible_body_reuse_blocked':True,'current_source_trace_bound':True,'unique_draft_hashes':True,'unique_visible_articles':True}

def finalize(runroot:Path)->dict:
    e=env(); meta=load(runroot/'run_meta.json'); snap=load(runroot/'snapshot.json'); items=snap['next_textmachine_metadata_batch']['items']; states=[runroot/f'item-{i}'/'state.json' for i in range(len(items))]
    for i,p in enumerate(states):
        if not p.is_file(): fail('STATE_MISSING:'+str(i))
        s=load(p)
        if s.get('phase')!='OUTPUT_GATE_REQUIRED' or s.get('checks',{}).get('status')!='PASS': fail('STATE_NOT_OUTPUT_GATE:'+str(i))
    state_values=[load(p) for p in states]
    freshness=_assert_fresh_final_states(runroot,state_values,meta)
    batchdir=runroot/'batch'; shutil.rmtree(batchdir,ignore_errors=True)
    cp=run([sys.executable,HERE/'batch_gate.py','collect',runroot/'snapshot.json',batchdir,*states],e); bout=json.loads(cp.stdout)
    if bout.get('status')!='SYSTEM4_BATCH_FULL_PASS_COLLECTED': fail('BATCH_NOT_FULL_PASS')
    payload=_handoff_payload(state_values,items,snap['next_textmachine_metadata_batch']['batch_sha256'])
    working=runroot/'handoff.working.json'; writej(working,payload); canonical=runroot/'SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2.json'; inline=runroot/'SYSTEM4_PARENT_CHAT_INLINE_V2.txt'; unpack=runroot/'unpacked'; shutil.rmtree(unpack,ignore_errors=True)
    run([sys.executable,HERE/'handoff_transport.py','validate',working],e); run([sys.executable,HERE/'handoff_transport.py','canonicalize',working,canonical],e); run([sys.executable,HERE/'handoff_transport.py','inline-pack',canonical,inline],e); run([sys.executable,HERE/'handoff_transport.py','inline-unpack',inline,unpack],e)
    rebuilt=unpack/'SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2.json'
    if canonical.read_bytes()!=rebuilt.read_bytes(): fail('INLINE_RECONSTRUCTION_NOT_BYTE_EQUAL')
    if len(states)>=2:
        cp=run([sys.executable,HERE/'batch_gate.py','collect',runroot/'snapshot.json',runroot/'neg-order',states[1],states[0],*states[2:]],e,check=False)
        if cp.returncode==0 or 'STATE_ORDER_MISMATCH' not in cp.stdout: fail('NEG_BATCH_REORDER_NOT_BLOCKED')
    count_states=states[:-1] if len(states)>=2 else [states[0],states[0]]
    cp=run([sys.executable,HERE/'batch_gate.py','collect',runroot/'snapshot.json',runroot/'neg-count',*count_states],e,check=False)
    if cp.returncode==0 or 'STATE_COUNT_MISMATCH' not in cp.stdout: fail('NEG_BATCH_COUNT_NOT_BLOCKED')
    bad=copy.deepcopy(payload); bad['articles'][0]['body']+='X'; badp=runroot/'bad-handoff.json'; writej(badp,bad); cp=run([sys.executable,HERE/'handoff_transport.py','validate',badp],e,check=False)
    if cp.returncode==0 or 'HANDOFF_BODY_SHA_MISMATCH' not in cp.stdout: fail('NEG_HANDOFF_TAMPER_NOT_BLOCKED')
    proof={'status':'REMOTE_PASS_PENDING_WORDPRESS_AND_CHAT_DELIVERY','head':meta['head'],'manifest':meta['manifest'],'article_count':len(payload['articles']),'pre_point0_article_body_count':meta['pre_point0_article_body_count'],'chat_start_receipt_sha256':meta['chat_start_receipt_sha256'],'batch_sha256':payload['batch_sha256'],'batch_evidence_sha256':bout['batch_evidence_sha256'],'handoff_sha256':hashlib.sha256(canonical.read_bytes()).hexdigest(),'handoff_bytes':len(canonical.read_bytes()),'inline_byte_equal':True,'codex_worker_start_verified':True,'codex_worker_start_count':len(state_values),'revisions':[s['revision'] for s in state_values],'lt':[s['checks']['production_evidence']['evidence']['languagetool']['status'] for s in state_values],'ppm':[s['checks']['production_evidence']['evidence']['ppm679']['status'] for s in state_values],**freshness}; writej(runroot/'LIVE_PARITY_V2_PROOF.json',proof)
    out=os.environ.get('SYSTEM4_LIVE_PARITY_PROOF','').strip()
    if out: writej(Path(out),proof)
    export=os.environ.get('SYSTEM4_LIVE_PARITY_OUTPUT_DIR','').strip()
    if export:
        target=Path(export); target.mkdir(parents=True,exist_ok=True); shutil.copyfile(canonical,target/canonical.name); shutil.copyfile(runroot/'LIVE_PARITY_V2_PROOF.json',target/f'LIVE_PARITY_V2_{len(items)}_PROOF.json')
    return proof

def main(argv:list[str])->int:
    cmd=argv[1] if len(argv)>1 else 'all'
    if cmd=='prepare':
        if len(argv)!=3: fail('USAGE: prepare <runroot>')
        print(json.dumps(prepare(Path(argv[2])),ensure_ascii=False)); return 0
    if cmd=='item':
        if len(argv)!=4: fail('USAGE: item <runroot> <index>')
        result=item(Path(argv[2]),int(argv[3])); print(json.dumps(result,ensure_ascii=False)); return 4 if result.get('status')=='PARENT_RETURN_REQUIRED' else 0
    if cmd=='finalize':
        if len(argv)!=3: fail('USAGE: finalize <runroot>')
        print(json.dumps(finalize(Path(argv[2])),ensure_ascii=False)); return 0
    if cmd=='all':
        rr=Path(tempfile.mkdtemp(prefix='system4-live-parity-v2-all-')); prepare(rr)
        for i in range(load(rr/'run_meta.json')['article_count']):
            result=item(rr,i)
            if result.get('status')=='PARENT_RETURN_REQUIRED':
                print(json.dumps(result,ensure_ascii=False,sort_keys=True))
                return 4
        print(json.dumps(finalize(rr),ensure_ascii=False,sort_keys=True)); return 0
    fail('BAD_COMMAND')
if __name__=='__main__': raise SystemExit(main(sys.argv))
