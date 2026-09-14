import unittest
from pathlib import Path
from full_chain import FullChainError, FullChainSupervisor

class ProductionAuthorityFailClosedTests(unittest.TestCase):
    def test_direct_production_callable_is_blocked_before_backend_worker_or_ingress(self):
        called=[]
        def worker(_request):
            called.append(True); return {"content":"must never run"}
        supervisor=FullChainSupervisor(mode="production")
        self.assertIsNone(supervisor._controller)
        with self.assertRaisesRegex(FullChainError,"PRODUCTION_REQUIRES_EXTERNAL_SUPERVISOR_HOST"):
            supervisor.run_full(Path("does-not-need-to-exist.json"),worker,Path("must-not-exist.json"))
        self.assertEqual(called,[])
        self.assertFalse(supervisor.status()["started"])
        self.assertIsNone(supervisor._controller)

if __name__=="__main__": unittest.main(verbosity=2)
