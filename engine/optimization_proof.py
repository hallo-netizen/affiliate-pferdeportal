from __future__ import annotations
from . import real_proof as rp

# Uses the canonical System4 WordPress exporter.

if __name__=='__main__':
    try:
        rp.main()
    except rp.Blocked as exc:
        import json
        print(json.dumps({'contract':'K10_OPTIMIZATION_REAL_PROOF_V1','status':'BLOCKED','reason':str(exc),'publish_allowed':False},ensure_ascii=False,indent=2))
        raise SystemExit(2)
