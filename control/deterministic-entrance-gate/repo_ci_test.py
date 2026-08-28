#!/usr/bin/env python3
from pathlib import Path
import hashlib,json,shutil,subprocess,sys,tempfile
REPO=Path(__file__).resolve().parents[2]
DOOR=REPO/'control/deterministic-entrance-gate/door.py'
HARNESS=REPO/'control/deterministic-entrance-gate/worker_harness.py'
def run(c): return subprocess.run(c,text=True,capture_output=True)
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p): return json.loads(Path(p).read_text())
def dump(p,o): Path(p).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n')
def main():
  with tempfile.TemporaryDirectory() as td:
    m=Path(td)/'m'; (m/'00_CONTROL/CONTROL_RUNNER_V2/runtime').mkdir(parents=True); (m/'00_CONTROL/STEP_BUNDLES').mkdir(parents=True); (m/'00_CONTROL/DETERMINISTIC_ENTRANCE_GATE_V1').mkdir(parents=True)
    shutil.copy(REPO/'control/startmaster0104/PFERDE_ATELIER_START_HERE.json',m/'PFERDE_ATELIER_START_HERE.json')
    shutil.copy(REPO/'control/startmaster0104/CURRENT_STATE.json',m/'00_CONTROL/CONTROL_RUNNER_V2/runtime/CURRENT_STATE.json')
    shutil.copy(REPO/'control/startmaster0104/STEP_104000_HARD_WORKER_SELFTEST_NO_API.json',m/'00_CONTROL/STEP_BUNDLES/STEP_104000_HARD_WORKER_SELFTEST_NO_API.json')
    shutil.copy(REPO/'control/startmaster0104/STEP_104001_ROOTFIX_LIVE_40_40.json',m/'00_CONTROL/STEP_BUNDLES/STEP_104001_ROOTFIX_LIVE_40_40.json')
    shutil.copy(DOOR,m/'00_CONTROL/DETERMINISTIC_ENTRANCE_GATE_V1/door.py'); shutil.copy(HARNESS,m/'00_CONTROL/DETERMINISTIC_ENTRANCE_GATE_V1/worker_harness.py')
    q=run([sys.executable,str(DOOR),'validate','--master',str(m)]); assert q.returncode==0,q.stdout+q.stderr
    cap=Path(td)/'cap'; rec=Path(td)/'rec.json'; assert run([sys.executable,str(DOOR),'issue','--master',str(m),'--out',str(cap)]).returncode==0
    assert run([sys.executable,str(HARNESS),'--capsule',str(cap),'--adapter','simulate','--out',str(rec)]).returncode==0
    assert run([sys.executable,str(DOOR),'validate-receipt','--ticket',str(cap/'TICKET.json'),'--receipt',str(rec)]).returncode==0
    a=run([sys.executable,str(DOOR),'advance','--master',str(m),'--ticket',str(cap/'TICKET.json'),'--receipt',str(rec)]); assert a.returncode==0,a.stdout+a.stderr
    assert load(m/'00_CONTROL/CONTROL_RUNNER_V2/runtime/CURRENT_STATE.json')['next_allowed_step']=='ROOTFIX_LIVE_40_40_MAX_FAMILIES_REACHED'
  text=(DOOR.read_text()+HARNESS.read_text()).lower()
  for token in ['pste','pserc','ppm','languagetool','wordpress','keyword','title_rule','beratung','pflege','cannibal','design_rule','api.openai.com','urllib.request']:
    assert token not in text,token
  print(json.dumps({'ok':True,'status':'GITHUB_ENTRANCE_GATE_CI_PASS','api_required':False,'free_chat_execution_authority':False},indent=2))
if __name__=='__main__': main()
