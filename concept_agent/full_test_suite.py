"""Ein Einstieg für die vollständige isolierte Concept-Agent-Teststrecke."""
import unittest
from pathlib import Path

BASE=Path(__file__).resolve().parent
suite=unittest.defaultTestLoader.discover(str(BASE/"tests"),pattern="test_*.py")
result=unittest.TextTestRunner(verbosity=2).run(suite)
raise SystemExit(0 if result.wasSuccessful() else 1)
