from __future__ import annotations
import hashlib, json, os, re, sys
from pathlib import Path

from .k0_portal_resolver import validate_intake
from .writer_contract_guard import POLICY, inspect_html, stable, sha_text, verify_package
from .k0_product_property_research import ARTICLE_TYPE as PROPERTY_WINNER_TYPE, validate_packet as validate_property_packet, Blocked as PropertyResearchBlocked
from .k0_full_rules import writer_rule_bundle, validate_rule_context, rule_binding

JOB_CONTRACT='K0_WRITER_JOB_V1'
DRAFT_CONTRACT='K0_WRITER_DRAFT_V1'
PACKAGE_CONTRACT='K0_ARTICLE_PACKAGE_V1'
SEAL_CONTRACT='K0_WRITER_SEAL_V1'
AUTHORING_CONTEXT_CONTRACT='K0_AUTHORING_CONTEXT_V1'


# The existing research owner alone approves the original publication site.
# Official institutions/providers are intentionally curated, never inferred
# from arbitrary self-declared source labels, domains ending in .org, or blogs.
K0_OFFICIAL_SOURCE_HOSTS = frozenset({
    'horseware.com',             # official manufacturer
    'equiva.com',               # verified official equestrian retailer and own-brand source
    'simprax.com',              # verified official manufacturer of blanket impregnation
    'tierschutzbund.de',         # official animal-welfare association
    'dlg.org',                   # official agricultural association
    'worldhorsewelfare.org',     # official animal-welfare organisation
    'umweltbundesamt.de',        # German federal authority
    'tiho-hannover.de',          # veterinary university
    'vetmeduni.ac.at',          # veterinary university
    'msdvetmanual.com',        # official MSD Veterinary Manual
    'usask.ca',                 # University of Saskatchewan / WCVM
    'umn.edu',                  # University of Minnesota Extension, official university service
    'landwirtschaftskammer.de', # Official Landwirtschaftskammer Nordrhein-Westfalen
    'llh.hessen.de',           # Verified official Landesbetrieb Landwirtschaft Hessen (impressum 2026-11-24)
    'app.pferd-aktuell.de',   # Verified official Deutsche Reiterliche Vereinigung FN (official footer 2026-11-24)
    'lk-nienburg.de',          # Verified official Landkreis Nienburg government website (impressum 2026-11-21)
    'aelf-al.bayern.de',       # Official Bavarian agriculture and forestry authority AELF (verified 2026-11-21)
    'tierschutz.hessen.de',    # Official state Hesse animal-welfare portal
    'recht.nrw.de',           # Official North Rhine-Westphalia law portal
    'bauportal.nrw',          # Official North Rhine-Westphalia building portal
    'bundesfinanzhof.de',     # Official German Federal Fiscal Court
    'gesetze-im-internet.de', # Official German federal law text portal
    'huk.de',                # HUK-COBURG verified original first-party page of its Barmenia partnership (2026-11-26)
    'agila.de',                # Verified AGILA official animal insurer, dogs and cats only (2026-11-26)
    'allianz.de',              # Verified Allianz official equine insurance producer (2026-11-26)
    'allianz.com',             # Allianz SE original corporate publisher; verified imprint and 2026 statements (2026-11-26)
    'uelzener.de',             # Verified Uelzener official equine insurance producer (2026-11-26)
    'agriatierversicherung.de',# Verified Agria official equine insurance producer (2026-11-26)
    'test.de',                 # Verified official Stiftung Warentest original publisher (2026-11-26)
})
K0_OWN_PORTAL_SOURCE_HOSTS = frozenset({
    'pferde-atelier.de', 'hobbydepot.de', 'hab-und-bewahr.de',
})
# One verified association document is published from its own dedicated
# cloud bucket; never allow the whole shared hosting provider.
K0_OFFICIAL_HOSTED_PATHS = {
    'storage.googleapis.com': ('/worldhorsewelfare-cloud/',),
}
K0_GOVERNMENT_HOST_SUFFIXES = (
    '.gov', '.gov.uk', '.bund.de', '.europa.eu', '.gouv.fr',
    '.admin.ch', '.gov.au',
)


