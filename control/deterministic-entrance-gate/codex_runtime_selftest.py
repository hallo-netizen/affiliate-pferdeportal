#!/usr/bin/env python3
"""One-time no-API hard-worker runtime proof.
Requires Codex CLI logged in via ChatGPT, never an API key.
"""
from __future__ import annotations
import argparse, json, os, shutil, subprocess, sys, tempfile
from pathlib import Path

HERE=Path(__file__).resolve().parent
DOOR=HERE/'door.py'; HARNESS=HERE/'worker_harness.py'

def run(cmd, **kw): return subprocess.run(cmd,text=True,capture_output=True,**kw)
def clean_env():
    allowed={"HOME","PATH","TMPDIR","TEMP","TMP","LANG","LC_ALL","TERM","USER","LOGNAME","SHELL","XDG_CONFIG_HOME","CODEX_HOME"}
    return {k:v for k,v in os.environ.items() if k in allowed}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--master',required=True); ap.add_argument('--model',default='gpt-5.6-sol'); ap.add_argument('--advance',action='store_true'); args=ap.parse_args()
    codex=shutil.which('codex')
    if not codex:
        print(json.dumps({'ok':False,'status':'HARD_WORKER_SELFTEST_BLOCKED','reason':'CODEX_CLI_NOT_INSTALLED'},indent=2)); return 2
    status=run([codex,'login','status'],env=clean_env())
    combined=(status.stdout+'\n'+status.stderr).strip()
    if status.returncode!=0 or 'Logged in using ChatGPT' not in combined:
        print(json.dumps({'ok':False,'status':'HARD_WORKER_SELFTEST_BLOCKED','reason':'CODEX_NOT_LOGGED_IN_USING_CHATGPT','login_status':combined},ensure_ascii=False,indent=2)); return 2
    with tempfile.TemporaryDirectory(prefix='pferde_gate_selftest_') as td:
        td=Path(td); cap=td/'capsule'; receipt=td/'receipt.json'
        q=run([sys.executable,str(DOOR),'issue','--master',args.master,'--out',str(cap)])
        if q.returncode!=0:
            print(q.stdout); return 2
        w=run([sys.executable,str(HARNESS),'--capsule',str(cap),'--adapter','codex','--model',args.model,'--effort','low','--out',str(receipt),'--timeout','600'],env=clean_env())
        if w.returncode!=0:
            print(w.stdout); return 2
        v=run([sys.executable,str(DOOR),'validate-receipt','--ticket',str(cap/'TICKET.json'),'--receipt',str(receipt)])
        if v.returncode!=0:
            print(v.stdout); return 2
        result={'ok':True,'status':'HARD_WORKER_SELFTEST_PASS_CHATGPT_AUTH_NO_API','login_status':combined,'receipt_validation':json.loads(v.stdout)}
        if args.advance:
            a=run([sys.executable,str(DOOR),'advance','--master',args.master,'--ticket',str(cap/'TICKET.json'),'--receipt',str(receipt)])
            if a.returncode!=0:
                print(a.stdout); return 2
            result['advance']=json.loads(a.stdout)
        print(json.dumps(result,ensure_ascii=False,indent=2)); return 0
if __name__=='__main__': sys.exit(main())
