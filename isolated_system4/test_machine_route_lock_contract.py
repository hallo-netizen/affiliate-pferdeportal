from __future__ import annotations

import contextlib
import io
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import controller
import parent_start
import root_entry


ROUTE_FILES = ('point0.json', 'root_receipt.json', 'supervisor_state.json', 'bound_snapshot.json')


def _touch_route(workspace: Path) -> None:
    workspace.mkdir(parents=True, exist_ok=True)
    for name in ROUTE_FILES:
        (workspace / name).write_text('{}\n', encoding='utf-8')


class MachineRouteLockContractTests(unittest.TestCase):
    def test_pre_codex_start_hardlock_blocks_before_any_temp_workspace(self):
        blocker = parent_start.pre_codex_start_hardlock.PreCodexStartBlocked(
            'PRECODEX_RECEIPT_NOT_PASS'
        )
        with mock.patch.object(
            parent_start.pre_codex_start_hardlock,
            'validate',
            side_effect=blocker,
        ), mock.patch.object(parent_start.tempfile, 'mkdtemp') as mkdtemp:
            with self.assertRaisesRegex(
                parent_start.pre_codex_start_hardlock.PreCodexStartBlocked,
                'PRECODEX_RECEIPT_NOT_PASS',
            ):
                parent_start.start_bound()
        mkdtemp.assert_not_called()

    def test_current_real_state_is_fail_closed_before_codex(self):
        with self.assertRaisesRegex(
            parent_start.pre_codex_start_hardlock.PreCodexStartBlocked,
            'PRECODEX_CURRENT_STATE_START_NOT_ALLOWED',
        ):
            parent_start.pre_codex_start_hardlock.validate(parent_start.REPO)

    def test_pre_codex_start_historical_negative_matrix(self):
        guard = parent_start.pre_codex_start_hardlock
        manifest = json.loads(guard.MANIFEST.read_text(encoding='utf-8'))
        head = 'a' * 40
        state = {
            'next_allowed_step': 'RUN_NEW_ARTICLE_BATCH_NO_STOP',
            'publish_allowed': False,
            'execution_gate': {
                'step_id': 'RUN_NEW_ARTICLE_BATCH_NO_STOP',
                'sequence': 107007,
            },
            'current_execution_blocker': {'codex_start_allowed': True},
            'external_execution_blocker': {'resolved': True},
        }
        root = {
            'current_state_sha256': 'b' * 64,
            'next_allowed_step': 'RUN_NEW_ARTICLE_BATCH_NO_STOP',
        }
        receipt = {
            'contract': 'PFERDE_ATELIER_PRE_CODEX_START_RECEIPT_V1',
            'status': 'PASS',
            'authorized_head_sha': head,
            'dispatcher_pr': 342,
            'dispatcher_head_sha': head,
            'hardlock_base_run': 1,
            'hardlock_base_status': 'PASS',
            'hardlock_base_head_sha': head,
            'user_approval': True,
            'codex_capacity_status': 'AVAILABLE',
            'approved_article_count': 7,
            'new_article_policy': 'COMPLETELY_NEW_NO_RECOVERY_BODY',
            'sequential_advance_policy': 'PASS_ONLY',
            'repair_policy': 'SAME_ARTICLE_SAME_WORKSPACE_UNTIL_PASS',
            'restart_recovery_status': 'PASS_CROSS_PROCESS_AND_DURABLE_TRANSPORT_READY',
            'durable_evidence_transport_status': 'PASS',
            'codex_side_github_write_required': False,
            'publish_allowed': False,
        }

        result = guard.validate_payload(
            head=head,
            manifest=manifest,
            receipt=receipt,
            state=state,
            root=root,
            state_sha256='b' * 64,
        )
        self.assertEqual(result['status'], 'PRE_CODEX_START_HARDLOCK_PASS')

        cases = (
            ('dispatcher_head_sha', 'c' * 40, 'PRECODEX_DISPATCHER_HEAD_DRIFT'),
            ('hardlock_base_status', 'FAIL', 'PRECODEX_HARDLOCK_BASE_NOT_FRESH_PASS'),
            ('codex_capacity_status', 'BLOCKED_USAGE_LIMIT', 'PRECODEX_CODEX_CAPACITY_NOT_AVAILABLE'),
            ('restart_recovery_status', 'LOCAL_ONLY', 'PRECODEX_RESTART_RECOVERY_NOT_READY'),
            ('durable_evidence_transport_status', 'BLOCKED', 'PRECODEX_DURABLE_EVIDENCE_TRANSPORT_NOT_PASS'),
            ('new_article_policy', 'RECOVERY_ALLOWED', 'PRECODEX_RECEIPT_NEW_ARTICLE_POLICY_INVALID'),
            ('publish_allowed', True, 'PRECODEX_RECEIPT_PUBLISH_NOT_FALSE'),
        )
        for field, value, expected in cases:
            bad = dict(receipt)
            bad[field] = value
            with self.subTest(field=field), self.assertRaisesRegex(
                guard.PreCodexStartBlocked,
                expected,
            ):
                guard.validate_payload(
                    head=head,
                    manifest=manifest,
                    receipt=bad,
                    state=state,
                    root=root,
                    state_sha256='b' * 64,
                )

    def test_legacy_root_start_is_hard_blocked(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            rc = root_entry.main(['root_entry.py', 'start', '/tmp/input.json', '/tmp/ws'])
        self.assertEqual(rc, 2)
        self.assertIn('SYSTEM4_ROOT_ENTRY_FAIL:MACHINE_ROUTE_BLOCK:POINT0_REQUIRED', out.getvalue())

    def test_legacy_root_start_stdin_is_hard_blocked(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            rc = root_entry.main(['root_entry.py', 'start-stdin', '/tmp/ws'])
        self.assertEqual(rc, 2)
        self.assertIn('SYSTEM4_ROOT_ENTRY_FAIL:MACHINE_ROUTE_BLOCK:POINT0_REQUIRED', out.getvalue())

    def test_direct_controller_stage_without_point0_route_is_blocked(self):
        with tempfile.TemporaryDirectory() as td:
            ws = Path(td) / 'ws'
            ws.mkdir()
            (ws / 'state.json').write_text('{}\n', encoding='utf-8')
            with self.assertRaisesRegex(controller.Fail, 'MACHINE_ROUTE_BLOCK:POINT0_JSON_MISSING'):
                controller._machine_route_lock('research', str(ws))

    def test_ingress_without_root_supervisor_binding_is_blocked(self):
        with tempfile.TemporaryDirectory() as td:
            ws = Path(td) / 'ws'
            ws.mkdir()
            with self.assertRaisesRegex(controller.Fail, 'MACHINE_ROUTE_BLOCK:POINT0_JSON_MISSING'):
                controller._machine_route_lock('ingress', str(ws))

    def test_ingress_with_existing_root_supervisor_route_is_allowed(self):
        with tempfile.TemporaryDirectory() as td:
            ws = Path(td) / 'ws'
            _touch_route(ws)
            with mock.patch.object(controller.root_supervisor_bridge, 'dispatch', return_value={'contract': 'worker'}):
                controller._machine_route_lock('ingress', str(ws))

    def test_post_ingress_requires_verified_worker_dispatch(self):
        with tempfile.TemporaryDirectory() as td:
            ws = Path(td) / 'ws'
            _touch_route(ws)
            (ws / 'state.json').write_text('{}\n', encoding='utf-8')
            with self.assertRaisesRegex(controller.Fail, 'MACHINE_ROUTE_BLOCK:WORKER_DISPATCH_MISSING'):
                controller._machine_route_lock('research', str(ws))

            (ws / 'worker_dispatch.json').write_text(json.dumps({'contract': 'stub'}), encoding='utf-8')
            with mock.patch.object(controller.root_entry, '_critical_manifest_sha256', return_value='a' * 64), \
                 mock.patch.object(controller.root_entry, '_git', return_value='b' * 40), \
                 mock.patch.object(controller.worker_dispatch, 'verify_bundle', return_value=({}, b'{}')), \
                 mock.patch.object(controller.supervisor, 'verify_controller_binding', return_value=None):
                controller._machine_route_lock('research', str(ws))

    def test_reconnected_parent_uses_current_point0_then_root_only_batch_start(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source_requests = root / 'source-requests.json'
            source_requests.write_text('{}\n', encoding='utf-8')
            runtime_root = root / 'runtime'
            runtime = {'batch_sha256': 'a' * 64}
            items = [{'plan_slot': 'b' * 64} for _ in range(7)]
            batch_result = json.dumps({
                'ok': True,
                'status': 'SYSTEM4_107007_BATCH_ROOT_READY_STOP',
                'batch_sha256': runtime['batch_sha256'],
                'item_count': 7,
                'item_index': 0,
                'completed_count': 0,
                'publish_allowed': False,
            })
            with mock.patch.object(parent_start, '_validate_current_source_requests', return_value=(runtime, items)), \
                 mock.patch.object(
                     parent_start,
                     '_run_checked',
                     side_effect=[
                         'SYSTEM4_MACHINE_POINT0_CURRENT_PASS:' + ('c' * 64),
                         batch_result,
                     ],
                 ) as runner:
                receipt = parent_start.start(
                    str(source_requests),
                    str(runtime_root),
                    'SYSTEM4_PARENT_MACHINE_HTTP_V2',
                )

            self.assertEqual(runner.call_count, 2)
            point0_cmd = runner.call_args_list[0].args[0]
            batch_cmd = runner.call_args_list[1].args[0]
            self.assertEqual(point0_cmd[1], str(parent_start.MACHINE_POINT0))
            self.assertIn('build-current-fetch', point0_cmd)
            self.assertEqual(batch_cmd[1], str(parent_start.BATCH_START))
            self.assertIn('start', batch_cmd)
            joined = ' '.join(point0_cmd + batch_cmd).lower()
            self.assertNotIn('codex_entry.py', joined)
            self.assertNotIn('worker-start', joined)
            self.assertNotIn('advance', joined)
            self.assertEqual(receipt['status'], 'SYSTEM4_PARENT_ROOT_READY_STOP')
            self.assertEqual(receipt['started_item_index'], 0)
            self.assertIs(receipt['root_only'], True)
            self.assertIs(receipt['codex_invoked'], False)
            self.assertIs(receipt['advance_invoked'], False)
            self.assertIs(receipt['publish_allowed'], False)


    def test_codex_root_override_matches_current_bound_parent_start(self):
        override = (parent_start.REPO / 'AGENTS.override.md').read_text(encoding='utf-8')
        self.assertIn(
            'python3 isolated_system4/parent_start.py start-current-bound',
            override,
        )
        self.assertIn('The first executable project production command is exactly:', override)
        self.assertIn(
            'No manual SOURCE_REQUESTS path, runtime-root path, workspace path, '
            'article index or provider argument may be supplied',
            override,
        )
        self.assertIn(
            'For current 107007, `parent_start.py start-current-bound` '
            'is the only allowed normal production entrance.',
            override,
        )
        self.assertIn(
            'python3 isolated_system4/root_entry.py start-point0 '
            '<POINT0_OUTSIDE_REPO> <WORKSPACE_OUTSIDE_REPO> <N>',
            override,
        )
        self.assertIn(
            'SYSTEM4 branch: DO NOT run `control/cloud-entry-gate/cloud_entry.py` '
            'before or instead of the System-4 root entry.',
            override,
        )
        self.assertNotIn(
            'This file exists only for the dedicated branch '
            '`hobbyroom/system4-true-single-room-v1`',
            override,
        )


    def test_real_current_parent_start_stops_at_root_index0(self):
        runtime, _, items = parent_start.entry.runtime_binding()
        self.assertEqual(len(items), 7)

        with mock.patch.object(
            parent_start.pre_codex_start_hardlock,
            'validate',
            return_value={
                'contract': 'PFERDE_ATELIER_PRE_CODEX_START_HARDLOCK_V1',
                'status': 'PRE_CODEX_START_HARDLOCK_PASS',
                'head': 'test',
                'approved_article_count': 7,
                'publish_allowed': False,
            },
        ):
            receipt = parent_start.start_bound()
        run_root = Path(receipt['run_root'])
        try:
            self.assertEqual(receipt['status'], 'SYSTEM4_PARENT_ROOT_READY_STOP')
            self.assertEqual(receipt['batch_sha256'], runtime['batch_sha256'])
            self.assertEqual(receipt['runtime_generation'], runtime['generation'])
            self.assertEqual(receipt['item_count'], 7)
            self.assertEqual(receipt['source_requests_item_count'], 7)
            self.assertEqual(receipt['started_item_index'], 0)
            self.assertIs(receipt['root_only'], True)
            self.assertIs(receipt['codex_invoked'], False)
            self.assertIs(receipt['advance_invoked'], False)
            self.assertIs(receipt['external_paths_auto_created'], True)
            self.assertIs(receipt['publish_allowed'], False)
            self.assertEqual(
                receipt['source_requests_bound_ref'],
                runtime['source_requests_ref'],
            )
            self.assertEqual(
                receipt['source_requests_bound_sha256'],
                runtime['source_requests_sha256'],
            )

            repo_root = parent_start.REPO.resolve()
            self.assertNotEqual(run_root.resolve(), repo_root)
            self.assertNotIn(repo_root, run_root.resolve().parents)

            source_requests = Path(receipt['source_requests'])
            self.assertTrue(source_requests.is_file())
            self.assertEqual(
                parent_start._sha256(source_requests),
                runtime['source_requests_sha256'],
            )

            batch_root = Path(receipt['batch_root'])
            batch_state = json.loads(
                (batch_root / 'SYSTEM4_107007_BATCH_STATE.json').read_text(encoding='utf-8')
            )
            self.assertEqual(batch_state['started_indices'], [0])
            self.assertEqual(batch_state['completed_indices'], [])
            self.assertEqual(batch_state['current_index'], 0)

            workspace = batch_root / 'item-000000'
            state = json.loads((workspace / 'state.json').read_text(encoding='utf-8'))
            self.assertEqual(state['phase'], 'RESEARCH_REQUIRED')
            self.assertIsNone(state['research'])
            self.assertIsNone(state['draft_markdown'])
            self.assertTrue((workspace / 'worker_dispatch.json').is_file())

            dispatch = json.loads((workspace / 'worker_dispatch.json').read_text(encoding='utf-8'))
            self.assertEqual(dispatch['worker_contract']['item_index'], 0)
            self.assertEqual(dispatch['worker_contract']['phase'], 'RESEARCH_REQUIRED')
            self.assertIs(dispatch['worker_contract']['publish_allowed'], False)
            print(
                'SYSTEM4_REAL_PARENT_BOUND_AUTOSTART_PROOF_PASS:'
                + runtime['batch_sha256']
                + ':generation=' + str(runtime['generation'])
                + ':source_requests_hash=' + runtime['source_requests_sha256']
                + ':SYSTEM4_ROOT_POINT0_PASS:WORKER_DISPATCH_READY'
                + ':SYSTEM4_107007_BATCH_ROOT_READY_STOP'
                + ':external_paths_auto_created=true'
                + ':worker_started=false'
            )
        finally:
            shutil.rmtree(run_root, ignore_errors=True)


if __name__ == '__main__':
    unittest.main(verbosity=2)
