#!/usr/bin/env python3
from pathlib import Path
import json, sys

ROOT=Path(__file__).resolve().parent
RUNTIME=ROOT/'runtime'
FORBIDDEN=(
    'isolated_system4','system4','system_4','system 4','system4a','4a',
    'konzept 1','konzept 2','konzept 3','konzept 4',
    'system 1','system 2','system 3'
)
def main():
    problems=[]
    if RUNTIME.exists():
        for p in RUNTIME.rglob('*'):
            if not p.is_file(): continue
            try: s=p.read_text(encoding='utf-8').lower()
            except Exception: continue
            for token in FORBIDDEN:
                if token in s:
                    problems.append(f'{p.relative_to(ROOT)} -> {token}')
    manifest=json.loads((ROOT/'RECONSTRUCTION_MANIFEST.json').read_text(encoding='utf-8'))
    missing=manifest.get('missing_exact_runtime_components') or []
    print(json.dumps({
        'contract':'KONZEPT0_ISOLATION_CHECK_V1',
        'runtime_cross_contact':'BLOCKED' if problems else 'PASS',
        'cross_contact_findings':problems,
        'full_runtime_reactivation_ready': False if missing else True,
        'missing_exact_runtime_components':missing,
        'codex_started':False,
        'publish_performed':False
    },ensure_ascii=False,indent=2))
    return 2 if problems else 0
if __name__=='__main__': sys.exit(main())
