from __future__ import annotations

import itertools
import json
import os
import unittest
from pathlib import Path

import batch_repetition_guard
import content_guard
import full_route_test_worker
import global_workshop
import production_checks


class ForcedBatchRepetitionPreflightTests(unittest.TestCase):
    def _body(self,index:int)->str:
        unique=' '.join(f'eigen{index}_{n}' for n in range(80))
        forced=full_route_test_worker._forced_batch_repeat_text(index)
        return f'<article><p>{unique}. {forced}</p></article>'

    def test_forced_fixture_hits_repetition_guard_not_pairwise_guard_and_repairs(self):
        forced=[full_route_test_worker._forced_batch_repeat_text(i) for i in range(4)]
        pair_scores=[
            content_guard.pairwise_shingle_jaccard(forced[left],forced[right])
            for left,right in itertools.combinations(range(4),2)
        ]
        self.assertLess(max(pair_scores),0.12)

        bodies=[self._body(i) for i in range(4)]
        diversity=content_guard.validate_batch_distinctness(bodies)
        self.assertEqual(diversity['status'],'PASS')
        self.assertLess(diversity['max_pairwise_shingle_jaccard'],content_guard.MAX_PAIRWISE_SHINGLE_JACCARD)

        expected=len(full_route_test_worker.BATCH_REPEAT_SENTENCES)
        self.assertGreaterEqual(expected,8)
        with self.assertRaises(batch_repetition_guard.BatchRepetitionError) as caught:
            batch_repetition_guard.validate_batch_repetition(bodies)
        exc=caught.exception
        self.assertTrue(str(exc).startswith(
            f'BATCH_REPEATED_SENTENCE_TEMPLATE_BLOCKED:{expected}>{batch_repetition_guard.MAX_MAJORITY_REPEATED_SENTENCES}'
        ))
        self.assertEqual(len(exc.findings),expected)
        self.assertTrue(all(row.get('article_indexes')==[0,1,2,3] for row in exc.findings))

        request=global_workshop.build_request('BATCH',exc)
        self.assertTrue(request['repairable'])
        self.assertEqual(set(request['repair_targets']),{'3'})
        self.assertEqual(len(request['repair_targets']['3']),expected)

        for lost_sentence in full_route_test_worker.BATCH_REPEAT_SENTENCES:
            degraded=[body.replace(lost_sentence,'',1) for body in bodies]
            diversity_after_loss=content_guard.validate_batch_distinctness(degraded)
            self.assertEqual(diversity_after_loss['status'],'PASS')
            with self.assertRaises(batch_repetition_guard.BatchRepetitionError) as lost:
                batch_repetition_guard.validate_batch_repetition(degraded)
            self.assertEqual(len(lost.exception.findings),expected-1)

        repaired=list(bodies)
        repaired[3]=full_route_test_worker._strip_forced_batch_repetition(repaired[3],3)
        after_diversity=content_guard.validate_batch_distinctness(repaired)
        self.assertEqual(after_diversity['status'],'PASS')
        after_repetition=batch_repetition_guard.validate_batch_repetition(repaired)
        self.assertEqual(after_repetition['status'],'PASS')
        self.assertLessEqual(after_repetition['majority_repeated_sentence_count'],6)

    def test_fresh_variation_indices_keep_first_four_template_residues_separate(self):
        old=os.environ.get(full_route_test_worker.RUN_NONCE_ENV)
        os.environ[full_route_test_worker.RUN_NONCE_ENV]='system4-forced-batch-preflight-nonce'
        try:
            values=[full_route_test_worker._fresh_variation_index(i) for i in range(4)]
        finally:
            if old is None: os.environ.pop(full_route_test_worker.RUN_NONCE_ENV,None)
            else: os.environ[full_route_test_worker.RUN_NONCE_ENV]=old
        self.assertEqual(len(set(values)),4)
        self.assertEqual(len({value%8 for value in values}),4)
        self.assertEqual(len({value%24 for value in values}),4)

    @unittest.skipUnless(os.environ.get('SYSTEM4_REAL_TOOL_CORRIDOR')=='1','real LT 6.8 preflight is an explicit CI stage')
    def test_forced_fixture_is_real_languagetool_68_clean(self):
        repo=Path(__file__).resolve().parent.parent
        for index in range(4):
            forced=full_route_test_worker._forced_batch_repeat_text(index)
            body=f'<article><p>Der vorhandene Absatz endet hier. {forced}</p></article>'
            try:
                result=production_checks.run_languagetool(repo,body)
            except production_checks.RepairRequired as exc:
                self.fail(
                    'FORCED_BATCH_LT68_NOT_CLEAN:'+str(index)+':'+
                    json.dumps(exc.findings,ensure_ascii=False,sort_keys=True,separators=(',',':'))
                )
            self.assertEqual(result['status'],'PASS')
            self.assertEqual(result['engine'],'LanguageTool 6.8 / Bestand 43')
            self.assertEqual(result['finding_count'],0)


if __name__=='__main__':
    unittest.main(verbosity=2)
