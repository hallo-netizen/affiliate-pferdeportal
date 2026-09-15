from __future__ import annotations

import html
import json
import re
import zipfile
from pathlib import Path
from typing import Any, Mapping

import production_checks

CONTRACT = 'SYSTEM4_AUTHORING_CONTRACT_V1'
STRUCTURE_MEMBER = 'portal-production-machine/contracts/content-structure-language-gate-v2.json'
TYPE_TEMPLATES_MEMBER = 'portal-production-machine/contracts/article-type-templates.json'
TYPE_EXTENSION_MANIFEST_MEMBER = 'portal-production-machine/contracts/article-type-extension-manifest-v1.json'
VALIDATOR_MEMBER = 'portal-production-machine/includes/content-validator.php'
STRUCTURE_GATE_MEMBER = 'portal-production-machine/includes/content-structure-language-gate.php'
STATIC_CONSTANTS = (
    'MIN_WORDS', 'MIN_PARAGRAPHS', 'MIN_H2', 'MIN_TABLE_BODY_ROWS',
    'MIN_FACT_PACK_COVERAGE_RATIO', 'MIN_TRACE_LEXICAL_SUPPORT_RATIO',
    'MAX_DUPLICATE_SENTENCE_RATIO', 'MAX_INTRO_PAIR_SIMILARITY',
)
FORBIDDEN_EXTERNAL_CONTROL_FIELDS = {
    'rules', 'ruleset', 'prompt', 'system_prompt', 'toolchain', 'workflow', 'route', 'next_state'
}

class AuthoringContractError(RuntimeError):
    pass

def _stable(value: Any) -> str:
    return production_checks.stable_hash(value)

def _type_class(article_type: str) -> str:
    value = article_type.strip().casefold().replace('ä','ae').replace('ö','oe').replace('ü','ue').replace('ß','ss')
    value = re.sub(r'[^a-z0-9]+','-',value).strip('-')
    if not value:
        raise AuthoringContractError('ARTICLE_TYPE_TOKEN_INVALID')
    return 'ppm-type-' + value

def _static_ppm_rules(package: Path) -> dict[str, Any]:
    try:
        with zipfile.ZipFile(package) as archive:
            structure = json.loads(archive.read(STRUCTURE_MEMBER).decode('utf-8'))
            validator = archive.read(VALIDATOR_MEMBER).decode('utf-8')
            structure_gate = archive.read(STRUCTURE_GATE_MEMBER).decode('utf-8')
    except Exception as exc:
        raise AuthoringContractError('PPM_AUTHORING_SOURCE_READ_FAILED') from exc
    if not isinstance(structure,dict) or structure.get('contract')!='content_structure_language_gate_v2':
        raise AuthoringContractError('PPM_STRUCTURE_CONTRACT_INVALID')
    constants={}
    for name in STATIC_CONSTANTS:
        m=re.search(r'const\s+'+re.escape(name)+r'\s*=\s*([^;]+);',validator)
        if not m:
            raise AuthoringContractError('PPM_CONSTANT_MISSING:'+name)
        raw=m.group(1).strip()
        if re.fullmatch(r'[0-9]+',raw): value=int(raw)
        elif re.fullmatch(r'[0-9]+\.[0-9]+',raw): value=float(raw)
        else: raise AuthoringContractError('PPM_CONSTANT_INVALID:'+name)
        constants[name.lower()]=value
    table_value_match=re.search(r'self::word_count\(\$statement\)\s*<\s*([0-9]+)',structure_gate)
    if not table_value_match:
        raise AuthoringContractError('PPM_TABLE_VALUE_MINIMUM_MISSING')
    source_trace_match=re.search(r'count\(\$trace_tags\)\s*<\s*([0-9]+)',validator)
    if not source_trace_match:
        raise AuthoringContractError('PPM_SOURCE_TRACE_MINIMUM_MISSING')
    return {'constants':constants,'structure':structure,'derived_binding_requirements':{'table_value_statement_minimum_words':int(table_value_match.group(1)),'source_trace_minimum':int(source_trace_match.group(1))}}

