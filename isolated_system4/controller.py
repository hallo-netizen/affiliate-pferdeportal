from __future__ import annotations
import json, subprocess, sys
from pathlib import Path

from controller_core import *  # noqa: F401,F403
import controller_core as core
import production_binding
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

def main(argv:list[str])->int:
    try:
        _verify_core()
        if len(argv)<2: raise SupervisedControllerFail('BAD_COMMAND')
        if argv[1]=='ingress': return _guarded_ingress(argv)
        if argv[1]=='research': return _guarded_research(argv)
        if argv[1]=='context': return _guarded_context(argv)
        if len(argv)>=3:
            supervisor.verify_controller_binding(Path(argv[2]))
        return core.main(argv)
    except (SupervisedControllerFail, supervisor.SupervisorError, production_binding.ProductionBindingError, json.JSONDecodeError, OSError, ValueError) as exc:
        print('SYSTEM4_FAIL:'+str(exc)); return 2

if __name__=='__main__': raise SystemExit(main(sys.argv))
