import json
import unittest
from pathlib import Path

FORBIDDEN = ("K8", "K9", "K10", "concept_agent", "repair", "design", "architecture")
ROOT = Path(__file__).resolve().parents[1]

def validate_start(start_text, current):
    haystack = start_text + "\n" + json.dumps(current, ensure_ascii=False)
    for token in FORBIDDEN:
        if token.casefold() in haystack.casefold():
            raise AssertionError("FORBIDDEN_ACTIVE_ROUTE_TOKEN:" + token)
    if current.get("mode") != "ARTICLE_PRODUCTION_ONLY":
        raise AssertionError("K0_NOT_ARTICLE_PRODUCTION_ONLY")
    if current.get("next_action") != "RUN_CURRENT_UPLOAD_ARTICLE_PRODUCTION_ONLY":
        raise AssertionError("K0_NEXT_ACTION_NOT_ARTICLE_PRODUCTION")
    boundary = current.get("article_run_boundary") or {}
    if boundary.get("non_article_work_allowed") is not False:
        raise AssertionError("NON_ARTICLE_WORK_NOT_HARD_BLOCKED")
    for key in ("code_changes_allowed","workflow_changes_allowed","configuration_changes_allowed","plugin_changes_allowed","presentation_changes_allowed","alternate_route_allowed","other_current_authority_allowed"):
        if boundary.get(key) is not False:
            raise AssertionError("ARTICLE_BOUNDARY_NOT_CLOSED:" + key)
    if "K0_CURRENT_STATE.json" not in start_text:
        raise AssertionError("K0_CURRENT_NOT_BOUND")
    return True

class K0ArticleOnlyStartTests(unittest.TestCase):
    def test_positive_actual_active_k0_start_passes(self):
        start = (ROOT / "K0_START_HERE.md").read_text(encoding="utf-8")
        current = json.loads((ROOT / "K0_CURRENT_STATE.json").read_text(encoding="utf-8"))
        self.assertTrue(validate_start(start, current))

    def test_negative_old_route_token_blocks(self):
        start = (ROOT / "K0_START_HERE.md").read_text(encoding="utf-8") + "\nK8 old route"
        current = json.loads((ROOT / "K0_CURRENT_STATE.json").read_text(encoding="utf-8"))
        with self.assertRaisesRegex(AssertionError, "FORBIDDEN_ACTIVE_ROUTE_TOKEN"):
            validate_start(start, current)

    def test_negative_non_article_action_blocks(self):
        start = (ROOT / "K0_START_HERE.md").read_text(encoding="utf-8")
        current = json.loads((ROOT / "K0_CURRENT_STATE.json").read_text(encoding="utf-8"))
        current["next_action"] = "SYSTEM_REPAIR"
        with self.assertRaisesRegex(AssertionError, "K0_NEXT_ACTION_NOT_ARTICLE_PRODUCTION"):
            validate_start(start, current)

if __name__ == "__main__":
    unittest.main()
