from __future__ import annotations
import json, subprocess, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parent
CONTROLLER=ROOT/'controller.py'
ALLOWED={
 'RESEARCH_REQUIRED':'Create only SYSTEM4_RESEARCH_EVIDENCE_V1 JSON with real source title/url/retrieved_at/evidence and snapshot_sha256=SHA256(evidence); then controller research.',
 'FACT_CHECK_REQUIRED':'Create only SYSTEM4_FACTS_EVIDENCE_V1 JSON with claims bound to the accepted research source_ids and evidence_text hashes; then controller facts.',
 'DRAFT_REQUIRED':'Bind production context from exactly the accepted research/facts first if not already bound; then write only the same article body using the unchanged current Textmaschine/content rules.',
 'CHECK_REQUIRED':'Run controller fullcheck. Writer may not choose routing.',
 'REPAIR_REQUIRED':'Edit only the same draft body for the exact reported first defect; controller repair rejects broad rewrites; then rerun fullcheck.',
 'OUTPUT_GATE_REQUIRED':'Article passed. Do not mutate content. For batch work keep the state unchanged until batch_gate collect.',
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

def main(argv):
 if len(argv)<3 or argv[1] not in {'start','next'}:
  print('SYSTEM4_CODEX_ENTRY_FAIL:BAD_COMMAND'); return 2
 if argv[1]=='start':
  if len(argv)!=4: print('SYSTEM4_CODEX_ENTRY_FAIL:BAD_START_ARGS'); return 2
  snapshot=Path(argv[2]); workspace=Path(argv[3])
  p=subprocess.run([sys.executable,str(CONTROLLER),'ingress',str(snapshot),str(workspace)],text=True)
  if p.returncode: return p.returncode
  return show(workspace)
 return show(Path(argv[2]))
if __name__=='__main__': raise SystemExit(main(sys.argv))
