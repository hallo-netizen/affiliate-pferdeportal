from __future__ import annotations

import json
import os
import pwd
import secrets
import selectors
import shutil
import subprocess
import sys
import tempfile
import threading
from pathlib import Path
from typing import Any, Mapping, Sequence

from full_chain import FullChainSupervisor
from production_ingress import bind_external_snapshot
from authority_store import SupervisorAuthorityStore
from persistent_full_chain import PersistentProductionFullChainSupervisor
from managed_agent_worker import ManagedAgentWorkerPool

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
BOUNDARY_CONTRACT = "SYSTEM4A_EXTERNAL_WORKER_SESSION_V2"
FORBIDDEN_WORKER_FILES = {"state.json", "authority.key", "AGENTS.md", ".git"}
FORBIDDEN_REQUEST_KEYS = {"phase", "controller_seal", "authority_key", "publish_allowed", "checks", "production_evidence"}
ALLOWED_TASKS = {"research", "facts", "context", "draft", "repair"}

class ExternalHostError(RuntimeError): pass

def _require(condition: bool, code: str) -> None:
    if not condition: raise ExternalHostError(code)

def _within(child: Path, parent: Path) -> bool:
    child=child.resolve(); parent=parent.resolve(); return child==parent or parent in child.parents

def _assert_no_authority_files(root: Path) -> None:
    if not root.exists(): return
    for path in root.rglob('*'):
        if path.name in FORBIDDEN_WORKER_FILES:
            raise ExternalHostError('WORKER_AUTHORITY_FILE_FORBIDDEN:'+path.name)

