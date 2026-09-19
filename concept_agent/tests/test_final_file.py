import sys
from pathlib import Path
import unittest

OFFICE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(OFFICE))

from contracts import ArticleJob,Draft
from final_file import build_final_file,canonical_json


class FinalFileTest(unittest.TestCase):
    def test_one_canonical_final_payload(self):
        job=ArticleJob("j1","Titel","kw","Beratung","kat",["/a/","/b/","/c/"])
        p=build_final_file(job,Draft("j1","Artikel"),["PASS"],"test-writer")
        self.assertEqual("CONCEPT_AGENT_FINAL_ARTICLE_V1",p["contract"])
        self.assertEqual("FINAL_FILE_READY",p["status"])
        self.assertEqual(64,len(p["article_sha256"]))
        self.assertEqual(canonical_json(p),canonical_json(p))


if __name__=="__main__":
    unittest.main()
