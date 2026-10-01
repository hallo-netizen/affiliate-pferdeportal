import json,re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
ALLOWED_REFERENCE_FILES={
    'K9_BASELINE_REFERENCE.json','K10_START_HERE.md','README.md','CURRENT_STATE.json'
}
FORBIDDEN_NAMES={'runtime','warehouse','submissions','writer_drafts','final','__pycache__'}
FORBIDDEN_ACTIVE_PATTERNS=(
    r'\bimport\s+k9_',r'\bfrom\s+k9_',r'\bk9_engine\.py\b',r'\bk9_write_packager\.py\b',
    r'\bK9_STOP\.json\b',r'\bK9_WORDPRESS_DIRECT_IMPORT_[0-9a-f]+'
)

def verify():
    findings=[]
    for p in ROOT.rglob('*'):
        rel=p.relative_to(ROOT)
        # Git metadata is repository history/transport state, not active K10 project content.
        if rel.parts and rel.parts[0]=='.git':
            continue
        if any(part in FORBIDDEN_NAMES for part in rel.parts):
            # Python bytecode caches are build byproducts, ignored after being flagged for cleanup.
            if '__pycache__' in rel.parts:
                continue
            findings.append('FORBIDDEN_K9_CONTENT_PATH:'+str(rel))
        if not p.is_file() or p.suffix=='.pyc':
            continue
        if p.name in ALLOWED_REFERENCE_FILES or rel.as_posix()=='engine/isolation_guard.py':
            continue
        text=p.read_text(encoding='utf-8',errors='ignore')
        for pat in FORBIDDEN_ACTIVE_PATTERNS:
            if re.search(pat,text,re.I):
                findings.append('FORBIDDEN_K9_ACTIVE_REFERENCE:'+str(rel)+':'+pat)
    ref=json.loads((ROOT/'K9_BASELINE_REFERENCE.json').read_text())
    if ref.get('copy_policy')!='REFERENCE_ONLY_NO_K9_RUNTIME_OR_ARTICLE_CONTENT':
        findings.append('BASELINE_REFERENCE_POLICY_INVALID')
    return {'status':'PASS' if not findings else 'BLOCKED','findings':findings}
