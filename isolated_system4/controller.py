from __future__ import annotations
import hashlib, json, subprocess, sys
from pathlib import Path

from controller_core import *  # noqa: F401,F403
import controller_core as core
import block_semantics
import global_workshop
import production_binding
import production_checks
import repair_router
import source_bound_lt_policy
import supervisor

HERE=Path(__file__).resolve().parent
REPO=HERE.parent
CORE=HERE/'controller_core.py'
CORE_GIT_BLOB='fe904b29f9d047fb1839c4169a3359d6e4bfc3f6'

class SupervisedControllerFail(RuntimeError): pass

def _require(ok:bool,code:str)->None:
    if not ok: raise SupervisedControllerFail(code)

def _git_blob(path:Path)->str:
    cp=subprocess.run(['git','hash-object',str(path)],cwd=REPO,text=True,capture_output=True,check=False)
    _require(cp.returncode==0,'CONTROLLER_CORE_IDENTITY_UNAVAILABLE')
    return cp.stdout.strip()

def _verify_core()->None:
    _require(CORE.is_file(),'CONTROLLER_CORE_MISSING')
    _require(_git_blob(CORE)==CORE_GIT_BLOB,'CONTROLLER_CORE_IDENTITY_MISMATCH')

source_bound_lt_policy.install(production_checks)

_ORIGINAL_RUN_ALL=production_checks.run_all

def _run_all_with_validator_routing(*args,**kwargs):
    try:
        return _ORIGINAL_RUN_ALL(*args,**kwargs)
    except production_checks.ProductionCheckError as exc:
        message=str(exc)
        prefix='PPM679_VALIDATOR_BLOCKED:'
        if not message.startswith(prefix):
            raise
        code=message[len(prefix):].strip() or 'PPM679_BLOCKED'
        finding={
            'error_code':code,
            'failed_rule':None,
            'field':None,
            'field_path':None,
            'expected':None,
            'actual':None,
            'reason':'AUTHORITATIVE_CONTENT_VALIDATOR_REJECTION_WITHOUT_STRUCTURED_FIELD',
            'validator_id':'PPM679_Content_Validator',
        }
        raise production_checks.RepairRequired('ppm679',[finding]) from exc

production_checks.run_all=_run_all_with_validator_routing

def _guarded_ingress(argv:list[str])->int:
    _require(len(argv)>=4,'BAD_INGRESS_ARGS')
    workspace=Path(argv[3])
    state_path=workspace/'state.json'
    try:
        core.cmd_ingress(argv[2],argv[3],int(argv[4]) if len(argv)>4 else 0)
        supervisor.verify_controller_binding(workspace)
    except Exception:
        try: state_path.unlink()
        except FileNotFoundError: pass
        raise
    print('SYSTEM4_SUPERVISOR_INGRESS_BINDING_PASS')
    return 0

def _guarded_research(argv:list[str])->int:
    _require(len(argv)==4,'BAD_RESEARCH_ARGS')
    workspace=Path(argv[2]); research_path=Path(argv[3])
    submitted=json.loads(research_path.read_text(encoding='utf-8'))
    supervisor.verify_controller_binding(workspace)
    supervisor.validate_research_submission(workspace,submitted)
    core.cmd_research(argv[2],argv[3])
    print('SYSTEM4_BOUND_RESEARCH_POOL_PASS')
    return 0

