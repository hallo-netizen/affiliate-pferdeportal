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
QUALITY_CONTRACT = 'content_structure_language_binding_v2'
FORBIDDEN_PREBOUND = {'quality_binding', 'quality_binding_hash', 'category_binding', 'category_binding_hash'}
WP_EXPORT_MEMBER = 'portal-production-machine/fixtures/editorial-plan/portal-ist-export-20260710-read-only.json'


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
    copy = dict(value); copy.pop('contract_self_sha256', None)
    _require(claimed == stable_hash(copy), code)


def _verify_wp_export(value: Mapping[str, Any]) -> None:
    claimed = str(value.get('export_hash_sha256') or '')
    _require(bool(re.fullmatch(r'[0-9a-f]{64}', claimed)), 'PPM679_WP_EXPORT_HASH_MISSING')
    copy = dict(value); copy.pop('export_hash_sha256', None)
    _require(claimed == stable_hash(copy), 'PPM679_WP_EXPORT_HASH_INVALID')


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
                if value: raw.append(value.replace('_', ' '))
    for text in raw:
        text = text.strip()
        if text and text not in terms: terms.append(text)
        for token in re.findall(r'[A-Za-zÄÖÜäöüß0-9-]{4,}', text):
            if token.lower() in {'eine','einer','eines','sicher','sichere','sicherer','wichtigsten','vorbereitung'}: continue
            if token not in terms: terms.append(token)
    _require(bool(terms), 'QUALITY_INTENT_TERMS_EMPTY')
    return terms[:24]


def _link_sections(template: Mapping[str, Any]) -> dict[str, str]:
    blocks = [str(x) for x in template.get('required_blocks', [])]
    content = [x for x in blocks if x not in {'intro', 'table', 'conclusion', 'further_information'}]
    _require(len(content) >= 2 and 'further_information' in blocks, 'ARTICLE_TYPE_LINK_SECTIONS_UNRESOLVED')
    return {'parent_category': content[0], 'semantic_related': content[1], 'further_information': 'further_information'}


def _wp_pages(export: Mapping[str, Any]) -> tuple[list[dict[str, Any]], dict[int, dict[str, Any]]]:
    content = export.get('content')
    _require(isinstance(content, Mapping), 'PPM679_WP_EXPORT_CONTENT_INVALID')
    pages = content.get('page')
    _require(isinstance(pages, list), 'PPM679_WP_EXPORT_PAGES_INVALID')
    rows = [p for p in pages if isinstance(p, dict)]
    by_id = {int(p['ID']): p for p in rows if isinstance(p.get('ID'), int)}
    return rows, by_id


def _page_for_expected(page_id: Any, slug: str, pages: list[dict[str, Any]]) -> dict[str, Any]:
    hits = [p for p in pages if int(p.get('ID') or 0) == int(page_id or 0) and str(p.get('post_name') or '') == slug]
    _require(len(hits) == 1, 'PORTAL_LINK_SOURCE_PAGE_MISSING:' + slug)
    page = hits[0]
    _require(page.get('post_type') == 'page' and page.get('post_status') == 'publish', 'PORTAL_LINK_SOURCE_PAGE_NOT_PUBLISHED:' + slug)
    return page


def _page_href(page: Mapping[str, Any], by_id: Mapping[int, dict[str, Any]]) -> tuple[str, list[str], list[int]]:
    slugs: list[str] = []
    ids: list[int] = []
    seen: set[int] = set()
    current = dict(page)
    while current:
        pid = int(current.get('ID') or 0)
        _require(pid > 0 and pid not in seen, 'PORTAL_LINK_PARENT_CHAIN_INVALID')
        seen.add(pid); ids.append(pid)
        _require(current.get('post_status') == 'publish' and current.get('post_type') == 'page', 'PORTAL_LINK_PARENT_NOT_PUBLISHED')
        slug = str(current.get('post_name') or '').strip('/')
        _require(bool(slug), 'PORTAL_LINK_PAGE_SLUG_MISSING')
        slugs.append(slug)
        parent = int(current.get('post_parent') or 0)
        if parent == 0: break
        _require(parent in by_id, 'PORTAL_LINK_PARENT_PAGE_MISSING:' + str(parent))
        current = dict(by_id[parent])
    slugs.reverse(); ids.reverse()
    return '/' + '/'.join(slugs) + '/', slugs, ids


