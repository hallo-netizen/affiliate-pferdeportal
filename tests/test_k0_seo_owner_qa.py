"""Regression of the approved redaction-only SEO ownership boundary.

This suite is deliberately in the isolated QA branch, never K0 production.
"""
import json
import unittest
from pathlib import Path

from engine.catalog_guard import validate_catalog
from engine.field_coverage import audit as field_audit
from engine.owner_guard import verify as owner_verify
from engine.ppm_parity_guard import verify as ppm_verify
from engine.k0_production_gate import _verify_semantic_intent, Blocked
from engine.checkers import run_article_checks
from engine.core import hard_rules, load_values
from test_k10 import make_base

ROOT=Path(__file__).resolve().parents[1]
REMOVED={
    'title.keyword_required',
    'title.colon_forbidden',
    'type.question_mark_policy',
    'heading.target_phrase_control',
}

class K0ApprovedSeoOwnerQA(unittest.TestCase):
    def test_eighty_one_hard_article_rules_and_all_text_limits_still_exist(self):
        ids={r['id'] for r in hard_rules('ARTICLE')}
        self.assertEqual(len(ids),81)
        self.assertFalse(ids & REMOVED)
        for rule in [
            'heading.keyword_staccato_forbidden', 'heading.phrase_family_repetition_forbidden',
            'surface.repetition_forbidden', 'surface.duplicate_sentence_ratio',
            'words.hard_total_range', 'words.section_range', 'words.section_balance_ratio',
            'structure.paragraph_floor', 'structure.h2_floor', 'structure.list_minimum_items',
            'table.required_for_comparison', 'table.value_required_if_present',
            'facts.trace_lexical_support', 'facts.referenced_fact_verified',
            'lt68.language_zero_unresolved',
        ]:
            self.assertIn(rule,ids,rule)
        v=load_values()
        self.assertEqual((v['balance']['hard_total_words_min'],v['balance']['hard_total_words_max']),(750,900))
        self.assertEqual(v['ppm_parity']['content']['minimum_paragraphs'],16)
        self.assertEqual(v['ppm_parity']['content']['minimum_h2'],4)
        self.assertEqual(v['heading']['significant_target_keyword_token_h2_occurrences_max'],2)

    def test_field_owner_and_104_ppm_legacy_parity(self):
        self.assertEqual(validate_catalog()['status'],'PASS')
        self.assertEqual(field_audit()['status'],'PASS')
        self.assertEqual(owner_verify()['status'],'PASS')
        ppm=ppm_verify()
        self.assertEqual(ppm['status'],'PASS',ppm)
        self.assertEqual(ppm['legacy_rule_count'],104)
        self.assertEqual(ppm['externally_owned_title_rules'],3)
        self.assertEqual(ppm['approved_table_policy_changes'],3)

    def test_final_receipts_preserve_all_remaining_rules(self):
        article=make_base()
        receipts=run_article_checks(article)
        ids={r['rule_id'] for r in receipts}
        self.assertEqual(ids,{r['id'] for r in hard_rules('ARTICLE')})
        self.assertEqual(len(receipts),81)
        self.assertNotIn('heading.target_phrase_control',ids)
        self.assertIn('heading.keyword_staccato_forbidden',ids)

    def test_approved_intent_is_no_longer_overruled_from_type_and_title(self):
        pkg={'content_profile':{'search_intent':'COMMERCIAL_INVESTIGATION'}}
        ident={'article_type':'Beratung','title':'Kombinierte Fliegen- und Regendecken für Pferde sinnvoll nutzen'}
        self.assertEqual(_verify_semantic_intent(pkg,ident,'<article>Eine gute fachliche Erklärung</article>'),'COMMERCIAL_INVESTIGATION')
        pkg['content_profile']['search_intent']='DECISION_SUPPORT'
        self.assertEqual(_verify_semantic_intent(pkg,ident,'<article>Eine gute fachliche Erklärung</article>'),'DECISION_SUPPORT')

    def test_real_three_item_metadata_handoff_is_still_valid(self):
        from engine.k0_portal_resolver import validate_intake
        path=ROOT/'real_runs/k0/batch-20261110-42619ca7/BATCH_INTAKE.json'
        batch=json.loads(path.read_text(encoding='utf-8'))
        items=validate_intake(batch)
        self.assertEqual(len(items),3)
        self.assertEqual([x['target_keyword'] for x in items],[
            'Horseware regendecken','Fliegen regendecke pferd','Regendecke pferd 0g'
        ])
        self.assertEqual(len({x['plan_slot'] for x in items}),3)

    def test_keyword_staccato_still_blocks_repetitive_h2s(self):
        article=make_base()
        article['target_keyword']='Longierpeitsche'
        article['html']=article['html'].replace(
            '<h2>Stimme und Longe im Zusammenspiel</h2>',
            '<h2>Stimme und Longierpeitsche im Zusammenspiel</h2>'
        ).replace(
            '<h2>Sicherer Einsatz beim Longieren</h2>',
            '<h2>Longierpeitsche sicher beim Longieren verwenden</h2>'
        )
        results={r['rule_id']:r['status'] for r in run_article_checks(article)}
        self.assertEqual(results['heading.keyword_staccato_forbidden'],'FAIL')

    def test_real_boilerplate_and_missing_intent_still_block(self):
        ident={'article_type':'Beratung','title':'Ein sachlicher Titel'}
        with self.assertRaises(Blocked):
            _verify_semantic_intent({'content_profile':{'search_intent':''}},ident,'<article>Neutraler Text</article>')
        with self.assertRaises(Blocked):
            _verify_semantic_intent({'content_profile':{'search_intent':'DECISION_SUPPORT'}},ident,'<article>Ein guter Vergleich beginnt mit einer klaren Reihenfolge der Auswahl</article>')

if __name__=='__main__':
    unittest.main()
