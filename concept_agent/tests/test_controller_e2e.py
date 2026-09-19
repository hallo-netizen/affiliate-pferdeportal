import sys
from pathlib import Path
import unittest

OFFICE=Path(__file__).resolve().parents[1]
sys.path.insert(0, str(OFFICE))

from contracts import ArticleJob, ResearchEvidence
from controller import ConceptAgentController


class ControllerE2ETest(unittest.TestCase):
    def setUp(self):
        self.job=ArticleJob(
            "j1","Boxenmatten richtig auswählen","Boxenmatten",
            "Beratung","haltung",["/haltung/","/stall/","/boden/"]
        )
        self.sources=[
            ResearchEvidence("s1","https://example.org/1","Boxenmatten beeinflussen den Stallboden und die Nutzung."),
            ResearchEvidence("s2","https://example.org/2","Untergrund und Pflege müssen zusammen betrachtet werden.")
        ]

    def test_complete_chain_reaches_final_file(self):
        result=ConceptAgentController().run(self.job,self.sources)
        self.assertEqual("FINAL_FILE_READY",result.status)
        self.assertIsNotNone(result.draft)
        self.assertIn("RESEARCH_PASS",result.trace)
        self.assertIn("FACTS_PASS",result.trace)
        self.assertIn("DRAFT_HANDOFF_PASS",result.trace)

    def test_empty_sources_block_before_writer(self):
        result=ConceptAgentController().run(self.job,[])
        self.assertEqual("BLOCKED_RESEARCH",result.status)
        self.assertIsNone(result.draft)

    def test_bad_input_blocks_immediately(self):
        bad=ArticleJob("","Titel","kw","Beratung","haltung",[])
        result=ConceptAgentController().run(bad,self.sources)
        self.assertEqual("BLOCKED_INPUT",result.status)


if __name__=="__main__":
    unittest.main()
