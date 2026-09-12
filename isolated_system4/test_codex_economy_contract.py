import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parent
class CodexEconomyContractTests(unittest.TestCase):
    def test_batch_task_forbids_duplicate_checker_orchestration(self):
        task=(ROOT/'FULL_RULE_BATCH_TASK.md').read_text(encoding='utf-8')
        required=[
            '`controller.py fullcheck` is the ONLY checker orchestrator.',
            'Do NOT call LanguageTool 6.8 directly.',
            'Do NOT call PPM 6.7.9 directly.',
            'Do NOT create or execute custom orchestration scripts/wrappers',
            'A normal LT/PPM/content finding must travel through the controller as `REPAIR_REQUIRED`',
            'Do not restart already-passed articles.',
            'The production Codex task MUST NOT rerun the unchanged-head unittest/NO-LEGACY preflight',
            '`controller.py repair`',
            '`controller.py draft` is forbidden in `REPAIR_REQUIRED`',
        ]
        for value in required: self.assertIn(value,task)
        self.assertIn('publish_allowed=false',task)
        self.assertIn('actual PPM 6.7.9 content validator',task)
        self.assertIn('real fail-closed LanguageTool 6.8',task)
    def test_agents_bind_same_repair_behavior_and_codex_economy(self):
        agents=(ROOT/'AGENTS.md').read_text(encoding='utf-8')
        required=[
            '`isolated_system4/controller.py fullcheck` is the ONLY production checker orchestrator.',
            'Do NOT run LanguageTool or PPM directly before/after `fullcheck`.',
            'A repairable LanguageTool/PPM/content finding is NOT a terminal process error.',
            'controller.py repair',
            'The repair transition must not mutate the bound production context',
            'A Codex production run MUST NOT repeat that unchanged-head preflight.',
        ]
        for value in required: self.assertIn(value,agents)
    def test_known_bad_ad_hoc_abort_is_not_in_bound_task(self):
        task=(ROOT/'FULL_RULE_BATCH_TASK.md').read_text(encoding='utf-8')
        self.assertNotIn('LT_PREFLIGHT_FINDINGS',task)
        self.assertNotIn('LT_FINDINGS_PRE_CONTEXT',task)
        self.assertNotIn('raise RuntimeError',task)
if __name__=='__main__': unittest.main(verbosity=2)