def _type_definition(package: Path, article_type: str) -> dict[str, Any]:
    try:
        with zipfile.ZipFile(package) as archive:
            templates=json.loads(archive.read(TYPE_TEMPLATES_MEMBER).decode('utf-8'))
            types=templates.get('types') if isinstance(templates,dict) else None
            if isinstance(types,dict) and isinstance(types.get(article_type),dict):
                return dict(types[article_type])
            manifest=json.loads(archive.read(TYPE_EXTENSION_MANIFEST_MEMBER).decode('utf-8'))
            extensions=manifest.get('extensions') if isinstance(manifest,dict) else None
            if isinstance(extensions,dict):
                for extension in extensions.values():
                    if not isinstance(extension,dict):
                        continue
                    aliases=extension.get('aliases') if isinstance(extension.get('aliases'),list) else []
                    if article_type not in aliases:
                        continue
                    caps=extension.get('ppm_capabilities') if isinstance(extension.get('ppm_capabilities'),dict) else {}
                    rel=str(caps.get('type_definition_contract') or '')
                    if not rel:
                        return {}
                    value=json.loads(archive.read('portal-production-machine/'+rel).decode('utf-8'))
                    definition=value.get('type_definition') if isinstance(value,dict) else None
                    return dict(definition) if isinstance(definition,dict) else {}
    except Exception as exc:
        raise AuthoringContractError('PPM_TYPE_SOURCE_READ_FAILED') from exc
    return {}

