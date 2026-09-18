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
