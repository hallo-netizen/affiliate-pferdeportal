# SYSTEM 4 ISOLATION — TEST ONLY

Scope: System 4 implementation only under `isolated_system4/**`.

- Do not modify anything outside `isolated_system4/`.
- Do not import/copy/wrap runtime, workers, gates, handoffs, signers, contracts or state machines from concepts 1–3.
- Historical systems may be read only as inspiration/negative evidence.
- No merge, no production, no publish.
- Runtime workspaces and generated article/output files must live in a temporary directory outside the repository unless the bound task explicitly requires otherwise.
- Allowed tasks:
  1. architecture live test via `live_test.py`;
  2. first generated article test exactly per `FIRST_ARTICLE_TASK.md`;
  3. first full-rule article test exactly per `FULL_RULE_ARTICLE_TASK.md`.
- For task 3 only, repository files outside `isolated_system4/**` may be read solely to identify current authoritative rule/specification content and pure tool/checker inputs. They may not be modified or used as old orchestration/runtime dependencies.
- For generated articles, Codex may create research/facts/draft only in the temporary workspace and may repair only the same draft when the controller returns a repairable FAIL.
- Codex may not alter immutable metadata, choose a free route, enable publish, or bypass a required checker.
