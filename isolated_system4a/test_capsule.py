import hashlib
import json
import unittest

from capsule import CapsuleController, CapsuleError


def sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


class MockChecks:
    def __init__(self):
        self.fullcheck_fail = False
        self.bad_research_hash = False
        self.batch_calls = 0

    def research(self, text):
        return {"status": "PASS", "sha256": "0" * 64 if self.bad_research_hash else sha(text)}

    def facts(self, text, research):
        if research != "research":
            raise AssertionError("facts did not receive bound research")
        return {"status": "PASS", "sha256": sha(text)}

    def context(self, text, **kwargs):
        if kwargs["research_text"] != "research" or kwargs["facts_text"] != "facts":
            raise AssertionError("context did not receive bound research/facts")
        return {
            "status": "PASS",
            "sha256": sha(text),
            "fact_pack": {"contract": "mock-pack", "marker": "immutable-context"},
            "production_plan_item": {"marker": "immutable-plan"},
        }

    def draft(self, text, **kwargs):
        if kwargs["fact_pack"].get("marker") != "immutable-context":
            raise AssertionError("draft did not receive bound fact pack")
        return {"status": "PASS", "sha256": sha(text)}

    def repair(self, old, new, **kwargs):
        if not old or old == new:
            raise AssertionError("repair continuity input invalid")
        return {"status": "PASS", "sha256": sha(new)}

    def fullcheck(self, text, **kwargs):
        if self.fullcheck_fail:
            return {
                "status": "FAIL",
                "checked_sha256": sha(text),
                "checker": "mock-real-checker",
                "findings": [{"error_code": "EXACT_FINDING"}],
            }
        return {
            "status": "PASS",
            "checked_sha256": sha(text),
            "evidence": {"marker": "real-checker-evidence-placeholder"},
        }

    def batch(self, bodies):
        self.batch_calls += 1
        if not bodies:
            raise AssertionError("empty batch")
        return {"status": "PASS", "article_count": len(bodies)}


class CapsuleTests(unittest.TestCase):
    def setUp(self):
        self.checks = MockChecks()
        self.key = b"k" * 32
        self.controller = CapsuleController(self.key, self.checks)
        self.article = {
            "title": "Titel",
            "target_keyword": "Keyword",
            "category": "kategorie",
            "article_type": "Beliebiger autoritativ definierter Typ",
            "plan_slot": "a" * 64,
        }
        self.cid = self.controller.create(self.article, "b" * 64, "c" * 64)

    def advance_to_context(self):
        self.controller.submit_research(self.cid, "research")
        self.controller.submit_facts(self.cid, "facts")
        self.controller.submit_context(self.cid, "context")

    def advance_to_draft(self):
        self.advance_to_context()
        self.controller.submit_draft(self.cid, "draft-v1")

    def test_happy_single_article_to_frozen_export(self):
        self.advance_to_draft()
        self.controller.fullcheck(self.cid)
        out = self.controller.export_article(self.cid)
        self.assertEqual(out["body"], "draft-v1")
        self.assertEqual(out["production_context"]["fact_pack"]["marker"], "immutable-context")
        self.assertEqual(out["production_evidence"]["marker"], "real-checker-evidence-placeholder")
        self.assertFalse(out["publish_allowed"])

    def test_status_is_read_only_copy_not_runtime_input(self):
        status = self.controller.status(self.cid)
        status["phase"] = "ARTICLE_PASS"
        status["article"]["title"] = "Fremder Titel"
        fresh = self.controller.status(self.cid)
        self.assertEqual(fresh["phase"], "RESEARCH_REQUIRED")
        self.assertEqual(fresh["article"]["title"], "Titel")
        with self.assertRaisesRegex(CapsuleError, "OUTPUT_GATE_CLOSED"):
            self.controller.export_article(self.cid)

    def test_external_publish_has_no_input_surface(self):
        status = self.controller.status(self.cid)
        status["publish_allowed"] = True
        self.assertFalse(self.controller.status(self.cid)["publish_allowed"])

    def test_unknown_capsule_cannot_enter_side_door(self):
        with self.assertRaisesRegex(CapsuleError, "CAPSULE_NOT_FOUND"):
            self.controller.submit_research("f" * 32, "research")

    def test_facts_cannot_skip_research(self):
        with self.assertRaisesRegex(CapsuleError, "PHASE_TRANSITION_FORBIDDEN"):
            self.controller.submit_facts(self.cid, "facts")

    def test_draft_cannot_skip_context(self):
        self.controller.submit_research(self.cid, "research")
        self.controller.submit_facts(self.cid, "facts")
        with self.assertRaisesRegex(CapsuleError, "PHASE_TRANSITION_FORBIDDEN"):
            self.controller.submit_draft(self.cid, "draft")

    def test_fail_stays_same_article_and_repairs_in_place(self):
        self.advance_to_draft()
        self.checks.fullcheck_fail = True
        self.controller.fullcheck(self.cid)
        status = self.controller.status(self.cid)
        self.assertEqual(status["phase"], "REPAIR_REQUIRED")
        self.assertEqual(status["article"], self.article)
        self.assertEqual(status["findings"], [{"error_code": "EXACT_FINDING"}])
        self.checks.fullcheck_fail = False
        self.controller.submit_draft(self.cid, "draft-v2")
        self.controller.fullcheck(self.cid)
        out = self.controller.export_article(self.cid)
        self.assertEqual(out["revision"], 2)
        self.assertEqual(out["production_context"]["fact_pack"]["marker"], "immutable-context")

    def test_wrong_checker_hash_cannot_open_gate(self):
        self.checks.bad_research_hash = True
        with self.assertRaisesRegex(CapsuleError, "RESEARCH_CHECK_HASH_MISMATCH"):
            self.controller.submit_research(self.cid, "research")
        self.assertEqual(self.controller.status(self.cid)["phase"], "RESEARCH_REQUIRED")

    def test_two_capsules_are_isolated(self):
        other_article = dict(self.article)
        other_article["plan_slot"] = "d" * 64
        other_article["title"] = "Anderer Artikel"
        other = self.controller.create(other_article, "b" * 64, "c" * 64)
        self.controller.submit_research(self.cid, "research")
        self.assertEqual(self.controller.status(self.cid)["phase"], "FACTS_REQUIRED")
        self.assertEqual(self.controller.status(other)["phase"], "RESEARCH_REQUIRED")

    def test_checkpoint_tamper_is_blocked(self):
        checkpoint = self.controller.checkpoint(self.cid)
        data = json.loads(checkpoint.decode("utf-8"))
        data["phase"] = "ARTICLE_PASS"
        tampered = json.dumps(data, sort_keys=True, separators=(",", ":")).encode("utf-8")
        restored = CapsuleController(self.key, MockChecks())
        with self.assertRaisesRegex(CapsuleError, "STATE_INTEGRITY_FAIL"):
            restored.restore(tampered)

    def test_valid_checkpoint_resumes_exact_bound_step(self):
        self.controller.submit_research(self.cid, "research")
        checkpoint = self.controller.checkpoint(self.cid)
        restored = CapsuleController(self.key, MockChecks())
        cid = restored.restore(checkpoint)
        self.assertEqual(restored.status(cid)["phase"], "FACTS_REQUIRED")
        restored.submit_facts(cid, "facts")
        self.assertEqual(restored.status(cid)["phase"], "CONTEXT_REQUIRED")

    def test_1000_capsules_complete_independently(self):
        ids = []
        for i in range(1000):
            article = dict(self.article)
            article["title"] = f"Titel {i}"
            article["target_keyword"] = f"Keyword {i}"
            article["plan_slot"] = hashlib.sha256(str(i).encode("utf-8")).hexdigest()
            ids.append(self.controller.create(article, "b" * 64, "c" * 64))
        for i, cid in enumerate(ids):
            self.controller.submit_research(cid, "research")
            self.controller.submit_facts(cid, "facts")
            self.controller.submit_context(cid, f"context {i}")
            self.controller.submit_draft(cid, f"draft {i}")
            self.controller.fullcheck(cid)
        self.assertTrue(all(self.controller.status(cid)["phase"] == "ARTICLE_PASS" for cid in ids))

    def test_batch_check_accepts_only_passed_capsules(self):
        with self.assertRaisesRegex(CapsuleError, "BATCH_ARTICLE_NOT_PASS"):
            self.controller.batch_check([self.cid])
        self.advance_to_draft()
        self.controller.fullcheck(self.cid)
        result = self.controller.batch_check([self.cid])
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(self.checks.batch_calls, 1)


