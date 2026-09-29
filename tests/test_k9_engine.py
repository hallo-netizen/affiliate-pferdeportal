import hashlib
import importlib.util
import tempfile
import unittest
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "k9_engine.py"
spec = importlib.util.spec_from_file_location("k9_engine", SRC)
k = importlib.util.module_from_spec(spec)
spec.loader.exec_module(k)
ORIGINAL_CHAT_ENTRY = k.CHAT_ENTRY

class K9Tests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        k.ROOT = root
        k.LEDGER = root / "state/ledger.json"
        k.CURRENT_JOB = root / "runtime/CURRENT_JOB.json"
        k.CHAT_ENTRY = root / "runtime/CHAT_ENTRY.json"
        k.STATUS_FILE = root / "state/STATUS.json"
        k.WAREHOUSE = root / "warehouse"
        k.write_json(k.LEDGER, {"contract":"K9_LEDGER_V1","generation":1,"items":[]})
        intake = root / "intake.json"
        k.write_json(intake, {"items":[
            {"item_id":"a","title":"A","metadata":{"article_type":"Beratung","target_keyword":"ka","category":"kat-a"}},
            {"item_id":"b","title":"B","metadata":{"article_type":"Beratung","target_keyword":"kb","category":"kat-b"}}
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

    def research_row(self, iid):
        source_id=f"src-{iid}"
        fact_id=f"fact-{iid}"
        pack={
            "fact_pack_id":f"fp-{iid}",
            "domain":"pferdeportal",
            "article_type":"Beratung",
            "fact_ids":[fact_id],
            "status":"SOURCE_VERIFIED_PRODUCTION_READY",
            "claims":[{
                "fact_id":fact_id,
                "source_id":source_id,
                "locator":f"snapshot:snap-{iid}:lines:1-2",
                "statement":f"Belastbarer Fakt {iid}.",
                "claim_status":"FULLY_SUPPORTED",
                "subject_scope":f"subject-{iid}",
                "time_scope":"SOURCE_SCOPE",
                "article_types":["Beratung"]
            }],
            "fact_pack_hash":"a"*64,
            "source_manifest_hash":"b"*64,
            "claim_register_hash":"c"*64,
            "required_block_coverage":"PASS",
            "table_evidence_coverage":"PASS",
            "conclusion_evidence_coverage":"PASS",
            "article_type_coverage":"PASS",
            "temporal_validity_status":"PASS_RETRIEVAL_DATE_BOUND",
            "contradiction_status":"PASS_NO_DIRECT_CONTRADICTION_IN_ACTIVE_ATOMIC_FACTS",
            "production_readiness_status":"SOURCE_VERIFIED_PRODUCTION_READY",
            "placeholder_content_status":"PASS"
        }
        product={
            "contract":"K9_RESEARCH_PRODUCT_V1",
            "sources":[{
                "source_id":source_id,
                "url":f"https://example.org/{iid}",
                "title":f"Quelle {iid}"
            }],
            "fact_pack":pack
        }
        product["product_sha256"]=k.stable(product)
        return {"item_id":iid,"research_product":product}

    def article_row(self, iid, research_product, text=None):
        html=text or f"<section data-block='intro'><p>Artikel {iid}</p></section>"
        title=f"Artikel {iid}"
        ppm_item={
            "article_type":"Beratung",
            "source_snapshot_id":research_product["fact_pack"]["fact_pack_id"],
            "target_keyword":f"k{iid}",
            "runtime_order":{"order_id":f"order-{iid}"},
            "canonical_article":{
                "title":title,
                "body_html":html
            }
        }
        product={
            "contract":"K9_ARTICLE_PRODUCT_V1",
            "article_type":"Beratung",
            "title":title,
            "content_html":html,
            "content_sha256":hashlib.sha256(html.encode()).hexdigest(),
            "research_product_sha256":research_product["product_sha256"],
            "ppm_item":ppm_item
        }
        product["product_sha256"]=k.stable(product)
        return {"item_id":iid,"article_product":product}

    def check_row(self, iid, article_product, lt_status="PASS", ppm_status="PASS"):
        sha=article_product["content_sha256"]
        return {
            "item_id":iid,
            "lt68_result":{
                "contract":"K9_LT68_RESULT_V1",
                "status":lt_status,
                "engine":"LanguageTool 6.8",
                "jar_sha256":k.LT68_JAR_SHA256,
                "article_sha256":sha,
                "finding_count":0 if lt_status=="PASS" else 1,
                "findings":[]
            },
            "ppm679_result":{
                "contract":"K9_PPM679_RESULT_V1",
                "status":ppm_status,
                "ppm_version":"6.7.9",
                "ppm_package_sha256":k.PPM679_PACKAGE_SHA256,
                "content_sha256":sha,
                "errors":[] if ppm_status=="PASS" else [{"error_code":"TEST_FAIL"}]
            }
        }

    def finish_research(self, count=2):
        job=k.prepare("research",count)["job"]
        rows=[self.research_row(iid) for iid in job["item_ids"]]
        k.accept(self.submission(job,rows,"research.json"))
        return job

    def finish_write_one(self):
        self.finish_research(1)
        job=k.prepare("write",1)["job"]
        research=job["items"][0]["input_products"]["research"]["research_product"]
        row=self.article_row("a",research)
        k.accept(self.submission(job,[row],"write.json"))
        return job,row

    def test_module_defines_real_chat_entry_path(self):
        self.assertEqual(ORIGINAL_CHAT_ENTRY.name,"CHAT_ENTRY.json")

    def test_prepare_creates_exact_chat_entry(self):
        job=k.prepare("research",2)["job"]
        entry=k.load_json(k.CHAT_ENTRY)
        self.assertEqual(entry["contract"],"K9_CHAT_ENTRY_V1")
        self.assertEqual(entry["job_id"],job["job_id"])
        self.assertEqual(entry["job_sha256"],job["job_sha256"])
        self.assertEqual(entry["station"],"research")
        self.assertEqual(entry["job_path"],"runtime/CURRENT_JOB.json")
        self.assertEqual(entry["submission_path"],"submissions/"+job["job_id"]+".json")
        self.assertEqual(entry["output_contract"],"K9_RESEARCH_PRODUCT_V1")

    def test_accept_removes_chat_entry(self):
        job=k.prepare("research",1)["job"]
        self.assertTrue(k.CHAT_ENTRY.exists())
        k.accept(self.submission(job,[self.research_row("a")],"research-one.json"))
        self.assertFalse(k.CHAT_ENTRY.exists())

    def test_status_stamp_shows_done_and_remaining(self):
        initial=k.load_json(k.STATUS_FILE)
        self.assertEqual(initial["total"],2)
        self.assertEqual(initial["fully_done"],0)
        self.assertEqual(initial["remaining"],2)
        self.finish_research(1)
        after_research=k.load_json(k.STATUS_FILE)
        self.assertEqual(after_research["ready_for_write"],1)

    def test_restart_reuses_exact_job(self):
        first=k.prepare("research",2)["job"]
        second=k.prepare("research",2)["job"]
        self.assertEqual(first["job_id"],second["job_id"])
        self.assertEqual(first["job_sha256"],second["job_sha256"])

    def test_partial_package_blocked_without_state_change(self):
        job=k.prepare("research",2)["job"]
        before=k.load_json(k.LEDGER)
        bad=self.submission(job,[self.research_row("a")])
        with self.assertRaises(k.K9Error):
            k.accept(bad)
        self.assertEqual(before,k.load_json(k.LEDGER))
        self.assertTrue(k.CURRENT_JOB.exists())

    def test_research_unknown_source_is_blocked(self):
        job=k.prepare("research",1)["job"]
        row=self.research_row("a")
        row["research_product"]["fact_pack"]["claims"][0]["source_id"]="src-unknown"
        core=dict(row["research_product"]); core.pop("product_sha256")
        row["research_product"]["product_sha256"]=k.stable(core)
        with self.assertRaisesRegex(k.K9Error,"RESEARCH_CLAIM_SOURCE_UNKNOWN"):
            k.accept(self.submission(job,[row],"bad-research.json"))

    def test_write_job_contains_complete_hash_bound_research_product(self):
        self.finish_research(2)
        job=k.prepare("write",2)["job"]
        by_id={x["item_id"]:x for x in job["items"]}
        ra=by_id["a"]["input_products"]["research"]["research_product"]
        rb=by_id["b"]["input_products"]["research"]["research_product"]
        self.assertEqual(ra["fact_pack"]["fact_ids"],["fact-a"])
        self.assertEqual(rb["sources"][0]["source_id"],"src-b")
        self.assertEqual(ra["product_sha256"],k.stable({x:y for x,y in ra.items() if x!="product_sha256"}))
        self.assertTrue(by_id["a"]["input_product_refs"]["research"]["path"].startswith("warehouse/research/"))

    def test_article_wrong_research_binding_is_blocked(self):
        self.finish_research(1)
        job=k.prepare("write",1)["job"]
        research=job["items"][0]["input_products"]["research"]["research_product"]
        row=self.article_row("a",research)
        row["article_product"]["research_product_sha256"]="0"*64
        core=dict(row["article_product"]); core.pop("product_sha256")
        row["article_product"]["product_sha256"]=k.stable(core)
        with self.assertRaisesRegex(k.K9Error,"ARTICLE_RESEARCH_BINDING_MISMATCH"):
            k.accept(self.submission(job,[row],"bad-write.json"))

    def test_other_station_cannot_steal_open_job(self):
        k.prepare("research",1)
        with self.assertRaises(k.K9Error):
            k.prepare("write",1)

    def test_check_job_contains_article_and_research(self):
        _,article_row=self.finish_write_one()
        check=k.prepare("check",1)["job"]
        inp=check["items"][0]["input_products"]
        self.assertEqual(inp["article"]["article_product"]["content_sha256"],article_row["article_product"]["content_sha256"])
        self.assertEqual(inp["research"]["research_product"]["fact_pack"]["fact_ids"],["fact-a"])

    def test_fake_boolean_check_is_rejected(self):
        self.finish_write_one()
        check=k.prepare("check",1)["job"]
        fake={"item_id":"a","lt68_pass":True,"ppm679_pass":True}
        with self.assertRaises(k.K9Error):
            k.accept(self.submission(check,[fake],"fake-check.json"))

    def test_check_wrong_article_hash_is_rejected(self):
        _,article_row=self.finish_write_one()
        check=k.prepare("check",1)["job"]
        row=self.check_row("a",article_row["article_product"])
        row["lt68_result"]["article_sha256"]="0"*64
        with self.assertRaisesRegex(k.K9Error,"CHECK_LT68_BINDING_INVALID"):
            k.accept(self.submission(check,[row],"wrong-hash-check.json"))

    def test_check_fail_routes_to_repair_with_complete_inputs(self):
        _,article_row=self.finish_write_one()
        check=k.prepare("check",1)["job"]
        row=self.check_row("a",article_row["article_product"],ppm_status="REPAIR_REQUIRED")
        k.accept(self.submission(check,[row],"check.json"))
        repair=k.prepare("repair",1)["job"]
        inp=repair["items"][0]["input_products"]
        self.assertEqual(inp["article"]["article_product"]["content_sha256"],article_row["article_product"]["content_sha256"])
        self.assertEqual(inp["failed_check"]["ppm679_result"]["status"],"REPAIR_REQUIRED")
        self.assertEqual(inp["research"]["research_product"]["fact_pack"]["fact_ids"],["fact-a"])

    def test_recheck_after_repair_uses_repaired_article(self):
        _,article_row=self.finish_write_one()
        check=k.prepare("check",1)["job"]
        row=self.check_row("a",article_row["article_product"],lt_status="REPAIR_REQUIRED")
        k.accept(self.submission(check,[row],"check1.json"))
        repair=k.prepare("repair",1)["job"]
        research=repair["items"][0]["input_products"]["research"]["research_product"]
        repaired=self.article_row("a",research,text="<section data-block='intro'><p>Artikel A repariert</p></section>")
        k.accept(self.submission(repair,[repaired],"repair.json"))
        recheck=k.prepare("check",1)["job"]
        self.assertEqual(
            recheck["items"][0]["input_products"]["article"]["article_product"]["content_sha256"],
            repaired["article_product"]["content_sha256"]
        )
        self.assertEqual(recheck["items"][0]["revision"],1)

    def test_tampered_warehouse_product_is_blocked(self):
        self.finish_research(1)
        data=k.ledger()
        ref=data["items"][0]["products"]["research"]
        package=k.load_json(k.ROOT/ref["path"])
        package["results"][0]["research_product"]["fact_pack"]["claims"][0]["statement"]="tampered"
        k.write_json(k.ROOT/ref["path"],package)
        with self.assertRaisesRegex(k.K9Error,"INPUT_PRODUCT_HASH_MISMATCH"):
            k.prepare("write",1)

    def test_duplicate_intake_blocked(self):
        path=k.ROOT/"duplicate.json"
        k.write_json(path,{"items":[{"item_id":"a","title":"A2"}]})
        with self.assertRaises(k.K9Error):
            k.import_intake(path)

if __name__=="__main__":
    unittest.main()
