import copy, json, sys, unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str((ROOT/"quality").resolve()))
import k9_rule_guard

class K9CompleteRuleCoverageTest(unittest.TestCase):
    def setUp(self):
        self.rules=json.loads((ROOT/"contracts"/"K9_WRITING_RULES.json").read_text(encoding="utf-8"))

    def test_all_rule_groups_have_enforcement_owner(self):
        result=k9_rule_guard.validate_coverage(self.rules)
        self.assertEqual(result["status"],"PASS")

    def test_missing_rule_group_fails_closed(self):
        broken=copy.deepcopy(self.rules)
        del broken["coverage"]["rule_groups"]["editorial_additive"]
        with self.assertRaisesRegex(k9_rule_guard.RuleGuardError,"GROUP_SET_INCOMPLETE"):
            k9_rule_guard.validate_coverage(broken)

    def test_keyword_staccato_in_h2_is_rejected(self):
        html="""<article>
        <h2>Regendecken schützen vor Nässe</h2>
        <h2>Regendecken bei Wind einschätzen</h2>
        <h2>Regendecken für alte Pferde</h2>
        <h2>Regendecken regelmäßig kontrollieren</h2>
        <h2>Regendecken nach Wetter beurteilen</h2>
        </article>"""
        meta={"title":"Frieren Pferde unter Regendecken?","target_keyword":"Frieren Pferde unter Regendecken"}
        codes={x["code"] for x in k9_rule_guard.heading_findings(html,meta,self.rules)}
        self.assertIn("K9_RULE_H2_KEYWORD_STACCATO",codes)
        self.assertIn("K9_RULE_H2_PHRASE_FAMILY_REPETITION",codes)

    def test_h2_length_limit_rejects_overlong_heading(self):
        html="""<article>
        <h2>Welche Bewässerungsarten sich für unterschiedliche Reitplätze im täglichen Betrieb wirklich sinnvoll unterscheiden</h2>
        <h2>Wasser von unten statt von oben</h2>
        </article>"""
        meta={"title":"Reitplatzbewässerung","target_keyword":"Reitplatzbewässerung"}
        codes={x["code"] for x in k9_rule_guard.heading_findings(html,meta,self.rules)}
        self.assertIn("K9_RULE_H2_TOO_LONG",codes)

    def test_compact_natural_h2_stays_within_limit(self):
        html="""<article>
        <h2>Wie die Bewässerung von unten funktioniert</h2>
        <h2>Wann ein Reitplatz dafür geeignet ist</h2>
        <h2>Fazit</h2>
        </article>"""
        meta={"title":"Ist eine Reitplatzbewässerung von unten möglich?","target_keyword":"Reitplatzbewässerung von unten"}
        findings=k9_rule_guard.heading_findings(html,meta,self.rules)
        self.assertNotIn("K9_RULE_H2_TOO_LONG",{x["code"] for x in findings})

    def test_two_keyword_headings_do_not_trigger_staccato(self):
        html="""<article>
        <h2>Regendecken bei Wind einschätzen</h2>
        <h2>Nässe und Winterfell richtig beurteilen</h2>
        <h2>Regendecken regelmäßig kontrollieren</h2>
        <h2>Fazit zum Wetterschutz</h2>
        </article>"""
        meta={"title":"Regendecken für Pferde auswählen","target_keyword":"Regendecken für Pferde"}
        codes={x["code"] for x in k9_rule_guard.heading_findings(html,meta,self.rules)}
        self.assertNotIn("K9_RULE_H2_KEYWORD_STACCATO",codes)
        self.assertNotIn("K9_RULE_H2_PHRASE_FAMILY_REPETITION",codes)

if __name__=="__main__":
    unittest.main()
