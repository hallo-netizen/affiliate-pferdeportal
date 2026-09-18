from __future__ import annotations

import contextlib
import io
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import controller
import parent_start
import root_entry

REPO = Path(__file__).resolve().parent.parent
_BATCH_SPEC = importlib.util.spec_from_file_location(
    'system4_107007_batch_tested',
    REPO / 'control/startmaster0107/system4_107007_batch.py',
)
assert _BATCH_SPEC and _BATCH_SPEC.loader
system4_batch = importlib.util.module_from_spec(_BATCH_SPEC)
_BATCH_SPEC.loader.exec_module(system4_batch)


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


    def test_batch_advance_requires_exact_five_field_article_identity(self):
        item = {
            'title': 'Title A',
            'target_keyword': 'Keyword A',
            'category': 'Category A',
            'article_type': 'Beratung',
            'plan_slot': 'a' * 64,
        }
        with tempfile.TemporaryDirectory() as td:
            batch_root = Path(td)
            workspace = batch_root / 'item-000000'
            workspace.mkdir()
            state = {
                'phase': 'OUTPUT_GATE_REQUIRED',
                'checks': {'status': 'PASS'},
                'article': dict(item),
            }
            (workspace / 'state.json').write_text(
                json.dumps(state, ensure_ascii=False, sort_keys=True) + '\n',
                encoding='utf-8',
            )
            self.assertTrue(system4_batch._item_passed(batch_root, 0, item))

            replacements = {
                'title': 'Title B',
                'target_keyword': 'Keyword B',
                'category': 'Category B',
                'article_type': 'FAQ',
                'plan_slot': 'b' * 64,
            }
            for field, bad_value in replacements.items():
                broken = json.loads(json.dumps(state))
                broken['article'][field] = bad_value
                (workspace / 'state.json').write_text(
                    json.dumps(broken, ensure_ascii=False, sort_keys=True) + '\n',
                    encoding='utf-8',
                )
                self.assertFalse(
                    system4_batch._item_passed(batch_root, 0, item),
                    field + ' drift must block advance',
                )


    def test_real_current_parent_start_stops_at_root_index0(self):
        runtime, _, items = parent_start.entry.runtime_binding()
        self.assertEqual(len(items), 7)
        source_by_slot = {
            '9c229b0e6a784a482575e3deb16d105e3b5355becbbbb8ecfc8e1f600b529c56': {
                'source_id': 'fn-stangen-cavaletti',
                'source_title': 'Online-Seminar: Mehr Losgelassenheit durch den Einsatz von Stangen und Cavaletti',
                'source_url': 'https://app.pferd-aktuell.de/eticketing/onlineseminar/11-11-2026/mehr-losgelassenheit-durch-den-einsatz-von-stangen-und-cavaletti/1985',
                'source_kind': 'WEB',
            },
            '6ce9a1e47446daf84e85f08e84c33ada214f92612a654d79e68df18ea4e9fa19': {
                'source_id': 'rieste-reitplatzbeleuchtung',
                'source_title': 'Reitplatzbeleuchtung mit LED: Optimale Sicht für Reiter - RIESTE Licht',
                'source_url': 'https://www.rieste.com/l/reitplatzbeleuchtung-led-reitplatz-flutlicht',
                'source_kind': 'WEB',
            },
            '7b0e8f8b0653eb3a40aee2a68f4b9909df9d8bda374db0ec8c49e7b53ecbee87': {
                'source_id': 'lwk-festmistlager',
                'source_title': 'Bauberatung - Landwirtschaftskammer Nordrhein-Westfalen',
                'source_url': 'https://www.landwirtschaftskammer.de/Landwirtschaft/technik/bauberatung/index.htm',
                'source_kind': 'WEB',
            },
            '5999b9b00de2a1756101c5ebfb2b547c6ff2b9360bd9bae0988696a795ff6288': {
                'source_id': 'vhv-fremdreiter',
                'source_title': 'Pferde-Haftpflichtversicherung | VHV',
                'source_url': 'https://www.vhv.de/tierhalterhaftpflicht-versicherung/ratgeber/pferdehaftpflicht',
                'source_kind': 'WEB',
            },
            '7f7a0b4169c19676b3dfe6457ac07c6685ae6ead6c1873a9467d9b6ee32a81da': {
                'source_id': 'fn-huffett-hufpflege',
                'source_title': 'Behandlung von Krankheiten und Verletzungen beim Pferd | FN',
                'source_url': 'https://app.pferd-aktuell.de/turniersport/anti-doping-und-medikation/behandlung-von-krankheiten-und-verletzungen',
                'source_kind': 'WEB',
            },
            '8c8408cebf7f41becc33cdccf04b60387cf75644468a887730a8d18a4a1a7648': {
                'source_id': 'fn-fliegenmaske',
                'source_title': 'FN-Turniertalk: Der Ausrüstungskatalog im Fokus',
                'source_url': 'https://app.pferd-aktuell.de/news/aktuelle-meldungen/sport/fn-turniertalk-der-ausruestungskatalog-im-fokus',
                'source_kind': 'WEB',
            },
            '906ddc4ee72429a8544da018e1f78d63cb2b80c1f11488180f381e2dc16c4af5': {
                'source_id': 'lwk-pellets',
                'source_title': 'Ergänzungsfutter für Stuten und Fohlen - Landwirtschaftskammer Nordrhein-Westfalen',
                'source_url': 'https://www.landwirtschaftskammer.de/landwirtschaft/tierproduktion/pferdehaltung/fuetterung/vft-2018-063.htm',
                'source_kind': 'WEB',
            },
        }
        request_items = []
        for index, item in enumerate(items):
            slot = item['plan_slot']
            self.assertIn(slot, source_by_slot)
            request_items.append({
                'item_index': index,
                'plan_slot': slot,
                'sources': [source_by_slot[slot]],
            })
        request = {
            'contract': parent_start.SOURCE_CONTRACT,
            'item_count': len(request_items),
            'items': request_items,
        }

        with tempfile.TemporaryDirectory(prefix='system4-real-parent-start-') as td:
            root = Path(td)
            source_requests = root / 'source-requests.json'
            source_requests.write_text(
                json.dumps(request, ensure_ascii=False, indent=2, sort_keys=True) + '\n',
                encoding='utf-8',
            )
            runtime_root = root / 'runtime'
            receipt = parent_start.start(
                str(source_requests),
                str(runtime_root),
                'SYSTEM4_PARENT_MACHINE_HTTP_V2',
            )

            self.assertEqual(receipt['status'], 'SYSTEM4_PARENT_ROOT_READY_STOP')
            self.assertEqual(receipt['batch_sha256'], runtime['batch_sha256'])
            self.assertEqual(receipt['item_count'], 7)
            self.assertEqual(receipt['started_item_index'], 0)
            self.assertIs(receipt['root_only'], True)
            self.assertIs(receipt['codex_invoked'], False)
            self.assertIs(receipt['advance_invoked'], False)
            self.assertIs(receipt['publish_allowed'], False)

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
                'SYSTEM4_REAL_PARENT_ROOT_PROOF_PASS:'
                + parent_start.entry.REPO.joinpath('.git').as_posix()
                + ':SYSTEM4_ROOT_POINT0_PASS:WORKER_DISPATCH_READY'
                + ':SYSTEM4_107007_BATCH_ROOT_READY_STOP'
                + ':worker_started=false'
            )


if __name__ == '__main__':
    unittest.main(verbosity=2)
