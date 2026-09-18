from __future__ import annotations

import hashlib
import html
import json
import re
from pathlib import Path
from typing import Any, Mapping

POLICY_CONTRACT='SYSTEM4_BLOCK_SEMANTIC_HEADING_POLICY_V1'
BINDING_CONTRACT='SYSTEM4_BOUND_BLOCK_SEMANTICS_V1'
POLICY_PATH=Path(__file__).resolve().with_name('block_semantics_v1.json')


class BlockSemanticError(RuntimeError):
    pass


class BlockSemanticRepairRequired(BlockSemanticError):
    def __init__(self, findings:list[dict[str,Any]]):
        self.findings=[dict(row) for row in findings]
        super().__init__('BLOCK_CONTENT_SEMANTIC_REPAIR_REQUIRED')


def _stable(value:Any)->str:
    payload=json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':'))
    return hashlib.sha256(payload.encode('utf-8')).hexdigest()


def _plain(value:str)->str:
    return re.sub(r'\s+',' ',html.unescape(re.sub(r'(?is)<[^>]+>',' ',value))).strip()


def normalize(value:str)->str:
    text=_plain(value).casefold()
    text=re.sub(r'[^a-z0-9äöüß]+',' ',text)
    return re.sub(r'\s+',' ',text).strip()


def _policy()->dict[str,Any]:
    try:
        value=json.loads(POLICY_PATH.read_text(encoding='utf-8'))
    except Exception as exc:
        raise BlockSemanticError('BLOCK_SEMANTIC_POLICY_READ_FAILED') from exc
    if not isinstance(value,dict) or value.get('contract')!=POLICY_CONTRACT:
        raise BlockSemanticError('BLOCK_SEMANTIC_POLICY_CONTRACT_INVALID')
    policies=value.get('block_policies')
    if not isinstance(policies,dict):
        raise BlockSemanticError('BLOCK_SEMANTIC_POLICY_BLOCKS_INVALID')
    return value


def bind(structure:Mapping[str,Any],type_definition:Mapping[str,Any])->dict[str,Any]:
    policy=_policy()
    required=[str(v) for v in (type_definition.get('required_blocks') if isinstance(type_definition.get('required_blocks'),list) else []) if str(v)]
    headings=structure.get('headings') if isinstance(structure.get('headings'),Mapping) else {}
    reserved={normalize(str(v)) for v in headings.get('reserved_headings',[]) if isinstance(v,str)}
    source=policy['block_policies']
    active={}
    for block_id in required:
        raw=source.get(block_id)
        if not isinstance(raw,Mapping):
            continue
        row=dict(raw)
        canonical=str(row.get('canonical_ppm_reserved_heading') or '').strip()
        markers=[str(v).strip() for v in row.get('accepted_heading_markers',[]) if isinstance(v,str) and str(v).strip()]
        if not canonical or normalize(canonical) not in reserved:
            raise BlockSemanticError('PPM_RESERVED_HEADING_BINDING_MISSING:'+block_id)
        if canonical not in markers:
            raise BlockSemanticError('BLOCK_SEMANTIC_CANONICAL_MARKER_MISSING:'+block_id)
        if not str(row.get('semantic_role') or '').strip() or not markers:
            raise BlockSemanticError('BLOCK_SEMANTIC_POLICY_INCOMPLETE:'+block_id)
        active[block_id]={
            'semantic_role':str(row['semantic_role']),
            'heading_required':bool(row.get('heading_required')),
            'canonical_ppm_reserved_heading':canonical,
            'accepted_heading_markers':markers,
        }
    return {
        'contract':BINDING_CONTRACT,
        'policy_contract':POLICY_CONTRACT,
        'policy_sha256':_stable(policy),
        'required_block_order':required,
        'semantic_blocks':active,
    }


def _finding(code:str,block_id:str,rule:str,expected:Any,actual:Any,reason:str)->dict[str,Any]:
    return {
        'error_code':code,
        'failed_rule':rule,
        'field':'content.blocks.'+block_id,
        'field_path':'content.blocks.'+block_id,
        'expected':expected,
        'actual':actual,
        'reason':reason,
        'repair_owner':'DRAFT_BODY',
        'repair_target':'SAME_ARTICLE_BODY',
    }


