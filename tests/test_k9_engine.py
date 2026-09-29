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
        k.CHAT_ENTRY = root / "runtime/CHAT_ENTRY.json"
        k.WAREHOUSE = root / "warehouse"
        k.write_json(k.LEDGER, {"contract":"K9_LEDGER_V1","generation":1,"items":[]})
        intake = root / "intake.json"
        k.write_json(intake, {"items":[
            {"item_id":"a","title":"A","metadata":{"keyword":"ka"}},
            {"item_id":"b","title":"B","metadata":{"keyword":"kb"}}
        ]})
        k.import_intake(intake)

    def tearDown(self):
        self.tmp.cleanup()

    def submission(self, job, results, name="submission.json"):
        path = k.ROOT / name
        k.write_json(path, {
            "contract":"K9_SUBMISSION_V1",
            "job_id":job["job_id"],
            "station":job["station"],
            "results":results
        })
        return path

    def finish_research(self, count=2):
        job = k.prepare("research", count)["job"]
        rows = []
        for iid in job["item_ids"]:
            rows.append({"item_id":iid,"facts":[f"fact-{iid}"],"sources":[f"source-{iid}"]})
        k.accept(self.submission(job, rows, "research.json"))
        return job

    def finish_write_one(self):
        self.finish_research(1)
        job = k.prepare("write", 1)["job"]
        self.assertEqual(job["items"][0]["input_products"]["research"]["facts"], ["fact-a"])
        k.accept(self.submission(job, [{"item_id":"a","article_text":"Artikel A"}], "write.json"))
        return job

    def test_prepare_creates_exact_chat_entry(self):
        job = k.prepare("research", 2)["job"]
        entry = k.load_json(k.CHAT_ENTRY)
        self.assertEqual(entry["contract"], "K9_CHAT_ENTRY_V1")
        self.assertEqual(entry["job_id"], job["job_id"])
        self.assertEqual(entry["job_sha256"], job["job_sha256"])
        self.assertEqual(entry["station"], "research")
        self.assertEqual(entry["job_path"], "runtime/CURRENT_JOB.json")

    def test_accept_removes_chat_entry(self):
        job = k.prepare("research", 1)["job"]
        self.assertTrue(k.CHAT_ENTRY.exists())
        good = self.submission(job, [{"item_id":"a","facts":["x"],"sources":["s"]}], "research-one.json")
        k.accept(good)
        self.assertFalse(k.CHAT_ENTRY.exists())

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

    def test_write_job_contains_complete_research_product(self):
        self.finish_research(2)
        job = k.prepare("write", 2)["job"]
        by_id = {x["item_id"]:x for x in job["items"]}
        self.assertEqual(by_id["a"]["input_products"]["research"]["facts"], ["fact-a"])
        self.assertEqual(by_id["b"]["input_products"]["research"]["sources"], ["source-b"])
        self.assertTrue(by_id["a"]["input_product_refs"]["research"]["path"].startswith("warehouse/research/"))

    def test_other_station_cannot_steal_open_job(self):
        k.prepare("research", 1)
        with self.assertRaises(k.K9Error):
            k.prepare("write", 1)

    def test_check_job_contains_article_and_research(self):
        self.finish_write_one()
        check = k.prepare("check", 1)["job"]
        inp = check["items"][0]["input_products"]
        self.assertEqual(inp["article"]["article_text"], "Artikel A")
        self.assertEqual(inp["research"]["facts"], ["fact-a"])

    def test_check_fail_routes_to_repair_with_complete_inputs(self):
        self.finish_write_one()
        check = k.prepare("check", 1)["job"]
        k.accept(self.submission(check, [{"item_id":"a","lt68_pass":True,"ppm679_pass":False}], "check.json"))
        repair = k.prepare("repair", 1)["job"]
        inp = repair["items"][0]["input_products"]
        self.assertEqual(inp["article"]["article_text"], "Artikel A")
        self.assertFalse(inp["failed_check"]["ppm679_pass"])
        self.assertEqual(inp["research"]["facts"], ["fact-a"])

    def test_recheck_after_repair_uses_repaired_article(self):
        self.finish_write_one()
        check = k.prepare("check", 1)["job"]
        k.accept(self.submission(check, [{"item_id":"a","lt68_pass":False,"ppm679_pass":True}], "check1.json"))
        repair = k.prepare("repair", 1)["job"]
        k.accept(self.submission(repair, [{"item_id":"a","article_text":"Artikel A repariert"}], "repair.json"))
        recheck = k.prepare("check", 1)["job"]
        self.assertEqual(recheck["items"][0]["input_products"]["article"]["article_text"], "Artikel A repariert")
        self.assertEqual(recheck["items"][0]["revision"], 1)

    def test_tampered_warehouse_product_is_blocked(self):
        self.finish_research(1)
        data = k.ledger()
        ref = data["items"][0]["products"]["research"]
        package = k.load_json(k.ROOT / ref["path"])
        package["results"][0]["facts"] = ["tampered"]
        k.write_json(k.ROOT / ref["path"], package)
        with self.assertRaisesRegex(k.K9Error, "INPUT_PRODUCT_HASH_MISMATCH"):
            k.prepare("write", 1)

    def test_duplicate_intake_blocked(self):
        path = k.ROOT / "duplicate.json"
        k.write_json(path, {"items":[{"item_id":"a","title":"A2"}]})
        with self.assertRaises(k.K9Error):
            k.import_intake(path)

if __name__ == "__main__":
    unittest.main()
