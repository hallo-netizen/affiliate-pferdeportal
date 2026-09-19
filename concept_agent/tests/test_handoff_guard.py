import sys
from pathlib import Path
import unittest

OFFICE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(OFFICE))

from contracts import ArticleJob, ResearchEvidence, Fact, Draft
from handoff_guard import check_job, check_research, check_facts, check_draft


class HandoffGuardTest(unittest.TestCase):
    def setUp(self):
        self.job = ArticleJob("j1","Titel","keyword","Beratung","haltung",["/a/","/b/","/c/"])
        self.research = [ResearchEvidence("s1","https://example.org/a","Belegtext")]
        self.facts = [Fact("f1","Aussage","s1")]

    def test_positive_chain(self):
        self.assertEqual([], check_job(self.job))
        self.assertEqual([], check_research(self.research))
        self.assertEqual([], check_facts(self.facts, self.research))
        self.assertEqual([], check_draft(Draft("j1","Artikeltext"), self.job))

    def test_bad_fact_source_is_blocked(self):
        bad = [Fact("f1","Aussage","unknown")]
        self.assertIn("FACT_SOURCE_NOT_ACCEPTED", check_facts(bad, self.research))

    def test_wrong_article_identity_is_blocked(self):
        self.assertIn("DRAFT_JOB_MISMATCH", check_draft(Draft("other","Artikeltext"), self.job))

    def test_empty_research_is_blocked(self):
        self.assertEqual(["RESEARCH_EMPTY"], check_research([]))


if __name__ == "__main__":
    unittest.main()
