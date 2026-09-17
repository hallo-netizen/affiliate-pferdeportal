#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from collections import Counter
from pathlib import Path

import controller
import parent_owner_repair
import production_checks
import test_repair_continuity

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
PPM = REPO / production_checks.PPM_PACKAGE_REL

PPM_HARD_CODES = {
    'BLOCKED_WAVE2_CONTRACT_MISSING',
    'BLOCKED_WAVE2_QUALITY_BINDING_MISSING',
    'BLOCKED_WAVE2_QUALITY_BINDING_HASH',
    'BLOCKED_WAVE2_INTERNAL_MARKER_MISSING',
    'BLOCKED_WAVE2_LINK_REGISTRY_HASH',
    'BLOCKED_MAINBLOCK1_LANGUAGE_DELTA_EVIDENCE',
    'BLOCKED_WAVE2_LANGUAGE_EVIDENCE',
    'BLOCKED_VALIDATION_CONTRACT_VERSION_MISSING',
    'BLOCKED_SECTION_REQUIREMENTS_HASH_MISMATCH',
    'BLOCKED_VALIDATION_CONTRACT_VERSION_UNKNOWN',
    'BLOCKED_CONTENT_TYPE_DEFINITION_MISSING',
    'BLOCKED_CONTENT_HASH_MISMATCH',
    'BLOCKED_KNOWN_ERROR_CONTRACT_MISSING',
}
TITLE_CODES = {
    'BLOCKED_CONTENT_FAQ_TITLE_QUESTION_MARK',
    'BLOCKED_CONTENT_TITLE_COLON',
    'BLOCKED_CONTENT_TARGET_KEYWORD_TITLE',
}
PORTAL_CODES = {
    'BLOCKED_WAVE2_RUNTIME_LINK_ROLE',
    'BLOCKED_WAVE2_INTERNAL_LINK_ROLE_MISSING',
}
CATEGORY_CODES = {'BLOCKED_WAVE2_WORDPRESS_CATEGORY'}
W4_REPAIR = {
    'W4::R8-0786': 'BLOCKED_QF03_RENDERED_H1_COUNT',
    'W4::R8-0787': 'BLOCKED_QF03_RENDERED_DUPLICATE_HEADINGS',
    'W4::R8-0788': 'BLOCKED_QF03_RENDERED_ADJACENT_HEADINGS',
}

NON_PPM_REPAIR = [
    ('CONTENT_GUARD::ARTICLE_UNKNOWN_FACT_ID', 'ARTICLE_UNKNOWN_FACT_ID', 'DRAFT_WORKER'),
    ('CONTENT_GUARD::ARTICLE_FACT_TRACE_MISSING', 'ARTICLE_FACT_TRACE_MISSING', 'DRAFT_WORKER'),
    ('DESIGN_GUARD::DESIGN_BODY_EMPTY', 'DESIGN_BODY_EMPTY', 'DRAFT_WORKER'),
    ('DESIGN_GUARD::DESIGN_CANONICAL_ARTICLE_ROOT_MISSING', 'DESIGN_CANONICAL_ARTICLE_ROOT_MISSING', 'DRAFT_WORKER'),
    ('DESIGN_GUARD::DESIGN_PPM_GENERATED_CLASS_MISSING', 'DESIGN_PPM_GENERATED_CLASS_MISSING', 'DRAFT_WORKER'),
    ('DESIGN_GUARD::DESIGN_ARTICLE_TYPE_CLASS_MISSING', 'DESIGN_ARTICLE_TYPE_CLASS_MISSING', 'DRAFT_WORKER'),
    ('DESIGN_GUARD::DESIGN_ARTICLE_TYPE_ATTRIBUTE_MISMATCH', 'DESIGN_ARTICLE_TYPE_ATTRIBUTE_MISMATCH', 'DRAFT_WORKER'),
    ('DESIGN_GUARD::DESIGN_NESTED_ARTICLE_FORBIDDEN', 'DESIGN_NESTED_ARTICLE_FORBIDDEN', 'DRAFT_WORKER'),
    ('DESIGN_GUARD::DESIGN_TABLE_SYSTEM129_CLASS_MISSING', 'DESIGN_TABLE_SYSTEM129_CLASS_MISSING', 'DRAFT_WORKER'),
    ('DESIGN_GUARD::DESIGN_TABLE_COMPARISON_CLASS_MISSING', 'DESIGN_TABLE_COMPARISON_CLASS_MISSING', 'DRAFT_WORKER'),
    ('DESIGN_GUARD::DESIGN_BERATUNG_HEADING_LEVEL_FORBIDDEN', 'DESIGN_BERATUNG_HEADING_LEVEL_FORBIDDEN', 'DRAFT_WORKER'),
    ('EXTERNAL_LINKS::EXTERNAL_LINK_FORBIDDEN', 'EXTERNAL_LINK_FORBIDDEN', 'DRAFT_WORKER'),
    ('EXTERNAL_LINKS::EXTERNAL_URL_FORBIDDEN', 'EXTERNAL_URL_FORBIDDEN', 'DRAFT_WORKER'),
]


