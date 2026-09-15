from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path
from typing import Any, Mapping

import production_checks

CONTRACT='SYSTEM4_FRESH_GENERATION_PROOF_V1'
FORBIDDEN_ACCEPTANCE_SOURCE_TOKENS=(
    'full_local_acceptance',
    'build_fixture(',
    'g9-single-faq-approved-candidate-v1.json',
    'recovery_sources',
    'legacy.build_fixture',
)
G9_MEMBER='portal-production-machine/contracts/g9-single-faq-approved-candidate-v1.json'

class AcceptanceParityError(RuntimeError):
    pass

def _canon(value: Any) -> bytes:
    return json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')

def _sha_text(value: str) -> str:
    return hashlib.sha256(value.encode('utf-8')).hexdigest()

def reject_forbidden_acceptance_source(source_text: str) -> None:
    folded=source_text.casefold()
    for token in FORBIDDEN_ACCEPTANCE_SOURCE_TOKENS:
        if token.casefold() in folded:
            raise AcceptanceParityError('ACCEPTANCE_PREBUILT_ARTICLE_PATH_FORBIDDEN:'+token)

def verify_acceptance_sources(repo: Path) -> None:
    for rel in (
        '.github/workflows/system4-chat-output-acceptance.yml',
        'isolated_system4/test_local_end_to_end_chat_handoff.py',
    ):
        path=Path(repo)/rel
        if not path.is_file():
            raise AcceptanceParityError('ACCEPTANCE_SOURCE_MISSING:'+rel)
        reject_forbidden_acceptance_source(path.read_text(encoding='utf-8'))

def verify_pre_author_state(state: Mapping[str,Any]) -> None:
    if state.get('phase')!='DRAFT_REQUIRED':
        raise AcceptanceParityError('FRESH_AUTHOR_DRAFT_PHASE_REQUIRED')
    if state.get('draft_markdown') is not None or state.get('draft_sha256') is not None:
        raise AcceptanceParityError('FRESH_AUTHOR_PREBUILT_DRAFT_FORBIDDEN')
    if int(state.get('revision') or 0)!=0:
        raise AcceptanceParityError('FRESH_AUTHOR_PREEXISTING_REVISION_FORBIDDEN')
    if not isinstance(state.get('research'),Mapping) or not isinstance(state.get('facts'),Mapping):
        raise AcceptanceParityError('FRESH_AUTHOR_EVIDENCE_REQUIRED')
    if not isinstance(state.get('production_context'),Mapping) or not isinstance(state.get('authoring_contract'),Mapping):
        raise AcceptanceParityError('FRESH_AUTHOR_CONTEXT_REQUIRED')

def _known_prebuilt_article_hashes(repo: Path) -> set[str]:
    hashes:set[str]=set()
    ppm=Path(repo)/production_checks.PPM_PACKAGE_REL
    if not ppm.is_file() or production_checks.file_sha256(ppm)!=production_checks.PPM_PACKAGE_SHA256:
        raise AcceptanceParityError('FRESH_AUTHOR_PPM_PACKAGE_IDENTITY_INVALID')
    try:
        with zipfile.ZipFile(ppm) as zf:
            g9=json.loads(zf.read(G9_MEMBER).decode('utf-8'))
    except Exception as exc:
        raise AcceptanceParityError('FRESH_AUTHOR_G9_IDENTITY_READ_FAILED') from exc
    candidate=g9.get('candidate') if isinstance(g9,dict) else None
    body=candidate.get('content_html') if isinstance(candidate,dict) else None
    if isinstance(body,str) and body:
        hashes.add(_sha_text(body))
    recovery=Path(repo)/'control/startmaster0107/recovery_sources'
    if recovery.is_dir():
        for path in recovery.rglob('ARTICLE_*.md'):
            try:
                text=path.read_text(encoding='utf-8').strip()
            except Exception:
                continue
            if text:
                hashes.add(_sha_text(text))
    return hashes

def build_fresh_generation_receipt(repo: Path,state: Mapping[str,Any],body: str) -> dict[str,Any]:
    verify_pre_author_state(state)
    if not isinstance(body,str) or not body.strip():
        raise AcceptanceParityError('FRESH_AUTHOR_BODY_REQUIRED')
    body_sha=_sha_text(body)
    if body_sha in _known_prebuilt_article_hashes(Path(repo)):
        raise AcceptanceParityError('FRESH_AUTHOR_BODY_MATCHES_PREBUILT_ARTICLE')
    research=state['research'];facts=state['facts'];contract=state['authoring_contract']
    receipt={
        'contract':CONTRACT,
        'generator':'NO_CODEX_FRESH_AUTHOR_V1',
        'generated_in_current_run':True,
        'prebuilt_article_input_used':False,
        'research_sha256':str(research.get('sha256') or ''),
        'facts_sha256':str(facts.get('sha256') or ''),
        'authoring_contract_sha256':hashlib.sha256(_canon(contract)).hexdigest(),
        'body_sha256':body_sha,
    }
    receipt['receipt_sha256']=hashlib.sha256(_canon(receipt)).hexdigest()
    return receipt

def verify_fresh_generation_receipt(state: Mapping[str,Any],body: str,receipt: Mapping[str,Any]) -> None:
    if receipt.get('contract')!=CONTRACT or receipt.get('generator')!='NO_CODEX_FRESH_AUTHOR_V1':
        raise AcceptanceParityError('FRESH_AUTHOR_RECEIPT_IDENTITY_INVALID')
    if receipt.get('generated_in_current_run') is not True or receipt.get('prebuilt_article_input_used') is not False:
        raise AcceptanceParityError('FRESH_AUTHOR_RECEIPT_PROVENANCE_INVALID')
    if receipt.get('body_sha256')!=_sha_text(body):
        raise AcceptanceParityError('FRESH_AUTHOR_RECEIPT_BODY_MISMATCH')
    expected=dict(receipt); actual=expected.pop('receipt_sha256',None)
    if actual!=hashlib.sha256(_canon(expected)).hexdigest():
        raise AcceptanceParityError('FRESH_AUTHOR_RECEIPT_HASH_INVALID')
    if receipt.get('research_sha256')!=str((state.get('research') or {}).get('sha256') or ''):
        raise AcceptanceParityError('FRESH_AUTHOR_RECEIPT_RESEARCH_MISMATCH')
    if receipt.get('facts_sha256')!=str((state.get('facts') or {}).get('sha256') or ''):
        raise AcceptanceParityError('FRESH_AUTHOR_RECEIPT_FACTS_MISMATCH')
    contract=state.get('authoring_contract')
    if not isinstance(contract,Mapping) or receipt.get('authoring_contract_sha256')!=hashlib.sha256(_canon(contract)).hexdigest():
        raise AcceptanceParityError('FRESH_AUTHOR_RECEIPT_CONTRACT_MISMATCH')
