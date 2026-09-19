import sys
from pathlib import Path
import unittest

OFFICE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(OFFICE))

from contracts import ArticleJob, Draft
from textmachine_guard import check_textmachine_snapshot


class TextmachineSnapshotTest(unittest.TestCase):
    def setUp(self):
        self.job=ArticleJob("j1","Titel","kw","Beratung","kat",["/a/","/b/","/c/"])

    def test_positive(self):
        body="# Titel\n\nkw\n\n/a/ /b/ /c/\n\n[TABLE]\nInhalt"
        self.assertEqual([],check_textmachine_snapshot(self.job,Draft("j1",body)))

    def test_missing_link_blocks(self):
        body="# Titel\n\nkw\n\n/a/ /b/\n\n[TABLE]"
        self.assertIn("TEXTMACHINE_REQUIRED_INTERNAL_LINK_MISSING",check_textmachine_snapshot(self.job,Draft("j1",body)))

    def test_external_link_blocks(self):
        body="# Titel\n\nkw /a/ /b/ /c/ [TABLE] https://example.org"
        self.assertIn("TEXTMACHINE_EXTERNAL_LINK_FORBIDDEN",check_textmachine_snapshot(self.job,Draft("j1",body)))

    def test_missing_table_blocks(self):
        body="# Titel\n\nkw /a/ /b/ /c/"
        self.assertIn("TEXTMACHINE_MANDATORY_TABLE_MISSING",check_textmachine_snapshot(self.job,Draft("j1",body)))


if __name__=="__main__":
    unittest.main()