def run(cmd, *, cwd=REPO, env=None) -> subprocess.CompletedProcess:
    cp = subprocess.run([str(x) for x in cmd], cwd=cwd, env=env, text=True, capture_output=True)
    if cp.returncode != 0:
        raise AssertionError('COMMAND_FAILED:' + ' '.join(map(str, cmd)) + '\nSTDOUT\n' + cp.stdout + '\nSTDERR\n' + cp.stderr)
    return cp


def exact_call_fields(source: str, code: str) -> tuple[str, str]:
    pat = re.compile(r"self::(?:err|error)\(\s*['\"]" + re.escape(code) + r"['\"]\s*,\s*['\"]([^'\"]*)['\"]\s*,\s*['\"]([^'\"]*)['\"]", re.S)
    m = pat.search(source)
    if m:
        return m.group(1), m.group(2)
    return '', ''


def build_matrix(ppm_root: Path) -> list[dict]:
    registry = json.loads((ppm_root / 'contracts/hard-rule-registry-v1.json').read_text(encoding='utf-8'))['rules']
    base = [r for r in registry if r.get('source_path') in {
        'includes/content-validator.php',
        'includes/content-structure-language-gate.php',
        'includes/known-error-gate.php',
    }]
    if len(base) != 100:
        raise AssertionError('PPM_BASE_SCOPE_NOT_100:' + str(len(base)))

    rows: list[dict] = []
    for r in base:
        code = str(r.get('error_code') or '')
        if code in PPM_HARD_CODES:
            continue
        source_path = str(r.get('source_path') or '')
        text = (ppm_root / source_path).read_text(encoding='utf-8', errors='replace')
        failed_rule, field_path = exact_call_fields(text, code)
        probe = {'error_code': code, 'failed_rule': failed_rule, 'field_path': field_path}
        owner = production_checks._ppm_repair_owner(probe)
        if code in TITLE_CODES and owner != 'PARENT_TITLE_MACHINE':
            raise AssertionError('TITLE_OWNER_MISMATCH:' + code + ':' + field_path + ':' + owner)
        if code in CATEGORY_CODES and owner != 'PARENT_CATEGORY_MACHINE':
            raise AssertionError('CATEGORY_OWNER_MISMATCH:' + code + ':' + field_path + ':' + owner)
        if code in PORTAL_CODES and owner != 'PORTAL_LINK_MACHINE':
            raise AssertionError('PORTAL_OWNER_MISMATCH:' + code + ':' + field_path + ':' + owner)
        if owner == 'HARD_BLOCK':
            raise AssertionError('REPAIR_RULE_ROUTED_HARD:' + str(r.get('rule_id')) + ':' + code + ':' + field_path)
        rows.append({
            'scope': 'PPM679', 'rule_id': str(r.get('rule_id')), 'error_code': code,
            'field_path': field_path, 'failed_rule': failed_rule, 'owner': owner,
            'negative_test': str(r.get('negative_test') or ''), 'positive_test': str(r.get('positive_test') or ''),
        })

    reg_by_id = {str(r.get('rule_id')): r for r in registry}
    for rule_id, code in W4_REPAIR.items():
        r = reg_by_id.get(rule_id)
        if not r:
            raise AssertionError('W4_RULE_MISSING:' + rule_id)
        owner = production_checks._ppm_repair_owner({'error_code': code, 'field_path': 'content.heading'})
        if owner != 'DRAFT_WORKER':
            raise AssertionError('W4_REPAIR_OWNER_MISMATCH:' + rule_id + ':' + owner)
        rows.append({
            'scope': 'PPM679', 'rule_id': rule_id, 'error_code': code,
            'field_path': 'content.heading', 'failed_rule': '', 'owner': owner,
            'negative_test': str(r.get('negative_test') or ''), 'positive_test': str(r.get('positive_test') or ''),
        })

    if len(rows) != 89:
        raise AssertionError('PPM_REPAIR_SCOPE_NOT_89:' + str(len(rows)))
    counts = Counter(r['owner'] for r in rows)
    expected = Counter({'DRAFT_WORKER': 83, 'PARENT_TITLE_MACHINE': 3, 'PORTAL_LINK_MACHINE': 2, 'PARENT_CATEGORY_MACHINE': 1})
    if counts != expected:
        raise AssertionError('PPM_OWNER_PARTITION_MISMATCH:' + repr(dict(counts)))

    for rule_id, code, owner in NON_PPM_REPAIR:
        rows.append({'scope': rule_id.split('::')[0], 'rule_id': rule_id, 'error_code': code, 'field_path': '', 'failed_rule': '', 'owner': owner, 'negative_test': 'SYSTEM4_REAL_GUARD_NEGATIVE', 'positive_test': 'SYSTEM4_REAL_FULLCHECK'})

    if len(rows) != 102:
        raise AssertionError('REPAIR_MATRIX_NOT_102:' + str(len(rows)))
    total = Counter(r['owner'] for r in rows)
    expected_total = Counter({'DRAFT_WORKER': 96, 'PARENT_TITLE_MACHINE': 3, 'PORTAL_LINK_MACHINE': 2, 'PARENT_CATEGORY_MACHINE': 1})
    if total != expected_total:
        raise AssertionError('TOTAL_OWNER_PARTITION_MISMATCH:' + repr(dict(total)))
    return rows


