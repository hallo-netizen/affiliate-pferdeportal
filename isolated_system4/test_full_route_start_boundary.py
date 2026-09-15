from __future__ import annotations
import json,subprocess,sys,tempfile,unittest
from pathlib import Path

import full_route_start
from full_route_test_fixture import SINGLE_ITEMS,write_start_fixture

HERE=Path(__file__).resolve().parent
WORKER=[sys.executable,str(HERE/'full_route_test_worker.py')]
BAD_WORKER=[sys.executable,str(HERE/'full_route_bad_worker.py')]

class FullRouteStartBoundaryTests(unittest.TestCase):
    def test_negative_source_count_mismatch_blocks_before_workspace(self):
        with tempfile.TemporaryDirectory(prefix='s4-full-start-neg-count-') as td:
            root=Path(td);snap,sources=write_start_fixture(root,SINGLE_ITEMS)
            sources.write_text(json.dumps({'contract':'SYSTEM4_FULL_ROUTE_TEST_SOURCES_V1','articles':[]}),encoding='utf-8')
            out=root/'out'
            with self.assertRaisesRegex(full_route_start.FullRouteError,'START_SOURCE_COUNT_MISMATCH'):
                full_route_start.run(snap,sources,WORKER,out)
            self.assertFalse(out.exists())

    def test_negative_testworker_before_point0_dispatch_cannot_read_or_generate(self):
        with tempfile.TemporaryDirectory(prefix='s4-testworker-before-point0-') as td:
            root=Path(td); workspace=root/'not-armed'; workspace.mkdir(); out=root/'forbidden.json'
            cp=subprocess.run([*WORKER,'research',str(workspace),str(out),'0'],cwd=HERE.parent,text=True,capture_output=True,check=False)
            self.assertNotEqual(cp.returncode,0)
            self.assertIn('FULL_ROUTE_TEST_WORKER_FAIL:DISPATCH_REQUIRED',cp.stdout)
            self.assertFalse(out.exists())

    def test_executed_test_route_contains_no_codex_entry(self):
        for name in ('full_route_start.py','full_route_test_worker.py','test_local_end_to_end_chat_handoff.py'):
            text=(HERE/name).read_text(encoding='utf-8')
            self.assertNotIn('codex_entry',text,name)

    def test_negative_unbound_worker_research_blocks_after_real_worker_start(self):
        with tempfile.TemporaryDirectory(prefix='s4-full-start-neg-research-') as td:
            root=Path(td);snap,sources=write_start_fixture(root,SINGLE_ITEMS);out=root/'out'
            with self.assertRaisesRegex(full_route_start.FullRouteError,'START_RESEARCH_FAILED:0'):
                full_route_start.run(snap,sources,BAD_WORKER,out)
            state=json.loads((out/'item-0/state.json').read_text(encoding='utf-8'))
            self.assertEqual(state['phase'],'RESEARCH_REQUIRED')
            self.assertIsNone(state['research'])
            self.assertTrue((out/'item-0/worker_dispatch.json').is_file())

    def test_negative_missing_worker_command_blocks(self):
        with tempfile.TemporaryDirectory(prefix='s4-full-start-neg-worker-') as td:
            root=Path(td);snap,sources=write_start_fixture(root,SINGLE_ITEMS);out=root/'out'
            with self.assertRaises((FileNotFoundError,full_route_start.FullRouteError)):
                full_route_start.run(snap,sources,['/definitely/not/a/worker'],out)
            self.assertTrue((out/'item-0/worker_dispatch.json').is_file())

if __name__=='__main__':unittest.main(verbosity=2)
