#!/usr/bin/env python3
import hashlib, json, sys

def canon(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")

def main():
    payload=json.load(sys.stdin)
    if not isinstance(payload,dict) or set(payload)!={"item_id","facts"}:
        raise SystemExit(2)
    if not isinstance(payload["item_id"],str) or not payload["item_id"]:
        raise SystemExit(2)
    facts=payload["facts"]
    if not isinstance(facts,list) or not all(isinstance(x,str) and x for x in facts):
        raise SystemExit(2)
    out={
        "engine_contract":"P2_FROZEN_TEXTMACHINE_STUB_V1",
        "input_hash":hashlib.sha256(canon(payload)).hexdigest(),
        "item_id":payload["item_id"],
        "facts":facts,
        "draft":"Draft: "+" | ".join(facts),
    }
    json.dump(out,sys.stdout,sort_keys=True,separators=(",",":"),ensure_ascii=False)

if __name__=="__main__":
    main()