class AutomaticSupervisorTests(unittest.TestCase):
    def setUp(self):
        self.checks = MockChecks()
        self.controller = CapsuleController(b"z" * 32, self.checks)
        article = {
            "title": "Auto Titel",
            "target_keyword": "Auto Keyword",
            "category": "auto",
            "article_type": "Typ",
            "plan_slot": "e" * 64,
        }
        self.cid = self.controller.create(article, "b" * 64, "c" * 64)

    def test_supervisor_owns_route_end_to_end(self):
        seen = []
        def worker(request):
            seen.append(request["task"])
            content = {
                "research": "research",
                "facts": "facts",
                "context": "context",
                "draft": "draft",
            }[request["task"]]
            return {"content": content}
        out = self.controller.run_automatic(self.cid, worker)
        self.assertEqual(seen, ["research", "facts", "context", "draft"])
        self.assertEqual(self.controller.status(self.cid)["phase"], "ARTICLE_PASS")
        self.assertEqual(out["body"], "draft")

    def test_worker_cannot_inject_phase_or_publish(self):
        def worker(request):
            return {"content": "ok", "phase": "ARTICLE_PASS", "publish_allowed": True}
        with self.assertRaisesRegex(CapsuleError, "WORKER_RESULT_SCHEMA_INVALID"):
            self.controller.run_automatic(self.cid, worker)
        self.assertEqual(self.controller.status(self.cid)["phase"], "RESEARCH_REQUIRED")
        self.assertFalse(self.controller.status(self.cid)["publish_allowed"])

    def test_fail_is_repaired_without_external_route_choice(self):
        calls = []
        def worker(request):
            calls.append(request["task"])
            if request["task"] == "research": return {"content": "research"}
            if request["task"] == "facts": return {"content": "facts"}
            if request["task"] == "context": return {"content": "context"}
            if request["task"] == "draft":
                self.checks.fullcheck_fail = True
                return {"content": "draft bad"}
            if request["task"] == "repair":
                self.assertEqual(request["findings"], [{"error_code": "EXACT_FINDING"}])
                self.checks.fullcheck_fail = False
                return {"content": "draft repaired"}
            raise AssertionError(request)
        out = self.controller.run_automatic(self.cid, worker)
        self.assertEqual(calls, ["research", "facts", "context", "draft", "repair"])
        self.assertEqual(out["body"], "draft repaired")
        self.assertEqual(self.controller.status(self.cid)["revision"], 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)