from __future__ import annotations

import copy
import hashlib
import json
import unittest

import parent_owner_repair


class ParentMetadataOwnerAuthorityContractTests(unittest.TestCase):
    BASE = {
        'title': 'Pferdeanhänger vor der Fahrt kontrollieren',
        'target_keyword': 'Pferdeanhänger kontrollieren',
        'category': 'pferdeanhaenger-beratung',
        'article_type': 'Beratung',
        'plan_slot': '9c229b0e6a784a482575e3deb16d105e3b5355becbbbb8ecfc8e1f600b529c56',
    }

    def _projection(self) -> tuple[bytes, str]:
        value = {
            'contract': 'PFERDE_ATELIER_RUNTIME_SNAPSHOT_PROJECTION_V1',
            'source_snapshot_filename': 'seo-redaktionsplan-metadaten-snapshot-test.json',
            'source_snapshot_sha256': 'a' * 64,
            'manifest_sha256': 'b' * 64,
            'next_textmachine_metadata_batch': {
                'contract': 'PSERC_TEXTMACHINE_METADATA_BATCH_V2',
                'status': 'READY_FOR_TEXTMACHINE_METADATA_INTAKE',
                'item_count': 1,
                'publish_allowed': False,
                'items': [copy.deepcopy(self.BASE)],
                'batch_sha256': 'c' * 64,
            },
        }
        raw = (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')) + '\n').encode('utf-8')
        return raw, hashlib.sha256(raw).hexdigest()

    def _restore_drift(self, owner: str, field: str, error_code: str, bad_value: str) -> dict:
        raw, digest = self._projection()
        item = dict(self.BASE)
        item[field] = bad_value
        finding = {
            'repair_owner': owner,
            'error_code': error_code,
            'failed_rule': 'REAL_DOWNSTREAM_VALIDATOR',
            'field_path': 'content.' + field,
            'expected': 'MALICIOUS_VALIDATOR_VALUE_MUST_BE_IGNORED',
        }
        result = parent_owner_repair.repair_item(
            item,
            finding,
            authority_projection_bytes=raw,
            authority_projection_sha256=digest,
            item_index=0,
        )
        self.assertEqual(result['owner'], owner)
        self.assertEqual(result['changed_fields'], [field])
        self.assertEqual(result['authority'], 'HASH_BOUND_UPSTREAM_METADATA_PROJECTION')
        self.assertEqual(result['item'][field], self.BASE[field])
        self.assertNotEqual(result['item'][field], finding['expected'])
        for key in self.BASE:
            if key != field:
                self.assertEqual(result['item'][key], item[key])
        return result

    def test_category_drift_is_restored_only_from_bound_projection(self):
        self._restore_drift('PARENT_CATEGORY_MACHINE', 'category', 'BLOCKED_CATEGORY_INVALID', 'wrong-category')

    def test_article_type_drift_is_restored_only_from_bound_projection(self):
        self._restore_drift('PARENT_ARTICLE_TYPE_MACHINE', 'article_type', 'BLOCKED_ARTICLE_TYPE_INVALID', 'FalscherTyp')

    def test_keyword_drift_is_restored_only_from_bound_projection(self):
        self._restore_drift('PARENT_KEYWORD_MACHINE', 'target_keyword', 'BLOCKED_TARGET_KEYWORD_INVALID', 'Falsches Keyword')

    def test_slot_drift_is_restored_only_from_bound_projection(self):
        self._restore_drift('PARENT_SLOT_MACHINE', 'plan_slot', 'BLOCKED_PLAN_SLOT_INVALID', 'd' * 64)

    def test_projection_itself_invalid_requires_upstream_editorial_rebuild(self):
        raw, digest = self._projection()
        finding = {
            'repair_owner': 'PARENT_CATEGORY_MACHINE',
            'error_code': 'BLOCKED_CATEGORY_INVALID',
            'field_path': 'content.category',
            'expected': 'validator-provided-category-must-not-be-copied',
        }
        with self.assertRaisesRegex(parent_owner_repair.ParentOwnerRepairError, 'UPSTREAM_METADATA_SOURCE_REBUILD_REQUIRED:category'):
            parent_owner_repair.repair_item(
                dict(self.BASE),
                finding,
                authority_projection_bytes=raw,
                authority_projection_sha256=digest,
                item_index=0,
            )

    def test_missing_or_wrong_projection_hash_is_fail_closed(self):
        raw, digest = self._projection()
        item = dict(self.BASE)
        item['category'] = 'wrong-category'
        finding = {'repair_owner': 'PARENT_CATEGORY_MACHINE', 'error_code': 'BLOCKED_CATEGORY_INVALID', 'field_path': 'content.category'}
        with self.assertRaisesRegex(parent_owner_repair.ParentOwnerRepairError, 'UPSTREAM_METADATA_SOURCE_REQUIRED'):
            parent_owner_repair.repair_item(item, finding, item_index=0)
        with self.assertRaisesRegex(parent_owner_repair.ParentOwnerRepairError, 'UPSTREAM_METADATA_SOURCE_HASH_MISMATCH'):
            parent_owner_repair.repair_item(
                item,
                finding,
                authority_projection_bytes=raw,
                authority_projection_sha256='f' * 64,
                item_index=0,
            )

    def test_non_owner_metadata_mismatch_is_fail_closed(self):
        raw, digest = self._projection()
        item = dict(self.BASE)
        item['category'] = 'wrong-category'
        item['target_keyword'] = 'also changed'
        finding = {'repair_owner': 'PARENT_CATEGORY_MACHINE', 'error_code': 'BLOCKED_CATEGORY_INVALID', 'field_path': 'content.category'}
        with self.assertRaisesRegex(parent_owner_repair.ParentOwnerRepairError, 'UPSTREAM_METADATA_NON_OWNER_MISMATCH:target_keyword'):
            parent_owner_repair.repair_item(
                item,
                finding,
                authority_projection_bytes=raw,
                authority_projection_sha256=digest,
                item_index=0,
            )


if __name__ == '__main__':
    unittest.main(verbosity=2)
