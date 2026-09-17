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


def _lt_finding_detail(raw: dict, plain: str) -> str:
    offset = raw.get('offset')
    length = raw.get('length')
    rule = raw.get('rule') if isinstance(raw.get('rule'), dict) else {}
    context = raw.get('context') if isinstance(raw.get('context'), dict) else {}
    target = ''
    if isinstance(offset, int) and isinstance(length, int) and offset >= 0 and length > 0:
        target = plain[offset:offset + length]
    detail = {
        'rule_id': str(rule.get('id') or ''),
        'category': str((rule.get('category') or {}).get('id') if isinstance(rule.get('category'), dict) else ''),
        'message': str(raw.get('message') or ''),
        'short_message': str(raw.get('shortMessage') or ''),
        'target': target,
        'context': str(context.get('text') or ''),
        'context_offset': context.get('offset'),
        'context_length': context.get('length'),
        'offset': offset,
        'length': length,
    }
    return json.dumps(detail, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def _project_checked_text(body: str, ppm_visible: bool) -> str:
    if ppm_visible:
        return production_checks._ppm_visible_language_text(body)
    return production_checks._plain_text(body)


def _compound_candidates(target: str) -> list[str]:
    candidates: list[str] = []

    # First try a single visible hyphen. This is the smallest possible
    # orthographic change and leaves the factual wording untouched.
    for split in range(len(target) - 3, 2, -1):
        left = target[:split]
        right = target[split:]
        if len(left) < 3 or len(right) < 3:
            continue
        upper_right = right[0].upper() + right[1:]
        for candidate in (left + '-' + upper_right, left + '-' + right):
            if candidate not in candidates:
                candidates.append(candidate)

    # If one hyphen is insufficient, try exactly three visible components.
    # Candidates are ordered by balanced component lengths, then by later
    # split points. No vocabulary or article-specific special case exists.
    triples: list[tuple[tuple[int, int, int], str]] = []
    n = len(target)
    for first in range(3, n - 5):
        for second in range(first + 3, n - 2):
            parts = [target[:first], target[first:second], target[second:]]
            if any(len(part) < 3 for part in parts):
                continue
            titled = [parts[0]] + [part[0].upper() + part[1:] for part in parts[1:]]
            plain = parts
            lengths = [len(part) for part in parts]
            balance = max(lengths) - min(lengths)
            distance = sum(abs(length - 7) for length in lengths)
            order_key = (balance, distance, -(first + second))
            triples.append((order_key, '-'.join(titled)))
            triples.append((order_key, '-'.join(plain)))
    for _, candidate in sorted(triples, key=lambda row: (row[0], row[1])):
        if candidate not in candidates:
            candidates.append(candidate)
    return candidates


def _validated_hyphen_replacement(repo: Path, state: dict, body: str, target: str, ppm_visible: bool) -> tuple[str, str]:
    if not re.fullmatch(r'[A-Za-zÄÖÜäöüß]{8,}', target):
        raise NoCodexRepairError('LT_NO_SUGGESTION_NOT_COMPOUND:' + target[:120])
    baseline_text = _project_checked_text(body, ppm_visible)
    baseline_report, _, _ = production_checks._run_languagetool_text(Path(repo), baseline_text)
    baseline_matches = baseline_report.get('matches') if isinstance(baseline_report, dict) else None
    if not isinstance(baseline_matches, list) or not baseline_matches:
        raise NoCodexRepairError('LT_NO_SUGGESTION_BASELINE_INVALID')
    baseline_count = len(baseline_matches)

    # Pure orthographic repair only. The real bound LT 6.8 is the sole
    # authority. A candidate is usable only when the complete article has
    # strictly fewer LT findings afterwards.
    for candidate in _compound_candidates(target):
        try:
            candidate_body = _replace_last_literal(body, target, candidate)
        except NoCodexRepairError:
            continue
        candidate_text = _project_checked_text(candidate_body, ppm_visible)
        report, _, _ = production_checks._run_languagetool_text(Path(repo), candidate_text)
        matches = report.get('matches') if isinstance(report, dict) else None
        if not isinstance(matches, list):
            continue
        if len(matches) >= baseline_count:
            continue
        authoring_contract.validate_candidate(candidate_body, state['authoring_contract'])
        return candidate_body, candidate
    raise NoCodexRepairError('LT_NO_SUGGESTION_NO_LT_VALIDATED_COMPOUND_REPAIR:' + target[:120])


def _repair_from_exact_lt_text(repo: Path, state: dict, body: str, checked_text: str, prefix: str, ppm_visible: bool) -> str:
    report, _, _ = production_checks._run_languagetool_text(Path(repo), checked_text)
    matches = report.get('matches') if isinstance(report, dict) else None
    if not isinstance(matches, list) or not matches:
        raise NoCodexRepairError(prefix + '_MATCHES_MISSING')

    normalized = []
    no_suggestion: list[dict] = []
    for raw in matches:
        if not isinstance(raw, dict):
            raise NoCodexRepairError(prefix + '_MATCH_INVALID')
        offset = raw.get('offset'); length = raw.get('length')
        replacements = raw.get('replacements')
        if not isinstance(offset, int) or not isinstance(length, int) or length <= 0:
            raise NoCodexRepairError(prefix + '_RANGE_INVALID:' + _lt_finding_detail(raw, checked_text))
        target = checked_text[offset:offset + length]
        if not target:
            raise NoCodexRepairError(prefix + '_TARGET_EMPTY:' + _lt_finding_detail(raw, checked_text))
        if not isinstance(replacements, list) or not replacements:
            rule = raw.get('rule') if isinstance(raw.get('rule'), dict) else {}
            if str(rule.get('id') or '') != 'GERMAN_SPELLER_RULE':
                raise NoCodexRepairError(prefix + '_NO_SUGGESTION:' + _lt_finding_detail(raw, checked_text))
            no_suggestion.append({'raw': raw, 'target': target, 'offset': offset})
            continue
        replacement = None
        for candidate in replacements:
            value = candidate.get('value') if isinstance(candidate, dict) else None
            if not isinstance(value, str) or not value.strip():
                continue
            if value == target:
                continue
            replacement = value
            break
        if replacement is None:
            raise NoCodexRepairError(prefix + '_NO_CHANGING_SUGGESTION:' + _lt_finding_detail(raw, checked_text))
        normalized.append((offset, target, replacement))

    repaired = body
    for _, target, replacement in sorted(normalized, key=lambda row: row[0], reverse=True):
        repaired = _replace_last_literal(repaired, target, replacement)

    chosen_by_target: dict[str, str] = {}
    for row in sorted(no_suggestion, key=lambda value: int(value['offset']), reverse=True):
        target = str(row['target'])
        chosen = chosen_by_target.get(target)
        if chosen is not None:
            repaired = _replace_last_literal(repaired, target, chosen)
            continue
        repaired, chosen = _validated_hyphen_replacement(repo, state, repaired, target, ppm_visible)
        chosen_by_target[target] = chosen

    if repaired == body:
        raise NoCodexRepairError(prefix + '_NO_CHANGE')
    authoring_contract.validate_candidate(repaired, state['authoring_contract'])
    return repaired


def repair_languagetool(repo: Path, workspace: Path) -> str:
    state = _state(workspace)
    body = str(state.get('draft_markdown') or '')
    if not body:
        raise NoCodexRepairError('LT_REPAIR_DRAFT_MISSING')
    plain = production_checks._plain_text(body)
    return _repair_from_exact_lt_text(repo, state, body, plain, 'LT_REPAIR', False)


def repair_ppm_language_evidence(repo: Path, workspace: Path) -> str:
    state = _state(workspace)
    body = str(state.get('draft_markdown') or '')
    if not body:
        raise NoCodexRepairError('PPM_LT_REPAIR_DRAFT_MISSING')
    checked = production_checks._ppm_visible_language_text(body)
    return _repair_from_exact_lt_text(repo, state, body, checked, 'PPM_LT_REPAIR', True)


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
    if any(code == 'BLOCKED_WAVE2_LANGUAGE_EVIDENCE' for code in codes):
        return repair_ppm_language_evidence(repo, workspace)
    if any(code == 'BLOCKED_WAVE2_CONCLUSION_BALANCE' for code in codes):
        return repair_conclusion_balance(workspace)
    raise NoCodexRepairError('NO_DETERMINISTIC_REPAIR_ADAPTER:' + checker + ':' + ','.join(codes))