def build(repo: Path, state: Mapping[str,Any], fact_pack: Mapping[str,Any], plan: Mapping[str,Any]) -> dict[str,Any]:
    try: production_checks.validate_bound_context(state,fact_pack,plan)
    except production_checks.ProductionCheckError as exc: raise AuthoringContractError('BOUND_CONTEXT_INVALID:'+str(exc)) from exc
    package=(repo/production_checks.PPM_PACKAGE_REL).resolve()
    if not package.is_file() or production_checks.file_sha256(package)!=production_checks.PPM_PACKAGE_SHA256:
        raise AuthoringContractError('PPM_PACKAGE_HASH_MISMATCH')
    article=state.get('article')
    if not isinstance(article,Mapping): raise AuthoringContractError('ARTICLE_BINDING_MISSING')
    quality=plan.get('quality_binding')
    if not isinstance(quality,Mapping) or quality.get('contract')!='content_structure_language_binding_v2':
        raise AuthoringContractError('QUALITY_BINDING_MISSING')
    for scope_name,scope in (('plan',plan),('quality_binding',quality)):
        hit=sorted(FORBIDDEN_EXTERNAL_CONTROL_FIELDS.intersection(scope.keys()))
        if hit: raise AuthoringContractError('EXTERNAL_CONTROL_FIELD_BLOCKED:'+scope_name+':'+hit[0])
    declared=str(plan.get('quality_binding_hash') or '').lower().strip()
    if not re.fullmatch(r'[0-9a-f]{64}',declared) or declared!=_stable(dict(quality)):
        raise AuthoringContractError('QUALITY_BINDING_HASH_INVALID')
    article_type=str(article.get('article_type') or '')
    static=_static_ppm_rules(package); structure=static['structure']; type_def=_type_definition(package,article_type)
    marker=str(quality.get('internal_test_marker') or '').strip()
    marker_regex=str(structure.get('visible_test_marker_regex') or '')
    try: marker_valid=bool(marker and marker_regex and re.fullmatch(marker_regex,'['+marker+']'))
    except re.error as exc: raise AuthoringContractError('PPM_MARKER_REGEX_INVALID') from exc
    if not marker_valid: raise AuthoringContractError('INTERNAL_TEST_MARKER_INVALID')

    registry=quality.get('portal_link_registry')
    registry_hash=str(quality.get('portal_link_registry_hash') or '').lower().strip()
    if not isinstance(registry,Mapping) or not re.fullmatch(r'[0-9a-f]{64}',registry_hash) or registry_hash!=_stable(dict(registry)):
        raise AuthoringContractError('PORTAL_LINK_REGISTRY_HASH_INVALID')
    registry_entries=registry.get('entries') if isinstance(registry.get('entries'),list) else []

    raw_links=quality.get('link_bindings')
    if not isinstance(raw_links,list): raise AuthoringContractError('LINK_BINDINGS_MISSING')
    links=[]
    for i,raw in enumerate(raw_links):
        if not isinstance(raw,Mapping): raise AuthoringContractError(f'LINK_BINDING_INVALID:{i}')
        row={k:raw.get(k) for k in ('role','section_id','anchor','href','active','reason')}
        href=str(row.get('href') or '')
        if not href.startswith('/') or href.startswith('//') or re.match(r'^[a-z]+:',href,re.I): raise AuthoringContractError(f'LINK_TARGET_INVALID:{i}')
        links.append(row)
    link_cfg=structure.get('links') if isinstance(structure.get('links'),Mapping) else {}
    required_roles=[str(v) for v in link_cfg.get('required_roles',[]) if isinstance(v,str) and v]
    runtime=plan.get('runtime_order') if isinstance(plan.get('runtime_order'),Mapping) else {}
    runtime_links=runtime.get('links') if isinstance(runtime.get('links'),list) else []
    for role in required_roles:
        bound_rows=[r for r in links if str(r.get('role') or '')==role]
        runtime_rows=[r for r in runtime_links if isinstance(r,Mapping) and str(r.get('role') or '')==role]
        if len(bound_rows)!=1: raise AuthoringContractError('REQUIRED_LINK_ROLE_BINDING_INVALID:'+role)
        if len(runtime_rows)!=1: raise AuthoringContractError('RUNTIME_LINK_ROLE_BINDING_INVALID:'+role)
        row=bound_rows[0]
        matching_registry=[e for e in registry_entries if isinstance(e,Mapping) and str(e.get('href') or '')==str(row.get('href') or '')]
        if len(matching_registry)!=1: raise AuthoringContractError('LINK_REGISTRY_ENTRY_INVALID:'+role)
        reg=matching_registry[0]
        for field in ('role','href','anchor','reason','section_id'):
            if str(reg.get(field) or '')!=str(row.get(field) or ''): raise AuthoringContractError('LINK_REGISTRY_BINDING_MISMATCH:'+role+':'+field)
        runtime_row=runtime_rows[0]
        for field in ('role','href','anchor','reason','section_id'):
            if str(runtime_row.get(field) or '')!=str(row.get(field) or ''):
                raise AuthoringContractError('RUNTIME_LINK_BINDING_MISMATCH:'+role+':'+field)

    category=quality.get('wordpress_category')
    wp_cfg=structure.get('wordpress_binding') if isinstance(structure.get('wordpress_binding'),Mapping) else {}
    if not isinstance(category,Mapping): raise AuthoringContractError('WORDPRESS_CATEGORY_BINDING_INVALID')
    slug=str(category.get('slug') or '').strip().casefold(); name=str(category.get('name') or '').strip()
    forbidden={str(v).strip().casefold() for v in wp_cfg.get('forbidden_category_slugs',[]) if isinstance(v,str)}
    legacy_valid=int(category.get('id') or 0)>=int(wp_cfg.get('category_id_minimum') or 1) and bool(slug) and bool(name) and slug not in forbidden
    semantic_valid=bool(slug and name and str(category.get('hierarchy_path') or '').strip() and str(category.get('taxonomy') or '')=='category' and re.fullmatch(r'[a-f0-9]{64}',str(category.get('category_source_snapshot_hash') or '')) and category.get('semantic_binding_not_numeric_identity') is True and slug not in forbidden)
    if not (legacy_valid or semantic_valid): raise AuthoringContractError('WORDPRESS_CATEGORY_BINDING_INVALID')

    intent_terms=[str(v).strip() for v in quality.get('intent_terms',[]) if isinstance(v,str) and str(v).strip()]
    if int(static['constants'].get('min_h2') or 0)>len(structure.get('headings',{}).get('reserved_headings',[]) if isinstance(structure.get('headings'),Mapping) else []) and not intent_terms:
        raise AuthoringContractError('INTENT_TERMS_BINDING_MISSING')

    faq_answer=quality.get('faq_direct_answer') if article_type=='FAQ' else None
    if article_type=='FAQ':
        faq_cfg=structure.get('faq') if isinstance(structure.get('faq'),Mapping) else {}
        minimum=int(faq_cfg.get('direct_answer_minimum_words') or 0)
        answer=str(faq_answer or '').strip()
        if len(re.findall(r'\b[\wÄÖÜäöüß-]+\b',answer,re.UNICODE))<minimum: raise AuthoringContractError('FAQ_DIRECT_ANSWER_BINDING_INVALID')

    table_statement=str(quality.get('table_value_statement') or '').strip()
    table_min=int(static['derived_binding_requirements']['table_value_statement_minimum_words'])
    if len(re.findall(r'\b[\wÄÖÜäöüß-]+\b',table_statement,re.UNICODE))<table_min: raise AuthoringContractError('TABLE_VALUE_STATEMENT_BINDING_INVALID')
    required_runtime_fields=('order_id','article_type','title','slug','subject_scope','subject_label','lead','conclusion','links','allowed_fact_ids')
    for field in required_runtime_fields:
        value=runtime.get(field)
        if value is None or value=='' or value==[]:
            raise AuthoringContractError('RUNTIME_ORDER_INCOMPLETE:'+field)
    if str(runtime.get('article_type') or '')!=article_type:
        raise AuthoringContractError('RUNTIME_ORDER_ARTICLE_TYPE_MISMATCH')
    if str(runtime.get('title') or '')!=str(article.get('title') or ''):
        raise AuthoringContractError('RUNTIME_ORDER_TITLE_MISMATCH')
    if str(plan.get('source_snapshot_id') or '')!=str(fact_pack.get('source_snapshot_id') or ''):
        raise AuthoringContractError('PLAN_FACT_PACK_SNAPSHOT_MISMATCH')

    claims=fact_pack.get('claims') if isinstance(fact_pack.get('claims'),list) else []
    if len(claims)<3:
        raise AuthoringContractError('FACT_PACK_CLAIM_COUNT_INVALID')
    claim_map={}
    for i,claim in enumerate(claims):
        if not isinstance(claim,Mapping):
            raise AuthoringContractError(f'FACT_PACK_CLAIM_INVALID:{i}')
        fact_id=str(claim.get('fact_id') or '').strip()
        if not fact_id:
            raise AuthoringContractError(f'FACT_PACK_FACT_ID_MISSING:{i}')
        if fact_id in claim_map:
            raise AuthoringContractError('FACT_PACK_FACT_ID_DUPLICATE:'+fact_id)
        if str(claim.get('claim_status') or '')!='FULLY_SUPPORTED':
            raise AuthoringContractError('FACT_PACK_CLAIM_NOT_SUPPORTED:'+fact_id)
        claim_map[fact_id]=claim

    source_ids=set()
    sources=fact_pack.get('sources') if isinstance(fact_pack.get('sources'),list) else []
    for i,source in enumerate(sources):
        if not isinstance(source,Mapping):
            raise AuthoringContractError(f'FACT_PACK_SOURCE_INVALID:{i}')
        source_id=str(source.get('source_id') or '').strip()
        if not source_id:
            raise AuthoringContractError(f'FACT_PACK_SOURCE_ID_MISSING:{i}')
        if source_id in source_ids:
            raise AuthoringContractError('FACT_PACK_SOURCE_ID_DUPLICATE:'+source_id)
        source_ids.add(source_id)

    allowed_raw=runtime.get('allowed_fact_ids')
    if not isinstance(allowed_raw,list) or not allowed_raw:
        raise AuthoringContractError('RUNTIME_ALLOWED_FACT_IDS_MISSING')
    allowed_fact_ids=[]
    seen_allowed=set()
    for raw in allowed_raw:
        fact_id=str(raw or '').strip()
        if not fact_id:
            raise AuthoringContractError('RUNTIME_ALLOWED_FACT_ID_EMPTY')
        if fact_id in seen_allowed:
            raise AuthoringContractError('RUNTIME_ALLOWED_FACT_ID_DUPLICATE:'+fact_id)
        if fact_id not in claim_map:
            raise AuthoringContractError('RUNTIME_ALLOWED_FACT_ID_UNKNOWN:'+fact_id)
        seen_allowed.add(fact_id)
        allowed_fact_ids.append(fact_id)

    fact_authority={}
    for fact_id,claim in claim_map.items():
        source_id=str(claim.get('source_id') or '').strip()
        if source_id not in source_ids:
            raise AuthoringContractError('FACT_PACK_CLAIM_SOURCE_UNKNOWN:'+fact_id)
        fact_authority[fact_id]={
            'source_id':source_id,
            'trace_source_title':source_id,
            'evidence_text_sha256':str(claim.get('evidence_text_sha256') or '').lower().strip(),
            'claim_status':str(claim.get('claim_status') or ''),
            'article_types':[str(v) for v in (claim.get('article_types') if isinstance(claim.get('article_types'),list) else [])],
        }

    schema=type_def.get('type_meta_schema') if isinstance(type_def.get('type_meta_schema'),Mapping) else {}
    required_type_fields=schema.get('required') if isinstance(schema.get('required'),list) else []
    type_values={k:runtime.get(k) for k in required_type_fields if k in runtime}
    return {
      'contract':CONTRACT,
      'authority':{'source_mode':'READ_ONLY_BOUND_AUTHORITIES_ONLY','external_rule_injection_allowed':False,'ppm_version':production_checks.PPM_VERSION,'ppm_package_sha256':production_checks.PPM_PACKAGE_SHA256,'structure_contract_sha256':_stable(structure),'quality_binding_sha256':_stable(dict(quality))},
      'article_identity':{k:article.get(k) for k in ('title','target_keyword','category','article_type','plan_slot')},
      'global_requirements':static['constants'],
      'structure_requirements':structure,
      'type_requirements':{k:type_def.get(k) for k in ('table','table_count_exact','table_fact_trace_required','required_link_roles','visible_links_exact','fact_trace_required','all_factual_blocks_require_trace','title_contract','required_blocks','required_lists','fact_trace_required_blocks','conclusion_min_ratio','type_meta_schema','structure_profile','purpose','search_intent')},
      'bound_requirements':{'internal_test_marker':marker,'intent_terms':intent_terms,'faq_direct_answer':faq_answer,'table_value_statement':table_statement,'table_value_statement_minimum_words':table_min,'link_bindings':links,'required_link_roles':required_roles,'portal_link_registry_hash':registry_hash,'wordpress_category':dict(category),'type_bound_values':type_values,'allowed_fact_ids':allowed_fact_ids,'canonical_fact_ids':list(claim_map.keys()),'fact_authority':fact_authority,'source_trace_minimum':int(static['derived_binding_requirements']['source_trace_minimum']),'validation_contract_version':str(plan.get('validation_contract_version') or '')},
      'system4_guards':{'external_links_forbidden':True,'design':{'required_root_classes':['ppm-generated',_type_class(article_type)],'required_table_classes':['system-129-table','comparison-table'],'inline_style_forbidden':True,'active_html_forbidden':True,'beratung_only_h2_headings':article_type.casefold()=='beratung'}},
    }

