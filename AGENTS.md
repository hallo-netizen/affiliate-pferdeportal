# SYSTEM 4 — ISOLATED CODEX TEST ENTRANCE

This branch exists only for the isolated System 4 prototype test.

Before any repository-wide workflow, STARTMASTER, capsule, production preflight, handoff or legacy gate: do not execute them on this branch.

Codex may operate only inside `isolated_system4/**` and must follow `isolated_system4/AGENTS.md`.

For the first live test execute exactly:

`python3 isolated_system4/live_test.py isolated_system4/live_fixture/wordpress_snapshot.json`

Rules:
- no modification outside `isolated_system4/**`;
- no import/copy/wrap/reuse of runtime, handoffs, workers, gates, signers, contracts or state machines from concepts 1–3;
- no merge;
- no production;
- no publish;
- if the command fails, return the first actual System 4 blocker and stop;
- if it passes, return complete stdout and terminal PASS only.

This branch-specific entrance is test isolation only. It does not change `main` or any productive workflow.