def _k0_research_source_quality_reason(url):
    """Return None only for an official original publisher or Wikipedia article.

    One source decision by the existing research owner, not a new workflow gate.
    Official new domains must be explicitly approved here after verification.
    """
    from urllib.parse import urlsplit

    try:
        p = urlsplit(str(url or '').strip())
        host = (p.hostname or '').lower().rstrip('.')
        port = p.port
    except ValueError:
        return 'RESEARCH_SOURCE_URL_INVALID'
    if (p.scheme != 'https' or not host or p.username or p.password
            or port not in (None, 443)):
        return 'RESEARCH_SOURCE_HTTPS_REQUIRED'
    if any(host == own or host.endswith('.' + own)
           for own in K0_OWN_PORTAL_SOURCE_HOSTS):
        return 'RESEARCH_OWN_PORTAL_SOURCE_FORBIDDEN'
    if host == 'wikipedia.org' or host.endswith('.wikipedia.org'):
        # Wikipedia encyclopedia articles are allowed; personal user pages,
        # discussion, search and administrative pages are not official sources.
        from urllib.parse import unquote
        wiki_path=unquote(p.path)
        if not wiki_path.startswith('/wiki/'):
            return 'RESEARCH_WIKIPEDIA_ARTICLE_REQUIRED'
        article=wiki_path[len('/wiki/'):].casefold()
        if not article or article.startswith((
                'benutzer:', 'benutzer_diskussion:', 'user:', 'user_talk:',
                'diskussion:', 'talk:', 'spezial:', 'special:',
                'wikipedia:', 'datei:', 'file:', 'vorlage:', 'template:',
                'kategorie:', 'category:', 'portal:')):
            return 'RESEARCH_WIKIPEDIA_ARTICLE_REQUIRED'
        return None
    if any(host == approved or host.endswith('.' + approved)
           for approved in K0_OFFICIAL_SOURCE_HOSTS):
        return None
    if any(host.endswith(suffix) and len(host) > len(suffix)
           for suffix in K0_GOVERNMENT_HOST_SUFFIXES):
        return None
    if any(p.path.startswith(prefix)
           for prefix in K0_OFFICIAL_HOSTED_PATHS.get(host, ())):
        return None
    return 'RESEARCH_SOURCE_NOT_APPROVED_OFFICIAL'

class Blocked(RuntimeError):
    pass

def _load(path):
    x=json.loads(Path(path).read_text(encoding='utf-8'))
    if not isinstance(x,dict):
        raise Blocked('JSON_OBJECT_REQUIRED:'+str(path))
    return x


def _k0_original_normalize(value):
    """Compare what the original source actually says, ignoring HTML punctuation."""
    import unicodedata
    return ' '.join(''.join(
        c if (c.isalnum() or c.isspace()) else ' '
        for c in unicodedata.normalize('NFKC', str(value or '')).casefold()
    ).split())