class PersistentArticleWorkerPool:
    """One logical worker/agent session per article over a bounded OS runtime pool."""
    boundary_contract=BOUNDARY_CONTRACT
    def __init__(self, command: Sequence[str], work_root: Path, *, run_as_user: str|None=None,
                 timeout_seconds: float=120.0, require_cross_uid: bool=False,
                 runtime_processes: int=2) -> None:
        _require(isinstance(command,Sequence) and command and all(isinstance(x,str) and x for x in command),'WORKER_COMMAND_INVALID')
        _require(isinstance(runtime_processes,int) and runtime_processes>=1,'WORKER_RUNTIME_LIMIT_INVALID')
        self._command=tuple(command); self._work_root=Path(work_root).resolve()
        _require(not _within(self._work_root,REPO),'WORKER_ROOT_MUST_BE_OUTSIDE_REPOSITORY')
        _require(timeout_seconds>0,'WORKER_TIMEOUT_INVALID')
        self._timeout=float(timeout_seconds); self._runtime_limit=runtime_processes; self._run_as_user=run_as_user
        self._worker_uid=None
        if run_as_user is not None:
            try: self._worker_uid=pwd.getpwnam(run_as_user).pw_uid
            except KeyError as exc: raise ExternalHostError('WORKER_USER_NOT_FOUND') from exc
        if require_cross_uid:
            _require(self._worker_uid is not None,'CROSS_UID_WORKER_USER_REQUIRED')
            _require(os.geteuid()!=self._worker_uid,'WORKER_UID_MUST_DIFFER_FROM_SUPERVISOR')
        self._work_root.mkdir(parents=True,exist_ok=True); _assert_no_authority_files(self._work_root)
        self._runtimes: list[subprocess.Popen[str]]=[]; self._runtime_locks: list[threading.Lock]=[]
        self._runtime_stderr: list[Any]=[]
        self._owned_staging_root: Path|None=None
        self._session_ids: dict[str,str]={}; self._runtime_by_slot: dict[str,int]={}; self._cross_uid_bound=bool(require_cross_uid); self._closed=False

    @classmethod
    def from_python_bundle(cls, source_dir: Path, entrypoint: str, *, run_as_user: str='nobody',
                           timeout_seconds: float=120.0, runtime_processes: int=2,
                           runtime_parent: Path|None=None) -> 'PersistentArticleWorkerPool':
        source_dir=Path(source_dir).resolve()
        _require(source_dir.is_dir(),'WORKER_BUNDLE_SOURCE_MISSING')
        _require(isinstance(entrypoint,str) and entrypoint and '/' not in entrypoint and '\\' not in entrypoint,
                 'WORKER_BUNDLE_ENTRYPOINT_INVALID')
        for path in source_dir.rglob('*'):
            _require(not path.is_symlink(),'WORKER_BUNDLE_SYMLINK_FORBIDDEN:'+path.name)
            _require(path.name not in FORBIDDEN_WORKER_FILES,'WORKER_AUTHORITY_FILE_FORBIDDEN:'+path.name)
        parent=Path(runtime_parent if runtime_parent is not None else tempfile.gettempdir()).resolve()
        _require(parent.is_dir(),'WORKER_RUNTIME_PARENT_MISSING')
        _require(not _within(parent,REPO),'WORKER_RUNTIME_PARENT_INSIDE_REPOSITORY')
        staging=Path(tempfile.mkdtemp(prefix='system4a-worker-stage-',dir=parent)).resolve()
        os.chmod(staging,0o755)
        bundle=staging/'bundle'
        shutil.copytree(source_dir,bundle,symlinks=False)
        for path in bundle.rglob('*'):
            if path.is_dir(): os.chmod(path,0o755)
            elif path.is_file(): os.chmod(path,0o644)
        os.chmod(bundle,0o755)
        entry=bundle/entrypoint
        _require(entry.is_file(),'WORKER_BUNDLE_ENTRYPOINT_MISSING')
        pool=cls([sys.executable,str(entry)],staging/'runtimes',run_as_user=run_as_user,
                 require_cross_uid=True,runtime_processes=runtime_processes,timeout_seconds=timeout_seconds)
        pool._owned_staging_root=staging
        return pool

    @staticmethod
    def _validate_request(request: Mapping[str,Any]) -> str:
        _require(isinstance(request,Mapping),'WORKER_REQUEST_INVALID')
        _require(not(set(request)&FORBIDDEN_REQUEST_KEYS),'WORKER_REQUEST_CONTAINS_AUTHORITY_FIELD')
        _require(request.get('task') in ALLOWED_TASKS,'WORKER_TASK_INVALID')
        article=request.get('article'); _require(isinstance(article,Mapping),'WORKER_ARTICLE_MISSING')
        slot=article.get('plan_slot'); _require(isinstance(slot,str) and len(slot)==64,'WORKER_PLAN_SLOT_INVALID')
        return slot

    def _runtime_workspace(self,index:int)->Path:
        workspace=self._work_root/f'runtime-{index}'
        if not workspace.exists():
            workspace.mkdir(mode=0o700)
            if self._worker_uid is not None and os.geteuid()==0:
                os.chown(workspace,self._worker_uid,self._worker_uid); os.chmod(workspace,0o700)
        _assert_no_authority_files(workspace); return workspace

    def _minimal_env(self,workspace:Path)->dict[str,str]:
        return {'PATH':os.environ.get('PATH','/usr/bin:/bin'),'HOME':str(workspace),'LANG':os.environ.get('LANG','C.UTF-8'),
                'PYTHONUNBUFFERED':'1','SYSTEM4A_WORKER_BOUNDARY':BOUNDARY_CONTRACT}

    @staticmethod
    def _stop_process(proc:subprocess.Popen[str])->None:
        if proc.poll() is None: proc.terminate()
        if proc.poll() is None:
            try: proc.wait(timeout=2)
            except subprocess.TimeoutExpired: proc.kill(); proc.wait(timeout=2)
        for stream in (proc.stdin,proc.stdout):
            if stream is not None:
                try: stream.close()
                except Exception: pass

    def _cross_uid_path_preflight(self, workspace: Path) -> None:
        if self._run_as_user is None:
            return
        _require(shutil.which('runuser') is not None,'RUNUSER_UNAVAILABLE')
        probes=[('-x',workspace)]
        for position,token in enumerate(self._command):
            candidate=Path(token)
            if candidate.is_absolute() and candidate.exists():
                probes.append(('-x' if position==0 else '-r',candidate))
        for flag,path in probes:
            rc=subprocess.run(['runuser','-u',self._run_as_user,'--','test',flag,str(path)],
                              stdin=subprocess.DEVNULL,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode
            _require(rc==0,'WORKER_COMMAND_PATH_NOT_ACCESSIBLE:'+str(path))

    def _spawn_runtime(self,index:int)->subprocess.Popen[str]:
        workspace=self._runtime_workspace(index); command=list(self._command)
        self._cross_uid_path_preflight(workspace)
        if self._run_as_user is not None:
            command=['runuser','-u',self._run_as_user,'--']+command
        stderr_file=tempfile.TemporaryFile(mode='w+t',encoding='utf-8')
        proc=subprocess.Popen(command,cwd=workspace,env=self._minimal_env(workspace),stdin=subprocess.PIPE,stdout=subprocess.PIPE,
                              stderr=stderr_file,text=True,bufsize=1)
        _require(proc.stdin is not None and proc.stdout is not None,'WORKER_PIPE_MISSING')
        self._runtimes.append(proc); self._runtime_locks.append(threading.Lock()); self._runtime_stderr.append(stderr_file); return proc

    def _ensure_runtime(self,index:int)->subprocess.Popen[str]:
        while len(self._runtimes)<=index: self._spawn_runtime(len(self._runtimes))
        proc=self._runtimes[index]; _require(proc.poll() is None,'WORKER_PROCESS_NOT_RUNNING'); return proc

    def _binding(self,slot:str)->tuple[str,int]:
        if slot not in self._session_ids:
            self._session_ids[slot]=secrets.token_hex(16)
            self._runtime_by_slot[slot]=len(self._session_ids)-1
            self._runtime_by_slot[slot]%=self._runtime_limit
        return self._session_ids[slot],self._runtime_by_slot[slot]

    def _stderr_excerpt(self,index:int)->str:
        if index>=len(self._runtime_stderr):
            return ''
        handle=self._runtime_stderr[index]
        try:
            handle.flush(); handle.seek(0); text=handle.read(4096)
        except Exception:
            return ''
        return ' '.join(text.strip().split())[:1000]

    def _readline(self,proc:subprocess.Popen[str],index:int)->str:
        _require(proc.stdout is not None,'WORKER_STDOUT_MISSING')
        selector=selectors.DefaultSelector()
        try:
            selector.register(proc.stdout,selectors.EVENT_READ); events=selector.select(self._timeout)
            _require(bool(events),'WORKER_RESPONSE_TIMEOUT'); line=proc.stdout.readline()
        finally: selector.close()
        if line=='':
            try: rc=proc.wait(timeout=0.2)
            except subprocess.TimeoutExpired: rc=proc.poll()
            detail=self._stderr_excerpt(index)
            suffix=':RC='+str(rc) if rc is not None else ':RC=UNKNOWN'
            if detail: suffix+=':STDERR='+detail
            raise ExternalHostError('WORKER_EXITED_WITHOUT_RESPONSE'+suffix)
        return line.rstrip('\n')

    def request(self,request:Mapping[str,Any])->dict[str,str]:
        _require(not self._closed,'WORKER_POOL_CLOSED'); slot=self._validate_request(request); session_id,index=self._binding(slot)
        proc=self._ensure_runtime(index); workspace=self._runtime_workspace(index)
        envelope={'contract':BOUNDARY_CONTRACT,'session_id':session_id,'request':dict(request)}
        with self._runtime_locks[index]:
            assert proc.stdin is not None
            proc.stdin.write(json.dumps(envelope,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n'); proc.stdin.flush()
            line=self._readline(proc,index)
        _assert_no_authority_files(workspace)
        try: response=json.loads(line)
        except Exception as exc: raise ExternalHostError('WORKER_RESPONSE_JSON_INVALID') from exc
        _require(isinstance(response,dict) and set(response)=={'contract','session_id','result'},'WORKER_RESPONSE_SCHEMA_INVALID')
        _require(response.get('contract')==BOUNDARY_CONTRACT,'WORKER_RESPONSE_CONTRACT_INVALID')
        _require(response.get('session_id')==session_id,'WORKER_SESSION_BINDING_MISMATCH')
        result=response.get('result'); _require(isinstance(result,dict) and set(result)=={'content'},'WORKER_RESULT_SCHEMA_INVALID')
        content=result.get('content'); _require(isinstance(content,str) and content.strip(),'WORKER_RESPONSE_CONTENT_EMPTY')
        return {'content':content}

    def session_bindings(self)->dict[str,dict[str,Any]]:
        return {slot:{'session_id':sid,'runtime_pid':self._runtimes[self._runtime_by_slot[slot]].pid if self._runtime_by_slot[slot]<len(self._runtimes) else None}
                for slot,sid in self._session_ids.items()}
    def runtime_pids(self)->list[int]: return [p.pid for p in self._runtimes]
    def max_runtime_processes(self)->int: return self._runtime_limit
    def cross_uid_bound(self)->bool: return self._cross_uid_bound
    def close(self)->None:
        if self._closed:return
        self._closed=True
        for proc in self._runtimes:self._stop_process(proc)
        for handle in self._runtime_stderr:
            try: handle.close()
            except Exception: pass
        self._runtimes.clear(); self._runtime_locks.clear(); self._runtime_stderr.clear()
        if self._owned_staging_root is not None:
            try: shutil.rmtree(self._owned_staging_root)
            except FileNotFoundError: pass
            self._owned_staging_root=None
    def __enter__(self):return self
    def __exit__(self,exc_type,exc,tb):self.close()


def _architecture_worker(pool: Any) -> str:
    if type(pool) is PersistentArticleWorkerPool:
        return 'PROCESS_WORKER'
    if type(pool) is ManagedAgentWorkerPool:
        _require(pool.authority_isolated(),'MANAGED_AGENT_AUTHORITY_BOUNDARY_INVALID')
        return 'MANAGED_AGENT_WORKER'
    raise ExternalHostError('EXTERNAL_WORKER_POOL_REQUIRED')


def _production_worker_boundary(pool: Any) -> str:
    if type(pool) is PersistentArticleWorkerPool:
        _require(pool.cross_uid_bound(),'PRODUCTION_CROSS_UID_BOUNDARY_REQUIRED')
        return 'CROSS_UID_PROCESS'
    if type(pool) is ManagedAgentWorkerPool:
        _require(pool.authority_isolated(),'PRODUCTION_MANAGED_AGENT_AUTHORITY_BOUNDARY_REQUIRED')
        _require(pool.production_boundary_configured(),'PRODUCTION_MANAGED_AGENT_OFFICIAL_BOUNDARY_REQUIRED')
        return 'REPO_LESS_MANAGED_AGENT'
    raise ExternalHostError('EXTERNAL_WORKER_POOL_REQUIRED')


class ExternalSupervisorHost:
    def __init__(self,*,mode:str='test',checks:Any|None=None,authority_root:Path|None=None)->None:
        _require(mode in {'test','production'},'HOST_MODE_INVALID')
        if mode=='production':_require(checks is None,'HOST_PRODUCTION_CHECK_INJECTION_FORBIDDEN')
        self._mode=mode; self._supervisor=FullChainSupervisor(mode='test',checks=checks) if mode=='test' else None
        self._authority_root=Path(authority_root).resolve() if authority_root is not None else None
    def run_architecture(self,snapshot_path:Path,pool:Any,output_path:Path,parent_chat_dir:Path)->dict[str,Any]:
        _require(self._mode=='test','HOST_ARCHITECTURE_MODE_REQUIRED')
        boundary=_architecture_worker(pool)
        try:
            _require(self._supervisor is not None,'HOST_SUPERVISOR_MISSING')
            result=self._supervisor.run_full(Path(snapshot_path),pool.request,Path(output_path))
            roundtrip=self._supervisor.simulate_parent_chat_roundtrip(Path(result['parent_chat_inline']['path']),Path(parent_chat_dir))
            _require(roundtrip['sha256']==result['output']['sha256'],'PARENT_CHAT_ROUNDTRIP_SHA_MISMATCH')
            return {'status':'SYSTEM4A_EXTERNAL_HOST_ARCHITECTURE_PASS','article_count':result['article_count'],'output':result['output'],
                    'parent_chat':roundtrip,'worker_sessions':pool.session_bindings(),'runtime_pids':pool.runtime_pids(),
                    'runtime_limit':pool.max_runtime_processes(),'worker_boundary':boundary,'publish_allowed':False}
        finally:pool.close()
    def run_production(self,snapshot_path:Path,pool:Any,output_path:Path,parent_chat_dir:Path)->dict[str,Any]:
        _require(self._mode=='production','HOST_PRODUCTION_MODE_REQUIRED')
        boundary=_production_worker_boundary(pool)
        _require(self._authority_root is not None,'HOST_AUTHORITY_ROOT_REQUIRED')
        bound=bind_external_snapshot(Path(snapshot_path),self._authority_root)
        try:
            authority_store=SupervisorAuthorityStore(self._authority_root)
            supervisor=PersistentProductionFullChainSupervisor(authority_store)
            result=supervisor._run_external_production(bound.bound_snapshot_path,pool.request,Path(output_path))
            roundtrip=supervisor.simulate_parent_chat_roundtrip(Path(result['parent_chat_inline']['path']),Path(parent_chat_dir))
            _require(roundtrip['sha256']==result['output']['sha256'],'PARENT_CHAT_ROUNDTRIP_SHA_MISMATCH')
            return {'status':'SYSTEM4A_EXTERNAL_HOST_PRODUCTION_PASS','article_count':result['article_count'],'output':result['output'],
                    'parent_chat':roundtrip,'worker_sessions':pool.session_bindings(),'runtime_pids':pool.runtime_pids(),
                    'runtime_limit':pool.max_runtime_processes(),'worker_boundary':boundary,'publish_allowed':False,
                    'ingress':{'external_input_sha256':bound.external_input_sha256,'bound_snapshot_sha256':bound.bound_snapshot_sha256,
                               'system4_manifest_sha256':bound.system4_manifest_sha256},
                    'durable_supervisor_state':True}
        finally:pool.close()
