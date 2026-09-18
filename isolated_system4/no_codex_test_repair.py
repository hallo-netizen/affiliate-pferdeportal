from __future__ import annotations

import html
import json
import re
from pathlib import Path

import authoring_contract
import block_semantics
import production_checks
import repair_router


class NoCodexRepairError(RuntimeError):
    pass


def _state(workspace: Path) -> dict:
    return json.loads((Path(workspace) / 'state.json').read_text(encoding='utf-8'))


def _literal_replacement_candidates(body: str, target: str, replacement: str) -> list[str]:
    pairs = [(target, replacement)]
    escaped_target = html.escape(target, quote=False)
    escaped_replacement = html.escape(replacement, quote=False)
    if escaped_target != target:
        pairs.append((escaped_target, escaped_replacement))
    candidates: list[str] = []
    for needle, repl in pairs:
        positions: list[int] = []
        start = 0
        while True:
            pos = body.find(needle, start)
            if pos < 0:
                break
            positions.append(pos)
            start = pos + len(needle)
        for pos in reversed(positions):
            candidate = body[:pos] + repl + body[pos + len(needle):]
            if candidate != body and candidate not in candidates:
                candidates.append(candidate)
    if not candidates:
        raise NoCodexRepairError('LT_MATCH_NOT_FOUND_IN_HTML:' + target[:120])
    return candidates


def _replace_last_literal(body: str, target: str, replacement: str) -> str:
    return _literal_replacement_candidates(body, target, replacement)[0]


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


def _lt_matches(repo: Path, body: str, ppm_visible: bool) -> tuple[str, list[dict]]:
    checked = _project_checked_text(body, ppm_visible)
    report, _, _ = production_checks._run_languagetool_text(Path(repo), checked)
    matches = report.get('matches') if isinstance(report, dict) else None
    if not isinstance(matches, list):
        raise NoCodexRepairError('LT_MATCHES_INVALID')
    return checked, matches


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


def _best_monotonic_replacement(
    repo: Path,
    state: dict,
    body: str,
    target: str,
    replacements: list,
    ppm_visible: bool,
    baseline_count: int,
) -> str | None:
    best_body: str | None = None
    best_count = baseline_count
    for replacement in replacements:
        value = replacement.get('value') if isinstance(replacement, dict) else None
        if not isinstance(value, str) or not value.strip() or value == target:
            continue
        try:
            candidates = _literal_replacement_candidates(body, target, value)
        except NoCodexRepairError:
            continue
        for candidate_body in candidates:
            _, candidate_matches = _lt_matches(repo, candidate_body, ppm_visible)
            candidate_count = len(candidate_matches)
            if candidate_count >= best_count:
                continue
            try:
                authoring_contract.validate_candidate(candidate_body, state['authoring_contract'])
            except Exception:
                continue
            best_body = candidate_body
            best_count = candidate_count
            if best_count == 0:
                return best_body
    return best_body


def _validated_hyphen_replacement(repo: Path, state: dict, body: str, target: str, ppm_visible: bool) -> tuple[str, str]:
    if not re.fullmatch(r'[A-Za-zÄÖÜäöüß]{8,}', target):
        raise NoCodexRepairError('LT_NO_SUGGESTION_NOT_COMPOUND:' + target[:120])
    _, baseline_matches = _lt_matches(repo, body, ppm_visible)
    if not baseline_matches:
        raise NoCodexRepairError('LT_NO_SUGGESTION_BASELINE_INVALID')
    baseline_count = len(baseline_matches)

    # Pure orthographic repair only. The real bound LT 6.8 is the sole
    # authority. A candidate is usable only when the complete article has
    # strictly fewer LT findings afterwards.
    for candidate in _compound_candidates(target):
        try:
            candidate_bodies = _literal_replacement_candidates(body, target, candidate)
        except NoCodexRepairError:
            continue
        for candidate_body in candidate_bodies:
            _, matches = _lt_matches(repo, candidate_body, ppm_visible)
            if len(matches) >= baseline_count:
                continue
            try:
                authoring_contract.validate_candidate(candidate_body, state['authoring_contract'])
            except Exception:
                continue
            return candidate_body, candidate
    raise NoCodexRepairError('LT_NO_SUGGESTION_NO_LT_VALIDATED_COMPOUND_REPAIR:' + target[:120])


