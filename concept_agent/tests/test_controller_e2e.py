import sys
from pathlib import Path
import unittest

OFFICE=Path(__file__).resolve().parents[1]
sys.path.insert(0, str(OFFICE))

from contracts import ArticleJob, ResearchEvidence
from controller import ConceptAgentController
from manual_chat_writer import ManualChatWriter
from claude_adapter import ClaudeWriterAdapter


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

    def test_complete_chain_reaches_one_final_file(self):
        result=ConceptAgentController().run(self.job,self.sources)
        self.assertEqual("FINAL_FILE_READY",result.status)
        self.assertIsNotNone(result.draft)
        self.assertIsNotNone(result.final_file)
        self.assertEqual("CONCEPT_AGENT_FINAL_ARTICLE_V1",result.final_file["contract"])
        self.assertIn("TEXTMACHINE_SNAPSHOT_PASS",result.trace)

    def test_empty_sources_block_before_writer(self):
        result=ConceptAgentController().run(self.job,[])
        self.assertEqual("BLOCKED_RESEARCH",result.status)
        self.assertIsNone(result.draft)
        self.assertIsNone(result.final_file)

    def test_bad_input_blocks_immediately(self):
        bad=ArticleJob("","Titel","kw","Beratung","haltung",[])
        result=ConceptAgentController().run(bad,self.sources)
        self.assertEqual("BLOCKED_INPUT",result.status)

    def test_chat_writer_can_be_injected(self):
        body="# Boxenmatten richtig auswählen\n\nBoxenmatten\n\n[TABLE]\n\n/haltung/ /stall/ /boden/\n\nGenügend Inhalt für den isolierten Test."
        result=ConceptAgentController(ManualChatWriter(body)).run(self.job,self.sources)
        self.assertEqual("FINAL_FILE_READY",result.status)
        self.assertEqual("chat-manual",result.final_file["writer"])

    def test_unconnected_claude_blocks_cleanly(self):
        result=ConceptAgentController(ClaudeWriterAdapter()).run(self.job,self.sources)
        self.assertEqual("BLOCKED_WRITER",result.status)
        self.assertIn("CLAUDE_NOT_CONNECTED",result.trace)


if __name__=="__main__":
    unittest.main()
