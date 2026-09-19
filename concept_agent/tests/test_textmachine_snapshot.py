import sys
from pathlib import Path
import unittest

OFFICE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(OFFICE))

from contracts import ArticleJob, Draft
from textmachine_guard import check_textmachine_snapshot


class TextmachineSnapshotTest(unittest.TestCase):
    def setUp(self):
        self.job=ArticleJob("j1","Das richtige Huffett für Pferde finden","Huffett für Pferde","Beratung","kat",["/a/","/b/","/c/"])

    def test_positive(self):
        body='<article><h2>Welches Huffett passt zu welchem Huf?</h2><p>Huffett für Pferde <a href="/a/">A</a> ordnet den Punkt ein.</p><a href="/b/">B</a> und <a href="/c/">C</a><table></table></article>'
        self.assertEqual([],check_textmachine_snapshot(self.job,Draft("j1",body)))

    def test_missing_link_blocks(self):
        body="# Das richtige Huffett für Pferde finden\n\nHuffett für Pferde\n\n/a/ /b/\n\n[TABLE]"
        self.assertIn("TEXTMACHINE_REQUIRED_INTERNAL_LINK_MISSING",check_textmachine_snapshot(self.job,Draft("j1",body)))

    def test_external_link_blocks(self):
        body="# Das richtige Huffett für Pferde finden\n\nHuffett für Pferde /a/ /b/ /c/ [TABLE] https://example.org"
        self.assertIn("TEXTMACHINE_EXTERNAL_LINK_FORBIDDEN",check_textmachine_snapshot(self.job,Draft("j1",body)))

    def test_missing_table_blocks(self):
        body="# Das richtige Huffett für Pferde finden\n\nHuffett für Pferde /a/ /b/ /c/"
        self.assertIn("TEXTMACHINE_MANDATORY_TABLE_MISSING",check_textmachine_snapshot(self.job,Draft("j1",body)))

    def test_weak_beratung_title_blocks(self):
        weak=ArticleJob("j1","So findest du Huffett für Pferde","Huffett für Pferde","Beratung","kat",["/a/","/b/","/c/"])
        body="# So findest du Huffett für Pferde\n\nHuffett für Pferde /a/ /b/ /c/ [TABLE]"
        self.assertIn("TEXTMACHINE_BERATUNG_TITLE_WEAK_SURFACE",check_textmachine_snapshot(weak,Draft("j1",body)))

    def test_attribute_rich_beratung_title_passes_title_gate(self):
        good=ArticleJob("j1","So findest du das richtige Huffett für Pferde","Huffett für Pferde","Beratung","kat",["/a/","/b/","/c/"])
        body="# So findest du das richtige Huffett für Pferde\n\nHuffett für Pferde /a/ /b/ /c/ [TABLE]"
        self.assertNotIn("TEXTMACHINE_BERATUNG_TITLE_WEAK_SURFACE",check_textmachine_snapshot(good,Draft("j1",body)))

    def test_missing_space_after_inline_link_blocks(self):
        body='<article><h2>Welches Huffett passt zu welchem Huf?</h2><p>Huffett für Pferde <a href="/a/">A</a>ordnet den Punkt ein.</p><a href="/b/">B</a> und <a href="/c/">C</a><table></table></article>'
        self.assertIn("TEXTMACHINE_INLINE_LINK_TRAILING_SPACE_MISSING",check_textmachine_snapshot(self.job,Draft("j1",body)))

    def test_punctuation_after_inline_link_is_allowed(self):
        body='<article><h2>Welches Huffett passt zu welchem Huf?</h2><p>Huffett für Pferde <a href="/a/">A</a>, danach weiter.</p><a href="/b/">B</a> und <a href="/c/">C</a><table></table></article>'
        self.assertNotIn("TEXTMACHINE_INLINE_LINK_TRAILING_SPACE_MISSING",check_textmachine_snapshot(self.job,Draft("j1",body)))

    def test_mechanical_beratung_h2_blocks(self):
        body='<article><h2>Fliegenmasken am Pferd sicher beurteilen</h2><p>Huffett für Pferde <a href="/a/">A</a> ordnet ein.</p><a href="/b/">B</a> und <a href="/c/">C</a><table></table></article>'
        self.assertIn("TEXTMACHINE_BERATUNG_H2_MECHANICAL",check_textmachine_snapshot(self.job,Draft("j1",body)))

    def test_natural_beratung_h2_passes(self):
        body='<article><h2>Welche Fliegenmaske passt zu deinem Pferd?</h2><p>Huffett für Pferde <a href="/a/">A</a> ordnet ein.</p><a href="/b/">B</a> und <a href="/c/">C</a><table></table></article>'
        self.assertNotIn("TEXTMACHINE_BERATUNG_H2_MECHANICAL",check_textmachine_snapshot(self.job,Draft("j1",body)))


if __name__=="__main__":
    unittest.main()
