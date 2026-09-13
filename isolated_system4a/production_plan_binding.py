from __future__ import annotations

import hashlib
import json
import re
import zipfile
from pathlib import Path
from typing import Any, Mapping

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
PPM_PACKAGE_REL = 'control/startmaster0107/runtime_packages/PORTAL_PRODUCTION_MACHINE_V6.7.9_SIGNED_ARTICLE_TYPE_EXTENSION_ROOTFIX_FINAL.zip'
PPM_PACKAGE_SHA256 = 'acbda93bd1c4292de7aaf88db2195631103991ff508b36c88cb694714818abd1'
PORTAL_AUDIT_SHA256 = '456ee43cb2d7d3ccde8b73047d83c27a055d50961c478b310d5fe7b25e3c2ece'
QUALITY_CONTRACT = 'content_structure_language_binding_v2'
FORBIDDEN_PREBOUND = {'quality_binding', 'quality_binding_hash', 'category_binding', 'category_binding_hash'}


class ProductionPlanBindingError(RuntimeError):
    pass


def _require(condition: bool, code: str) -> None:
    if not condition:
        raise ProductionPlanBindingError(code)


def _canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')


def stable_hash(value: Any) -> str:
    return hashlib.sha256(_canonical(value)).hexdigest()


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with Path(path).open('rb') as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def _ppm_package() -> Path:
    path = REPO / PPM_PACKAGE_REL
    _require(path.is_file(), 'PPM679_PACKAGE_MISSING')
    _require(file_sha256(path) == PPM_PACKAGE_SHA256, 'PPM679_PACKAGE_HASH_MISMATCH')
    return path


def _zip_raw_and_json(archive: zipfile.ZipFile, suffix: str) -> tuple[bytes, dict[str, Any]]:
    hits = [name for name in archive.namelist() if name.endswith(suffix)]
    _require(len(hits) == 1, 'PPM679_CONTRACT_RESOLUTION_INVALID:' + suffix)
    raw = archive.read(hits[0])
    try:
        value = json.loads(raw.decode('utf-8'))
    except Exception as exc:
        raise ProductionPlanBindingError('PPM679_CONTRACT_JSON_INVALID:' + suffix) from exc
    _require(isinstance(value, dict), 'PPM679_CONTRACT_OBJECT_REQUIRED:' + suffix)
    return raw, value


def _zip_json(archive: zipfile.ZipFile, suffix: str) -> dict[str, Any]:
    return _zip_raw_and_json(archive, suffix)[1]


def _verify_contract_self(value: Mapping[str, Any], code: str) -> None:
    claimed = str(value.get('contract_self_sha256') or '')
    if not claimed:
        return
    copy = dict(value)
    copy.pop('contract_self_sha256', None)
    _require(claimed == stable_hash(copy), code)


def _verify_hierarchy_snapshot(value: Mapping[str, Any]) -> None:
    _verify_contract_self(value, 'PPM679_CATEGORY_HIERARCHY_SELF_HASH_INVALID')
    claimed = str(value.get('snapshot_sha256') or '')
    copy = dict(value)
    copy.pop('snapshot_sha256', None)
    copy.pop('contract_self_sha256', None)
    _require(bool(re.fullmatch(r'[0-9a-f]{64}', claimed)), 'PPM679_CATEGORY_HIERARCHY_SNAPSHOT_HASH_MISSING')
    _require(claimed == stable_hash(copy), 'PPM679_CATEGORY_HIERARCHY_SNAPSHOT_HASH_INVALID')


def _unique(rows: list[dict[str, Any]], key: str, value: str, code: str) -> dict[str, Any]:
    hits = [row for row in rows if isinstance(row, dict) and str(row.get(key) or '') == value]
    _require(len(hits) == 1, code + ':' + value)
    return hits[0]


