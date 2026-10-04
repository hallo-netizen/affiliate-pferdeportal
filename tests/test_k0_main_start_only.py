import unittest
from pathlib import Path

FORBIDDEN = ("K8", "K9", "K10", "concept_agent", "repair", "design", "architecture")

class K0MainStartOnlyTests(unittest.TestCase):
    def test_positive_main_start_routes_only_to_k0_article_production(self):
        text = Path("K0_START_HERE.md").read_text(encoding="utf-8")
        self.assertIn("konzept0-portal-neutral-20261002:K0_START_HERE.md", text)
        self.assertIn("K0_CURRENT_STATE.json", text)
        self.assertIn("ARTICLE PRODUCTION ONLY", text)
        for token in FORBIDDEN:
            self.assertNotIn(token.casefold(), text.casefold())

    def test_negative_old_route_marker_would_fail(self):
        text = Path("K0_START_HERE.md").read_text(encoding="utf-8") + "\nconcept_agent/START_HERE.md"
        self.assertTrue(any(token.casefold() in text.casefold() for token in FORBIDDEN))

if __name__ == "__main__":
    unittest.main()