def validate_bound(repo: Path, state: Mapping[str,Any]) -> dict[str,Any]:
    context=state.get('production_context'); stored=state.get('authoring_contract')
    if not isinstance(context,Mapping) or not isinstance(stored,Mapping): raise AuthoringContractError('AUTHORING_CONTRACT_MISSING')
    expected=build(repo,state,context['fact_pack'],context['production_plan_item'])
    if _stable(expected)!=_stable(dict(stored)): raise AuthoringContractError('AUTHORING_CONTRACT_AUTHORITY_MISMATCH')
    return expected

def _plain(value: str) -> str:
    return re.sub(r'\s+',' ',html.unescape(re.sub(r'(?is)<[^>]+>',' ',value))).strip()

def validate_candidate(article_html: str, contract: Mapping[str,Any]) -> dict[str,Any]:
    if contract.get('contract')!=CONTRACT: raise AuthoringContractError('PREWRITE_CONTRACT_INVALID')
    global_req=contract.get('global_requirements') if isinstance(contract.get('global_requirements'),Mapping) else {}
    structure=contract.get('structure_requirements') if isinstance(contract.get('structure_requirements'),Mapping) else {}
    type_req=contract.get('type_requirements') if isinstance(contract.get('type_requirements'),Mapping) else {}
    bound=contract.get('bound_requirements') if isinstance(contract.get('bound_requirements'),Mapping) else {}
    identity=contract.get('article_identity') if isinstance(contract.get('article_identity'),Mapping) else {}
    plain=_plain(article_html); words=len(re.findall(r'\b[\wÄÖÜäöüß-]+\b',plain,re.UNICODE)); paragraphs=len(re.findall(r'(?is)<p\b[^>]*>',article_html)); h2s=len(re.findall(r'(?is)<h2\b[^>]*>',article_html))
    for label,actual,key in (('WORD_FLOOR',words,'min_words'),('PARAGRAPH_FLOOR',paragraphs,'min_paragraphs'),('H2_FLOOR',h2s,'min_h2')):
        minimum=int(global_req.get(key) or 0)
        if actual<minimum: raise AuthoringContractError(f'PREWRITE_{label}:{actual}:{minimum}')
    if re.search(r'(?is)<h1\b',article_html): raise AuthoringContractError('PREWRITE_BODY_H1_FORBIDDEN')
    blocks={m.group(2):m.group(3) for m in re.finditer(r'(?is)<section\b[^>]*data-block\s*=\s*(["\'])([^"\']+)\1[^>]*>(.*?)</section>',article_html)}
    for name in (type_req.get('required_blocks') if isinstance(type_req.get('required_blocks'),list) else []):
        if name not in blocks: raise AuthoringContractError('PREWRITE_REQUIRED_BLOCK_MISSING:'+str(name))
    intro_cfg=structure.get('intro') if isinstance(structure.get('intro'),Mapping) else {}; intro_name=str(intro_cfg.get('required_block') or 'intro')
    if intro_name in blocks:
        intro=blocks[intro_name]; intro_plain=_plain(intro); iw=len(re.findall(r'\b[\wÄÖÜäöüß-]+\b',intro_plain,re.UNICODE)); lo=int(intro_cfg.get('minimum_words') or 0); hi=int(intro_cfg.get('maximum_words') or 10**9)
        if iw<lo or iw>hi: raise AuthoringContractError(f'PREWRITE_INTRO_WORD_RANGE:{iw}:{lo}:{hi}')
        if intro_cfg.get('heading_forbidden') and re.search(r'(?is)<h[1-6]\b',intro): raise AuthoringContractError('PREWRITE_INTRO_HEADING_FORBIDDEN')
        if str(intro_cfg.get('first_visible_element') or '')=='p' and not re.match(r'(?is)^\s*<p\b',intro): raise AuthoringContractError('PREWRITE_INTRO_MUST_START_WITH_P')
        direct=bound.get('faq_direct_answer')
        if isinstance(direct,str) and direct.strip() and str(identity.get('article_type') or '')=='FAQ' and not intro_plain.startswith(re.sub(r'\s+',' ',direct).strip()): raise AuthoringContractError('PREWRITE_FAQ_DIRECT_ANSWER_MISMATCH')
    tables=list(re.finditer(r'(?is)<table\b([^>]*)>(.*?)</table>',article_html)); exact_tables=int(type_req.get('table_count_exact') or 0)
    if exact_tables and len(tables)!=exact_tables: raise AuthoringContractError(f'PREWRITE_TABLE_COUNT:{len(tables)}:{exact_tables}')
    if tables:
        tbody=re.search(r'(?is)<tbody\b[^>]*>(.*?)</tbody>',tables[0].group(2)); rows=len(re.findall(r'(?is)<tr\b[^>]*>.*?</tr>',tbody.group(1))) if tbody else 0; min_rows=int(global_req.get('min_table_body_rows') or 0)
        if rows<min_rows: raise AuthoringContractError(f'PREWRITE_TABLE_ROW_FLOOR:{rows}:{min_rows}')
    links=[]
    for m in re.finditer(r'(?is)<a\b([^>]*)>(.*?)</a>',article_html):
        hm=re.search(r'(?is)\bhref\s*=\s*(["\'])(.*?)\1',m.group(1)); href=html.unescape(hm.group(2)).strip() if hm else ''; links.append((href,_plain(m.group(2))))
    link_cfg=structure.get('links') if isinstance(structure.get('links'),Mapping) else {}; expected_count=int(type_req.get('visible_links_exact') or link_cfg.get('required_count') or 0)
    if expected_count and len(links)!=expected_count: raise AuthoringContractError(f'PREWRITE_LINK_COUNT:{len(links)}:{expected_count}')
    for href,_ in links:
        if re.match(r'(?i)^(?:https?:)?//',href) or re.match(r'(?i)^[a-z][a-z0-9+.-]*:',href): raise AuthoringContractError('PREWRITE_EXTERNAL_LINK_FORBIDDEN')
    for row in (bound.get('link_bindings') if isinstance(bound.get('link_bindings'),list) else []):
        if isinstance(row,Mapping) and row.get('active') is not False and (str(row.get('href') or ''),str(row.get('anchor') or '')) not in links: raise AuthoringContractError('PREWRITE_BOUND_LINK_MISSING:'+str(row.get('role') or 'unknown'))

    heading_cfg=structure.get('headings') if isinstance(structure.get('headings'),Mapping) else {}
    def _ppm_normalize(text: str) -> str:
        value=_plain(text).casefold()
        value=re.sub(r'[^a-z0-9äöüß]+',' ',value)
        return re.sub(r'\s+',' ',value).strip()
    heading_rows=[]
    reserved={_ppm_normalize(str(v)) for v in heading_cfg.get('reserved_headings',[]) if isinstance(v,str)}
    generic={_ppm_normalize(str(v)) for v in heading_cfg.get('generic_or_technical_headings',[]) if isinstance(v,str)}
    forbidden=[_ppm_normalize(str(v)) for v in heading_cfg.get('forbidden_fragments',[]) if isinstance(v,str)]
    for m in re.finditer(r'(?is)<h([23])\b[^>]*>(.*?)</h\1>',article_html):
        label=_plain(m.group(2)); heading_rows.append((m.start(),m.end(),label))
        hw=len(re.findall(r"[\wÄÖÜäöüß]+(?:['’\-][\wÄÖÜäöüß]+)*",label,re.UNICODE))
        lo=int(heading_cfg.get('minimum_words') or 0); hi=int(heading_cfg.get('maximum_words') or 10**9)
        normalized=_ppm_normalize(label)
        if normalized not in reserved and (hw<lo or hw>hi): raise AuthoringContractError(f'PREWRITE_HEADING_WORD_RANGE:{hw}:{lo}:{hi}')
        if normalized in generic: raise AuthoringContractError('PREWRITE_GENERIC_HEADING:'+label)
        for fragment in forbidden:
            if fragment and fragment in normalized: raise AuthoringContractError('PREWRITE_HEADING_FORBIDDEN_FRAGMENT:'+fragment)
    min_between=int(heading_cfg.get('minimum_words_between_headings') or 0)
    if min_between and len(heading_rows)>1:
        for left,right in zip(heading_rows,heading_rows[1:]):
            between=_plain(article_html[left[1]:right[0]])
            between_words=len(re.findall(r'\b[\wÄÖÜäöüß-]+\b',between,re.UNICODE))
            if between_words<min_between: raise AuthoringContractError(f'PREWRITE_HEADING_DISTANCE:{between_words}:{min_between}')

    marker_regex=str(structure.get('visible_test_marker_regex') or '')
    if marker_regex:
        try:
            if re.search(marker_regex,str(identity.get('title') or '')) or re.search(marker_regex,article_html): raise AuthoringContractError('PREWRITE_VISIBLE_TEST_MARKER')
        except re.error as exc: raise AuthoringContractError('PREWRITE_MARKER_REGEX_INVALID') from exc

    allowed={str(v) for v in bound.get('allowed_fact_ids',[]) if isinstance(v,str)}
    canonical={str(v) for v in bound.get('canonical_fact_ids',[]) if isinstance(v,str)}
    authority=bound.get('fact_authority') if isinstance(bound.get('fact_authority'),Mapping) else {}
    used=set()
    is_v5=str(bound.get('validation_contract_version') or '')=='SECTION_REQUIREMENTS_V1'
    unit_tags='p|li|th|td' if is_v5 else 'p|li|td'
    for m in re.finditer(r'(?is)<('+unit_tags+r')\b([^>]*)>(.*?)</\1>',article_html):
        attrs=m.group(2); body=m.group(3); text=_plain(body)
        if not text: continue
        if re.search(r'(?is)\bclass\s*=\s*(["\'])[^"\']*\b(?:ppm|pm)-ai-disclosure\b[^"\']*\1',attrs): continue
        if not is_v5 and m.group(1).casefold()=='p' and re.search(r'(?is)<a\b',body): continue
        rm=re.search(r'(?is)\bdata-fact-ids\s*=\s*(["\'])(.*?)\1',attrs)
        refs=[v for v in re.split(r'\s+',html.unescape(rm.group(2)).strip()) if v] if rm else []
        if not refs and type_req.get('all_factual_blocks_require_trace') is True:
            raise AuthoringContractError('PREWRITE_FACT_REFS_MISSING')
        for fact_id in refs:
            if fact_id not in allowed or fact_id not in canonical:
                raise AuthoringContractError('PREWRITE_FACT_ID_UNKNOWN:'+fact_id)
            meta=authority.get(fact_id) if isinstance(authority.get(fact_id),Mapping) else {}
            if str(meta.get('claim_status') or '')!='FULLY_SUPPORTED':
                raise AuthoringContractError('PREWRITE_FACT_NOT_VERIFIED:'+fact_id)
            article_types=meta.get('article_types') if isinstance(meta.get('article_types'),list) else []
            if article_types and str(identity.get('article_type') or '') not in [str(v) for v in article_types]:
                raise AuthoringContractError('PREWRITE_FACT_TYPE_MISMATCH:'+fact_id)
            used.add(fact_id)
    if canonical:
        minimum_ratio=float(global_req.get('min_fact_pack_coverage_ratio') or 0)
        if len(used.intersection(canonical))/len(canonical)<minimum_ratio:
            raise AuthoringContractError('PREWRITE_FACT_PACK_COVERAGE')

    traces=[]
    for m in re.finditer(r'(?is)<span\b([^>]*)\bclass\s*=\s*(["\'])[^"\']*\bppm-source-trace\b[^"\']*\2[^>]*>',article_html):
        tag=m.group(0)
        def attr(name: str) -> str:
            am=re.search(r'(?is)\b'+re.escape(name)+r'\s*=\s*(["\'])(.*?)\1',tag)
            return html.unescape(am.group(2)).strip() if am else ''
        traces.append((attr('data-fact-id'),attr('data-source-title'),attr('data-source-hash').lower()))
    trace_min=int(bound.get('source_trace_minimum') or 0)
    if type_req.get('fact_trace_required') is True and len(traces)<trace_min:
        raise AuthoringContractError(f'PREWRITE_SOURCE_TRACE_COUNT:{len(traces)}:{trace_min}')
    for fact_id,title,source_hash in traces:
        if fact_id not in canonical:
            raise AuthoringContractError('PREWRITE_SOURCE_TRACE_FACT_UNKNOWN:'+fact_id)
        meta=authority.get(fact_id) if isinstance(authority.get(fact_id),Mapping) else {}
        if title!=str(meta.get('trace_source_title') or '') or source_hash!=str(meta.get('evidence_text_sha256') or '').lower():
            raise AuthoringContractError('PREWRITE_SOURCE_TRACE_MISMATCH:'+fact_id)

    return {'status':'PASS','word_count':words,'paragraph_count':paragraphs,'h2_count':h2s,'table_count':len(tables),'link_count':len(links),'source_trace_count':len(traces),'used_fact_count':len(used)}
