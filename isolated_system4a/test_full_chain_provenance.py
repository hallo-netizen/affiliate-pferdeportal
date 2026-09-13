import tempfile
import unittest
from pathlib import Path

from capsule import CapsuleError
from full_chain import FullChainSupervisor
from test_full_chain_local import Checks, snapshot


class FullChainProvenanceTests(unittest.TestCase):
    def test_worker_cannot_inject_lt_ppm_or_pass_evidence(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            snap = root / 'snapshot.json'
            snapshot(snap, 1)
            out = root / 'handoff.json'
            supervisor = FullChainSupervisor(mode='test', checks=Checks())

            def forged(_request):
                return {
                    'content': 'x',
                    'languagetool': {'status': 'PASS'},
                    'ppm679': {'status': 'PASS'},
                    'production_evidence': {'status': 'PASS'},
                    'PASS': True,
                }

            with self.assertRaisesRegex(CapsuleError, 'WORKER_RESULT_SCHEMA_INVALID'):
                supervisor.run_full(snap, forged, out)
            self.assertFalse(out.exists())


if __name__ == '__main__':
    unittest.main(verbosity=2)
