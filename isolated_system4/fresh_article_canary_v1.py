#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import secrets
import sys
import time
import zipfile
from pathlib import Path
from typing import Any

import production_checks

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
SPEC = HERE / 'FRESH_ARTICLE_CANARY_V1.json'
CHALLENGE = 'SYSTEM4_FRESH_ARTICLE_CANARY_CHALLENGE_V1'
PROVENANCE = 'SYSTEM4_FRESH_WORKER_PROVENANCE_V1'


def sha_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(value, dict):
        raise RuntimeError('JSON_OBJECT_REQUIRED:' + path.name)
    return value


def fail(code: str) -> int:
    print('SYSTEM4_FRESH_ARTICLE_CANARY_BLOCKED:' + code)
    return 3


def prepare(workspace: Path) -> int:
    spec = load_json(SPEC)
    topic = spec['topic']
    title = str(topic['title'])
    forbidden = [str(v).casefold() for v in spec['forbidden_body_terms']]
    if any(token in title.casefold() for token in forbidden):
        return fail('CANARY_TOPIC_NOT_OFF_DOMAIN')
    workspace.mkdir(parents=True, exist_ok=True)
    for name in ('worker_provenance.json', 'research.json', 'facts.json', 'article.html'):
        p = workspace / name
        if p.exists():
            return fail('PREEXISTING_WORKER_OUTPUT:' + name)
    challenge = {
        'contract': CHALLENGE,
        'nonce': secrets.token_hex(24),
        'created_unix_ns': time.time_ns(),
        'git_head': os.popen('git -C ' + str(REPO) + ' rev-parse HEAD').read().strip(),
        'topic': topic,
        'required_outputs': ['worker_provenance.json', 'research.json', 'facts.json', 'article.html'],
        'prewritten_body_allowed': False,
        'publish_allowed': False,
    }
    (workspace / 'challenge.json').write_text(
        json.dumps(challenge, ensure_ascii=False, indent=2, sort_keys=True) + '\n', encoding='utf-8'
    )
    print('SYSTEM4_FRESH_ARTICLE_CANARY_PREPARED:' + challenge['nonce'])
    print('TOPIC:' + title)
    return 0


def _collect_ppm_candidate_hashes() -> set[str]:
    package = REPO / production_checks.PPM_PACKAGE_REL
    if not package.is_file() or production_checks.file_sha256(package) != production_checks.PPM_PACKAGE_SHA256:
        raise RuntimeError('PPM679_HASH_BOUND_PACKAGE_REQUIRED')
    hashes: set[str] = set()

    def walk(value: Any) -> None:
        if isinstance(value, dict):
            for key, child in value.items():
                if key in {'content_html', 'body_html', 'article_html', 'draft_markdown'} and isinstance(child, str) and child.strip():
                    hashes.add(sha_bytes(child.strip().encode('utf-8')))
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    with zipfile.ZipFile(package) as archive:
        for name in archive.namelist():
            if not name.lower().endswith('.json'):
                continue
            try:
                value = json.loads(archive.read(name).decode('utf-8'))
            except Exception:
                continue
            walk(value)
    return hashes


def verify(workspace: Path) -> int:
    spec = load_json(SPEC)
    challenge_path = workspace / 'challenge.json'
    if not challenge_path.is_file():
        return fail('CHALLENGE_MISSING')
    challenge = load_json(challenge_path)
    if challenge.get('contract') != CHALLENGE:
        return fail('CHALLENGE_CONTRACT_INVALID')

    required = [workspace / n for n in challenge.get('required_outputs', [])]
    missing = [p.name for p in required if not p.is_file()]
    if missing:
        return fail('LIVE_WORKER_OUTPUT_MISSING:' + ','.join(missing))

    provenance = load_json(workspace / 'worker_provenance.json')
    if provenance.get('contract') != PROVENANCE:
        return fail('WORKER_PROVENANCE_CONTRACT_INVALID')
    if provenance.get('challenge_nonce') != challenge.get('nonce'):
        return fail('WORKER_PROVENANCE_NONCE_MISMATCH')
    if provenance.get('generated_after_start_gate') is not True:
        return fail('WORKER_NOT_PROVEN_AFTER_START_GATE')
    if provenance.get('prewritten_fixture_used') is not False:
        return fail('PREWRITTEN_FIXTURE_USED')
    if provenance.get('generation_mode') != 'LIVE_WORKER_GENERATION':
        return fail('LIVE_WORKER_GENERATION_NOT_PROVEN')

    research = load_json(workspace / 'research.json')
    facts = load_json(workspace / 'facts.json')
    if research.get('contract') != 'SYSTEM4_RESEARCH_EVIDENCE_V1':
        return fail('RESEARCH_CONTRACT_INVALID')
    if facts.get('contract') != 'SYSTEM4_FACTS_EVIDENCE_V1':
        return fail('FACTS_CONTRACT_INVALID')

    body_path = workspace / 'article.html'
    body_raw = body_path.read_bytes()
    try:
        body = body_raw.decode('utf-8').strip()
    except UnicodeDecodeError:
        return fail('ARTICLE_NOT_UTF8')
    if not body:
        return fail('ARTICLE_EMPTY')

    body_sha = sha_bytes(body.encode('utf-8'))
    if provenance.get('article_sha256') != body_sha:
        return fail('WORKER_ARTICLE_HASH_MISMATCH')
    if body_sha in _collect_ppm_candidate_hashes():
        return fail('ARTICLE_MATCHES_PREEXISTING_PPM_CANDIDATE')

    forbidden_terms = [str(v) for v in spec['forbidden_body_terms']]
    body_cf = body.casefold()
    hits = [term for term in forbidden_terms if term.casefold() in body_cf]
    if hits:
        return fail('HORSE_DOMAIN_LEAK:' + ','.join(hits))

    required_topic_terms = ('badezimmerspiegel', 'duschen')
    if any(term not in body_cf for term in required_topic_terms):
        return fail('CANARY_TOPIC_NOT_REALIZED')

    combined_support = json.dumps({'research': research, 'facts': facts}, ensure_ascii=False).casefold()
    if 'badezimmerspiegel' not in combined_support and 'kondens' not in combined_support:
        return fail('CANARY_RESEARCH_NOT_TOPIC_BOUND')

    result = {
        'contract': 'SYSTEM4_FRESH_ARTICLE_CANARY_RESULT_V1',
        'status': 'PASS',
        'topic': spec['topic'],
        'article_sha256': body_sha,
        'article_bytes': len(body_raw),
        'preexisting_ppm_candidate_match': False,
        'horse_domain_leak': False,
        'live_worker_generation_proven': True,
        'publish_allowed': False,
        'next_state': spec['required_final_state'],
    }
    (workspace / 'canary_result.json').write_text(
        json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + '\n', encoding='utf-8'
    )
    print('SYSTEM4_FRESH_ARTICLE_CANARY_PASS:' + body_sha)
    return 0


def main(argv: list[str]) -> int:
    if len(argv) != 3 or argv[1] not in {'prepare', 'verify'}:
        print('USAGE: fresh_article_canary_v1.py prepare|verify WORKSPACE')
        return 2
    workspace = Path(argv[2]).resolve()
    if REPO.resolve() == workspace or REPO.resolve() in workspace.parents:
        return fail('WORKSPACE_INSIDE_REPOSITORY_FORBIDDEN')
    try:
        return prepare(workspace) if argv[1] == 'prepare' else verify(workspace)
    except Exception as exc:
        return fail(type(exc).__name__ + ':' + str(exc))


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