def collect_findings(article_html:str,authoring_contract:Mapping[str,Any])->list[dict[str,Any]]:
    binding=authoring_contract.get('block_semantics') if isinstance(authoring_contract.get('block_semantics'),Mapping) else {}
    if binding.get('contract')!=BINDING_CONTRACT:
        raise BlockSemanticError('BLOCK_SEMANTIC_BINDING_MISSING')
    required=[str(v) for v in binding.get('required_block_order',[]) if str(v)]
    semantic=binding.get('semantic_blocks') if isinstance(binding.get('semantic_blocks'),Mapping) else {}

    sections=[]
    for match in re.finditer(r'(?is)<section\b[^>]*data-block\s*=\s*(["\'])([^"\']+)\1[^>]*>(.*?)</section>',article_html):
        sections.append({'id':str(match.group(2)),'body':str(match.group(3))})
    actual=[row['id'] for row in sections]
    findings:list[dict[str,Any]]=[]

    seen=set()
    for block_id in actual:
        if block_id in seen:
            findings.append(_finding(
                'BLOCK_CONTENT_BLOCK_DUPLICATE',block_id,'REQUIRED_BLOCK_MUST_BE_UNIQUE',
                'exactly once','duplicate','A semantic article block occurs more than once.'
            ))
        seen.add(block_id)

    for block_id in required:
        if block_id not in actual:
            findings.append(_finding(
                'BLOCK_CONTENT_REQUIRED_BLOCK_ABSENT',block_id,'PPM_REQUIRED_BLOCK_MUST_EXIST',
                'present exactly once',False,'A PPM-required article block is absent.'
            ))

    if not any(row['error_code']=='BLOCK_CONTENT_REQUIRED_BLOCK_ABSENT' for row in findings):
        actual_required=[block_id for block_id in actual if block_id in required]
        if actual_required!=required:
            findings.append(_finding(
                'BLOCK_CONTENT_BLOCK_ORDER_INVALID','__order__','PPM_REQUIRED_BLOCK_RELATIVE_ORDER',
                required,actual_required,'PPM-required blocks are not in their bound relative order.'
            ))

    section_map={}
    for row in sections:
        section_map.setdefault(row['id'],row['body'])
    for block_id,raw in semantic.items():
        if block_id not in section_map or not isinstance(raw,Mapping):
            continue
        body=section_map[block_id]
        h2=list(re.finditer(r'(?is)<h2\b[^>]*>(.*?)</h2>',body))
        if bool(raw.get('heading_required')) and len(h2)!=1:
            findings.append(_finding(
                'BLOCK_CONTENT_SEMANTIC_HEADING_ABSENT',block_id,
                'SEMANTIC_BLOCK_REQUIRES_EXACTLY_ONE_H2',
                1,len(h2),'The semantic block needs exactly one visible H2 heading.'
            ))
            continue
        if not h2:
            continue
        heading=_plain(h2[0].group(1))
        normalized=normalize(heading)
        markers=[normalize(str(v)) for v in raw.get('accepted_heading_markers',[]) if isinstance(v,str) and str(v).strip()]
        matched=next((marker for marker in markers if normalized==marker or normalized.startswith(marker+' ')),None)
        if matched is None:
            findings.append(_finding(
                'BLOCK_CONTENT_SEMANTIC_HEADING_MISMATCH',block_id,
                'VISIBLE_HEADING_MUST_EXPRESS_BOUND_SEMANTIC_ROLE',
                {'semantic_role':str(raw.get('semantic_role') or ''),'accepted_heading_markers':list(raw.get('accepted_heading_markers') or [])},
                heading,'The visible H2 does not unambiguously express the semantic purpose of its block.'
            ))
    return findings


def validate(article_html:str,authoring_contract:Mapping[str,Any])->dict[str,Any]:
    findings=collect_findings(article_html,authoring_contract)
    if findings:
        raise BlockSemanticRepairRequired(findings)
    binding=authoring_contract['block_semantics']
    return {
        'status':'PASS',
        'contract':BINDING_CONTRACT,
        'required_block_order':list(binding.get('required_block_order') or []),
        'semantic_block_count':len(binding.get('semantic_blocks') or {}),
    }


def canonical_heading(authoring_contract:Mapping[str,Any],block_id:str)->str|None:
    binding=authoring_contract.get('block_semantics') if isinstance(authoring_contract.get('block_semantics'),Mapping) else {}
    semantic=binding.get('semantic_blocks') if isinstance(binding.get('semantic_blocks'),Mapping) else {}
    row=semantic.get(block_id)
    if not isinstance(row,Mapping):
        return None
    value=str(row.get('canonical_ppm_reserved_heading') or '').strip()
    return value or None
