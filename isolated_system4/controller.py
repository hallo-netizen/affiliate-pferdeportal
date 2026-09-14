from __future__ import annotations
import json, subprocess, sys
from pathlib import Path

from controller_core import *  # noqa: F401,F403
import controller_core as core
import production_binding
import production_checks
import repair_router
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

# Preserve the real production checker. The wrapper below changes only error
# classification, never validator execution or PASS authority.
_ORIGINAL_RUN_ALL=production_checks.run_all

def _run_all_with_validator_routing(*args,**kwargs):
    """Turn completed content-validator rejections into structured repair findings.

    A PPM679_VALIDATOR_BLOCKED result means the authoritative PPM validator ran
    successfully and rejected article content/metadata. That is a production
    validation finding, not an infrastructure/integrity failure. It therefore
    must enter the stage-aware repair router even when PPM omitted field_path.

    Execution, package, hash, result-schema and other technical failures remain
    ProductionCheckError and fail closed.
    """
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

# Bind classification centrally for every full production check.
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
    core.cmd_context(argv[2],argv[3],str(bound_path))
    print('SYSTEM4_MACHINE_PRODUCTION_BINDING_PASS')
    return 0

def _route_repair_after_fullcheck(workspace:Path,rc:int)->int:
    if rc!=3:
        return rc
    result=repair_router.route(workspace)
    status=str(result.get('status') or '')
    if status=='SAME_ARTICLE_BODY_REPAIR':
        print('SYSTEM4_MACHINE_REPAIR_ROUTE:DRAFT_BODY:SAME_ARTICLE_BODY_REPAIR')
        return 3
    if status=='RESTARTED':
        print('SYSTEM4_MACHINE_REPAIR_ROUTE:PARENT_METADATA:RESTARTED:'+str(result['workspace']))
        return 4
    if status=='RETURN_TO_OWNER':
        print('SYSTEM4_MACHINE_REPAIR_ROUTE:'+str(result.get('owner'))+':'+str(result.get('target'))+':RETURN_TO_OWNER')
        return 4
    raise SupervisedControllerFail('REPAIR_ROUTER_BAD_STATUS:'+status)

def main(argv:list[str])->int:
    try:
        _verify_core()
        if len(argv)<2: raise SupervisedControllerFail('BAD_COMMAND')
        if argv[1]=='ingress': return _guarded_ingress(argv)
        if argv[1]=='research': return _guarded_research(argv)
        if argv[1]=='context': return _guarded_context(argv)
        if len(argv)>=3:
            supervisor.verify_controller_binding(Path(argv[2]))
        rc=core.main(argv)
        if argv[1]=='fullcheck' and len(argv)==3:
            return _route_repair_after_fullcheck(Path(argv[2]),rc)
        return rc
    except (SupervisedControllerFail, supervisor.SupervisorError, production_binding.ProductionBindingError, repair_router.RepairRouteError, json.JSONDecodeError, OSError, ValueError) as exc:
        print('SYSTEM4_FAIL:'+str(exc)); return 2

if __name__=='__main__': raise SystemExit(main(sys.argv))