def _k0_fetch_original_source_text(url):
    """Read original HTTPS web content, not a claim or an assistant-made excerpt."""
    import ipaddress
    import shutil
    import socket
    import subprocess
    import urllib.parse
    import urllib.request
    from html.parser import HTMLParser

    class SourceReadError(RuntimeError):
        pass

    def safe_url(value):
        # Redirects must not quietly leave the approved official publisher.
        if _k0_research_source_quality_reason(value) is not None:
            raise SourceReadError('SOURCE_REDIRECT_NOT_APPROVED_OFFICIAL')
        p = urllib.parse.urlsplit(value)
        host = p.hostname
        if (p.scheme != 'https' or not host or p.username or p.password
                or p.port not in (None, 443) or host == 'localhost'
                or host.endswith(('.localhost', '.local', '.internal'))):
            raise SourceReadError('UNSAFE_SOURCE_URL')
        try:
            ipaddress.ip_address(host)
            raise SourceReadError('SOURCE_LITERAL_IP_DENIED')
        except ValueError:
            pass
        for item in socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM):
            if not ipaddress.ip_address(item[4][0]).is_global:
                raise SourceReadError('SOURCE_PRIVATE_IP_DENIED')
        return value

    class SafeRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            safe_url(newurl)
            return super().redirect_request(req, fp, code, msg, headers, newurl)

    class ReadableHTML(HTMLParser):
        def __init__(self):
            super().__init__(convert_charrefs=True)
            self.parts = []
            self.hidden = 0
        def handle_starttag(self, tag, attrs):
            if tag in ('script', 'style', 'noscript', 'svg'):
                self.hidden += 1
            if tag in ('br', 'p', 'div', 'li', 'td', 'h1', 'h2', 'h3'):
                self.parts.append(' ')
        def handle_endtag(self, tag):
            if tag in ('script', 'style', 'noscript', 'svg') and self.hidden:
                self.hidden -= 1
            self.parts.append(' ')
        def handle_data(self, data):
            if not self.hidden:
                self.parts.append(data)

    safe_url(url)
    opener = urllib.request.build_opener(SafeRedirect())
    request = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
        'Accept': 'text/html, text/plain, application/pdf, application/xhtml+xml',
        'Accept-Encoding': 'identity',
    })
    with opener.open(request, timeout=12) as response:
        if response.status != 200:
            raise SourceReadError('SOURCE_HTTP_NOT_OK')
        data = response.read(5_000_001)
        if len(data) > 5_000_000:
            raise SourceReadError('SOURCE_TOO_LARGE')
        mime = response.headers.get_content_type()
        charset = response.headers.get_content_charset() or 'utf-8'
    if mime == 'application/pdf' or data.startswith(b'%PDF'):
        if not shutil.which('pdftotext'):
            raise SourceReadError('PDF_TEXT_EXTRACTION_UNAVAILABLE')
        result = subprocess.run(
            ['pdftotext', '-layout', '-', '-'],
            input=data, capture_output=True, timeout=20, check=False,
        )
        if result.returncode != 0:
            raise SourceReadError('PDF_TEXT_EXTRACTION_FAILED')
        return result.stdout.decode('utf-8', errors='replace')
    if mime not in ('text/html', 'text/plain', 'text/xml', 'application/xml',
                    'application/xhtml+xml'):
        raise SourceReadError('SOURCE_FORMAT_NOT_READABLE')
    decoded = data.decode(charset, errors='replace')
    if mime == 'text/plain':
        return decoded
    parser = ReadableHTML()
    parser.feed(decoded)
    return ' '.join(parser.parts)


def research_owner_decision(context, identity, run_instance_id):
    """Single research-owner decision at existing K0 intake.

    A claim restated as its own evidence is not an independently recorded
    original-source excerpt.  Repair stays with the SAME research owner.
    """
    import hashlib
    import unicodedata

    claims=(context.get('rule_context') or {}).get('research_claims')
    if not isinstance(claims,dict):
        return None  # Existing schema owns missing/malformed claim objects.
    problems=[]
    require_original=os.environ.get('K0_REQUIRE_ORIGINAL_SOURCE_PROOF')=='1'
    original_cache={}
    source_quality_cache={}
    source_quality_reported=set()
    def check_source(url, fact_id):
        # Cached per original URL: one domain decision, even with many claims.
        if url not in source_quality_cache:
            source_quality_cache[url]=_k0_research_source_quality_reason(url)
        reason=source_quality_cache[url]
        if reason is not None and url not in source_quality_reported:
            problems.append({'fact_id':fact_id,'reason':reason,'source_url':url})
            source_quality_reported.add(url)
        return reason is None
    def normal(s):
        return ' '.join(unicodedata.normalize('NFKC',str(s or '')).casefold().split())
    for fact_id, claim in sorted(claims.items()):
        if not isinstance(claim,dict):
            continue
        excerpt=str(claim.get('evidence_text') or '')
        statement=str(claim.get('statement') or '')
        url=str(claim.get('source_url') or '').strip()
        if require_original and not check_source(url, str(fact_id)):
            continue
        if not excerpt.strip() or not statement.strip() or normal(excerpt)==normal(statement):
            problems.append({'fact_id':fact_id,'reason':'INDEPENDENT_ORIGINAL_SOURCE_EXCERPT_REQUIRED'})
        elif hashlib.sha256(excerpt.encode('utf-8')).hexdigest()!=str(claim.get('evidence_text_sha256') or ''):
            problems.append({'fact_id':fact_id,'reason':'SOURCE_EXCERPT_DIGEST_MISMATCH'})
        elif require_original:
            url=str(claim.get('source_url') or '').strip()
            try:
                if url not in original_cache:
                    original_cache[url]=_k0_original_normalize(_k0_fetch_original_source_text(url))
                original_text=original_cache[url]
            except Exception as exc:
                print('K0_ORIGINAL_SOURCE_FETCH_DIAGNOSTIC', type(exc).__name__, str(exc)[:180], file=sys.stderr)
                problems.append({'fact_id':fact_id,'reason':'ORIGINAL_SOURCE_NOT_RETRIEVABLE'})
                continue
            if not _k0_original_normalize(excerpt) in original_text:
                problems.append({'fact_id':fact_id,'reason':'ORIGINAL_SOURCE_EXCERPT_NOT_PROVEN'})
    if require_original:
        # The same research-owner decision covers all research inputs, not
        # only facts later quoted in the article.
        pc=context.get('production_context') or {}
        fact_pack=pc.get('fact_pack') or {}
        rc=context.get('rule_context') or {}
        extra_groups=(
            ('fact_pack', fact_pack.get('sources')),
            ('comparison', rc.get('comparison_source_bindings')),
            ('product', (pc.get('property_research') or {}).get('candidates')),
            ('winner', [(pc.get('property_research') or {}).get('winner')]),
        )
        for label, rows in extra_groups:
            if not isinstance(rows, list):
                continue
            for index, source in enumerate(rows):
                if isinstance(source, dict) and source:
                    check_source(str(source.get('source_url') or '').strip(),
                                 label + ':' + str(index))
    if not problems:
        return None
    return {
      'contract':'K0_RESEARCH_RETURN_V1',
      'status':'REPAIR_REQUIRED',
      'owner':'SAME_RESEARCH_OWNER',
      'identity':identity,
      'run_instance_id':run_instance_id,
      'return_to':'AUTHORING_CONTEXT.json',
      'issues':problems,
      'next_action':'RESEARCH_AGAIN_OR_PROVE_ORIGINAL_SOURCE_AND_RESUBMIT_SAME_RUN',
      'publish_allowed':False,
    }

