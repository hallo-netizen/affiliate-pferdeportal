from __future__ import annotations
import json,subprocess,sys,tempfile,unittest
from pathlib import Path
from unittest import mock

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

    def test_repairable_batch_workshop_repairs_rechecks_and_recollects(self):
        with tempfile.TemporaryDirectory(prefix='s4-full-batch-workshop-') as td:
            root=Path(td); workspace=root/'item-0'; workspace.mkdir(); state_path=workspace/'state.json'; state_path.write_text('{}',encoding='utf-8')
            states=[{'old':True}]
            request={'repairable':True,'request_sha256':'a'*64,'error_code':'BATCH_REPEATED_SENTENCE_TEMPLATE_BLOCKED:7>6'}
            workshop=full_route_start.batch_gate.BatchGateWorkshop(RuntimeError(request['error_code']),request,root/'batch/GLOBAL_WORKSHOP_REQUEST.json',[0])
            route={'status':'SAME_ARTICLE_BODY_REPAIR','owner':'DRAFT_BODY','target':'SAME_ARTICLE_BODY'}
            repaired={'phase':'OUTPUT_GATE_REQUIRED','checks':{'status':'PASS'}}
            with mock.patch.object(full_route_start.batch_gate,'collect_batch',side_effect=[workshop,{'status':'SYSTEM4_BATCH_FULL_PASS_COLLECTED'}]) as collect, \
                 mock.patch.object(full_route_start.repair_router,'route',return_value=route) as routed, \
                 mock.patch.object(full_route_start.repair_router,'verify_continuation_result'), \
                 mock.patch.object(full_route_start,'_run_worker') as worker, \
                 mock.patch.object(full_route_start.controller,'main',return_value=0) as controller_main, \
                 mock.patch.object(full_route_start,'_fullcheck_with_existing_repair_loop',return_value=repaired) as fullcheck:
                result=full_route_start._batch_collect_with_workshop(WORKER,root/'snapshot.json',[state_path],states,root)
            self.assertEqual(result['status'],'SYSTEM4_BATCH_FULL_PASS_COLLECTED')
            self.assertEqual(states[0],repaired)
            self.assertEqual(collect.call_count,2)
            routed.assert_called_once_with(workspace)
            worker.assert_called_once()
            controller_main.assert_called_once()
            fullcheck.assert_called_once()

    def test_repairable_batch_workshop_without_article_target_is_continuation(self):
        with tempfile.TemporaryDirectory(prefix='s4-full-batch-workshop-no-target-') as td:
            root=Path(td)
            request={'repairable':True,'request_sha256':'b'*64,'error_code':'REPAIR_REQUIRED'}
            workshop=full_route_start.batch_gate.BatchGateWorkshop(RuntimeError('REPAIR_REQUIRED'),request,None,[])
            with mock.patch.object(full_route_start.batch_gate,'collect_batch',side_effect=workshop):
                with self.assertRaisesRegex(full_route_start.FullRouteContinuation,'START_BATCH_WORKSHOP_CONTINUATION_REQUIRED'):
                    full_route_start._batch_collect_with_workshop(WORKER,root/'snapshot.json',[],[],root)

if __name__=='__main__':unittest.main(verbosity=2)
