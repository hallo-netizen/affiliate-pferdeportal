from __future__ import annotations

import hashlib
import json
import re
from typing import Any, Mapping

CONTRACT = 'SYSTEM4_SOURCE_BOUND_LT_EXCEPTION_V1'
SPELLER_RULE = 'GERMAN_SPELLER_RULE'
_TOKEN_RE = re.compile(r'^[A-Za-zÄÖÜäöüß][A-Za-zÄÖÜäöüß-]{3,}$')


def _canon(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def _target(checked_text: str, match: Mapping[str, Any]) -> str:
    offset = match.get('offset')
    length = match.get('length')
    if not isinstance(offset, int) or not isinstance(length, int) or offset < 0 or length <= 0:
        return ''
    return checked_text[offset:offset + length]


def _rule_id(match: Mapping[str, Any]) -> str:
    rule = match.get('rule') if isinstance(match.get('rule'), Mapping) else {}
    return str(rule.get('id') or '')


def _has_replacement(match: Mapping[str, Any]) -> bool:
    replacements = match.get('replacements')
    if not isinstance(replacements, list):
        return False
    return any(isinstance(row, Mapping) and isinstance(row.get('value'), str) and row.get('value').strip() for row in replacements)


def _whole_token_present(source_text: str, token: str) -> bool:
    if not source_text or not token:
        return False
    return re.search(r'(?<!\w)' + re.escape(token) + r'(?!\w)', source_text, flags=re.IGNORECASE | re.UNICODE) is not None


def classify_report(report: Mapping[str, Any], checked_text: str, trusted_source_text: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    matches = report.get('matches') if isinstance(report, Mapping) else None
    if not isinstance(matches, list):
        raise ValueError('LANGUAGETOOL_MATCHES_INVALID')
    unresolved: list[dict[str, Any]] = []
    approved: list[dict[str, Any]] = []
    source_hash = hashlib.sha256(trusted_source_text.encode('utf-8')).hexdigest() if trusted_source_text else ''
    for raw in matches:
        match = dict(raw) if isinstance(raw, Mapping) else {}
        token = _target(checked_text, match)
        source_bound = (
            _rule_id(match) == SPELLER_RULE
            and not _has_replacement(match)
            and bool(_TOKEN_RE.fullmatch(token))
            and _whole_token_present(trusted_source_text, token)
        )
        if not source_bound:
            unresolved.append(match)
            continue
        approved.append({
            'contract': CONTRACT,
            'rule_id': SPELLER_RULE,
            'target': token,
            'target_sha256': hashlib.sha256(token.encode('utf-8')).hexdigest(),
            'trusted_source_text_sha256': source_hash,
            'reason': 'EXACT_SOURCE_BOUND_TECHNICAL_TERM_WITHOUT_LT_REPLACEMENT',
        })
    return unresolved, approved


def install(pc: Any) -> None:
    if getattr(pc, '_SYSTEM4_SOURCE_BOUND_LT_POLICY_INSTALLED', False):
        return
    original_run_all = pc.run_all
    original_run_lt = pc.run_languagetool
    original_fresh = pc._fresh_ppm_language_evidence
    original_valid = pc._language_evidence_valid_for
    active = {'source_text': ''}

    def source_text_from_state(state: Mapping[str, Any]) -> str:
        research = state.get('research') if isinstance(state, Mapping) else None
        if not isinstance(research, Mapping):
            return ''
        value = research.get('text')
        return value if isinstance(value, str) else ''

    def run_languagetool(repo, article_html):
        plain = pc._plain_text(article_html)
        report, raw, return_code = pc._run_languagetool_text(repo, plain)
        unresolved, approved = classify_report(report, plain, active['source_text'])
        if unresolved:
            raise pc.RepairRequired('languagetool', pc._repair_findings_from_lt({'matches': unresolved}))
        return {
            'status': 'PASS',
            'engine': pc.LT_ENGINE,
            'commandline_jar_sha256': pc.LT_JAR_SHA256,
            'finding_count': 0,
            'approved_exception_count': len(approved),
            'approved_exceptions': approved,
            '_checked_text': plain.rstrip('\n'),
            '_raw_report_json': raw,
            '_return_code': return_code,
            '_approved_exceptions': approved,
        }

    def fresh_ppm_language_evidence(repo, article_html, lt_pass=None):
        checked = pc._ppm_visible_language_text(article_html)
        if isinstance(lt_pass, Mapping) and lt_pass.get('_checked_text') == checked:
            raw = str(lt_pass.get('_raw_report_json') or '')
            return_code = int(lt_pass.get('_return_code', -1))
            try:
                report = json.loads(raw)
            except json.JSONDecodeError as exc:
                raise pc.ProductionCheckError('LANGUAGETOOL_REPORT_INVALID') from exc
            source = 'REAL_LT68_FULLCHECK_REUSED'
        else:
            report, raw, return_code = pc._run_languagetool_text(repo, checked)
            source = 'REAL_LT68_CURRENT_DRAFT_REFRESHED'
        unresolved, approved = classify_report(report, checked, active['source_text'])
        if unresolved:
            raise pc.RepairRequired('languagetool', pc._repair_findings_from_lt({'matches': unresolved}))
        checked_hash = pc.text_sha256(checked)
        raw_hash = pc.text_sha256(raw)
        evidence = {
            'engine': pc.LT_ENGINE,
            'outer_dependency_sha256': pc.LT_OUTER_DEPENDENCY_SHA256,
            'inner_dependency_sha256': pc.LT_INNER_DEPENDENCY_SHA256,
            'content_hash': pc.text_sha256(article_html),
            'checked_text': checked,
            'checked_text_sha256': checked_hash,
            'raw_report_json': raw,
            'raw_report_sha256': raw_hash,
            'raw_finding_count': len(report.get('matches') or []),
            'unresolved_finding_count': 0,
            'return_code': return_code,
            'approved_exceptions': approved,
            'execution_record': {
                'input_sha256': checked_hash,
                'raw_stdout_sha256': raw_hash,
                'return_code': return_code,
            },
        }
        return evidence, source

    def language_evidence_valid_for(article_html, evidence):
        if not isinstance(evidence, dict):
            return False
        checked = pc._ppm_visible_language_text(article_html)
        raw = evidence.get('raw_report_json')
        if not isinstance(raw, str):
            return False
        try:
            report = json.loads(raw)
        except json.JSONDecodeError:
            return False
        try:
            unresolved, approved = classify_report(report, checked, active['source_text'])
        except ValueError:
            return False
        execution = evidence.get('execution_record') if isinstance(evidence.get('execution_record'), dict) else {}
        checked_hash = pc.text_sha256(checked)
        raw_hash = pc.text_sha256(raw)
        return (
            evidence.get('engine') == pc.LT_ENGINE
            and evidence.get('outer_dependency_sha256') == pc.LT_OUTER_DEPENDENCY_SHA256
            and evidence.get('inner_dependency_sha256') == pc.LT_INNER_DEPENDENCY_SHA256
            and evidence.get('content_hash') == pc.text_sha256(article_html)
            and evidence.get('checked_text') == checked
            and evidence.get('checked_text_sha256') == checked_hash
            and evidence.get('raw_report_sha256') == raw_hash
            and not unresolved
            and evidence.get('raw_finding_count') == len(report.get('matches') or [])
            and evidence.get('unresolved_finding_count') == 0
            and evidence.get('return_code') == 0
            and evidence.get('approved_exceptions') == approved
            and execution.get('input_sha256') == checked_hash
            and execution.get('raw_stdout_sha256') == raw_hash
            and execution.get('return_code') == 0
        )

    def run_all(repo, state, fact_pack, production_plan_item):
        previous = active['source_text']
        active['source_text'] = source_text_from_state(state)
        try:
            return original_run_all(repo, state, fact_pack, production_plan_item)
        finally:
            active['source_text'] = previous

    pc.run_languagetool = run_languagetool
    pc._fresh_ppm_language_evidence = fresh_ppm_language_evidence
    pc._language_evidence_valid_for = language_evidence_valid_for
    pc.run_all = run_all
    pc._SYSTEM4_SOURCE_BOUND_LT_POLICY_INSTALLED = True
