from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any, Mapping

import production_checks

PORTAL_STRUCTURE_REL = 'affiliate-portal-router/assets/portal-structure-v279.json'
QUALITY_CONTRACT = 'content_structure_language_binding_v2'
REGISTRY_CONTRACT = 'portal_link_registry_snapshot_v2'
ROLE_SECTIONS = {
    'parent_category': 'criteria',
    'semantic_related': 'decision',
    'further_information': 'further_information',
}


class ProductionBindingError(RuntimeError):
    pass


def _walk(value: Any):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from _walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk(child)


def _one(nodes: list[dict[str, Any]], predicate, code: str) -> dict[str, Any]:
    matches = [node for node in nodes if predicate(node)]
    if len(matches) != 1:
        raise ProductionBindingError(code + ':' + str(len(matches)))
    return matches[0]


def _dedupe(values: list[str]) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    for value in values:
        text = str(value or '').strip()
        key = text.casefold()
        if text and key not in seen:
            seen.add(key)
            out.append(text)
    return out


def _marker(plan_slot: str) -> str:
    slot = str(plan_slot or '').strip()
    if not re.fullmatch(r'[0-9a-f]{64}', slot):
        raise ProductionBindingError('PLAN_SLOT_INVALID_FOR_MACHINE_BINDING')
    return 'LT' + slot[:12].upper()


def _href(*slugs: str) -> str:
    clean = [str(slug or '').strip().strip('/') for slug in slugs]
    if any(not re.fullmatch(r'[a-z0-9-]+', slug) for slug in clean):
        raise ProductionBindingError('PORTAL_HIERARCHY_SLUG_INVALID')
    return '/' + '/'.join(clean) + '/'


def _load_snapshot_bytes(repo: Path) -> bytes:
    path = (Path(repo) / PORTAL_STRUCTURE_REL).resolve()
    root = Path(repo).resolve()
    if root not in path.parents or not path.is_file():
        raise ProductionBindingError('PORTAL_STRUCTURE_MISSING')
    return path.read_bytes()


