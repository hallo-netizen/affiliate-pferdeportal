from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

CONTRACT = 'K0_RESEARCH_FRESHNESS_GUARD_V1'

class Blocked(RuntimeError):
    pass

def _stable(value):
    return hashlib.sha256(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')
    ).hexdigest()

def _parts(ctx):
    pc = ctx.get('production_context') if isinstance(ctx, dict) else None
    rc = ctx.get('rule_context') if isinstance(ctx, dict) else None
    fp = pc.get('fact_pack') if isinstance(pc, dict) else None
    claims = rc.get('research_claims') if isinstance(rc, dict) else None
    if not isinstance(fp, dict) or not isinstance(claims, dict) or not claims:
        raise Blocked('K0_RESEARCH_FRESHNESS_INPUT_INVALID')
    return fp, claims

def verify(current_context_path, repo_root='.'):
    root = Path(repo_root).resolve()
    current = (root / str(current_context_path)).resolve()
    if not current.is_file():
        raise Blocked('K0_RESEARCH_FRESHNESS_CURRENT_CONTEXT_MISSING')
    try:
        current.relative_to(root)
    except ValueError:
        raise Blocked('K0_RESEARCH_FRESHNESS_CONTEXT_OUTSIDE_REPO')

    ctx = json.loads(current.read_text(encoding='utf-8'))
    fp, claims = _parts(ctx)
    fp_hash = _stable(fp)
    claims_hash = _stable(claims)
    compared = 0

    for p in root.glob('real_runs/k0/**/AUTHORING_CONTEXT.json'):
        rp = p.resolve()
        if rp == current:
            continue
        compared += 1
        try:
            old = json.loads(p.read_text(encoding='utf-8'))
            old_fp, old_claims = _parts(old)
        except Exception:
            continue
        if _stable(old_fp) == fp_hash:
            raise Blocked('K0_HISTORICAL_FACT_PACK_REUSE_BLOCKED')
        if _stable(old_claims) == claims_hash:
            raise Blocked('K0_HISTORICAL_RESEARCH_PACKET_REUSE_BLOCKED')

    return {
        'contract': CONTRACT,
        'status': 'PASS',
        'fact_pack_sha256': fp_hash,
        'research_claims_sha256': claims_hash,
        'compared_historical_contexts': compared,
        'historical_fact_pack_reuse': False,
        'historical_research_packet_reuse': False,
        'publish_allowed': False,
    }

def main():
    if len(sys.argv) != 3:
        raise SystemExit('usage: k0_research_freshness_guard.py CURRENT_AUTHORING_CONTEXT OUT')
    try:
        out = verify(sys.argv[1], '.')
        Path(sys.argv[2]).write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print(json.dumps(out, ensure_ascii=False))
    except Exception as exc:
        print(json.dumps({
            'contract': CONTRACT,
            'status': 'BLOCKED',
            'reason': str(exc),
            'publish_allowed': False,
        }, ensure_ascii=False))
        raise SystemExit(2)

if __name__ == '__main__':
    main()