def _category_term(export: Mapping[str, Any], slug: str, expected_id: Any) -> dict[str, Any]:
    terms = export.get('terms')
    _require(isinstance(terms, Mapping) and isinstance(terms.get('category'), list), 'PPM679_WP_CATEGORY_TERMS_INVALID')
    hits = [t for t in terms['category'] if isinstance(t, dict) and t.get('slug') == slug]
    _require(len(hits) == 1, 'PPM679_WP_CATEGORY_TERM_MISSING:' + slug)
    term = hits[0]
    _require(int(term.get('term_id') or 0) == int(expected_id or 0), 'PPM679_WP_CATEGORY_TERM_ID_MISMATCH:' + slug)
    _require(term.get('taxonomy') == 'category', 'PPM679_WP_CATEGORY_TAXONOMY_MISMATCH:' + slug)
    return term


def _make_link(role: str, section: str, page: Mapping[str, Any], by_id: Mapping[int, dict[str, Any]], snapshot_sha: str, reason: str) -> dict[str, Any]:
    href, chain_slugs, chain_ids = _page_href(page, by_id)
    return {
        'role': role,
        'href': href,
        'anchor': str(page.get('post_title') or '').strip(),
        'section_id': section,
        'reason': reason,
        'active': True,
        'target_type': 'page',
        'target_status': 'publish',
        'target_id': int(page['ID']),
        'target_slug': str(page['post_name']),
        'parent_chain_slugs': chain_slugs,
        'parent_chain_ids': chain_ids,
        'snapshot_contract': 'PFERDE_ATELIER_PORTAL_IST_EXPORT_20260710_READ_ONLY',
        'snapshot_sha256': snapshot_sha,
    }


