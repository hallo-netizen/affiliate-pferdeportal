#!/usr/bin/env python3
"""Generic no-API worker harness for a previously issued capsule.

Hard-mode target: Codex CLI authenticated with the user's ChatGPT plan.
The harness never reads the master tree. It receives only the capsule directory.
"""
from __future__ import annotations
import argparse, json, os, shutil, subprocess, sys
from pathlib import Path

class HarnessBlocked(RuntimeError): pass

def read_json(p: Path): return json.loads(p.read_text(encoding="utf-8"))

def build_codex_command(capsule: Path, model: str, effort: str, out: Path):
    codex = shutil.which("codex")
    if not codex: raise HarnessBlocked("CODEX_CLI_NOT_INSTALLED")
    schema = capsule / "RECEIPT_SCHEMA.json"
    if not schema.is_file(): raise HarnessBlocked("RECEIPT_SCHEMA_MISSING")
    # The worker receives only a minimal process environment; project credentials are not forwarded.
    return [
        codex, "exec",
        "--ephemeral",
        "--ignore-user-config",
        "--ignore-rules",
        "--sandbox", "read-only",
        "--skip-git-repo-check",
        "-C", str(capsule),
        "-m", model,
        "-c", f'model_reasoning_effort="{effort}"',
        "-c", 'approval_policy="never"',
        "-c", 'web_search="disabled"',
        "--output-schema", str(schema),
        "--output-last-message", str(out),
        "-",
    ]

def instruction_text(capsule: Path):
    ticket = read_json(capsule / "TICKET.json")
    instruction = (capsule / "INSTRUCTION.txt").read_text(encoding="utf-8")
    return (
        "You are a step worker with ZERO workflow-navigation authority.\n"
        f"Execute exactly step_id={ticket['step_id']} and no other workflow step.\n"
        "Use only the files in this capsule. Do not inspect a parent directory, another repository, old state, old master, chat history, or unrelated files.\n"
        "Do not choose, suggest, repeat, skip, or reorder workflow steps.\n"
        "Do not request a state write or workflow change. Return only the receipt required by RECEIPT_SCHEMA.json.\n\n"
        "BOUND STEP INSTRUCTION:\n" + instruction
    )

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--capsule", required=True)
    ap.add_argument("--adapter", choices=["codex", "simulate"], default="codex")
    ap.add_argument("--model", default="gpt-5.6-sol")
    ap.add_argument("--effort", choices=["low","medium","high","xhigh","max","ultra"], default="high")
    ap.add_argument("--out", required=True)
    ap.add_argument("--timeout", type=int, default=1800)
    args=ap.parse_args()
    capsule=Path(args.capsule).resolve(); out=Path(args.out).resolve()
    try:
        if not (capsule/"TICKET.json").is_file() or not (capsule/"CAPSULE_MANIFEST.json").is_file():
            raise HarnessBlocked("CAPSULE_INVALID")
        if args.adapter == "simulate":
            ticket=read_json(capsule/"TICKET.json")
            receipt={
                "contract":"PFERDE_ATELIER_STEP_RECEIPT_V1",
                "ticket_id":ticket["ticket_id"],"step_id":ticket["step_id"],"sequence":ticket["sequence"],
                "state_sha256":ticket["state_sha256"],"bundle_sha256":ticket["bundle_sha256"],
                "status":"PASS","navigation_decision":False,"state_write_requested":False,"workflow_change_requested":False,
                "payload":{"simulation":True},"evidence":["SIMULATED_WORKER_ONLY"]
            }
            out.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
            print(json.dumps({"ok":True,"status":"SIMULATED_RECEIPT_WRITTEN","out":str(out)},ensure_ascii=False,indent=2)); return 0
        cmd=build_codex_command(capsule,args.model,args.effort,out)
        allowed_env={"HOME","PATH","TMPDIR","TEMP","TMP","LANG","LC_ALL","TERM","USER","LOGNAME","SHELL","XDG_CONFIG_HOME","CODEX_HOME"}
        env={k:v for k,v in os.environ.items() if k in allowed_env}
        proc=subprocess.run(cmd,input=instruction_text(capsule),text=True,capture_output=True,env=env,timeout=args.timeout)
        if proc.returncode != 0: raise HarnessBlocked("CODEX_EXEC_FAILED:"+str(proc.returncode))
        if not out.is_file(): raise HarnessBlocked("CODEX_RECEIPT_MISSING")
        print(json.dumps({"ok":True,"status":"CODEX_RECEIPT_WRITTEN","out":str(out),"model":args.model,"effort":args.effort},ensure_ascii=False,indent=2)); return 0
    except (HarnessBlocked, subprocess.TimeoutExpired) as exc:
        print(json.dumps({"ok":False,"status":"WORKER_HARNESS_BLOCKED","reason":str(exc)},ensure_ascii=False,indent=2)); return 2
if __name__=="__main__": sys.exit(main())
