# SYSTEM 3 CODEX CLOUD ENTRANCE

This repository state is a test-only isolated System 3 workspace.

Hard rules:
- First run exactly `python3 isolated_system3/cloud_entry.py start`.
- Only if that returns `SYSTEM3_CLOUD_ENTRY_PASS`, continue.
- Work only with `isolated_system3/**`.
- Do not inspect Git history, refs, remotes, APIs, `.git` contents, or any other repository path.
- Do not choose workflow steps, tools, repairs, or alternate routes.
- Read `isolated_system3/codex_prompt.md` and `isolated_system3/live_fixture/wordpress_input.json` only for the requested article task.
- Create only `isolated_system3/codex_output.md` when explicitly requested.
- Never write to WordPress or any external publication target.
- Before completion run exactly `python3 isolated_system3/cloud_entry.py verify`.
- If any required input is missing or any forbidden path is needed, fail closed.
