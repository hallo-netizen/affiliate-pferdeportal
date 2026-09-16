import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent


class CodexEconomyContractTests(unittest.TestCase):
    def test_batch_task_forbids_duplicate_checker_orchestration(self):
        task = (ROOT / 'FULL_RULE_BATCH_TASK.md').read_text(encoding='utf-8')
        required = [
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
        for value in required:
            self.assertIn(value, task)
        self.assertIn('publish_allowed=false', task)
        self.assertIn('actual PPM 6.7.9 content validator', task)
        self.assertIn('real fail-closed LanguageTool 6.8', task)

    def test_agents_bind_same_repair_behavior_and_codex_economy(self):
        agents = (ROOT / 'AGENTS.md').read_text(encoding='utf-8')
        required = [
            '`isolated_system4/controller.py fullcheck` is the ONLY production checker orchestrator.',
            'LanguageTool 6.8 and PPM 6.7.9 must be invoked only through that bound `fullcheck` path via `production_checks.run_all` for the real article corridor.',
            'A repairable LanguageTool/PPM/content finding is NOT a terminal process error.',
            'controller.py repair',
            'The repair transition must not mutate the bound production context',
            'A Codex production run MUST NOT repeat that unchanged-head preflight.',
        ]
        for value in required:
            self.assertIn(value, agents)

    def test_textmaschine_and_design_are_hard_read_only(self):
        task = (ROOT / 'FULL_RULE_BATCH_TASK.md').read_text(encoding='utf-8')
        agents = (ROOT / 'AGENTS.md').read_text(encoding='utf-8')
        for value in [
            'TEXTMASCHINE + DESIGN ARE IMMUTABLE',
            'Textmaschine/content-rule authority is READ-ONLY.',
            'PPM 6.7.9 package/rules, current table contract, PSERC/PSTE rule inputs, WordPress plugin, theme/CSS and design selectors are READ-ONLY.',
            '`design_guard.py` performs PASS/BLOCK only and ZERO mutation.',
            'BLOCKED_TEXTMASCHINE_OR_DESIGN_IMMUTABLE',
            'No Textmaschine-rule changes. No design changes.',
        ]:
            self.assertIn(value, task)
        for value in [
            'TEXTMASCHINE + DESIGN IMMUTABILITY HARD RULE',
            'The existing Textmaschine/content-rule authority is READ-ONLY.',
            'Existing design is equally immutable.',
            '`design_guard.py` is validation-only.',
            'System 4 MUST NOT write CSS',
            'BLOCKED_TEXTMASCHINE_OR_DESIGN_IMMUTABLE',
        ]:
            self.assertIn(value, agents)

    def test_universal_batch_and_article_type_contract_is_hard_bound(self):
        task = (ROOT / 'FULL_RULE_BATCH_TASK.md').read_text(encoding='utf-8')
        agents = (ROOT / 'AGENTS.md').read_text(encoding='utf-8')
        target = (ROOT / 'ZIELVERTRAG_SYSTEM4_MACHINE_POINT0_WORKER_DISPATCH_20260916.md').read_text(encoding='utf-8')
        for text in (task, agents, target):
            self.assertNotIn('SYSTEM4_7_ARTICLE_CHAT_HANDOFF_V1', text)
            self.assertNotIn('SYSTEM4_7_7_REAL_ARTICLE_BATCH_PASS', text)
        self.assertIn('NO fixed article count', task)
        self.assertIn('NO artificial maximum count', task)
        self.assertIn('NO `Beratung` allowlist', task)
        self.assertIn('NO fixed article count', agents)
        self.assertIn('NO artificial maximum count', agents)
        self.assertIn('1..N', target)
        self.assertIn('ohne künstliche System-4-Obergrenze', target)
        self.assertIn('keine System-4-Whitelist', target)

    def test_current_handoff_contract_has_one_truth(self):
        task = (ROOT / 'FULL_RULE_BATCH_TASK.md').read_text(encoding='utf-8')
        agents = (ROOT / 'AGENTS.md').read_text(encoding='utf-8')
        target = (ROOT / 'ZIELVERTRAG_SYSTEM4_MACHINE_POINT0_WORKER_DISPATCH_20260916.md').read_text(encoding='utf-8')
        transport = (ROOT / 'handoff_transport.py').read_text(encoding='utf-8')

        for text in (task, agents, target):
            self.assertIn('SYSTEM4_WORDPRESS_HANDOFF_V1', text)
            self.assertIn('SYSTEM4_WORDPRESS_HANDOFF_V1.json', text)
            self.assertIn('SYSTEM4_PARENT_CHAT_INLINE_V2', text)

        self.assertNotIn('SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2', task)
        self.assertNotIn('SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2', target)
        self.assertIn("HANDOFF_CONTRACT='SYSTEM4_WORDPRESS_HANDOFF_V1'", transport)
        self.assertIn("INLINE_CONTRACT='SYSTEM4_PARENT_CHAT_INLINE_V2'", transport)
        self.assertIn("HANDOFF_FILENAME='SYSTEM4_WORDPRESS_HANDOFF_V1.json'", transport)
        self.assertIn('transport only', transport)
        self.assertIn('nicht der finale WordPress-Dateivertrag', target)
        self.assertIn('transport only and is not the final WordPress file contract', agents)

    def test_parent_chat_handoff_is_direct_inline_and_wordpress_ready(self):
        task = (ROOT / 'FULL_RULE_BATCH_TASK.md').read_text(encoding='utf-8')
        agents = (ROOT / 'AGENTS.md').read_text(encoding='utf-8')
        for value in [
            'SYSTEM4_WORDPRESS_HANDOFF_V1.json',
            'WORDPRESS_DIRECT_IMPORT',
            'direct_wordpress_upload_ready=true',
            'direct_upload_block_reason=null',
            'required_downstream_components=[]',
            'inline-pack',
            'inline-unpack',
            'SYSTEM4_PARENT_CHAT_INLINE_V2',
            'The parent Chat exposes it unchanged as one download',
            'No signature step, no design transformation and no second WordPress transformation occur in between.',
        ]:
            self.assertIn(value, task)
        for forbidden in [
            'SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2',
            'system4-parent-chat-handoff',
            'write ONLY `isolated_system4/.handoff/',
            'push that transport branch',
        ]:
            self.assertNotIn(forbidden, task)
        for value in [
            'DIRECT PARENT-CHAT FILE HANDOFF HARD RULE',
            'No repository branch, commit, push, artifact, PR-file or external storage by itself satisfies the terminal file-handoff criterion.',
            'inline-pack',
            'inline-unpack',
            'SYSTEM4_WORDPRESS_HANDOFF_V1',
            'direct_wordpress_upload_ready',
            'The user must never be asked to treat a GitHub Actions artifact, repository file, internal temp path or hash as the completed parent-chat delivery.',
            'System 4 MUST NOT modify the WordPress plugin or its signature switch as part of acceptance.',
        ]:
            self.assertIn(value, agents)

    def test_known_bad_ad_hoc_abort_is_not_in_bound_task(self):
        task = (ROOT / 'FULL_RULE_BATCH_TASK.md').read_text(encoding='utf-8')
        self.assertNotIn('LT_PREFLIGHT_FINDINGS', task)
        self.assertNotIn('LT_FINDINGS_PRE_CONTEXT', task)
        self.assertNotIn('raise RuntimeError', task)


if __name__ == '__main__':
    unittest.main(verbosity=2)
