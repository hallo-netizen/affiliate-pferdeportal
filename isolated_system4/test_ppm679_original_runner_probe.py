from __future__ import annotations

import unittest

import ppm679_original_runner_probe as probe


class Ppm679OriginalRunnerProbeTests(unittest.TestCase):
    def test_exact_package_exposes_original_runner_and_bootstrap_context(self):
        self.assertEqual(probe.main(),0)


if __name__=='__main__': unittest.main(verbosity=2)
