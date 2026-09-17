from __future__ import annotations
import json, subprocess, sys
from pathlib import Path

import root_entry, worker_dispatch, supervisor

ROOT=Path(__file__).resolve().parent
CONTROLLER=ROOT/'controller.py'
ALLOWED={
 'RESEARCH_REQUIRED':'Create only SYSTEM4_RESEARCH_EVIDENCE_V1 JSON with real source title/url/retrieved_at/evidence and snapshot_sha256=SHA256(evidence); then controller research.',
 'FACT_CHECK_REQUIRED':'Create only SYSTEM4_FACTS_EVIDENCE_V1 JSON with claims bound to the accepted research source_ids and evidence_text hashes; then controller facts.',
 'CONTEXT_REQUIRED':'Bind production context from exactly the accepted research/facts and derive the hash-bound authoring contract; then controller context.',
 'DRAFT_REQUIRED':'Bind production context from exactly the accepted research/facts first if not already bound; then write only the same article body using the unchanged current Textmaschine/content rules AND unchanged existing production/design markup. Do not create CSS, inline styles, replacement classes or alternate heading/table design.',
 'CHECK_REQUIRED':'Run controller fullcheck. Writer may not choose routing and may not alter Textmaschine/design authority.',
 'REPAIR_REQUIRED':'WORKSHOP: repair every reported finding assigned to the current authoritative owner/target in machine_repair_request.json; do not reduce the request to findings[0], do not broaden beyond reported findings, and do not alter Textmaschine/design authority. Then controller repair and rerun the complete fullcheck.',
 'OUTPUT_GATE_REQUIRED':'Article passed. Do not mutate content or design. For batch work keep the state unchanged until batch_gate collect. If batch_gate routes any error to GLOBAL_WORKSHOP, continue only through the workshop-directed REPAIR_REQUIRED article states and rerun the complete checks before collecting the batch again.',
 'SIGNATURE_REQUIRED':'STOP. Signing is not part of the current unsigned System-4 article path.',
 'RELEASED':'STOP. Return release paths and hashes only.'}

def show(workspace: Path) -> int:
 p=workspace/'state.json'
 if not p.is_file(): print('SYSTEM4_CODEX_ENTRY_FAIL:STATE_MISSING'); return 2
 v=subprocess.run([sys.executable,str(CONTROLLER),'verify',str(workspace)],text=True,capture_output=True)
 if v.returncode:
  print('SYSTEM4_CODEX_ENTRY_FAIL:'+v.stdout.strip().removeprefix('SYSTEM4_FAIL:')); return v.returncode
 s=json.loads(p.read_text(encoding='utf-8')); phase=s.get('phase')
 if phase not in ALLOWED: print('SYSTEM4_CODEX_ENTRY_FAIL:UNKNOWN_PHASE'); return 2
 print('SYSTEM4_CODEX_ENTRY_PASS:'+phase)
 print(ALLOWED[phase]); return 0

def _head()->str:
 cp=subprocess.run(['git','rev-parse','--verify','HEAD'],cwd=ROOT.parent,text=True,capture_output=True,check=True)
 return cp.stdout.strip()

def worker_start(workspace:Path)->int:
 bundle_path=workspace/'worker_dispatch.json'
 if not bundle_path.is_file(): print('SYSTEM4_CODEX_ENTRY_FAIL:WORKER_DISPATCH_MISSING'); return 2
 try:
  bundle=json.loads(bundle_path.read_text(encoding='utf-8'))
  manifest=root_entry._critical_manifest_sha256(); head=_head()
  wc,_=worker_dispatch.verify_bundle(bundle,actual_manifest=manifest,actual_head=head)
  supervisor.verify_controller_binding(workspace)
  if wc.get('external_web_search_allowed') is not False: raise RuntimeError('FREE_WEB_NOT_BLOCKED')
 except Exception as exc:
  print('SYSTEM4_CODEX_ENTRY_FAIL:WORKER_DISPATCH_INVALID:'+str(exc)); return 2
 return show(workspace)

def main(argv):
 if len(argv)<3 or argv[1] not in {'start','next','worker-start'}:
  print('SYSTEM4_CODEX_ENTRY_FAIL:BAD_COMMAND'); return 2
 if argv[1]=='worker-start':
  if len(argv)!=3: print('SYSTEM4_CODEX_ENTRY_FAIL:BAD_WORKER_START_ARGS'); return 2
  return worker_start(Path(argv[2]))
 if argv[1]=='start':
  print('SYSTEM4_CODEX_ENTRY_FAIL:SUPERVISOR_DISPATCH_REQUIRED'); return 2
 return show(Path(argv[2]))
if __name__=='__main__': raise SystemExit(main(sys.argv))
