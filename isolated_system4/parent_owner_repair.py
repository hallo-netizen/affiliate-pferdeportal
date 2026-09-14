from __future__ import annotations

import copy
import re
from typing import Any, Mapping


OWNER = 'PARENT_TITLE_MACHINE'
SUPPORTED_CODES = {
    'BLOCKED_CONTENT_TITLE_COLON',
    'BLOCKED_CONTENT_FAQ_TITLE_QUESTION_MARK',
    'BLOCKED_CONTENT_TARGET_KEYWORD_TITLE',
}
SUPPORTED_RULES = {
    'ARTICLE_TITLE_MUST_NOT_CONTAIN_COLON',
    'FAQ_TITLE_MUST_END_WITH_QUESTION_MARK',
    'TITLE_MUST_CONTAIN_TARGET_KEYWORD',
}
REQUIRED_ITEM_KEYS = ('title', 'target_keyword', 'category', 'article_type', 'plan_slot')


class ParentOwnerRepairError(RuntimeError):
    pass


def _clean_title(value: str) -> str:
    value = re.sub(r'\s+', ' ', str(value or '')).strip()
    value = re.sub(r'\s+([?!.,])', r'\1', value)
    return value


def _validate_item(item: Mapping[str, Any]) -> dict[str, str]:
    if not isinstance(item, Mapping):
        raise ParentOwnerRepairError('ITEM_INVALID')
    out: dict[str, str] = {}
    for key in REQUIRED_ITEM_KEYS:
        value = item.get(key)
        if not isinstance(value, str) or not value.strip():
            raise ParentOwnerRepairError('ITEM_FIELD_INVALID:' + key)
        out[key] = value.strip()
    if not re.fullmatch(r'[0-9a-f]{64}', out['plan_slot']):
        raise ParentOwnerRepairError('ITEM_PLAN_SLOT_INVALID')
    return out


def _validate_finding(finding: Mapping[str, Any]) -> tuple[str, str]:
    if not isinstance(finding, Mapping):
        raise ParentOwnerRepairError('FINDING_INVALID')
    owner = str(finding.get('repair_owner') or '').strip()
    if owner != OWNER:
        raise ParentOwnerRepairError('OWNER_MISMATCH:' + (owner or 'MISSING'))
    field = str(finding.get('field_path') or '').strip().casefold()
    if field and 'title' not in field and 'headline' not in field:
        raise ParentOwnerRepairError('TITLE_FIELD_MISMATCH:' + field)
    code = str(finding.get('error_code') or '').strip()
    rule = str(finding.get('failed_rule') or '').strip()
    if code not in SUPPORTED_CODES and rule not in SUPPORTED_RULES:
        raise ParentOwnerRepairError('TITLE_RULE_UNSUPPORTED:' + (code or rule or 'MISSING'))
    return code, rule


def _remove_colon(title: str) -> str:
    # Deterministic punctuation-only repair. No semantic rewriting is permitted here.
    value = re.sub(r'\s*:\s*', ' – ', title)
    value = re.sub(r'\s+–\s+', ' – ', value)
    return _clean_title(value)


def _ensure_question_mark(title: str) -> str:
    value = title.rstrip()
    if value.endswith('?'):
        return _clean_title(value)
    value = value.rstrip('.!;,:–- ')
    return _clean_title(value + '?')


def _ensure_keyword(title: str, keyword: str) -> str:
    if keyword.casefold() in title.casefold():
        return _clean_title(title)
    # The keyword is machine-bound input. Adding it verbatim is deterministic; no generated
    # wording or semantic freedom is introduced.
    return _clean_title(keyword + ' – ' + title)


def _validate_result(before: Mapping[str, str], after: Mapping[str, str], code: str, rule: str) -> None:
    title = after['title']
    keyword = after['target_keyword']
    if not title:
        raise ParentOwnerRepairError('TITLE_RESULT_EMPTY')
    if ':' in title:
        raise ParentOwnerRepairError('TITLE_RESULT_COLON_FORBIDDEN')
    if keyword.casefold() not in title.casefold():
        raise ParentOwnerRepairError('TITLE_RESULT_TARGET_KEYWORD_MISSING')
    if after['article_type'].casefold() == 'faq' and not title.endswith('?'):
        raise ParentOwnerRepairError('TITLE_RESULT_FAQ_QUESTION_MARK_MISSING')
    for key in ('target_keyword', 'category', 'article_type', 'plan_slot'):
        if after[key] != before[key]:
            raise ParentOwnerRepairError('NON_OWNER_FIELD_MUTATION:' + key)
    if title == before['title']:
        raise ParentOwnerRepairError('TITLE_REPAIR_NO_CHANGE')


def repair_item(item: Mapping[str, Any], finding: Mapping[str, Any]) -> dict[str, Any]:
    before = _validate_item(item)
    code, rule = _validate_finding(finding)
    after = copy.deepcopy(before)
    title = _clean_title(after['title'])

    if code == 'BLOCKED_CONTENT_TITLE_COLON' or rule == 'ARTICLE_TITLE_MUST_NOT_CONTAIN_COLON':
        title = _remove_colon(title)
    elif code == 'BLOCKED_CONTENT_FAQ_TITLE_QUESTION_MARK' or rule == 'FAQ_TITLE_MUST_END_WITH_QUESTION_MARK':
        title = _ensure_question_mark(title)
    elif code == 'BLOCKED_CONTENT_TARGET_KEYWORD_TITLE' or rule == 'TITLE_MUST_CONTAIN_TARGET_KEYWORD':
        title = _ensure_keyword(title, after['target_keyword'])
    else:
        raise ParentOwnerRepairError('TITLE_RULE_UNSUPPORTED:' + (code or rule or 'MISSING'))

    # A repair must leave the title valid against all title invariants that can be checked
    # solely from the machine-bound item. This prevents one owner repair from creating the
    # next known title defect.
    title = _ensure_keyword(title, after['target_keyword'])
    if after['article_type'].casefold() == 'faq':
        title = _ensure_question_mark(title)
    after['title'] = title
    _validate_result(before, after, code, rule)
    return {
        'contract': 'SYSTEM4_PARENT_OWNER_REPAIR_V1',
        'owner': OWNER,
        'changed_fields': ['title'],
        'error_code': code,
        'failed_rule': rule,
        'item': after,
    }