def _job_core(intake, portal, ctx):
    rows=validate_intake(intake)
    if len(rows)!=1:
        raise Blocked('K0_WRITER_JOB_REQUIRES_ONE_ITEM')
    ident=rows[0]
    if portal.get('contract')!='K0_PORTAL_ASSIGNMENT_V1' or portal.get('status')!='PASS':
        raise Blocked('K0_WRITER_PORTAL_NOT_PASS')
    prows=portal.get('items') or []
    if len(prows)!=1 or prows[0].get('status')!='AUTO_DETECTED' or prows[0].get('job_identity')!=ident:
        raise Blocked('K0_WRITER_PORTAL_BINDING_INVALID')
    if ctx.get('contract')!=AUTHORING_CONTEXT_CONTRACT or ctx.get('publish_allowed') is not False:
        raise Blocked('K0_AUTHORING_CONTEXT_INVALID')
    run_instance_id=str(ctx.get('run_instance_id') or '')
    if not re.fullmatch(r'run:[0-9a-f]{24}',run_instance_id):
        raise Blocked('K0_AUTHORING_CONTEXT_RUN_INSTANCE_INVALID')
    if ctx.get('identity')!=ident:
        raise Blocked('K0_AUTHORING_CONTEXT_IDENTITY_MISMATCH')
    for forbidden in ('html','body','content_html','draft','article_text'):
        if forbidden in ctx:
            raise Blocked('K0_AUTHORING_CONTEXT_TEXT_PAYLOAD_FORBIDDEN:'+forbidden)
    cp=ctx.get('content_profile')
    if not isinstance(cp,dict) or not str(cp.get('search_intent') or ''):
        raise Blocked('K0_AUTHORING_CONTEXT_INTENT_MISSING')
    pc=ctx.get('production_context')
    if not isinstance(pc,dict) or not isinstance(pc.get('fact_pack'),dict) or not isinstance(pc.get('production_plan_item'),dict):
        raise Blocked('K0_AUTHORING_CONTEXT_RESEARCH_MISSING')
    research_return=research_owner_decision(ctx,ident,run_instance_id)
    if research_return is not None:
        return research_return
    if ident.get('article_type')==PROPERTY_WINNER_TYPE:
        try:
            property_result=validate_property_packet(ident,pc.get('property_research'))
        except PropertyResearchBlocked as exc:
            raise Blocked('K0_PROPERTY_RESEARCH_BLOCKED:'+str(exc)) from exc
        if str(cp.get('search_intent') or '')!=property_result.get('search_intent'):
            raise Blocked('K0_PROPERTY_RESEARCH_INTENT_MISMATCH')
    try:
        rule_context=validate_rule_context(ctx.get('rule_context'),ident)
        full_rule_bundle=writer_rule_bundle(ident.get('article_type'))
        full_rule_binding=rule_binding(full_rule_bundle)
    except Exception as exc:
        raise Blocked('K0_AUTHORING_FULL_RULE_CONTEXT_INVALID:'+str(exc)) from exc
    return {
      'contract':JOB_CONTRACT,
      'status':'OPEN',
      'identity':ident,
      'portal_id':prows[0]['portal_id'],
      'run_instance_id':run_instance_id,
      'content_profile':cp,
      'production_context':pc,
      'rule_context':rule_context,
      'writer_rule_bundle':full_rule_bundle,
      'writer_rule_binding':full_rule_binding,
      'writer_policy':POLICY,
      'writer_policy_sha256':stable(POLICY),
      'publish_allowed':False,
    }