def bind_plan_from_snapshot(
    state: Mapping[str, Any],
    fact_pack: Mapping[str, Any],
    incoming_plan: Mapping[str, Any],
    snapshot_bytes: bytes,
) -> dict[str, Any]:
    article = state.get('article')
    if not isinstance(article, Mapping):
        raise ProductionBindingError('ARTICLE_BINDING_MISSING')
    if not isinstance(fact_pack, Mapping) or not isinstance(incoming_plan, Mapping):
        raise ProductionBindingError('BINDING_INPUT_OBJECT_REQUIRED')
    if incoming_plan.get('quality_binding') is not None or incoming_plan.get('quality_binding_hash') is not None:
        raise ProductionBindingError('EXTERNAL_QUALITY_BINDING_FORBIDDEN')
    runtime_in = incoming_plan.get('runtime_order')
    if not isinstance(runtime_in, Mapping):
        raise ProductionBindingError('RUNTIME_ORDER_MISSING_FOR_MACHINE_BINDING')
    if runtime_in.get('links') not in (None, []):
        raise ProductionBindingError('EXTERNAL_RUNTIME_LINK_BINDING_FORBIDDEN')

    try:
        structure = json.loads(snapshot_bytes.decode('utf-8'))
    except Exception as exc:
        raise ProductionBindingError('PORTAL_STRUCTURE_INVALID') from exc
    nodes = [dict(node) for node in _walk(structure)]

    category_slug = str(article.get('category') or '').strip()
    article_type = str(article.get('article_type') or '').strip()
    category = _one(
        nodes,
        lambda n: n.get('node_type') == 'themenkategorie'
        and n.get('category_slug') == category_slug
        and int(n.get('level') or 0) == 4,
        'PORTAL_CATEGORY_NOT_UNIQUE',
    )
    if str(category.get('theme') or '').casefold() != article_type.casefold():
        raise ProductionBindingError('PORTAL_CATEGORY_ARTICLE_TYPE_MISMATCH')

    main_slug = str(category.get('main_slug') or '').strip()
    hub_slug = str(category.get('hub_slug') or '').strip()
    product_slug = str(category.get('product_slug') or '').strip()
    main_title = str(category.get('main_hub') or '').strip()
    hub_title = str(category.get('hub') or '').strip()
    product_title = str(category.get('product') or '').strip()
    category_name = str(category.get('category_name') or '').strip()
    hierarchy_path = str(category.get('path') or '').strip()
    if not all((main_slug, hub_slug, product_slug, main_title, hub_title, product_title, category_name, hierarchy_path)):
        raise ProductionBindingError('PORTAL_CATEGORY_HIERARCHY_INCOMPLETE')

    main = _one(
        nodes,
        lambda n: n.get('node_type') == 'main_hub' and n.get('slug') == main_slug and int(n.get('level') or 0) == 1,
        'PORTAL_MAIN_HUB_NOT_UNIQUE',
    )
    hub = _one(
        nodes,
        lambda n: n.get('node_type') == 'bereichs_hub' and n.get('slug') == hub_slug and int(n.get('level') or 0) == 2,
        'PORTAL_AREA_HUB_NOT_UNIQUE',
    )
    product = _one(
        nodes,
        lambda n: n.get('node_type') == 'produktseite' and n.get('slug') == product_slug and int(n.get('level') or 0) == 3,
        'PORTAL_PRODUCT_PAGE_NOT_UNIQUE',
    )
    if str(hub.get('parent_slug') or '') != main_slug:
        raise ProductionBindingError('PORTAL_AREA_PARENT_MISMATCH')
    if str(product.get('parent_slug') or '') != hub_slug:
        raise ProductionBindingError('PORTAL_PRODUCT_PARENT_MISMATCH')
    if str(main.get('title') or '') != main_title or str(hub.get('title') or '') != hub_title or str(product.get('title') or '') != product_title:
        raise ProductionBindingError('PORTAL_HIERARCHY_TITLE_MISMATCH')

    snapshot_sha = hashlib.sha256(snapshot_bytes).hexdigest()
    links = [
        {
            'role': 'parent_category',
            'href': _href(main_slug),
            'anchor': main_title,
            'reason': 'Maschinell gebundener Portal-Hauptbereich',
            'section_id': ROLE_SECTIONS['parent_category'],
        },
        {
            'role': 'semantic_related',
            'href': _href(main_slug, hub_slug),
            'anchor': hub_title,
            'reason': 'Maschinell gebundener Portal-Bereich',
            'section_id': ROLE_SECTIONS['semantic_related'],
        },
        {
            'role': 'further_information',
            'href': _href(main_slug, hub_slug, product_slug),
            'anchor': product_title,
            'reason': 'Maschinell gebundene Portal-Produktseite',
            'section_id': ROLE_SECTIONS['further_information'],
        },
    ]
    registry_entries = [dict(row, active=True, target_type='portal_route', target_status='publish') for row in links]
    registry = {
        'contract': REGISTRY_CONTRACT,
        'snapshot_source_sha256': snapshot_sha,
        'entries': registry_entries,
    }
    registry_hash = production_checks.stable_hash(registry)

    target_keyword = str(article.get('target_keyword') or '').strip()
    intent_terms = _dedupe([target_keyword, product_title, hub_title, main_title])
    if not intent_terms:
        raise ProductionBindingError('MACHINE_INTENT_TERMS_EMPTY')
    table_statement = (
        'Die Tabelle bündelt die wichtigsten Auswahlkriterien für '
        + target_keyword
        + ' und macht die entscheidenden Prüfpunkte direkt vergleichbar.'
    )
    quality = {
        'contract': QUALITY_CONTRACT,
        'internal_test_marker': _marker(str(article.get('plan_slot') or '')),
        'intent_terms': intent_terms,
        'table_value_statement': table_statement,
        'language_evidence': {},
        'wordpress_category': {
            'slug': category_slug,
            'name': category_name,
            'hierarchy_path': hierarchy_path,
            'taxonomy': 'category',
            'category_source_snapshot_hash': snapshot_sha,
            'semantic_binding_not_numeric_identity': True,
        },
        'link_bindings': links,
        'portal_link_registry': registry,
        'portal_link_registry_hash': registry_hash,
    }

    plan = json.loads(json.dumps(dict(incoming_plan), ensure_ascii=False))
    runtime = plan['runtime_order']
    runtime['links'] = links
    plan['runtime_order'] = runtime
    plan['quality_binding'] = quality
    plan['quality_binding_hash'] = production_checks.stable_hash(quality)
    return plan


def bind_plan(repo: Path, state: Mapping[str, Any], fact_pack: Mapping[str, Any], incoming_plan: Mapping[str, Any]) -> dict[str, Any]:
    return bind_plan_from_snapshot(state, fact_pack, incoming_plan, _load_snapshot_bytes(Path(repo)))
