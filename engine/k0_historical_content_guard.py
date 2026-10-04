from __future__ import annotations

import hashlib
import html
import json
import re
import sys
from pathlib import Path

CONTRACT = 'K0_HISTORICAL_CONTENT_GUARD_V1'
SHINGLE_WORDS = 18

class Blocked(RuntimeError):
    pass

def _plain(value):
    value = re.sub(r'(?is)<[^>]+>', ' ', str(value or ''))
    value = html.unescape(value)
    return re.sub(r'\s+', ' ', value).strip()

def _words(value):
    return re.findall(r'[\wÄÖÜäöüß-]+', _plain(value).casefold(), re.UNICODE)

def _shingles(words, width=SHINGLE_WORDS):
    if len(words) < width:
        return {}
    return {' '.join(words[i:i+width]): i for i in range(len(words)-width+1)}

def _stable_json(value):
    return hashlib.sha256(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')
    ).hexdigest()

def _is_exact_current_source_draft(path, package):
    if path.parent.name != 'writer_drafts' or path.suffix.casefold() != '.json':
        return False
    try:
        draft = json.loads(path.read_text(encoding='utf-8'))
    except Exception:
        return False
    provenance = package.get('writer_provenance') if isinstance(package, dict) else None
    if not isinstance(provenance, dict):
        return False
    return bool(
        draft.get('contract') == 'K0_WRITER_DRAFT_V1'
        and str(draft.get('job_id') or '') == str(provenance.get('job_id') or '')
        and _stable_json(draft) == str(provenance.get('draft_sha256') or '')
    )

def _json_texts(value, parent_key=''):
    if isinstance(value, dict):
        for k, v in value.items():
            key = str(k)
            if key in {'body', 'html', 'content_html', 'body_html'} and isinstance(v, str):
                yield v
            else:
                yield from _json_texts(v, key)
    elif isinstance(value, list):
        for v in value:
            yield from _json_texts(v, parent_key)

def _candidate_paths(root):
    seen = set()
    patterns = (
        'real_runs/k0/**/WORDPRESS_SINGLE.json',
        'real_runs/k0/**/WORDPRESS_BATCH.json',
        'real_runs/k0/**/SEALED_WRITER_PRODUCT.json',
        'real_runs/k0_batch/**/*.json',
        'recovery/**/*.md',
        'recovery/**/*.json',
        'writer_drafts/*.json',
    )
    for pattern in patterns:
        for p in root.glob(pattern):
            if p.is_file() and p not in seen:
                seen.add(p)
                yield p

def _historical_texts(path):
    if path.suffix.casefold() == '.md':
        yield path.read_text(encoding='utf-8', errors='ignore')
        return
    try:
        data = json.loads(path.read_text(encoding='utf-8'))
    except Exception:
        return
    yield from _json_texts(data)

def verify(package, current_run_dir, repo_root='.'):
    if not isinstance(package, dict) or package.get('contract') != 'K0_ARTICLE_PACKAGE_V1':
        raise Blocked('K0_HISTORICAL_GUARD_PACKAGE_INVALID')
    body = str(package.get('html') or '')
    words = _words(body)
    if len(words) < SHINGLE_WORDS:
        raise Blocked('K0_HISTORICAL_GUARD_BODY_TOO_SHORT')
    new_shingles = _shingles(words)

    root = Path(repo_root).resolve()
    current = (root / str(current_run_dir)).resolve()
    scanned = 0

    for path in _candidate_paths(root):
        if _is_exact_current_source_draft(path, package):
            continue
        rp = path.resolve()
        try:
            rp.relative_to(current)
            continue
        except ValueError:
            pass
        scanned += 1
        for old_text in _historical_texts(path):
            old_words = _words(old_text)
            if len(old_words) < SHINGLE_WORDS:
                continue
            old_set = set(_shingles(old_words))
            overlap = next((s for s in new_shingles if s in old_set), None)
            if overlap:
                rel = str(path.relative_to(root))
                raise Blocked('K0_HISTORICAL_TEXT_REUSE_BLOCKED:' + rel + ':' + overlap)

    return {
        'contract': CONTRACT,
        'status': 'PASS',
        'historical_text_reuse': 'NOT_DETECTED',
        'shingle_words': SHINGLE_WORDS,
        'scanned_historical_files': scanned,
        'publish_allowed': False,
    }

def main():
    if len(sys.argv) != 4:
        raise SystemExit('usage: k0_historical_content_guard.py SEALED_PACKAGE CURRENT_RUN_DIR OUT')
    try:
        package = json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
        out = verify(package, sys.argv[2], '.')
        Path(sys.argv[3]).write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
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
