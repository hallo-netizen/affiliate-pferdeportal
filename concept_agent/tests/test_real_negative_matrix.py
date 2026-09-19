import sys
from pathlib import Path
import unittest

OFFICE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(OFFICE))

from contracts import ArticleJob,ResearchEvidence,Fact,Draft
from handoff_guard import check_research,check_facts
from textmachine_guard import check_textmachine_snapshot


class RealNegativeMatrixTest(unittest.TestCase):
    def setUp(self):
        self.job=ArticleJob("j1","Titel","kw","Beratung","kat",["/a/","/b/","/c/"])
        self.research=[ResearchEvidence("s1","https://example.org","Beleg")]

    def test_bad_source_url_blocks(self):
        bad=[ResearchEvidence("s1","not-a-url","Beleg")]
        self.assertIn("SOURCE_URL_INVALID",check_research(bad))

    def test_fact_from_unknown_source_blocks(self):
        self.assertIn("FACT_SOURCE_NOT_ACCEPTED",check_facts([Fact("f1","Aussage","unknown")],self.research))

    def test_missing_internal_link_blocks(self):
        draft=Draft("j1","# Titel\nkw\n/a/ /b/ [TABLE]")
        self.assertIn("TEXTMACHINE_REQUIRED_INTERNAL_LINK_MISSING",check_textmachine_snapshot(self.job,draft))

    def test_external_link_blocks(self):
        draft=Draft("j1","# Titel\nkw\n/a/ /b/ /c/ [TABLE] https://example.org")
        self.assertIn("TEXTMACHINE_EXTERNAL_LINK_FORBIDDEN",check_textmachine_snapshot(self.job,draft))

    def test_missing_table_blocks(self):
        draft=Draft("j1","# Titel\nkw\n/a/ /b/ /c/")
        self.assertIn("TEXTMACHINE_MANDATORY_TABLE_MISSING",check_textmachine_snapshot(self.job,draft))


if __name__=="__main__":
    unittest.main()
