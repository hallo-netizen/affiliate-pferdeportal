from __future__ import annotations

import re
from typing import Any


class DesignGuardError(RuntimeError):
    pass


def _require(condition: bool, code: str) -> None:
    if not condition:
        raise DesignGuardError(code)


def _class_tokens(attrs: str) -> set[str]:
    match = re.search(r'(?is)\bclass\s*=\s*(["\'])(.*?)\1', attrs)
    if not match:
        return set()
    return {token for token in re.split(r'\s+', match.group(2).strip()) if token}


def validate_design_neutrality(article_html: str, article_type: str) -> dict[str, Any]:
    """Fail-closed guard for the already-existing Pferde-Atelier content/design contract.

    This function never rewrites HTML. It only blocks article HTML that would bypass the
    already-bound production/design selectors. The rules mirror the existing PPM/table
    contract and the documented August design failure: no inline/global styling payload,
    canonical article classes, and canonical table selector classes.
    """
    _require(isinstance(article_html, str) and article_html.strip(), 'DESIGN_BODY_EMPTY')
    _require(isinstance(article_type, str) and article_type.strip(), 'DESIGN_ARTICLE_TYPE_MISSING')

    lowered = article_html.casefold()
    _require(re.search(r'(?is)<(?:style|script|iframe|form)\b', article_html) is None, 'DESIGN_ACTIVE_OR_GLOBAL_HTML_FORBIDDEN')
    _require(re.search(r'(?is)\sstyle\s*=', article_html) is None, 'DESIGN_INLINE_STYLE_FORBIDDEN')
    _require(re.search(r'(?is)\son[a-z0-9_-]+\s*=', article_html) is None, 'DESIGN_EVENT_HANDLER_FORBIDDEN')
    _require('javascript:' not in lowered, 'DESIGN_JAVASCRIPT_URL_FORBIDDEN')

    root = re.match(r'(?is)^\s*<article\b([^>]*)>', article_html)
    _require(root is not None, 'DESIGN_CANONICAL_ARTICLE_ROOT_MISSING')
    root_attrs = root.group(1)
    root_classes = _class_tokens(root_attrs)
    _require('ppm-generated' in root_classes, 'DESIGN_PPM_GENERATED_CLASS_MISSING')
    expected_type_class = 'ppm-type-' + article_type.strip().casefold()
    _require(expected_type_class in root_classes, 'DESIGN_ARTICLE_TYPE_CLASS_MISSING:' + expected_type_class)
    type_attr = re.search(r'(?is)\bdata-article-type\s*=\s*(["\'])(.*?)\1', root_attrs)
    _require(type_attr is not None and type_attr.group(2).strip() == article_type.strip(), 'DESIGN_ARTICLE_TYPE_ATTRIBUTE_MISMATCH')
    _require(len(re.findall(r'(?is)<article\b', article_html)) == 1, 'DESIGN_NESTED_ARTICLE_FORBIDDEN')

    table_count = 0
    for table_count, table_match in enumerate(re.finditer(r'(?is)<table\b([^>]*)>', article_html), start=1):
        attrs = table_match.group(1)
        classes = _class_tokens(attrs)
        _require('system-129-table' in classes, f'DESIGN_TABLE_SYSTEM129_CLASS_MISSING:{table_count - 1}')
        _require('comparison-table' in classes, f'DESIGN_TABLE_COMPARISON_CLASS_MISSING:{table_count - 1}')
        _require(re.search(r'(?is)\bstyle\s*=', attrs) is None, f'DESIGN_TABLE_INLINE_STYLE_FORBIDDEN:{table_count - 1}')

    # Documented existing Beratung design uses H2 for article section headings. The bad
    # live run proved that additional H3 headings changed visible styling. Do not repair
    # or restyle them here; block before WordPress instead.
    if article_type.strip().casefold() == 'beratung':
        _require(re.search(r'(?is)<h[13456]\b', article_html) is None, 'DESIGN_BERATUNG_HEADING_LEVEL_FORBIDDEN')

    return {
        'status': 'PASS',
        'article_type': article_type.strip(),
        'table_count': table_count,
        'content_mutation_performed': False,
        'design_mutation_performed': False,
    }
