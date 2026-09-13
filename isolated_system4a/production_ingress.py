from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
REPO = HERE.parent


class ProductionIngressError(RuntimeError):
    pass


def _require(condition: bool, code: str) -> None:
    if not condition:
        raise ProductionIngressError(code)


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _load_system4_root_entry() -> Any:
    path = REPO / 'isolated_system4' / 'root_entry.py'
    _require(path.is_file(), 'SYSTEM4_ROOT_IDENTITY_MODULE_MISSING')
    spec = importlib.util.spec_from_file_location('_system4a_bound_root_entry', path)
    _require(spec is not None and spec.loader is not None, 'SYSTEM4_ROOT_IDENTITY_MODULE_LOAD_FAILED')
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except Exception as exc:
        raise ProductionIngressError('SYSTEM4_ROOT_IDENTITY_MODULE_LOAD_FAILED') from exc
    _require(callable(getattr(module, '_critical_manifest_sha256', None)), 'SYSTEM4_ROOT_IDENTITY_API_MISSING')
    _require(isinstance(getattr(module, 'MANIFEST_FIELD', None), str), 'SYSTEM4_ROOT_IDENTITY_API_MISSING')
    return module


EXTERNAL_TOP_KEYS = {'contract', 'next_textmachine_metadata_batch'}
EXTERNAL_CONTRACT = 'SYSTEM4_WORDPRESS_LIVE_INPUT_FIXTURE_V1'
BATCH_KEYS = {'contract', 'status', 'batch_sha256', 'item_count', 'items', 'publish_allowed'}
BATCH_CONTRACT = 'PSERC_TEXTMACHINE_METADATA_BATCH_V2'
BATCH_STATUS = 'READY_FOR_TEXTMACHINE_METADATA_INTAKE'
ITEM_KEYS = {'title', 'target_keyword', 'category', 'article_type', 'plan_slot'}


