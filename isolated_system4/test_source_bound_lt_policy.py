from __future__ import annotations

import unittest

import source_bound_lt_policy as policy

class SourceBoundLtPolicyTests(unittest.TestCase):
    def _match(self,target:str,replacements:list[dict]|None=None,rule_id:str='GERMAN_SPELLER_RULE'):
        return {
            'offset':0,'length':len(target),'message':'Möglicher Tippfehler gefunden.',
            'replacements':[] if replacements is None else replacements,
            'rule':{'id':rule_id},
        }

    def test_exact_source_bound_speller_term_without_replacement_is_approved(self):
        target='Starrdeichselanhänger'
        unresolved,approved=policy.classify_report(
            {'matches':[self._match(target)]},target,
            'Nach § 44 StVZO gelten für Starrdeichselanhänger Anforderungen an die Stützlast.',
        )
        self.assertEqual(unresolved,[])
        self.assertEqual(len(approved),1)
        self.assertEqual(approved[0]['target'],target)
        self.assertEqual(approved[0]['rule_id'],'GERMAN_SPELLER_RULE')

    def test_unbound_unknown_word_remains_unresolved(self):
        target='Erfundenerquatschbegriff'
        unresolved,approved=policy.classify_report(
            {'matches':[self._match(target)]},target,
            'Die versiegelte Quelle enthält diesen Begriff ausdrücklich nicht.',
        )
        self.assertEqual(len(unresolved),1)
        self.assertEqual(approved,[])

    def test_speller_finding_with_replacement_must_be_repaired(self):
        target='Pferdeanhnger'
        unresolved,approved=policy.classify_report(
            {'matches':[self._match(target,[{'value':'Pferdeanhänger'}])]},target,
            'Pferdeanhnger',
        )
        self.assertEqual(len(unresolved),1)
        self.assertEqual(approved,[])

    def test_non_speller_rule_never_becomes_source_exception(self):
        target='irgendwas'
        unresolved,approved=policy.classify_report(
            {'matches':[self._match(target,[],rule_id='SOME_GRAMMAR_RULE')]},target,
            'irgendwas',
        )
        self.assertEqual(len(unresolved),1)
        self.assertEqual(approved,[])

if __name__=='__main__':
    unittest.main(verbosity=2)
