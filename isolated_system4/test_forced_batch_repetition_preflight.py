from __future__ import annotations

import itertools
import unittest

import batch_repetition_guard
import content_guard
import full_route_test_worker
import global_workshop


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
        self.assertLess(max(pair_scores),0.10)

        bodies=[self._body(i) for i in range(4)]
        diversity=content_guard.validate_batch_distinctness(bodies)
        self.assertEqual(diversity['status'],'PASS')
        self.assertLess(diversity['max_pairwise_shingle_jaccard'],content_guard.MAX_PAIRWISE_SHINGLE_JACCARD)

        with self.assertRaises(batch_repetition_guard.BatchRepetitionError) as caught:
            batch_repetition_guard.validate_batch_repetition(bodies)
        exc=caught.exception
        self.assertTrue(str(exc).startswith('BATCH_REPEATED_SENTENCE_TEMPLATE_BLOCKED:7>6'))
        self.assertEqual(len(exc.findings),7)
        self.assertTrue(all(row.get('article_indexes')==[0,1,2,3] for row in exc.findings))

        request=global_workshop.build_request('BATCH',exc)
        self.assertTrue(request['repairable'])
        self.assertEqual(set(request['repair_targets']),{'3'})
        self.assertEqual(len(request['repair_targets']['3']),7)

        repaired=list(bodies)
        repaired[3]=full_route_test_worker._strip_forced_batch_repetition(repaired[3],3)
        after_diversity=content_guard.validate_batch_distinctness(repaired)
        self.assertEqual(after_diversity['status'],'PASS')
        after_repetition=batch_repetition_guard.validate_batch_repetition(repaired)
        self.assertEqual(after_repetition['status'],'PASS')
        self.assertLessEqual(after_repetition['majority_repeated_sentence_count'],6)


if __name__=='__main__':
    unittest.main(verbosity=2)