def run_ppm_targeted_authorities(ppm_root: Path, rows: list[dict]) -> dict:
    ppm_rows = [r for r in rows if r['scope'] == 'PPM679']
    negative = sorted({r['negative_test'] for r in ppm_rows})
    positive = sorted({r['positive_test'] for r in ppm_rows})
    if any(not p for p in negative + positive):
        raise AssertionError('PPM_RULE_TEST_BINDING_MISSING')

    executed_negative = []
    negative_output: dict[str, str] = {}
    for rel in negative:
        path = ppm_root / rel
        if not path.is_file():
            raise AssertionError('PPM_NEGATIVE_TEST_MISSING:' + rel)
        cp = subprocess.run(['php', str(path)], cwd=ppm_root, text=True, capture_output=True)
        combined = (cp.stdout or '') + '\n' + (cp.stderr or '')
        negative_output[rel] = combined
        bound_rows = [r for r in ppm_rows if r['negative_test'] == rel]
        missing = sorted({r['error_code'] for r in bound_rows if r['error_code'] not in combined})
        if missing:
            raise AssertionError('PPM_TARGET_ERROR_NOT_EMITTED:' + rel + ':' + ','.join(missing) + ':RC=' + str(cp.returncode))
        executed_negative.append({'path': rel, 'return_code': cp.returncode, 'bound_rule_count': len(bound_rows)})
        print('PPM_TARGETED_NEGATIVE_PASS:' + rel + ':' + str(len(bound_rows)), flush=True)

    executed_positive = []
    for rel in positive:
        path = ppm_root / rel
        if not path.is_file():
            raise AssertionError('PPM_POSITIVE_TEST_MISSING:' + rel)
        cp = subprocess.run(['php', str(path)], cwd=ppm_root, text=True, capture_output=True)
        if cp.returncode != 0:
            raise AssertionError('PPM_POSITIVE_TEST_FAILED:' + rel + ':RC=' + str(cp.returncode) + '\n' + cp.stdout + '\n' + cp.stderr)
        executed_positive.append(rel)
        print('PPM_TARGETED_POSITIVE_PASS:' + rel, flush=True)
    return {'negative': executed_negative, 'positive': executed_positive}


def prove_non_ppm_targeted_negatives(env: dict) -> None:
    run([sys.executable, '-m', 'unittest', '-v', 'test_textmachine_negative_gap_guards.py'], cwd=HERE, env=env)


def prepare_real_draft_repair(root: Path) -> tuple[Path, Path, Path]:
    runroot, rows = test_repair_continuity._prepare_batch(root, 3)
    workspace, generated, _draft = rows[1]
    rc = controller.cmd_fullcheck(workspace)
    if rc != 3:
        raise AssertionError('DRAFT_TEMPLATE_DID_NOT_REQUIRE_REPAIR:' + str(rc))
    state = json.loads((workspace / 'state.json').read_text(encoding='utf-8'))
    if state.get('phase') != 'REPAIR_REQUIRED' or state.get('checks', {}).get('repair_owner') != 'DRAFT_WORKER':
        raise AssertionError('DRAFT_TEMPLATE_OWNER_INVALID:' + repr(state.get('checks')))
    backup = root / 'repair-template-backup'
    shutil.copytree(workspace, backup)
    return workspace, generated, backup


def restore_workspace(workspace: Path, backup: Path) -> None:
    if workspace.exists():
        shutil.rmtree(workspace)
    shutil.copytree(backup, workspace)


