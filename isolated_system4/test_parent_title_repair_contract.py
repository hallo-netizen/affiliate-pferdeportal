import copy
import unittest

import parent_owner_repair


BASE = {
    'title': 'Pferdeanhänger vor der Fahrt kontrollieren: Checkliste für einen sicheren Transport',
    'target_keyword': 'Pferdeanhänger',
    'category': 'pferdeanhaenger-beratung',
    'article_type': 'Beratung',
    'plan_slot': 'a' * 64,
}


class ParentTitleRepairContractTests(unittest.TestCase):
    def test_colon_rule_repairs_only_title(self):
        before = copy.deepcopy(BASE)
        result = parent_owner_repair.repair_item(
            BASE,
            {
                'error_code': 'BLOCKED_CONTENT_TITLE_COLON',
                'failed_rule': 'ARTICLE_TITLE_MUST_NOT_CONTAIN_COLON',
                'field_path': 'content.title',
                'repair_owner': 'PARENT_TITLE_MACHINE',
            },
        )
        self.assertEqual(result['owner'], 'PARENT_TITLE_MACHINE')
        self.assertEqual(result['changed_fields'], ['title'])
        self.assertNotIn(':', result['item']['title'])
        self.assertIn(before['target_keyword'], result['item']['title'])
        for key in ('target_keyword', 'category', 'article_type', 'plan_slot'):
            self.assertEqual(result['item'][key], before[key])
        self.assertEqual(BASE, before, 'input item must not be mutated in place')

    def test_faq_question_mark_is_deterministic(self):
        item = dict(BASE, article_type='FAQ', title='Was muss vor der Fahrt mit Pferdeanhänger geprüft werden')
        result = parent_owner_repair.repair_item(item, {
            'error_code': 'BLOCKED_CONTENT_FAQ_TITLE_QUESTION_MARK',
            'failed_rule': 'FAQ_TITLE_MUST_END_WITH_QUESTION_MARK',
            'field_path': 'content.title',
            'repair_owner': 'PARENT_TITLE_MACHINE',
        })
        self.assertEqual(result['item']['title'], item['title'] + '?')

    def test_missing_keyword_is_added_without_forbidden_colon(self):
        item = dict(BASE, title='Checkliste für einen sicheren Transport')
        result = parent_owner_repair.repair_item(item, {
            'error_code': 'BLOCKED_CONTENT_TARGET_KEYWORD_TITLE',
            'failed_rule': 'TITLE_MUST_CONTAIN_TARGET_KEYWORD',
            'field_path': 'content.title',
            'repair_owner': 'PARENT_TITLE_MACHINE',
        })
        self.assertIn(item['target_keyword'], result['item']['title'])
        self.assertNotIn(':', result['item']['title'])

    def test_wrong_owner_is_hard_block(self):
        with self.assertRaisesRegex(parent_owner_repair.ParentOwnerRepairError, 'OWNER_MISMATCH'):
            parent_owner_repair.repair_item(BASE, {
                'error_code': 'BLOCKED_CONTENT_TITLE_COLON',
                'field_path': 'content.title',
                'repair_owner': 'DRAFT_WORKER',
            })

    def test_unknown_title_rule_is_hard_block(self):
        with self.assertRaisesRegex(parent_owner_repair.ParentOwnerRepairError, 'TITLE_RULE_UNSUPPORTED'):
            parent_owner_repair.repair_item(BASE, {
                'error_code': 'BLOCKED_FUTURE_TITLE_RULE',
                'field_path': 'content.title',
                'repair_owner': 'PARENT_TITLE_MACHINE',
            })

    def test_invalid_result_is_hard_block(self):
        item = dict(BASE, target_keyword='Pferdeanhänger: Spezial')
        with self.assertRaises(parent_owner_repair.ParentOwnerRepairError):
            parent_owner_repair.repair_item(item, {
                'error_code': 'BLOCKED_CONTENT_TARGET_KEYWORD_TITLE',
                'field_path': 'content.title',
                'repair_owner': 'PARENT_TITLE_MACHINE',
            })


if __name__ == '__main__':
    unittest.main(verbosity=2)