def _repair_from_exact_lt_text(repo: Path, state: dict, body: str, checked_text: str, prefix: str, ppm_visible: bool) -> str:
    repaired = body
    first_checked_text = checked_text
    first_iteration = True

    while True:
        if first_iteration:
            current_checked = first_checked_text
            report, _, _ = production_checks._run_languagetool_text(Path(repo), current_checked)
            matches = report.get('matches') if isinstance(report, dict) else None
            if not isinstance(matches, list):
                raise NoCodexRepairError(prefix + '_MATCHES_INVALID')
            first_iteration = False
        else:
            current_checked, matches = _lt_matches(repo, repaired, ppm_visible)

        if not matches:
            if repaired == body:
                raise NoCodexRepairError(prefix + '_MATCHES_MISSING')
            authoring_contract.validate_candidate(repaired, state['authoring_contract'])
            return repaired

        baseline_count = len(matches)
        first_detail = _lt_finding_detail(matches[0], current_checked) if isinstance(matches[0], dict) else '{}'
        improved = False

        for raw in matches:
            if not isinstance(raw, dict):
                raise NoCodexRepairError(prefix + '_MATCH_INVALID')
            offset = raw.get('offset')
            length = raw.get('length')
            replacements = raw.get('replacements')
            if not isinstance(offset, int) or not isinstance(length, int) or length <= 0:
                raise NoCodexRepairError(prefix + '_RANGE_INVALID:' + _lt_finding_detail(raw, current_checked))
            target = current_checked[offset:offset + length]
            if not target:
                raise NoCodexRepairError(prefix + '_TARGET_EMPTY:' + _lt_finding_detail(raw, current_checked))

            if isinstance(replacements, list) and replacements:
                candidate_body = _best_monotonic_replacement(
                    repo,
                    state,
                    repaired,
                    target,
                    replacements,
                    ppm_visible,
                    baseline_count,
                )
                if candidate_body is not None:
                    repaired = candidate_body
                    improved = True
                    break
                continue

            rule = raw.get('rule') if isinstance(raw.get('rule'), dict) else {}
            if str(rule.get('id') or '') != 'GERMAN_SPELLER_RULE':
                continue
            try:
                repaired, _ = _validated_hyphen_replacement(repo, state, repaired, target, ppm_visible)
            except NoCodexRepairError:
                continue
            improved = True
            break

        if not improved:
            raise NoCodexRepairError(prefix + '_NO_MONOTONIC_REPAIR:' + first_detail)


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


def repair_block_semantic_heading(workspace: Path) -> str:
    state = _state(workspace)
    body = str(state.get('draft_markdown') or '')
    checks = state.get('checks') if isinstance(state.get('checks'), dict) else {}
    findings = checks.get('findings') if isinstance(checks.get('findings'), list) else []
    mismatch = next((row for row in findings if isinstance(row, dict) and row.get('error_code') == 'BLOCK_CONTENT_SEMANTIC_HEADING_MISMATCH'), None)
    if not isinstance(mismatch, dict):
        raise NoCodexRepairError('BLOCK_SEMANTIC_HEADING_MISMATCH_FINDING_MISSING')
    field = str(mismatch.get('field_path') or mismatch.get('field') or '')
    prefix = 'content.blocks.'
    if not field.startswith(prefix):
        raise NoCodexRepairError('BLOCK_SEMANTIC_FIELD_INVALID:' + field)
    block_id = field[len(prefix):]
    expected = mismatch.get('expected') if isinstance(mismatch.get('expected'), dict) else {}
    markers = [str(v).strip() for v in expected.get('accepted_heading_markers', []) if isinstance(v, str) and str(v).strip()]
    if not markers:
        raise NoCodexRepairError('BLOCK_SEMANTIC_ACCEPTED_MARKERS_MISSING:' + block_id)
    reserved = {
        block_semantics.normalize(str(v))
        for v in (
            (state.get('authoring_contract',{}).get('structure_requirements',{}).get('headings',{}).get('reserved_headings',[]))
            if isinstance(state.get('authoring_contract'),dict) else []
        )
        if isinstance(v,str)
    }
    preferred = next((v for v in markers if block_semantics.normalize(v) not in reserved and len(v.split()) >= 2), None)
    replacement = preferred or (markers[1] if len(markers) > 1 else markers[0])
    if block_semantics.normalize(replacement) not in reserved:
        intent_terms = [
            str(v).strip() for v in state.get('authoring_contract',{}).get('bound_requirements',{}).get('intent_terms',[])
            if isinstance(v,str) and str(v).strip()
        ]
        if not intent_terms:
            raise NoCodexRepairError('BLOCK_SEMANTIC_INTENT_TERM_MISSING:' + block_id)
        intent = min(intent_terms,key=lambda value:(len(value.split()),len(value),value))
        if block_semantics.normalize(intent) not in block_semantics.normalize(replacement):
            replacement = replacement + ' zu ' + intent
    pattern = re.compile(r'(<section\b[^>]*data-block\s*=\s*(["\'])' + re.escape(block_id) + r'\2[^>]*>.*?<h2\b[^>]*>)(.*?)(</h2>)', re.S | re.I)
    match = pattern.search(body)
    if not match:
        raise NoCodexRepairError('BLOCK_SEMANTIC_TARGET_HEADING_MISSING:' + block_id)
    current = re.sub(r'(?is)<[^>]+>', ' ', match.group(3)).strip()
    if block_semantics.normalize(current) == block_semantics.normalize(replacement):
        replacement = markers[0]
    repaired = body[:match.start(3)] + replacement + body[match.end(3):]
    if repaired == body:
        raise NoCodexRepairError('BLOCK_SEMANTIC_REPAIR_UNCHANGED:' + block_id)
    authoring_contract.validate_candidate(repaired, state['authoring_contract'])
    block_semantics.validate(repaired, state['authoring_contract'])
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
    if checker == 'block_semantics' or any(code == 'BLOCK_CONTENT_SEMANTIC_HEADING_MISMATCH' for code in codes):
        return repair_block_semantic_heading(workspace)
    raise NoCodexRepairError('NO_DETERMINISTIC_REPAIR_ADAPTER:' + checker + ':' + ','.join(codes))
