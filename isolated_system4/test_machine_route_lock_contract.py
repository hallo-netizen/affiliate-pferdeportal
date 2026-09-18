from __future__ import annotations

import contextlib
import io
import json
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


if __name__ == '__main__':
    unittest.main(verbosity=2)
