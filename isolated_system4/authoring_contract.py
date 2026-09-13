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
    return {'constants':constants,'structure':structure}

def _type_definition(package: Path, article_type: str) -> dict[str, Any]:
    """Read existing static PPM type authority without executing PPM before fullcheck."""
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
    # Unknown/new types are not rejected by System 4; unchanged fullcheck authority decides later.
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
    raw_links=quality.get('link_bindings')
    if not isinstance(raw_links,list): raise AuthoringContractError('LINK_BINDINGS_MISSING')
    links=[]
    for i,raw in enumerate(raw_links):
        if not isinstance(raw,Mapping): raise AuthoringContractError(f'LINK_BINDING_INVALID:{i}')
        row={k:raw.get(k) for k in ('role','section_id','anchor','href','active')}
        href=str(row.get('href') or '')
        if not href.startswith('/') or href.startswith('//') or re.match(r'^[a-z]+:',href,re.I): raise AuthoringContractError(f'LINK_TARGET_INVALID:{i}')
        links.append(row)
    runtime=plan.get('runtime_order') if isinstance(plan.get('runtime_order'),Mapping) else {}
    schema=type_def.get('type_meta_schema') if isinstance(type_def.get('type_meta_schema'),Mapping) else {}
    required_type_fields=schema.get('required') if isinstance(schema.get('required'),list) else []
    type_values={k:runtime.get(k) for k in required_type_fields if k in runtime}
    allowed_fact_ids=runtime.get('allowed_fact_ids') if isinstance(runtime.get('allowed_fact_ids'),list) else [r.get('fact_id') for r in fact_pack.get('claims',[]) if isinstance(r,Mapping)]
    return {
      'contract':CONTRACT,
      'authority':{'source_mode':'READ_ONLY_BOUND_AUTHORITIES_ONLY','external_rule_injection_allowed':False,'ppm_version':production_checks.PPM_VERSION,'ppm_package_sha256':production_checks.PPM_PACKAGE_SHA256,'structure_contract_sha256':_stable(structure),'quality_binding_sha256':_stable(dict(quality))},
      'article_identity':{k:article.get(k) for k in ('title','target_keyword','category','article_type','plan_slot')},
      'global_requirements':static['constants'],
      'structure_requirements':structure,
      'type_requirements':{k:type_def.get(k) for k in ('table','table_count_exact','table_fact_trace_required','required_link_roles','visible_links_exact','fact_trace_required','all_factual_blocks_require_trace','title_contract','required_blocks','required_lists','fact_trace_required_blocks','conclusion_min_ratio','type_meta_schema','structure_profile','purpose','search_intent')},
      'bound_requirements':{'intent_terms':list(quality.get('intent_terms') or []),'faq_direct_answer':quality.get('faq_direct_answer') if article_type=='FAQ' else None,'table_value_statement':quality.get('table_value_statement'),'link_bindings':links,'type_bound_values':type_values,'allowed_fact_ids':allowed_fact_ids},
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

    # Only validate constraints already present in the bound, hash-checked authority bundle.
    heading_cfg=structure.get('headings') if isinstance(structure.get('headings'),Mapping) else {}
    heading_rows=[]
    for m in re.finditer(r'(?is)<h2\b[^>]*>(.*?)</h2>',article_html):
        label=_plain(m.group(1)); heading_rows.append((m.start(),m.end(),label))
        hw=len(re.findall(r'\b[\wÄÖÜäöüß-]+\b',label,re.UNICODE))
        lo=int(heading_cfg.get('minimum_words') or 0); hi=int(heading_cfg.get('maximum_words') or 10**9)
        if hw<lo or hw>hi: raise AuthoringContractError(f'PREWRITE_HEADING_WORD_RANGE:{hw}:{lo}:{hi}')
        folded=label.casefold()
        generic={str(v).casefold() for v in heading_cfg.get('generic_or_technical_headings',[]) if isinstance(v,str)}
        if folded in generic: raise AuthoringContractError('PREWRITE_GENERIC_HEADING:'+label)
        for fragment in heading_cfg.get('forbidden_fragments',[]) if isinstance(heading_cfg.get('forbidden_fragments'),list) else []:
            if isinstance(fragment,str) and fragment.casefold() in folded: raise AuthoringContractError('PREWRITE_HEADING_FORBIDDEN_FRAGMENT:'+fragment)
    min_between=int(heading_cfg.get('minimum_words_between_headings') or 0)
    if min_between and len(heading_rows)>1:
        for left,right in zip(heading_rows,heading_rows[1:]):
            between=_plain(article_html[left[1]:right[0]])
            between_words=len(re.findall(r'\b[\wÄÖÜäöüß-]+\b',between,re.UNICODE))
            if between_words<min_between: raise AuthoringContractError(f'PREWRITE_HEADING_DISTANCE:{between_words}:{min_between}')

    allowed={str(v) for v in bound.get('allowed_fact_ids',[]) if isinstance(v,str)}
    if allowed:
        for m in re.finditer(r'(?is)\bdata-fact-ids\s*=\s*(["\'])(.*?)\1',article_html):
            for fact_id in re.split(r'\s+',html.unescape(m.group(2)).strip()):
                if fact_id and fact_id not in allowed: raise AuthoringContractError('PREWRITE_FACT_ID_UNKNOWN:'+fact_id)

    return {'status':'PASS','word_count':words,'paragraph_count':paragraphs,'h2_count':h2s,'table_count':len(tables),'link_count':len(links)}