def prepare(intake, portal, ctx):
    core=_job_core(intake,portal,ctx)
    if core.get('status')=='REPAIR_REQUIRED':
        return core
    job_seed=stable(core)
    job_id='k0w-'+job_seed[:24]
    core['job_id']=job_id
    core['job_sha256']=stable({k:v for k,v in core.items() if k!='job_sha256'})
    return core

def _draft_sha(draft):
    return stable(draft)

def conclusion_heading_repair_request(job, draft):
    """Return a failed Fazit heading to the SAME original writer job."""
    if job.get('contract')!=JOB_CONTRACT or job.get('status')!='OPEN' or job.get('publish_allowed') is not False:
        raise Blocked('K0_WRITER_JOB_INVALID')
    if job.get('job_sha256')!=stable({k:v for k,v in job.items() if k!='job_sha256'}):
        raise Blocked('K0_WRITER_JOB_HASH_INVALID')
    if draft.get('contract')!=DRAFT_CONTRACT or draft.get('job_id')!=job.get('job_id') or draft.get('publish_allowed') is not False:
        raise Blocked('K0_WRITER_DRAFT_JOB_MISMATCH')
    return {
      'contract':'K0_WRITER_REVISION_REQUEST_V1',
      'status':'RETURN_TO_SAME_WRITER',
      'job_id':job['job_id'],
      'writer_job_sha256':job['job_sha256'],
      'draft_sha256':_draft_sha(draft),
      'rule_id':'writer.conclusion_heading_exact',
      'reason':'WRITER_CONCLUSION_HEADING_INVALID',
      'required_heading':'Fazit',
      'instruction':'Rewrite the SAME draft: the conclusion section must have an exact visible <h2>Fazit</h2>. Preserve the original writer job, all other content, facts, links, identity and K0 rules. Resubmit the revised draft to the same original writer acceptance workflow.',
      'publish_allowed':False,
    }

def list_bridge_repair_request(job, draft):
    """Return the same draft to its writer when a list touches Fazit."""
    if job.get('contract')!=JOB_CONTRACT or job.get('status')!='OPEN' or job.get('publish_allowed') is not False:
        raise Blocked('K0_WRITER_JOB_INVALID')
    if job.get('job_sha256')!=stable({k:v for k,v in job.items() if k!='job_sha256'}):
        raise Blocked('K0_WRITER_JOB_HASH_INVALID')
    if draft.get('contract')!=DRAFT_CONTRACT or draft.get('job_id')!=job.get('job_id') or draft.get('publish_allowed') is not False:
        raise Blocked('K0_WRITER_DRAFT_JOB_MISMATCH')
    return {
      'contract':'K0_WRITER_REVISION_REQUEST_V1',
      'status':'RETURN_TO_SAME_WRITER',
      'job_id':job['job_id'],
      'writer_job_sha256':job['job_sha256'],
      'draft_sha256':_draft_sha(draft),
      'rule_id':'writer.list_before_fazit_bridge',
      'reason':'WRITER_LIST_BEFORE_FAZIT_BRIDGE_REQUIRED',
      'minimum_bridge_words':18,
      'instruction':'Rewrite the SAME draft: immediately after the final list before Fazit, add a meaningful, source-supported prose paragraph of at least 18 words ending with a complete sentence. Do not repeat the bullets as filler. Keep the original job, facts, links, title, category, article type, keyword and K0 rules. Respect the existing word and section limits, and resubmit this same draft to the original writer workflow.',
      'publish_allowed':False,
    }


