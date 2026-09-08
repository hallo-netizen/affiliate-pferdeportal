from __future__ import annotations
import copy, hashlib, json, os, subprocess, sys
from pathlib import Path
from typing import Any

class Blocked(RuntimeError):
    pass

def canon(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")

def sha_obj(obj: Any) -> str:
    return hashlib.sha256(canon(obj)).hexdigest()

def sha_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

STEP_ORDER=("RESEARCH","TEXT_SLOT","FINAL_CHECK")
RESEARCH_KEYS={"job_id","input_hash","output","output_hash"}
TEXTMACHINE_FILE="frozen_textmachine_stub.py"
TEXTMACHINE_SHA256="8fa1056b76ef83dc1e1b2557fcbf3ac7b0996bfe377a8d1c7f4357426dd1cbcd"
TEXTMACHINE_CONTRACT="P2_FROZEN_TEXTMACHINE_STUB_V1"

class CentralMachine:
    def __init__(self, job_id: str, item_id: str):
        if not isinstance(job_id,str) or not job_id:
            raise ValueError("job_id required")
        if not isinstance(item_id,str) or not item_id:
            raise ValueError("item_id required")
        self._job_id=job_id
        self._item_id=item_id
        self._index=0
        self._payload={"item_id":item_id}
        self._history=[]
        self._blocked=False

    @property
    def current_step(self):
        return None if self._blocked or self._index>=len(STEP_ORDER) else STEP_ORDER[self._index]

    @property
    def finished(self):
        return not self._blocked and self._index==len(STEP_ORDER)

    def research_input(self):
        self._require("RESEARCH")
        payload=copy.deepcopy(self._payload)
        return {"job_id":self._job_id,"input_hash":sha_obj(payload),"payload":payload}

    def submit_research(self, raw: dict):
        self._require("RESEARCH")
        if not isinstance(raw,dict) or set(raw)!=RESEARCH_KEYS:
            self._block("RESEARCH_SCHEMA_INVALID")
        if raw["job_id"]!=self._job_id:
            self._block("JOB_ID_MISMATCH")
        if raw["input_hash"]!=sha_obj(self._payload):
            self._block("INPUT_HASH_MISMATCH")
        if raw["output_hash"]!=sha_obj(raw["output"]):
            self._block("OUTPUT_HASH_MISMATCH")
        out=raw["output"]
        if not isinstance(out,dict) or set(out)!={"item_id","facts"}:
            self._block("RESEARCH_OUTPUT_INVALID")
        if out.get("item_id")!=self._item_id:
            self._block("ITEM_ID_MISMATCH")
        facts=out.get("facts")
        if not isinstance(facts,list) or not facts or not all(isinstance(x,str) and x for x in facts):
            self._block("RESEARCH_FACTS_INVALID")
        self._advance(out,raw["input_hash"],raw["output_hash"])

    def run_textmachine(self):
        self._require("TEXT_SLOT")
        engine=Path(__file__).with_name(TEXTMACHINE_FILE)
        if not engine.is_file() or sha_file(engine)!=TEXTMACHINE_SHA256:
            self._block("TEXTMACHINE_IDENTITY_MISMATCH")
        inp={"item_id":self._item_id,"facts":copy.deepcopy(self._payload["facts"])}
        env={k:v for k,v in os.environ.items() if k not in {"TEXTMACHINE_PATH","TEXTMACHINE_ENGINE","TEXTMACHINE_ARGS"}}
        proc=subprocess.run(
            [sys.executable,str(engine)],
            input=canon(inp),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=10,
            env=env,
        )
        if proc.returncode!=0:
            self._block("TEXTMACHINE_EXECUTION_FAILED")
        try:
            out=json.loads(proc.stdout.decode("utf-8"))
        except Exception:
            self._block("TEXTMACHINE_OUTPUT_INVALID")
        required={"engine_contract","input_hash","item_id","facts","draft"}
        if not isinstance(out,dict) or set(out)!=required:
            self._block("TEXTMACHINE_OUTPUT_INVALID")
        if out["engine_contract"]!=TEXTMACHINE_CONTRACT:
            self._block("TEXTMACHINE_CONTRACT_MISMATCH")
        if out["input_hash"]!=sha_obj(inp):
            self._block("TEXTMACHINE_INPUT_BINDING_MISMATCH")
        if out["item_id"]!=self._item_id or out["facts"]!=inp["facts"]:
            self._block("TEXTMACHINE_CONTEXT_DRIFT")
        if not isinstance(out["draft"],str) or not out["draft"]:
            self._block("TEXTMACHINE_DRAFT_INVALID")
        self._advance(
            {"item_id":self._item_id,"facts":inp["facts"],"draft":out["draft"]},
            sha_obj(inp),
            sha_obj(out),
        )

    def run_final_check(self):
        self._require("FINAL_CHECK")
        draft=self._payload.get("draft")
        if not isinstance(draft,str) or not draft:
            self._block("FINAL_DRAFT_INVALID")
        low=draft.lower()
        if "http://" in low or "https://" in low:
            self._block("PROTOTYPE_LINK_RULE_BLOCKED")
        out=copy.deepcopy(self._payload)
        out["checks"]={"all_required_checks_passed":True}
        self._advance(out,sha_obj(self._payload),sha_obj(out))

    def final_output(self):
        if not self.finished:
            raise Blocked("NOT_FINISHED")
        return copy.deepcopy(self._payload)

    def snapshot(self):
        return {
            "job_id":self._job_id,
            "item_id":self._item_id,
            "current_step":self.current_step,
            "finished":self.finished,
            "blocked":self._blocked,
            "payload":copy.deepcopy(self._payload),
            "history":copy.deepcopy(self._history),
        }

    def _require(self,step):
        if self.current_step!=step:
            self._block("STEP_ORDER_VIOLATION")

    def _advance(self,out,input_hash,output_hash):
        self._history.append({
            "step_id":STEP_ORDER[self._index],
            "input_hash":input_hash,
            "output_hash":output_hash,
        })
        self._payload=copy.deepcopy(out)
        self._index+=1

    def _block(self,code):
        self._blocked=True
        raise Blocked(code)

def make_research_result(inp: dict, facts: list[str]):
    out={"item_id":inp["payload"]["item_id"],"facts":facts}
    return {
        "job_id":inp["job_id"],
        "input_hash":inp["input_hash"],
        "output":out,
        "output_hash":sha_obj(out),
    }
