from __future__ import annotations
import json, subprocess, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parent
CONTROLLER=ROOT/'controller.py'
ALLOWED={
 'RESEARCH_REQUIRED':'Writer may create/update research only; then controller research.',
 'FACT_CHECK_REQUIRED':'Writer may create/update facts only; then controller facts.',
 'DRAFT_REQUIRED':'Writer may create/update draft only; then controller draft.',
 'CHECK_REQUIRED':'Run controller check. Writer may not choose routing.',
 'REPAIR_REQUIRED':'Writer may edit only the same draft field to fix last_error; then resubmit and recheck.',
 'OUTPUT_GATE_REQUIRED':'Run controller release. No content mutation allowed.',
 'RELEASED':'STOP. Return release paths and hashes only.'}

def show(workspace: Path) -> int:
 p=workspace/'state.json'
 if not p.is_file(): print('SYSTEM4_CODEX_ENTRY_FAIL:STATE_MISSING'); return 2
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
