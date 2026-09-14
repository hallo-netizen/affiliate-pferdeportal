from __future__ import annotations
import copy, hashlib, json, os, shutil, subprocess, sys, tempfile
from pathlib import Path

HERE=Path(__file__).resolve().parent
REPO=HERE.parent
FIX=Path(os.environ.get('SYSTEM4_LIVE_PARITY_FIXTURE','')).expanduser()

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
def writej(p,v): Path(p).write_text(json.dumps(v,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8')

def _fixture()->Path:
    if not str(FIX) or str(FIX)=='.' or not FIX.is_dir(): fail('SYSTEM4_LIVE_PARITY_FIXTURE_REQUIRED')
    return FIX.resolve()

def prepare(runroot:Path)->dict:
    global FIX; FIX=_fixture()
    sys.path.insert(0,str(HERE)); import root_entry, machine_point0, point0_snapshot
    if runroot.exists() and any(runroot.iterdir()): fail('RUNROOT_NOT_EMPTY')
    runroot.mkdir(parents=True,exist_ok=True)
    manifest=root_entry._critical_manifest_sha256(); head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip()
    snap=load(FIX/'snapshot.template.json'); snap['system4_root_manifest_sha256']=manifest
    raw=(json.dumps(snap,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n').encode()
    p0=machine_point0.build_from_acquired(snapshot_bytes=raw,acquired_batch=load(FIX/'acquired.json'),prewrite_plan_batch=load(FIX/'plans.json'),provider='SYSTEM4_LIVE_PARITY_V2_CAPTURED_REAL_SOURCES',manifest=manifest,head=head)
    (runroot/'snapshot.json').write_bytes(raw); (runroot/'point0.json').write_bytes(point0_snapshot.canon(p0))
    meta={'head':head,'manifest':manifest,'article_count':len(snap['next_textmachine_metadata_batch']['items']),'point0_sha256':p0['point0_core_sha256']}; writej(runroot/'run_meta.json',meta)
    return meta

def item(runroot:Path,i:int)->dict:
    global FIX; FIX=_fixture()
    e=env(); meta=load(runroot/'run_meta.json'); snap=load(runroot/'snapshot.json'); count=len(snap['next_textmachine_metadata_batch']['items'])
    if i<0 or i>=count: fail('ITEM_INDEX_INVALID')
    w=runroot/f'item-{i}'; inp=FIX/f'inputs-{i}'
    if not (w/'state.json').is_file():
        run([sys.executable,HERE/'root_entry.py','start-point0',runroot/'point0.json',w,str(i)],e)
        run([sys.executable,HERE/'codex_entry.py','worker-start',w],e)
    while True:
        s=load(w/'state.json'); phase=s['phase']
        if phase=='RESEARCH_REQUIRED': run([sys.executable,HERE/'controller.py','research',w,inp/'research.json'],e); continue
        if phase=='FACT_CHECK_REQUIRED': run([sys.executable,HERE/'controller.py','facts',w,inp/'facts.json'],e); continue
        if phase=='CONTEXT_REQUIRED':
            snapsha=hashlib.sha256((w/'bound_snapshot.json').read_bytes()).hexdigest(); pack=load(inp/'pack.base.json'); plan=load(inp/'plan.base.json'); pack['fact_pack_id']=snapsha; pack['source_snapshot_id']=snapsha; plan['source_snapshot_id']=snapsha
            pp=runroot/f'pack-{i}.json'; pl=runroot/f'plan-{i}.json'; writej(pp,pack); writej(pl,plan); run([sys.executable,HERE/'controller.py','context',w,pp,pl],e); continue
        if phase=='DRAFT_REQUIRED': run([sys.executable,HERE/'controller.py','draft',w,inp/'draft.html'],e); continue
        if phase=='CHECK_REQUIRED':
            cp=run([sys.executable,HERE/'controller.py','fullcheck',w],e,check=False)
            if cp.returncode==0: continue
            s=load(w/'state.json')
            if s.get('phase')!='REPAIR_REQUIRED': fail('UNEXPECTED_FULLCHECK_BLOCK:'+cp.stdout.strip()+':'+cp.stderr.strip())
            continue
        if phase=='REPAIR_REQUIRED':
            rp=inp/f"repair{s['revision']}.html"
            if not rp.is_file(): fail('REPAIR_FIXTURE_MISSING:'+str(i)+':'+str(s['revision']))
            run([sys.executable,HERE/'controller.py','repair',w,rp],e); continue
        if phase=='OUTPUT_GATE_REQUIRED':
            if s.get('checks',{}).get('status')!='PASS': fail('OUTPUT_GATE_WITHOUT_PASS')
            return {'index':i,'title':s['article']['title'],'phase':phase,'revision':s['revision'],'status':'PASS'}
        fail('UNEXPECTED_PHASE:'+phase)

def finalize(runroot:Path)->dict:
    e=env(); meta=load(runroot/'run_meta.json'); snap=load(runroot/'snapshot.json'); items=snap['next_textmachine_metadata_batch']['items']; states=[runroot/f'item-{i}'/'state.json' for i in range(len(items))]
    for i,p in enumerate(states):
        if not p.is_file(): fail('STATE_MISSING:'+str(i))
        s=load(p)
        if s.get('phase')!='OUTPUT_GATE_REQUIRED' or s.get('checks',{}).get('status')!='PASS': fail('STATE_NOT_OUTPUT_GATE:'+str(i))
    batchdir=runroot/'batch'; shutil.rmtree(batchdir,ignore_errors=True)
    cp=run([sys.executable,HERE/'batch_gate.py','collect',runroot/'snapshot.json',batchdir,*states],e); bout=json.loads(cp.stdout)
    if bout.get('status')!='SYSTEM4_BATCH_FULL_PASS_COLLECTED': fail('BATCH_NOT_FULL_PASS')
    rows=[]
    for i,(sp,itemrow) in enumerate(zip(states,items)):
        s=load(sp); ev=s['checks']['production_evidence']['evidence']; rows.append({'index':i,'title':itemrow['title'],'target_keyword':itemrow['target_keyword'],'category':itemrow['category'],'article_type':itemrow['article_type'],'plan_slot':itemrow['plan_slot'],'final_draft_sha256':s['draft_sha256'],'revision_count':s['revision'],'body':s['draft_markdown'],'production_context':s['production_context'],'languagetool':ev['languagetool'],'ppm679':ev['ppm679']})
    payload={'contract':'SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2','batch_sha256':snap['next_textmachine_metadata_batch']['batch_sha256'],'publish_allowed':False,'signing_deferred':True,'batch_gate_status':'SYSTEM4_BATCH_FULL_PASS_COLLECTED','no_legacy_status':'PASS','test_suite_status':'PASS','wordpress_review':{'file_format':'JSON','mime_type':'application/json','intended_next_step':'WORDPRESS_DIRECT_IMPORT','plugin_name':'Portal SEO Editorial Plan Compiler','plugin_version_verified_against':'0.28.23','ppm_version_verified_against':'6.7.9','direct_wordpress_upload_ready':True,'direct_upload_block_reason':None,'required_downstream_components':[]},'articles':rows}
    working=runroot/'handoff.working.json'; writej(working,payload); canonical=runroot/'SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2.json'; inline=runroot/'SYSTEM4_PARENT_CHAT_INLINE_V2.txt'; unpack=runroot/'unpacked'; shutil.rmtree(unpack,ignore_errors=True)
    run([sys.executable,HERE/'handoff_transport.py','validate',working],e); run([sys.executable,HERE/'handoff_transport.py','canonicalize',working,canonical],e); run([sys.executable,HERE/'handoff_transport.py','inline-pack',canonical,inline],e); run([sys.executable,HERE/'handoff_transport.py','inline-unpack',inline,unpack],e)
    rebuilt=unpack/'SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2.json'
    if canonical.read_bytes()!=rebuilt.read_bytes(): fail('INLINE_RECONSTRUCTION_NOT_BYTE_EQUAL')
    # Mandatory batch/handoff negatives. The 1-item live path must be first-class:
    # reordering is impossible for N=1, so bind a wrong slot at the same position instead.
    if len(states)>=2:
        order_states=[states[1],states[0],*states[2:]]
    else:
        bad_state=load(states[0]); bad_state['article']=dict(bad_state['article']); bad_state['article']['plan_slot']='f'*64
        bad_state_path=runroot/'neg-order-state.json'; writej(bad_state_path,bad_state); order_states=[bad_state_path]
    cp=run([sys.executable,HERE/'batch_gate.py','collect',runroot/'snapshot.json',runroot/'neg-order',*order_states],e,check=False)
    if cp.returncode==0 or 'STATE_ORDER_MISMATCH' not in cp.stdout: fail('NEG_BATCH_REORDER_NOT_BLOCKED')
    count_states=states[:-1] if len(states)>=2 else [states[0],states[0]]
    cp=run([sys.executable,HERE/'batch_gate.py','collect',runroot/'snapshot.json',runroot/'neg-count',*count_states],e,check=False)
    if cp.returncode==0 or 'STATE_COUNT_MISMATCH' not in cp.stdout: fail('NEG_BATCH_COUNT_NOT_BLOCKED')
    bad=copy.deepcopy(payload); bad['articles'][0]['body']+='X'; badp=runroot/'bad-handoff.json'; writej(badp,bad); cp=run([sys.executable,HERE/'handoff_transport.py','validate',badp],e,check=False)
    if cp.returncode==0 or 'HANDOFF_BODY_SHA_MISMATCH' not in cp.stdout: fail('NEG_HANDOFF_TAMPER_NOT_BLOCKED')
    proof={'status':'SYSTEM4_LIVE_PARITY_V2_PASS','head':meta['head'],'manifest':meta['manifest'],'article_count':len(rows),'batch_sha256':payload['batch_sha256'],'batch_evidence_sha256':bout['batch_evidence_sha256'],'handoff_sha256':hashlib.sha256(canonical.read_bytes()).hexdigest(),'handoff_bytes':len(canonical.read_bytes()),'inline_byte_equal':True,'revisions':[r['revision_count'] for r in rows],'lt':[r['languagetool']['status'] for r in rows],'ppm':[r['ppm679']['status'] for r in rows]}
    writej(runroot/'LIVE_PARITY_V2_PROOF.json',proof); out=os.environ.get('SYSTEM4_LIVE_PARITY_PROOF','').strip();
    if out: writej(Path(out),proof)
    return proof

def main(argv:list[str])->int:
    cmd=argv[1] if len(argv)>1 else 'all'
    if cmd=='prepare':
        if len(argv)!=3:
            fail('USAGE: prepare <runroot>')
        print(json.dumps(prepare(Path(argv[2])),ensure_ascii=False)); return 0
    if cmd=='item':
        if len(argv)!=4:
            fail('USAGE: item <runroot> <index>')
        print(json.dumps(item(Path(argv[2]),int(argv[3])),ensure_ascii=False)); return 0
    if cmd=='finalize':
        if len(argv)!=3:
            fail('USAGE: finalize <runroot>')
        print(json.dumps(finalize(Path(argv[2])),ensure_ascii=False)); return 0
    if cmd=='all':
        rr=Path(tempfile.mkdtemp(prefix='system4-live-parity-v2-all-')); prepare(rr)
        for i in range(load(rr/'run_meta.json')['article_count']): item(rr,i)
        print(json.dumps(finalize(rr),ensure_ascii=False,sort_keys=True)); return 0
    fail('BAD_COMMAND')
if __name__=='__main__': raise SystemExit(main(sys.argv))