def _load_ppm_category_contract() -> tuple[dict[str, Any], str]:
    path = REPO / 'isolated_system4' / 'production_checks.py'
    _require(path.is_file(), 'SYSTEM4_PRODUCTION_CHECKS_MISSING')
    spec = importlib.util.spec_from_file_location('_system4a_production_checks', path)
    _require(spec is not None and spec.loader is not None, 'SYSTEM4_PRODUCTION_CHECKS_LOAD_FAILED')
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except Exception as exc:
        raise ProductionIngressError('SYSTEM4_PRODUCTION_CHECKS_LOAD_FAILED') from exc
    package = REPO / str(module.PPM_PACKAGE_REL)
    _require(package.is_file(), 'PPM679_PACKAGE_MISSING')
    _require(module.file_sha256(package) == module.PPM_PACKAGE_SHA256, 'PPM679_PACKAGE_HASH_MISMATCH')
    rel = 'portal-production-machine/contracts/complete-portal-category-source-v1.json'
    try:
        with zipfile.ZipFile(package) as zf:
            raw = zf.read(rel)
    except Exception as exc:
        raise ProductionIngressError('PPM679_CATEGORY_CONTRACT_MISSING') from exc
    try:
        contract = json.loads(raw.decode('utf-8'))
    except Exception as exc:
        raise ProductionIngressError('PPM679_CATEGORY_CONTRACT_JSON_INVALID') from exc
    _require(isinstance(contract, dict) and isinstance(contract.get('categories'), list), 'PPM679_CATEGORY_CONTRACT_INVALID')
    declared = str(contract.get('contract_self_sha256') or '')
    copy = dict(contract); copy.pop('contract_self_sha256', None)
    actual = hashlib.sha256(json.dumps(copy, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')).hexdigest()
    _require(declared == actual, 'PPM679_CATEGORY_CONTRACT_SELF_HASH_MISMATCH')
    return contract, hashlib.sha256(raw).hexdigest()


def _validate_ppm_category(article: dict[str, Any]) -> None:
    contract, _ = _load_ppm_category_contract()
    slug = str(article.get('category') or '').strip()
    article_type = str(article.get('article_type') or '').strip().lower()
    matches = [c for c in contract['categories'] if isinstance(c, dict) and c.get('category_slug') == slug]
    _require(len(matches) == 1, 'PPM679_CATEGORY_NOT_CANONICAL:' + slug)
    category = matches[0]
    _require(str(category.get('theme') or '').strip().lower() == article_type, 'PPM679_CATEGORY_ARTICLE_TYPE_MISMATCH:' + slug)


def _validate_external_business_contract(value: dict[str, Any]) -> None:
    _require(set(value) == EXTERNAL_TOP_KEYS, 'EXTERNAL_SNAPSHOT_SCHEMA_INVALID')
    _require(value.get('contract') == EXTERNAL_CONTRACT, 'EXTERNAL_SNAPSHOT_CONTRACT_INVALID')
    batch = value.get('next_textmachine_metadata_batch')
    _require(isinstance(batch, dict) and set(batch) == BATCH_KEYS, 'EXTERNAL_BATCH_SCHEMA_INVALID')
    _require(batch.get('contract') == BATCH_CONTRACT, 'EXTERNAL_BATCH_CONTRACT_INVALID')
    _require(batch.get('status') == BATCH_STATUS, 'EXTERNAL_BATCH_STATUS_INVALID')
    _require(batch.get('publish_allowed') is False, 'EXTERNAL_PUBLISH_FORBIDDEN')
    batch_sha = batch.get('batch_sha256')
    _require(isinstance(batch_sha, str) and len(batch_sha) == 64 and all(c in '0123456789abcdef' for c in batch_sha), 'EXTERNAL_BATCH_SHA_INVALID')
    items = batch.get('items')
    _require(isinstance(items, list) and len(items) >= 1, 'EXTERNAL_BATCH_ITEMS_INVALID')
    _require(batch.get('item_count') == len(items), 'EXTERNAL_BATCH_COUNT_MISMATCH')
    seen_slots: set[str] = set()
    for raw in items:
        _require(isinstance(raw, dict) and set(raw) == ITEM_KEYS, 'EXTERNAL_ITEM_SCHEMA_INVALID')
        _require(all(isinstance(raw.get(key), str) and raw[key].strip() for key in ITEM_KEYS), 'EXTERNAL_ITEM_VALUE_INVALID')
        slot = raw['plan_slot']
        _require(len(slot) == 64 and all(c in '0123456789abcdef' for c in slot), 'EXTERNAL_PLAN_SLOT_INVALID')
        _require(slot not in seen_slots, 'EXTERNAL_PLAN_SLOT_DUPLICATE')
        _validate_ppm_category(raw)
        seen_slots.add(slot)


@dataclass(frozen=True)
class BoundProductionInput:
    external_input_sha256: str
    bound_snapshot_sha256: str
    system4_manifest_sha256: str
    bound_snapshot_path: Path


def bind_external_snapshot(external_snapshot: Path, authority_root: Path) -> BoundProductionInput:
    external_snapshot = Path(external_snapshot).resolve()
    authority_root = Path(authority_root).resolve()
    _require(external_snapshot.is_file(), 'EXTERNAL_SNAPSHOT_MISSING')
    _require(not (authority_root == REPO.resolve() or REPO.resolve() in authority_root.parents), 'AUTHORITY_ROOT_INSIDE_REPOSITORY')

    raw = external_snapshot.read_bytes()
    try:
        value = json.loads(raw.decode('utf-8'))
    except Exception as exc:
        raise ProductionIngressError('EXTERNAL_SNAPSHOT_JSON_INVALID') from exc
    _require(isinstance(value, dict), 'EXTERNAL_SNAPSHOT_OBJECT_REQUIRED')

    root_entry = _load_system4_root_entry()
    field = root_entry.MANIFEST_FIELD
    _require(field not in value, 'EXTERNAL_CONTROL_FIELD_FORBIDDEN:' + field)
    _validate_external_business_contract(value)
    try:
        manifest = str(root_entry._critical_manifest_sha256())
    except Exception as exc:
        raise ProductionIngressError('SYSTEM4_ROOT_MANIFEST_EVALUATION_FAILED:' + str(exc)) from exc
    _require(len(manifest) == 64 and all(c in '0123456789abcdef' for c in manifest), 'SYSTEM4_ROOT_MANIFEST_INVALID')

    bound = dict(value)
    bound[field] = manifest
    bound_raw = json.dumps(bound, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')
    external_sha = _sha(raw)
    bound_sha = _sha(bound_raw)

    authority_root.mkdir(parents=True, exist_ok=True, mode=0o700)
    os.chmod(authority_root, 0o700)
    _require((authority_root.stat().st_mode & 0o077) == 0, 'AUTHORITY_ROOT_PERMISSIONS_INVALID')
    ingress_dir = authority_root / 'ingress'
    ingress_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
    os.chmod(ingress_dir, 0o700)

    name = external_sha[:20] + '-' + manifest[:20] + '.json'
    target = ingress_dir / name
    tmp = ingress_dir / (name + '.tmp')
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    try:
        os.write(fd, bound_raw)
        os.fsync(fd)
    finally:
        os.close(fd)
    os.replace(tmp, target)
    os.chmod(target, 0o600)

    reread = target.read_bytes()
    _require(reread == bound_raw, 'BOUND_SNAPSHOT_READBACK_CHANGED')
    return BoundProductionInput(
        external_input_sha256=external_sha,
        bound_snapshot_sha256=bound_sha,
        system4_manifest_sha256=manifest,
        bound_snapshot_path=target,
    )
