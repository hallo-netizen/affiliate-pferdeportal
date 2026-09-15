from __future__ import annotations

import unittest
import parent_owner_repair


class ParentMetadataOwnerAuthorityContractTests(unittest.TestCase):
    """Owner return is only valid when a machine authority can deterministically rebuild its field.

    These are deliberately RED until the upstream machine owns an authoritative source/rebuild
    rule for category, article type, target keyword and plan slot. Copying an expected value from
    a downstream validator finding is forbidden because that would turn the validator into an author.
    """

    BASE = {
        'title': 'Pferdeanhänger vor der Fahrt kontrollieren',
        'target_keyword': 'Pferdeanhänger kontrollieren',
        'category': 'pferdeanhaenger-beratung',
        'article_type': 'Beratung',
        'plan_slot': '9c229b0e6a784a482575e3deb16d105e3b5355becbbbb8ecfc8e1f600b529c56',
    }

    def _assert_machine_authority(self, owner: str, field: str, error_code: str) -> None:
        item = dict(self.BASE)
        finding = {
            'repair_owner': owner,
            'error_code': error_code,
            'failed_rule': 'REAL_DOWNSTREAM_VALIDATOR',
            'field_path': 'content.' + field,
            # No expected/correct value is supplied on purpose. The producing machine must own it.
        }
        result = parent_owner_repair.repair_item(item, finding)
        self.assertEqual(result['owner'], owner)
        self.assertEqual(result['changed_fields'], [field])
        self.assertNotEqual(result['item'][field], item[field])
        for key in self.BASE:
            if key != field:
                self.assertEqual(result['item'][key], item[key])

    def test_category_owner_has_real_machine_authority(self):
        self._assert_machine_authority('PARENT_CATEGORY_MACHINE', 'category', 'BLOCKED_CATEGORY_INVALID')

    def test_article_type_owner_has_real_machine_authority(self):
        self._assert_machine_authority('PARENT_ARTICLE_TYPE_MACHINE', 'article_type', 'BLOCKED_ARTICLE_TYPE_INVALID')

    def test_keyword_owner_has_real_machine_authority(self):
        self._assert_machine_authority('PARENT_KEYWORD_MACHINE', 'target_keyword', 'BLOCKED_TARGET_KEYWORD_INVALID')

    def test_slot_owner_has_real_machine_authority(self):
        self._assert_machine_authority('PARENT_SLOT_MACHINE', 'plan_slot', 'BLOCKED_PLAN_SLOT_INVALID')

    def test_downstream_expected_value_cannot_be_used_as_authority(self):
        item = dict(self.BASE)
        finding = {
            'repair_owner': 'PARENT_CATEGORY_MACHINE',
            'error_code': 'BLOCKED_CATEGORY_INVALID',
            'field_path': 'content.category',
            'expected': 'validator-provided-category-must-not-be-copied',
        }
        with self.assertRaisesRegex(parent_owner_repair.ParentOwnerRepairError, 'VALIDATOR_EXPECTED_VALUE_NOT_AUTHORITY'):
            parent_owner_repair.repair_item(item, finding)


if __name__ == '__main__':
    unittest.main(verbosity=2)
