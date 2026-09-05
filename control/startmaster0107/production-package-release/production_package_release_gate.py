#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import shutil
import sys
from pathlib import Path
from typing import Any, Mapping

PACKAGE_CONTRACT = 'PSERC_APPROVED_PRODUCTION_PACKAGE_V1'
PLAN_CONTRACT = 'production_plan_v4'
RECOVERY_CONTRACT = 'PFERDE_ATELIER_EXISTING_TEXT_RECOVERY_LOCK_V1'

class ReleaseBlocked(RuntimeError):
    pass


def stable_hash(obj: Any) -> str:
    return hashlib.sha256(json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')).hexdigest()


def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    try:
        obj = json.loads(Path(path).read_text(encoding='utf-8'))
    except Exception as exc:
        raise ReleaseBlocked('RELEASE_INPUT_JSON_INVALID') from exc
    if not isinstance(obj, dict):
        raise ReleaseBlocked('RELEASE_INPUT_MUST_BE_OBJECT')
    return obj


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ReleaseBlocked('RELEASE_VALIDATOR_MODULE_LOAD_FAILED:' + path.name)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    try:
        spec.loader.exec_module(mod)
    except Exception:
        sys.modules.pop(name, None)
        raise
    return mod


def repo_root_from_here() -> Path:
    return Path(__file__).resolve().parents[3]


def current_generation_binding(repo: Path) -> dict[str, Any]:
    state_path = repo / 'control/startmaster0107/runtime_inbox/RUNTIME_INBOX_STATE.json'
    state = load_json(state_path)
    ref = str(state.get('source_snapshot_ref') or '')
    expected_file_sha = str(state.get('source_snapshot_sha256') or '')
    batch_sha = str(state.get('batch_sha256') or '')
    if not ref or not expected_file_sha or not batch_sha:
        raise ReleaseBlocked('CURRENT_GENERATION_BINDING_INCOMPLETE')
    snap_path = (repo / ref).resolve()
    if repo.resolve() not in snap_path.parents:
        raise ReleaseBlocked('CURRENT_GENERATION_SOURCE_PATH_ESCAPE')
    if not snap_path.is_file() or file_sha(snap_path) != expected_file_sha:
        raise ReleaseBlocked('CURRENT_GENERATION_SOURCE_HASH_MISMATCH')
    snap = load_json(snap_path)
    batch = snap.get('next_textmachine_metadata_batch')
    if not isinstance(batch, dict) or str(batch.get('batch_sha256') or '') != batch_sha:
        raise ReleaseBlocked('CURRENT_GENERATION_BATCH_HASH_MISMATCH')
    items = batch.get('items')
    if not isinstance(items, list) or len(items) != int(batch.get('item_count') or 0):
        raise ReleaseBlocked('CURRENT_GENERATION_ITEM_COUNT_MISMATCH')
    slots = []
    bindings = {}
    for item in items:
        if not isinstance(item, dict):
            raise ReleaseBlocked('CURRENT_GENERATION_ITEM_INVALID')
        slot = str(item.get('plan_slot') or '')
        if len(slot) != 64 or slot in bindings:
            raise ReleaseBlocked('CURRENT_GENERATION_SLOT_INVALID_OR_DUPLICATE')
        slots.append(slot)
        bindings[slot] = {k: item.get(k) for k in ['title', 'target_keyword', 'category', 'article_type', 'plan_slot']}
    return {
        'generation': int(state.get('generation') or 0),
        'batch_sha256': batch_sha,
        'slots': slots,
        'bindings': bindings,
        'source_snapshot_ref': ref,
        'source_snapshot_sha256': expected_file_sha,
    }


def validate_package(path: Path, repo: Path, require_current_generation: bool = True, trusted_keys: Mapping[str, Mapping[str, str]] | None = None) -> dict[str, Any]:
    env = load_json(path)
    contract = str(env.get('contract') or '')
    if contract == PLAN_CONTRACT:
        raise ReleaseBlocked('INTERMEDIATE_PRODUCTION_PLAN_NOT_UPLOADABLE')
    if contract != PACKAGE_CONTRACT:
        raise ReleaseBlocked('UPLOAD_ARTIFACT_CONTRACT_INVALID')

    h7 = load_module(repo / 'control/single-door-boundary/single_door_preproduction_handoff.py', 'package_release_h7_validator')
    proof = h7.validate_production_package(Path(path), trusted_keys=trusted_keys) if trusted_keys is not None else h7.validate_production_package(Path(path))
    if not isinstance(proof, Mapping) or not proof.get('ok'):
        raise ReleaseBlocked('H7_PACKAGE_VALIDATION_FAILED')

    preflight = load_module(repo / 'control/production-package-preflight/PRODUCTION_PACKAGE_PREFLIGHT_GUARD_STARTMASTER0103.py', 'package_release_preflight')
    pf = preflight.validate(env)
    if not isinstance(pf, Mapping) or not pf.get('ok'):
        raise ReleaseBlocked('PRODUCTION_PACKAGE_PREFLIGHT_BLOCKED:' + json.dumps(pf.get('errors', []), ensure_ascii=False, sort_keys=True))

    generation = None
    if require_current_generation:
        generation = current_generation_binding(repo)
        release = env.get('workflow_release')
        release_items = release.get('items') if isinstance(release, dict) else None
        if not isinstance(release_items, list) or not release_items:
            raise ReleaseBlocked('WORKFLOW_RELEASE_ITEMS_MISSING')
        release_slots = [str(x.get('plan_slot') or '') for x in release_items if isinstance(x, dict)]
        if len(release_slots) != len(release_items) or len(set(release_slots)) != len(release_slots):
            raise ReleaseBlocked('WORKFLOW_RELEASE_SLOT_SET_INVALID')
        if set(release_slots) != set(generation['slots']):
            raise ReleaseBlocked('PACKAGE_NOT_EXACT_CURRENT_GENERATION')

    return {
        'ok': True,
        'status': 'UPLOAD_ARTIFACT_RELEASE_PASS',
        'contract': PACKAGE_CONTRACT,
        'package_id': env.get('package_id'),
        'artifact_sha256': file_sha(path),
        'h7_status': proof.get('status'),
        'preflight_status': pf.get('status'),
        'current_generation': generation['generation'] if generation else None,
        'current_batch_sha256': generation['batch_sha256'] if generation else None,
        'publish_allowed': False,
        'content_semantics_inspected': False,
        'content_mutation_performed': False,
    }


def build_recovery_manifest(plan_path: Path, repo: Path) -> dict[str, Any]:
    plan = load_json(plan_path)
    if str(plan.get('contract') or '') != PLAN_CONTRACT:
        raise ReleaseBlocked('RECOVERY_INPUT_NOT_PRODUCTION_PLAN_V4')
    generation = current_generation_binding(repo)
    source = plan.get('source_ready_batch')
    if not isinstance(source, dict):
        raise ReleaseBlocked('RECOVERY_SOURCE_READY_BATCH_MISSING')
    if int(source.get('generation') or 0) != generation['generation']:
        raise ReleaseBlocked('RECOVERY_GENERATION_MISMATCH')
    if str(source.get('batch_sha256') or '') != generation['batch_sha256']:
        raise ReleaseBlocked('RECOVERY_BATCH_SHA_MISMATCH')
    bindings = source.get('bindings')
    items = plan.get('items')
    if not isinstance(bindings, list) or not isinstance(items, list) or len(bindings) != len(items) or len(items) != len(generation['slots']):
        raise ReleaseBlocked('RECOVERY_ITEM_COUNT_MISMATCH')

    item_by_id = {}
    for item in items:
        if not isinstance(item, dict):
            raise ReleaseBlocked('RECOVERY_PLAN_ITEM_INVALID')
        cid = str(item.get('canonical_article_id') or '')
        if not cid or cid in item_by_id:
            raise ReleaseBlocked('RECOVERY_CANONICAL_ID_INVALID_OR_DUPLICATE')
        item_by_id[cid] = item

    locked = []
    seen_slots = set()
    for binding in bindings:
        if not isinstance(binding, dict):
            raise ReleaseBlocked('RECOVERY_BINDING_INVALID')
        slot = str(binding.get('plan_slot') or '')
        cid = str(binding.get('canonical_article_id') or '')
        if slot in seen_slots or slot not in generation['bindings'] or cid not in item_by_id:
            raise ReleaseBlocked('RECOVERY_BINDING_NOT_CURRENT_GENERATION')
        seen_slots.add(slot)
        expected = generation['bindings'][slot]
        for field in ['title', 'target_keyword', 'category', 'article_type']:
            if str(binding.get(field) or '') != str(expected.get(field) or ''):
                raise ReleaseBlocked('RECOVERY_METADATA_DRIFT:' + field)
        item = item_by_id[cid]
        article = item.get('canonical_article')
        if not isinstance(article, dict):
            raise ReleaseBlocked('RECOVERY_CANONICAL_ARTICLE_MISSING')
        if str(article.get('title') or '') != str(binding.get('title') or ''):
            raise ReleaseBlocked('RECOVERY_TITLE_DRIFT')
        if str(article.get('target_keyword') or '') != str(binding.get('target_keyword') or ''):
            raise ReleaseBlocked('RECOVERY_KEYWORD_DRIFT')
        if str(item.get('article_type') or '') != str(binding.get('article_type') or ''):
            raise ReleaseBlocked('RECOVERY_ARTICLE_TYPE_DRIFT')
        body_html = str(article.get('body_html') or '')
        body_text = str(article.get('body_text') or '')
        declared_html = str(article.get('body_html_sha256') or '')
        actual_html = hashlib.sha256(body_html.encode('utf-8')).hexdigest()
        if declared_html != actual_html:
            raise ReleaseBlocked('RECOVERY_BODY_HTML_HASH_INVALID')
        locked.append({
            'plan_slot': slot,
            'canonical_article_id': cid,
            'plan_item_key': str(binding.get('plan_item_key') or item.get('plan_item_key') or ''),
            'title': str(binding.get('title') or ''),
            'target_keyword': str(binding.get('target_keyword') or ''),
            'category': str(binding.get('category') or ''),
            'article_type': str(binding.get('article_type') or ''),
            'body_html_sha256': actual_html,
            'body_text_sha256': hashlib.sha256(body_text.encode('utf-8')).hexdigest(),
        })

    manifest = {
        'contract': RECOVERY_CONTRACT,
        'status': 'EXISTING_TEXTS_LOCKED_FOR_EXISTING_GATES_ONLY',
        'generation': generation['generation'],
        'batch_sha256': generation['batch_sha256'],
        'source_snapshot_ref': generation['source_snapshot_ref'],
        'source_snapshot_sha256': generation['source_snapshot_sha256'],
        'production_plan_sha256': file_sha(plan_path),
        'item_count': len(locked),
        'items': locked,
        'content_mutation_allowed': False,
        'metadata_reselection_allowed': False,
        'new_topic_research_allowed': False,
        'required_existing_process': [
            'fact_pack_binding',
            'language_quality_binding',
            'workflow_supervisor_signed_release',
            'production_package_envelope',
            'existing_preflight',
            'H7_R_PRE_001_handoff',
        ],
        'required_upload_contract': PACKAGE_CONTRACT,
        'publish_allowed': False,
    }
    manifest['manifest_sha256'] = stable_hash(manifest)
    return manifest


def verify_recovery_manifest(manifest_path: Path, plan_path: Path, repo: Path) -> dict[str, Any]:
    expected = build_recovery_manifest(plan_path, repo)
    actual = load_json(manifest_path)
    if actual != expected:
        raise ReleaseBlocked('RECOVERY_LOCK_MISMATCH')
    return {'ok': True, 'status': 'EXISTING_TEXT_RECOVERY_LOCK_PASS', 'manifest_sha256': expected['manifest_sha256'], 'publish_allowed': False}


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='cmd', required=True)
    v = sub.add_parser('validate')
    v.add_argument('package')
    v.add_argument('--allow-other-generation', action='store_true')
    r = sub.add_parser('release')
    r.add_argument('package')
    r.add_argument('output')
    r.add_argument('--allow-other-generation', action='store_true')
    m = sub.add_parser('recovery-manifest')
    m.add_argument('plan')
    m.add_argument('output')
    q = sub.add_parser('verify-recovery')
    q.add_argument('manifest')
    q.add_argument('plan')
    args = ap.parse_args(argv)
    repo = repo_root_from_here()
    try:
        if args.cmd == 'validate':
            result = validate_package(Path(args.package), repo, not args.allow_other_generation)
        elif args.cmd == 'release':
            result = validate_package(Path(args.package), repo, not args.allow_other_generation)
            out = Path(args.output)
            out.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(args.package, out)
            result['released_path'] = str(out)
            result['released_sha256'] = file_sha(out)
        elif args.cmd == 'recovery-manifest':
            result = build_recovery_manifest(Path(args.plan), repo)
            out = Path(args.output)
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        else:
            result = verify_recovery_manifest(Path(args.manifest), Path(args.plan), repo)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except Exception as exc:
        print(json.dumps({'ok': False, 'status': 'UPLOAD_ARTIFACT_RELEASE_BLOCKED', 'reason': str(exc), 'publish_allowed': False}, ensure_ascii=False, indent=2))
        return 2

if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:]))
