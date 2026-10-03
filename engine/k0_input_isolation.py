from __future__ import annotations

import hashlib
import json
from urllib.parse import urlparse

CONTRACT = 'K0_FRESH_INPUT_ISOLATION_V1'

BLOCKED_RESEARCH_HOSTS = {
    'github.com',
    'www.github.com',
    'raw.githubusercontent.com',
    'api.github.com',
    'pferde-atelier.de',
    'www.pferde-atelier.de',
}

BLOCKED_HISTORY_TOKENS = (
    'real_runs/k0/',
    'real_runs/k0_batch/',
    'recovery/',
    'archive/',
    'writer_drafts/',
    'WORDPRESS_SINGLE.json',
    'WORDPRESS_BATCH.json',
    'SEALED_WRITER_PRODUCT.json',
)

class Blocked(RuntimeError):
    pass

def _stable(value):
    return hashlib.sha256(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')
    ).hexdigest()

def _walk_strings(value):
    if isinstance(value, dict):
        for v in value.values():
            yield from _walk_strings(v)
    elif isinstance(value, list):
        for v in value:
            yield from _walk_strings(v)
    elif isinstance(value, str):
        yield value

def _source_urls(payload):
    pc = payload.get('production_context')
    if not isinstance(pc, dict):
        raise Blocked('K0_INPUT_ISOLATION_PRODUCTION_CONTEXT_MISSING')
    fp = pc.get('fact_pack')
    if not isinstance(fp, dict):
        raise Blocked('K0_INPUT_ISOLATION_FACT_PACK_MISSING')
    sources = fp.get('sources')
    if not isinstance(sources, list) or not sources:
        raise Blocked('K0_INPUT_ISOLATION_FRESH_RESEARCH_SOURCES_MISSING')
    urls = []
    for row in sources:
        if not isinstance(row, dict):
            raise Blocked('K0_INPUT_ISOLATION_SOURCE_INVALID')
        url = str(row.get('source_url') or '').strip()
        parsed = urlparse(url)
        if parsed.scheme not in {'http', 'https'} or not parsed.netloc:
            raise Blocked('K0_INPUT_ISOLATION_SOURCE_URL_INVALID:' + url)
        host = (parsed.hostname or '').casefold()
        if host in BLOCKED_RESEARCH_HOSTS:
            raise Blocked('K0_INPUT_ISOLATION_HISTORICAL_OR_PORTAL_SOURCE_FORBIDDEN:' + host)
        urls.append(url)
    if len(set(urls)) != len(urls):
        raise Blocked('K0_INPUT_ISOLATION_DUPLICATE_RESEARCH_SOURCE')
    return urls

def validate(payload, run_instance_id):
    if not isinstance(payload, dict):
        raise Blocked('K0_INPUT_ISOLATION_CONTEXT_INVALID')
    run_instance_id = str(run_instance_id or '')
    if not run_instance_id.startswith('run:') or len(run_instance_id) != 28:
        raise Blocked('K0_INPUT_ISOLATION_RUN_INSTANCE_INVALID')

    for text in _walk_strings(payload):
        normalized = text.replace('\\', '/')
        for token in BLOCKED_HISTORY_TOKENS:
            if token in normalized:
                raise Blocked('K0_INPUT_ISOLATION_HISTORY_REFERENCE_FORBIDDEN:' + token)

    urls = _source_urls(payload)
    allowed = set(urls)

    rule_context = payload.get('rule_context')
    if not isinstance(rule_context, dict):
        raise Blocked('K0_INPUT_ISOLATION_RULE_CONTEXT_MISSING')
    claims = rule_context.get('research_claims')
    if not isinstance(claims, dict) or not claims:
        raise Blocked('K0_INPUT_ISOLATION_RESEARCH_CLAIMS_MISSING')
    for fact_id, row in claims.items():
        if not isinstance(row, dict):
            raise Blocked('K0_INPUT_ISOLATION_RESEARCH_CLAIM_INVALID:' + str(fact_id))
        url = str(row.get('source_url') or '').strip()
        if url not in allowed:
            raise Blocked('K0_INPUT_ISOLATION_CLAIM_SOURCE_NOT_IN_FRESH_FACT_PACK:' + str(fact_id))

    pc = payload['production_context']
    fp = pc['fact_pack']
    receipt = {
        'contract': CONTRACT,
        'status': 'PASS',
        'run_instance_id': run_instance_id,
        'current_upload_identity_authority': True,
        'fresh_external_research_only': True,
        'historical_article_content_allowed': False,
        'historical_writer_draft_allowed': False,
        'historical_fact_pack_allowed': False,
        'historical_research_packet_allowed': False,
        'historical_repair_text_allowed': False,
        'historical_run_output_allowed': False,
        'live_portal_content_as_research_allowed': False,
        'current_k0_rules_allowed': True,
        'live_category_and_internal_link_binding_allowed': True,
        'fact_pack_sha256': _stable(fp),
        'research_claims_sha256': _stable(claims),
        'research_source_urls_sha256': _stable(sorted(urls)),
        'publish_allowed': False,
    }
    return receipt
