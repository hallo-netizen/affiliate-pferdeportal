from __future__ import annotations

import copy
import hashlib
import json
import re
from typing import Any, Mapping


TITLE_OWNER = 'PARENT_TITLE_MACHINE'
METADATA_OWNER_FIELDS = {
    'PARENT_CATEGORY_MACHINE': 'category',
    'PARENT_ARTICLE_TYPE_MACHINE': 'article_type',
    'PARENT_KEYWORD_MACHINE': 'target_keyword',
    'PARENT_SLOT_MACHINE': 'plan_slot',
}
SUPPORTED_TITLE_CODES = {
    'BLOCKED_CONTENT_TITLE_COLON',
    'BLOCKED_CONTENT_FAQ_TITLE_QUESTION_MARK',
    'BLOCKED_CONTENT_TARGET_KEYWORD_TITLE',
}
SUPPORTED_TITLE_RULES = {
    'ARTICLE_TITLE_MUST_NOT_CONTAIN_COLON',
    'FAQ_TITLE_MUST_END_WITH_QUESTION_MARK',
    'TITLE_MUST_CONTAIN_TARGET_KEYWORD',
}
REQUIRED_ITEM_KEYS = ('title', 'target_keyword', 'category', 'article_type', 'plan_slot')


class ParentOwnerRepairError(RuntimeError):
    pass


def _canon(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')) + '\n').encode('utf-8')


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


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


def _validate_title_finding(finding: Mapping[str, Any]) -> tuple[str, str]:
    if not isinstance(finding, Mapping):
        raise ParentOwnerRepairError('FINDING_INVALID')
    owner = str(finding.get('repair_owner') or '').strip()
    if owner != TITLE_OWNER:
        raise ParentOwnerRepairError('OWNER_MISMATCH:' + (owner or 'MISSING'))
    field = str(finding.get('field_path') or '').strip().casefold()
    if field and 'title' not in field and 'headline' not in field:
        raise ParentOwnerRepairError('TITLE_FIELD_MISMATCH:' + field)
    code = str(finding.get('error_code') or '').strip()
    rule = str(finding.get('failed_rule') or '').strip()
    if code not in SUPPORTED_TITLE_CODES and rule not in SUPPORTED_TITLE_RULES:
        raise ParentOwnerRepairError('TITLE_RULE_UNSUPPORTED:' + (code or rule or 'MISSING'))
    return code, rule


def _remove_colon(title: str) -> str:
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
    return _clean_title(keyword + ' – ' + title)


def _validate_title_result(before: Mapping[str, str], after: Mapping[str, str]) -> None:
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


def _projection_item(*, authority_projection_bytes: bytes | None, authority_projection_sha256: str | None, item_index: int | None) -> dict[str, str]:
    if not isinstance(authority_projection_bytes, (bytes, bytearray)) or not authority_projection_bytes:
        raise ParentOwnerRepairError('UPSTREAM_METADATA_SOURCE_REQUIRED')
    if not isinstance(authority_projection_sha256, str) or not re.fullmatch(r'[0-9a-f]{64}', authority_projection_sha256):
        raise ParentOwnerRepairError('UPSTREAM_METADATA_SOURCE_HASH_REQUIRED')
    raw = bytes(authority_projection_bytes)
    if _sha(raw) != authority_projection_sha256:
        raise ParentOwnerRepairError('UPSTREAM_METADATA_SOURCE_HASH_MISMATCH')
    try:
        projection = json.loads(raw.decode('utf-8'))
    except Exception as exc:
        raise ParentOwnerRepairError('UPSTREAM_METADATA_SOURCE_JSON_INVALID') from exc
    if not isinstance(projection, dict):
        raise ParentOwnerRepairError('UPSTREAM_METADATA_SOURCE_OBJECT_REQUIRED')
    batch = projection.get('next_textmachine_metadata_batch')
    items = batch.get('items') if isinstance(batch, dict) else None
    count = batch.get('item_count') if isinstance(batch, dict) else None
    if not isinstance(items, list) or not isinstance(count, int) or isinstance(count, bool) or count != len(items):
        raise ParentOwnerRepairError('UPSTREAM_METADATA_BATCH_INVALID')
    if not isinstance(item_index, int) or isinstance(item_index, bool) or item_index < 0 or item_index >= len(items):
        raise ParentOwnerRepairError('UPSTREAM_METADATA_ITEM_INDEX_INVALID')
    return _validate_item(items[item_index])


def _restore_metadata_field(
    item: Mapping[str, Any],
    finding: Mapping[str, Any],
    *,
    authority_projection_bytes: bytes | None,
    authority_projection_sha256: str | None,
    item_index: int | None,
) -> dict[str, Any]:
    before = _validate_item(item)
    if not isinstance(finding, Mapping):
        raise ParentOwnerRepairError('FINDING_INVALID')
    owner = str(finding.get('repair_owner') or '').strip()
    field = METADATA_OWNER_FIELDS.get(owner)
    if field is None:
        raise ParentOwnerRepairError('OWNER_MISMATCH:' + (owner or 'MISSING'))
    authority = _projection_item(
        authority_projection_bytes=authority_projection_bytes,
        authority_projection_sha256=authority_projection_sha256,
        item_index=item_index,
    )
    for key in REQUIRED_ITEM_KEYS:
        if key != field and before[key] != authority[key]:
            raise ParentOwnerRepairError('UPSTREAM_METADATA_NON_OWNER_MISMATCH:' + key)
    if before[field] == authority[field]:
        # The downstream validator rejected exactly the value already supplied by the bound
        # upstream metadata projection. The projection therefore cannot repair itself. Going
        # further upstream to the real editorial-plan producer is mandatory and fail-closed.
        raise ParentOwnerRepairError('UPSTREAM_METADATA_SOURCE_REBUILD_REQUIRED:' + field)
    after = copy.deepcopy(before)
    after[field] = authority[field]
    # Validator-provided expected/actual values are deliberately ignored. The authority is the
    # hash-bound upstream projection only.
    return {
        'contract': 'SYSTEM4_PARENT_OWNER_REPAIR_V1',
        'owner': owner,
        'changed_fields': [field],
        'error_code': str(finding.get('error_code') or ''),
        'failed_rule': str(finding.get('failed_rule') or ''),
        'authority': 'HASH_BOUND_UPSTREAM_METADATA_PROJECTION',
        'item': after,
    }


def repair_item(
    item: Mapping[str, Any],
    finding: Mapping[str, Any],
    *,
    authority_projection_bytes: bytes | None = None,
    authority_projection_sha256: str | None = None,
    item_index: int | None = None,
) -> dict[str, Any]:
    owner = str(finding.get('repair_owner') or '').strip() if isinstance(finding, Mapping) else ''
    if owner in METADATA_OWNER_FIELDS:
        return _restore_metadata_field(
            item,
            finding,
            authority_projection_bytes=authority_projection_bytes,
            authority_projection_sha256=authority_projection_sha256,
            item_index=item_index,
        )

    before = _validate_item(item)
    code, rule = _validate_title_finding(finding)
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

    title = _ensure_keyword(title, after['target_keyword'])
    if after['article_type'].casefold() == 'faq':
        title = _ensure_question_mark(title)
    after['title'] = title
    _validate_title_result(before, after)
    return {
        'contract': 'SYSTEM4_PARENT_OWNER_REPAIR_V1',
        'owner': TITLE_OWNER,
        'changed_fields': ['title'],
        'error_code': code,
        'failed_rule': rule,
        'authority': 'DETERMINISTIC_BOUND_TITLE_RULE',
        'item': after,
    }
