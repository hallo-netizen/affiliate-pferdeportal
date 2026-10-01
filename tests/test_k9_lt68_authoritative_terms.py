import sys, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str((ROOT/"quality").resolve()))
import k9_lt68

def match(rule_id,checked,token):
    off=checked.index(token)
    return {"rule":{"id":rule_id},"offset":off,"length":len(token),"message":"x","context":{"text":checked}}

class LTAuthoritativeTermsTests(unittest.TestCase):
    def test_authoritative_exact_term_ignores_only_speller(self):
        checked="Heutaschen Heutaschn"
        report={"matches":[
            match("GERMAN_SPELLER_RULE",checked,"Heutaschen"),
            match("GERMAN_SPELLER_RULE",checked,"Heutaschn"),
            match("DE_AGREEMENT",checked,"Heutaschen"),
        ]}
        filtered,ignored,_,_=k9_lt68.apply_domain_dictionary(checked,report,["Heutaschen"])
        self.assertEqual(len(ignored),1)
        self.assertEqual(ignored[0]["token"],"Heutaschen")
        self.assertEqual(ignored[0]["source"],"AUTHORITATIVE_ARTICLE_METADATA")
        kept=[x["rule"]["id"] for x in filtered["matches"]]
        self.assertEqual(kept,["GERMAN_SPELLER_RULE","DE_AGREEMENT"])

    def test_partial_or_invalid_authoritative_term_is_not_accepted(self):
        checked="Heutaschn"
        report={"matches":[match("GERMAN_SPELLER_RULE",checked,"Heutaschn")]}
        filtered,ignored,_,_=k9_lt68.apply_domain_dictionary(checked,report,["Heutaschen"])
        self.assertEqual(len(ignored),0)
        self.assertEqual(len(filtered["matches"]),1)
        with self.assertRaisesRegex(k9_lt68.LTError,"LT68_AUTHORITATIVE_DOMAIN_WORD_NOT_EXACT_TOKEN"):
            k9_lt68.apply_domain_dictionary(checked,report,["Heutaschen!"])

if __name__=="__main__": unittest.main()
