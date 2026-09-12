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

    def test_parent_chat_handoff_is_direct_inline_and_wordpress_ready(self):
        task=(ROOT/'FULL_RULE_BATCH_TASK.md').read_text(encoding='utf-8')
        agents=(ROOT/'AGENTS.md').read_text(encoding='utf-8')
        for value in [
            'SYSTEM4_7_ARTICLE_CHAT_HANDOFF_V1.json',
            'WORDPRESS_DIRECT_IMPORT',
            'direct_wordpress_upload_ready=true',
            'direct_upload_block_reason=null',
            'required_downstream_components=[]',
            'inline-pack',
            'inline-unpack',
            'SYSTEM4_PARENT_CHAT_INLINE_V1',
            'The parent Chat exposes it unchanged as one download',
            'No signature step and no second WordPress transformation occur in between.',
        ]: self.assertIn(value,task)
        for forbidden in [
            'system4-parent-chat-handoff',
            'write ONLY `isolated_system4/.handoff/',
            'push that transport branch',
        ]: self.assertNotIn(forbidden,task)
        for value in [
            'DIRECT PARENT-CHAT FILE HANDOFF HARD RULE',
            'No repository branch, commit, push, artifact, PR-file or external storage is part of the file handoff.',
            'inline-pack',
            'inline-unpack',
            'WORDPRESS_DIRECT_IMPORT',
            'direct_wordpress_upload_ready=true',
            'The user must never be asked to download anything from GitHub or from the Codex task UI.',
            'System 4 MUST NOT modify the WordPress plugin or its signature switch.',
        ]: self.assertIn(value,agents)

    def test_known_bad_ad_hoc_abort_is_not_in_bound_task(self):
        task=(ROOT/'FULL_RULE_BATCH_TASK.md').read_text(encoding='utf-8')
        self.assertNotIn('LT_PREFLIGHT_FINDINGS',task)
        self.assertNotIn('LT_FINDINGS_PRE_CONTEXT',task)
        self.assertNotIn('raise RuntimeError',task)

if __name__=='__main__': unittest.main(verbosity=2)