def seal(job, draft):
    if job.get('contract')!=JOB_CONTRACT or job.get('status')!='OPEN' or job.get('publish_allowed') is not False:
        raise Blocked('K0_WRITER_JOB_INVALID')
    expected_job_sha=stable({k:v for k,v in job.items() if k!='job_sha256'})
    if job.get('job_sha256')!=expected_job_sha:
        raise Blocked('K0_WRITER_JOB_HASH_INVALID')
    if job.get('writer_policy_sha256')!=stable(POLICY) or job.get('writer_policy')!=POLICY:
        raise Blocked('K0_WRITER_POLICY_DRIFT')
    try:
        current_bundle=writer_rule_bundle(job.get('identity',{}).get('article_type'))
        current_binding=rule_binding(current_bundle)
    except Exception as exc:
        raise Blocked('K0_WRITER_FULL_RULE_BUNDLE_INVALID:'+str(exc)) from exc
    if job.get('writer_rule_bundle')!=current_bundle or job.get('writer_rule_binding')!=current_binding:
        raise Blocked('K0_WRITER_FULL_RULE_BUNDLE_DRIFT')
    if validate_rule_context(job.get('rule_context'),job.get('identity') or {})!=job.get('rule_context'):
        raise Blocked('K0_WRITER_RULE_CONTEXT_DRIFT')

    allowed={'contract','job_id','title','content_html','table_decision','lt_authoritative_terms','revision_count','publish_allowed'}
    if set(draft)-allowed:
        raise Blocked('K0_WRITER_DRAFT_FIELDS_INVALID:'+','.join(sorted(set(draft)-allowed)))
    if draft.get('contract')!=DRAFT_CONTRACT or draft.get('job_id')!=job.get('job_id'):
        raise Blocked('K0_WRITER_DRAFT_JOB_MISMATCH')
    if draft.get('publish_allowed') is not False:
        raise Blocked('K0_WRITER_DRAFT_PUBLISH_INVALID')
    ident=job['identity']
    if str(draft.get('title') or '')!=ident['title']:
        raise Blocked('K0_WRITER_DRAFT_TITLE_MISMATCH')
    body=str(draft.get('content_html') or '')
    metrics=inspect_html(body)

    table=draft.get('table_decision')
    if not isinstance(table,dict):
        raise Blocked('K0_WRITER_DRAFT_TABLE_DECISION_MISSING')
    if table!=job.get('rule_context',{}).get('table_decision'):
        raise Blocked('K0_WRITER_DRAFT_TABLE_DECISION_NOT_PREBOUND')
    terms=draft.get('lt_authoritative_terms')
    if not isinstance(terms,list):
        raise Blocked('K0_WRITER_DRAFT_LT_TERMS_INVALID')

    core={
      'contract':SEAL_CONTRACT,
      'status':'PASS',
      'route':'K0_WRITER_DRAFT_ONLY',
      'job_id':job['job_id'],
      'job_sha256':job['job_sha256'],
      'draft_sha256':_draft_sha(draft),
      'identity_sha256':stable(ident),
      'visible_text_sha256':sha_text(_plain_for_seal(body)),
      'section_structure_sha256':stable(metrics['normal_h2_sections']),
      'policy_sha256':metrics['policy_sha256'],
      'full_rule_bundle_sha256':job['writer_rule_binding']['bundle_sha256'],
      'full_rule_catalog_sha256':job['writer_rule_binding']['catalog_sha256'],
      'full_rule_values_sha256':job['writer_rule_binding']['rule_values_sha256'],
      'full_rule_hard_count':job['writer_rule_binding']['article_hard_rule_count'],
      'total_words':metrics['total_words'],
      'conclusion_ratio':round(metrics['conclusion_ratio'],6),
      'section_balance_status':'PASS',
      'conclusion_status':'PASS',
      'further_information_status':'PASS',
      'publish_allowed':False,
    }
    provenance={**core,'seal_sha256':stable(core)}
    out={
      'contract':PACKAGE_CONTRACT,
      'identity':ident,
      'html':body,
      'final_draft_sha256':sha_text(body),
      'content_profile':job['content_profile'],
      'rule_context':job['rule_context'],
      'writer_rule_binding':job['writer_rule_binding'],
      'table_decision':table,
      'lt_authoritative_terms':terms,
      'production_context':job['production_context'],
      'revision_count':int(draft.get('revision_count') or 1),
      'writer_provenance':provenance,
      'publish_allowed':False,
    }
    verify(job,out)
    return out

