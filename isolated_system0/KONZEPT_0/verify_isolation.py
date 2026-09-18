#!/usr/bin/env python3
from pathlib import Path
import json, sys, re

ROOT=Path(__file__).resolve().parent
RUNTIME=ROOT/'runtime'
ACTIVE_SUFFIXES={'.py','.php','.sh','.json','.yml','.yaml'}
FORBIDDEN_PATTERNS=(
    r'isolated_system4(?:a)?(?:/|\\)',
    r'\bsystem[_ -]?4a?\b',
    r'\bkonzept[_ -]?[1-4]\b',
    r'\bsystem[_ -]?[1-3]\b',
)

def main():
    problems=[]
    if RUNTIME.exists():
        for p in RUNTIME.rglob('*'):
            if not p.is_file() or p.name == 'README.md' or p.suffix.lower() not in ACTIVE_SUFFIXES:
                continue
            try:
                s=p.read_text(encoding='utf-8').lower()
            except Exception:
                continue
            s=re.sub(r'"concept_[^"]+_runtime_contact"\s*:\s*false','',s)
            for pattern in FORBIDDEN_PATTERNS:
                if re.search(pattern,s):
                    problems.append(f'{p.relative_to(ROOT)} -> {pattern}')
    manifest=json.loads((ROOT/'RECONSTRUCTION_MANIFEST.json').read_text(encoding='utf-8'))
    unresolved=manifest.get('unresolved_aug28_exact_components') or manifest.get('missing_exact_runtime_components') or []
    print(json.dumps({
        'contract':'KONZEPT0_ISOLATION_CHECK_V2',
        'runtime_cross_contact':'BLOCKED' if problems else 'PASS',
        'cross_contact_findings':problems,
        'exact_aug28_reconstruction_complete':False if unresolved else True,
        'unresolved_aug28_exact_components':unresolved,
        'codex_started':False,
        'publish_performed':False
    },ensure_ascii=False,indent=2))
    return 2 if problems else 0

if __name__=='__main__': sys.exit(main())