def _intent_terms(article: Mapping[str, Any], category: Mapping[str, Any], fact_pack: Mapping[str, Any]) -> list[str]:
    terms: list[str] = []
    raw = [str(article.get('target_keyword') or ''), str(article.get('title') or '')]
    raw.extend(str(x) for x in category.get('semantic_keywords', []) if isinstance(x, str))
    for claim in fact_pack.get('claims', []) if isinstance(fact_pack.get('claims'), list) else []:
        if isinstance(claim, Mapping):
            for key in ('display_label', 'subject_scope'):
                value = str(claim.get(key) or '').strip()
                if value:
                    raw.append(value.replace('_', ' '))
    for text in raw:
        text = text.strip()
        if text and text not in terms:
            terms.append(text)
        for token in re.findall(r'[A-Za-zÄÖÜäöüß0-9-]{4,}', text):
            if token.lower() in {'eine','einer','eines','sicher','sichere','sicherer','wichtigsten','vorbereitung'}:
                continue
            if token not in terms:
                terms.append(token)
    _require(bool(terms), 'QUALITY_INTENT_TERMS_EMPTY')
    return terms[:24]


def _link_sections(template: Mapping[str, Any]) -> dict[str, str]:
    blocks = [str(x) for x in template.get('required_blocks', [])]
    content = [x for x in blocks if x not in {'intro', 'table', 'conclusion', 'further_information'}]
    _require(len(content) >= 2 and 'further_information' in blocks, 'ARTICLE_TYPE_LINK_SECTIONS_UNRESOLVED')
    return {
        'parent_category': content[0],
        'semantic_related': content[1],
        'further_information': 'further_information',
    }


def _make_link(role: str, section: str, href: str, anchor: str, hierarchy: str) -> dict[str, Any]:
    href = str(href)
    anchor = str(anchor).strip()
    _require(href.startswith('/') and not href.startswith('//'), 'PORTAL_LINK_NOT_RELATIVE:' + role)
    _require(bool(anchor), 'PORTAL_LINK_ANCHOR_EMPTY:' + role)
    reason = {
        'parent_category': 'Direkter interner Verweis auf die gebundene Themenkategorie.',
        'semantic_related': 'Semantisch übergeordneter interner Verweis auf den gebundenen Fachbereich.',
        'further_information': 'Weiterführender interner Verweis auf den gebundenen Hauptbereich.',
    }[role]
    return {
        'role': role,
        'href': href,
        'anchor': anchor,
        'section_id': section,
        'reason': reason,
        'active': True,
        'target_type': 'page',
        'target_status': 'publish',
        'hierarchy_path': [part.strip() for part in hierarchy.split('>') if part.strip()],
        'snapshot_contract': 'PFERDE_ATELIER_CATEGORYTEXT_AUDIT_20260830',
        'snapshot_sha256': PORTAL_AUDIT_SHA256,
    }


