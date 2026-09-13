import sys, tempfile, unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
SYSTEM4=ROOT/'isolated_system4'
if str(SYSTEM4) not in sys.path: sys.path.insert(0,str(SYSTEM4))

import batch_gate
import test_batch_gate as system4_batch_fixture

class System4StateAuthorityGapProof(unittest.TestCase):
    def test_batch_gate_accepts_system4_own_synthetic_full_pass_fixture(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            snapshot,states=system4_batch_fixture.make_fixture(root,count=1)
            result=batch_gate.collect_batch(snapshot,states,root/'out')
        self.assertEqual(result['status'],'SYSTEM4_BATCH_FULL_PASS_COLLECTED')
        self.assertEqual(result['article_count'],1)

if __name__=='__main__': unittest.main(verbosity=2)