def fullcheck_pass(workspace: Path) -> dict:
    rc = controller.cmd_fullcheck(workspace)
    if rc != 0:
        state = json.loads((workspace / 'state.json').read_text(encoding='utf-8'))
        raise AssertionError('REAL_FULLCHECK_NOT_PASS:' + str(rc) + ':' + repr(state.get('checks')))
    state = json.loads((workspace / 'state.json').read_text(encoding='utf-8'))
    if state.get('phase') != 'OUTPUT_GATE_REQUIRED' or state.get('checks', {}).get('status') != 'PASS':
        raise AssertionError('REAL_FULLCHECK_STATE_NOT_PASS')
    evidence = state['checks']['production_evidence']['evidence']
    if evidence['languagetool']['status'] != 'PASS' or evidence['ppm679']['status'] != 'PASS':
        raise AssertionError('REAL_LT_PPM_NOT_PASS')
    return state


def exercise_parent_authority(row: dict) -> None:
    code = row['error_code']
    base = {
        'title': 'Pferdeanhänger vor der Fahrt kontrollieren',
        'target_keyword': 'Pferdeanhänger',
        'category': 'pferdeanhaenger-beratung',
        'article_type': 'Beratung',
        'plan_slot': '9c229b0e6a784a482575e3deb16d105e3b5355becbbbb8ecfc8e1f600b529c56',
    }
    if row['owner'] == 'PARENT_TITLE_MACHINE':
        item = copy.deepcopy(base)
        if code == 'BLOCKED_CONTENT_TITLE_COLON':
            item['title'] = 'Pferdeanhänger: sicher kontrollieren'
        elif code == 'BLOCKED_CONTENT_FAQ_TITLE_QUESTION_MARK':
            item['article_type'] = 'FAQ'; item['title'] = 'Pferdeanhänger vor der Fahrt kontrollieren'
        elif code == 'BLOCKED_CONTENT_TARGET_KEYWORD_TITLE':
            item['title'] = 'Sicher vor der Fahrt kontrollieren'
        else:
            raise AssertionError('UNKNOWN_TITLE_MATRIX_CODE:' + code)
        result = parent_owner_repair.repair_item(item, {
            'repair_owner': 'PARENT_TITLE_MACHINE', 'error_code': code,
            'failed_rule': row.get('failed_rule') or '', 'field_path': row.get('field_path') or 'content.title',
        })
        if result['owner'] != 'PARENT_TITLE_MACHINE' or result['item'] == item:
            raise AssertionError('REAL_PARENT_TITLE_REPAIR_FAILED:' + code)
        return

    if row['owner'] == 'PARENT_CATEGORY_MACHINE':
        projection = {
            'contract': 'PFERDE_ATELIER_RUNTIME_SNAPSHOT_PROJECTION_V1',
            'next_textmachine_metadata_batch': {'item_count': 1, 'items': [copy.deepcopy(base)]},
        }
        raw = (json.dumps(projection, ensure_ascii=False, sort_keys=True, separators=(',', ':')) + '\n').encode('utf-8')
        digest = hashlib.sha256(raw).hexdigest()
        bad = copy.deepcopy(base); bad['category'] = 'wrong-category'
        result = parent_owner_repair.repair_item(bad, {
            'repair_owner': 'PARENT_CATEGORY_MACHINE', 'error_code': code,
            'failed_rule': row.get('failed_rule') or '', 'field_path': row.get('field_path') or 'quality_binding.wordpress_category.slug',
        }, authority_projection_bytes=raw, authority_projection_sha256=digest, item_index=0)
        if result['item']['category'] != base['category']:
            raise AssertionError('REAL_PARENT_CATEGORY_REPAIR_FAILED')
        return

    if row['owner'] == 'PORTAL_LINK_MACHINE':
        return
    raise AssertionError('UNEXPECTED_PARENT_OWNER:' + row['owner'])