def _plain_for_seal(value):
    import html as htmlmod
    value=re.sub(r'(?is)<[^>]+>',' ',str(value or ''))
    value=htmlmod.unescape(value)
    return re.sub(r'\s+',' ',value).strip()

def verify(job, package):
    if job.get('contract')!=JOB_CONTRACT:
        raise Blocked('K0_WRITER_JOB_CONTRACT_INVALID')
    expected_job_sha=stable({k:v for k,v in job.items() if k!='job_sha256'})
    if job.get('job_sha256')!=expected_job_sha:
        raise Blocked('K0_WRITER_JOB_HASH_INVALID')
    if package.get('contract')!=PACKAGE_CONTRACT or package.get('publish_allowed') is not False:
        raise Blocked('K0_WRITER_PACKAGE_INVALID')
    if package.get('identity')!=job.get('identity'):
        raise Blocked('K0_WRITER_PACKAGE_IDENTITY_MISMATCH')
    if package.get('content_profile')!=job.get('content_profile'):
        raise Blocked('K0_WRITER_PACKAGE_INTENT_MISMATCH')
    if package.get('production_context')!=job.get('production_context'):
        raise Blocked('K0_WRITER_PACKAGE_CONTEXT_MISMATCH')
    if package.get('rule_context')!=job.get('rule_context'):
        raise Blocked('K0_WRITER_PACKAGE_RULE_CONTEXT_MISMATCH')
    if package.get('writer_rule_binding')!=job.get('writer_rule_binding'):
        raise Blocked('K0_WRITER_PACKAGE_FULL_RULE_BINDING_MISMATCH')
    prov=package.get('writer_provenance') or {}
    if prov.get('job_id')!=job.get('job_id') or prov.get('job_sha256')!=job.get('job_sha256'):
        raise Blocked('K0_WRITER_PACKAGE_JOB_BINDING_INVALID')
    if prov.get('identity_sha256')!=stable(job['identity']):
        raise Blocked('K0_WRITER_PACKAGE_IDENTITY_HASH_INVALID')
    if prov.get('full_rule_bundle_sha256')!=job['writer_rule_binding']['bundle_sha256'] or prov.get('full_rule_hard_count')!=job['writer_rule_binding']['article_hard_rule_count']:
        raise Blocked('K0_WRITER_PACKAGE_FULL_RULE_PROVENANCE_INVALID')
    metrics=verify_package(package)
    return {
      'contract':'K0_WRITER_SEAL_VERIFY_V1',
      'status':'PASS',
      'job_id':job['job_id'],
      'job_sha256':job['job_sha256'],
      'policy_sha256':metrics['policy_sha256'],
      'total_words':metrics['total_words'],
      'conclusion_ratio':metrics['conclusion_ratio'],
      'publish_allowed':False,
    }

def main():
    try:
        if len(sys.argv)==6 and sys.argv[1]=='prepare':
            out=prepare(_load(sys.argv[2]),_load(sys.argv[3]),_load(sys.argv[4]))
            Path(sys.argv[5]).write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
            if out.get('status')=='REPAIR_REQUIRED':
                print(json.dumps({'contract':out['contract'],'status':'REPAIR_REQUIRED','owner':out['owner'],'issues':out['issues'],'publish_allowed':False},ensure_ascii=False))
            else:
                print(json.dumps({'contract':JOB_CONTRACT,'status':'PASS','job_id':out['job_id'],'job_sha256':out['job_sha256'],'publish_allowed':False},ensure_ascii=False))
            return
        if len(sys.argv)==5 and sys.argv[1]=='seal':
            out=seal(_load(sys.argv[2]),_load(sys.argv[3]))
            Path(sys.argv[4]).write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
            print(json.dumps({'contract':SEAL_CONTRACT,'status':'PASS','job_id':out['writer_provenance']['job_id'],'seal_sha256':out['writer_provenance']['seal_sha256'],'publish_allowed':False},ensure_ascii=False))
            return
        if len(sys.argv)==4 and sys.argv[1]=='verify':
            out=verify(_load(sys.argv[2]),_load(sys.argv[3]))
            print(json.dumps(out,ensure_ascii=False))
            return
        raise Blocked('K0_WRITER_STATION_USAGE_INVALID')
    except Exception as exc:
        print(json.dumps({'contract':'K0_WRITER_STATION_V1','status':'BLOCKED','reason':str(exc),'publish_allowed':False},ensure_ascii=False))
        raise SystemExit(2)

if __name__=='__main__':
    main()