def validate_link_bindings_against_wp_snapshot(binding: Mapping[str, Any]) -> None:
    package = _ppm_package()
    with zipfile.ZipFile(package) as archive:
        wp_raw, wp = _zip_raw_and_json(archive, 'portal-ist-export-20260710-read-only.json')
    _verify_wp_export(wp)
    pages, by_id = _wp_pages(wp)
    bindings = binding.get('link_bindings')
    _require(isinstance(bindings, list) and len(bindings) == 3, 'PORTAL_LINK_BINDING_COUNT_INVALID')
    snapshot_sha = hashlib.sha256(wp_raw).hexdigest()
    for row in bindings:
        _require(isinstance(row, Mapping), 'PORTAL_LINK_BINDING_ROW_INVALID')
        target_id = int(row.get('target_id') or 0)
        page = by_id.get(target_id)
        _require(page is not None, 'PORTAL_LINK_BINDING_TARGET_ID_UNKNOWN:' + str(target_id))
        _require(page.get('post_status') == 'publish' and page.get('post_type') == 'page', 'PORTAL_LINK_BINDING_TARGET_NOT_PUBLISHED:' + str(target_id))
        expected_href, chain_slugs, chain_ids = _page_href(page, by_id)
        checks = [
            str(row.get('href') or '') == expected_href,
            str(row.get('anchor') or '') == str(page.get('post_title') or '').strip(),
            str(row.get('target_slug') or '') == str(page.get('post_name') or ''),
            list(row.get('parent_chain_slugs') or []) == chain_slugs,
            [int(x) for x in (row.get('parent_chain_ids') or [])] == chain_ids,
            str(row.get('snapshot_sha256') or '') == snapshot_sha,
            row.get('active') is True,
            row.get('target_type') == 'page',
            row.get('target_status') == 'publish',
        ]
        _require(all(checks), 'PORTAL_LINK_BINDING_SOURCE_MISMATCH:' + str(row.get('role') or ''))


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
        wp_raw, wp = _zip_raw_and_json(archive, 'portal-ist-export-20260710-read-only.json')
    _verify_contract_self(complete, 'PPM679_CATEGORY_SOURCE_SELF_HASH_INVALID')
    _verify_wp_export(wp)

    slug = str(article.get('category') or '').strip()
    article_type = str(article.get('article_type') or '').strip()
    complete_row = _unique(list(complete.get('categories') or []), 'category_slug', slug, 'PPM679_CATEGORY_NOT_UNIQUE')
    _require(str(complete_row.get('theme') or '') == article_type, 'PPM679_CATEGORY_ARTICLE_TYPE_MISMATCH')
    type_template = (templates.get('types') or {}).get(article_type)
    _require(isinstance(type_template, dict), 'PPM679_ARTICLE_TYPE_TEMPLATE_MISSING:' + article_type)
    sections = _link_sections(type_template)

    pages, by_id = _wp_pages(wp)
    main = _page_for_expected(complete_row.get('main_hub_page_id_historical'), str(complete_row.get('main_hub_slug') or ''), pages)
    section = _page_for_expected(complete_row.get('section_hub_page_id_historical'), str(complete_row.get('section_hub_slug') or ''), pages)
    product = _page_for_expected(complete_row.get('product_page_id_historical'), str(complete_row.get('product_slug') or ''), pages)
    _require(int(section.get('post_parent') or 0) == int(main['ID']), 'PORTAL_LINK_SECTION_PARENT_MISMATCH')
    _require(int(product.get('post_parent') or 0) == int(section['ID']), 'PORTAL_LINK_PRODUCT_PARENT_MISMATCH')
    snapshot_sha = hashlib.sha256(wp_raw).hexdigest()
    reasons = {
        'parent_category':'Direkter interner Verweis auf die gebundene Themenkategorie.',
        'semantic_related':'Semantisch übergeordneter interner Verweis auf den gebundenen Fachbereich.',
        'further_information':'Weiterführender interner Verweis auf den gebundenen Hauptbereich.',
    }
    link_bindings = [
        _make_link('parent_category', sections['parent_category'], product, by_id, snapshot_sha, reasons['parent_category']),
        _make_link('semantic_related', sections['semantic_related'], section, by_id, snapshot_sha, reasons['semantic_related']),
        _make_link('further_information', sections['further_information'], main, by_id, snapshot_sha, reasons['further_information']),
    ]
    _require(len({x['href'] for x in link_bindings}) == 3, 'PORTAL_LINK_TARGETS_NOT_DISTINCT')
    _require(len({x['section_id'] for x in link_bindings}) == 3, 'PORTAL_LINK_SECTIONS_NOT_DISTINCT')

    term = _category_term(wp, slug, complete_row.get('historical_term_id'))
    wordpress_category = {
        'id': int(term['term_id']),
        'slug': str(term['slug']),
        'name': str(term['name']),
        'hierarchy_path': str(complete_row['portal_path']),
        'taxonomy': 'category',
        'category_source_snapshot_hash': snapshot_sha,
    }
    registry = {
        'contract': 'portal_link_registry_snapshot_v2',
        'source_contract': 'PFERDE_ATELIER_PORTAL_IST_EXPORT_20260710_READ_ONLY',
        'source_snapshot_sha256': snapshot_sha,
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
    validate_link_bindings_against_wp_snapshot(quality)

    out = json.loads(json.dumps(dict(bare_plan), ensure_ascii=False))
    out['quality_binding'] = quality
    out['quality_binding_hash'] = stable_hash(quality)
    runtime_out = dict(out.get('runtime_order') or {})
    runtime_out['links'] = [dict(x) for x in link_bindings]
    out['runtime_order'] = runtime_out
    return out