def _return_claim_count_to_facts(workspace:Path,bound_path:Path,exc:Exception)->int:
    message=str(exc)
    if message!='AUTHORING_CONTRACT_FAIL:FACT_PACK_CLAIM_COUNT_INVALID':
        raise exc
    state,state_path=core.load(workspace)
    _require(state.get('phase')=='CONTEXT_REQUIRED','FACTS_RETURN_PHASE_MISMATCH')
    immutable_before=state.get('immutable_core_sha256')
    article_before=json.loads(json.dumps(state.get('article'),ensure_ascii=False))
    research_before=json.loads(json.dumps(state.get('research'),ensure_ascii=False))
    state['facts']=None
    state['production_context']=None
    state['authoring_contract']=None
    state['draft_markdown']=None
    state['draft_sha256']=None
    state['checks']={}
    state['last_error']=None
    state['release_prepared']=None
    state['released']=False
    state['phase']='FACT_CHECK_REQUIRED'
    core.save(state,state_path)
    _require(state.get('immutable_core_sha256')==immutable_before,'FACTS_RETURN_IMMUTABLE_CORE_MUTATION')
    _require(state.get('article')==article_before,'FACTS_RETURN_ARTICLE_MUTATION')
    _require(state.get('research')==research_before,'FACTS_RETURN_RESEARCH_MUTATION')
    bound_path.unlink(missing_ok=True)
    print('SYSTEM4_STAGE_OWNER_RETURN:FACTS_WORKER:FACTS_STAGE:'+message+':CONTINUATION_REQUIRED')
    return 4

def _guarded_context(argv:list[str])->int:
    _require(len(argv)==5,'BAD_CONTEXT_ARGS')
    workspace=Path(argv[2]); fact_path=Path(argv[3]); plan_path=Path(argv[4])
    supervisor.verify_controller_binding(workspace)
    state,_=core.load(workspace)
    _require(state.get('phase')=='CONTEXT_REQUIRED','PHASE_FAIL:CONTEXT')
    fact=json.loads(fact_path.read_text(encoding='utf-8'))
    incoming=json.loads(plan_path.read_text(encoding='utf-8'))
    bound=production_binding.bind_plan(REPO,state,fact,incoming)
    bound_path=workspace/'MACHINE_PRODUCTION_BINDING.json'
    tmp=workspace/'.MACHINE_PRODUCTION_BINDING.tmp'
    tmp.write_text(json.dumps(bound,ensure_ascii=False,indent=2,sort_keys=True),encoding='utf-8')
    tmp.replace(bound_path)
    try:
        core.cmd_context(argv[2],argv[3],str(bound_path))
    except core.Fail as exc:
        return _return_claim_count_to_facts(workspace,bound_path,exc)
    print('SYSTEM4_MACHINE_PRODUCTION_BINDING_PASS')
    return 0

def _record_semantic_draft_workshop(workspace:Path,text:str,exc:block_semantics.BlockSemanticRepairRequired)->int:
    state,state_path=core.load(workspace)
    _require(state.get('phase')=='DRAFT_REQUIRED','SEMANTIC_DRAFT_PHASE_MISMATCH')
    state['draft_markdown']=text
    state['draft_sha256']=hashlib.sha256(text.encode('utf-8')).hexdigest()
    state['revision']=int(state.get('revision') or 0)+1
    findings=[dict(row) for row in exc.findings]
    first=str(findings[0].get('error_code') or 'BLOCK_CONTENT_SEMANTIC_REPAIR_REQUIRED') if findings else 'BLOCK_CONTENT_SEMANTIC_REPAIR_REQUIRED'
    state['checks']={
        'status':'FAIL','mode':'GLOBAL_WORKSHOP','errors':['FULL:block_semantics:'+first],
        'findings':findings,'checker':'block_semantics','checked_draft_sha256':state['draft_sha256'],
    }
    state['last_error']='FULL:block_semantics:'+first
    state['phase']='REPAIR_REQUIRED'
    core.save(state,state_path)
    request,path,_=global_workshop.capture(
        'DRAFT_BLOCK_SEMANTICS',
        exc,
        output_dir=workspace,
        findings=findings,
        context={'workspace':str(workspace),'checker':'block_semantics'},
    )
    _require(request.get('repairable') is True,'SEMANTIC_DRAFT_WORKSHOP_MUST_BE_REPAIRABLE')
    result=repair_router.route(workspace)
    repair_router.verify_continuation_result(workspace,result)
    _require(result.get('status')=='SAME_ARTICLE_BODY_REPAIR','SEMANTIC_DRAFT_REPAIR_ROUTE_INVALID')
    print('SYSTEM4_WORKSHOP_REQUIRED:'+str(path)+':BLOCK_SEMANTICS:DRAFT_BODY:SAME_ARTICLE_BODY_REPAIR')
    return 3

