import importlib.util, tempfile, unittest
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "k9_engine.py"
spec = importlib.util.spec_from_file_location("k9_engine", SRC)
k = importlib.util.module_from_spec(spec)
spec.loader.exec_module(k)

class K9Tests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        k.ROOT = root
        k.LEDGER = root / "state/ledger.json"
        k.CURRENT_JOB = root / "runtime/CURRENT_JOB.json"
        k.WAREHOUSE = root / "warehouse"
        k.write_json(k.LEDGER, {"contract":"K9_LEDGER_V1","generation":1,"items":[]})
        intake = root / "intake.json"
        k.write_json(intake, {"items":[{"item_id":"a","title":"A"},{"item_id":"b","title":"B"}]})
        k.import_intake(intake)

    def tearDown(self):
        self.tmp.cleanup()

    def submission(self, job, results):
        path = k.ROOT / "submission.json"
        k.write_json(path, {
            "contract":"K9_SUBMISSION_V1",
            "job_id":job["job_id"],
            "station":job["station"],
            "results":results
        })
        return path

    def test_restart_reuses_exact_job(self):
        first = k.prepare("research", 2)["job"]
        second = k.prepare("research", 2)["job"]
        self.assertEqual(first["job_id"], second["job_id"])
        self.assertEqual(first["job_sha256"], second["job_sha256"])

    def test_partial_package_blocked_without_state_change(self):
        job = k.prepare("research", 2)["job"]
        before = k.load_json(k.LEDGER)
        bad = self.submission(job, [{"item_id":"a","facts":["x"],"sources":["s"]}])
        with self.assertRaises(k.K9Error):
            k.accept(bad)
        self.assertEqual(before, k.load_json(k.LEDGER))
        self.assertTrue(k.CURRENT_JOB.exists())

    def test_completed_research_unlocks_write_only_after_accept(self):
        job = k.prepare("research", 2)["job"]
        good = self.submission(job, [
            {"item_id":"a","facts":["x"],"sources":["s"]},
            {"item_id":"b","facts":["y"],"sources":["t"]}
        ])
        k.accept(good)
        write_job = k.prepare("write", 2)["job"]
        self.assertEqual(set(write_job["item_ids"]), {"a","b"})

    def test_other_station_cannot_steal_open_job(self):
        k.prepare("research", 1)
        with self.assertRaises(k.K9Error):
            k.prepare("write", 1)

    def test_check_fail_routes_to_repair_as_new_station_product(self):
        research = k.prepare("research", 1)["job"]
        k.accept(self.submission(research, [{"item_id":"a","facts":["x"],"sources":["s"]}]))
        write = k.prepare("write", 1)["job"]
        k.accept(self.submission(write, [{"item_id":"a","article_text":"Artikel"}]))
        check = k.prepare("check", 1)["job"]
        k.accept(self.submission(check, [{"item_id":"a","lt68_pass":True,"ppm679_pass":False}]))
        repair = k.prepare("repair", 1)["job"]
        self.assertEqual(repair["item_ids"], ["a"])

    def test_duplicate_intake_blocked(self):
        path = k.ROOT / "duplicate.json"
        k.write_json(path, {"items":[{"item_id":"a","title":"A2"}]})
        with self.assertRaises(k.K9Error):
            k.import_intake(path)

if __name__ == "__main__":
    unittest.main()
