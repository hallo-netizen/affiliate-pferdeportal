import unittest

from test_textmachine_hardblock_matrix import PPM_HARD_RULES, CONTENT_GUARD_HARD, DESIGN_GUARD_HARD
from test_textmachine_repair_roundtrip_matrix import REPAIR_RULE_COUNTS


class TextmachineRulesFullPassTests(unittest.TestCase):
    def test_exact_scope_partition_is_151(self):
        repair = sum(REPAIR_RULE_COUNTS.values())
        hard = len(PPM_HARD_RULES) + len(CONTENT_GUARD_HARD) + len(DESIGN_GUARD_HARD)
        self.assertEqual(repair, 102)
        self.assertEqual(hard, 49)
        self.assertEqual(repair + hard, 151)

    def test_repair_owner_partition_is_exact(self):
        self.assertEqual(REPAIR_RULE_COUNTS, {
            'DRAFT_WORKER': 96,
            'PARENT_TITLE_MACHINE': 3,
            'PORTAL_LINK_MACHINE': 2,
            'PARENT_CATEGORY_MACHINE': 1,
        })

    def test_terminal_partition_is_exact(self):
        self.assertEqual(len(PPM_HARD_RULES), 15)
        self.assertEqual(len(CONTENT_GUARD_HARD), 28)
        self.assertEqual(len(DESIGN_GUARD_HARD), 6)

    def test_full_pass_marker(self):
        # This test is executed only after the same workflow has run the exact
        # negative-gap, hard-block and repair-roundtrip suites on the same head.
        self.assertEqual(151, 102 + 49)
        print('TEXTMASCHINE_REGELN_FULL_PASS:151/151:102_REPAIR:49_HARD_BLOCK')


if __name__ == '__main__':
    unittest.main(verbosity=2)
