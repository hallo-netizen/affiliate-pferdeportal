import sys
from pathlib import Path
import unittest

OFFICE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(OFFICE))

from contracts import ArticleJob,Fact
from manual_chat_writer import ManualChatWriter
from claude_adapter import ClaudeWriterAdapter


class WriterVariantsTest(unittest.TestCase):
    def setUp(self):
        self.job=ArticleJob("j1","Titel","kw","Beratung","kat",["/a/","/b/","/c/"])
        self.facts=[Fact("f1","Aussage","s1")]

    def test_chat_port_builds_fixed_request(self):
        req=ManualChatWriter().build_request(self.job,self.facts)
        self.assertEqual("writer",req["role"])
        self.assertEqual("j1",req["job_id"])

    def test_chat_without_supplied_text_is_blocked(self):
        with self.assertRaisesRegex(RuntimeError,"CHAT_TEXT_NOT_SUPPLIED"):
            ManualChatWriter().run(self.job,self.facts)

    def test_claude_port_is_not_silently_connected(self):
        adapter=ClaudeWriterAdapter()
        self.assertFalse(adapter.connected)
        with self.assertRaisesRegex(RuntimeError,"CLAUDE_NOT_CONNECTED"):
            adapter.run(self.job,self.facts)


if __name__=="__main__":
    unittest.main()
