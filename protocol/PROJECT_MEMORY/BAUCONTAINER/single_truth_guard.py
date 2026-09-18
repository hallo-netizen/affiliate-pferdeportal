#!/usr/bin/env python3
import json, pathlib, re, sys

ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
PLAN = ROOT / "protocol/PROJECT_MEMORY/AUTORITAETSPLAN.json"
MARK_ENTRY = "CAMPUS_SINGLE_TRUTH_ENTRY_V1"
MARK_EXEC = "DERIVED_EXECUTION_SURFACE_V1"

class Blocked(RuntimeError): pass

def read(p):
    if not p.is_file(): raise Blocked("MISSING:" + p.relative_to(ROOT).as_posix())
    return p.read_text(encoding="utf-8")

def has_next_action(path, text):
    if path.suffix == ".json":
        try: data=json.loads(text)
        except Exception as e: raise Blocked("CURRENT_JSON_INVALID:" + path.as_posix() + ":" + str(e))
        es=data.get("execution_state") if isinstance(data,dict) else None
        return bool(
            isinstance(data,dict) and (
                data.get("next_action") or data.get("next_allowed_step") or data.get("authorized_next_action")
                or (isinstance(es,dict) and (es.get("authorized_next_action") or es.get("next_action")))
            )
        )
    return bool(re.search(r"(?mi)^##\s+NEXT ACTION\b", text))

def main():
    data=json.loads(read(PLAN))
    if data.get("contract")!="CAMPUS_SINGLE_TRUTH_ROUTING_V1":
        raise Blocked("AUTHORITY_PLAN_CONTRACT")
    if not data.get("rules",{}).get("exactly_one_current_authority_per_scope"):
        raise Blocked("SINGLE_TRUTH_RULE_DISABLED")
    ids=set(); starts=set()
    for scope in data.get("scopes",[]):
        sid=str(scope.get("id","")).strip()
        cur=str(scope.get("current_authority","")).strip()
        start=str(scope.get("start_here","")).strip()
        if not sid or sid in ids: raise Blocked("SCOPE_ID_INVALID:"+sid)
        ids.add(sid)
        if not cur or not start: raise Blocked("SCOPE_ROUTE_INCOMPLETE:"+sid)
        sp=ROOT/start; cp=ROOT/cur
        st=read(sp); ct=read(cp)
        if MARK_ENTRY not in st: raise Blocked("START_HERE_SINGLE_TRUTH_MARKER_MISSING:"+start)
        if not has_next_action(cp,ct):
            raise Blocked("CURRENT_NEXT_ACTION_MISSING:"+cur)
        if start in starts: raise Blocked("START_HERE_DUPLICATE_SCOPE:"+start)
        starts.add(start)
        ex=str(scope.get("execution_surface","")).strip()
        if ex:
            ep=ROOT/ex; et=read(ep)
            if MARK_EXEC not in et: raise Blocked("EXECUTION_SURFACE_MARKER_MISSING:"+ex)
            forbidden=[
                "AKTUELLER AUFTRAG / NEXT ACTION: ausschließlich diese",
                "AKTUELLE ARBEIT / NEXT ACTION: ausschließlich diese",
                "HOBBYRAUM = eine aktuelle Auftragswahrheit"
            ]
            if any(x.lower() in et.lower() for x in forbidden):
                raise Blocked("EXECUTION_SURFACE_CLAIMS_CURRENT_AUTHORITY:"+ex)
    navigation=[
        "protocol/PROJECT_MEMORY/START_HERE.md",
        "protocol/PROJECT_MEMORY/HAUPTPFOERTNER.md",
        "protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/START_HERE.md",
    ]
    for rel in navigation:
        t=read(ROOT/rel)
        if "AUTORITAETSPLAN.json" not in t:
            raise Blocked("NAVIGATION_AUTHORITY_PLAN_MISSING:"+rel)
    print("CAMPUS_SINGLE_TRUTH_GUARD_PASS:"+str(len(ids)))

if __name__=="__main__":
    try: main()
    except Blocked as e:
        print("CAMPUS_SINGLE_TRUTH_GUARD_BLOCKED:"+str(e), file=sys.stderr)
        sys.exit(2)
