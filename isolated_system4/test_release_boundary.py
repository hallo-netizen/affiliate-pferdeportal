import unittest
from pathlib import Path

import release_adapter


class ReleaseBoundaryTests(unittest.TestCase):
    def test_single_article_prepare_is_hard_blocked(self):
        with self.assertRaisesRegex(
            release_adapter.ReleaseError,
            "PER_ARTICLE_FULL_PRODUCTION_RELEASE_FORBIDDEN_USE_BATCH_GATE",
        ):
            release_adapter.build_unsigned({}, Path("unused"))

    def test_single_article_finalize_is_hard_blocked(self):
        with self.assertRaisesRegex(
            release_adapter.ReleaseError,
            "PER_ARTICLE_SIGNED_FINALIZE_FORBIDDEN_USE_BATCH_GATE",
        ):
            release_adapter.finalize_signed({}, {}, Path("unused.json"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