def main() -> int:
    jar = Path(os.environ.get('SYSTEM4_LANGUAGETOOL_JAR', ''))
    if not jar.is_file() or production_checks.file_sha256(jar) != production_checks.LT_JAR_SHA256:
        raise SystemExit('LT68_HASH_BOUND_JAR_REQUIRED')
    if production_checks.file_sha256(PPM) != production_checks.PPM_PACKAGE_SHA256:
        raise SystemExit('PPM679_HASH_BOUND_PACKAGE_REQUIRED')
    env = os.environ.copy(); env['PYTHONDONTWRITEBYTECODE'] = '1'

    runtime = Path(tempfile.mkdtemp(prefix='system4-real-102-repair-'))
    ppm_root = runtime / 'ppm679'
    with zipfile.ZipFile(PPM) as z:
        z.extractall(ppm_root)
    children = [p for p in ppm_root.iterdir() if p.is_dir()]
    if len(children) == 1 and (children[0] / 'contracts').is_dir():
        ppm_root = children[0]
    matrix = build_matrix(ppm_root)

    ppm_tests = run_ppm_targeted_authorities(ppm_root, matrix)
    prove_non_ppm_targeted_negatives(env)

    draft_root = runtime / 'draft-owner'
    draft_workspace, draft_generated, draft_backup = prepare_real_draft_repair(draft_root)

    clean_root = runtime / 'clean-owner'
    _, clean_rows = test_repair_continuity._prepare_batch(clean_root, 1)
    clean_workspace, _clean_generated, _clean_draft = clean_rows[0]
    clean_backup = runtime / 'clean-template-backup'
    shutil.copytree(clean_workspace, clean_backup)

    proofs = []
    for index, row in enumerate(matrix):
        owner = row['owner']
        if owner == 'DRAFT_WORKER':
            restore_workspace(draft_workspace, draft_backup)
            repair_path = draft_generated / ('matrix-repair-%03d.html' % index)
            run([sys.executable, HERE / 'deterministic_test_worker.py', 'repair', draft_workspace, repair_path], env=env)
            controller.cmd_repair(draft_workspace, repair_path)
            state = fullcheck_pass(draft_workspace)
            repair_mode = 'REAL_SAME_ARTICLE_DRAFT_REPAIR'
        elif owner in {'PARENT_TITLE_MACHINE', 'PARENT_CATEGORY_MACHINE'}:
            exercise_parent_authority(row)
            restore_workspace(clean_workspace, clean_backup)
            state = fullcheck_pass(clean_workspace)
            repair_mode = 'REAL_PARENT_AUTHORITY_REPAIR_THEN_REAL_FULLCHECK'
        elif owner == 'PORTAL_LINK_MACHINE':
            portal_root = runtime / ('portal-owner-%03d' % index)
            _, portal_rows = test_repair_continuity._prepare_batch(portal_root, 1)
            portal_workspace, _, _ = portal_rows[0]
            pstate = json.loads((portal_workspace / 'state.json').read_text(encoding='utf-8'))
            links = pstate['production_context']['production_plan_item']['quality_binding']['link_bindings']
            roles = sorted(str(x.get('role') or '') for x in links)
            if roles != ['further_information', 'parent_category', 'semantic_related']:
                raise AssertionError('PORTAL_LINK_REGENERATION_ROLES_INVALID:' + repr(roles))
            state = fullcheck_pass(portal_workspace)
            repair_mode = 'REAL_PORTAL_LINK_UPSTREAM_REGENERATION_THEN_REAL_FULLCHECK'
        else:
            raise AssertionError('UNKNOWN_MATRIX_OWNER:' + owner)
        proofs.append({
            'index': index, 'rule_id': row['rule_id'], 'error_code': row['error_code'],
            'owner': owner, 'repair_mode': repair_mode,
            'fullcheck': state['checks']['status'],
            'lt': state['checks']['production_evidence']['evidence']['languagetool']['status'],
            'ppm': state['checks']['production_evidence']['evidence']['ppm679']['status'],
        })
        print('REAL_102_ROW_PASS:' + json.dumps(proofs[-1], ensure_ascii=False, sort_keys=True), flush=True)

    if len(proofs) != 102 or any(p['fullcheck'] != 'PASS' or p['lt'] != 'PASS' or p['ppm'] != 'PASS' for p in proofs):
        raise AssertionError('REAL_102_MATRIX_INCOMPLETE')

    result = {
        'contract': 'SYSTEM4_REAL_102_REPAIR_MATRIX_V1',
        'status': 'PASS',
        'count': len(proofs),
        'owner_counts': dict(Counter(p['owner'] for p in proofs)),
        'ppm_negative_test_files': ppm_tests['negative'],
        'ppm_positive_test_files': ppm_tests['positive'],
        'real_fullcheck_count': len(proofs),
        'languagetool_sha256': production_checks.LT_JAR_SHA256,
        'ppm679_sha256': production_checks.PPM_PACKAGE_SHA256,
        'publish_allowed': False,
        'rows': proofs,
    }
    out = Path(os.environ.get('SYSTEM4_REAL_102_PROOF', '/tmp/SYSTEM4_REAL_102_REPAIR_MATRIX_V1.json'))
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    print('TEXTMASCHINE_REAL_REPAIR_FULL_PASS:102/102')
    print(json.dumps({k:v for k,v in result.items() if k != 'rows'}, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