def _guarded_draft(argv:list[str])->int:
    _require(len(argv)==4,'BAD_DRAFT_ARGS')
    workspace=Path(argv[2]); draft_path=Path(argv[3])
    state,_=core.load(workspace)
    if state.get('phase')!='DRAFT_REQUIRED':
        return core.main(argv)
    text=draft_path.read_text(encoding='utf-8').strip()
    if not text:
        return core.main(argv)
    contract=state.get('authoring_contract') if isinstance(state.get('authoring_contract'),dict) else {}
    try:
        block_semantics.validate(text,contract)
    except block_semantics.BlockSemanticRepairRequired as exc:
        return _record_semantic_draft_workshop(workspace,text,exc)
    return core.main(argv)

def _route_repair_after_fullcheck(workspace:Path,rc:int)->int:
    if rc!=3:
        return rc
    result=repair_router.route(workspace)
    repair_router.verify_continuation_result(workspace,result)
    status=str(result.get('status') or '')
    if status=='SAME_ARTICLE_BODY_REPAIR':
        print('SYSTEM4_MACHINE_REPAIR_ROUTE:DRAFT_BODY:SAME_ARTICLE_BODY_REPAIR:CONTINUATION_REQUIRED')
        return 3
    if status=='RESTARTED':
        print('SYSTEM4_MACHINE_REPAIR_ROUTE:PARENT_METADATA:RESTARTED:'+str(result['workspace'])+':CONTINUATION_REQUIRED')
        return 4
    if status=='RETURN_TO_OWNER':
        print('SYSTEM4_MACHINE_REPAIR_ROUTE:'+str(result.get('owner'))+':'+str(result.get('target'))+':RETURN_TO_OWNER:CONTINUATION_REQUIRED')
        return 4
    raise SupervisedControllerFail('REPAIR_ROUTER_BAD_STATUS:'+status)

def _workshop_failure(argv:list[str],exc:BaseException)->int:
    workspace=None
    if len(argv)>=3:
        candidate=Path(argv[2])
        if candidate.is_dir():
            workspace=candidate
    request,path,_=global_workshop.capture(
        'CONTROLLER',
        exc,
        output_dir=workspace,
        findings=getattr(exc,'findings',None),
        context={'command':argv[1] if len(argv)>1 else None,'workspace':str(workspace) if workspace else None},
    )
    status='SYSTEM4_WORKSHOP_REQUIRED' if request.get('repairable') else 'SYSTEM4_WORKSHOP_BLOCKED'
    print(status+':'+(str(path) if path is not None else 'INLINE')+':'+str(exc))
    return 4 if request.get('repairable') else 2

def main(argv:list[str])->int:
    try:
        _verify_core()
        if len(argv)<2: raise SupervisedControllerFail('BAD_COMMAND')
        if argv[1]=='ingress': return _guarded_ingress(argv)
        if argv[1]=='research': return _guarded_research(argv)
        if argv[1]=='context': return _guarded_context(argv)
        if len(argv)>=3:
            supervisor.verify_controller_binding(Path(argv[2]))
        if argv[1]=='draft': return _guarded_draft(argv)
        rc=core.main(argv)
        if argv[1]=='fullcheck' and len(argv)==3:
            return _route_repair_after_fullcheck(Path(argv[2]),rc)
        return rc
    except (
        SupervisedControllerFail,
        supervisor.SupervisorError,
        production_binding.ProductionBindingError,
        repair_router.RepairRouteError,
        json.JSONDecodeError,
        OSError,
        ValueError,
        core.Fail,
        production_checks.ProductionCheckError,
    ) as exc:
        return _workshop_failure(argv,exc)

if __name__=='__main__': raise SystemExit(main(sys.argv))
