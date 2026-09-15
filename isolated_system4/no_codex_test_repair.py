from __future__ import annotations

import html
import json
import re
from pathlib import Path

import authoring_contract
import production_checks
import repair_router


class NoCodexRepairError(RuntimeError):
    pass


def _state(workspace: Path) -> dict:
    return json.loads((Path(workspace) / 'state.json').read_text(encoding='utf-8'))


def _replace_last_literal(body: str, target: str, replacement: str) -> str:
    candidates = [(target, replacement)]
    escaped_target = html.escape(target, quote=False)
    escaped_replacement = html.escape(replacement, quote=False)
    if escaped_target != target:
        candidates.append((escaped_target, escaped_replacement))
    for needle, repl in candidates:
        pos = body.rfind(needle)
        if pos >= 0:
            return body[:pos] + repl + body[pos + len(needle):]
    raise NoCodexRepairError('LT_MATCH_NOT_FOUND_IN_HTML:' + target[:120])


def repair_languagetool(repo: Path, workspace: Path) -> str:
    state = _state(workspace)
    body = str(state.get('draft_markdown') or '')
    if not body:
        raise NoCodexRepairError('LT_REPAIR_DRAFT_MISSING')
    plain = production_checks._plain_text(body)
    report, _, _ = production_checks._run_languagetool_text(Path(repo), plain)
    matches = report.get('matches') if isinstance(report, dict) else None
    if not isinstance(matches, list) or not matches:
        raise NoCodexRepairError('LT_REPAIR_MATCHES_MISSING')
    normalized = []
    for raw in matches:
        if not isinstance(raw, dict):
            raise NoCodexRepairError('LT_REPAIR_MATCH_INVALID')
        offset = raw.get('offset'); length = raw.get('length')
        replacements = raw.get('replacements')
        if not isinstance(offset, int) or not isinstance(length, int) or length <= 0:
            raise NoCodexRepairError('LT_REPAIR_RANGE_INVALID')
        if not isinstance(replacements, list) or not replacements:
            raise NoCodexRepairError('LT_REPAIR_NO_SUGGESTION')
        replacement = replacements[0].get('value') if isinstance(replacements[0], dict) else None
        if not isinstance(replacement, str) or not replacement.strip():
            raise NoCodexRepairError('LT_REPAIR_SUGGESTION_INVALID')
        target = plain[offset:offset + length]
        if not target:
            raise NoCodexRepairError('LT_REPAIR_TARGET_EMPTY')
        normalized.append((offset, target, replacement))
    repaired = body
    for _, target, replacement in sorted(normalized, key=lambda row: row[0], reverse=True):
        repaired = _replace_last_literal(repaired, target, replacement)
    if repaired == body:
        raise NoCodexRepairError('LT_REPAIR_NO_CHANGE')
    authoring_contract.validate_candidate(repaired, state['authoring_contract'])
    return repaired


def repair_conclusion_balance(workspace: Path) -> str:
    state = _state(workspace)
    body = str(state.get('draft_markdown') or '')
    pattern = re.compile(r'(<section data-block="conclusion">.*?)(</section>)', re.S)
    match = pattern.search(body)
    if not match:
        raise NoCodexRepairError('CONCLUSION_BLOCK_MISSING')
    section = match.group(1)
    last_p = section.rfind('</p>')
    if last_p < 0:
        raise NoCodexRepairError('CONCLUSION_PARAGRAPH_MISSING')
    keyword = state['article']['target_keyword']
    addition = (
        f' Für {keyword} bleibt die Entscheidung deshalb an den bereits gebundenen Kriterien auszurichten.'
        ' Der gebundene Quellenstand setzt zugleich die Grenze der Bewertung; zusätzliche Tatsachen werden ausdrücklich nicht ergänzt.'
    )
    section = section[:last_p] + addition + section[last_p:]
    repaired = body[:match.start(1)] + section + body[match.end(1):]
    authoring_contract.validate_candidate(repaired, state['authoring_contract'])
    return repaired


def candidate_for_current_failure(repo: Path, workspace: Path) -> str:
    state = _state(workspace)
    if state.get('phase') != 'REPAIR_REQUIRED':
        raise NoCodexRepairError('REPAIR_PHASE_REQUIRED')
    checks = state.get('checks') if isinstance(state.get('checks'), dict) else {}
    checker = str(checks.get('checker') or '')
    findings = checks.get('findings') if isinstance(checks.get('findings'), list) else []
    codes = [str(row.get('error_code') or '') for row in findings if isinstance(row, dict)]
    route = repair_router.classify(state)
    owner = str(route.get('owner') or '')
    target = str(route.get('target') or '')
    if owner != 'DRAFT_BODY' or target != 'SAME_ARTICLE_BODY':
        raise NoCodexRepairError('NON_BODY_REPAIR_ROUTE:' + owner + ':' + target)
    if checker == 'languagetool' or any(code == 'LANGUAGETOOL_FINDING' for code in codes):
        return repair_languagetool(repo, workspace)
    if any(code == 'BLOCKED_WAVE2_CONCLUSION_BALANCE' for code in codes):
        return repair_conclusion_balance(workspace)
    raise NoCodexRepairError('NO_DETERMINISTIC_REPAIR_ADAPTER:' + checker + ':' + ','.join(codes))
