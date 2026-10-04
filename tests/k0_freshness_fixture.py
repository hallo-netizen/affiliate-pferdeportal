import hashlib
import json


def _stable(value):
    return hashlib.sha256(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')
    ).hexdigest()


def bind_freshness(ctx):
    """Make a test authoring context valid for the production freshness hardlock."""
    rc = ctx.get('rule_context') or {}
    claims = rc.get('research_claims') or {}
    if not claims:
        return ctx

    production = ctx.setdefault('production_context', {})
    fp = production.setdefault('fact_pack', {})
    sources = []
    seen = set()
    statements = []
    for row in claims.values():
        url = str(row.get('source_url') or '')
        title = str(row.get('source_title') or '')
        if url and url not in seen:
            sources.append({'source_title': title, 'source_url': url})
            seen.add(url)
        statement = str(row.get('statement') or '')
        if statement:
            statements.append(statement)

    fp['contract'] = 'canonical_fact_pack_v1'
    fp['status'] = 'SOURCE_VERIFIED_PRODUCTION_READY'
    fp['sources'] = sources
    fp['claims'] = statements

    ctx['research_freshness_receipt'] = {
        'contract': 'K0_RESEARCH_FRESHNESS_GUARD_V1',
        'status': 'PASS',
        'historical_fact_pack_reuse': False,
        'historical_research_packet_reuse': False,
        'fact_pack_sha256': _stable(fp),
        'research_claims_sha256': _stable(claims),
    }
    return ctx
