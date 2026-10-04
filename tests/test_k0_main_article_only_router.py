import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN = ("K8", "K9", "K10", "concept_agent", "repair", "design", "architecture")

def load(path):
    return (ROOT / path).read_text(encoding="utf-8")

def validate_main_router():
    files = {
        "K0_START_HERE.md": load("K0_START_HERE.md"),
        "control/CURRENT_STARTMASTER.json": load("control/CURRENT_STARTMASTER.json"),
        "control/startmaster0107/PFERDE_ATELIER_START_HERE.json": load("control/startmaster0107/PFERDE_ATELIER_START_HERE.json"),
        "control/startmaster0107/CURRENT_STATE.json": load("control/startmaster0107/CURRENT_STATE.json"),
    }
    haystack = "\n".join(files.values()).casefold()
    for token in FORBIDDEN:
        if token.casefold() in haystack:
            raise AssertionError("FORBIDDEN_ACTIVE_ROUTE_TOKEN:" + token)
    ptr = json.loads(files["control/CURRENT_STARTMASTER.json"])
    start = json.loads(files["control/startmaster0107/PFERDE_ATELIER_START_HERE.json"])
    disabled = json.loads(files["control/startmaster0107/CURRENT_STATE.json"])
    target = "konzept0-portal-neutral-20261002:K0_CURRENT_STATE.json"
    if ptr.get("root_ref") != "K0_START_HERE.md":
        raise AssertionError("MAIN_ROOT_NOT_K0")
    if ptr.get("state_ref") != target:
        raise AssertionError("MAIN_STATE_NOT_K0")
    if start.get("current_authority") != target:
        raise AssertionError("START_CURRENT_NOT_K0")
    if start.get("article_production_only") is not True:
        raise AssertionError("START_NOT_ARTICLE_ONLY")
    if disabled.get("role") != "NON_AUTHORITATIVE_REDIRECT_ONLY":
        raise AssertionError("OLD_CURRENT_STILL_AUTHORITATIVE")
    if disabled.get("may_define_next_action") is not False or disabled.get("may_define_runtime") is not False:
        raise AssertionError("OLD_CURRENT_CAN_STILL_CONTROL")
    return True

class K0MainArticleOnlyRouterTests(unittest.TestCase):
    def test_positive_main_router_is_k0_article_only(self):
        self.assertTrue(validate_main_router())

    def test_negative_forbidden_route_token_is_rejected(self):
        bad = load("K0_START_HERE.md") + "\nconcept_agent/START_HERE.md"
        for token in FORBIDDEN:
            if token.casefold() in bad.casefold():
                self.assertEqual(token, "concept_agent")
                return
        self.fail("negative route token was not detected")

    def test_negative_disabled_current_cannot_control(self):
        disabled = json.loads(load("control/startmaster0107/CURRENT_STATE.json"))
        disabled["may_define_next_action"] = True
        with self.assertRaisesRegex(AssertionError, "OLD_CURRENT_CAN_STILL_CONTROL"):
            if disabled.get("role") != "NON_AUTHORITATIVE_REDIRECT_ONLY":
                raise AssertionError("OLD_CURRENT_STILL_AUTHORITATIVE")
            if disabled.get("may_define_next_action") is not False or disabled.get("may_define_runtime") is not False:
                raise AssertionError("OLD_CURRENT_CAN_STILL_CONTROL")

if __name__ == "__main__":
    unittest.main()
