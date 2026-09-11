# SYSTEM 4 ISOLATION — TEST ONLY

Scope: only `isolated_system4/**` repository code.

- Do not modify anything outside `isolated_system4/`.
- Do not import/copy/wrap runtime, workers, gates, handoffs, signers, contracts or state machines from concepts 1–3.
- Historical systems may be read only as inspiration/negative evidence.
- No merge, no production, no publish.
- Runtime workspaces and generated article/output files must live in a temporary directory outside the repository unless the bound task explicitly requires otherwise.
- Allowed tasks:
  1. architecture live test via `live_test.py`;
  2. first generated article test exactly per `FIRST_ARTICLE_TASK.md`.
- For a generated article, Codex may create research/facts/draft only in the temporary workspace and may repair only the same draft when the controller returns `REPAIR_REQUIRED`.
- Codex may not alter metadata, route, controller, checks or publish status during the run.
