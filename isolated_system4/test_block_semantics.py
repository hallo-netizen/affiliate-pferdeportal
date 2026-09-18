from __future__ import annotations

import unittest

import block_semantics
import global_workshop
import repair_router


def contract():
    structure={'headings':{'reserved_headings':['Fazit','Weiterführende Informationen']}}
    type_def={'required_blocks':['intro','body','conclusion','further_information']}
    return {
        'contract':'SYSTEM4_AUTHORING_CONTRACT_V1',
        'type_requirements':{'required_blocks':list(type_def['required_blocks'])},
        'block_semantics':block_semantics.bind(structure,type_def),
    }


def html(conclusion='Abschließende Bewertung zum Thema',further='Ergänzende Informationen zum Thema',order=None):
    bodies={
        'intro':'<p>Einleitung.</p>',
        'body':'<h2>Thema prüfen</h2><p>Inhalt.</p>',
        'conclusion':f'<h2>{conclusion}</h2><p>Abschluss eins.</p><p>Abschluss zwei.</p>',
        'further_information':f'<h2>{further}</h2><p>Weitere Hinweise.</p>',
    }
    ids=order or ['intro','body','conclusion','further_information']
    return '<article>'+''.join(f'<section data-block="{name}">{bodies[name]}</section>' for name in ids)+'</article>'


class BlockSemanticContractTests(unittest.TestCase):
    def test_future_article_type_uses_data_driven_synonyms_without_type_code(self):
        result=block_semantics.validate(html(),contract())
        self.assertEqual(result['status'],'PASS')
        self.assertEqual(result['required_block_order'],['intro','body','conclusion','further_information'])

    def test_canonical_ppm_headings_are_valid(self):
        result=block_semantics.validate(
            html('Fazit','Weiterführende Informationen'),
            contract(),
        )
        self.assertEqual(result['status'],'PASS')

    def test_non_synonym_heading_is_repairable_workshop_body_finding(self):
        with self.assertRaises(block_semantics.BlockSemanticRepairRequired) as caught:
            block_semantics.validate(html('Weitere Aspekte zum Thema'),contract())
        findings=caught.exception.findings
        self.assertEqual(findings[0]['error_code'],'BLOCK_CONTENT_SEMANTIC_HEADING_MISMATCH')
        request=global_workshop.build_request('FULLCHECK',caught.exception,findings=findings)
        self.assertTrue(request['repairable'])
        state={'checks':{'findings':findings},'last_error':findings[0]['error_code']}
        route=repair_router.classify(state)
        self.assertEqual((route['owner'],route['target']),('DRAFT_BODY','SAME_ARTICLE_BODY'))

    def test_missing_and_wrong_order_are_structured_repairable_content_findings(self):
        missing_html=html(order=['intro','body','further_information'])
        with self.assertRaises(block_semantics.BlockSemanticRepairRequired) as caught:
            block_semantics.validate(missing_html,contract())
        self.assertIn('BLOCK_CONTENT_REQUIRED_BLOCK_ABSENT',[row['error_code'] for row in caught.exception.findings])
        request=global_workshop.build_request('DRAFT_BLOCK_SEMANTICS',caught.exception,findings=caught.exception.findings)
        self.assertTrue(request['repairable'])

        with self.assertRaises(block_semantics.BlockSemanticRepairRequired) as caught_order:
            block_semantics.validate(html(order=['intro','body','further_information','conclusion']),contract())
        self.assertIn('BLOCK_CONTENT_BLOCK_ORDER_INVALID',[row['error_code'] for row in caught_order.exception.findings])

    def test_ppm_reserved_heading_is_authority_anchor(self):
        with self.assertRaisesRegex(block_semantics.BlockSemanticError,'PPM_RESERVED_HEADING_BINDING_MISSING:conclusion'):
            block_semantics.bind(
                {'headings':{'reserved_headings':['Weiterführende Informationen']}},
                {'required_blocks':['intro','conclusion','further_information']},
            )


if __name__=='__main__':
    unittest.main()
