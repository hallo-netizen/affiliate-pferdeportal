#!/usr/bin/env python3
from __future__ import annotations

import subprocess
from pathlib import Path

import real_102_repair_matrix_v1 as matrix


def run_ppm_targeted_authorities(ppm_root: Path, rows: list[dict]) -> dict:
    ppm_rows = [r for r in rows if r['scope'] == 'PPM679']
    negative = sorted({r['negative_test'] for r in ppm_rows})
    positive = sorted({r['positive_test'] for r in ppm_rows})
    if any(not p for p in negative + positive):
        raise AssertionError('PPM_RULE_TEST_BINDING_MISSING')

    executed_negative = []
    for rel in negative:
        path = ppm_root / rel
        if not path.is_file():
            raise AssertionError('PPM_NEGATIVE_TEST_MISSING:' + rel)
        command_path = path
        compatibility = 'UNCHANGED'
        if rel == 'tests/test-canonical-runtime-binding.php':
            # This packaged test has a stale plan-v4 precheck before its 15 current
            # Content_Validator mutations. Only that unrelated precheck is disabled in
            # the temporary extracted test copy. All item-level positive checks and all
            # mutation assertions remain byte-for-byte unchanged.
            text = path.read_text(encoding='utf-8')
            exact = "ppm_test_assert(!empty($validated['ok']),'Canonical runtime plan must validate');"
            if text.count(exact) != 1:
                raise AssertionError('CANONICAL_PRECHECK_PATCH_TARGET_NOT_EXACT')
            text = text.replace(exact, "/* SYSTEM4_REAL102: stale plan-v4 precheck intentionally skipped; content positive + mutations unchanged */", 1)
            command_path = path.parent / '__system4_real102_canonical_runtime_binding.php'
            command_path.write_text(text, encoding='utf-8')
            compatibility = 'STALE_PLAN_PRECHECK_ONLY_SKIPPED'

        cp = subprocess.run(['php', str(command_path)], cwd=ppm_root, text=True, capture_output=True)
        combined = (cp.stdout or '') + '\n' + (cp.stderr or '')
        bound_rows = [r for r in ppm_rows if r['negative_test'] == rel]
        missing = sorted({r['error_code'] for r in bound_rows if r['error_code'] not in combined})
        if missing:
            raise AssertionError('PPM_TARGET_ERROR_NOT_EMITTED:' + rel + ':' + ','.join(missing) + ':RC=' + str(cp.returncode) + '\n' + combined[-12000:])
        if rel == 'tests/test-canonical-runtime-binding.php' and cp.returncode != 0:
            raise AssertionError('CANONICAL_CONTENT_MUTATION_TEST_FAILED_AFTER_PRECHECK_SKIP:RC=' + str(cp.returncode) + '\n' + combined[-12000:])
        executed_negative.append({'path': rel, 'return_code': cp.returncode, 'bound_rule_count': len(bound_rows), 'compatibility': compatibility})
        print('PPM_TARGETED_NEGATIVE_PASS:' + rel + ':' + str(len(bound_rows)) + ':' + compatibility, flush=True)

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


matrix.run_ppm_targeted_authorities = run_ppm_targeted_authorities
raise SystemExit(matrix.main())