def bind_production_plan(article: Mapping[str, Any], bare_plan: Mapping[str, Any], fact_pack: Mapping[str, Any]) -> dict[str, Any]:
    _require(isinstance(article, Mapping) and isinstance(bare_plan, Mapping) and isinstance(fact_pack, Mapping), 'PRODUCTION_PLAN_BIND_INPUT_INVALID')
    prebound = sorted(FORBIDDEN_PREBOUND.intersection(bare_plan.keys()))
    _require(not prebound, 'PRODUCTION_PLAN_PREBOUND_FIELD_FORBIDDEN:' + ','.join(prebound))
    runtime = bare_plan.get('runtime_order')
    if isinstance(runtime, Mapping) and runtime.get('links') not in (None, [], ()):
        raise ProductionPlanBindingError('PRODUCTION_PLAN_PREBOUND_RUNTIME_LINKS_FORBIDDEN')

    package = _ppm_package()
    with zipfile.ZipFile(package) as archive:
        complete_raw, complete = _zip_raw_and_json(archive, 'complete-portal-category-source-v1.json')
        templates = _zip_json(archive, 'article-type-templates.json')
    _verify_contract_self(complete, 'PPM679_CATEGORY_SOURCE_SELF_HASH_INVALID')

    slug = str(article.get('category') or '').strip()
    article_type = str(article.get('article_type') or '').strip()
    complete_row = _unique(list(complete.get('categories') or []), 'category_slug', slug, 'PPM679_CATEGORY_NOT_UNIQUE')
    _require(str(complete_row.get('theme') or '') == article_type, 'PPM679_CATEGORY_ARTICLE_TYPE_MISMATCH')

    type_template = (templates.get('types') or {}).get(article_type)
    _require(isinstance(type_template, dict), 'PPM679_ARTICLE_TYPE_TEMPLATE_MISSING:' + article_type)
    sections = _link_sections(type_template)

    main_slug = str(complete_row.get('main_hub_slug') or '')
    section_slug = str(complete_row.get('section_hub_slug') or '')
    product_slug = str(complete_row.get('product_slug') or '')
    _require(all((main_slug, section_slug, product_slug)), 'PORTAL_LINK_HIERARCHY_SLUG_MISSING')
    role_targets = {
        'parent_category': (f'/{main_slug}/{section_slug}/{product_slug}/', str(complete_row.get('product') or '')),
        'semantic_related': (f'/{main_slug}/{section_slug}/', str(complete_row.get('section_hub') or '')),
        'further_information': (f'/{main_slug}/', str(complete_row.get('main_hub') or '')),
    }
    link_bindings = [
        _make_link(role, sections[role], role_targets[role][0], role_targets[role][1], str(complete_row.get('portal_path') or ''))
        for role in ('parent_category', 'semantic_related', 'further_information')
    ]
    _require(len({x['href'] for x in link_bindings}) == 3, 'PORTAL_LINK_TARGETS_NOT_DISTINCT')
    _require(len({x['section_id'] for x in link_bindings}) == 3, 'PORTAL_LINK_SECTIONS_NOT_DISTINCT')

    wordpress_category = {
        'slug': str(complete_row['category_slug']),
        'name': str(complete_row['category_name']),
        'hierarchy_path': str(complete_row['portal_path']),
        'taxonomy': str(complete_row['wp_taxonomy']),
        'category_source_snapshot_hash': hashlib.sha256(complete_raw).hexdigest(),
        'semantic_binding_not_numeric_identity': True,
    }
    registry = {
        'contract': 'portal_link_registry_snapshot_v2',
        'source_contract': 'PFERDE_ATELIER_CATEGORYTEXT_AUDIT_20260830',
        'source_snapshot_sha256': PORTAL_AUDIT_SHA256,
        'entries': link_bindings,
    }
    marker_seed = str(article.get('plan_slot') or '') + '|' + str(article.get('target_keyword') or '')
    marker = 'LT4A-' + hashlib.sha256(marker_seed.encode('utf-8')).hexdigest()[:12].upper()
    quality = {
        'contract': QUALITY_CONTRACT,
        'internal_test_marker': marker,
        'intent_terms': _intent_terms(article, {'semantic_keywords':[complete_row.get('product',''), complete_row.get('section_hub',''), complete_row.get('main_hub','')]}, fact_pack),
        'table_value_statement': 'Die Tabelle ergänzt die Entscheidung mit konkreten Prüfkriterien und klaren praktischen Folgerungen.',
        'wordpress_category': wordpress_category,
        'link_bindings': link_bindings,
        'portal_link_registry': registry,
        'portal_link_registry_hash': stable_hash(registry),
        'language_evidence': {},
    }

    out = json.loads(json.dumps(dict(bare_plan), ensure_ascii=False))
    out['quality_binding'] = quality
    out['quality_binding_hash'] = stable_hash(quality)
    runtime_out = dict(out.get('runtime_order') or {})
    runtime_out['links'] = [dict(x) for x in link_bindings]
    out['runtime_order'] = runtime_out
    return out
