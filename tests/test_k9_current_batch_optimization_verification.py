import tempfile, unittest
from pathlib import Path

import k9_terminal_preflight as terminal

ROOT=Path(__file__).resolve().parents[1]

class CurrentThreeArticleOptimizationVerification(unittest.TestCase):
    def test_completed_current_batch_is_terminal_ready_read_only(self):
        with tempfile.TemporaryDirectory() as td:
            out=Path(td)/"pserc.json"
            result=terminal.run(
                ROOT,
                ROOT/"quality/PORTAL_PRODUCTION_MACHINE_V6.7.9.zip",
                ROOT/"quality/PSERC-FIX.zip",
                out,
            )
        self.assertEqual(result["status"],"PASS")
        self.assertEqual(result["article_count"],3)
        self.assertEqual(result["active_intake_batch_sha256"],"7e432df903a68c6a1a0a08dedcffa005647917b690de34c5180cb0b27ac897d1")
        self.assertEqual(result["wordpress_ledger_readiness"],"PASS")

if __name__=="__main__": unittest.main()
