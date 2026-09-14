from __future__ import annotations
import hashlib, json, subprocess, sys
from pathlib import Path

import root_supervisor_bridge, worker_dispatch

SYSTEM4_ROOT_CONTRACT='SYSTEM4_ISOLATED_ROOT_ENTRY_V4_POINT0_ONLY'
HERE=Path(__file__).resolve().parent
REPO=HERE.parent
CONTROLLER=HERE/'controller.py'
ROOT_AGENTS=REPO/'AGENTS.md'
ROOT_OVERRIDE=REPO/'AGENTS.override.md'
MARKER='SYSTEM4_ISOLATED_ROOT_ENTRY_V4_POINT0_ONLY'
ROOT_COMMAND_POINT0='python3 isolated_system4/root_entry.py start-point0'
OLD_ENTRY_EXCLUSION='SYSTEM4 branch: DO NOT run `control/cloud-entry-gate/cloud_entry.py` before or instead of the System-4 root entry.'
CRITICAL_PATHS=(
 'AGENTS.md','AGENTS.override.md','isolated_system4/root_entry.py','isolated_system4/codex_entry.py',
 'isolated_system4/controller.py','isolated_system4/controller_core.py','isolated_system4/source_acquisition.py','isolated_system4/production_binding.py','isolated_system4/authoring_contract.py',
 'isolated_system4/content_guard.py','isolated_system4/design_guard.py','isolated_system4/production_checks.py',
 'isolated_system4/batch_gate.py','isolated_system4/batch_repetition_guard.py','isolated_system4/handoff_transport.py',
 'isolated_system4/LT68Worker.java','isolated_system4/point0_snapshot.py','isolated_system4/supervisor.py',
 'isolated_system4/root_supervisor_bridge.py','isolated_system4/worker_dispatch.py',
)

class EntryFail(RuntimeError):pass

def _within(child:Path,parent:Path)->bool:
 child=child.resolve(); parent=parent.resolve(); return child==parent or parent in child.parents

def _git(*args:str)->str:
 try:return subprocess.run(['git',*args],cwd=REPO,text=True,capture_output=True,check=True).stdout.strip()
 except Exception as exc:raise EntryFail('ROOT_ENTRY_GIT_IDENTITY_UNAVAILABLE') from exc

def _critical_manifest_sha256()->str:
 if Path(_git('rev-parse','--show-toplevel')).resolve()!=REPO.resolve():raise EntryFail('ROOT_ENTRY_GIT_ROOT_MISMATCH')
 _git('rev-parse','--verify','HEAD')
 tracked=set(_git('ls-files','--',*CRITICAL_PATHS).splitlines())
 missing=[rel for rel in CRITICAL_PATHS if rel not in tracked]
 if missing:raise EntryFail('ROOT_ENTRY_CRITICAL_FILE_UNTRACKED:'+missing[0])
 if _git('status','--porcelain=v1','--untracked-files=no','--',*CRITICAL_PATHS):raise EntryFail('ROOT_ENTRY_CRITICAL_FILES_DIRTY')
 rows=[]
 for rel in CRITICAL_PATHS:
  path=REPO/rel
  if not path.is_file():raise EntryFail('ROOT_ENTRY_CRITICAL_FILE_MISSING:'+rel)
  rows.append(rel+'\0'+hashlib.sha256(path.read_bytes()).hexdigest()+'\n')
 return hashlib.sha256(''.join(rows).encode()).hexdigest()

def _verify_common(workspace:Path)->str:
 if not ROOT_AGENTS.is_file():raise EntryFail('ROOT_AGENTS_MISSING')
 if not ROOT_OVERRIDE.is_file():raise EntryFail('ROOT_OVERRIDE_MISSING')
 base=ROOT_AGENTS.read_text(encoding='utf-8'); text=ROOT_OVERRIDE.read_text(encoding='utf-8')
 if 'python3 control/cloud-entry-gate/cloud_entry.py start' not in base:raise EntryFail('ROOT_AGENTS_IMMUTABLE_GATE_MISSING')
 if MARKER not in text:raise EntryFail('ROOT_OVERRIDE_SYSTEM4_ROUTE_MISSING')
 if ROOT_COMMAND_POINT0 not in text:raise EntryFail('ROOT_OVERRIDE_SYSTEM4_COMMAND_MISSING')
 if 'root_entry.py start-stdin' in text or 'root_entry.py start <' in text:raise EntryFail('ROOT_OVERRIDE_LEGACY_ENTRY_STILL_PRESENT')
 if OLD_ENTRY_EXCLUSION not in text:raise EntryFail('ROOT_OVERRIDE_OLD_ENTRY_EXCLUSION_MISSING')
 if _within(workspace,REPO):raise EntryFail('ROOT_ENTRY_WORKSPACE_MUST_BE_OUTSIDE_REPO')
 return _critical_manifest_sha256()

def _start_point0(point0:Path,workspace:Path,actual_manifest:str)->int:
 if not point0.is_file() or _within(point0,REPO):raise EntryFail('ROOT_POINT0_FILE_INVALID')
 actual_head=_git('rev-parse','--verify','HEAD')
 try:receipt=root_supervisor_bridge.bind_point0(point0,workspace,actual_manifest=actual_manifest,actual_head=actual_head)
 except Exception as exc:raise EntryFail('ROOT_POINT0_BIND_FAIL:'+str(exc)) from exc
 snapshot=workspace/'bound_snapshot.json'
 p=subprocess.run([sys.executable,str(CONTROLLER),'ingress',str(snapshot),str(workspace),'0'],text=True)
 if p.returncode:return p.returncode
 try:
  point0_value=json.loads((workspace/'point0.json').read_text(encoding='utf-8'))
  wc=root_supervisor_bridge.dispatch(workspace); bundle=worker_dispatch.build_bundle(point0_value,receipt,wc)
  worker_dispatch.verify_bundle(bundle,actual_manifest=actual_manifest,actual_head=actual_head)
  (workspace/'worker_dispatch.json').write_bytes(worker_dispatch.canon(bundle))
 except Exception as exc:raise EntryFail('ROOT_WORKER_DISPATCH_BUILD_FAIL:'+str(exc)) from exc
 print('SYSTEM4_ROOT_POINT0_PASS:WORKER_DISPATCH_READY'); return 0

def main(argv:list[str])->int:
 try:
  if len(argv)<2:raise EntryFail('ROOT_ENTRY_BAD_COMMAND')
  if argv[1] in {'start','start-stdin'}:raise EntryFail('ROOT_POINT0_REQUIRED')
  if argv[1]!='start-point0' or len(argv)!=4:raise EntryFail('ROOT_ENTRY_BAD_COMMAND')
  point0=Path(argv[2]); workspace=Path(argv[3]); manifest=_verify_common(workspace)
  return _start_point0(point0,workspace,manifest)
 except EntryFail as exc:
  print('SYSTEM4_ROOT_ENTRY_FAIL:'+str(exc)); return 2

if __name__=='__main__':raise SystemExit(main(sys.argv))
